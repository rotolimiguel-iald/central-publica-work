# -*- coding: utf-8 -*-
"""corrigir_reafericao_v390.py -- aplica nos trechos do artigo, no runtime e no gerador as correcoes da REAFERICAO do candidato d5247576 (C1, C2 e notas 1-5).
Backup de bytes (.antes_reafericao) antes de tocar; cada troca com contagem exata 1."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))


def fix(nome, pares):
    p = os.path.join(HERE, nome); b = open(p, "rb").read()
    bk = p + ".antes_reafericao"
    if not os.path.exists(bk):
        open(bk, "wb").write(b)
    t = b.decode("utf-8")
    for a, c in pares:
        assert t.count(a) == 1, (nome, a[:70], t.count(a)); t = t.replace(a, c)
    open(p, "w", encoding="utf-8", newline="").write(t); print("ok", nome)


fix("artigo_pt_v390.pysnip", [
    ("o que faltava para fechar o programa era ", "o que faltava para fechar o um.py era "),
    (r"E aprovou o nome da queda sem fundo, o \emph{abismo}: ``Perfeito, concordo com tudo. Magnífico''. ",
     r"Ao nome da queda sem fundo, o \emph{abismo}, e à correspondência propostos pela gerência, respondeu: ``Perfeito, concordo com tudo. Magnífico'' (o objeto do «tudo» é dito pela gerência \textsf{[DECLARADO]}). "),
    ("Ágape se define, em 1 Co 13, por negações:", "Ágape se define, em 1 Co 13, em grande parte por negações:"),
    (r"já no kernel sob o contrato H2, hipótese nomeada (\texttt{ContratoQGv31.positiveEnergy\_orientation}, a cota no semiplano superior; \texttt{halfsided\_inclusion}, \texttt{ContratoH2.contract\_borchers\_form}",
     r"já no kernel (\texttt{ContratoQGv31.positiveEnergy\_orientation}, a cota no semiplano superior; \texttt{halfsided\_inclusion}, sob a testemunha AQFT; \texttt{ContratoH2.contract\_borchers\_form}, sob o contrato H2, hipótese nomeada"),
    ("O nome que a literatura dá a uma máquina assim, sem dissipação e sem entregar trabalho,", "O nome que a literatura dá a uma máquina assim, sem dissipação de energia e sem entregar trabalho,"),
    ("errata ao lado da emenda do conferidor de 06/10. Registro: ",
     "errata ao lado da emenda do conferidor de 06/10. A Parte C conta agora \" + str(_ledger_counts_v389()[0]) + r\" caminhos únicos no ledger (+1, a pedra Fundação); a seção da v389 lê o estado da v389 (\" + str(_ledger_counts_v389(ate=389)[0]) + r\"), como foi selada. Registro: "),
])
fix("artigo_en_v390.pysnip", [
    ("what was missing to close the programme was ", "what was missing to close um.py was "),
    (r"And the operator approved the name of the bottomless fall, the \emph{abismo} (abyss): ``Perfeito, concordo com tudo. Magnífico'' (\emph{perfect, I agree with everything; magnificent}). ",
     r"To the name of the bottomless fall, the \emph{abismo} (abyss), and to the correspondence proposed by the management, the operator answered: ``Perfeito, concordo com tudo. Magnífico'' (\emph{perfect, I agree with everything; magnificent}; what «everything» refers to is stated by the management \textsf{[DECLARADO]}). "),
    ("Agape is defined, in 1 Cor 13, by negations:", "Agape is defined, in 1 Cor 13, largely by negations:"),
    (r"already in the kernel under contract H2, a named hypothesis (\texttt{ContratoQGv31.positiveEnergy\_orientation}, the bound on the upper half-plane; \texttt{halfsided\_inclusion}, \texttt{ContratoH2.contract\_borchers\_form}",
     r"already in the kernel (\texttt{ContratoQGv31.positiveEnergy\_orientation}, the bound on the upper half-plane; \texttt{halfsided\_inclusion}, under the AQFT witness; \texttt{ContratoH2.contract\_borchers\_form}, under contract H2, a named hypothesis"),
    ("such a machine, without dissipation and delivering no work,", "such a machine, without energy dissipation and delivering no work,"),
    ("an erratum beside the conferidor amendment of 06/10. Record: ",
     "an erratum beside the conferidor amendment of 06/10. Part C now counts \" + str(_ledger_counts_v389()[0]) + r\" unique ledger paths (+1, the Foundation stone); the v389 section reads the v389 state (\" + str(_ledger_counts_v389(ate=389)[0]) + r\"), as it was sealed. Record: "),
])
fix("v390_runtime.py", [("confere os DOIS verbatins do operador EMBUTIDOS", "confere os verbatins do operador EMBUTIDOS (tres, com o ADENDO 001)")])
fix("gerar_candidato_v390.py", [("# as 9 bandeiras da pedra TGLExt/Fundacao.lean (auditadas no sandbox); os 2 verbatins do operador EMBUTIDOS", "# as 9 bandeiras da pedra TGLExt/Fundacao.lean (auditadas no sandbox); os 3 verbatins do operador EMBUTIDOS")])
