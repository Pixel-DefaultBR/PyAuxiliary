# Como Gerar Executavel (.exe)

Este guia explica como transformar o SOC Log Sanitizer em um executavel standalone que nao precisa de Python instalado.

## Opcao 1: Automatico (Recomendado)

### Windows

1. Abra o Prompt de Comando na pasta do projeto
2. Execute:
```cmd
build_windows.bat
```

O script automaticamente:
- Instala PyInstaller se necessario
- Limpa builds anteriores
- Gera o executavel
- Mostra o resultado

**Resultado:** `dist\SOC Log Sanitizer.exe`

### Linux/Mac

1. Abra o terminal na pasta do projeto
2. De permissao de execucao:
```bash
chmod +x build_linux.sh
```
3. Execute:
```bash
./build_linux.sh
```

**Resultado:** `dist/SOC-Log-Sanitizer`

## Opcao 2: Manual

### 1. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 2. Gerar o Executavel

**Windows (com janela, sem console):**
```cmd
pyinstaller --onefile --windowed --name "SOC Log Sanitizer" --add-data "sanitize_soc_logs.py;." --noconsole sanitizer_gui.py
```

**Windows (com console para debug):**
```cmd
pyinstaller --onefile --name "SOC Log Sanitizer" --add-data "sanitize_soc_logs.py;." sanitizer_gui.py
```

**Linux/Mac:**
```bash
pyinstaller --onefile --name "SOC-Log-Sanitizer" --add-data "sanitize_soc_logs.py:." sanitizer_gui.py
```

### 3. Encontrar o Executavel

O executavel estara em:
- Windows: `dist\SOC Log Sanitizer.exe`
- Linux/Mac: `dist/SOC-Log-Sanitizer`

## Parametros do PyInstaller

- `--onefile`: Gera um unico arquivo executavel
- `--windowed` / `--noconsole`: Esconde a janela do console (somente GUI)
- `--name`: Nome do executavel
- `--add-data`: Inclui arquivos adicionais necessarios
- `--icon`: Adiciona um icone personalizado (opcional)

## Adicionar Icone (Opcional)

1. Coloque um arquivo `.ico` na pasta do projeto (ex: `icon.ico`)
2. Adicione o parametro:
```cmd
--icon=icon.ico
```

## Tamanho do Executavel

O executavel gerado tera aproximadamente:
- Windows: 15-25 MB
- Linux: 15-20 MB
- Mac: 15-20 MB

O tamanho e maior porque inclui o interpretador Python e todas as bibliotecas necessarias.

## Distribuicao

Apos gerar o executavel, voce pode:

1. **Distribuir apenas o .exe**
   - Nao precisa de Python instalado
   - Funciona em qualquer Windows (64-bit)

2. **Criar um instalador** (opcional)
   - Use Inno Setup (Windows)
   - Use makeself (Linux)
   - Use create-dmg (Mac)

3. **Compactar**
   - ZIP ou 7z para facilitar distribuicao
   - Inclua o README se desejar

## Teste

Antes de distribuir, teste o executavel:

1. Copie o .exe para outra pasta
2. Execute em uma maquina sem Python instalado
3. Teste todas as funcionalidades:
   - Adicionar clientes customizados
   - Sanitizar texto
   - Salvar/carregar arquivos
   - Trocar temas
   - Copiar para area de transferencia

## Solucao de Problemas

### Erro: "Failed to execute script"
- Compile com console (`sem --noconsole`) para ver o erro
- Verifique se todos os imports estao corretos

### Antivirus bloqueia o executavel
- Normal para executaveis gerados com PyInstaller
- Adicione excecao no antivirus
- Ou assine digitalmente o executavel

### Executavel muito grande
- Use `--exclude-module` para remover modulos nao usados
- Exemplo: `--exclude-module matplotlib`

### Erro ao importar modulos
- Verifique se todos os arquivos necessarios foram incluidos
- Use `--add-data` para arquivos adicionais
- Use `--hidden-import` para imports dinamicos

## Versao com Console (Debug)

Para debug, gere versao com console:

```cmd
pyinstaller --onefile --name "SOC Log Sanitizer Debug" --add-data "sanitize_soc_logs.py;." sanitizer_gui.py
```

Isso mostra erros e prints no console.

## Build Multiplataforma

Para gerar executaveis para diferentes sistemas operacionais:

1. **Windows**: Compile no Windows
2. **Linux**: Compile no Linux
3. **Mac**: Compile no Mac

Nao e possivel gerar .exe no Linux ou vice-versa (cross-compilation limitada).

## Alternativas ao PyInstaller

Se PyInstaller nao funcionar, experimente:

- **cx_Freeze**: `pip install cx_Freeze`
- **py2exe**: Apenas Windows
- **Nuitka**: Compila para C (mais rapido)
- **auto-py-to-exe**: Interface grafica para PyInstaller

## Recursos Avancados

### Adicionar splash screen:
```cmd
pyinstaller --onefile --windowed --splash=splash.png sanitizer_gui.py
```

### Especificar versao:
Crie arquivo `version.txt` e use:
```cmd
pyinstaller --onefile --windowed --version-file=version.txt sanitizer_gui.py
```

### Build limpo:
```cmd
pyinstaller --clean --onefile sanitizer_gui.py
```

## Estrutura de Pastas Apos Build

```
projeto/
├── build/              (temporario, pode deletar)
├── dist/               (executavel final aqui)
│   └── SOC Log Sanitizer.exe
├── sanitizer_gui.py
├── sanitize_soc_logs.py
└── SOC Log Sanitizer.spec  (configuracao, pode editar)
```

## Automatizando Builds

Para builds frequentes, edite o arquivo `.spec` gerado e use:

```cmd
pyinstaller "SOC Log Sanitizer.spec"
```

Mais rapido que recriar tudo.

## Suporte

Para mais informacoes sobre PyInstaller:
- Documentacao: https://pyinstaller.org/
- GitHub: https://github.com/pyinstaller/pyinstaller
- Troubleshooting: https://pyinstaller.org/en/stable/when-things-go-wrong.html
