#!/bin/sh
# refaz, NA ORDEM, tudo o que depende do texto do candidato v406 (gerador -> comparacao AST -> ensaio a seco [com simular_arvore_do_nos e exame_pontos] -> ESPERADOS -> conferidor [controle negativo e caminho positivo] -> diff e pinos -> precondicoes).
# USAR quando mudar qualquer script/texto que entra no candidato (runtime_v406.py, registros_v406.py, artigo_*_v406.pysnip, gerar_candidato_v406.py) ou o kernel (preparar_kernel_v406.py gerar + construir_kernel_v406.sh + pos_build_kernel_v406.py + copiar_insumos_v406.py antes).
# Nao toca o Nos, nao instala, nao roda o rito. Cada passo para na primeira falha (set -e). Saida inteira em refazer_out_v406.txt.   uso: sh ./refazer_candidato_v406.sh [--regerar]   (--regerar autoriza sobrescrever um candidato ja existente)
# [v406, adaptado em 02/11/2026] o candidato e' o do BUNDLE de 301 modulos (nao as oito pedras da v405). O passo 9 (p00) imprime PENDENTE, nao FALHA, para o que so' existe depois do B(n) pre-selo (PINO_RECIBO_PRE_SELO_v406.json, PROVA_PRODUCAO_INTACTA_v406_pre_selo.json), das guardas/harnesses do pos-rito e do MEMORY.md: o p00 final (TODAS PASSARAM) so' vale depois deles.
# O passo 7 grava DIFF_KERNEL_v406.txt, DIFF_v405_v406.diff (diff -u do um.py v405 contra o candidato) e PINOS_BN_v406.json.
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v406"
cd "$V"
[ "$1" = "--regerar" ] && export V406_REGERAR=1
PY="python -I -B -X utf8"
PYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o conferidor e o teste dele
echo "== 1. gerar_candidato_v406.py $(date +%T)"; $PY gerar_candidato_v406.py
echo "== 2. comparar_v405_v406.py (nada da v405 perdido)"; $PY comparar_v405_v406.py
echo "== 3. ensaio_a_seco_v406.py (inclui simular_arvore_do_nos, exame_pontos e as guardas ESTATICAS da Bancada sobre o candidato) $(date +%T)"; python -B -X utf8 ensaio_a_seco_v406.py um_v406_candidato.py v406 > ensaio_out.txt 2>&1 || { tail -c 3000 ensaio_out.txt; exit 1; }
tail -2 ensaio_out.txt
echo "== 4. gerar_esperados_v406.py"; $PY gerar_esperados_v406.py
echo "== 5. conferir_rito_v406.py: controle negativo (Nos ainda v405: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PYN conferir_rito_v406.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PYN teste_conferidor_positivo_v406.py | tail -1
echo "== 6. conferir_citacoes_v406.py"; $PY conferir_citacoes_v406.py | tail -1
echo "== 7. diff_e_pinos_v406.py"; $PY diff_e_pinos_v406.py | tail -1
echo "== 8. conferir_instalar_rito_v406.py (instalar/reverter/rito: invariantes, sintaxe e a condicao do modulo novo)"; $PY conferir_instalar_rito_v406.py | tail -1
echo "== 9. p00_precondicoes_v406.py $(date +%T)"; $PY p00_precondicoes_v406.py | tail -6
echo "== FIM $(date +%T)"
