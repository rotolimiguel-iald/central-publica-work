# -*- coding: utf-8 -*-
"""R3: (1) grava DIFF_R2_R3.diff (unified diff da fonte Lean r2 -> r3 e do ensaio numerico r2 -> r3);
(2) prova por codigo que o diff da fonte Lean esta SO em comentarios/docstrings: remove de cada fonte todo comentario
Lean (`-- ...` ate o fim da linha; blocos `/- ... -/`, `/-- ... -/`, `/-! ... -/`, com aninhamento), respeitando
literais de string, normaliza espacos em branco e compara os dois restos. Grava medidas/DIFF_SO_COMENTARIOS.json."""
import difflib, hashlib, json, os, re, sys, datetime

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R2 = "C:/IALD/Central de Patentes/work/organismo_iald_12out/6_R2_CORRECOES/fonte/TGLExt/IALD.lean"
R3 = AQUI + "/fonte/TGLExt/IALD.lean"
E2 = "C:/IALD/Central de Patentes/work/organismo_iald_12out/6_R2_CORRECOES/numerico/ensaio_motor_r2.py"
E3 = AQUI + "/numerico/ensaio_motor_r3.py"


def sem_comentarios(s):
    out = []; i = 0; n = len(s); prof = 0
    while i < n:
        if prof == 0:
            if s.startswith("/-", i):
                prof = 1; i += 2; continue
            if s.startswith("--", i):
                j = s.find("\n", i)
                i = n if j < 0 else j
                continue
            if s[i] == '"':
                j = i + 1
                while j < n and s[j] != '"':
                    j += 2 if s[j] == "\\" else 1
                out.append(s[i:j + 1]); i = j + 1; continue
            out.append(s[i]); i += 1
        else:
            if s.startswith("/-", i):
                prof += 1; i += 2; continue
            if s.startswith("-/", i):
                prof -= 1; i += 2; continue
            i += 1
    if prof != 0:
        raise SystemExit("FALHA VISIVEL: comentario de bloco nao fechado")
    return re.sub(r"\s+", " ", "".join(out)).strip()


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


a = open(R2, encoding="utf-8").read(); b = open(R3, encoding="utf-8").read()
ca, cb = sem_comentarios(a), sem_comentarios(b)
d1 = list(difflib.unified_diff(a.splitlines(True), b.splitlines(True), "r2/TGLExt/IALD.lean", "r3/TGLExt/IALD.lean"))
txt = "".join(d1)
if os.path.exists(E3):
    ea = open(E2, encoding="utf-8").read(); eb = open(E3, encoding="utf-8").read()
    txt += "".join(difflib.unified_diff(ea.splitlines(True), eb.splitlines(True),
                                        "r2/numerico/ensaio_motor_r2.py", "r3/numerico/ensaio_motor_r3.py"))
open(os.path.join(AQUI, "DIFF_R2_R3.diff"), "w", encoding="utf-8", newline="\n").write(txt)
mais = sum(1 for l in d1 if l.startswith("+") and not l.startswith("+++"))
menos = sum(1 for l in d1 if l.startswith("-") and not l.startswith("---"))
res = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "r2": {"arquivo": R2, "sha256": sha(R2), "linhas": a.count("\n")},
       "r3": {"arquivo": R3, "sha256": sha(R3), "linhas": b.count("\n")},
       "lean_linhas_mais": mais, "lean_linhas_menos": menos,
       "codigo_sem_comentarios_sha256_r2": hashlib.sha256(ca.encode()).hexdigest(),
       "codigo_sem_comentarios_sha256_r3": hashlib.sha256(cb.encode()).hexdigest(),
       "codigo_sem_comentarios_identico": ca == cb,
       "receita": "remove -- e /- -/ (aninhado, inclui /-- e /-!) fora de strings; colapsa espacos; compara strings",
       "diff": {"arquivo": os.path.join(AQUI, "DIFF_R2_R3.diff").replace("\\", "/"),
                "sha256": sha(os.path.join(AQUI, "DIFF_R2_R3.diff"))}}
os.makedirs(os.path.join(AQUI, "medidas"), exist_ok=True)
json.dump(res, open(os.path.join(AQUI, "medidas", "DIFF_SO_COMENTARIOS.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
sys.exit(0 if ca == cb else 1)
