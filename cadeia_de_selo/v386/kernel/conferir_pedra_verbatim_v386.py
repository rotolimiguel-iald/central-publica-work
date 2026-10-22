# -*- coding: utf-8 -*-
"""conferir_pedra_verbatim_v386.py -- confere, por script, TODAS as citacoes «…» da pedra TGLExt/TheVerbSelectsTheAction.lean (sandbox) contra os DOIS
arquivos do operador (VERBO_operador_05out.txt, RESPOSTAS_operador_05out.txt), EXATAS (sem casefold). Normaliza SO: (a) espacos/quebras colapsados;
(b) LaTeX -> Unicode onde a pedra transliterou, pela TABELA abaixo (cada uso e' dito no relatorio). Cada pedaco (separado por «…», o corte) e' procurado NA
ORDEM no MESMO arquivo. Tres excecoes DECLARADAS: (1) a frase «estado dinamico estacionado» / «a posicao e' o estado dinamico estacionado…» vem da mensagem
do operador de 2026-10-05T11:19:54 UTC (conferida AQUI no transcrito desta sessao, type=user); (2) «decidido por delegacao» e' frase da gerencia (a pedra o diz);
(3) «…» sozinho e' o sinal de corte. Qualquer outra divergencia e' FALHA (rc 1). Grava CONFERENCIA_PEDRA_VERBATIM_v386.json."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.dirname(HERE); SP = os.path.dirname(V6)
KS = os.path.join(SP, "v376", "kernel_src")
P = os.path.join(KS, "TGLExt", "TheVerbSelectsTheAction.lean")
TR = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
ws = lambda s: re.sub(r"\s+", " ", s).strip()
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
FONTES = {"VERBO_operador_05out.txt": ws(open(os.path.join(V6, "VERBO_operador_05out.txt"), encoding="utf-8").read()),
          "RESPOSTAS_operador_05out.txt": ws(open(os.path.join(V6, "RESPOSTAS_operador_05out.txt"), encoding="utf-8").read())}
FONTES_SHA = {k: sha(os.path.join(V6, k)) for k in FONTES}
# a tabela: Unicode na pedra -> LaTeX cru do operador (o que ele escreveu)
TABELA = {"𝒱 = |a⟩⟨a|": r"\mathcal{V} = |a\rangle \langle a|",
          "ℛ(𝒱) = 𝒱 (ponto fixo)": r"\mathcal{R}(\mathcal{V}) = \mathcal{V} \quad \text{(ponto fixo)}",
          "núcleo Π": r"núcleo \Pi",
          "Nome = lim_{t→∞} 𝒱(t)": r"\text{Nome} = \lim_{t \to \infty} \mathcal{V}(t)",
          "α²": r"\alpha^2", "D_folds = 0,74": r"D_{\text{folds}} = 0{,}74", "g = √|L|": r"g = \sqrt{|L|}", "−εΠ": r"-\varepsilon \Pi", "δS = 0": r"\delta S = 0"}
# a mensagem de 11:19:54 UTC no transcrito (a 3a fonte, declarada no cabecalho da pedra)
MSG_1119 = None
for ln in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(ln)
    except ValueError:
        continue
    if d.get("type") != "user" or d.get("isCompactSummary") or d.get("isMeta") or not str(d.get("timestamp", "")).startswith("2026-10-05T11:19:54"):
        continue
    c = d.get("message", {}).get("content"); tx = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    MSG_1119 = ws(" ".join(tx)); MSG_TS = d.get("timestamp")
assert MSG_1119, "a mensagem de 2026-10-05T11:19:54 UTC nao foi achada no transcrito"
DECLARADAS_1119 = {"estado dinâmico estacionado", "a posição é o estado dinâmico estacionado como portador do conteúdo da inscrição"}
DECLARADAS_GERENCIA = {"decidido por delegação"}

pedra = open(P, encoding="utf-8").read()
cits = re.findall(r"«(.*?)»", pedra, flags=re.S)
R = {"pedra": P, "pedra_sha256": sha(P), "fontes_sha256": FONTES_SHA, "mensagem_11_19_54": {"quando": MSG_TS, "chars": len(MSG_1119)}, "n_citacoes": len(cits),
     "normalizacao_declarada": ["espacos/quebras colapsados", "LaTeX->Unicode pela TABELA (uso dito por citacao)", "sem casefold"], "tabela": TABELA, "citacoes": [], "divergencias": []}
for q in cits:
    qn = ws(q)
    pedacos = [ws(p) for p in qn.split("…") if ws(p)]
    item = {"citacao": qn[:160], "pedacos": len(pedacos)}
    if not pedacos:
        item["status"] = "SO_O_SINAL_DE_CORTE"; R["citacoes"].append(item); continue
    if qn in DECLARADAS_GERENCIA:
        item["status"] = "FRASE_DA_GERENCIA (declarada na pedra; nao e' citacao do operador)"; R["citacoes"].append(item); continue
    if qn in DECLARADAS_1119:
        item["status"] = "EXATA no transcrito, mensagem %s" % MSG_TS if qn in MSG_1119 else "DIVERGENCIA (nao esta na mensagem de 11:19:54)"
        if "DIVERGENCIA" in item["status"]:
            R["divergencias"].append(item)
        R["citacoes"].append(item); continue
    usados = []
    pecas = []
    for p in pedacos:
        p2 = p
        for uni, latex in TABELA.items():
            if uni in p2:
                p2 = p2.replace(uni, latex); usados.append(uni)
        pecas.append(ws(p2))
    achado = None
    for nome, txt in FONTES.items():
        i = 0; ok = True
        for p in pecas:
            j = txt.find(p, i)
            if j < 0:
                ok = False; break
            i = j + len(p)
        if ok:
            achado = nome; break
    item["tabela_usada"] = sorted(set(usados)) or None
    if achado:
        item["status"] = "EXATA em %s" % achado + (" (LaTeX->Unicode pela tabela)" if usados else "")
    else:
        item["status"] = "DIVERGENCIA"; item["pecas_procuradas"] = pecas
        R["divergencias"].append(item)
    R["citacoes"].append(item)
R["n_exatas_nos_arquivos"] = sum(1 for c in R["citacoes"] if c["status"].startswith("EXATA em "))
R["n_com_tabela"] = sum(1 for c in R["citacoes"] if c.get("tabela_usada"))
R["n_do_transcrito_11_19_54"] = sum(1 for c in R["citacoes"] if "transcrito" in c["status"])
R["n_gerencia"] = sum(1 for c in R["citacoes"] if c["status"].startswith("FRASE_DA_GERENCIA"))
R["n_so_corte"] = sum(1 for c in R["citacoes"] if c["status"] == "SO_O_SINAL_DE_CORTE")
R["n_divergencias"] = len(R["divergencias"])
R["sic_fora_das_aspas"] = len(re.findall(r"» \[sic\]", pedra))
R["ok"] = R["n_divergencias"] == 0
json.dump(R, open(os.path.join(HERE, "CONFERENCIA_PEDRA_VERBATIM_v386.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("pedra_sha256", "n_citacoes", "n_exatas_nos_arquivos", "n_com_tabela", "n_do_transcrito_11_19_54", "n_gerencia", "n_so_corte", "n_divergencias", "sic_fora_das_aspas", "ok")}, ensure_ascii=False, indent=1))
for d in R["divergencias"]:
    print("DIVERGENCIA:", json.dumps(d, ensure_ascii=False)[:600])
sys.exit(0 if R["ok"] else 1)
