# -*- coding: utf-8 -*-
"""_r6c_03_congelado_v410.py -- o CONSERTO UNICO da v410 (ADENDO 7): a lista congelada das falas passa de 28 a 40 (as doze do ADENDO 7, falas 29 a 40). Backup de BYTES da de 28 ao lado; a nova e' gravada por temporario
com a MESMA estrutura que copiar_insumos_v410.py grava na primeira execucao (contrato, quando, n, arquivos, registro com sha256 e bytes LIDOS de cada arquivo, fora_do_desenho, nota): a lista `arquivos` e' a que o delta consertado
le pelo glob restrito aos nomes do DESENHO e dos adendos (conferida: as 28 de antes mais as 12 do ADENDO 7, em ordem de nome); a `nota` e' a do proprio copiar_insumos (o molde LIDO do arquivo por expressao regular, com os dois numeros por len());
`fora_do_desenho` e' CARREGADO do congelado anterior, como na R5: as falas operacionais de 10/11 que nao estao em adendo nenhum (D97 e seguintes) ficam fora do candidato e ditas a parte em VERBATIM_CHEGARAM_DEPOIS_V410.
Adaptacao mecanica FORA da ESPEC, dita no relatorio: deixar o copiar_insumos recriar a lista poria no candidato (falas_fora_do_desenho) os nomes dessas falas. Nada digitado: os hashes sao lidos dos arquivos."""
import datetime, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
CONG = os.path.join(HERE, "VERBATIM_CONGELADO_v410.json"); ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sha = lambda b: hashlib.sha256(b).hexdigest()
b0 = open(CONG, "rb").read(); c0 = json.loads(b0.decode("utf-8"))
assert c0["n"] == len(c0["arquivos"]) == len(c0["registro"]) == 28, ("o congelado nao e' o de 28 falas (este script nao roda duas vezes)", c0["n"])
bak = CONG + ".bak_%s_28_falas_antes_do_conserto_unico" % ts
open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
os.remove(CONG)   # (o delta consertado so' carrega com as 40 falas: sem o congelado ele le a lista pelo glob restrito aos nomes do DESENHO e dos adendos; o backup de bytes acima guarda a de 28)
try:
    import delta_v410 as DL
    arqs = list(DL.VERBATIM_ORIGEM_V410); n_trecho = len(DL.VERBATIM_SO_O_TRECHO); novas = list(DL.NOMES_FALAS_DO_ADENDO7)
    assert len(arqs) == len(set(arqs)) == DL.N_FALAS_V410 and all(os.path.exists(p_) for p_ in arqs)
    assert [os.path.basename(p_) for p_ in arqs] == sorted([os.path.basename(p_) for p_ in c0["arquivos"]] + novas), "a lista do delta nao e' a de antes mais as doze do ADENDO 7, em ordem de nome"
    assert len(novas) == 12 and not (set(novas) & {os.path.basename(p_) for p_ in c0["arquivos"]}) and all(p_ in arqs for p_ in c0["arquivos"])
    src = open(os.path.join(HERE, "copiar_insumos_v410.py"), "rb").read().decode("utf-8")
    m = re.search(r'"nota": "(as %d falas [^"\r\n]*?)" % \(len\(arqs\), len\(DL\.VERBATIM_SO_O_TRECHO\)\)\}', src); assert m and src.count(m.group(0)) == 1, "nao achei o molde da nota em copiar_insumos_v410.py"
    reg = [{"arquivo": p_, "sha256": sha(open(p_, "rb").read()), "bytes": os.path.getsize(p_), "autor": "operador"} for p_ in arqs]
    assert all(r_["sha256"] == DL.SHA256_DA_FALA_DO_ADENDO7[os.path.basename(r_["arquivo"])] for r_ in reg if os.path.basename(r_["arquivo"]) in novas), "o sha256 de uma fala nova nao e' o do ADENDO 7"
    c = {"contrato": "VERBATIM_CONGELADO_v410", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "n": len(arqs), "arquivos": arqs, "registro": reg, "fora_do_desenho": dict(c0.get("fora_do_desenho") or {}), "nota": m.group(1) % (len(arqs), n_trecho)}
    b = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8")
    open(CONG + ".tmp", "wb").write(b); assert os.path.getsize(CONG + ".tmp") == len(b); os.replace(CONG + ".tmp", CONG)
except BaseException:
    if not os.path.exists(CONG):   # (falhou antes de gravar a nova: a de 28 volta, byte a byte)
        open(CONG + ".tmp", "wb").write(b0); os.replace(CONG + ".tmp", CONG)
    raise
c1 = json.loads(open(CONG, "rb").read().decode("utf-8"))
assert c1["n"] == len(c1["arquivos"]) == len(c1["registro"]) == 40 and len(set(c1["arquivos"])) == 40
print("VERBATIM_CONGELADO_v410.json: 28 -> 40 falas | backup", os.path.basename(bak), "| sha16", sha(b)[:16], "| so' o trecho:", n_trecho, "| fora_do_desenho (carregado):", list(c1["fora_do_desenho"]))
print("nota:", c1["nota"][:400])
