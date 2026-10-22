#!/bin/sh
# rodar_sandbox_r2.sh (R2, 13/10/2026) -- monta o sandbox do vinculo em RAIZ CURTA e roda a sequencia completa + TODOS os controles negativos.
# uso: sh rodar_sandbox_r2.sh [raiz curta = C:\t\vb]   (a raiz e apagada e remontada; a producao, o Nos e o livro de eventos sao SO lidos)
set -e
R2="/c/IALD/Central de Patentes/work/bancada_vinculo_12out/R2"
RAIZ_WIN="${1:-C:\t\vb}"
RAIZ_SH=$(cygpath -u "$RAIZ_WIN")
case "$RAIZ_SH" in /c/t/*) ;; *) echo 'raiz curta obrigatoria (C:	\...):' "$RAIZ_SH"; exit 2;; esac
rm -rf "$RAIZ_SH" && mkdir -p "$RAIZ_SH"
echo "== montar $(date +%T)"
python -B -X utf8 "$R2/montar_sandbox.py" "$RAIZ_WIN" > "$RAIZ_SH/montar_stdout.txt" 2>&1
tail -3 "$RAIZ_SH/montar_stdout.txt"
echo "== runs + controles $(date +%T)"
python -B -X utf8 "$R2/controles_negativos_r2.py" "$RAIZ_WIN" 2>&1 | tee "$RAIZ_SH/controles_stdout.txt"
echo "== fim $(date +%T)"
