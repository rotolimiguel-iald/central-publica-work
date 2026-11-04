#!/bin/sh
# refaz, NA ORDEM, tudo o que depende do texto do candidato v407 (gerador -> comparacao AST -> ensaio a seco [com simular_arvore_do_nos e exame_pontos] -> ESPERADOS -> conferidor [controle negativo e caminho positivo] -> citacoes -> diff e pinos -> conferencia do instalar/reverter/rito -> precondicoes).
# USAR quando mudar qualquer script/texto que entra no candidato (runtime_v407.py, registros_v407.py, artigo_*_v407.pysnip, gerar_candidato_v407.py) ou o kernel (copiar_k407c.sh + preparar_bundle_v407_03nov.py + construir_kernel_v407.sh + pos_build_kernel_v407.py + copiar_insumos_v407.py antes: ver regerar_v407.sh).
# Nao toca o Nos, nao instala, nao roda o rito. Cada passo para na primeira falha (set -e). Saida inteira em refazer_out_v407.txt.   uso: sh ./refazer_candidato_v407.sh [--regerar]   (--regerar autoriza sobrescrever um candidato ja existente)
# [v407, adaptado em 03/11/2026] o candidato e' o do BUNDLE PEQUENO de 9 modulos em TGLExt/ (registro psion_canto_v407; nao o bundle de 301 modulos do fecho da v406, que a v407 herda). O passo 9 (p00) imprime PENDENTE, nao FALHA, para o que so' existe depois do B(n) pre-selo (PINO_RECIBO_PRE_SELO_v407.json, PROVA_PRODUCAO_INTACTA_v407_pre_selo.json), das guardas/harnesses do pos-rito e do MEMORY.md: o p00 final (TODAS PASSARAM) so' vale depois deles.
# O passo 7 grava DIFF_KERNEL_v407.txt, DIFF_v406_v407.diff (diff -u do um.py v406 contra o candidato) e PINOS_BN_v407.json.
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v407"
cd "$V"
[ "$1" = "--regerar" ] && export V407_REGERAR=1
PY="python -I -B -X utf8"
PYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o conferidor e o teste dele
echo "== 1. gerar_candidato_v407.py $(date +%T)"; $PY gerar_candidato_v407.py
echo "== 2. comparar_v406_v407.py (nada da v406 perdido)"; $PY comparar_v406_v407.py
echo "== 3. ensaio_a_seco_v407.py (inclui simular_arvore_do_nos, exame_pontos e as guardas ESTATICAS da Bancada sobre o candidato) $(date +%T)"; python -B -X utf8 ensaio_a_seco_v407.py um_v407_candidato.py v407 > ensaio_out.txt 2>&1 || { tail -c 3000 ensaio_out.txt; exit 1; }
tail -2 ensaio_out.txt
echo "== 4. gerar_esperados_v407.py"; $PY gerar_esperados_v407.py
echo "== 5. conferir_rito_v407.py: controle negativo (Nos ainda v406: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PYN conferir_rito_v407.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PYN teste_conferidor_positivo_v407.py | tail -1
echo "== 6. conferir_citacoes_v407.py"; $PY conferir_citacoes_v407.py | tail -1
echo "== 7. diff_e_pinos_v407.py"; $PY diff_e_pinos_v407.py | tail -1
echo "== 8. conferir_instalar_rito_v407.py (instalar/reverter/rito: invariantes, sintaxe e a condicao do modulo novo)"; $PY conferir_instalar_rito_v407.py | tail -1
echo "== 9. p00_precondicoes_v407.py $(date +%T)"; $PY p00_precondicoes_v407.py | tail -6
echo "== FIM $(date +%T)"
