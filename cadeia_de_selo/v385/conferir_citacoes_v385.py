# -*- coding: utf-8 -*-
"""Confere, por script, que toda citacao do operador na v385 esta VERBATIM numa MENSAGEM DE ENTRADA DO OPERADOR, SEM BLOCO COLADO MARCADO (a regua nº 1:
nunca fabricar citacao; achado 1 da 1a afericao de texto, achado 2 da 2a passada e o CORRIGIR da 3a: o script NAO distingue texto colado SEM marca dentro
da mensagem -- por isso grava, para cada citacao, o carimbo e o TAMANHO da mensagem onde acha, para a leitura humana):
  * o que conta como palavra do operador: mensagens do tipo user e queued_command, SEM o resumo de compactacao (isCompactSummary) nem as meta (isMeta), e com
    os blocos <pasted_content ...>...</pasted_content ...> CORTADOS (texto colado de outra IA nao e' do operador); so o texto puro (nada que comece com «<»);
  * as citacoes conferidas: (a) os trechos entre `` e '' dos .pysnip PT e EN que nao sao da lista do proprio artigo (codigo, formas da errata); (b) os «…» da
    pedra TheAxiomAndTheFalseWitness.lean e do comentario da v385 no TGL/Audit.lean com 4 palavras ou mais, fora as leituras do proprio modulo -- contra o
    transcrito desta sessao (05/10) E o da sessao d554e796 (20/08). Reticencias «…» sao lacuna: os pedacos tem de aparecer NA ORDEM na MESMA mensagem.
  * normaliza so: \\texttt{x} -> x; as aspas internas `x' -> "x"; espacos.
E confere que as formas que a errata cita EXISTEM no texto antigo (dry_v385_pt/en.txt). Uso: python conferir_citacoes_v385.py [dry_dir]. Sai 0 se tudo bate."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MP = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
TRS = [os.path.join(MP, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"), os.path.join(MP, "d554e796-415e-450f-9fd4-dd07892b02b9.jsonl")]
K = os.path.join(os.path.dirname(HERE), "v376", "kernel_src")
DRY = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dry_v385")
NAO_SAO_DO_OPERADOR = {"Inscreva o UM para iniciar", "um único postulado", "o único postulado", "o postulado do Um", "a single postulate", "the single postulate",
                       "the One postulate", "$1=1$ deixa de ser postulado e vira o teorema do traço", "$1=1$ ceases to be a postulate and becomes the trace theorem",
                       "postulado", "postulate", "axioma único ($\\omega(I)=1$)", "single axiom ($\\omega(I)=1$)", "Axioma", "Axiom", "conjugado", "conjugated",
                       "invariante sob \\emph{todos} os operadores", "invariant under \\emph{all} operators", "invariante sob TODOS os operadores"}
PASTED = re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S)


def norm(t):
    t = re.sub(r"\\texttt\{([^}]*)\}", r"\1", t)
    t = re.sub(r"`([^`']*)'", r'"\1"', t)
    t = t.replace("\\", "")
    return re.sub(r"\s+", " ", t).strip()


msgs = []; puladas = {"compact_ou_meta": 0, "blocos_colados_cortados": 0}
for tr in TRS:
    for line in open(tr, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("isCompactSummary") or d.get("isMeta"):
            puladas["compact_ou_meta"] += 1; continue
        if d.get("type") == "user":
            c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
        elif d.get("type") == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
            pr = d["attachment"].get("prompt"); ts = [pr] if isinstance(pr, str) else [x.get("text", "") for x in (pr or []) if isinstance(x, dict) and x.get("type") == "text"]
        else:
            continue
        for t in ts:
            if not t:
                continue
            t2, n = PASTED.subn(" ", t); puladas["blocos_colados_cortados"] += n
            if t2.strip() and not t2.strip().startswith("<") and not t2.strip().startswith("This session is being continued"):
                msgs.append((d.get("timestamp"), norm(t2)))


def acha(q):
    """os pedacos (separados por «…») NA ORDEM na MESMA mensagem; devolve os carimbos das mensagens que contem."""
    partes = [norm(p) for p in re.split(r"…", q) if norm(p)]
    out = []
    for ts, m in msgs:
        i = 0; ok = True
        for p in partes:
            j = m.find(p, i)
            if j < 0:
                ok = False; break
            i = j + len(p)
        if ok:
            out.append({"quando": ts, "tamanho_da_mensagem": len(m)})
    return out


R = {"mensagens_do_operador": len(msgs), "puladas": puladas, "citacoes": {}, "formas_da_errata": {}}
ok = True
por_lingua = {}
for lg in ("pt", "en"):
    src = open(os.path.join(HERE, "artigo_%s_v385.pysnip" % lg), encoding="utf-8").read()
    cits = [c for c in re.findall(r"``(.*?)''", src, flags=re.S) if c not in NAO_SAO_DO_OPERADOR]
    por_lingua[lg] = cits
    for c in cits:
        onde = acha(c)
        R["citacoes"]["artigo %s: %s" % (lg, norm(c)[:90])] = onde[:1] or "NAO ACHADA"
        ok = ok and bool(onde)
R["en_cita_as_mesmas_do_pt"] = sorted(map(norm, por_lingua["en"])) == sorted(map(norm, por_lingua["pt"]))
ok = ok and R["en_cita_as_mesmas_do_pt"]
# (b) a pedra e o comentario da v385 no Audit.lean
pedra = open(os.path.join(K, "TGLExt", "TheAxiomAndTheFalseWitness.lean"), encoding="utf-8").read()
au = open(os.path.join(K, "TGL", "Audit.lean"), encoding="utf-8").read(); au = au[au.index("-- 2026-10-05, v385"):].split("\n", 1)[0]
for nome, txt in (("pedra", pedra), ("Audit.lean", au)):
    for q in re.findall(r"«(.*?)»", txt, flags=re.S):
        qn = re.sub(r"\s+", " ", q).strip()
        if len(qn.split()) < 4 or qn in NAO_SAO_DO_OPERADOR:
            continue
        onde = acha(qn)
        R["citacoes"]["%s: %s" % (nome, qn[:90])] = onde[:1] or "NAO ACHADA"
        ok = ok and bool(onde)
# as formas que a errata cita existem no texto (o artigo do ensaio a seco), FORA da secao v385
for lg, formas in (("pt", ["um único postulado", "o único postulado", "o postulado do Um", "$1=1$ deixa de ser postulado e vira o teorema do traço", "axioma único (ω(I)=1)"]),
                   ("en", ["a single postulate", "the single postulate", "the One postulate", "$1=1$ ceases to be a postulate and becomes the trace theorem", "single axiom (ω(I)=1)"])):
    p = os.path.join(DRY, "dry_v385_%s.txt" % lg)
    t = re.sub(r"\s+", " ", open(p, encoding="utf-8").read()) if os.path.exists(p) else ""
    k = t.find("Ao lado (v385)" if lg == "pt" else "Beside (v385)")
    antigo = (t[:k] + t[t.find("Introdução" if lg == "pt" else "Introduction", k):]) if k >= 0 else t
    for f in formas:
        f2 = f.replace("(ω(I)=1)", "")
        achou = (f in antigo) or (f2.strip() in antigo)
        R["formas_da_errata"]["%s: %s" % (lg, f)] = achou
        ok = ok and achou
R["ok"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v385.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:5000])
print("CITACOES:", "TODAS VERBATIM" if ok else "FALHOU")
sys.exit(0 if ok else 1)
