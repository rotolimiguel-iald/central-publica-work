import sys, os, shutil, re, subprocess, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
POS = r"C:\t\k411c\revisao_C\nos_pos"; VAR = r"C:\t\k411c\revisao_C\nos_var"
if not os.path.exists(VAR):
    shutil.copytree(POS, VAR)
MUT = ["um_absoluto_pt.txt", "um_absoluto_en.txt", "um_absoluto_forma_canonica.md", "rodada_v411_stdout.txt", "um_absoluto_pt.toc", "um_absoluto_en.toc", "um_absoluto_selo.json"]
def restore():
    for f in MUT:
        p = VAR + "\\" + f
        if os.path.exists(p): os.remove(p)
        shutil.copyfile(POS + "\\" + f, p)
def rw(f, fn):
    p = VAR + "\\" + f; t = rd(p); t2 = fn(t); assert t2 != t, ("mutacao nao mudou nada", f)
    open(p, "wb").write(t2.encode("utf-8"))
pt = rd(POS + r"\um_absoluto_pt.txt"); en = rd(POS + r"\um_absoluto_en.txt")
i = pt.find("Dois resultados abrem este resumo"); j = en.find("Two results open this abstract")
print("topo pt em", i, "en em", j)
seg_pt = pt[i:i+1500]
m = re.search(r"a (\d+,\d+)σ", seg_pt); print("trecho pt:", seg_pt[:700].replace("\n", " "))

VARS = {
 "V1_recuo_pt": [("um_absoluto_pt.txt", lambda t: t.replace("Dois resultados abrem este resumo.", "O texto do topo não é dito nesta rodada.", 1))],
 "V2_numero_pt": [("um_absoluto_pt.txt", lambda t: t.replace("6,11$σ$", "6,12$σ$", 1))],
 "V3_sem_cefeidas_pt": [("um_absoluto_pt.txt", lambda t: t.replace("4,38$σ$", "", 1))],
 "V4_recuo_en": [("um_absoluto_en.txt", lambda t: t.replace("Two results open this abstract.", "The top text is not stated this round.", 1))],
 "V5_en_sem_validade": [("um_absoluto_en.txt", lambda t: t.replace("(validity, not creditation)", "", 1))],
 "V6_pt_vazio": [("um_absoluto_pt.txt", lambda t: "")],
 "V7_stdout_sem_bloco": [("rodada_v411_stdout.txt", lambda t: t.replace("H0DN x BG1 ABERTO [v411", "H0DN x BG1 [v411"))],
 "V8_md_sem_linha": [("um_absoluto_forma_canonica.md", lambda t: t.replace("> **H0DN × BG1 ABERTO (v411", "> **H0DN × BG1 (v411", 1))],
}
only = sys.argv[1:] or list(VARS)
res = {}
for nome in only:
    restore()
    for f, fn in VARS[nome]:
        try:
            rw(f, fn)
        except AssertionError as e:
            print(nome, "MUTACAO NAO APLICOU", e); res[nome] = "MUTACAO_NAO_APLICOU"; break
    else:
        out = r"C:\t\k411c\revisao_C\conf_%s_out.txt" % nome
        with open(out, "wb") as fo:
            r = subprocess.run([sys.executable, "-B", "-X", "utf8", RT + r"\c_run_conf.py", VAR, "_REV_C_" + nome], stdout=fo, stderr=subprocess.STDOUT)
        t = rd(out)
        nao = [l.strip()[:150] for l in t.split("\n") if l.strip().startswith("[NAO]")]
        veredito = "TUDO BATE" if "\nTUDO BATE" in t else ("NAO BATE" if "\nNAO BATE" in t else "SEM_VEREDITO(%s)" % t[-200:].replace("\n", " | "))
        res[nome] = {"veredito": veredito, "n_nao": len(nao), "nao": nao[:6]}
        print(nome, veredito, len(nao)); [print("    ", n) for n in nao[:6]]
json.dump(res, open(RT + r"\c_13_resultado.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
