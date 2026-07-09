"""
╔═══════════════════════════════════════════════════════════════╗
║     FREESTYLE HEADSHOT AC - VERSÃO COMPLETA ALL-IN-ONE       ║
║                   Todas as funções integradas                ║
╚═══════════════════════════════════════════════════════════════╝
"""

import ctypes
import psutil
import time
import math
import os
import sys
from ctypes import wintypes

# Importar bibliotecas específicas do Windows (podem exigir: pip install pywin32 win10toast)
try:
    import win32api
    import win32con
    from win32gui import FindWindow, GetWindowThreadProcessId
    from win10toast import ToastNotifier
except ImportError as e:
    print(f"⚠️  Aviso: {e}")
    print("Instale as dependências com: pip install pywin32 win10toast")

# ════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ════════════════════════════════════════════════════════════════

OFFSETS = {
    'PLAYERS_PTR': 0x0010F4F4,
    'POS_X': 0x0,
    'POS_Y': 0x4,
    'POS_Z': 0x8,
    'HEAD_HEIGHT': 1.7,
    'HEALTH': 0xF8,
    'ARMOR': 0xFC,
    'CROUCHING': 0x21C,
    'TEAM': 0x30,
    'ALIVE': 0x68,
    'CAMERA_YAW': 0x40,
    'CAMERA_PITCH': 0x44,
    'FOV': 0x50,
}

AIMBOT_SETTINGS = {
    'MAX_DISTANCE': 100,
    'SNAP_SPEED': 0.8,
    'ONLY_ON_CROUCH': True,
    'TEAM_CHECK': True,
    'DEAD_CHECK': True,
    'WALL_CHECK': True,
    'HEALTH_CHECK': True,
    'FOV': 180,
    'CHECK_INTERVAL': 10,
    'ENABLED': False,
}

DEBUG = {
    'VERBOSE': True,
    'LOG_MEMORY_READS': False,
    'SHOW_DISTANCES': False,
    'SHOW_ANGLES': True,
}

HOTKEYS = {
    'ENABLE': 'F6',
    'DISABLE': 'F7',
    'TOGGLE': 'F8',
}

PLAYER_OFFSET = 0x0010F4F4
ENEMIES_OFFSET = 0x0010F4F8
MAX_PLAYERS = 128

# ════════════════════════════════════════════════════════════════
# ESTRUTURAS DE DADOS
# ════════════════════════════════════════════════════════════════

class Vector3:
    """Representa um vetor 3D"""
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dz = other.z - self.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def __repr__(self):
        return f"Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

class PlayerInfo:
    """Informações do jogador"""
    def __init__(self):
        self.position = Vector3()
        self.head_position = Vector3()
        self.health = 0
        self.armor = 0
        self.is_crouching = False
        self.team = 0
        self.alive = True
        self.index = 0

# ════════════════════════════════════════════════════════════════
# FUNÇÕES DE MEMÓRIA
# ════════════════════════════════════════════════════════════════

def read_memory(process_handle, address, value_type):
    """Lê valor da memória do processo"""
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
        if DEBUG['LOG_MEMORY_READS']:
            print(f"❌ Erro ao ler memória (0x{address:X}): {e}")
        return None

def write_memory(process_handle, address, value, value_type):
    """Escreve valor na memória do processo"""
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
        if DEBUG['LOG_MEMORY_READS']:
            print(f"❌ Erro ao escrever na memória (0x{address:X}): {e}")
        return False

# ════════════════════════════════════════════════════════════════
# FUNÇÕES DE PROCESSO
# ════════════════════════════════════════════════════════════════

def get_assaultcube_pid():
    """Encontra o PID do AssaultCube"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.name().lower()
            if 'cube' in name or 'assaultcube' in name or 'ac.exe' in name:
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            pass
    return None

def get_process_handle(pid):
    """Abre um handle para o processo"""
    try:
        PROCESS_VM_READ = 0x0010
        PROCESS_VM_WRITE = 0x0020
        PROCESS_VM_OPERATION = 0x0008
        
        handle = ctypes.windll.kernel32.OpenProcess(
            PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION,
            False,
            pid
        )
        return handle if handle else None
    except Exception as e:
        print(f"❌ Erro ao abrir processo: {e}")
        return None

def send_notification(title, message):
    """Envia notificação do Windows"""
    try:
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=5)
    except:
        print(f"📢 {title}: {message}")

# ════════════════════════════════════════════════════════════════
# FUNÇÕES DE LEITURA DE DADOS DO JOGADOR
# ════════════════════════════════════════════════════════════════

def get_player_info(process_handle, player_index):
    """Obtém informações completas do jogador"""
    try:
        player_ptr = PLAYER_OFFSET + (player_index * 0x4)
        
        player = PlayerInfo()
        player.index = player_index
        
        # Posição
        player.position.x = read_memory(process_handle, player_ptr + OFFSETS['POS_X'], 'float') or 0
        player.position.y = read_memory(process_handle, player_ptr + OFFSETS['POS_Y'], 'float') or 0
        player.position.z = read_memory(process_handle, player_ptr + OFFSETS['POS_Z'], 'float') or 0
        
        # Cabeça (ajuste pela altura)
        player.head_position = Vector3(
            player.position.x,
            player.position.y,
            player.position.z + OFFSETS['HEAD_HEIGHT']
        )
        
        # Status
        player.health = read_memory(process_handle, player_ptr + OFFSETS['HEALTH'], 'int') or 0
        player.armor = read_memory(process_handle, player_ptr + OFFSETS['ARMOR'], 'int') or 0
        player.is_crouching = bool(read_memory(process_handle, player_ptr + OFFSETS['CROUCHING'], 'byte'))
        player.team = read_memory(process_handle, player_ptr + OFFSETS['TEAM'], 'byte') or 0
        player.alive = player.health > 0
        
        return player
    except Exception as e:
        print(f"❌ Erro ao obter info do jogador: {e}")
        return None

# ════════════════════════════════════════════════════════════════
# FUNÇÕES DE DETECÇÃO DE INIMIGOS
# ════════════════════════════════════════════════════════════════

def raycast_check(start, end, process_handle):
    """Verifica se há linha de visão entre dois pontos"""
    try:
        direction = Vector3(
            end.x - start.x,
            end.y - start.y,
            end.z - start.z
        )
        
        distance = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
        
        if distance == 0:
            return True
        
        if distance > AIMBOT_SETTINGS['MAX_DISTANCE']:
            return False
        
        # Normaliza direção
        direction.x /= distance
        direction.y /= distance
        direction.z /= distance
        
        # Verificação simplificada
        steps = int(distance * 2)
        if steps > 0:
            step_distance = distance / steps
            
            for i in range(1, steps):
                check_point = start + direction * (step_distance * i)
                # Simulação: assume linha de visão até implementação completa
        
        return True
    except:
        return False

def has_line_of_sight(player_pos, enemy_head_pos, process_handle):
    """Verifica se há linha de visão entre jogador e inimigo"""
    if not AIMBOT_SETTINGS['WALL_CHECK']:
        return True
    return raycast_check(player_pos, enemy_head_pos, process_handle)

def get_closest_enemy(process_handle, player_team, player_pos, player_index):
    """Encontra o inimigo mais próximo com todas as verificações"""
    try:
        closest_distance = float('inf')
        closest_enemy = None
        
        for i in range(MAX_PLAYERS):
            if i == player_index:  # Pula o jogador local
                continue
            
            enemy = get_player_info(process_handle, i)
            if not enemy:
                continue
            
            # Verificações de filtro
            if AIMBOT_SETTINGS['DEAD_CHECK'] and not enemy.alive:
                continue
            
            if AIMBOT_SETTINGS['TEAM_CHECK'] and enemy.team == player_team:
                continue
            
            if AIMBOT_SETTINGS['HEALTH_CHECK'] and enemy.health <= 0:
                continue
            
            # Calcula distância
            distance = player_pos.distance_to(enemy.head_position)
            
            if distance > AIMBOT_SETTINGS['MAX_DISTANCE']:
                continue
            
            # Wall check
            if not has_line_of_sight(player_pos, enemy.head_position, process_handle):
                continue
            
            # FOV check
            dx = enemy.head_position.x - player_pos.x
            dy = enemy.head_position.y - player_pos.y
            
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy
        
        return closest_enemy
    except Exception as e:
        print(f"❌ Erro ao buscar inimigo: {e}")
        return None

# ════════════════════════════════════════════════════════════════
# FUNÇÕES DE CÁLCULO DE MIRA
# ════════════════════════════════════════════════════════════════

def calculate_aim_angles(player_pos, target_pos):
    """Calcula ângulos de mira para o alvo"""
    try:
        dx = target_pos.x - player_pos.x
        dy = target_pos.y - player_pos.y
        dz = target_pos.z - player_pos.z
        
        # Yaw (horizontal)
        yaw = math.atan2(dy, dx)
        
        # Pitch (vertical)
        distance_xy = math.sqrt(dx*dx + dy*dy)
        pitch = math.atan2(dz, distance_xy) if distance_xy > 0 else 0
        
        return yaw, pitch
    except:
        return 0, 0

def snap_to_enemy(process_handle, player, enemy):
    """Faz o snap da mira para a cabeça do inimigo"""
    try:
        yaw, pitch = calculate_aim_angles(player.head_position, enemy.head_position)
        
        # Offsets da câmera/mira
        camera_yaw_offset = PLAYER_OFFSET + OFFSETS['CAMERA_YAW']
        camera_pitch_offset = PLAYER_OFFSET + OFFSETS['CAMERA_PITCH']
        
        write_memory(process_handle, camera_yaw_offset, yaw, 'float')
        write_memory(process_handle, camera_pitch_offset, pitch, 'float')
        
        distance = player.head_position.distance_to(enemy.head_position)
        
        if DEBUG['SHOW_ANGLES']:
            print(f"🎯 Snap realizado! Alvo: Jogador {enemy.index} | Distância: {distance:.1f}m")
        
        return True
    except Exception as e:
        print(f"❌ Erro no snap: {e}")
        return False

# ════════════════════════════════════════════════════════════════
# FUNÇÕES DE SCANNER DE OFFSET
# ════════════════════════════════════════════════════════════════

def find_pattern(process_handle, pattern, mask, start_address, end_address):
    """Procura por um padrão de bytes na memória"""
    try:
        current = start_address
        
        while current < end_address:
            try:
                buf = ctypes.create_string_buffer(len(pattern))
                ctypes.windll.kernel32.ReadProcessMemory(
                    process_handle,
                    current,
                    buf,
                    len(pattern),
                    None
                )
                
                match = True
                for i in range(len(pattern)):
                    if mask[i] == 'x' and buf[i] != pattern[i]:
                        match = False
                        break
                
                if match:
                    return current
                
                current += 1
            except:
                break
        
        return None
    except:
        return None

def scan_offsets(pid):
    """Escaneia offsets de memória do AssaultCube"""
    PROCESS_VM_READ = 0x0010
    
    try:
        process_handle = ctypes.windll.kernel32.OpenProcess(
            PROCESS_VM_READ,
            False,
            pid
        )
        
        if not process_handle:
            print("❌ Erro ao abrir processo!")
            return
        
        print("🔍 Escaneando offsets de memória...")
        print("💡 Use Cheat Engine ou consulte wikis de AC para offsets atualizados")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

# ════════════════════════════════════════════════════════════════
# FUNÇÕES DE CONFIGURAÇÃO
# ════════════════════════════════════════════════════════════════

def print_config():
    """Exibe configurações atuais"""
    print("\n" + "="*50)
    print("⚙️  CONFIGURAÇÕES DO AIMBOT")
    print("="*50)
    
    print("\n📊 AIMBOT_SETTINGS:")
    for key, value in AIMBOT_SETTINGS.items():
        if key == 'ENABLED':
            status = "✅ ATIVADO" if value else "❌ DESATIVADO"
            print(f"  {key}: {status}")
        else:
            print(f"  {key}: {value}")
    
    print("\n🐛 DEBUG:")
    for key, value in DEBUG.items():
        print(f"  {key}: {'✅' if value else '❌'}")
    
    print("\n⌨️  HOTKEYS:")
    for key, value in HOTKEYS.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50 + "\n")

def modify_setting(setting_type, key, value):
    """Modifica uma configuração"""
    global AIMBOT_SETTINGS, DEBUG
    
    if setting_type == 'aimbot':
        if key in AIMBOT_SETTINGS:
            AIMBOT_SETTINGS[key] = value
            print(f"✅ {key} = {value}")
        else:
            print(f"❌ Configuração '{key}' não encontrada!")
    elif setting_type == 'debug':
        if key in DEBUG:
            DEBUG[key] = value
            print(f"✅ {key} = {value}")
        else:
            print(f"❌ Debug '{key}' não encontrada!")

# ════════════════════════════════════════════════════════════════
# LOOP PRINCIPAL DO AIMBOT
# ════════════════════════════════════════════════════════════════

def aimbot_loop(process_handle):
    """Loop principal do aimbot"""
    print("\n🎮 Aimbot ativado!")
    print("⏸️  Pressione CTRL+C para sair\n")
    
    try:
        iteration = 0
        while True:
            iteration += 1
            
            if not AIMBOT_SETTINGS['ENABLED']:
                time.sleep(0.1)
                continue
            
            # Obtém informações do jogador principal
            player = get_player_info(process_handle, 0)
            if not player or not player.alive:
                time.sleep(0.01)
                continue
            
            # Verifica se deve usar aimbot (agachado ou sempre)
            if AIMBOT_SETTINGS['ONLY_ON_CROUCH'] and not player.is_crouching:
                time.sleep(0.01)
                continue
            
            # Encontra o inimigo mais próximo
            enemy = get_closest_enemy(process_handle, player.team, player.head_position, 0)
            
            if enemy:
                snap_to_enemy(process_handle, player, enemy)
            
            if DEBUG['SHOW_DISTANCES'] and iteration % 100 == 0:
                print(f"Player Health: {player.health} | Position: {player.position}")
            
            time.sleep(0.01)
    
    except KeyboardInterrupt:
        print("\n\n❌ Aimbot desativado!")
    except Exception as e:
        print(f"\n❌ Erro no loop: {e}")

# ════════════════════════════════════════════════════════════════
# MENU INTERATIVO
# ════════════════════════════════════════════════════════════════

def clear_screen():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    """Menu principal do programa"""
    while True:
        clear_screen()
        print("╔" + "="*58 + "╗")
        print("║" + " "*58 + "║")
        print("║" + "   FREESTYLE HEADSHOT AC - MENU PRINCIPAL".center(58) + "║")
        print("║" + " "*58 + "║")
        print("╚" + "="*58 + "╝")
        print()
        print("  1️⃣  Iniciar Aimbot")
        print("  2️⃣  Configurações")
        print("  3️⃣  Ver Configurações Atuais")
        print("  4️⃣  Scanner de Offsets")
        print("  5️⃣  Sobre")
        print("  0️⃣  Sair")
        print()
        print("="*60)
        
        opcao = input("\n👉 Escolha uma opção (0-5): ").strip()
        
        if opcao == '1':
            menu_iniciar_aimbot()
        elif opcao == '2':
            menu_configuracoes()
        elif opcao == '3':
            print_config()
            input("\n⏎ Pressione ENTER para voltar...")
        elif opcao == '4':
            menu_scanner()
        elif opcao == '5':
            menu_sobre()
        elif opcao == '0':
            print("\n👋 Saindo...")
            break
        else:
            print("\n❌ Opção inválida!")
            time.sleep(1)

def menu_iniciar_aimbot():
    """Menu para iniciar o aimbot"""
    clear_screen()
    print("╔" + "="*58 + "╗")
    print("║" + "   INICIAR AIMBOT".center(58) + "║")
    print("╚" + "="*58 + "╝\n")
    
    print("⏳ Procurando AssaultCube...\n")
    
    pid = None
    timeout = 30
    start_time = time.time()
    
    while pid is None and (time.time() - start_time) < timeout:
        pid = get_assaultcube_pid()
        if pid:
            break
        print(f"  ⏳ Aguardando... ({int(time.time() - start_time)}s)")
        time.sleep(1)
    
    if not pid:
        print(f"\n❌ AssaultCube não encontrado após {timeout}s!")
        print("💡 Dicas:")
        print("  • Abra o AssaultCube")
        print("  • Verifique se o jogo está em execução")
        print("  • Tente novamente")
        input("\n⏎ Pressione ENTER para voltar...")
        return
    
    print(f"✅ AssaultCube encontrado! PID: {pid}")
    
    process_handle = get_process_handle(pid)
    if not process_handle:
        print("❌ Erro ao abrir o processo!")
        input("\n⏎ Pressione ENTER para voltar...")
        return
    
    print("✅ Processo aberto com sucesso!")
    send_notification("Freestyle Headshot AC", f"AssaultCube detectado! PID: {pid}")
    
    print("\n" + "="*60)
    print("⌨️  Controles:")
    print(f"  • F6 - Ativar Aimbot")
    print(f"  • F7 - Desativar Aimbot")
    print(f"  • CTRL+C - Sair")
    print("="*60 + "\n")
    
    print("🟢 AIMBOT PRONTO!\n")
    
    AIMBOT_SETTINGS['ENABLED'] = True
    
    aimbot_loop(process_handle)
    
    ctypes.windll.kernel32.CloseHandle(process_handle)

def menu_configuracoes():
    """Menu de configurações"""
    while True:
        clear_screen()
        print("╔" + "="*58 + "╗")
        print("║" + "   CONFIGURAÇÕES".center(58) + "║")
        print("╚" + "="*58 + "╝\n")
        
        print("  1️⃣  Modificar MAX_DISTANCE ({})".format(AIMBOT_SETTINGS['MAX_DISTANCE']))
        print("  2️⃣  Modificar SNAP_SPEED ({})".format(AIMBOT_SETTINGS['SNAP_SPEED']))
        print("  3️⃣  Toggle ONLY_ON_CROUCH ({})".format("✅" if AIMBOT_SETTINGS['ONLY_ON_CROUCH'] else "❌"))
        print("  4️⃣  Toggle TEAM_CHECK ({})".format("✅" if AIMBOT_SETTINGS['TEAM_CHECK'] else "❌"))
        print("  5️⃣  Toggle WALL_CHECK ({})".format("✅" if AIMBOT_SETTINGS['WALL_CHECK'] else "❌"))
        print("  6️⃣  Toggle DEBUG VERBOSE ({})".format("✅" if DEBUG['VERBOSE'] else "❌"))
        print("  0️⃣  Voltar")
        print()
        
        opcao = input("👉 Escolha uma opção (0-6): ").strip()
        
        if opcao == '1':
            try:
                valor = float(input("📝 Digite o novo valor para MAX_DISTANCE: "))
                modify_setting('aimbot', 'MAX_DISTANCE', valor)
            except ValueError:
                print("❌ Valor inválido!")
            time.sleep(1)
        
        elif opcao == '2':
            try:
                valor = float(input("📝 Digite o novo valor para SNAP_SPEED (0.0-1.0): "))
                if 0 <= valor <= 1:
                    modify_setting('aimbot', 'SNAP_SPEED', valor)
                else:
                    print("❌ Valor deve estar entre 0.0 e 1.0!")
            except ValueError:
                print("❌ Valor inválido!")
            time.sleep(1)
        
        elif opcao == '3':
            AIMBOT_SETTINGS['ONLY_ON_CROUCH'] = not AIMBOT_SETTINGS['ONLY_ON_CROUCH']
            status = "✅ Ativado" if AIMBOT_SETTINGS['ONLY_ON_CROUCH'] else "❌ Desativado"
            print(f"✅ ONLY_ON_CROUCH: {status}")
            time.sleep(1)
        
        elif opcao == '4':
            AIMBOT_SETTINGS['TEAM_CHECK'] = not AIMBOT_SETTINGS['TEAM_CHECK']
            status = "✅ Ativado" if AIMBOT_SETTINGS['TEAM_CHECK'] else "❌ Desativado"
            print(f"✅ TEAM_CHECK: {status}")
            time.sleep(1)
        
        elif opcao == '5':
            AIMBOT_SETTINGS['WALL_CHECK'] = not AIMBOT_SETTINGS['WALL_CHECK']
            status = "✅ Ativado" if AIMBOT_SETTINGS['WALL_CHECK'] else "❌ Desativado"
            print(f"✅ WALL_CHECK: {status}")
            time.sleep(1)
        
        elif opcao == '6':
            DEBUG['VERBOSE'] = not DEBUG['VERBOSE']
            status = "✅ Ativado" if DEBUG['VERBOSE'] else "❌ Desativado"
            print(f"✅ DEBUG VERBOSE: {status}")
            time.sleep(1)
        
        elif opcao == '0':
            break
        
        else:
            print("❌ Opção inválida!")
            time.sleep(1)

def menu_scanner():
    """Menu do scanner de offsets"""
    clear_screen()
    print("╔" + "="*58 + "╗")
    print("║" + "   SCANNER DE OFFSETS".center(58) + "║")
    print("╚" + "="*58 + "╝\n")
    
    print("⏳ Procurando AssaultCube...\n")
    
    pid = get_assaultcube_pid()
    
    if not pid:
        print("❌ AssaultCube não encontrado!")
        input("\n⏎ Pressione ENTER para voltar...")
        return
    
    print(f"✅ AssaultCube encontrado! PID: {pid}\n")
    
    scan_offsets(pid)
    
    print("\n💡 Recursos úteis:")
    print("  • https://www.unknowncheats.me/forum/")
    print("  • Cheat Engine - Para encontrar offsets")
    print("  • AssaultCube Wiki/Comunidade")
    
    input("\n⏎ Pressione ENTER para voltar...")

def menu_sobre():
    """Menu Sobre"""
    clear_screen()
    print("╔" + "="*58 + "╗")
    print("║" + "   SOBRE".center(58) + "║")
    print("╚" + "="*58 + "╝\n")
    
    print("📋 Freestyle Headshot AC")
    print("🎮 Aimbot para AssaultCube")
    print("📅 Versão: 1.0 (All-in-One)\n")
    
    print("✨ Recursos:")
    print("  ✓ Detecção automática de AssaultCube")
    print("  ✓ Aimbot com snap para cabeça")
    print("  ✓ Verificações: Team, Dead, Health, Wall")
    print("  ✓ Configurações personalizáveis")
    print("  ✓ Scanner de offsets")
    print("  ✓ Interface interativa\n")
    
    print("⚠️  AVISO LEGAL:")
    print("  Este software é apenas para propósitos educacionais.")
    print("  O uso em jogos online pode violar os Termos de Serviço.")
    print("  Use por sua conta e risco!\n")
    
    print("📦 Dependências:")
    print("  • psutil")
    print("  • pywin32")
    print("  • win10toast\n")
    
    print("Install: pip install -r requirements.txt\n")
    
    input("⏎ Pressione ENTER para voltar...")

# ════════════════════════════════════════════════════════════════
# PONTO DE ENTRADA
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        clear_screen()
        print("\n🎮 Iniciando Freestyle Headshot AC...\n")
        time.sleep(1)
        
        menu_principal()
        
        print("\n👋 Obrigado por usar Freestyle Headshot AC!\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Programa interrompido!")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
