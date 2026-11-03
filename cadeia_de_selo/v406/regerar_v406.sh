#!/bin/sh
# regerar_v406.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE de 301 modulos (adaptado em 02/11/2026 da v405: la' eram as OITO pedras; aqui o kernel novo sao os 300 modulos da bancada do ChatGPT, normalizados pela integracao R3, e a candidata CanonicalFullTGLWitnessR1):
# guarda do sandbox (o bundle esta' la' e e' o pinado em BUNDLE_v406.json), `lake build` + Audit no sandbox (C:\t\k406c), pos-build (FLAGS, KH_N1, KERNEL_RECIBO, CRITERIOS), insumos duraveis e depois o refazer_candidato_v406.sh --regerar
# (candidato, comparacao AST, ensaio a seco, ESPERADOS, conferidor, citacoes, pinos, pre-condicoes). Nao toca o Nos, nao instala, nao roda o rito.
# O QUE ESTE SCRIPT NAO FAZ (decisao da gerencia): montar o sandbox. O sandbox C:\t\k406c\final nasce de `preparar_kernel_v406.py copiar` (robocopy do kernel do Nos v405 selado) e recebe o bundle UMA VEZ por preparar_bundle_v406_02nov.py (ele recusa sobrescrever: dst existente aborta);
# para refazer o bundle do zero, apague o sandbox (ato da gerencia) e repita essas duas etapas. Aqui o sandbox e' so' conferido (DL.bundle_fontes() le os 301 modulos do sandbox e confere o sha256 de cada um contra BUNDLE_v406.json).
# ANTES: (1) se o CONTEUDO de algum modulo mudar, o BUNDLE_v406.json e o delta_v406.py (as ancoras) mudam por ato da gerencia; (2) apagar de insumos\ as COPIAS antigas que mudarem (insumos\KH_N1_v406.json e o que a medida nova substitui): os copiadores NAO sobrescrevem o que difere (abortam).
# O build a frio leva ~29 min e o Audit ~5 min no sandbox (medido: kernel/construir_marcas.txt, 1736 s e 280 s). Depois: python -I -B -X utf8 purga_v406.py (tem de dar ZERO).
# uso: sh ./regerar_v406.sh   (cada passo para na primeira falha; nenhum passo e' mascarado por pipe)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v406"
cd "$V"
PY="python -I -B -X utf8"
echo "== a. guarda do sandbox: os 301 modulos do bundle estao em C:\\t\\k406c\\final e batem com BUNDLE_v406.json $(date +%T)"
$PY -c "
import sys
sys.path.insert(0, '.')
import delta_v406 as DL
f = DL.bundle_fontes()
assert len(f) == DL.N_BUNDLE == 301, len(f)
print('bundle no sandbox:', len(f), 'modulos, sha256 conferidos contra BUNDLE_v406.json')"
echo "== b. construir_kernel_v406.sh (lake build + Audit; marcas em kernel/construir_marcas.txt) $(date +%T)"; sh ./construir_kernel_v406.sh
echo "== c. pos_build_kernel_v406.py (tem de dar VERDE)"; $PY pos_build_kernel_v406.py > /tmp/regerar_c.txt; tail -1 /tmp/regerar_c.txt
echo "== d. copiar_insumos_v406.py"; $PY copiar_insumos_v406.py > /tmp/regerar_d.txt; tail -1 /tmp/regerar_d.txt
echo "== e. refazer_candidato_v406.sh --regerar $(date +%T)"; sh ./refazer_candidato_v406.sh --regerar
echo "== FIM $(date +%T)"
