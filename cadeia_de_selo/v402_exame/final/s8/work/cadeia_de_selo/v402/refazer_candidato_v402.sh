#!/bin/sh
# refaz, NA ORDEM, tudo o que depende do texto do candidato v402 (gerador -> comparacao AST -> ensaio a seco [com simular_arvore_do_nos e exame_pontos] -> ESPERADOS -> conferidor [controle negativo e caminho positivo] -> diff e pinos -> precondicoes).
# USAR quando mudar qualquer script/texto que entra no candidato (runtime_v402.py, registros_v402.py, artigo_*_v402.pysnip, gerar_candidato_v402.py) ou o kernel (preparar_kernel_v402.py gerar + construir_kernel_v402.sh + pos_build_kernel_v402.py + copiar_insumos_v402.py antes).
# Nao toca o Nos, nao instala, nao roda o rito. Cada passo para na primeira falha (set -e). Saida inteira em refazer_out_v402.txt.   uso: sh ./refazer_candidato_v402.sh [--regerar]   (--regerar autoriza sobrescrever um candidato ja existente)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v402"
cd "$V"
[ "$1" = "--regerar" ] && export V402_REGERAR=1
PY="python -I -B -X utf8"
PYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o conferidor e o teste dele
echo "== 1. gerar_candidato_v402.py $(date +%T)"; $PY gerar_candidato_v402.py
echo "== 2. comparar_v401_v402.py (nada da v401 perdido)"; $PY comparar_v401_v402.py
echo "== 3. ensaio_a_seco_v402.py (inclui simular_arvore_do_nos, exame_pontos e as guardas ESTATICAS da Bancada sobre o candidato) $(date +%T)"; python -B -X utf8 ensaio_a_seco_v402.py um_v402_candidato.py v402 > ensaio_out.txt 2>&1 || { tail -c 3000 ensaio_out.txt; exit 1; }
tail -2 ensaio_out.txt
echo "== 4. gerar_esperados_v402.py"; $PY gerar_esperados_v402.py
echo "== 5. conferir_rito_v402.py: controle negativo (Nos ainda v401: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PYN conferir_rito_v402.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PYN teste_conferidor_positivo_v402.py | tail -1
echo "== 6. conferir_citacoes_v402.py"; $PY conferir_citacoes_v402.py | tail -1
echo "== 7. diff_e_pinos_v402.py"; $PY diff_e_pinos_v402.py | tail -1
echo "== 8. conferir_instalar_rito_v402.py (instalar/reverter/rito: invariantes, sintaxe e a condicao do modulo novo)"; $PY conferir_instalar_rito_v402.py | tail -1
echo "== 9. p00_precondicoes_v402.py $(date +%T)"; $PY p00_precondicoes_v402.py | tail -6
echo "== FIM $(date +%T)"
