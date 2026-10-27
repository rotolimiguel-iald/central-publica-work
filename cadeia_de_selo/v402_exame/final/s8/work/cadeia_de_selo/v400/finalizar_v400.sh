#!/bin/sh
# finalizar_v400.sh -- a rodada FINAL e ESTRITA da preparacao da v400, na ordem: (1) refazer_candidato_v400.sh (tudo o que depende do texto do candidato: runtime -> candidato -> comparacao -> guardas -> ensaio -> esperados -> conferidor -> citacoes -> instalar/reverter/rito -> pinos -> pre-condicoes);
# (2) gerar_textos_v400.py (idempotente); (3) os dois harness do pos_rito, ESTRITOS (sem --nao-exigir-refazer: exigem o '== FIM' do refazer_out e que ele seja mais novo que o ESPERADOS). Nao toca o Nos, nao instala, nao roda o rito.
# Saida: refazer_out_v400.txt (com a linha final rc=<n>), pos_rito/harness_*_out_final.txt. uso: sh ./finalizar_v400.sh
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v400"
cd "$V" || exit 9
sh ./refazer_candidato_v400.sh > refazer_out_v400.txt 2>&1
echo "rc=$?" >> refazer_out_v400.txt
tail -n 3 refazer_out_v400.txt
python -I -B -X utf8 gerar_textos_v400.py
cd pos_rito || exit 9
python -B -X utf8 harness_textos_ensaio_v400.py --rotulo final > harness_textos_out_final.txt 2>&1
echo "rc=$?" >> harness_textos_out_final.txt
tail -n 2 harness_textos_out_final.txt | cut -c1-300
python -B -X utf8 harness_fechar_sandbox_v400.py > harness_fechar_out_final.txt 2>&1
echo "rc=$?" >> harness_fechar_out_final.txt
tail -n 2 harness_fechar_out_final.txt | cut -c1-300
echo "== FINALIZAR FIM $(date +%T)"
