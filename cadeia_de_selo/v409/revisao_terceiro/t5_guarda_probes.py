import importlib.util, sys, json
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v409_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
G = m._v409_guarda_frases
casos = [
 # R1 (4 sondas) -- devem PEGAR
 ("nem o par na face de Fock, que segue [OPEN].", True), ("[OPEN] o par na face de Fock como ligacao;", True), ("[OPEN] o Ω do psíon da luz como o uniforme da instância", True), ("a ligação do par de Fock segue em aberto", True),
 ("o par de psíons na face de Fock (ligação) [OPEN]", True), ("the pair on the Fock face remains [OPEN]", True), ("o par na face de Fock segue aberto", True),
 # R2 (a forma do MEDIO e as 6 do construtor) -- devem PEGAR
 ("[REAL: os termos do kernel do rito · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]", True),
 ("o par na face de Fock ainda não foi ligado", True), ("a ligação do par na face de Fock fica para a v411", True), ("a ligação passa à v412", True), ("a ligação do par na face de Fock segue aberta", True), ("a ligação do par na face de Fock permanece pendente", True), ("o resto fica para a v411", True),
 # sondas MINHAS (independentes) -- devem PEGAR
 ("[INPUT: a ordem · OPEN: o Ω do psíon da luz como o uniforme da instância · KNOWN: x]", True),
 ("o par de psíons na face de Fock continua por fazer", True), ("the pair on the Fock face is still pending", True), ("the link of the pair on the Fock face is not yet linked", True), ("a ligação do par de Fock fica deixada para a v413", True),
 ("o par na face de Fock está pendente de prova", True), ("nesta versão o par de Fock ficou em aberto", True),
 ("[REAL: x · OPEN: o par na face de Fock como ligação]", True),
 # frases certas -- devem PASSAR
 ("[REAL: os termos do kernel do rito, as respostas do operador conferidas nele, a instância de brinquedo calculada, o par na face de Fock LIGADO (`ParNaFaceDeFock`) · INPUT: a ordem e as falas do operador · KNOWN: as referências do alcance · PODADA: a identidade de vetores Ω = uniforme (a ponte é a inscrição) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]", False),
 ("nem que o par finito de Bell e o par de Fock sejam o mesmo objeto (espaços distintos, a MESMA Meia-Nat); o par na face de Fock está ligado nesta versão", False),
 ("o par na face de Fock está ligado nesta versão (ParNaFaceDeFock)", False), ("a identidade Ω = uniforme fica podada: a ponte é a inscrição", False),
 ("a E21 dizia que o par de psions na face de Fock ficava [OPEN] como LIGACAO a fazer; a ligacao foi feita na v409", False),
 ("a ligacao do [OPEN] da v407: o par de psions no setor 2 do Fock concreto da luz tem norma 1", False),
 ("a igualdade completa está provada para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, não creditação); para o leitor que só conta, não está provada (E28, validade não afirmada)", False),
 ("[OPEN] a independência da pergunta da máquina sem leitor · [OPEN] o teste com a natureza", False),
 ("eu quero que entre tudo na versão 409 não deixar nada para a v410", None),
]
sai = []
for fr, deve in casos:
    g = G(fr) + m._v392_guarda_texto(fr)
    pega = bool(g); ok = None if deve is None else (pega == deve)
    sai.append({"frase": fr, "pega": pega, "esperado_pegar": deve, "ok": ok, "regras": [x[0] for x in g][:2]})
    print("%-6s" % ("PEGA" if pega else "PASSA"), "(esperado %s)" % ("pegar" if deve else "passar" if deve is False else "informativo"), "OK" if ok else ("FALHA" if ok is False else "--"), repr(fr[:78]), [x[0] for x in g][:2])
json.dump(sai, open(R + "revisao_terceiro/t5_guarda_probes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("FALHAS:", [s["frase"][:60] for s in sai if s["ok"] is False])
