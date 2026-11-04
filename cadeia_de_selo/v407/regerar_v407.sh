#!/bin/sh
# regerar_v407.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO de 9 modulos (adaptado em 03/11/2026 da v406: la' eram os 301 modulos do fecho em TGLExt/F1Fecho394; aqui o kernel novo sao 9 modulos em TGLExt/: PsionCanto e Par, da gerencia c1, e as sete pedras de 02/11, todas de nome ratificado, normalizados por preparar_bundle_v407_03nov.py):
# guarda do sandbox (o bundle esta' la' e e' o pinado em BUNDLE_v407.json), `lake build` + Audit no sandbox (C:\t\k407c), pos-build (FLAGS, KH_N1, KERNEL_RECIBO, CRITERIOS), insumos duraveis e depois o refazer_candidato_v407.sh --regerar
# (candidato, comparacao AST, ensaio a seco, ESPERADOS, conferidor, citacoes, pinos, conferencia do instalar/reverter/rito, pre-condicoes). Nao toca o Nos, nao instala, nao roda o rito.
# O QUE ESTE SCRIPT NAO FAZ (decisao da gerencia): montar o sandbox. O sandbox C:\t\k407c\final nasce de `sh ./copiar_k407c.sh` (robocopy do kernel do Nos v406 selado, so' leitura; sem /PURGE) e recebe o bundle UMA VEZ por `preparar_bundle_v407_03nov.py` (ele ABORTA se o sandbox ja' tem o modulo e difere);
# para refazer o bundle do zero, apague o sandbox (ato da gerencia) e repita essas duas etapas. Aqui o sandbox e' so' conferido (DL.bundle_fontes() le os modulos do sandbox e confere o sha256 de cada um contra BUNDLE_v407.json).
# ANTES: (1) se o CONTEUDO de algum modulo mudar, o BUNDLE_v407.json e o delta_v407.py (as ancoras) mudam por ato da gerencia; (2) apagar de insumos\ as COPIAS antigas que mudarem (insumos\KH_N1_v407.json e o que a medida nova substitui): os copiadores NAO sobrescrevem o que difere (abortam).
# O build leva ~6 min e o Audit ~4 min no sandbox (medido em 03/11/2026: kernel/construir_marcas.txt, 379 s e 245 s: incremental sobre a v406 compilada, so' os 9 modulos a frio). Depois: python -I -B -X utf8 purga_v407.py (tem de dar ZERO; leva ~20 min, por fora).
# uso: sh ./regerar_v407.sh   (cada passo para na primeira falha; nenhum passo e' mascarado por pipe)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v407"
cd "$V"
PY="python -I -B -X utf8"
echo "== a. guarda do sandbox: os modulos do bundle estao em C:\\t\\k407c\\final e batem com BUNDLE_v407.json $(date +%T)"
$PY -c "
import sys
sys.path.insert(0, '.')
import delta_v407 as DL
f = DL.bundle_fontes()
assert len(f) == DL.N_BUNDLE > 0, len(f)
assert [x['rel'] for x in f] == list(DL.BUNDLE_RELS), 'a ordem do bundle no sandbox nao e a de DL.BUNDLE_RELS'
print('bundle no sandbox:', len(f), 'modulos em TGLExt/, sha256 conferidos contra BUNDLE_v407.json')"
echo "== b. construir_kernel_v407.sh (lake build + Audit; marcas em kernel/construir_marcas.txt) $(date +%T)"; sh ./construir_kernel_v407.sh
echo "== c. pos_build_kernel_v407.py (tem de dar VERDE)"; $PY pos_build_kernel_v407.py > /tmp/regerar_c.txt; tail -1 /tmp/regerar_c.txt
echo "== d. copiar_insumos_v407.py"; $PY copiar_insumos_v407.py > /tmp/regerar_d.txt; tail -1 /tmp/regerar_d.txt
echo "== e. refazer_candidato_v407.sh --regerar $(date +%T)"; sh ./refazer_candidato_v407.sh --regerar
echo "== FIM $(date +%T)"
