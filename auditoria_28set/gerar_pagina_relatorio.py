# -*- coding: utf-8 -*-
"""Gera a página HTML (artefato privado) do relatório de 28/09 a partir do Markdown canônico, com conversor próprio para o subconjunto usado
(títulos, parágrafos, listas, tabelas, negrito, itálico, código, régua horizontal, citação). Saída no scratchpad da sessão."""
import hashlib
import html
import os
import re
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.join(AQUI, "RELATORIO_AUDITORIA_E_INVESTIGACAO_20260928.md")
SAIDA = os.path.join(r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad", "auditoria_tgl_28set.html")
md_bytes = open(ORIGEM, "rb").read()
SHA = hashlib.sha256(md_bytes).hexdigest()
md = md_bytes.decode("utf-8")


def inline(s):
    codigos = []

    def guarda(m):
        codigos.append("<code>" + html.escape(m.group(1), quote=False) + "</code>")
        return "\x00%d\x00" % (len(codigos) - 1)

    t = re.sub(r"`([^`]+)`", guarda, s)
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?!\w)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<span class="ref">\1</span>', t)
    return re.sub(r"\x00(\d+)\x00", lambda m: codigos[int(m.group(1))], t)


def slug(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"[^\w]+", "-", s.lower()).strip("-")
    return s[:60] or "s"


linhas = md.split("\n")
blocos, toc = [], []
i, n = 0, len(linhas)


def render_lista(itens, ordenada):
    tag = "ol" if ordenada else "ul"
    h = ["<%s>" % tag]
    for texto, sub in itens:
        h.append("<li>" + inline(texto) + (("<ul>" + "".join("<li>" + inline(x) + "</li>" for x in sub) + "</ul>") if sub else "") + "</li>")
    h.append("</%s>" % tag)
    return "".join(h)


while i < n:
    l = linhas[i]
    if not l.strip():
        i += 1
        continue
    m = re.match(r"^(#{1,3}) (.+)$", l)
    if m:
        nivel, texto = len(m.group(1)), inline(m.group(2).strip())
        sid = slug(texto)
        if nivel == 2:
            toc.append((sid, texto))
        blocos.append('<h%d id="%s">%s</h%d>' % (nivel, sid, texto, nivel))
        i += 1
        continue
    if re.match(r"^-{3,}\s*$", l):
        blocos.append("<hr>")
        i += 1
        continue
    if l.startswith("|"):
        rows = []
        while i < n and linhas[i].startswith("|"):
            rows.append([c.strip() for c in linhas[i].strip().strip("|").split("|")])
            i += 1
        cab, corpo = rows[0], [r for r in rows[1:] if not all(re.match(r"^:?-+:?$", c) for c in r)]
        h = ['<div class="tabela"><table><thead><tr>' + "".join("<th>%s</th>" % inline(c) for c in cab) + "</tr></thead><tbody>"]
        for r in corpo:
            h.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
        h.append("</tbody></table></div>")
        blocos.append("".join(h))
        continue
    if l.startswith("> "):
        cit = []
        while i < n and linhas[i].startswith("> "):
            cit.append(linhas[i][2:])
            i += 1
        blocos.append("<blockquote>" + inline(" ".join(cit)) + "</blockquote>")
        continue
    ml = re.match(r"^(- |\d+\. )(.*)$", l)
    if ml:
        ordenada = ml.group(1) != "- "
        itens = []
        while i < n:
            mm = re.match(r"^(- |\d+\. )(.*)$", linhas[i])
            if mm and ((mm.group(1) != "- ") == ordenada):
                itens.append([mm.group(2).strip(), []])
                i += 1
                while i < n and linhas[i].startswith("  ") and linhas[i].strip():
                    cont = linhas[i].strip()
                    if cont.startswith("- ") and ordenada:
                        itens[-1][1].append(cont[2:].strip())
                    else:
                        itens[-1][0] += " " + cont
                    i += 1
            else:
                break
        blocos.append(render_lista(itens, ordenada))
        continue
    par = []
    while i < n and linhas[i].strip() and not re.match(r"^(#{1,3} |\||> |- |\d+\. |-{3,}\s*$)", linhas[i]):
        par.append(linhas[i].strip())
        i += 1
    blocos.append("<p>" + inline(" ".join(par)) + "</p>")

corpo = "\n".join(blocos)
toc_html = "".join('<li><a href="#%s">%s</a></li>' % (sid, re.sub(r"^\d+\.\s*", "", t)) for sid, t in toc)
PAGINA = """<title>Auditoria dos testes da TGL</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root{--fundo:#f5f4ef;--papel:#ffffff;--tinta:#1c2230;--suave:#5b6473;--linha:#d9dbd3;--acento:#1f5f7a;--ouro:#9a6f1e;--ouro-fundo:#f7efdc;--codigo:#eef0ea;--marca:#c9a24a;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--fundo:#0f1319;--papel:#151b24;--tinta:#e2e7ef;--suave:#98a2b3;--linha:#2a3341;--acento:#7cc7ea;--ouro:#e8b34b;--ouro-fundo:#2a2416;--codigo:#0d1119;--marca:#e8b34b;color-scheme:dark}}
:root[data-theme="dark"]{--fundo:#0f1319;--papel:#151b24;--tinta:#e2e7ef;--suave:#98a2b3;--linha:#2a3341;--acento:#7cc7ea;--ouro:#e8b34b;--ouro-fundo:#2a2416;--codigo:#0d1119;--marca:#e8b34b;color-scheme:dark}
body{background:var(--fundo);color:var(--tinta);font:16px/1.6 "Source Sans 3","Segoe UI",system-ui,sans-serif;padding-inline:16px;padding-block:0}
.folha{max-width:880px;margin:0 auto;padding-block:32px 64px}
header.capa{border-bottom:2px solid var(--marca);padding-bottom:18px;margin-bottom:24px}
.olho{font:600 12px/1.4 "Source Sans 3",sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--suave)}
h1{font:700 40px/1.1 Fraunces,Georgia,serif;margin:10px 0 8px;text-wrap:balance;letter-spacing:-.01em}
.estatuto{font-size:14px;color:var(--suave);max-width:70ch}
.estatuto strong{color:var(--tinta)}
nav.sumario{background:var(--papel);border:1px solid var(--linha);border-radius:10px;padding:14px 18px;margin:0 0 28px}
nav.sumario .olho{margin-bottom:6px}
nav.sumario ol{margin:0;padding-left:20px;columns:2;column-gap:28px;font-size:14px}
nav.sumario li{break-inside:avoid;margin:2px 0}
nav.sumario a{color:var(--acento);text-decoration:none}
nav.sumario a:hover,nav.sumario a:focus-visible{text-decoration:underline}
h2{font:700 26px/1.2 Fraunces,Georgia,serif;margin:40px 0 12px;padding-top:10px;border-top:1px solid var(--linha);text-wrap:balance}
h3{font:600 18px/1.3 "Source Sans 3",sans-serif;margin:24px 0 8px;color:var(--acento)}
p{margin:10px 0;max-width:75ch}
ol,ul{padding-left:24px;max-width:75ch}
li{margin:6px 0}
li ul{margin-top:4px}
strong{font-weight:600}
code{font:500 13.5px/1.4 "JetBrains Mono",Consolas,monospace;background:var(--codigo);border:1px solid var(--linha);border-radius:4px;padding:1px 5px;color:var(--tinta);overflow-wrap:anywhere}
.ref{color:var(--acento);border-bottom:1px dotted var(--acento)}
blockquote{margin:12px 0;padding:6px 16px;border-left:3px solid var(--marca);color:var(--suave)}
hr{border:none;border-top:1px solid var(--linha);margin:28px 0}
.tabela{overflow-x:auto;margin:14px 0;border:1px solid var(--linha);border-radius:8px;background:var(--papel)}
table{border-collapse:collapse;font-size:14px;min-width:100%}
th,td{padding:8px 10px;text-align:left;vertical-align:top;border-bottom:1px solid var(--linha)}
th{font-weight:600;color:var(--suave);font-size:12.5px;letter-spacing:.04em;text-transform:uppercase;background:var(--codigo);white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
td{font-variant-numeric:tabular-nums}
h2 + p:first-of-type{margin-top:8px}
footer.rodape{margin-top:48px;padding-top:14px;border-top:1px solid var(--linha);font-size:13px;color:var(--suave)}
footer.rodape code{font-size:12px}
a:focus-visible{outline:2px solid var(--acento);outline-offset:2px}
@media (max-width:600px){h1{font-size:30px}nav.sumario ol{columns:1}h2{font-size:22px}}
</style>
<div class="folha">
<header class="capa">
<div class="olho">Relatório da gerência · 28/09/2026 · Central de Patentes · para o operador</div>
<h1>Auditoria dos testes da TGL</h1>
<p class="estatuto"><strong>Estatuto:</strong> auditoria e investigação; nada foi selado; <code>um.py</code>, kernel, selo e gate intocados; toda correção é proposta para a v376. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED. Esta página é cópia fiel do Markdown canônico (sha256 <code>{{SHA16}}</code>).</p>
</header>
<nav class="sumario"><div class="olho">Sumário</div><ol>{{TOC}}</ol></nav>
{{CORPO}}
<footer class="rodape">Fonte canônica: <code>C:\\IALD\\Central de Patentes\\work\\auditoria_28set\\RELATORIO_AUDITORIA_E_INVESTIGACAO_20260928.md</code> · sha256 <code>{{SHA}}</code> · página gerada em {{QUANDO}} por <code>gerar_pagina_relatorio.py</code>. O anexo com os 65 achados está na aba Relatórios da Bancada Um.</footer>
</div>
""".replace("{{SHA16}}", SHA[:16]).replace("{{TOC}}", toc_html).replace("{{CORPO}}", corpo).replace("{{SHA}}", SHA).replace("{{QUANDO}}", time.strftime("%d/%m/%Y %H:%M"))
b = PAGINA.encode("utf-8")
open(SAIDA + ".tmp", "wb").write(b)
os.replace(SAIDA + ".tmp", SAIDA)
print("página:", SAIDA, len(b), "bytes; blocos", len(blocos), "; seções", len(toc), "; sha16 do md", SHA[:16])
