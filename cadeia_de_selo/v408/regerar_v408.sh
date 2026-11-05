#!/bin/sh
# regerar_v408.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO de 4 modulos (adaptado em 04/11/2026 da v407: la' eram os 9 modulos do psion e do canto; aqui o kernel novo sao 4 modulos em TGLExt/: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes dados pelo operador em 04/11, normalizados por preparar_bundle_v408_04nov.py):
# guarda do sandbox (o bundle esta' la' e e' o pinado em BUNDLE_v408.json), `lake build` + Audit no sandbox (C:\t\k408c), pos-build (FLAGS, KH_N1, KERNEL_RECIBO, CRITERIOS), insumos duraveis e depois o refazer_candidato_v408.sh --regerar
# (candidato, comparacao AST, ensaio a seco, ESPERADOS, conferidor, citacoes, pinos, conferencia do instalar/reverter/rito, pre-condicoes). Nao toca o Nos, nao instala, nao roda o rito.
# O QUE ESTE SCRIPT NAO FAZ (decisao da gerencia): montar o sandbox. O sandbox C:\t\k408c\final nasce de `sh ./copiar_k408c.sh` (robocopy do kernel do Nos v407 selado, so' leitura; sem /PURGE) e recebe o bundle UMA VEZ por `preparar_bundle_v408_04nov.py` (ele ABORTA se o sandbox ja' tem o modulo e difere);
# para refazer o bundle do zero, apague o sandbox (ato da gerencia) e repita essas duas etapas. Aqui o sandbox e' so' conferido (DL.bundle_fontes() le os modulos do sandbox e confere o sha256 de cada um contra BUNDLE_v408.json).
# ANTES: (1) se o CONTEUDO de algum modulo mudar, o BUNDLE_v408.json e o delta_v408.py (as ancoras) mudam por ato da gerencia; (2) apagar de insumos\ as COPIAS antigas que mudarem (insumos\KH_N1_v408.json e o que a medida nova substitui): os copiadores NAO sobrescrevem o que difere (abortam).
# O build leva ~6 min e o Audit ~4 min no sandbox (medido em 04/11/2026: kernel/construir_marcas.txt, 331 s e 251 s: incremental sobre a v407 compilada, so' os 4 modulos a frio). Depois: python -I -B -X utf8 purga_v408.py (tem de dar ZERO; leva ~20 min, por fora).
# uso: sh ./regerar_v408.sh   (cada passo para na primeira falha; nenhum passo e' mascarado por pipe)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v408"
cd "$V"
PY="python -I -B -X utf8"
echo "== a. guarda do sandbox: os modulos do bundle estao em C:\\t\\k408c\\final e batem com BUNDLE_v408.json $(date +%T)"
$PY -c "
import sys
sys.path.insert(0, '.')
import delta_v408 as DL
f = DL.bundle_fontes()
assert len(f) == DL.N_BUNDLE > 0, len(f)
assert [x['rel'] for x in f] == list(DL.BUNDLE_RELS), 'a ordem do bundle no sandbox nao e a de DL.BUNDLE_RELS'
print('bundle no sandbox:', len(f), 'modulos em TGLExt/, sha256 conferidos contra BUNDLE_v408.json')"
echo "== b. construir_kernel_v408.sh (lake build + Audit; marcas em kernel/construir_marcas.txt) $(date +%T)"; sh ./construir_kernel_v408.sh
echo "== c. pos_build_kernel_v408.py (tem de dar VERDE)"; $PY pos_build_kernel_v408.py > /tmp/regerar_c.txt; tail -1 /tmp/regerar_c.txt
echo "== d. copiar_insumos_v408.py"; $PY copiar_insumos_v408.py > /tmp/regerar_d.txt; tail -1 /tmp/regerar_d.txt
echo "== e. refazer_candidato_v408.sh --regerar $(date +%T)"; sh ./refazer_candidato_v408.sh --regerar
echo "== FIM $(date +%T)"
