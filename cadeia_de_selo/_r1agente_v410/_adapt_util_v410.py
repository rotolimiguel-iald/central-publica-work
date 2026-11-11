# -*- coding: utf-8 -*-
"""_adapt_util_v410.py -- (claude-construtor-v410, 06/11/2026) as trocas da adaptacao, com CONTAGEM EXATA: aplicar(arquivo, trocas, nota=None).
- backup de BYTES <arquivo>.bak_<ts>_adapt antes de tocar; escreve por temporario -> confere o tamanho -> substitui;
- o fim de linha e' respeitado: se o arquivo e' CRLF, os padroes (escritos com \\n) sao trocados com \\r\\n;
- cada troca (antigo, novo, n) tem de casar EXATAMENTE n vezes (senao PARA e diz a contagem); n = None aceita >= 1 e diz quantas;
- `nota`: troca a marca `# [A ADAPTAR v410] ...` (se houver) por `# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] <nota>` e devolve ao rotulo verdadeiro as marcas herdadas da v409 que o bump subiu;
- .py: ast.parse; .sh: sh -n."""
import ast, datetime, os, subprocess

_TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def aplicar(p, trocas, nota=None, conferir=True):
    raw = open(p, "rb").read(); t = raw.decode("utf-8")
    crlf = "\r\n" in t and t.count("\r\n") == t.count("\n")
    rel = []
    for a, b, n in trocas:
        if crlf:
            a, b = a.replace("\r\n", "\n").replace("\n", "\r\n"), b.replace("\r\n", "\n").replace("\n", "\r\n")
        c = t.count(a)
        if n is None:
            assert c >= 1, ("TROCA NAO CASOU NENHUMA VEZ", os.path.basename(p), a[:160])
        else:
            assert c == n, ("TROCA NAO CASOU %d VEZ(ES) (casou %d)" % (n, c), os.path.basename(p), a[:160])
        t = t.replace(a, b); rel.append(c)
    if nota is not None:
        ls = t.split("\n")
        idx = [i for i, l in enumerate(ls[:4]) if l.startswith("# [A ADAPTAR v410]")]
        if idx:
            cr = "\r" if ls[idx[0]].endswith("\r") else ""
            ls[idx[0]] = "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] " + nota + cr
        for k, l in enumerate(ls):
            if l.startswith("#") and "[ADAPTADO v410, 05/11/2026, claude-construtor-v410]" in l:
                ls[k] = l.replace("[ADAPTADO v410, 05/11/2026, claude-construtor-v410]", "[ADAPTADO v409, 05/11/2026, claude-construtor-v409 -- marca herdada da v409]")
        t = "\n".join(ls)
    novo = t.encode("utf-8")
    if novo == raw:
        print(os.path.basename(p), "IGUAL (nada a trocar)")
        return rel
    if conferir and p.endswith(".py"):
        ast.parse(t)
    if conferir and p.endswith(".sh"):
        r = subprocess.run(["sh", "-n"], input=novo, capture_output=True); assert r.returncode == 0, (p, r.stderr[:300])
    bk = p + ".bak_" + _TS + "_adapt"
    if not os.path.exists(bk):
        open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
    print(os.path.basename(p), "trocas:", rel, "| bytes", len(raw), "->", len(novo))
    return rel
