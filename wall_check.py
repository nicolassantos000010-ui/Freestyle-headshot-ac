"""
Sistema de Wall Check - Detecta se há obstáculos entre jogador e inimigo
Usa raycasting básico ou verificação de colisão
"""

import math
import ctypes

class Vector3:
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

def raycast_check(start, end, process_handle):
    """
    Faz raycasting entre dois pontos
    Retorna True se há linha de visão clara
    """
    # Implementação simplificada
    # Idealmente seria feito com a física do motor do jogo
    
    direction = Vector3(
        end.x - start.x,
        end.y - start.y,
        end.z - start.z
    )
    
    distance = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
    
    if distance == 0:
        return True
    
    # Normaliza direção
    direction.x /= distance
    direction.y /= distance
    direction.z /= distance
    
    # Faz passos ao longo do raio
    steps = int(distance * 2)
    step_distance = distance / steps
    
    for i in range(1, steps):
        check_point = start + direction * (step_distance * i)
        
        # TODO: Verificar colisão no ponto
        # Isso depende de como acessar o mapa/colisão do AssaultCube
        pass
    
    return True  # Sem obstáculos detectados

def has_line_of_sight(player_pos, enemy_head_pos, process_handle):
    """Verifica se há linha de visão entre jogador e cabeça do inimigo"""
    return raycast_check(player_pos, enemy_head_pos, process_handle)

def check_obstacle_between_points(start, end, max_distance=100):
    """Verifica obstáculos com limite de distância"""
    distance = math.sqrt(
        (end.x - start.x)**2 + 
        (end.y - start.y)**2 + 
        (end.z - start.z)**2
    )
    
    if distance > max_distance:
        return True  # Muito longe, considera como bloqueado
    
    return False
