# -*- coding: utf-8 -*-
"""c1_ponte_byte_a_byte_v402.py -- exame final v402, SO LEITURA: (a) a pedra do Codex (ORDEM 025) e' byte a byte a mesma em: a entrega
(Chatgpt\TUNEL\DO_CHATGPT\ORDEM_025), v402\pedra, k402c\final e k402c\arvore, e o corpo embutido no candidato (sha do embutido vem do
ESTRUTURA_v401_v402.json, medido por literal_eval); (b) condicao C1: NENHUM outro arquivo da entrega aparece (mesmo sha256) em v402\ ou em C:\t\k402c;
a busca hasheia so' os arquivos de tamanho igual a algum arquivo da entrega. Grava C1_PONTE_v402.json."""
import hashlib, json, os, collections
W = os.path.join("C:" + os.sep, "IALD", "Central de Patentes")
ENT = os.path.join(W, "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_025")
V = os.path.join(W, "work", "cadeia_de_selo", "v402")
K = os.path.join("C:" + os.sep, "t", "k402c")
def sha(p):
    d = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): d.update(c)
    return d.hexdigest()
ent = {}
for d, ds, fs in os.walk(ENT):
    for f in fs:
        p = os.path.join(d, f); ent[os.path.relpath(p, ENT)] = (os.path.getsize(p), sha(p))
leans = {k: v for k, v in ent.items() if os.path.basename(k) == "PonteDaEscalaDual.lean"}
R = {"entrega_n_arquivos": len(ent), "entrega_PonteDaEscalaDual_lean": {k: v[1][:16] for k, v in leans.items()}}
copias = {"v402/pedra": os.path.join(V, "pedra", "PonteDaEscalaDual.lean"), "k402c/final": os.path.join(K, "final", "TGLExt", "PonteDaEscalaDual.lean"),
          "k402c/arvore": os.path.join(K, "arvore", "TGLExt", "PonteDaEscalaDual.lean"), "v402/insumos?": None}
for p in [os.path.join(V, "insumos", x) for x in os.listdir(os.path.join(V, "insumos"))] if os.path.isdir(os.path.join(V, "insumos")) else []:
    pass
R["copias"] = {k: (sha(p)[:16] if p and os.path.exists(p) else None) for k, p in copias.items()}
est = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ESTRUTURA_v401_v402.json"), encoding="utf-8"))
R["copias"]["candidato_embutido"] = est["pedras_sha16_embutidas"]["TGLExt/PonteDaEscalaDual.lean"]
alvo = "0e55b6e448adbd91"
R["todas_iguais_a_0e55b6e448adbd91"] = all(v == alvo for v in R["copias"].values() if v is not None) and any(v[1][:16] == alvo for v in leans.values())
# C1
outros = {v[1]: k for k, v in ent.items() if v[1][:16] != alvo}
tam = collections.defaultdict(list)
for k, (s, h) in ent.items():
    if h in outros: tam[s].append(k)
achados = []; n = 0; nh = 0
for raiz in (V, K):
    for d, ds, fs in os.walk(raiz):
        for f in fs:
            p = os.path.join(d, f); n += 1
            try: s = os.path.getsize(p)
            except OSError: continue
            if s in tam and s > 0:
                nh += 1; h = sha(p)
                if h in outros: achados.append({"arquivo": p, "igual_a_entrega": outros[h]})
nomes = set(os.path.basename(k) for k in ent if os.path.basename(k) != "PonteDaEscalaDual.lean")
mesmo_nome = []
for raiz in (V, K):
    for d, ds, fs in os.walk(raiz):
        for f in fs:
            if f in nomes and f not in ("README.md",): mesmo_nome.append(os.path.join(d, f))
R["C1"] = {"arquivos_varridos": n, "hasheados_por_tamanho": nh, "outros_arquivos_da_entrega_copiados_por_sha256": achados, "arquivos_com_mesmo_nome_de_outro_da_entrega": mesmo_nome[:40], "n_mesmo_nome": len(mesmo_nome)}
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "C1_PONTE_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:5000])
