## 🎮 Freestyle Headshot AC - Aplicativo Desktop C#

### ✨ Características

- ✅ Aplicativo Windows nativo (exe)
- ✅ Interface gráfica intuitiva
- ✅ Detecção automática de AssaultCube
- ✅ Aimbot com snap para cabeça
- ✅ Verificações avançadas (Team, Dead, Health, Wall)
- ✅ Configurações personalizáveis em tempo real
- ✅ Scanner de offsets de memória
- ✅ Sem dependências Python

---

## 📦 Requisitos

- **Windows 10/11** (64-bit ou 32-bit)
- **.NET 6.0 Runtime** (ou superior)
- **AssaultCube** instalado e em execução

---

## 🚀 Instalação Rápida

1. **Baixar**
   ```bash
   git clone https://github.com/nicolassantos000010-ui/Freestyle-headshot-ac.git
   cd Freestyle-headshot-ac
   ```

2. **Executar**
   ```bash
   dotnet run
   ```

3. **Ou compilar executável**
   ```bash
   dotnet publish -c Release -r win-x64 --self-contained
   ```

---

## 📋 Estrutura do Projeto

```
FreestyleHeadshot/
├── FreestyleHeadshot.csproj    # Configuração do projeto
├── Program.cs                   # Ponto de entrada
├── MainForm.cs                  # Interface principal
├── AimbotManager.cs             # Lógica do aimbot
├── SettingsForm.cs              # Formulário de config
├── ScannerForm.cs               # Scanner de offsets
└── README.md                    # Este arquivo
```

---

## 🎯 Como Usar

### 1. **Inicie o AssaultCube**
   - O jogo deve estar aberto antes de usar o aimbot

### 2. **Execute o Freestyle Headshot**
   ```bash
   dotnet run
   ```

### 3. **Clique em "Iniciar Aimbot"**
   - O programa procurará automaticamente o AssaultCube
   - Se encontrado, o status mudará para ✅ ATIVADO

### 4. **Configure se necessário**
   - Clique em "Configurações"
   - Ajuste os valores desejados
   - Clique em "Salvar"

---

## ⚙️ Configurações Disponíveis

| Configuração | Padrão | Descrição |
|---|---|---|
| **Max Distance** | 100m | Distância máxima para detectar inimigos |
| **Snap Speed** | 0.8 | Velocidade de mira (0.0-1.0) |
| **Only on Crouch** | ✅ | Ativa aimbot apenas quando agachado |
| **Team Check** | ✅ | Não mira em aliados |
| **Dead Check** | ✅ | Ignora jogadores mortos |
| **Wall Check** | ✅ | Verifica linha de visão |
| **Health Check** | ✅ | Ignora jogadores sem saúde |
| **FOV** | 180° | Campo de visão para detecção |

---

## 🔧 Offsets de Memória

```
PLAYERS_PTR:    0x0010F4F4
POS_X:          0x0
POS_Y:          0x4
POS_Z:          0x8
HEAD_HEIGHT:    1.7
HEALTH:         0xF8
ARMOR:          0xFC
CROUCHING:      0x21C
TEAM:           0x30
ALIVE:          0x68
CAMERA_YAW:     0x40
CAMERA_PITCH:   0x44
FOV:            0x50
```

---

## ⚠️ Aviso Legal

- Este software é **apenas para propósitos educacionais**
- O uso em **servidores online** pode violar os **Termos de Serviço**
- Use por sua conta e risco

---

## 📞 Suporte

- 💬 Abra uma Issue no GitHub
- 📧 Verifique a discussão do projeto

**Aproveite! 🎮**
