"""Diagnostico SOMENTE LEITURA da missao recusada: acha QUAL folha do estado aciona o guarda, sem imprimir o conteudo confidencial.
Usa a biblioteca (store.get) e as funcoes do proprio guarda; imprime caminho da folha, regras, tamanhos e um contexto com o caminho MASCARADO."""
import sys, json, re, hashlib
sys.path.insert(0, r"C:\IALD\MEMORIA_IALD\lib")
from pathlib import Path
from iald_memory import MemoryStore
from iald_memory import guard
ref = json.load(open(r"C:\IALD\MEMORIA_IALD\sessions\claude-central-9c_patentes-atualizacao-12out.json", encoding="utf-8"))
store = MemoryStore(Path(ref["store"]))
snap = store.get(ref["context_id"], ref["scope"])
print("chaves do snapshot:", list(snap.keys()))
print("revisao:", snap.get("revision"), "| estado de p.phase:", (snap.get("flow") or {}).get("phase"))
achados = []
def andar(x, caminho):
    if isinstance(x, str):
        r = guard.scan_text(x)
        if r:
            achados.append((caminho, r, x))
    elif isinstance(x, dict):
        for k, v in x.items():
            andar(v, caminho + "." + str(k))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            andar(v, caminho + "[%d]" % i)
andar(snap, "$")
print("folhas que acionam o guarda:", len(achados))
pat = re.compile(r"\S*(?:[\/]|%5c|%2f|\b[a-z]:)escritorio\S*", re.I)
for c, r, x in achados:
    m = pat.search(guard.fold(x)) if False else pat.search(x)
    ctx = None
    if m:
        a = max(0, m.start() - 120); z = min(len(x), m.end() + 120)
        ctx = x[a:m.start()] + "<CAMINHO_ESCRITORIO len=%d>" % (m.end() - m.start()) + x[m.end():z]
    print(json.dumps({"caminho": c, "regras": r, "chars_da_folha": len(x), "sha16_da_folha": hashlib.sha256(x.encode("utf-8")).hexdigest()[:16],
                      "n_ocorrencias": len(pat.findall(x)), "contexto_mascarado": ctx}, ensure_ascii=False, indent=1))
