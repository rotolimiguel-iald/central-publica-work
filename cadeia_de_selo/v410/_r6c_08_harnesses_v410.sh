#!/bin/sh
# _r6c_08_harnesses_v410.sh -- o CONSERTO UNICO da v410, passo 6 da ordem (pre-teste, nao e' a cadeia): os dois harness do pos-rito sobre o candidato, o ESPERADOS e o dry_v410 que estao em disco, com pasta de saida PROPRIA
# e --nao-exigir-refazer (o refazer_candidato inteiro e' da cadeia; o veredito de cada harness DIZ que a regeneracao nao foi comprovada por ele). Lancado desacoplado; saida em _r6c_harnesses_out.txt.
# (o do fechar vai primeiro so' porque e' o mais curto: a etapa nova dos ADITIVOS 1 e 2, blocos_do_readme_e_gatilho_da_custodia, aparece em minutos)
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
cd "$V/pos_rito" || exit 9
echo "== harness do fechar $(date +%T)"; python -B -X utf8 harness_fechar_sandbox_v410.py --nao-exigir-refazer --out harness_saida_v410_r6c_fechar > ../_r6c_harness_fechar_out.txt 2>&1; RC2=$?; echo "RC_HF=$RC2"; tail -3 ../_r6c_harness_fechar_out.txt | cut -c1-500
echo "== harness dos textos $(date +%T)"; python -B -X utf8 harness_textos_ensaio_v410.py --manter-copias --nao-exigir-refazer --out harness_saida_v410_r6c_textos > ../_r6c_harness_textos_out.txt 2>&1; RC=$?; echo "RC_HT=$RC"; tail -3 ../_r6c_harness_textos_out.txt | cut -c1-500
echo "== FIM $(date +%T)"; echo "RC_HARNESSES=$((RC + RC2))"
