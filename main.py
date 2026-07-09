import ctypes
import psutil
import time
import math
from ctypes import wintypes
import win32api
import win32con
from win32gui import FindWindow, GetWindowThreadProcessId
from win10toast import ToastNotifier

# Offsets de memória do AssaultCube
PLAYER_OFFSET = 0x0010F4F4
ENEMIES_OFFSET = 0x0010F4F8
MAX_PLAYERS = 128

# Estrutura do jogador
class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class PlayerInfo:
    def __init__(self):
        self.position = Vector3()
        self.head_position = Vector3()
        self.health = 0
        self.is_crouching = False
        self.team = 0
        self.alive = True

def get_assaultcube_pid():
    """Encontra o PID do AssaultCube"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'cube' in proc.name().lower() or 'assaultcube' in proc.name().lower():
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def send_notification(title, message):
    """Envia notificação do Windows"""
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=5)

def read_memory(process_handle, address, value_type):
    """Lê valor da memória"""
    try:
        if value_type == 'float':
            buf = ctypes.c_float()
        elif value_type == 'int':
            buf = ctypes.c_int()
        elif value_type == 'byte':
            buf = ctypes.c_byte()
        else:
            return None
        
        ctypes.windll.kernel32.ReadProcessMemory(
            process_handle,
            address,
            ctypes.byref(buf),
            ctypes.sizeof(buf),
            None
        )
        return buf.value
    except Exception as e:
        print(f"Erro ao ler memória: {e}")
        return None

def write_memory(process_handle, address, value, value_type):
    """Escreve valor na memória"""
    try:
        if value_type == 'float':
            buf = ctypes.c_float(value)
        elif value_type == 'int':
            buf = ctypes.c_int(value)
        elif value_type == 'byte':
            buf = ctypes.c_byte(value)
        else:
            return False
        
        ctypes.windll.kernel32.WriteProcessMemory(
            process_handle,
            address,
            ctypes.byref(buf),
            ctypes.sizeof(buf),
            None
        )
        return True
    except Exception as e:
        print(f"Erro ao escrever na memória: {e}")
        return False

def get_player_info(process_handle, player_index):
    """Obtém informações do jogador"""
    player_ptr = PLAYER_OFFSET + (player_index * 0x4)
    
    player = PlayerInfo()
    player.position.x = read_memory(process_handle, player_ptr, 'float')
    player.position.y = read_memory(process_handle, player_ptr + 0x4, 'float')
    player.position.z = read_memory(process_handle, player_ptr + 0x8, 'float')
    
    # Cabeça está 1.7 unidades acima do centro do corpo
    player.head_position.x = player.position.x
    player.head_position.y = player.position.y
    player.head_position.z = player.position.z + 1.7
    
    player.health = read_memory(process_handle, player_ptr + 0xF8, 'int')
    player.is_crouching = read_memory(process_handle, player_ptr + 0x21C, 'byte')
    player.team = read_memory(process_handle, player_ptr + 0x30, 'byte')
    player.alive = player.health > 0
    
    return player

def get_closest_enemy(process_handle, player_team, player_pos):
    """Encontra o inimigo mais próximo com verificações"""
    closest_distance = float('inf')
    closest_enemy = None
    
    for i in range(1, MAX_PLAYERS):  # Começa em 1 (0 é o jogador)
        enemy = get_player_info(process_handle, i)
        
        # Verificações
        if not enemy.alive:  # Dead check
            continue
        
        if enemy.team == player_team:  # Team check
            continue
        
        if enemy.health <= 0:  # Health check
            continue
        
        # Calcula distância
        dx = enemy.head_position.x - player_pos.x
        dy = enemy.head_position.y - player_pos.y
        dz = enemy.head_position.z - player_pos.z
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        if distance < closest_distance:
            # TODO: Wall check aqui (raycasting)
            closest_distance = distance
            closest_enemy = enemy
    
    return closest_enemy

def calculate_aim_angles(player_pos, target_pos):
    """Calcula ângulos de mira para o alvo"""
    dx = target_pos.x - player_pos.x
    dy = target_pos.y - player_pos.y
    dz = target_pos.z - player_pos.z
    
    # Yaw (horizontal)
    yaw = math.atan2(dy, dx)
    
    # Pitch (vertical)
    distance_xz = math.sqrt(dx*dx + dy*dy)
    pitch = math.atan2(dz, distance_xz)
    
    return yaw, pitch

def snap_to_enemy(process_handle, player, enemy):
    """Faz o snap da mira para a cabeça do inimigo"""
    yaw, pitch = calculate_aim_angles(player.position, enemy.head_position)
    
    # Offsets da câmera/mira (ajustar conforme necessário)
    camera_yaw_offset = 0x0010F4F4 + 0x40  # Ajustar offset real
    camera_pitch_offset = 0x0010F4F4 + 0x44
    
    write_memory(process_handle, camera_yaw_offset, yaw, 'float')
    write_memory(process_handle, camera_pitch_offset, pitch, 'float')
    
    print(f"🎯 Snap realizado! Yaw: {math.degrees(yaw):.2f}° Pitch: {math.degrees(pitch):.2f}°")

def main():
    print("⏳ Aguardando AssaultCube...")
    
    # Aguarda AssaultCube abrir
    pid = None
    while pid is None:
        pid = get_assaultcube_pid()
        time.sleep(1)
    
    # Notifica PID
    send_notification("Freestyle Headshot AC", f"AssaultCube detectado! PID: {pid}")
    print(f"✅ AssaultCube encontrado! PID: {pid}")
    
    # Abre handle do processo
    PROCESS_VM_READ = 0x0010
    PROCESS_VM_WRITE = 0x0020
    PROCESS_VM_OPERATION = 0x0008
    
    process_handle = ctypes.windll.kernel32.OpenProcess(
        PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION,
        False,
        pid
    )
    
    if not process_handle:
        print("❌ Erro ao abrir o processo!")
        return
    
    print("🎮 Aimbot ativado! Agache para usar o snap.")
    
    try:
        while True:
            # Obtém informações do jogador principal (índice 0)
            player = get_player_info(process_handle, 0)
            
            # Se o jogador agachar
            if player.is_crouching:
                # Encontra o inimigo mais próximo
                enemy = get_closest_enemy(process_handle, player.team, player.position)
                
                if enemy:
                    snap_to_enemy(process_handle, player, enemy)
            
            time.sleep(0.01)  # 10ms entre verificações
    
    except KeyboardInterrupt:
        print("\n❌ Aimbot desativado!")
    finally:
        ctypes.windll.kernel32.CloseHandle(process_handle)

if __name__ == "__main__":
    main()
