# -*- coding: utf-8 -*-
"""D -- a rodada 2 da pedra muda algum ENUNCIADO ou PROVA da rodada 1? (implementacao propria)
Remove comentarios Lean (blocos /- -/ aninhados, inclusive docstrings /-- -/ e /-! -/; e '--' de linha), corta o
texto em declaracoes (theorem/def/lemma/... no inicio da linha) e compara declaracao a declaracao, com espacos
normalizados."""
import hashlib, json, os, re

K = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out\3_KERNEL"
R1 = os.path.join(K, r"sandbox\TGLExt\TheUnitIsTheRank.lean")
R2F = os.path.join(K, r"rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "D_R1_VS_R2.json")


def sem_comentarios(t):
    out, i, prof = [], 0, 0
    while i < len(t):
        if t.startswith("/-", i):
            prof += 1
            i += 2
            continue
        if prof > 0 and t.startswith("-/", i):
            prof -= 1
            i += 2
            continue
        if prof > 0:
            i += 1
            continue
        if t.startswith("--", i):
            j = t.find("\n", i)
            i = len(t) if j < 0 else j
            continue
        out.append(t[i])
        i += 1
    return "".join(out)


DECL = re.compile(r"^(theorem|lemma|def|noncomputable def|abbrev|instance|structure|example)\s+([^\s(:{\[]+)", re.M)


def decls(t):
    s = sem_comentarios(t)
    ms = list(DECL.finditer(s))
    d = {}
    for k, m in enumerate(ms):
        fim = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        corpo = re.sub(r"\s+", " ", s[m.start():fim]).strip()
        # tira cauda de 'end Secao' / 'section' / 'variable' que pertence ao arcabouco
        corpo = re.split(r" (?:end|section|variable|namespace|open|noncomputable section)\b", corpo)[0]
        d[m.group(2)] = corpo
    return s, d


t1 = open(R1, encoding="utf-8").read()
t2 = open(R2F, encoding="utf-8").read()
s1, d1 = decls(t1)
s2, d2 = decls(t2)
mudadas = [n for n in d1 if n in d2 and d1[n] != d2[n]]
sumidas = [n for n in d1 if n not in d2]
novas = [n for n in d2 if n not in d1]
res = dict(r1=dict(arquivo=R1, sha256=hashlib.sha256(t1.encode()).hexdigest(), n_decl=len(d1)),
           r2=dict(arquivo=R2F, sha256=hashlib.sha256(t2.encode()).hexdigest(), n_decl=len(d2)),
           r1_decl_mudadas_na_r2=mudadas, r1_decl_ausentes_na_r2=sumidas, decl_novas_na_r2=novas,
           cabecalho_igual=(s1.split("namespace")[0].split() == s2.split("namespace")[0].split()))
with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
