import re, sys
sys.stdout.reconfigure(encoding="utf-8")
src = open("t6_varredura_independente_r3.py", encoding="utf-8").read()
# extrai so' as definicoes (ruim, isenta, segs, varre) sem rodar a varredura
pre = src.split("A = {}")[0]
ns = {}; exec(pre.replace("sys.stdout.reconfigure(encoding=\"utf-8\")", ""), ns)
casos = ["[REAL: x · KNOWN: y · OPEN: o par na face de Fock como ligação, a independência da pergunta]", "o par na face de Fock ainda não foi ligado", "o Ω do psíon da luz como o uniforme da instância [OPEN]", "a ligação do par de Fock fica para a v411",
         "the pair on the Fock face remains open", "a E21 dizia que o par de Fock ficava [OPEN]", "o par na face de Fock está ligado nesta versão", "o par de Fock é pendência"]
for c in casos:
    D = {}; ns["varre"]("t", c, D); print("PEGA " if D else "passa", "|", c)
