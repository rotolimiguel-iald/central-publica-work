"""Varredura SOMENTE-LEITURA das declaracoes do tgl_kernel do Nos (TGL/, TGLExt/ e subpastas; nunca .lake).
Para cada declaracao (theorem/lemma/def/structure/abbrev/class/instance/inductive) registra:
arquivo relativo, linha, nome qualificado (pilha de namespace), tipo, cabeca do enunciado e a docstring anterior.
Grava kernel_decls.jsonl e, por tema, kernel_temas.json (temas = regex sobre nome + docstring).
Uso: python -I varrer_kernel.py"""
import hashlib
import json
import os
import re

ROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
SUBS = ["TGL", "TGLExt"]
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+)*"
                  r"(theorem|lemma|def|structure|abbrev|class|instance|inductive)\s+([^\s:({\[]+)")
NS_OPEN = re.compile(r"^\s*namespace\s+(\S+)")
NS_END = re.compile(r"^\s*end\s+(\S+)\s*$")
SEC_OPEN = re.compile(r"^\s*(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")

TEMAS = {
    "tempo_relogio": r"\btime\b|tempo|clock|rel[oó]gio|\bnow\b|agora|\bpresent\b",
    "periodo_kms_unruh": r"period|per[ií]odo|\bkms\b|KMSAt|unruh|temperature|temperatura|wick|2\s*\*\s*Real\.pi",
    "fluxo_modular_tomita": r"modular|tomita|takesaki|lightDelta|\bDelta\b|Δ\^|modularFlow|bisognano|connes|cocycle|cociclo",
    "semigrupo_dephasing_gkls": r"semigroup|semigrupo|dephas|defas|lindblad|gkls|axiomFlow|dissip|spohn|subordin|poisson",
    "atrator_contracao_limite": r"attract|atrator|contract|contra[cç]|tendsto|limit|basin|bacia|ergod|lyapunov|fixed.?point|ponto fixo",
    "liouville_volume_unitario": r"liouville|measurePreserving|volume|unitary|unit[aá]ri|isometr|symplectic|simpl[eé]tic|recurr|det_exp|exp_trace",
    "pauli_ccr_operador_tempo": r"time.?operator|operador de tempo|\bccr\b|heisenberg|canonical commutation|weyl relation|commutator.*(one|identity|smul)|semibounded|bounded.?below",
    "landauer_custo_perda": r"landauer|erasure|apag|\bcost\b|custo|leak|vazamento|loss|perda|irrevers|\barrow\b|seta",
    "fundacao_agape_piso": r"agape|[aá]gape|fundac|abismo|floor|piso|climb|fall_never|nothing_above",
    "posto_rank_nome": r"\bpost\b|post_|posto|\brank\b|rank_|starProjection|PFmic|the_post|name_one|Nome|\bName\b",
    "leitura_palavra_observador": r"reading|leitura|observ|palavra|letra|Palavra|adds_nothing|reads_the_angle",
    "sem_testemunha_estatica": r"full_static|static_witness|NoFullWitness|forbids_full|beta_forbids|testemunha plena|fotografia",
    "inner_outer_semifinito_traco": r"\bouter\b|\binner\b|IsInner|semifinite|semifinit|tracial|trace_state|breuer",
    "santo_kadosh": r"kadosh|santo|sagrad|holy|sacred|separad",
}


def scan():
    decls = []
    for sub in SUBS:
        base = os.path.join(ROOT, sub)
        for dp, dn, fn in os.walk(base):
            dn.sort()
            for f in sorted(fn):
                if not f.endswith(".lean"):
                    continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, ROOT).replace("\\", "/")
                with open(p, "rb") as fh:
                    raw = fh.read()
                sha16 = hashlib.sha256(raw).hexdigest()[:16]
                lines = raw.decode("utf-8", "replace").splitlines()
                ns = []
                doc_buf = []
                in_doc = False
                for i, line in enumerate(lines, 1):
                    s = line.strip()
                    if in_doc:
                        doc_buf.append(s)
                        if "-/" in s:
                            in_doc = False
                        continue
                    if s.startswith("/--") or s.startswith("/-!"):
                        doc_buf = [s]
                        in_doc = "-/" not in s[3:]
                        continue
                    m = NS_OPEN.match(line)
                    if m:
                        ns.append(m.group(1))
                        continue
                    m = NS_END.match(line)
                    if m and ns and ns[-1] == m.group(1):
                        ns.pop()
                        continue
                    m = DECL.match(line)
                    if m:
                        kind, name = m.group(1), m.group(2)
                        q = ".".join(ns + [name]) if ns else name
                        head = " ".join(l.strip() for l in lines[i - 1:i + 3])[:400]
                        doc = " ".join(doc_buf)[:900]
                        decls.append(dict(file=rel, sha16=sha16, line=i, kind=kind, name=q, head=head, doc=doc))
                        doc_buf = []
                    elif s and not s.startswith("--"):
                        if not s.startswith("@["):
                            doc_buf = doc_buf if s.startswith("#") else []
    return decls


def main():
    decls = scan()
    with open("kernel_decls.jsonl", "w", encoding="utf-8") as fo:
        for d in decls:
            fo.write(json.dumps(d, ensure_ascii=False) + "\n")
    temas = {}
    for tema, rx in TEMAS.items():
        r = re.compile(rx, re.I)
        hits = [d for d in decls if d["kind"] in ("theorem", "lemma", "def", "structure", "abbrev", "class", "inductive")
                and (r.search(d["name"]) or r.search(d["doc"]))]
        temas[tema] = dict(regex=rx, n=len(hits),
                           arquivos=sorted({h["file"] for h in hits}),
                           decls=[dict(name=h["name"], file=h["file"], line=h["line"], kind=h["kind"], sha16=h["sha16"]) for h in hits])
    with open("kernel_temas.json", "w", encoding="utf-8") as fo:
        json.dump(temas, fo, ensure_ascii=False, indent=1)
    print("declaracoes:", len(decls), "arquivos:", len({d['file'] for d in decls}))
    for t, v in temas.items():
        print(f"{t:34s} n={v['n']:6d} arquivos={len(v['arquivos'])}")


if __name__ == "__main__":
    main()
