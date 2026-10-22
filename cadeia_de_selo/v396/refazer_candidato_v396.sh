#!/bin/sh
# refaz, NA ORDEM, tudo o que depende do texto do candidato v396 (gerador -> comparacao AST -> ensaio a seco [com simular_arvore_do_nos e exame_pontos] -> ESPERADOS -> conferidor [controle negativo e caminho positivo] -> diff e pinos -> precondicoes).
# USAR quando mudar qualquer script/texto que entra no candidato (runtime_testemunha_v396.py, registros_v396.py, artigo_*_v396.pysnip, gerar_candidato_v396.py) ou o kernel (refazer_sandbox_v396.sh + pos_build_kernel_v396.py + copiar_insumos_v396.py antes).
# Nao toca o Nos, nao instala, nao roda o rito. Cada passo para na primeira falha (set -e). Saida inteira em refazer_out_v396.txt.   uso: sh ./refazer_candidato_v396.sh [--regerar]   (--regerar autoriza sobrescrever um candidato ja existente)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v396"
cd "$V"
[ "$1" = "--regerar" ] && export V396_REGERAR=1
PY="python -I -B -X utf8"
echo "== 1. gerar_candidato_v396.py $(date +%T)"; $PY gerar_candidato_v396.py
echo "== 2. comparar_v395_v396.py (nada da v395 perdido)"; $PY comparar_v395_v396.py
echo "== 3. ensaio_a_seco_v396.py (inclui simular_arvore_do_nos e exame_pontos) $(date +%T)"; python -B -X utf8 ensaio_a_seco_v396.py um_v396_candidato.py v396 > ensaio_out.txt 2>&1 || { tail -c 3000 ensaio_out.txt; exit 1; }
tail -2 ensaio_out.txt
echo "== 4. gerar_esperados_v396.py"; $PY gerar_esperados_v396.py
echo "== 5. conferir_rito_v396.py: controle negativo (Nos ainda v395: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PY conferir_rito_v396.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PY teste_conferidor_positivo_v396.py | tail -1
echo "== 6. conferir_citacoes_v396.py"; $PY conferir_citacoes_v396.py | tail -1
echo "== 7. diff_e_pinos_v396.py"; $PY diff_e_pinos_v396.py | tail -1
echo "== 8. p00_precondicoes_v396.py $(date +%T)"; $PY p00_precondicoes_v396.py | tail -6
echo "== FIM $(date +%T)"
