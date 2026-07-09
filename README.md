# Freestyle Headshot AC - Aimbot para AssaultCube

Aplicativo que detecta agachamento do jogador no AssaultCube e realiza snap automático para a cabeça do inimigo mais próximo com verificações de time, status e wall-check.

## Funcionalidades

- ✅ Detecção de processo AssaultCube
- ✅ Notificação com PID ao iniciar
- ✅ Detecção de agachamento do jogador
- ✅ Snap automático para cabeça do inimigo mais próximo
- ✅ Team check (não atira em aliados)
- ✅ Dead check (não atira em mortos)
- ✅ Wall check (detecta obstáculos)
- ✅ Uso de offsets oficiais do jogo

## Como usar

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o aplicativo:**
   ```bash
   python main.py
   ```

3. **Abra o AssaultCube**

4. O app notificará o PID quando detectar o jogo

5. **Agache** para ativar o aimbot automático

6. O snap será ativado automaticamente quando agachado

## Arquivos do Projeto

- `main.py` - Script principal com lógica do aimbot
- `config.py` - Configurações e offsets de memória
- `wall_check.py` - Sistema de verificação de obstáculos
- `memory_scanner.py` - Ferramentas para escanear offsets
- `requirements.txt` - Dependências do projeto

## Offsets

Os offsets de memória estão em `config.py` e devem ser atualizados conforme versões do AssaultCube.

Referências:
- [UnknownCheats AC Forum](https://www.unknowncheats.me/forum/)
- [AssaultCube Modding Wiki](https://assault.cubers.net/)

## ⚠️ Aviso Legal

Este projeto é apenas para fins educacionais. O uso em servidores online pode violar os termos de serviço do AssaultCube.
