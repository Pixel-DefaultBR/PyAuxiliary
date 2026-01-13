# Guia Rapido: Gerar Executavel

## Windows

### Passo 1: Instalar PyInstaller
```cmd
pip install pyinstaller
```

### Passo 2: Gerar o executavel
```cmd
build_windows.bat
```

**OU manualmente:**
```cmd
pyinstaller --onefile --windowed --name "SOC Log Sanitizer" --add-data "sanitize_soc_logs.py;." --noconsole sanitizer_gui.py
```

### Passo 3: Encontrar o arquivo
O executavel estara em: `dist\SOC Log Sanitizer.exe`

---

## Linux/Mac

### Passo 1: Instalar PyInstaller
```bash
pip3 install pyinstaller
```

### Passo 2: Gerar o executavel
```bash
chmod +x build_linux.sh
./build_linux.sh
```

**OU manualmente:**
```bash
pyinstaller --onefile --name "SOC-Log-Sanitizer" --add-data "sanitize_soc_logs.py:." sanitizer_gui.py
```

### Passo 3: Encontrar o arquivo
O executavel estara em: `dist/SOC-Log-Sanitizer`

---

## Usando arquivo .spec (Mais rapido)

Apos o primeiro build, use:

```bash
pyinstaller sanitizer.spec
```

Mais rapido e mantem configuracoes.

---

## Distribuir

Apenas copie o arquivo da pasta `dist/` e distribua.

**NAO precisa:**
- Python instalado
- Arquivos .py
- Dependencias

**O executavel e standalone (completo)!**

---

## Problemas Comuns

**Antivirus bloqueia:**
- Normal para executaveis PyInstaller
- Adicione excecao

**Erro ao executar:**
- Compile com console (sem `--noconsole`) para ver erros
- Verifique se `sanitize_soc_logs.py` esta na mesma pasta

**Muito grande:**
- Normal, inclui Python completo (~20MB)

---

Para mais detalhes, veja: `BUILD_README.md`
