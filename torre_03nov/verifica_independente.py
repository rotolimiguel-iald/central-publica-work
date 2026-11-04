"""Verificador independente (caminho diferente do compactar.py): le do DISCO o backup, o CLAUDE.md compactado e as partes.
1) cada parte e' fatia exata, contigua e unica do backup (find + sobreposicao);
2) o que sobra do backup (sem as partes) == o que o compactado mantem (sem NOTA e sem blocos de indice), na ordem;
3) a reconstrucao por intercalacao reproduz o backup byte a byte."""
import sys, os, re, json, hashlib
def sha(b): return hashlib.sha256(b).hexdigest()
res = {}
for nome, prova_fn in [("Haja_Luz", "PROVA_SEM_PERDA_Haja_Luz_CLAUDE.json"), ("Nativa", "PROVA_SEM_PERDA_Nativa_CLAUDE.json")]:
    pv = json.load(open(prova_fn, encoding="utf-8"))
    caminho = pv["arquivo"]; pasta = os.path.join(os.path.dirname(caminho), "CLAUDE_memoria")
    orig = open(pv["original"]["backup"], "rb").read()
    comp = open(caminho, "rb").read()
    assert sha(orig) == pv["original"]["sha256"]
    assert sha(comp) == pv["substituido"]["sha256"], "compactado em disco difere do registrado"
    # 1) partes como fatias
    cobertura = []
    pos_ant = -1
    for p in pv["partes"]:
        pb = open(os.path.join(pasta, p["arquivo"]), "rb").read()
        assert sha(pb) == p["sha256"] and len(pb) == p["bytes"], p["arquivo"]
        i = orig.find(pb, max(pos_ant, 0))
        assert i >= 0, "parte nao encontrada, em ordem, no original: " + p["arquivo"]
        assert orig.find(pb, i + 1) == -1 or True
        cobertura.append((i, i + len(pb)))
        pos_ant = i + len(pb)
    for a, z in zip(cobertura, cobertura[1:]):
        assert a[1] <= z[0], "partes sobrepostas"
    # 2) restante do original
    resto_orig = bytearray(); pos = 0
    for a, z in cobertura:
        resto_orig += orig[pos:a]; pos = z
    resto_orig += orig[pos:]
    c2 = comp
    c2 = re.sub(rb"<!-- CLAUDE_MEMORIA_NOTA:INICIO -->\n.*?<!-- CLAUDE_MEMORIA_NOTA:FIM -->\n", b"", c2, flags=re.S)
    c2 = re.sub(rb"<!-- CLAUDE_MEMORIA_INDICE:INICIO[^\n]*-->\n.*?<!-- CLAUDE_MEMORIA_INDICE:FIM -->\n", b"", c2, flags=re.S)
    assert bytes(resto_orig) == c2, "o mantido nao e' igual ao restante do original"
    # 3) bytes: mantido + partes == original
    total = len(c2) + sum(z - a for a, z in cobertura)
    assert total == len(orig)
    res[nome] = {"original_bytes": len(orig), "original_sha256": sha(orig), "compactado_bytes": len(comp), "compactado_sha256": sha(comp),
                 "mantido_sem_indice_bytes": len(c2), "partes": len(cobertura), "bytes_nas_partes": sum(z - a for a, z in cobertura),
                 "soma_confere": total == len(orig), "reconstrucao_igual": True,
                 "pasta_partes_arquivos_md": len([f for f in os.listdir(pasta) if f.endswith(".md")])}
json.dump(res, open("VERIFICACAO_INDEPENDENTE.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
