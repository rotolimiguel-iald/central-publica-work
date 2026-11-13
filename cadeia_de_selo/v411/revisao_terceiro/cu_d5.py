import os
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
nomes = ["um.py", "um_absoluto.json", "um_absoluto_pt.txt", "um_absoluto_en.txt", "um_absoluto_pt.toc", "um_absoluto_en.toc", "um_absoluto_pt.tex", "um_absoluto_en.tex", "um_absoluto_pt.pdf", "um_absoluto_en.pdf",
         "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "um_absoluto_selo.json", "um_absoluto_selo_acom.json", "tgl_kernel"]
for n in nomes:
    p = os.path.join(NOS, n)
    print("%-34s %s" % (n, "existe" + (" (dir)" if os.path.isdir(p) else " %d B" % os.path.getsize(p)) if os.path.exists(p) else "AUSENTE"))
for n in ("rodada_v411_stdout.txt",):
    print("%-34s %s" % (n, "existe" if os.path.exists(os.path.join(NOS, n)) else "ausente hoje (o rito o grava; o rito_v411.sh move um anterior para _tentativaN)"))
print("rito_horarios_v411.txt no pacote:", os.path.exists(os.path.join(V, "rito_horarios_v411.txt")), "(o rito o grava em $PK, linhas 248 e 261 do rito_v411.sh; o conferidor le HERE antes do Nos)")
# o um.py v410 do Nos e' mesmo o 'base'?
import hashlib
print("um.py do Nos sha16:", hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16])
