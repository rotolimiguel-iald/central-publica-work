"""Compacta um CLAUDE.md SEM PERDER UM BYTE: as secoes '## ' historicas viram arquivos CLAUDE_memoria/NNN_slug.md
(BYTES exatos da secao), e o CLAUDE.md ganha um indice no lugar. Prova de nao-perda por reconstrucao byte a byte.

Uso: compactar.py <config.json> [--aplicar]
Sem --aplicar: so o plano e a prova EM MEMORIA (nada e escrito).
Com --aplicar: grava as partes (pasta nova), a prova, e so entao substitui o CLAUDE.md (temporario -> conferir -> os.replace).
"""
import sys, os, re, json, hashlib, time, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from secoes import segmentar, gancho

MAX_PARTE = 56 * 1024          # alvo de tamanho de cada subparte quando a secao e dividida
LIMIAR_DIVIDIR = 90 * 1024     # secoes acima disto sao divididas em '### '
NOTA_INI = b"<!-- CLAUDE_MEMORIA_NOTA:INICIO -->\n"
NOTA_FIM = b"<!-- CLAUDE_MEMORIA_NOTA:FIM -->\n"
IND_INI = b"<!-- CLAUDE_MEMORIA_INDICE:INICIO"
IND_FIM = b"<!-- CLAUDE_MEMORIA_INDICE:FIM -->\n"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def slug(t, n=46):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return (s[:n].rstrip("_")) or "secao"


def dividir(seg):
    """Divide os bytes de uma secao grande em subpartes nos cabecalhos '### ' (fora de cercas)."""
    lines = seg.split(b"\n")
    offs, o = [], 0
    for l in lines:
        offs.append(o); o += len(l) + 1
    incode, cortes = False, [0]
    for i, l in enumerate(lines):
        ls = l.rstrip(b"\r")
        if ls.lstrip().startswith(b"```"):
            incode = not incode
        if not incode and ls.startswith(b"### ") and offs[i] > 0:
            cortes.append(offs[i])
    cortes.append(len(seg))
    subs = [(cortes[k], cortes[k + 1]) for k in range(len(cortes) - 1)]
    partes, ini, fim = [], subs[0][0], subs[0][0]
    for (a, z) in subs:
        if (z - ini) > MAX_PARTE and fim > ini:
            partes.append((ini, fim)); ini = a
        fim = z
    partes.append((ini, fim))
    assert partes[0][0] == 0 and partes[-1][1] == len(seg)
    for k in range(len(partes) - 1):
        assert partes[k][1] == partes[k + 1][0]
    return partes


def primeiro_titulo_h3(bytes_):
    for l in bytes_.split(b"\n"):
        ls = l.rstrip(b"\r")
        if ls.startswith(b"### "):
            return ls[4:].decode("utf8", "replace")
    return None


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    aplicar = "--aplicar" in sys.argv
    path = cfg["arquivo"]
    b = open(path, "rb").read()
    h0 = sha(b)
    assert h0 == cfg["sha256_esperado"], "o arquivo mudou desde o backup (CAS): %s != %s" % (h0, cfg["sha256_esperado"])
    pre, segs = segmentar(b)
    n = len(segs)
    # --- decidir o que fica
    keep_idx = set(cfg.get("manter_indices", []))
    keep_re = [re.compile(r) for r in cfg.get("manter_titulo_regex", [])]
    for k, s in enumerate(segs):
        s["k"] = k
        s["fica"] = (k in keep_idx) or any(r.search(s["titulo"]) for r in keep_re)
    # asserção de títulos dos índices fixos (para não errar de seção)
    for k, prefixo in cfg.get("assegurar_prefixo_titulo", {}).items():
        assert segs[int(k)]["titulo"].startswith(prefixo), (k, segs[int(k)]["titulo"], prefixo)
    pasta = os.path.join(os.path.dirname(path), "CLAUDE_memoria")
    nome_pasta = "CLAUDE_memoria"
    # --- montar as partes (bytes exatos)
    partes = []   # lista na ordem original: dicts {k, arquivo, bytes(offsets), ...}
    for s in segs:
        if s["fica"]:
            continue
        seg = b[s["ini"]:s["fim"]]
        base = "%03d_%s" % (s["k"] + 1, slug(s["titulo"]))
        s["gancho"] = gancho(seg, 100)
        if len(seg) > LIMIAR_DIVIDIR:
            ps = dividir(seg)
            s["arquivos"] = []
            for j, (a, z) in enumerate(ps, 1):
                fn = "%s_p%02d.md" % (base, j)
                s["arquivos"].append({"arquivo": fn, "ini": s["ini"] + a, "fim": s["ini"] + z, "bytes": z - a,
                                      "h3": primeiro_titulo_h3(seg[a:z]) or "(cabecalho da secao)"})
        else:
            s["arquivos"] = [{"arquivo": base + ".md", "ini": s["ini"], "fim": s["fim"], "bytes": s["bytes"], "h3": None}]
        for a in s["arquivos"]:
            a["sha256"] = sha(b[a["ini"]:a["fim"]])
            partes.append(a)
    # --- compor o CLAUDE.md compactado: preambulo + NOTA + (secoes mantidas | blocos de indice)
    out = bytearray()
    out += pre
    nota = cfg["nota"].format(
        sha_original=h0, bytes_original=len(b), backup=cfg["backup"], data=cfg["data"],
        n_mov=sum(1 for s in segs if not s["fica"]), n_total=n, n_partes=len(partes),
        bytes_mov=sum(s["bytes"] for s in segs if not s["fica"]), pasta=nome_pasta, n_h2=sum(s["n_h2"] for s in segs))
    out += NOTA_INI + nota.encode("utf8") + b"\n" + NOTA_FIM
    k = 0
    blocos = 0
    while k < n:
        s = segs[k]
        if s["fica"]:
            out += b[s["ini"]:s["fim"]]
            k += 1
            continue
        j = k
        while j < n and not segs[j]["fica"]:
            j += 1
        run = segs[k:j]
        blocos += 1
        txt = []
        txt.append("Seções movidas (%d, de §%d a §%d da ordem original) · leia sob demanda; nada daqui foi cortado." % (len(run), run[0]["k"] + 1, run[-1]["k"] + 1))
        for s2 in run:
            t = s2["titulo"]
            t = t.replace("`", "'")
            t = (t[:100].rstrip() + "…") if len(t) > 100 else t
            ll = "L%d–%d" % (s2["linha_ini"], s2["linha_fim"])
            if len(s2["arquivos"]) == 1:
                txt.append("- **%03d %s** · %s · %d B — %s → `%s/%s`" % (s2["k"] + 1, t, ll, s2["bytes"], s2["gancho"], nome_pasta, s2["arquivos"][0]["arquivo"]))
            else:
                txt.append("- **%03d %s** · %s · %d B — %s → %d partes:" % (s2["k"] + 1, t, ll, s2["bytes"], s2["gancho"], len(s2["arquivos"])))
                for a in s2["arquivos"]:
                    h3 = a["h3"]
                    h3 = (h3[:80] + "…") if len(h3) > 80 else h3
                    txt.append("  - `%s/%s` · %d B · a partir de «%s»" % (nome_pasta, a["arquivo"], a["bytes"], h3))
        cab = (IND_INI + (" n=%d seq=%d-%d -->\n" % (len(run), run[0]["k"] + 1, run[-1]["k"] + 1)).encode("utf8"))
        out += cab + ("\n".join(txt) + "\n").encode("utf8") + IND_FIM
        k = j
    comp = bytes(out)
    # --- PROVA: reconstruir o original a partir do compactado + partes (somente com o que sera gravado)
    rec = reconstruir(comp, {a["arquivo"]: b[a["ini"]:a["fim"]] for a in partes}, [p["arquivo"] for p in partes], segs)
    ok = (rec == b)
    # prova auxiliar por linha: o multiconjunto de linhas
    prova = {
        "arquivo": path, "data": cfg["data"], "metodo": "reconstrucao: compactado sem NOTA, cada bloco de INDICE trocado pelas partes na ordem == original byte a byte",
        "original": {"bytes": len(b), "sha256": h0, "backup": cfg["backup"]},
        "compactado": {"bytes": len(comp), "sha256": sha(comp)},
        "reconstruido": {"bytes": len(rec), "sha256": sha(rec)},
        "byte_a_byte_igual": ok,
        "secoes": n, "secoes_mantidas": sum(1 for s in segs if s["fica"]), "secoes_movidas": sum(1 for s in segs if not s["fica"]),
        "arquivos_de_parte": len(partes), "blocos_de_indice": blocos,
        "bytes_nas_partes": sum(a["bytes"] for a in partes),
        "bytes_mantidos_do_original": sum(s["bytes"] for s in segs if s["fica"]) + len(pre),
        "tamanho_do_indice_e_nota": len(comp) - (sum(s["bytes"] for s in segs if s["fica"]) + len(pre)),
        "partes": [{"arquivo": a["arquivo"], "bytes": a["bytes"], "sha256": a["sha256"]} for a in partes],
        "mantidas": [{"seq": s["k"] + 1, "titulo": s["titulo"][:120], "bytes": s["bytes"]} for s in segs if s["fica"]],
    }
    print(json.dumps({k2: v for k2, v in prova.items() if k2 not in ("partes", "mantidas")}, ensure_ascii=False, indent=1))
    if not ok:
        print("PROVA FALHOU - nada sera substituido"); sys.exit(2)
    if not aplicar:
        print("(plano: nada gravado)")
        open(cfg["saida_previa"], "wb").write(comp)
        return
    # --- aplicar
    assert not os.path.exists(pasta) or not os.listdir(pasta), "pasta CLAUDE_memoria ja existe e nao esta vazia"
    os.makedirs(pasta, exist_ok=True)
    for a in partes:
        fp = os.path.join(pasta, a["arquivo"])
        assert not os.path.exists(fp)
        with open(fp, "wb") as f:
            f.write(b[a["ini"]:a["fim"]])
        lido = open(fp, "rb").read()
        assert sha(lido) == a["sha256"] and len(lido) == a["bytes"], a["arquivo"]
    leia = cfg["leia_me"].format(sha_original=h0, backup=cfg["backup"], data=cfg["data"], n=len(partes))
    open(os.path.join(pasta, "LEIA-ME.md"), "wb").write(leia.encode("utf8"))
    # reconferir a prova LENDO as partes do disco
    partes_disco = {a["arquivo"]: open(os.path.join(pasta, a["arquivo"]), "rb").read() for a in partes}
    rec2 = reconstruir(comp, partes_disco, [p["arquivo"] for p in partes], segs)
    assert rec2 == b, "reconstrucao a partir do disco difere"
    prova["reconstruido_do_disco"] = {"bytes": len(rec2), "sha256": sha(rec2), "igual_ao_original": True}
    prova["pasta_partes"] = pasta
    json.dump(prova, open(cfg["prova"], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # CAS final e substituicao
    atual = open(path, "rb").read()
    assert sha(atual) == h0, "o CLAUDE.md mudou durante a compactacao - abortando antes de substituir"
    tmp = path + ".compactado_tmp"
    open(tmp, "wb").write(comp)
    assert open(tmp, "rb").read() == comp
    os.replace(tmp, path)
    fin = open(path, "rb").read()
    assert fin == comp
    print("SUBSTITUIDO: %s %d -> %d B; sha256 %s" % (path, len(b), len(fin), sha(fin)))
    prova["substituido"] = {"bytes": len(fin), "sha256": sha(fin), "quando": time.strftime("%Y-%m-%d %H:%M:%S")}
    json.dump(prova, open(cfg["prova"], "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def reconstruir(comp, partes_bytes, ordem_partes, segs):
    """compactado -> original: tira a NOTA; troca cada bloco de INDICE pelas partes (na ordem do manifesto) que ele lista."""
    # 1. tirar NOTA
    i = comp.index(NOTA_INI); j = comp.index(NOTA_FIM) + len(NOTA_FIM)
    resto = comp[:i] + comp[j:]
    # 2. blocos de indice
    saida = bytearray()
    pos = 0
    usados = 0
    pat = re.compile(re.escape(IND_INI) + rb"[^\n]*-->\n.*?" + re.escape(IND_FIM), re.S)
    for m in pat.finditer(resto):
        saida += resto[pos:m.start()]
        bloco = m.group(0).decode("utf8")
        # as partes que o bloco cita, na ordem em que aparecem
        citados = re.findall(r"`CLAUDE_memoria/([^`]+)`", bloco)
        for fn in citados:
            saida += partes_bytes[fn]
            usados += 1
        pos = m.end()
    saida += resto[pos:]
    assert usados == len(ordem_partes), (usados, len(ordem_partes))
    # a ordem citada tem de ser a ordem do manifesto
    todas = re.findall(r"`CLAUDE_memoria/([^`]+)`", b"".join(m.group(0) for m in pat.finditer(resto)).decode("utf8"))
    assert todas == ordem_partes, "ordem das partes no indice difere do manifesto"
    return bytes(saida)


if __name__ == "__main__":
    main()
