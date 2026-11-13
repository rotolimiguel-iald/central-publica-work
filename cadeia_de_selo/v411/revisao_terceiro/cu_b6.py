"""CU-B6: DEPOIS do meu proprio scan: a guarda do construtor (importada em memoria, -B, sem rodar o main, sem gerar base) sobre os mesmos alvos."""
import json, os, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import guarda_conversa_v411 as GC


def _nunca(*a, **k):
    raise RuntimeError("gerar_base recusado pelo revisor (escreveria na pasta do pacote)")


GC.gerar_base = _nunca
rd = lambda p: open(p, "rb").read()
alvos = {"um_py": rd(os.path.join(V, "um_v411_candidato.py")),
         "core": json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8")),
         "pt": rd(r"C:\t\k411c\dry_v411\dry_v411_pt.txt"), "en": rd(r"C:\t\k411c\dry_v411\dry_v411_en.txt"),
         "md": rd(r"C:\t\k411c\falso_nos_v411\um_absoluto_forma_canonica.md"), "manifest": rd(r"C:\t\k411c\falso_nos_v411\um_absoluto_manifest.md"),
         "stdout": rd(r"C:\t\k411c\falso_nos_v411\rodada_v411_stdout.txt")}
b = GC.base()
print("base v410 (json) tem", len(b["linhas"]), "linhas curtas; arquivos da base:", {k: v["sha16"] for k, v in b["arquivos"].items()})
v = GC.verificar(alvos, b)
print("verificar: ok =", v["ok"], "| n achados:", len(v["achados"]), "| n_agulhas:", v["n_agulhas"], "| informativos:", len(v["informativo"]))
for a in v["achados"][:10]:
    print("ACHADO", a)
for a in v["informativo"][:10]:
    print("INFO", a)
cn = GC.controle_negativo(alvos, b, v)
print("controle_negativo:", cn)
json.dump({"ok": v["ok"], "n_achados": len(v["achados"]), "n_informativo": len(v["informativo"]), "n_agulhas": v["n_agulhas"], "controle_negativo": cn, "alvos": v["alvos"]}, open(r"C:\t\k411c\revisao_CU\b6_guarda_do_construtor.json", "w"), indent=1)
# contraste: a mesma guarda sobre o candidato ANTIGO (tem de recusar)
old = rd(os.path.join(V, "um_v411_candidato.py.bak_20261112_195053"))
vo = GC.verificar({"um_py": old}, b)
print("candidato antigo na guarda do construtor: ok =", vo["ok"], "| achados:", len(vo["achados"]), "| regras:", sorted({a["regra"] for a in vo["achados"]}))
