#!/bin/bash

echo "================================================"
echo "  SOC Log Sanitizer - Build para Linux/Mac"
echo "================================================"
echo ""

echo "Verificando se PyInstaller esta instalado..."
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "PyInstaller nao encontrado. Instalando..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao instalar PyInstaller"
        exit 1
    fi
fi

echo ""
echo "Limpando builds anteriores..."
rm -rf build dist "SOC Log Sanitizer.spec"

echo ""
echo "Gerando executavel..."
echo "Isso pode levar alguns minutos..."
echo ""

pyinstaller --onefile \
    --name "SOC-Log-Sanitizer" \
    --add-data "sanitize_soc_logs.py:." \
    sanitizer_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERRO: Falha ao gerar executavel"
    exit 1
fi

echo ""
echo "================================================"
echo "  Build concluido com sucesso!"
echo "================================================"
echo ""
echo "O executavel esta em: dist/SOC-Log-Sanitizer"
echo ""
echo "Tamanho do arquivo:"
ls -lh dist/SOC-Log-Sanitizer | awk '{print $5 "  " $9}'
echo ""
echo "Para executar:"
echo "  ./dist/SOC-Log-Sanitizer"
echo ""
echo "Para tornar executavel:"
echo "  chmod +x dist/SOC-Log-Sanitizer"
echo ""
