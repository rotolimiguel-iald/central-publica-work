#!/bin/sh
# refaz, NA ORDEM, tudo o que depende do texto do candidato v400 (montagem do runtime -> gerador -> comparacao AST -> ensaio a seco [com as guardas ESTATICAS da Bancada, simular_arvore_do_nos e exame_pontos] -> ESPERADOS -> conferidor [controle negativo e caminho positivo]
# -> citacoes -> conferencia do instalar/reverter/rito -> diff e pinos -> precondicoes).
# USAR quando mudar qualquer script/texto que entra no candidato (runtime_v400.py [montado por montar_runtime_v400.py], artigo_*_v400.pysnip, gerar_candidato_v400.py). O kernel NAO muda na v400 (nenhum modulo novo): o sandbox C:\t\k400c e' copia do da v399 e o recibo do kernel
# (kernel\KERNEL_RECIBO_v400.json) sai de construir_kernel_v400.sh + pos_build_kernel_v400.py, que NAO sao refeitos aqui (so' se o kernel mudar). Antes: bateria_pre_selo\conferir_recibo_pre_selo_v400.py e gerar_pino_recibo_pre_selo_v400.py (o recibo pre_selo e' o da cadeia v399).
# Nao toca o Nos, nao instala, nao roda o rito. Cada passo para na primeira falha (set -e). Saida inteira em refazer_out_v400.txt.   uso: sh ./refazer_candidato_v400.sh [--regerar]
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v400"
cd "$V"
PY="python -I -B -X utf8"
PYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o ensaio, o conferidor e o teste dele, as citacoes
echo "== 0. montar_runtime_v400.py (a secao do selo ACOM v400 = runtime_v399.py + as 8 edicoes declaradas) $(date +%T)"; $PY montar_runtime_v400.py | tail -3
echo "== 1. gerar_candidato_v400.py $(date +%T)"; $PY gerar_candidato_v400.py
echo "== 2. comparar_v399_v400.py (nada da v399 perdido)"; $PY comparar_v399_v400.py | tail -2
echo "== 3. guardas_estaticas_bancada_v400.py (a funcao ler_nos do esboco R3.5 sobre o candidato)"; $PY guardas_estaticas_bancada_v400.py | head -1
echo "== 4. ensaio_a_seco_v400.py (inclui as guardas estaticas, simular_arvore_do_nos e exame_pontos) $(date +%T)"; $PYN ensaio_a_seco_v400.py um_v400_candidato.py v400 > ensaio_out.txt 2>&1 || { tail -c 3000 ensaio_out.txt; exit 1; }
tail -2 ensaio_out.txt
echo "== 5. gerar_esperados_v400.py"; $PY gerar_esperados_v400.py
echo "== 6. conferir_rito_v400.py: controle negativo (Nos ainda v399: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PYN conferir_rito_v400.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PYN teste_conferidor_positivo_v400.py | tail -1
echo "== 7. conferir_citacoes_v400.py"; $PYN conferir_citacoes_v400.py | tail -1
echo "== 8. conferir_instalar_rito_v400.py (instalar/reverter/rito: invariantes, sintaxe e a condicao dos zero modulos novos)"; $PY conferir_instalar_rito_v400.py | tail -1
echo "== 9. diff_e_pinos_v400.py"; $PY diff_e_pinos_v400.py | tail -1
echo "== 10. p00_precondicoes_v400.py $(date +%T)"; $PY p00_precondicoes_v400.py | tail -6
echo "== FIM $(date +%T)"
