import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
j = json.load(open(V + r"\pos_rito\HARNESS_TEXTOS_ENSAIO_v411.json", encoding="utf-8"))
ln = j["etapas"]["leitura_negativos"]
cs = ln.get("controles") or []
print("leitura_negativos: controles", len(cs), "| reprovou True:", sum(1 for c in cs if c.get("reprovou") is True), "| nao reprovou:", [c.get("controle") for c in cs if c.get("reprovou") is not True][:5])
print("chaves do etapa:", [k for k in ln if k != "controles"])
for c in cs:
    if "errata A MAIS" in str(c.get("controle")) or "ultima errata da v410" in str(c.get("controle")) or "escada" in str(c.get("controle")).lower()[:60]:
        print("   ", c.get("controle")[:100], c.get("reprovou"))
f = json.load(open(V + r"\pos_rito\HARNESS_FECHAR_SANDBOX_v411.json", encoding="utf-8"))
fn = f["etapas"]["fechar_negativos"]
print("fechar_negativos:", len(fn), "| recusou True:", sum(1 for c in fn if c.get("recusou") is True), "| handoff escrito:", sum(1 for c in fn if c.get("handoff_escrito")))
print([c["controle"][:60] for c in fn if c.get("recusou") is not True])
# conferidor: controles dentro do harness
ct = j["etapas"].get("conferidor"); print("conferidor etapa:", json.dumps(ct, ensure_ascii=False)[:300])
