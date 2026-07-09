"""
Ferramentas para escanear e encontrar offsets de memória no AssaultCube
Útil para atualizar offsets quando o jogo é atualizado
"""

import ctypes
import psutil

def find_pattern(process_handle, pattern, mask, start_address, end_address):
    """
    Procura por um padrão de bytes na memória
    pattern: bytes para procurar
    mask: máscara (x = verificar, ? = ignorar)
    """
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

def scan_offsets(pid):
    """Escaneia offsets de memória do AssaultCube"""
    PROCESS_VM_READ = 0x0010
    
    process_handle = ctypes.windll.kernel32.OpenProcess(
        PROCESS_VM_READ,
        False,
        pid
    )
    
    if not process_handle:
        print("Erro ao abrir processo!")
        return
    
    print("Escaneando offsets de memória...")
    
    # Exemplo de padrão para procurar (ajustar conforme necessário)
    # pattern = b'\x8B\x0D' + b'\x00' * 4 + b'\x85\xC9'
    # mask = "xx????xx"
    
    print("Use Cheat Engine para encontrar offsets ou consulte wikis de AC")
    print("Offsets conhecidos podem estar em:")
    print("- Forums de modding do AssaultCube")
    print("- Repositórios públicos no GitHub")
    print("- Documentação de bots do AC")

if __name__ == "__main__":
    for proc in psutil.process_iter(['pid', 'name']):
        if 'cube' in proc.name().lower():
            scan_offsets(proc.pid)
