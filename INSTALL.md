## 📥 GUIA DE INSTALAÇÃO DETALHADO

### ⚡ Quick Start (Rápido)

1. **Baixar Release**
   - Acesse a página de Releases
   - Download `FreestyleHeadshot.exe`

2. **Extrair**
   - Clique direito → Extrair Tudo

3. **Executar**
   - Duplo clique no `.exe`
   - Clique "Sim" se pedir permissão de administrador

---

## 📋 Pré-Requisitos

### Windows
- ✅ Windows 10 ou 11 (64-bit recomendado)
- ✅ Acesso de Administrador (para acessar memória do jogo)

### .NET Runtime
- ✅ .NET 6.0 ou superior

**Verificar se está instalado:**
```cmd
dotnet --version
```

Se não estiver:
1. Acesse: https://dotnet.microsoft.com/download/dotnet/6.0
2. Baixe **".NET Desktop Runtime"**
3. Execute o instalador
4. Reinicie o computador

### AssaultCube
- ✅ Jogo instalado e funcional
- ✅ Deve estar aberto quando usar o aimbot

---

## 🛠️ Instalação Passo a Passo

### Método 1: Arquivo Executável (Mais Fácil)

```
1. Clone ou baixe o repositório
   git clone https://github.com/nicolassantos000010-ui/Freestyle-headshot-ac.git

2. Navegue até a pasta
   cd Freestyle-headshot-ac

3. Execute o programa
   FreestyleHeadshot.exe
```

### Método 2: Compilar com Visual Studio

**Instalação do Visual Studio:**

1. **Baixar Visual Studio Community**
   - Acesse: https://visualstudio.microsoft.com/
   - Download "Community 2022"

2. **Instalar**
   - Execute o instalador
   - Selecione "Desktop Development with C#"
   - Clique "Instalar"
   - Aguarde completar

3. **Clonar Repositório**
   ```cmd
   git clone https://github.com/nicolassantos000010-ui/Freestyle-headshot-ac.git
   cd Freestyle-headshot-ac
   ```

4. **Abrir no Visual Studio**
   - Arquivo → Abrir → Projeto/Solução
   - Selecione `FreestyleHeadshot.csproj`

5. **Compilar**
   - Menu: Compilar → Compilar Solução
   - Ou: `Ctrl+Shift+B`

6. **Executar**
   - Menu: Depurar → Iniciar Depuração
   - Ou: Pressione `F5`

### Método 3: Compilar via CLI

```cmd
# Clonar
git clone https://github.com/nicolassantos000010-ui/Freestyle-headshot-ac.git
cd Freestyle-headshot-ac

# Restaurar dependências
dotnet restore

# Compilar
dotnet build -c Release

# Executar
dotnet run --no-build -c Release
```

### Método 4: Criar Executável Independente

```cmd
# Publicar como executável único
dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true

# O exe estará em:
# bin\Release\net6.0-windows\win-x64\publish\FreestyleHeadshot.exe
```

---

## ✅ Verificação de Instalação

1. **Abra Command Prompt**
   - Pressione `Win + R`
   - Digite: `cmd`
   - Pressione Enter

2. **Verifique .NET**
   ```cmd
   dotnet --version
   ```
   Deve mostrar algo como: `6.0.0` ou superior

3. **Teste o programa**
   ```cmd
   cd caminho\para\Freestyle-headshot-ac
   dotnet run
   ```

---

## 🚀 Primeira Execução

1. **Inicie o AssaultCube**
   - Abra o jogo antes de usar o aimbot

2. **Execute o Freestyle Headshot**
   - Duplo clique em `FreestyleHeadshot.exe`

3. **Clique em "Iniciar Aimbot"**
   - O programa procurará o AssaultCube
   - Status deve mudar para ✅ ATIVADO

4. **Configure se necessário**
   - Clique "Configurações"
   - Ajuste os valores desejados
   - Clique "Salvar"

---

## 🔧 Troubleshooting

### Erro: "Cannot find .NET Runtime"
**Solução:**
- Baixe .NET 6.0 Desktop Runtime
- Link: https://dotnet.microsoft.com/download/dotnet/6.0
- Instale e reinicie

### Erro: "Access Denied"
**Solução:**
- Execute como Administrador
- Clique direito no `.exe` → "Executar como administrador"

### Erro: "AssaultCube not found"
**Solução:**
- Certifique-se que o jogo está aberto
- Tente novamente após alguns segundos

### O aimbot não funciona
**Solução:**
- Verifique se os offsets estão corretos
- Use Cheat Engine para encontrar novos offsets
- Pode ser versão diferente do AssaultCube

---

## 📂 Estrutura de Diretórios

```
FreestyleHeadshot/
├── FreestyleHeadshot.csproj
├── Program.cs
├── MainForm.cs
├── AimbotManager.cs
├── SettingsForm.cs
├── ScannerForm.cs
├── README.md
├── INSTALL.md
├── bin/
│   └── Release/
│       └── net6.0-windows/
│           └── FreestyleHeadshot.exe
└── obj/
```

---

## 🔄 Atualizar para Versão Mais Nova

```cmd
# Entre na pasta do projeto
cd Freestyle-headshot-ac

# Puxe as atualizações
git pull origin main

# Recompile
dotnet build -c Release

# Execute
dotnet run -c Release
```

---

**Instalação concluída! Aproveite o jogo! 🎮**
