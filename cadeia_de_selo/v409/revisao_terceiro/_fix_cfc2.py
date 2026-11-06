p = "c_fail_closed.py"
t = open(p, encoding="utf-8").read()
old = '    (E28 + "; o oráculo de contagem", False),\n]'
new = '''    (E28 + "; o oráculo de contagem", False),
    # R2: as quatro sondas da R1 (MEDIO) agora devem REPROVAR; as frases certas (R2) devem PASSAR
    ("nem o par na face de Fock, que segue [OPEN].", True), ("[OPEN] o par na face de Fock como ligacao;", True), ("[OPEN] o Ω do psíon da luz como o uniforme da instância", True), ("a ligação do par de Fock segue em aberto", True),
    ("nem que o par finito de Bell e o par de Fock sejam o mesmo objeto (espaços distintos, a MESMA Meia-Nat); o par na face de Fock está ligado nesta versão", False),
    ("[REAL] o par na face de Fock LIGADO (ParNaFaceDeFock); PODADA a identidade de vetores Omega = uniforme (a ponte e' a inscricao); [OPEN] a independencia de P vs NP dos axiomas; a igualdade com o leitor que so' conta (E28); o teste com a natureza", False),
    ("a E21 dizia que o par de psions na face de Fock ficava [OPEN] como LIGACAO a fazer; a ligacao foi feita na v409", False),
    ("a ligacao do [OPEN] da v407: o par de psions no setor 2 do Fock concreto da luz tem norma 1", False),
    ("the pair on the Fock face stays [OPEN]", True), ("the pair on the Fock face is linked in this version", False),
    ("a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay; E28)", False),
]'''
assert old in t
t = t.replace(old, new)
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
