# -*- coding: utf-8 -*-
"""derivar_servico_v400.py -- DERIVA, SEM EXECUTAR, os tres scripts do servico da Bancada Um da v400 (evento_c1_b3_v400.py, recibo_parada_v400.py, recibo_religamento_v400.py) e o conferidor estatico deles a partir dos da v399
(v399\\bancada_B3_servico). A UNICA troca e' 399 -> 400 (a versao DESTA cadeia); o 398 FICA: a Bancada de producao AINDA pina a v398 e o ultimo B(n) feito nela, o ultimo religamento do servico e a geracao dela (B8) sao os da v398 -- a v399 foi recusada pela
Bancada e nunca foi aplicada. Cada troca tem contagem exata (aborta se casar menos ou mais). So' escreve em v400\\bancada_B3_servico; NAO executa nenhum dos scripts. uso: python -I -B -X utf8 derivar_servico_v400.py [--refazer]"""
import ast, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V9S = os.path.join(os.path.dirname(HERE), "v399", "bancada_B3_servico"); DST = os.path.join(HERE, "bancada_B3_servico")
os.makedirs(DST, exist_ok=True)
NUM = re.compile(r"(?<![0-9])399(?![0-9])")
ARQS = ("evento_c1_b3_v399.py", "recibo_parada_v399.py", "recibo_religamento_v399.py", "conferir_exigencias_servico_v399.py")
# trocas ESPECIFICAS (depois do 399 -> 400), com contagem exata, no conferidor: o ESPERADOS_v400.json EXISTE (o ensaio o gerou) e o evento abortaria hoje porque o um.py do Nos ainda e' a v399 (nao o candidato)
ESPEC = {"conferir_exigencias_servico_v400.py": [
    ('esp_p = os.path.join(V, "ESPERADOS_v400.json")\nchk("ESPERADOS_v400.json NAO existe agora (o evento abortaria no assert, como no molde)", not os.path.exists(esp_p), os.path.exists(esp_p), False)\n',
     'esp_p = os.path.join(V, "ESPERADOS_v400.json")\n'
     'cand16_ = json.load(open(esp_p, encoding="utf-8"))["candidato_sha16"] if os.path.exists(esp_p) else None\n'
     'um_nos16_ = sha(os.path.join(NOS, "um.py"))[:16]\n'
     'chk("ESPERADOS_v400.json existe (gerado pelo ensaio) e o um.py do Nos AINDA NAO e o candidato dele: o evento ABORTARIA hoje no assert do candidato (antes de anotar no quadro)", bool(cand16_) and um_nos16_ != cand16_, [cand16_, um_nos16_], "diferentes")\n', 1),
    ('V8 = os.path.join(os.path.dirname(V), "v398")\n', 'V8 = os.path.join(os.path.dirname(V), "v398")\nNOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")\n', 1)]}
rel = {}
for nome in ARQS:
    src = open(os.path.join(V9S, nome), "rb").read().decode("utf-8")
    novo_nome = NUM.sub("400", nome)
    t = NUM.sub("400", src)
    for old, new, c in ESPEC.get(novo_nome, []):
        assert t.count(old) == c, ("troca especifica nao casou", novo_nome, old[:60], t.count(old))
        t = t.replace(old, new)
    ast.parse(t)
    assert not re.search(r"(?<![0-9])399(?![0-9])", t), ("sobrou 399 em " + novo_nome)
    p = os.path.join(DST, novo_nome)
    b = t.encode("utf-8")
    if os.path.exists(p) and open(p, "rb").read() != b and "--refazer" not in sys.argv:
        raise SystemExit("EXISTE e DIFERE (editado depois?): " + p)
    open(p + ".tmp", "wb").write(b); os.replace(p + ".tmp", p)
    rel[novo_nome] = {"origem": os.path.join(V9S, nome), "origem_sha256": hashlib.sha256(src.encode("utf-8")).hexdigest(), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "trocas_399_para_400": len(NUM.findall(src)) + len(NUM.findall(nome))}
json.dump({"contrato": "DERIVACAO_SERVICO_v400", "executado": False, "regra": "399 -> 400 e nada mais (o 398 fica: a Bancada ainda pina a v398)", "arquivos": rel}, open(os.path.join(DST, "DERIVACAO_SERVICO_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: v["sha256"][:16] for k, v in rel.items()})
