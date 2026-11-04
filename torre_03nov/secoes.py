"""Segmentacao de CLAUDE.md em preambulo + secoes '## ' (fora de cercas ```), em BYTES.
Secoes minusculas (< 100 B) cujo titulo continua na linha '## ' seguinte sao fundidas com a seguinte
(titulos partidos em duas linhas '## ' pelo arquivo original)."""
import re

def segmentar(b):
    """Devolve (preambulo_bytes, [ {ini, fim, linha_ini, titulo(str), corpo_bytes} ... ])  em offsets de bytes; cobre b inteiro."""
    lines = b.split(b'\n')
    offs = []
    o = 0
    for l in lines:
        offs.append(o); o += len(l) + 1
    incode = False
    cab = []  # (indice_linha, offset)
    for i, l in enumerate(lines):
        ls = l.rstrip(b'\r')
        if ls.lstrip().startswith(b'```'):
            incode = not incode
        if not incode and ls.startswith(b'## '):
            cab.append(i)
    if not cab:
        return b, []
    segs = []
    for k, i in enumerate(cab):
        ini = offs[i]
        fim = offs[cab[k+1]] if k+1 < len(cab) else len(b)
        segs.append({"ini": ini, "fim": fim, "linha_ini": i+1, "titulo": lines[i].rstrip(b'\r')[3:].decode('utf8')})
    # fundir secoes minusculas (titulo partido) com a seguinte
    fund = []
    k = 0
    while k < len(segs):
        s = dict(segs[k]); s["n_h2"] = 1
        while (s["fim"] - s["ini"]) < 100 and k+1 < len(segs):
            nxt = segs[k+1]
            s["titulo"] = s["titulo"] + " " + nxt["titulo"]
            s["fim"] = nxt["fim"]
            s["n_h2"] += 1
            k += 1
        fund.append(s); k += 1
    for s in fund:
        s["linha_fim"] = b[:s["fim"]].count(b'\n')  # ultima linha (1-based) que a secao ocupa
        s["bytes"] = s["fim"] - s["ini"]
    pre = b[:fund[0]["ini"]]
    return pre, fund

def gancho(corpo, n=150):
    """Primeira frase util do corpo (sem titulo, comentarios HTML, separadores, tabelas)."""
    txt = corpo.decode('utf8', 'replace')
    ls = txt.split('\n')[1:]
    for l in ls:
        t = l.strip().replace('\r', '')
        if not t or t.startswith('<!--') or t.startswith('---') or t.startswith('|') or t.startswith('```') or t.startswith('#'):
            continue
        t = re.sub(r'^(?:[>\-\*]\s+|\d+[\.\)]\s+)+', '', t)
        t = re.sub(r'\*\*|`|__', '', t)
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) < 12:
            continue
        m = re.match(r'(.{25,%d}?[\.\:\;])(\s|$)' % n, t)
        out = m.group(1) if m else t[:n]
        if (not m and len(t) > n) or len(out) > n:
            out = out[:n-1].rstrip() + '…'
        return out
    return ''
