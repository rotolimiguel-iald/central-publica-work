#!/bin/sh
# _r6c_07_preteste_v410.sh -- o CONSERTO UNICO da v410, passo 6 da ordem (guardas e testes ANTES da cadeia; pre-teste, nao e' a cadeia): a guarda da ordem de chamada, o ensaio a seco (com o LaTeX PT e EN) e os passos 4 a 9 do refazer
# (esperados, conferidor negativo e positivo, citacoes, diff e pinos, instalar/rito, precondicoes) sobre o candidato corrente. Para na primeira falha. Lancado desacoplado; saida em _r6c_preteste_out.txt.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
cd "$V" || exit 9
echo "== candidato $(sha256sum um_v410_candidato.py | cut -c1-16) $(date +%T)"
echo "== ordem de chamada $(date +%T)"; python -B -X utf8 guarda_ordem_de_chamada_v410.py um_v410_candidato.py > _r6c_pre_ordem_out.txt 2>&1; RC=$?; echo "RC_ORDEM=$RC"; [ "$RC" -eq 0 ] || { tail -c 1500 _r6c_pre_ordem_out.txt; echo "RC_PRETESTE6=1"; exit 1; }
echo "== ensaio a seco $(date +%T)"; python -B -X utf8 ensaio_a_seco_v410.py um_v410_candidato.py v410 > ensaio_out.txt 2>&1; RC=$?; echo "RC_ENSAIO=$RC"; tail -2 ensaio_out.txt | cut -c1-400
[ "$RC" -eq 0 ] || { tail -c 3000 ensaio_out.txt; echo "RC_PRETESTE6=1"; exit 1; }
echo "== passos 4 a 9 $(date +%T)"; sh ./refazer_do_passo4_v410.sh > _r6c_pre_passo4_out.txt 2>&1; RC=$?; echo "RC_PASSO4=$RC"; tail -12 _r6c_pre_passo4_out.txt | cut -c1-400
[ "$RC" -eq 0 ] || { echo "RC_PRETESTE6=1"; exit 1; }
echo "== FIM $(date +%T)"; echo "RC_PRETESTE6=0"
