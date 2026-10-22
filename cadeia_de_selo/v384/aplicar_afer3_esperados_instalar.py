# -*- coding: utf-8 -*-
"""3a afericao: os ESPERADOS e o INSTALADOR exigem o candidato ratificado (nao de ensaio), com o trabalhador e a especificacao do pre-registro V1
congelado no lugar permanente; o candidato ANTIGO (0dd43652, anterior a 2a afericao) sai dos nomes padrao (renomeado, nunca apagado)."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
GUARDA = '''# a guarda da ratificacao (3a afericao): candidato de ENSAIO ou sem a ratificacao do operador NAO passa daqui
PRP_V1 = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json")
assert CM.get("ensaio") is False, "o candidato e' de ENSAIO -- nao sigo"
_RAT = CM.get("ratificacao_do_operador") or {}
assert _RAT.get("verbatim") and _RAT.get("quando"), "o candidato nao traz a ratificacao do operador -- nao sigo"
_PJ = json.load(open(PRP_V1, encoding="utf-8"))
assert hashlib.sha256(open(PRP_V1, "rb").read()).hexdigest() == (CM.get("prereg_sha256") or {}).get("json"), "o pre-registro do candidato nao e' o V1 do lugar permanente"
assert _PJ["spec_sha256"] == CM["spec_sha256"] and _PJ["spec"]["worker_sha256"] == CM["worker_sha256"] and (_PJ.get("ratificacao_do_operador") or {}).get("verbatim") == _RAT["verbatim"], \\
    "o trabalhador, a especificacao ou a ratificacao do candidato nao sao os do pre-registro V1"
'''
# esperados
P = os.path.join(HERE, "gerar_esperados_v384.py"); raw = open(P, "rb").read(); s = raw.decode("utf-8")
if not os.path.exists(P + ".bak_antes_afer3"):
    open(P + ".bak_antes_afer3", "wb").write(raw)
old = '''assert CM["sha16"] == h16(cand), "o registro do candidato nao bate com o arquivo"
'''
assert s.count(old) == 1
s = s.replace(old, old + GUARDA); ast.parse(s)
open(P + ".tmp", "wb").write(s.encode("utf-8")); os.replace(P + ".tmp", P); print("ok esperados")
# instalador
P = os.path.join(HERE, "instalar_v384.py"); raw = open(P, "rb").read(); s = raw.decode("utf-8")
if not os.path.exists(P + ".bak_antes_afer3"):
    open(P + ".bak_antes_afer3", "wb").write(raw)
old = '''cand = open(CAND, "rb").read()
assert h16(cand) == ESP["candidato_sha16"], "o candidato mudou (%s != %s)" % (h16(cand), ESP["candidato_sha16"])
'''
new = old + '''CM = json.load(open(os.path.join(HERE, "CANDIDATO_v384.json"), encoding="utf-8"))
assert CM["sha16"] == h16(cand) == ESP["candidato_sha16"], "o registro do candidato nao bate com o arquivo nem com os esperados"
''' + GUARDA
assert s.count(old) == 1
s = s.replace(old, new)
s = s.replace('assert not vivos, "ha processo um.py rodando: %s -- nao instalo" % vivos', 'assert not vivos, "ha processo um.py ou trabalhador do pilar rodando: %s -- nao instalo" % vivos')
ast.parse(s)
open(P + ".tmp", "wb").write(s.encode("utf-8")); os.replace(P + ".tmp", P); print("ok instalar")
# o candidato antigo sai dos nomes padrao
for a, b in (("um_v384_candidato.py", "um_v384_candidato_PRE_AFER2.py"), ("CANDIDATO_v384.json", "CANDIDATO_v384_PRE_AFER2.json")):
    pa, pb = os.path.join(HERE, a), os.path.join(HERE, b)
    if os.path.exists(pa):
        assert not os.path.exists(pb)
        h = hashlib.sha256(open(pa, "rb").read()).hexdigest()[:16]
        os.replace(pa, pb); print("renomeado", a, "->", b, h)
