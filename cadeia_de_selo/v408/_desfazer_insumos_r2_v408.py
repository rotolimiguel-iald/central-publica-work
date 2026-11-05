# -*- coding: utf-8 -*-
"""_desfazer_insumos_r2_v408.py -- (claude-construtor-v408-r2, a servico da gerencia c1, 05/11/2026) as COPIAS DURAVEIS de insumos\\ que a nova rodada substitui
(regerar_v408.sh, ANTES (2): «apagar de insumos\\ as COPIAS antigas que mudarem: os copiadores NAO sobrescrevem o que difere»). Medido antes, comparando cada destino de
registros_v408.ORIGENS com a sua origem: as 4 <Nome>_embutida.lean (o bundle novo), BUNDLE_v408.json (o bundle novo), DESENHO_v408.md (o AO LADO da gerencia de 05/11) e
KH_N1_v408.json (o Audit novo). Nada e' apagado: cada um vai, por copia conferida por sha256, para insumos\\superado_r2_<TS>\\ e so' entao sai. Grava RECIBO_DESFAZER_INSUMOS_R2_v408_<TS>.json.
So' move o que DIFERE da origem atual (ou cuja origem foi regerada); recusa se a lista medida nao for exatamente a esperada. uso: python -I -B -X utf8 _desfazer_insumos_r2_v408.py"""
import datetime, hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import registros_v408 as RG  # noqa: E402
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
INS = os.path.join(HERE, "insumos"); SUP = os.path.join(INS, "superado_r2_" + TS)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ESPERADOS = {"TetelestaiTerminal_embutida.lean", "TempoIgualMoeda_embutida.lean", "PontoDeContradicao_embutida.lean", "PIgualNP_embutida.lean", "DESENHO_v408.md", "BUNDLE_v408.json", "KH_N1_v408.json"}
difere = []
for nome, orig in RG.ORIGENS:
    d = os.path.join(INS, nome)
    if os.path.exists(d):
        assert os.path.exists(orig), ("a origem nao existe (rode o pos_build antes)", nome, orig)
        if sha(d) != sha(orig):
            difere.append(nome)
assert set(difere) == ESPERADOS, ("a lista medida nao e' a esperada: PARAR", sorted(set(difere) ^ ESPERADOS))
rec = {"quando": TS, "quem": "claude-construtor-v408-r2 (a servico da gerencia c1)", "motivo": "nova rodada (R3 do PIgualNP, MEDIO 1 da revisao R1, opcao B): as copias duraveis que mudam", "movidos": []}
os.makedirs(SUP)
for nome in sorted(difere):
    src = os.path.join(INS, nome); dst = os.path.join(SUP, nome)
    h = sha(src); shutil.copy2(src, dst); assert sha(dst) == h; os.remove(src)
    rec["movidos"].append({"de": src, "para": dst, "sha256": h})
json.dump(rec, open(os.path.join(HERE, "RECIBO_DESFAZER_INSUMOS_R2_v408_%s.json" % TS), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("movidos para insumos\\superado_r2_%s:" % TS, len(rec["movidos"]), sorted(difere))
