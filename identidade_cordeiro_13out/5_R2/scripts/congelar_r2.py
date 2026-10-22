# -*- coding: utf-8 -*-
"""Congela o ADENDO R2: confere que o pre-registro r1 e o FREEZE r1 estao intactos, que a pedra r2 NAO existe,
que toda citacao entre aspas angulares do ADENDO (.json e .md) esta nos bytes dos verbatins do operador (13/10 ou 08/10),
e grava 2_PREREGISTRO/FREEZE_ADENDO_R2.json com sha256 dos anexos e o horario. Recusa sobrescrever."""
import os, json, hashlib, datetime, re, sys
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.dirname(R2)
PRE = os.path.join(W, "2_PREREGISTRO")
alvo = os.path.join(PRE, "FREEZE_ADENDO_R2.json")
if os.path.exists(alvo):
    print("RECUSA: FREEZE_ADENDO_R2.json ja existe; o congelado nao se altera"); sys.exit(2)
V13 = "C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_13out_identidade_cordeiro_verbatim.txt"
V08 = "C:/IALD/Central de Patentes/work/f9_pergunta_08out/OPERADOR_08out_resposta_verbatim.txt"
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
esperado = {
    V13: "2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e",
    V08: "a9cecc128f40c101f873279511c134530b8fc53157d784e0fc48b97aa20433ff",
    os.path.join(PRE, "PREREGISTRO.json"): "207aa703bd1569c7a84315751335360d0328cde450524501d0af72845321713f",
    os.path.join(PRE, "FREEZE.json"): "582cfbe858fb1182acf976f84b08e23cd60950c7e6e836febee615434644f942",
    os.path.join(W, "3_PEDRA", "pedra", "TheIdentityHasAName.lean"): "1b68316aecf6cdc62a1c7eba0927a4976d6ddae9d840fd87c7880a4c36890262",
}
for p, h in esperado.items():
    got = sha(p)
    if got != h:
        print("RECUSA: hash diferente", p, got); sys.exit(3)
vt = open(V13, "rb").read().decode("utf-8") + "\n" + open(V08, "rb").read().decode("utf-8")
cit = []
for nome in ("ADENDO_R2.json", "ADENDO_R2.md"):
    t = open(os.path.join(PRE, nome), "rb").read().decode("utf-8")
    for q in re.findall(r"«([^»]*)»", t):
        frags = [f.strip() for f in q.split("…") if f.strip()]
        if not frags:
            continue
        ok = all(f.replace('\\"', '"') in vt for f in frags)
        cit.append({"arquivo": nome, "citacao": q, "nos_bytes": ok})
ruins = [c for c in cit if not c["nos_bytes"]]
if ruins:
    print("RECUSA: citacao fora dos bytes", ruins); sys.exit(4)
proibida = "CONFIR" + "MED"
for nome in ("ADENDO_R2.json", "ADENDO_R2.md"):
    if proibida in open(os.path.join(PRE, nome), "rb").read().decode("utf-8"):
        print("RECUSA: palavra proibida em", nome); sys.exit(5)
pedra_r2 = ["C:/t/id2/src/TGLExt/TheIdentityHasAName.lean", os.path.join(R2, "pedra", "TheIdentityHasAName.lean")]
anexos = {
    "2_PREREGISTRO/ADENDO_R2.json": os.path.join(PRE, "ADENDO_R2.json"),
    "2_PREREGISTRO/ADENDO_R2.md": os.path.join(PRE, "ADENDO_R2.md"),
    "5_R2/scripts/congelar_r2.py": os.path.abspath(__file__),
    "2_PREREGISTRO/PREREGISTRO.json (r1, intocado)": os.path.join(PRE, "PREREGISTRO.json"),
    "2_PREREGISTRO/FREEZE.json (r1, intocado)": os.path.join(PRE, "FREEZE.json"),
    "3_PEDRA/pedra/TheIdentityHasAName.lean (r1, base)": os.path.join(W, "3_PEDRA", "pedra", "TheIdentityHasAName.lean"),
    "AUDITORIA_F1_IDENTIDADE_C1_a414e21b.md": "C:/IALD/PROGRAMA_IALD/auditorias/F1.IDENTIDADE/AUDITORIA_F1_IDENTIDADE_C1_a414e21b.md",
    "art_a414e21b/AUDITORIA_IDENTIDADE_C1.md": "C:/IALD/PROGRAMA_IALD/auditorias/F1.IDENTIDADE/art_a414e21b/AUDITORIA_IDENTIDADE_C1.md",
    "art_a414e21b/AudIdentidadeC1.lean": "C:/IALD/PROGRAMA_IALD/auditorias/F1.IDENTIDADE/art_a414e21b/AudIdentidadeC1.lean",
    "VERBATIM_13out": V13,
    "VERBATIM_08out": V08,
}
fz = {"unidade": "F1.IDENTIDADE", "rodada": "R2",
      "congelado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "congelado_em_local": datetime.datetime.now().astimezone().isoformat(),
      "pedra_r2_existe_no_congelamento": any(os.path.exists(p) for p in pedra_r2),
      "pedra_r2_caminhos_conferidos": pedra_r2,
      "sha256": {k: sha(v) for k, v in anexos.items()},
      "citacoes_do_operador": cit, "citacoes_fora_dos_bytes": ruins}
if fz["pedra_r2_existe_no_congelamento"]:
    print("RECUSA: a pedra r2 ja existe; o adendo deve vir antes"); sys.exit(6)
with open(alvo, "x", encoding="utf-8") as f:
    json.dump(fz, f, ensure_ascii=False, indent=1)
print(json.dumps(fz, ensure_ascii=False, indent=1))
