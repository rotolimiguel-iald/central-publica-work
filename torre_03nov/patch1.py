p='secoes.py'
s=open(p,encoding='utf-8').read()
s=s.replace("""        s = dict(segs[k])
        while""","""        s = dict(segs[k]); s["n_h2"] = 1
        while""")
s=s.replace("""            s["fim"] = nxt["fim"]
            k += 1""","""            s["fim"] = nxt["fim"]
            s["n_h2"] += 1
            k += 1""")
s=s.replace("""        out = m.group(1) if m else t[:n]
        if len(out) > n:""","""        out = m.group(1) if m else t[:n]
        if (not m and len(t) > n) or len(out) > n:""")
open(p,'w',encoding='utf-8').write(s)
p='compactar.py'
s=open(p,encoding='utf-8').read()
s=s.replace('bytes_mov=sum(s["bytes"] for s in segs if not s["fica"]), pasta=nome_pasta)','bytes_mov=sum(s["bytes"] for s in segs if not s["fica"]), pasta=nome_pasta, n_h2=sum(s["n_h2"] for s in segs))')
open(p,'w',encoding='utf-8').write(s)
p='gerar_configs.py'
s=open(p,encoding='utf-8').read()
s=s.replace("em {n_total} seções `## `, acima","em {n_total} seções ({n_h2} linhas `## `; títulos partidos em duas linhas contam como uma seção), acima")
open(p,'w',encoding='utf-8').write(s)
