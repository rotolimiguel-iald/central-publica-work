#!/bin/sh
# refaz, NA ORDEM, tudo o que depende do texto do candidato v399 (gerador -> comparacao AST -> ensaio a seco [com simular_arvore_do_nos e exame_pontos] -> ESPERADOS -> conferidor [controle negativo e caminho positivo] -> diff e pinos -> precondicoes).
# USAR quando mudar qualquer script/texto que entra no candidato (runtime_v399.py [montado por montar_runtime_v399.py], registros_v399.py, artigo_*_v399.pysnip, gerar_candidato_v399.py) ou o kernel (refazer_sandbox_v399.sh + pos_build_kernel_v399.py + copiar_insumos_v399.py antes).
# Nao toca o Nos, nao instala, nao roda o rito. Cada passo para na primeira falha (set -e). Saida inteira em refazer_out_v399.txt.   uso: sh ./refazer_candidato_v399.sh [--regerar]   (--regerar autoriza sobrescrever um candidato ja existente)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v399"
cd "$V"
[ "$1" = "--regerar" ] && export V399_REGERAR=1
PY="python -I -B -X utf8"
PYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o conferidor e o teste dele
echo "== 0. montar_runtime_v399.py (o codigo novo do um.py, montado dos insumos aprovados do estudo) $(date +%T)"; $PY montar_runtime_v399.py | tail -3
echo "== 1. gerar_candidato_v399.py $(date +%T)"; $PY gerar_candidato_v399.py
echo "== 2. comparar_v398_v399.py (nada da v398 perdido)"; $PY comparar_v398_v399.py
echo "== 3. ensaio_a_seco_v399.py (inclui simular_arvore_do_nos e exame_pontos) $(date +%T)"; python -B -X utf8 ensaio_a_seco_v399.py um_v399_candidato.py v399 > ensaio_out.txt 2>&1 || { tail -c 3000 ensaio_out.txt; exit 1; }
tail -2 ensaio_out.txt
echo "== 4. gerar_esperados_v399.py"; $PY gerar_esperados_v399.py
echo "== 5. conferir_rito_v399.py: controle negativo (Nos ainda v398: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PYN conferir_rito_v399.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PYN teste_conferidor_positivo_v399.py | tail -1
echo "== 6. conferir_citacoes_v399.py"; $PY conferir_citacoes_v399.py | tail -1
echo "== 7. diff_e_pinos_v399.py"; $PY diff_e_pinos_v399.py | tail -1
echo "== 8. p00_precondicoes_v399.py $(date +%T)"; $PY p00_precondicoes_v399.py | tail -6
echo "== FIM $(date +%T)"
