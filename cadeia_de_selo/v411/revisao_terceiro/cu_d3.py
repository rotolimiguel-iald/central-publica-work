"""CU-D3 (item D.4): a guarda da conversa (do construtor, em memoria) sobre as saidas REAIS da v410 selada no Nos (o que o rito real da v411 reproduz do texto antigo): regra (a) e (c) tem de dar zero; a (b) a base da propria v410 (esperado: passa por construcao); contagens da linha curta por alvo na base e no ensaio."""
import json, os, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import guarda_conversa_v411 as GC


def _nunca(*a, **k):
    raise RuntimeError("gerar_base recusado")


GC.gerar_base = _nunca
rd = lambda p: open(p, "rb").read()
b = GC.base()
print("base: linhas curtas", len(b["linhas"]), "| contagens por alvo (sem texto):", {k: {t: n for t, n in v.items() if t not in ("fala", "len")} for k, v in b["linhas"].items()})
alvos410 = {"um_py": rd(os.path.join(NOS, "um.py")), "core": json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")),
            "pt": rd(os.path.join(NOS, "um_absoluto_pt.txt")), "en": rd(os.path.join(NOS, "um_absoluto_en.txt")), "md": rd(os.path.join(NOS, "um_absoluto_forma_canonica.md")),
            "manifest": rd(os.path.join(NOS, "um_absoluto_manifest.md")), "stdout": rd(os.path.join(NOS, "rodada_v410_stdout.txt"))}
v = GC.verificar(alvos410, b)
print("guarda sobre a v410 REAL selada: ok =", v["ok"], "| achados:", len(v["achados"]), "| regras:", sorted({a["regra"] for a in v["achados"]}), "| informativos:", len(v["informativo"]))
for a in v["achados"][:6]:
    print("   ACHADO", a)
# o ensaio do v411 (stdout, md, etc): contagens da linha curta no ensaio contra a base
ens = {"um_py": rd(os.path.join(V, "um_v411_candidato.py")), "core": json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8")),
       "pt": rd(r"C:\t\k411c\dry_v411\dry_v411_pt.txt"), "en": rd(r"C:\t\k411c\dry_v411\dry_v411_en.txt"), "md": rd(r"C:\t\k411c\falso_nos_v411\um_absoluto_forma_canonica.md"),
       "manifest": rd(r"C:\t\k411c\falso_nos_v411\um_absoluto_manifest.md"), "stdout": rd(r"C:\t\k411c\falso_nos_v411\rodada_v411_stdout.txt")}
c_ens = GC.contagens_curtas(ens)
c_410 = GC.contagens_curtas(alvos410)
for k in c_ens:
    print("linha curta", k, "| ensaio v411:", {t: n for t, n in c_ens[k].items() if t not in ("fala", "len")}, "| v410 real:", {t: n for t, n in c_410[k].items() if t not in ("fala", "len")})
# tamanho do stdout: v410 real x ensaio
print("stdout: v410 real", len(alvos410["stdout"]), "bytes | ensaio v411", len(ens["stdout"]), "bytes; core v410 real", os.path.getsize(os.path.join(NOS, "um_absoluto.json")), "| core ensaio", os.path.getsize(r"C:\t\k411c\dry_v411\core_ensaio.json"))
