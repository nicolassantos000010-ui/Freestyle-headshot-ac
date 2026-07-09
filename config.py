"""
Configurações do Freestyle Headshot AC
"""

# Offsets de Memória (AssaultCube versão mais recente)
# Esses offsets podem mudar com atualizações do jogo
# Consulte: https://www.unknowncheats.me/forum/ para offsets atualizados

OFFSETS = {
    # Ponteiro base para jogadores
    'PLAYERS_PTR': 0x0010F4F4,
    
    # Offset dentro da estrutura do jogador
    'POS_X': 0x0,
    'POS_Y': 0x4,
    'POS_Z': 0x8,
    'HEAD_HEIGHT': 1.7,  # Altura da cabeça em relação ao corpo
    
    # Status do jogador
    'HEALTH': 0xF8,
    'ARMOR': 0xFC,
    'CROUCHING': 0x21C,
    'TEAM': 0x30,
    'ALIVE': 0x68,
    
    # Câmera/Mira
    'CAMERA_YAW': 0x40,
    'CAMERA_PITCH': 0x44,
    'FOV': 0x50,
}

# Configurações de Comportamento
AIMBOT_SETTINGS = {
    # Distância máxima para ativar aimbot (em unidades do jogo)
    'MAX_DISTANCE': 100,
    
    # Velocidade do snap (0.0 = instantâneo, 1.0 = muito lento)
    'SNAP_SPEED': 0.8,
    
    # Ativar apenas quando agachado
    'ONLY_ON_CROUCH': True,
    
    # Verificações obrigatórias
    'TEAM_CHECK': True,
    'DEAD_CHECK': True,
    'WALL_CHECK': True,
    'HEALTH_CHECK': True,
    
    # FOV (Field of View) - ângulo de visão para snap
    'FOV': 180,
    
    # Intervalo de verificação em milissegundos
    'CHECK_INTERVAL': 10,
}

# Configurações de Debug
DEBUG = {
    'VERBOSE': True,
    'LOG_MEMORY_READS': False,
    'SHOW_DISTANCES': False,
    'SHOW_ANGLES': True,
}

# Hotkeys (se implementado)
HOTKEYS = {
    'ENABLE': 'F6',
    'DISABLE': 'F7',
    'TOGGLE': 'F8',
}

def print_config():
    """Printa as configurações atuais"""
    print("\n=== CONFIGURAÇÕES AIMBOT ===")
    for key, value in AIMBOT_SETTINGS.items():
        print(f"{key}: {value}")
    print("=" * 30 + "\n")

if __name__ == "__main__":
    print_config()
