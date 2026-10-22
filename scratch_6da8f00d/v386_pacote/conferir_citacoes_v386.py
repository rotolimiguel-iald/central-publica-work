# -*- coding: utf-8 -*-
"""conferir_citacoes_v386.py -- confere, por script, que toda citacao do operador na v386 esta VERBATIM numa MENSAGEM DE ENTRADA DO OPERADOR, SEM BLOCO COLADO
MARCADO (molde: conferir_citacoes_v385.py; a regua nº 1: nunca fabricar citacao):
  * o que conta como palavra do operador: mensagens do tipo user e queued_command, SEM o resumo de compactacao (isCompactSummary) nem as meta (isMeta), com os
    blocos <pasted_content ...>...</pasted_content ...> CORTADOS e so o texto puro (nada que comece com «<»); transcritos: esta sessao (05/10) E a d554e796 (20/08);
  * ESTRITO (decide o rc): (a) os trechos entre `` e '' dos .pysnip PT e EN que nao estao na lista NAO_SAO_DO_OPERADOR (frases da gerencia/do artigo antigo,
    ditas); (b) os «…» de 4+ palavras dos comentarios de v386_runtime.py (a logica da gerencia) -- cada pedaco (separado por «…», a lacuna) NA ORDEM, na MESMA
    mensagem; o EN cita as MESMAS do PT; e as formas que a errata cita EXISTEM onde ela diz (o R6 da v383 no core selado; a frase da secao v385 no artigo);
  * INFORMATIVO (nao decide o rc, mas e' impresso e gravado): os «…» de 4+ palavras da pedra TGLExt/TheVerbSelectsTheAction.lean e do comentario v386 do
    TGL/Audit.lean (fase A; compilados e auditados -- so a gerencia os muda): com a tabela de FORMULAS (o LaTeX do operador renderizado em Unicode na pedra);
    o que NAO acha fica listado como NAO_VERBATIM_NA_PEDRA, para a gerencia decidir uma revisao da pedra.
  Normaliza so: \\texttt{x} -> x; `x' -> "x"; barras; espacos; casefold (uma inicial minuscula no meio de frase e' pratica editorial -- dito).
  Grava, para cada citacao, o carimbo e o TAMANHO da mensagem onde acha (leitura humana). Uso: python conferir_citacoes_v386.py [dry_dir]. Sai 0 se o estrito bate."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.dirname(HERE); SP = os.path.dirname(V6)
MP = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
TRS = [os.path.join(MP, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"), os.path.join(MP, "d554e796-415e-450f-9fd4-dd07892b02b9.jsonl")]
K = os.path.join(SP, "v376", "kernel_src")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
DRY = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "dry_v386")
NAO_SAO_DO_OPERADOR = {"o ramo B segue ENCERRADO", "O pilar rodou de novo, inteiro", "a natureza decidiu", "nature has decided"}
# o LaTeX do operador (16:53) renderizado em Unicode nas docstrings da pedra: a TABELA diz QUAL fonte LaTeX cada rendering cita (Unicode na pedra -> LaTeX cru do
# operador; acha() tira as barras dos dois lados). Desde a revisao verbatim da pedra (05/10, noite) nao ha mais parafrases entre «» (sequência 𝒱ⁿ(a); 𝒱(t) = U 𝒱(0) U*;
# i·(constante); 1 = (1 − β) + β sairam das «»); a formula da comutacao esta no LaTeX do operador tal qual. A 3a fonte da pedra -- UMA frase («a posição é o estado
# dinâmico estacionado…») -- vem da mensagem do operador de 2026-10-05T11:19:54 UTC (transcrito desta sessao): acha() a encontra la, com o carimbo.
TABELA = {"𝒱 = |a⟩⟨a|": r"\mathcal{V} = |a\rangle \langle a|", "ℛ(𝒱) = 𝒱 (ponto fixo)": r"\mathcal{R}(\mathcal{V}) = \mathcal{V} \quad \text{(ponto fixo)}",
          "núcleo Π": r"núcleo \Pi", "Nome = lim_{t→∞} 𝒱(t)": r"\text{Nome} = \lim_{t \to \infty} \mathcal{V}(t)",
          "α²": r"\alpha^2", "D_folds = 0,74": r"D_{\text{folds}} = 0{,}74", "g = √|L|": r"g = \sqrt{|L|}", "−εΠ": r"-\varepsilon \Pi", "δS = 0": r"\delta S = 0"}
PASTED = re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S)


def norm(t):
    t = re.sub(r"\\texttt\{([^}]*)\}", r"\1", t)
    t = re.sub(r"`([^`']*)'", r'"\1"', t)
    t = t.replace("\\", "")
    return re.sub(r"\s+", " ", t).strip().casefold()


msgs = []; raw = []; puladas = {"compact_ou_meta": 0, "blocos_colados_cortados": 0}
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
                msgs.append((d.get("timestamp"), norm(t2))); raw.append((d.get("timestamp"), re.sub(r"\s+", " ", t2)))


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


def acha_cru(q):
    """a fonte LaTeX, crua (sem normalizar barras), na mesma mensagem."""
    qq = re.sub(r"\s+", " ", q)
    return [{"quando": ts, "tamanho_da_mensagem": len(m)} for ts, m in raw if qq in m]


R = {"mensagens_do_operador": len(msgs), "puladas": puladas, "estrito": {}, "pedra_informativo": {}, "formas_da_errata": {}}
ok = True
por_lingua = {}
for lg in ("pt", "en"):
    src = open(os.path.join(HERE, "artigo_%s_v386.pysnip" % lg), encoding="utf-8").read()
    cits = [c for c in re.findall(r"``(.*?)''", src, flags=re.S) if c not in NAO_SAO_DO_OPERADOR]
    por_lingua[lg] = cits
    for c in cits:
        onde = acha(c)
        R["estrito"]["artigo %s: %s" % (lg, norm(c)[:90])] = onde[:1] or "NAO ACHADA"
        ok = ok and bool(onde)
R["en_cita_as_mesmas_do_pt"] = sorted(map(norm, por_lingua["en"])) == sorted(map(norm, por_lingua["pt"]))
ok = ok and R["en_cita_as_mesmas_do_pt"]
rt = open(os.path.join(HERE, "v386_runtime.py"), encoding="utf-8").read()
rt = re.sub(r"\n#\s*", " ", rt)   # os comentarios continuam na linha seguinte com «# »: a citacao atravessa a quebra
for q in re.findall(r"«(.*?)»", rt, flags=re.S):
    qn = re.sub(r"\s+", " ", q).strip()
    if len(qn.split()) < 4 or qn in NAO_SAO_DO_OPERADOR or qn.startswith("decidido por"):
        continue
    onde = acha(qn)
    R["estrito"]["runtime: %s" % qn[:90]] = onde[:1] or "NAO ACHADA"
    ok = ok and bool(onde)
# as formas que a errata cita existem onde ela diz
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
R["formas_da_errata"]["R6 da v383 no core selado: «o ramo B segue ENCERRADO»"] = "o ramo B segue ENCERRADO" in str(core0["the_ledger_of_charges_v383"]["corrections_beside_20261002"]["R6"])
R["formas_da_errata"]["F2 da v383 no core selado: «ramo B ENCERRADO»"] = any("ramo B ENCERRADO" in str(c.get("law")) for c in core0["the_ledger_of_charges_v383"]["ledger"] if c.get("id") == "F2")
for lg, frase, marca in (("pt", "O pilar rodou de novo, inteiro", "Ao lado (v385)"), ("en", "The pillar ran again, whole", "Beside (v385)")):
    p = os.path.join(DRY, "dry_v386_%s.txt" % lg)
    t = re.sub(r"\s+", " ", open(p, encoding="utf-8").read()) if os.path.exists(p) else ""
    k = t.find(marca)
    R["formas_da_errata"]["%s: «%s» na secao v385 do artigo" % (lg, frase)] = (k >= 0 and frase in t[k:k + 12000]) if t else "SEM_TXT_DO_ENSAIO"
    if t:
        ok = ok and R["formas_da_errata"]["%s: «%s» na secao v385 do artigo" % (lg, frase)]
ok = ok and all(v is True for k_, v in R["formas_da_errata"].items() if "core selado" in k_)
# INFORMATIVO: a pedra e o comentario v386 do Audit.lean
pedra = open(os.path.join(K, "TGLExt", "TheVerbSelectsTheAction.lean"), encoding="utf-8").read()
au = open(os.path.join(K, "TGL", "Audit.lean"), encoding="utf-8").read(); au = au[au.index("-- 2026-10-05, v386"):].split("\n", 1)[0]
nao_verbatim_pedra = []
for nome, txt in (("pedra", pedra), ("Audit.lean", au)):
    for q in re.findall(r"«(.*?)»", txt, flags=re.S):
        qn = re.sub(r"\s+", " ", q).strip()
        if len(qn.split()) < 4 or qn.startswith("decidido por"):
            continue
        onde = acha(qn); via = None
        if not onde:
            # o Unicode da pedra -> o LaTeX cru do operador (pela TABELA), dentro de cada pedaco; depois a busca normal (pedacos NA ORDEM, mesma mensagem)
            qt = qn
            for uni, latex in TABELA.items():
                qt = qt.replace(uni, latex)
            if qt != qn:
                onde = acha(qt); via = "FORMULA_RENDERIZADA_OK (LaTeX->Unicode pela tabela)" if onde else None
        status = (([dict(onde[0], via=via)] if via else onde[:1]) if onde else "NAO_VERBATIM_NA_PEDRA")
        R["pedra_informativo"]["%s: %s" % (nome, qn[:100])] = status
        if status == "NAO_VERBATIM_NA_PEDRA":
            nao_verbatim_pedra.append("%s: %s" % (nome, qn[:120]))
R["pedra_nao_verbatim"] = nao_verbatim_pedra
ok = ok and not nao_verbatim_pedra   # v386 (05/10, noite): a pedra foi revisada para VERBATIM -- desde entao as «» da pedra tambem DECIDEM o rc
R["ok"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v386.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("mensagens_do_operador", "puladas", "estrito", "en_cita_as_mesmas_do_pt", "formas_da_errata")}, ensure_ascii=False, indent=1)[:7000])
print("PEDRA (estrito desde a revisao verbatim de 05/10): %d citacoes «» nao verbatim -> %s" % (len(nao_verbatim_pedra), nao_verbatim_pedra))
print("CITACOES (estrito: artigo + runtime + formas da errata + pedra/Audit):", "TODAS VERBATIM" if ok else "FALHOU")
sys.exit(0 if ok else 1)
