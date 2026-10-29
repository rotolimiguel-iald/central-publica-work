#!/bin/sh
# refaz, NA ORDEM, tudo o que depende do texto do candidato v404 (gerador -> comparacao AST -> ensaio a seco [com simular_arvore_do_nos e exame_pontos] -> ESPERADOS -> conferidor [controle negativo e caminho positivo] -> diff e pinos -> precondicoes).
# USAR quando mudar qualquer script/texto que entra no candidato (runtime_v404.py, registros_v404.py, artigo_*_v404.pysnip, gerar_candidato_v404.py) ou o kernel (preparar_kernel_v404.py gerar + construir_kernel_v404.sh + pos_build_kernel_v404.py + copiar_insumos_v404.py antes).
# Nao toca o Nos, nao instala, nao roda o rito. Cada passo para na primeira falha (set -e). Saida inteira em refazer_out_v404.txt.   uso: sh ./refazer_candidato_v404.sh [--regerar]   (--regerar autoriza sobrescrever um candidato ja existente)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v404"
cd "$V"
[ "$1" = "--regerar" ] && export V404_REGERAR=1
PY="python -I -B -X utf8"
PYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o conferidor e o teste dele
echo "== 1. gerar_candidato_v404.py $(date +%T)"; $PY gerar_candidato_v404.py
echo "== 2. comparar_v403_v404.py (nada da v403 perdido)"; $PY comparar_v403_v404.py
echo "== 3. ensaio_a_seco_v404.py (inclui simular_arvore_do_nos, exame_pontos e as guardas ESTATICAS da Bancada sobre o candidato) $(date +%T)"; python -B -X utf8 ensaio_a_seco_v404.py um_v404_candidato.py v404 > ensaio_out.txt 2>&1 || { tail -c 3000 ensaio_out.txt; exit 1; }
tail -2 ensaio_out.txt
echo "== 4. gerar_esperados_v404.py"; $PY gerar_esperados_v404.py
echo "== 5. conferir_rito_v404.py: controle negativo (Nos ainda v403: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PYN conferir_rito_v404.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PYN teste_conferidor_positivo_v404.py | tail -1
echo "== 6. conferir_citacoes_v404.py"; $PY conferir_citacoes_v404.py | tail -1
echo "== 7. diff_e_pinos_v404.py"; $PY diff_e_pinos_v404.py | tail -1
echo "== 8. conferir_instalar_rito_v404.py (instalar/reverter/rito: invariantes, sintaxe e a condicao do modulo novo)"; $PY conferir_instalar_rito_v404.py | tail -1
echo "== 9. p00_precondicoes_v404.py $(date +%T)"; $PY p00_precondicoes_v404.py | tail -6
echo "== FIM $(date +%T)"
