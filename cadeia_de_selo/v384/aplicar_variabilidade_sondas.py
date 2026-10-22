# -*- coding: utf-8 -*-
"""O orcamento do pre-registro passa a mostrar a VARIABILIDADE das sondas de tempo (todas as teste_tempo_v*/result.json do pacote, lidas por script, com o
trabalhador de cada uma): o orcamento usa uma so sonda, e as sondas variam. Backup de bytes; ast."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bak = P + ".bak_antes_variabilidade_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = [
    ('''assert ORC["o_D128_comeca_no_prazo_mesmo_com_a_margem"]''', '''import glob as _glob
_SOND = []
for _tp in sorted(_glob.glob(os.path.join(ESTD, "teste_tempo_v*", "result.json"))):
    try:
        _tj = json.load(open(_tp, encoding="utf-8"))
        _SOND.append({"sonda": os.path.basename(os.path.dirname(_tp)), "trabalhador": str(_tj.get("worker_sha256"))[:16], "d64_instancia_s": round(_tj["timing"]["64"]["pipeline_s"], 2),
                      "d64_injecao_T1_s": round(_tj["timing"]["64"]["t1_injection_sigma0_s"], 2), "sha256": fsha(_tp)[:16]})
    except Exception:
        pass
ORC["variabilidade_das_sondas"] = {"sondas": _SOND, "nota": ("o orcamento usa SO a sonda deste trabalhador; as outras sao de versoes anteriores do trabalhador (a mesma maquina, os mesmos "
                                   "caminhos de calculo do tempo) e mostram a dispersao entre rodadas; a margem x1,25 cobre a faixa observada, mas nao foi medida sob a carga do rito")}
if _SOND:
    _v = [x["d64_instancia_s"] for x in _SOND]
    ORC["variabilidade_das_sondas"]["d64_instancia_faixa_s"] = [min(_v), max(_v)]
assert ORC["o_D128_comeca_no_prazo_mesmo_com_a_margem"]'''),
    ('''A(ORC["nota"] + "; fonte: " + ORC["fonte"]); A("")''', '''A(ORC["nota"] + "; fonte: " + ORC["fonte"]); A("")
_VS = ORC.get("variabilidade_das_sondas") or {}
if _VS.get("sondas"):
    A("Variabilidade das sondas de tempo (d = 64; s por instância / por injeção do T1): " + "; ".join("%s (trabalhador %s): %s / %s" % (x["sonda"], x["trabalhador"], x["d64_instancia_s"], x["d64_injecao_T1_s"]) for x in _VS["sondas"])
      + " — faixa da instância: %s a %s s. %s." % (_VS.get("d64_instancia_faixa_s", ["?", "?"])[0], _VS.get("d64_instancia_faixa_s", ["?", "?"])[1], _VS["nota"])); A("")'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:100])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
print("ok")
