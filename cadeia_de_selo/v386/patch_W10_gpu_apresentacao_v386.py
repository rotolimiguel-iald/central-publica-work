# -*- coding: utf-8 -*-
"""W10 (v386) — ORDEM DO OPERADOR (05/10/2026, tarde): «verifique se a apresentação do artigo, logo no início, quando apresenta-se o programa terminal
da TGL, se foi inserido o texto dizendo o teste que o programa agora faz em tempo real na GPU, isso também precisa estar no sumário do artigo».
MEDIDO no artigo selado v385 (um_absoluto_pt.txt / _en.txt / .toc): a apresentação (linha 2), o resumo (linhas 13–21) e as palavras-chave (23)
têm 0 ocorrências de «GPU»; a primeira menção está na «Introdução: o que este código faz agora (v384)» (linha 77) e na «Nota: o que se calcula na
GPU e como» (87) — ambas section*/subsection* (sem numeração), logo AUSENTES do sumário (um_absoluto_pt.toc: 83 entradas, 0 «GPU»).
O QUE ESTE PATCH FAZ (PT e EN; números LIDOS do core em runtime — nunca literais; fail-closed se o resumo do pilar faltar):
 (1) a apresentação (subtítulo) ganha a oração do teste em tempo real na GPU; (2) o resumo («O método») ganha a frase; (3) as palavras-chave ganham
 o termo; (4) o sumário passa a listar «Ao lado (v385)», «Introdução (v384)» e a «Nota: GPU» por \addcontentsline (as seções seguem sem numeração).
Aplica-se ao candidato v386 (depois dos patches do gerador); cada troca é única (assert). Modo --teste: aplica a uma CÓPIA em memória do um.py do Nós e
faz ast.parse, sem gravar nada."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")

QP_PT = (
    '    _nclean = (core.get("external_ladder") or {}).get("n_theorems_clean") or "auditados"\n',
    '    _nclean = (core.get("external_ladder") or {}).get("n_theorems_clean") or "auditados"\n'
    '    # v386 (W10, ordem do operador 05/10/2026): o teste que o programa faz em tempo real na GPU entra na APRESENTAÇÃO, no resumo, nas\n'
    '    # palavras-chave e no sumário; números lidos do core (pilar computado ou reaproveitado: o resumo é montado pela mesma _qp_summary); nunca literais\n'
    '    _qs = ((core.get("quantum_pillar_v384") or {}).get("summary") or {})\n'
    '    _qt2, _qt4, _qcpu, _qenv = (_qs.get("T2") or {}), (_qs.get("T4") or {}), (_qs.get("cpuref") or {}), (_qs.get("env") or {})\n'
    '    if all(_qt2.get(k_) is not None for k_ in ("points", "unique")) and _qt4.get("instances") is not None and _qcpu.get("compared") is not None:\n'
    '        _qp_sub = (r", e calcula em tempo real na GPU (" + str(_qenv.get("gpu") or "GPU").replace("_", r"\\_").replace("&", r"\\&")\n'
    '                   + r") --- em paralelo com o kernel e os ritos --- o sistema quântico aberto da teoria, o hamiltoniano luminodinâmico e os cinco "\n'
    '                   r"saltos de Lindblad, com atrator único em " + str(_qt2.get("unique")) + r" de " + str(_qt2.get("points"))\n'
    '                   + r" configurações da grade, " + str(_qt4.get("instances")) + r" instâncias de estresse e referência independente na CPU ("\n'
    '                   + str(_qcpu.get("compared")) + r" comparações, " + str(_qcpu.get("disagreements")) + r" discordâncias) --- cálculo do sistema "\n'
    '                   r"da teoria \\textsf{[COMPUTED]}, não medição da natureza")\n'
    '    else:\n'
    '        _qp_sub = r", e calcula em tempo real na GPU o sistema quântico aberto da teoria (nesta rodada o pilar quântico não trouxe resumo: dito, não suposto)"\n',
)
QP_EN = (
    '    _nclean = (core.get("external_ladder") or {}).get("n_theorems_clean") or "audited"\n',
    '    _nclean = (core.get("external_ladder") or {}).get("n_theorems_clean") or "audited"\n'
    '    # v386 (W10, operator order 2026-10-05): the real-time GPU test enters the PRESENTATION, the abstract, the keywords and the contents\n'
    '    _qs = ((core.get("quantum_pillar_v384") or {}).get("summary") or {})\n'
    '    _qt2, _qt4, _qcpu, _qenv = (_qs.get("T2") or {}), (_qs.get("T4") or {}), (_qs.get("cpuref") or {}), (_qs.get("env") or {})\n'
    '    if all(_qt2.get(k_) is not None for k_ in ("points", "unique")) and _qt4.get("instances") is not None and _qcpu.get("compared") is not None:\n'
    '        _qp_sub = (r", and computes in real time on the GPU (" + str(_qenv.get("gpu") or "GPU").replace("_", r"\\_").replace("&", r"\\&")\n'
    '                   + r") --- in parallel with the kernel and the rites --- the theory\'s open quantum system, the luminodynamic Hamiltonian and the "\n'
    '                   r"five Lindblad jump operators, with a unique attractor in " + str(_qt2.get("unique")) + r" of " + str(_qt2.get("points"))\n'
    '                   + r" grid configurations, " + str(_qt4.get("instances")) + r" stress instances and an independent CPU reference ("\n'
    '                   + str(_qcpu.get("compared")) + r" comparisons, " + str(_qcpu.get("disagreements")) + r" disagreements) --- a computation of the "\n'
    '                   r"theory\'s system \\textsf{[COMPUTED]}, not a measurement of nature")\n'
    '    else:\n'
    '        _qp_sub = r", and computes in real time on the GPU the theory\'s open quantum system (in this run the quantum pillar brought no summary: stated, not assumed)"\n',
)
PATCHES = [
    ("W10a_PT_qp_sub", QP_PT[0], QP_PT[1]),
    ("W10b_PT_subtitulo",
     '             r"confronta a massa dos neutrinos "\n'
     '             r"com falsificadores pré-registrados --- tudo enquanto audita um kernel Lean de "\n',
     '             r"confronta a massa dos neutrinos "\n'
     '             r"com falsificadores pré-registrados" + _qp_sub + r" --- tudo enquanto audita um kernel Lean de "\n'),
    ("W10c_PT_metodo",
     '             r"são emitidos pela máquina, nunca por declaração. A cadeia é "\n',
     '             r"são emitidos pela máquina, nunca por declaração; e o mundo quântico da teoria --- o sistema aberto GKLS do pilar pré-registrado --- "\n'
     '             r"é calculado em tempo real na GPU, em paralelo com o kernel e os ritos (cálculo do sistema, não medição da natureza). A cadeia é "\n'),
    ("W10d_PT_palavras_chave",
     '             r"piso dos vazios cósmicos\\par\\vspace{4pt}")\n',
     '             r"piso dos vazios cósmicos; sistema quântico aberto (GKLS) calculado em tempo real na GPU\\par\\vspace{4pt}")\n'),
    ("W10e_PT_sumario_v385",
     '    s.append(r"\\section*{Ao lado (v385): o Axioma e a testemunha falsa}")\n',
     '    s.append(r"\\section*{Ao lado (v385): o Axioma e a testemunha falsa}")\n'
     '    s.append(r"\\addcontentsline{toc}{section}{Ao lado (v385): o Axioma e a testemunha falsa}")   # v386 (W10): no sumário\n'),
    ("W10f_PT_sumario_intro",
     '    s.append(r"\\section*{Introdução: o que este código faz agora (v384)}")\n',
     '    s.append(r"\\section*{Introdução: o que este código faz agora (v384)}")\n'
     '    s.append(r"\\addcontentsline{toc}{section}{Introdução: o que este código faz agora (v384) --- o kernel, os ritos e o mundo quântico na GPU}")   # v386 (W10): no sumário\n'),
    ("W10g_PT_sumario_gpu",
     '    s.append(r"\\subsection*{Nota: o que se calcula na GPU e como}")\n',
     '    s.append(r"\\subsection*{Nota: o que se calcula na GPU e como}")\n'
     '    s.append(r"\\addcontentsline{toc}{subsection}{Nota: o que se calcula na GPU e como (em tempo real, em paralelo com o kernel e os ritos)}")   # v386 (W10): no sumário\n'),
    ("W10h_EN_qp_sub", QP_EN[0], QP_EN[1]),
    ("W10i_EN_subtitle",
     '             r"confronts the neutrino mass with pre-registered falsifiers --- all while auditing a Lean "\n',
     '             r"confronts the neutrino mass with pre-registered falsifiers" + _qp_sub + r" --- all while auditing a Lean "\n'),
    ("W10j_EN_method",
     '             r"--- are emitted by the machine, never by declaration. The chain is "\n',
     '             r"--- are emitted by the machine, never by declaration; and the theory\'s quantum world --- the pre-registered open GKLS system of the "\n'
     '             r"pillar --- is computed in real time on the GPU, in parallel with the kernel and the rites (a computation of the system, not a measurement of nature). The chain is "\n'),
    ("W10k_EN_keywords",
     '             r"cosmic void floor\\par\\vspace{4pt}")\n',
     '             r"cosmic void floor; open quantum system (GKLS) computed in real time on the GPU\\par\\vspace{4pt}")\n'),
    ("W10l_EN_contents_v385",
     '    s.append(r"\\section*{Beside (v385): the Axiom and the false witness}")\n',
     '    s.append(r"\\section*{Beside (v385): the Axiom and the false witness}")\n'
     '    s.append(r"\\addcontentsline{toc}{section}{Beside (v385): the Axiom and the false witness}")   # v386 (W10): in the contents\n'),
    ("W10m_EN_contents_intro",
     '    s.append(r"\\section*{Introduction: what this code does now (v384)}")\n',
     '    s.append(r"\\section*{Introduction: what this code does now (v384)}")\n'
     '    s.append(r"\\addcontentsline{toc}{section}{Introduction: what this code does now (v384) --- the kernel, the rites and the quantum world on the GPU}")   # v386 (W10): in the contents\n'),
    ("W10n_EN_contents_gpu",
     '    s.append(r"\\subsection*{Note: what is computed on the GPU and how}")\n',
     '    s.append(r"\\subsection*{Note: what is computed on the GPU and how}")\n'
     '    s.append(r"\\addcontentsline{toc}{subsection}{Note: what is computed on the GPU and how (in real time, in parallel with the kernel and the rites)}")   # v386 (W10): in the contents\n'),
]


def aplicar(src):
    """Aplica os patches W10 a `src` (texto do um.py); cada `old` deve ocorrer exatamente uma vez. Devolve (texto_novo, relatorio)."""
    rel = []
    nl = "\r\n" if src.count("\r\n") > src.count("\n") // 2 else "\n"   # o um.py pode ser CRLF: os patches seguem o fim de linha do arquivo
    for nome, old, new in PATCHES:
        if nl != "\n":
            old, new = old.replace("\n", nl), new.replace("\n", nl)
        n = src.count(old)
        assert n == 1, (nome, "ocorrencias", n)
        src = src.replace(old, new); rel.append((nome, len(new) - len(old)))
    ast.parse(src)
    return src, rel


if __name__ == "__main__":
    if "--teste" in sys.argv:
        P = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "um.py")
        src = open(P, encoding="utf-8", newline="").read()
        novo, rel = aplicar(src)
        print("TESTE OK (copia em memoria do um.py do Nos; nada gravado):", len(src), "->", len(novo), "chars;", len(rel), "trocas")
        for nome, d in rel:
            print("  ", nome, "%+d" % d)
    else:
        print("uso: --teste  (ou importar aplicar() do gerador do candidato)")
