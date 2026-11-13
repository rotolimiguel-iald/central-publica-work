"""CU-E4: as contagens declaradas no CONSERTO_R1_v411.md (secao contagem de controles) contra o que os arquivos mostram."""
import ast, glob, json, os, re, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
sys.dont_write_bytecode = True
sys.path.insert(0, V)
rd = lambda p: open(p, "rb").read().decode("utf-8")


def par(rel):
    o = os.path.join(V, rel.replace("/", os.sep))
    b = glob.glob(o + ".bak_*_r1fix")
    return rd(b[0]), rd(o)


# 1. guarda_frases: proibidas / limpas / falas
import guarda_frases_v411 as G
src_old, src_new = par("guarda_frases_v411.py")
print("guarda_frases: nomes publicos do modulo:", [n for n in dir(G) if not n.startswith("__")][:20])
for nm in ("PROIBIDAS", "LIMPAS", "FALAS", "CASOS_PROIBIDOS", "CASOS_LIMPOS"):
    if hasattr(G, nm):
        print("  ", nm, len(getattr(G, nm)))
# 2. conferidor: itens deve_mudar (84 -> 89): o dict que tem a chave com '(C-02) o artigo em PDF e TeX'


def maior_dict_com(src, marca):
    t = ast.parse(src)
    best = None
    for n in ast.walk(t):
        if isinstance(n, ast.Dict):
            for k in n.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str) and marca in k.value:
                    best = n
    return best


for marca in ("os registros por spec v411 (cunhagens_v411",):
    o, n = par("conferir_rito_v411.py")
    for tag, s in (("antes", o), ("hoje", n)):
        d = maior_dict_com(s, marca)
        print("conferidor itens do dict com a marca:", tag, len(d.keys) if d is not None else None)
# 3. variante( no harness dos textos; falha(; P.append( na leitura; _recusa_com_core( no fechar
for rel, pats in (("pos_rito/harness_textos_ensaio_v411.py", ["variante(", "falha("]), ("pos_rito/leitura_v411.py", ["P.append("]), ("pos_rito/harness_fechar_sandbox_v411.py", ["_recusa_com_core("]), ("p00_precondicoes_v411.py", ["chk(", "tenta("])):
    o, n = par(rel)
    for p in pats:
        print("%-44s %-22s antes %d | hoje %d" % (rel, p, o.count(p), n.count(p)))
# harness do fechar: 88 -> 89 (o conserto fala 'fechar_negativos'); conta as linhas _recusa_com_core("fechar_
o, n = par("pos_rito/harness_fechar_sandbox_v411.py")
print("harness_fechar: _recusa_com_core(\"fechar_ antes", len(re.findall(r'_recusa_com_core\("fechar_', o)), "hoje", len(re.findall(r'_recusa_com_core\("fechar_', n)))
# 4. p00: resultado
P = json.load(open(os.path.join(V, "PRECONDICOES_v411.json"), encoding="utf-8"))
print("PRECONDICOES: veredito", P.get("veredito"), "| n_checagens", P.get("n_checagens"), "| n_ok", P.get("n_ok"), "| pendentes", len(P.get("pendentes") or []))
ck = P.get("checagens") or []
print("   checagens com (C-01):", sum(1 for c in ck if "(C-01)" in json.dumps(c, ensure_ascii=False)[:200]), "| (C-05):", sum(1 for c in ck if "(C-05)" in json.dumps(c, ensure_ascii=False)[:200]), "| (D181):", sum(1 for c in ck if "(D181)" in json.dumps(c, ensure_ascii=False)[:200]))
# 5. guarda_conversa: controle negativo (b6)
b6 = json.load(open(r"C:\t\k411c\revisao_CU\b6_guarda_do_construtor.json"))
cn = b6["controle_negativo"]
print("guarda_conversa controle negativo (meu run sobre 7 alvos: um_py,core,pt,en,md,manifest,stdout): n chaves", len(cn) - 1 if "ok" in cn else len(cn), "| todos True:", all(v is True for v in cn.values()))
