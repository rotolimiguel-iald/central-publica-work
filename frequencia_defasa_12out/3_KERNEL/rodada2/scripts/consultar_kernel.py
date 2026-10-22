# -*- coding: utf-8 -*-
"""Rodada 2 — consultas SO DE LEITURA ao kernel do Nos (cetico aferidor), citadas nas notas da pedra:
 (1) o «homonimo» de B9.c: algum ENUNCIADO do kernel liga `axiomFlow` (o fluxo do lock) a `Smat`, `rhoOut` ou
     `dephase`/`diagExpect` (a matriz-S e a defasagem)? Varre todo .lean de TGLExt e TGL fora de .lake; para cada
     declaracao (theorem/lemma/def) cujo ENUNCIADO (ate o primeiro ':=') menciona `axiomFlow`, ve se o mesmo enunciado
     menciona algum dos outros; lista tambem os arquivos onde os dois nomes coexistem;
 (2) as pedras da F1.ATRATOR estao no kernel? (nomes TheSingularityReadsTheAttractor*, por texto e por arquivo);
 (3) a pedra desta unidade ja esta no kernel? (TheUnitIsTheRank, por texto e por arquivo).
Grava SO em 3_KERNEL\\rodada2\\CONSULTAS_KERNEL.json."""
import hashlib, json, os, re

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel"
OUTROS = re.compile(r"\b(Smat|rhoOut|dephase|diagExpect)\b")
decl = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma|def|abbrev)\s+(\S+)", re.M)
arquivos = []
for sub in ("TGLExt", "TGL"):
    for dp, dns, fns in os.walk(os.path.join(RAIZ, sub)):
        for fn in fns:
            if fn.endswith(".lean"):
                arquivos.append(os.path.join(dp, fn))
arquivos.sort()
coexistem, pontes, com_axiomFlow = [], [], []
atrator, unidade = [], []
for p in arquivos:
    b = open(p, "rb").read()
    t = b.decode("utf-8", errors="replace")
    rel = os.path.relpath(p, RAIZ).replace("\\", "/")
    if "TheSingularityReadsTheAttractor" in t or "TheSingularityReadsTheAttractor" in rel:
        atrator.append(rel)
    if "TheUnitIsTheRank" in t or "TheUnitIsTheRank" in rel:
        unidade.append(rel)
    if "axiomFlow" not in t:
        continue
    com_axiomFlow.append(rel)
    if OUTROS.search(t):
        coexistem.append(rel)
    ms = list(decl.finditer(t))
    for i, m in enumerate(ms):
        fim = ms[i + 1].start() if i + 1 < len(ms) else len(t)
        bloco = t[m.start():fim]
        enun = bloco.split(":=", 1)[0]
        if "axiomFlow" in enun and OUTROS.search(enun):
            ln = t.count("\n", 0, m.start()) + 1
            pontes.append({"arquivo": rel, "linha": ln, "declaracao": m.group(2), "enunciado": " ".join(enun.split())[:400]})
out = {
    "documento": "CONSULTAS_KERNEL — rodada 2 do construtor do kernel (so leitura do tgl_kernel do Nos)",
    "raiz": RAIZ, "arquivos_lean_varridos": len(arquivos),
    "homonimo_B9c": {"arquivos_com_axiomFlow": com_axiomFlow, "arquivos_onde_coexistem_com_Smat_rhoOut_dephase": coexistem,
                     "enunciados_que_ligam_axiomFlow_a_Smat_rhoOut_dephase": pontes,
                     "leitura": "nenhum enunciado liga os dois objetos" if not pontes else "HA enunciado-ponte (ver lista)"},
    "pedras_F1_ATRATOR_no_kernel": atrator,
    "pedra_TheUnitIsTheRank_no_kernel": unidade,
}
dst = os.path.join(R2, "CONSULTAS_KERNEL.json")
with open(dst + ".tmp", "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(out, ensure_ascii=False, indent=1))
