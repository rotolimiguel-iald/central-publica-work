from b_lib import *
import re, hashlib
p = r"C:\IALD\Central de Patentes\work\h0dn_bg1_v411_emenda_11nov\EMENDA_E_PRE_REGISTRO_V411.md"
raw = open(p, "rb").read(); t = raw.decode("utf-8").replace(chr(13) + chr(10), chr(10))
print("sha16 pre-registro (arquivo):", hashlib.sha256(raw).hexdigest()[:16])
C = core()["core"]; h = C["h0dn_bg1_v411"]
print("sha16 pre-registro (core insumos):", {k: v["sha256"][:16] for k, v in h["insumos_pinados"].items() if "PRE_REGISTRO" in k.upper()})
def sec(n):
    m = re.search(r"^## %d\. .*$" % n, t, re.M); m2 = re.search(r"^## %d\. .*$" % (n + 1), t, re.M); return t[m.end():m2.start()]
s8 = sec(8)
items = [" ".join(x.split()) for x in re.findall(r"^\d\. (.+?)(?=\n\d\. |\n\n|\Z)", s8, re.M | re.S)]
print("itens da secao 8 no arquivo:", len(items))
core_items = h["values"]["ressalvas_secao8"]
print("core == arquivo:", core_items == items)
# renders
pt_ = pt(); en_ = en(); md_ = md()
nrm = lambda s: re.sub(r"\s+", " ", s)
def has(tx, s):
    return nrm(s) in nrm(tx)
for i, it in enumerate(items, 1):
    print(i, "PT quadro", has(pt_[pt_.index("A razão de Hubble, H0DN"):pt_.index("O Teste da Única Palavra [")], it),
          "PT secao", has(pt_[pt_.index("== O teste decisivo"):pt_.index("== IALD ao quadrado")], it),
          "EN quadro", has(en_[en_.index("The Hubble ratio, H0DN"):en_.index("The Test of the Only Word [")], it),
          "EN secao", has(en_[en_.index("== The decisive test"):en_.index("== IALD squared")], it),
          "MD", has(md_[:8000], it))
# nao decide: section 6
s6 = sec(6)
m6 = re.search(r"\*\*O que o teste n[ãa]o decide\.\*\*\n\n(.*?)(?=\n\n|\Z)", s6, re.S)
nd = [x.strip() for x in re.findall(r"^- (.+)$", m6.group(1), re.M)]
print("nao decide no arquivo:", len(nd))
for x in nd: print("  -", x[:200])
print("core nao decide:", h["o_que_o_teste_nao_decide"])
print("numeracao nos rendidos PT quadro: '[1.]' etc:", re.findall(r"\[\d\.\]", pt_[pt_.index("As sete ressalvas"):pt_.index("As sete ressalvas")+2500])[:8])
