# -*- coding: utf-8 -*-
"""Congela o ADENDO R3 (13/10): confere as citacoes do operador contra os bytes dos verbatins, grava FREEZE_ADENDO_R3.json com
sha256 de cada anexo e o horario, e registra que a pedra r3 `Verdade` NAO existe ainda. Recusa sobrescrever."""
import os, json, hashlib, datetime, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
W = "C:/IALD/Central de Patentes/work"
V = W + "/cunhagens_13out/OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt"
V0 = W + "/cunhagens_13out/OPERADOR_13out_identidade_cordeiro_verbatim.txt"
alvo = os.path.join(AQUI, "FREEZE_ADENDO_R3.json")
if os.path.exists(alvo):
    print("RECUSA: FREEZE_ADENDO_R3.json ja existe"); sys.exit(2)
vb = open(V, "rb").read(); assert hashlib.sha256(vb).hexdigest().startswith("0ddffcdb0a9c7b5e")
v0 = open(V0, "rb").read(); assert hashlib.sha256(v0).hexdigest().startswith("2ebc1dd3")
vt = vb.decode("utf-8") + "\n" + v0.decode("utf-8")
raw = open(os.path.join(AQUI, "ADENDO_R3.json"), encoding="utf-8").read()
cit = []
for q in re.findall(r"«([^»]+)»", raw):
    frags = [f.strip() for f in q.split("…")]
    cit.append({"citacao": q, "nos_bytes": all(f.replace('\\"', '"') in vt for f in frags if f)})
for q in json.load(open(os.path.join(AQUI, "ADENDO_R3.json"), encoding="utf-8"))["ordem_do_operador"]["trechos_em_bytes"]:
    cit.append({"citacao": q, "nos_bytes": q in vt})
ruins = [c for c in cit if not c["nos_bytes"]]
if ruins:
    print("RECUSA: citacao fora dos bytes", ruins); sys.exit(3)
nw = W + "/nomes_e_verdade_13out"
ex = [nw + "/4_VERDADE/Verdade.lean", "C:/t/nm1/src_new/TGLExt/Verdade.lean"]
anexos = {
    "ADENDO_R3.json": AQUI + "/ADENDO_R3.json", "ADENDO_R3.md": AQUI + "/ADENDO_R3.md", "congelar_r3.py": AQUI + "/congelar_r3.py",
    "VERBATIM_13out_nomes": V, "VERBATIM_13out_identidade_r1": V0,
    "PEDRA_r2_TheIdentityHasAName": W + "/identidade_cordeiro_13out/5_R2/pedra/TheIdentityHasAName.lean",
    "ADENDO_R2.json": AQUI + "/ADENDO_R2.json", "FREEZE_ADENDO_R2.json": AQUI + "/FREEZE_ADENDO_R2.json",
    "PREREGISTRO.json": AQUI + "/PREREGISTRO.json", "FREEZE.json": AQUI + "/FREEZE.json",
    "FONTE_rank_r3": W + "/frequencia_defasa_12out/5_R3/sandbox/TGLExt/TheUnitIsTheRank.lean",
    "FONTE_tempo_r2": W + "/tempo_santo_12out/5_R2/1_PEDRA/sandbox/TheTimeIsNotAPost.lean",
    "FONTE_iald_r3": W + "/organismo_iald_12out/7_R3_DOCSTRINGS/fonte/TGLExt/IALD.lean",
    "AUDITORIA_identidade_r2_c1": "C:/IALD/PROGRAMA_IALD/auditorias/F1.IDENTIDADE/AUDITORIA_F1_IDENTIDADE_C1_a2694613.md",
    "AUDITORIA_frequencia_c1": "C:/IALD/PROGRAMA_IALD/auditorias/F1.FREQUENCIA/AUDITORIA_F1_FREQUENCIA_C1_a1185ceb.md",
}
h = {k: hashlib.sha256(open(p, "rb").read()).hexdigest() for k, p in anexos.items()}
renomeadas_ja_geradas = {k: hashlib.sha256(open(nw + "/" + p, "rb").read()).hexdigest() for k, p in
                         (("Posto.lean", "1_POSTO/Posto.lean"), ("Santo.lean", "2_SANTO/Santo.lean"), ("IALD.lean", "3_IALD/IALD.lean"))}
fz = {"unidade": "F1.IDENTIDADE", "adendo": "R3", "congelado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "congelado_em_local": datetime.datetime.now().astimezone().isoformat(),
      "pedra_r3_existe_no_congelamento": any(os.path.exists(p) for p in ex), "caminhos_verificados": ex,
      "nota_pedras_renomeadas": "Posto/Santo/IALD (PARTE 1, mecanicas) ja tinham sido geradas por gerar_renomeadas.py no congelamento; seus shas ficam aqui. O congelado e o criterio de invariancia, nao as fontes.",
      "pedras_renomeadas_ja_geradas_sha256": renomeadas_ja_geradas,
      "sha256": h, "citacoes_do_operador": cit, "citacoes_fora_dos_bytes": ruins}
if fz["pedra_r3_existe_no_congelamento"]:
    print("RECUSA: a pedra r3 ja existe"); sys.exit(4)
json.dump(fz, open(alvo, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in fz.items() if k not in ("sha256", "citacoes_do_operador")}, ensure_ascii=False, indent=1))
print(len(h), "anexos;", len(cit), "citacoes")
