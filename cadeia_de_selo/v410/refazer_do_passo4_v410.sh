#!/bin/sh
# refazer_do_passo4_v410.sh -- [claude-construtor-v410, 09/11/2026, parte 2] RESERVA: os passos 4 a 9 do refazer_candidato_v410.sh, copiados dele por script (as mesmas linhas), para retomar DEPOIS de um ensaio a seco que ja deu TUDO PASSOU sobre o candidato corrente, sem repetir o ensaio. Nao regenera nada.
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
cd "$V"
PY="python -I -B -X utf8"
PYN="python -B -X utf8"   # SEM -I onde o script importa o um.py (precisa do numpy do usuario): o conferidor e o teste dele
echo "== 4. gerar_esperados_v410.py"; $PY gerar_esperados_v410.py
echo "== 5. conferir_rito_v410.py: controle negativo (Nos ainda v409: tudo_bate tem de ser falso) e caminho positivo (Nos FALSO do ensaio)"
$PYN conferir_rito_v410.py _CONTROLE_NEGATIVO_PRE_RITO > /dev/null 2>&1 && { echo "FALHOU: o controle negativo deu TUDO BATE"; exit 1; } || echo "controle negativo: nao bate (esperado)"
$PYN teste_conferidor_positivo_v410.py | tail -1
echo "== 6. conferir_citacoes_v410.py"; $PY conferir_citacoes_v410.py | tail -1
echo "== 7. diff_e_pinos_v410.py"; $PY diff_e_pinos_v410.py | tail -1
echo "== 8. conferir_instalar_rito_v410.py (instalar/reverter/rito: invariantes, sintaxe e a condicao do modulo novo)"; $PY conferir_instalar_rito_v410.py | tail -1
echo "== 9. p00_precondicoes_v410.py $(date +%T)"; $PY p00_precondicoes_v410.py | tail -6
echo "== FIM $(date +%T)"
