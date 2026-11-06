#!/bin/sh
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] regera, na ordem, o que depende do bundle de um modulo (guarda do sandbox, build, pos_build, insumos, refazer_candidato); o sandbox nasce de copiar_k409c.sh + preparar_bundle_v409_05nov.py
# regerar_v409.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO de um modulo (adaptado em 05/11/2026 da v408: la' eram os 4 modulos do terminal; aqui o kernel novo e' UM modulo em TGLExt/: TraducaoTuring, com o nome dado pela gerencia e ratificado pelo operador em 05/11, normalizado por preparar_bundle_v409_05nov.py):
# guarda do sandbox (o bundle esta' la' e e' o pinado em BUNDLE_v409.json), `lake build` + Audit no sandbox (C:\t\k409c), pos-build (FLAGS, KH_N1, KERNEL_RECIBO, CRITERIOS), insumos duraveis e depois o refazer_candidato_v409.sh --regerar
# (candidato, comparacao AST, ensaio a seco, ESPERADOS, conferidor, citacoes, pinos, conferencia do instalar/reverter/rito, pre-condicoes). Nao toca o Nos, nao instala, nao roda o rito.
# O QUE ESTE SCRIPT NAO FAZ (decisao da gerencia): montar o sandbox. O sandbox C:\t\k409c\final nasce de `sh ./copiar_k409c.sh` (robocopy de C:\t\k408c\final, o kernel da v408 ja' compilado, so' leitura; sem /PURGE) e recebe o bundle UMA VEZ por `preparar_bundle_v409_05nov.py` (ele ABORTA se o sandbox ja' tem o modulo e difere);
# para refazer o bundle do zero, apague o sandbox (ato da gerencia) e repita essas duas etapas. Aqui o sandbox e' so' conferido (DL.bundle_fontes() le os modulos do sandbox e confere o sha256 de cada um contra BUNDLE_v409.json).
# ANTES: (1) se o CONTEUDO de algum modulo mudar, o BUNDLE_v409.json e o delta_v409.py (as ancoras) mudam por ato da gerencia; (2) apagar de insumos\ as COPIAS antigas que mudarem (insumos\KH_N1_v409.json e o que a medida nova substitui): os copiadores NAO sobrescrevem o que difere (abortam).
# O build leva ~5 min e o Audit ~4 min no sandbox (medido em 05/11/2026: kernel/construir_marcas.txt, 295 s e 218 s: incremental sobre a v408 compilada, so' o modulo novo a frio). Depois: python -I -B -X utf8 purga_v409.py (tem de dar ZERO; leva ~20 min, por fora).
# uso: sh ./regerar_v409.sh   (cada passo para na primeira falha; nenhum passo e' mascarado por pipe)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v409"
cd "$V"
PY="python -I -B -X utf8"
echo "== a. guarda do sandbox: os modulos do bundle estao em C:\\t\\k409c\\final e batem com BUNDLE_v409.json $(date +%T)"
$PY -c "
import sys
sys.path.insert(0, '.')
import delta_v409 as DL
f = DL.bundle_fontes()
assert len(f) == DL.N_BUNDLE > 0, len(f)
assert [x['rel'] for x in f] == list(DL.BUNDLE_RELS), 'a ordem do bundle no sandbox nao e a de DL.BUNDLE_RELS'
print('bundle no sandbox:', len(f), 'modulos em TGLExt/, sha256 conferidos contra BUNDLE_v409.json')"
echo "== b. construir_kernel_v409.sh (lake build + Audit; marcas em kernel/construir_marcas.txt) $(date +%T)"; sh ./construir_kernel_v409.sh
echo "== c. pos_build_kernel_v409.py (tem de dar VERDE)"; $PY pos_build_kernel_v409.py > /tmp/regerar_c.txt; tail -1 /tmp/regerar_c.txt
echo "== d. copiar_insumos_v409.py"; $PY copiar_insumos_v409.py > /tmp/regerar_d.txt; tail -1 /tmp/regerar_d.txt
echo "== e. refazer_candidato_v409.sh --regerar $(date +%T)"; sh ./refazer_candidato_v409.sh --regerar
echo "== FIM $(date +%T)"
