# -*- coding: utf-8 -*-
"""fidelidade_pedra_v401.py -- exame final v401: cada trecho entre «» na docstring da pedra FalsidadeDaInercia.lean (9f6efcb2) e' substring, por bytes
normalizados (espacos), de UM arquivo-fonte do operador (cunhagens_13out, o recorte incluido), do adendo de 03-04/09 ou do um.py v400 (a l.117522 de
TGLExt.costless) -- ou e' um rotulo; os sha16 citados na docstring batem com os arquivos; a paráfrase «tende ao seu movimento por si» NAO esta entre aspas;
a frase do ADENDO superada e a errata «em nome proprio»; nenhum literal de beta/alfa na pedra; a palavra proibida ausente; nenhum teorema tem binder H_tau."""
import glob, hashlib, json, os, re
H = os.path.dirname(os.path.abspath(__file__))
W = r"C:\IALD\Central de Patentes\work"
L = open(r"C:\t\k401c\final\TGLExt\FalsidadeDaInercia.lean", "rb").read(); assert hashlib.sha256(L).hexdigest().startswith("9f6efcb2a0987e18")
lean = L.decode("utf-8")
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2009", " ").replace("\xa0", " ")).strip()
fontes = {}
for p in glob.glob(os.path.join(W, "cunhagens_13out", "OPERADOR_25out_*_verbatim.txt")) + [os.path.join(W, "cadeia_de_selo", "v401", "insumos", "adendo", "ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md")]:
    b = open(p, "rb").read(); fontes[os.path.basename(p)] = (hashlib.sha256(b).hexdigest()[:16], norm(b.decode("utf-8")))
um400 = open(os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s", "um.py"), "rb").read().decode("utf-8").splitlines()
l117522 = um400[117521]
R = {"linha_117522_do_um_py_v400": l117522.strip()[:200], "citacoes": [], "sha16_citados": {}, "nao_achadas": []}
for m in re.finditer(r"«([^«»]{3,600})»", lean):
    q = norm(m.group(1)); ctx = norm(lean[max(0, m.start() - 160): m.end() + 60])
    onde = [k for k, (h, t) in fontes.items() if q in t]
    if not onde and norm(q.replace("**", "")) in norm(l117522.replace("**", "")): onde = ["um.py v400 l.117522 (TGLExt.costless)"]
    if not onde and norm(q) in norm(" ".join(um400[117440:117530]).replace("**", "")): onde = ["um.py v400 (TheCorrespondence embutido)"]
    rot = bool(re.search(r"\[1=0=FALSO\]|\[1=1=VERDADEIRO\]|falsidade \(simulacro\) da inércia|resistência do corpo|ω\(I\)=1 é a INÉRCIA|nunca correspondeu", q))
    R["citacoes"].append({"citacao": q[:120], "fontes": onde, "rotulo": rot})
    if not onde and not rot: R["nao_achadas"].append({"citacao": q[:160], "ctx": ctx[:220]})
for h in set(re.findall(r"sha16 `?([0-9a-f]{16})", lean)):
    R["sha16_citados"][h] = sorted(k for k, (hh, _) in fontes.items() if hh == h)
R["parafrase_sem_aspas"] = {"ocorrencias": len(re.findall(r"tende ao movimento por si|tende ao seu movimento por si", lean)), "entre_aspas": len(re.findall(r"[«“\"][^»”\"]{0,40}tende ao (seu )?movimento por si", lean)), "marcada_parafrase": "paráfrase, sem aspas" in lean}
R["errata"] = {"em_nome_proprio_gerencia": len(re.findall(r"ERRATA AO LADO \(gerência c1, em nome próprio", lean)), "superada": "fica SUPERADA" in lean, "adendo_sha16": "1459b477b496e1f0" in lean, "costless_l117522": "linha 117522" in lean and "TGLExt.costless" in lean}
pal = "".join(chr(c) for c in (67, 79, 78, 70, 73, 82, 77, 69, 68))
R["palavra_proibida"] = len(re.findall(pal, lean)); R["beta_literal"] = re.findall(r"0[.,]0120\d|1[.,]6487\d|0[.,]00729\d", lean)
R["H_tau_binder_em_teorema"] = len(re.findall(r"\(H_τ|\(H_tau|\(Hτ", lean)); R["H_tau_mencoes_docstring"] = len(re.findall(r"H_τ", lean))
R["DERIVED_e_OPEN"] = {"DERIVED": lean.count("[DERIVED]"), "OPEN": lean.count("[OPEN]"), "ONTO": lean.count("[ONTO]"), "KNOWN": lean.count("[KNOWN]"), "REAL": lean.count("[REAL]")}
R["ponte_docstring"] = {"diz_coordenada_rfl": "Ponte sem hipótese nova" in lean and "rfl" in lean.split("diagFlow_coordinate_is_the_scaling")[0][-900:], "nao_vende_equivalencia_das_estruturas": "equivalência" not in lean.lower().replace("não uma equivalência", ""), "H_tau_fora_do_kernel_dita": "NÃO é termo deste kernel e nada abaixo a usa" in lean}
R["beta_nas_assinaturas"] = {"β como variável {β g : ℝ}": lean.count("{β g : ℝ}"), "β dupla na derivada (β e b)": "{b : ℝ} (hb : 0 < b)" in lean}
R["recorte_dito_como_recorte"] = "recorte declarado da fala de 25/10" in lean and "e26364c5c805734c" in lean
json.dump(R, open(os.path.join(H, "FIDELIDADE_PEDRA_v401.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k != "citacoes"}, ensure_ascii=False, indent=1)); print("n citacoes", len(R["citacoes"]), "sem fonte e sem rotulo", len(R["nao_achadas"]))
for c in R["citacoes"]: print(" -", c["fontes"] or ("ROTULO" if c["rotulo"] else "???"), "|", c["citacao"][:90])
