# -*- coding: utf-8 -*-
"""conferir_citacoes_v387.py -- confere, por script, que toda citacao do operador na v387 esta VERBATIM numa MENSAGEM DE ENTRADA DO OPERADOR, sem bloco colado
(molde: conferir_citacoes_v386.py; a regua nº 1: nunca fabricar citacao):
  * mensagens do tipo user e queued_command, sem resumo de compactacao nem meta, com os blocos <pasted_content ...> CORTADOS; transcrito: a sessao de 05/10
    (6da8f00d), onde estao os TRES TESTES (23:00:29 UTC) e a LEI DA PROVA (23:19:05 UTC);
  * ESTRITO: os trechos entre `` e '' dos .pysnip PT e EN (os tres testes, rascunho da lente redacao; e o «Ao lado (v387)») -- cada pedaco (separado por «…»)
    NA ORDEM, na MESMA mensagem; o EN cita as MESMAS do PT; e os «…» de 4+ palavras dos comentarios de v387_runtime.py.
  Normaliza so: \\texttt{x} -> x; `x' -> "x"; barras; espacos; casefold. Uso: python conferir_citacoes_v387.py. Sai 0 se o estrito bate."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(os.path.dirname(HERE), "scratch_6da8f00d")
MP = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
TRS = [os.path.join(MP, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")]
NAO_SAO_DO_OPERADOR = set()
SNIPS = {"pt": [os.path.join(HERE, "artigo_pt_v387_tres_testes.pysnip"), os.path.join(HERE, "artigo_pt_v387.pysnip")],
         "en": [os.path.join(HERE, "artigo_en_v387_tres_testes.pysnip"), os.path.join(HERE, "artigo_en_v387.pysnip")]}
PASTED = re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S)


def norm(t):
    t = re.sub(r"\\texttt\{([^}]*)\}", r"\1", t)
    t = re.sub(r"`([^`']*)'", r'"\1"', t)
    t = t.replace("\\", "")
    return re.sub(r"\s+", " ", t).strip().casefold()


msgs = []
for tr in TRS:
    for line in open(tr, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("isCompactSummary") or d.get("isMeta"):
            continue
        if d.get("type") == "user":
            c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        elif d.get("type") == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
            pr = d["attachment"].get("prompt"); ts = [pr] if isinstance(pr, str) else [x.get("text", "") for x in (pr or []) if isinstance(x, dict) and x.get("type") == "text"]
        else:
            continue
        for t in ts:
            if not t:
                continue
            t2 = PASTED.sub(" ", t)
            if t2.strip() and not t2.strip().startswith("<") and not t2.strip().startswith("This session is being continued"):
                msgs.append((d.get("timestamp"), norm(t2)))


def acha(q):
    partes = [norm(p) for p in re.split(r"…", q) if norm(p)]
    out = []
    for ts, m in msgs:
        i = 0; ok_ = True
        for p in partes:
            j = m.find(p, i)
            if j < 0:
                ok_ = False; break
            i = j + len(p)
        if ok_:
            out.append({"quando": ts, "tamanho_da_mensagem": len(m)})
    return out


R = {"mensagens_do_operador": len(msgs), "estrito": {}}
ok = True
por_lingua = {}
for lg, paths in SNIPS.items():
    cits = []
    for p in paths:
        src = open(p, encoding="utf-8").read()
        cits += [c for c in re.findall(r"``(.*?)''", src, flags=re.S) if c not in NAO_SAO_DO_OPERADOR and '" + ' not in c]   # aspa DINAMICA (codigo) fica fora: o conteudo vem abaixo
        # os segmentos verbatim montados dinamicamente (_vb3s = {...} -> _q3s(k) = ``seg''): extraidos por AST e conferidos um a um
        import ast as _ast
        for _n in _ast.walk(_ast.parse("def _f():" + chr(10) + src)):
            if isinstance(_n, _ast.Assign) and any(isinstance(t_, _ast.Name) and t_.id == "_vb3s" for t_ in _n.targets):
                cits += [v_ for v_ in _ast.literal_eval(_n.value).values()]
    por_lingua[lg] = cits
    for c in cits:
        onde = acha(c)
        R["estrito"]["artigo %s: %s" % (lg, norm(c)[:90])] = onde[:1] or "NAO ACHADA"
        ok = ok and bool(onde)
R["n_citacoes"] = {k: len(v) for k, v in por_lingua.items()}
R["en_cita_as_mesmas_do_pt"] = sorted(map(norm, por_lingua["en"])) == sorted(map(norm, por_lingua["pt"]))
ok = ok and R["en_cita_as_mesmas_do_pt"]
rt = open(os.path.join(HERE, "v387_runtime.py"), encoding="utf-8").read()
rt = re.sub(r"\n#\s*", " ", rt)
for q in re.findall(r"«(.*?)»", rt, flags=re.S):
    qn = re.sub(r"\s+", " ", q).strip()
    if len(qn.split()) < 4 or qn in NAO_SAO_DO_OPERADOR:
        continue
    onde = acha(qn)
    R["estrito"]["runtime: %s" % qn[:90]] = onde[:1] or "NAO ACHADA"
    ok = ok and bool(onde)
R["ok"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v387.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:6000])
print("CITACOES (estrito: artigo + runtime):", "TODAS VERBATIM" if ok else "FALHOU")
sys.exit(0 if ok else 1)
