# -*- coding: utf-8 -*-
"""montar_textos_v402.py -- MONTA pos_rito\\textos_v402.py enxertando as definicoes de textos_v402_novo.pysnip (escritas a mao para a v402) no esqueleto textos_v402.semente (a semente derivada de textos_v401.py: so' o numero de versao subido).
Cada nome definido no fragmento SUBSTITUI o de mesmo nome da semente (ou entra no fim); os nomes de DELETAR saem; o cabecalho de comentarios e' o do fragmento (__HEADER__). Nao executa nada do textos: so' le texto e confere a sintaxe (ast.parse).
Backup de bytes do textos_v402.py anterior (.bak_<data>) antes de gravar. uso: python -I -B -X utf8 montar_textos_v402.py"""
import ast, datetime, hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEMENTE = os.path.join(HERE, "textos_v402.semente"); NOVO = os.path.join(HERE, "textos_v402_novo.pysnip"); DEST = os.path.join(HERE, "textos_v402.py")
DELETAR = {"_definicao", "_cadeia", "_calculo", "_errata_adendo", "_ratificacoes", "_emc2", "_linha_maquina_falsidade", "_paragrafo_falsidade_de", "verificar_paragrafo_falsidade", "paragrafo_falsidade", "MARC_FAL_INI", "MARC_FAL_FIM"}
RETOCAR = {   # nomes MANTIDOS da semente, com troca de texto exata (nome -> [(velho, novo, vezes)])
    "_falas": [("SEIS", "TRES", 0), ("seis", "tres", 0), ("25/10", "26/10", 0)],
    "_cita": [("SEIS", "TRES", 0), ("seis", "tres", 0)],
    "_sidecar": [("agora também o do registro `falsidade_da_inercia_v401`", "agora também os dos três registros com função da v402", 1)],
}
sha = lambda b: hashlib.sha256(b).hexdigest()


def blocos(src):
    """[(nomes, ini, fim)] (linhas 0-based, fim exclusivo) dos nos de nivel de modulo que definem nomes (def ou atribuicao), com os comentarios contiguos acima; atribuicoes na mesma linha formam UM bloco."""
    ls = src.split("\n"); tree = ast.parse(src); out = []
    for nd in tree.body:
        if isinstance(nd, ast.FunctionDef):
            nomes = [nd.name]
        elif isinstance(nd, ast.Assign):
            nomes = [t.id for t in nd.targets if isinstance(t, ast.Name)]
        else:
            continue
        ini = nd.lineno - 1; fim = nd.end_lineno
        while ini > 0 and ls[ini - 1].lstrip().startswith("#"):
            ini -= 1
        if out and ini < out[-1][2]:                 # mesma linha (A = 1; B = 2): junta
            out[-1] = (out[-1][0] + nomes, out[-1][1], max(out[-1][2], fim))
        else:
            out.append((nomes, ini, fim))
    return out


def main():
    seed = open(SEMENTE, "rb").read().decode("utf-8"); novo = open(NOVO, "rb").read().decode("utf-8")
    nb = blocos(novo); header = None; defs = {}
    for nomes, i, f in nb:
        txt = "\n".join(novo.split("\n")[i:f])
        if nomes == ["__HEADER__"]:
            header = ast.literal_eval(ast.parse(txt).body[0].value)
            continue
        for n in nomes:
            defs[n] = txt if len(nomes) == 1 else txt
    ls = seed.split("\n"); sb = blocos(seed)
    # cabecalho: da linha 1 ate' antes do primeiro 'import hashlib'
    k = next(i for i, l in enumerate(ls) if l.startswith("import hashlib"))
    assert ls[0].startswith("# -*- coding"), ls[0]
    assert header, "o fragmento nao traz __HEADER__"
    reps = []     # (ini, fim, texto)
    reps.append((0, k, header.rstrip("\n")))
    usados = set()
    for nomes, i, f in sb:
        if i < k:
            continue
        if all(n in DELETAR for n in nomes):
            reps.append((i, f, None)); continue
        hit = [n for n in nomes if n in defs]
        if hit:
            assert len(nomes) == len(hit) or len(nomes) == 1, ("bloco misto na semente", nomes)
            tx = [defs[n] for n in hit]
            if len(set(tx)) == 1:
                reps.append((i, f, tx[0]))
            else:
                reps.append((i, f, "\n".join(tx)))
            usados.update(hit); continue
        if any(n in RETOCAR for n in nomes):
            txt = "\n".join(ls[i:f])
            for nome in nomes:
                for v, nw, vezes in RETOCAR.get(nome, []):
                    c = txt.count(v)
                    assert (vezes == 0 and c >= 0) or c == vezes, ("retoque nao casou", nome, v, c)
                    txt = txt.replace(v, nw)
            reps.append((i, f, txt))
    # blocos do fragmento que a semente nao tinha: entram no fim (na ordem do fragmento)
    fim_txt = []
    for nomes, i, f in nb:
        if nomes == ["__HEADER__"]:
            continue
        if not any(n in usados for n in nomes):
            fim_txt.append("\n".join(novo.split("\n")[i:f]))
    out = list(ls)
    for ini, fim, tx in sorted(reps, key=lambda r: -r[0]):
        out[ini:fim] = [] if tx is None else tx.split("\n")
    res = "\n".join(out).rstrip("\n") + "\n\n\n" + "\n\n\n".join(fim_txt) + "\n"
    res = re.sub(r"\n{4,}", "\n\n\n", res)
    ast.parse(res)
    antigo = open(DEST, "rb").read() if os.path.exists(DEST) else b""
    if antigo and sha(antigo) != sha(res.encode("utf-8")):
        open(DEST + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(antigo)
    tmp = DEST + ".tmp"; open(tmp, "wb").write(res.encode("utf-8"))
    assert os.path.getsize(tmp) > 20000, "o textos montado ficou pequeno demais"
    os.replace(tmp, DEST)
    print("textos_v402.py montado: %d B, sha16 %s; substituidos %d nomes, deletados %d blocos, acrescentados %d blocos" % (os.path.getsize(DEST), sha(res.encode("utf-8"))[:16], len(usados), sum(1 for r in reps if r[2] is None), len(fim_txt)))
    faltam = sorted(n for n in defs if n not in usados and not any(n in b[0] for b in [(nm,) for nm in []]))
    print("nomes novos (nao estavam na semente):", ", ".join(faltam))


if __name__ == "__main__":
    main()
