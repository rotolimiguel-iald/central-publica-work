p = "c_fail_closed.py"
t = open(p, encoding="utf-8").read()
old = '    ("a igualdade completa vale so\' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay; E28)", False),\n]'
new = '''    ("a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay; E28)", False),
    # R3: a forma do MEDIO da R2 e as paraphrases; a frase nova do leitor
    ("[REAL: os termos do kernel do rito · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]", True),
    ("o par na face de Fock ainda não foi ligado", True), ("a ligação do par na face de Fock fica para a v411", True), ("a ligação passa à v412", True), ("a ligação do par na face de Fock segue aberta", True), ("a ligação do par na face de Fock permanece pendente", True), ("o resto fica para a v411", True),
    ("[INPUT: a ordem · OPEN: o Ω do psíon da luz como o uniforme da instância · KNOWN: x]", True), ("the pair on the Fock face is still pending", True),
    ("[REAL: x, o par na face de Fock LIGADO (`ParNaFaceDeFock`) · PODADA: a identidade de vetores Ω = uniforme (a ponte é a inscrição) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]", False),
    ("a igualdade completa está provada para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, não creditação); para o leitor que só conta, não está provada (E28, validade não afirmada)", False),
]'''
assert old in t
open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
print("ok")
