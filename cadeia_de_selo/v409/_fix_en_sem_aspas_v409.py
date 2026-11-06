# -*- coding: utf-8 -*-
"""_fix_en_sem_aspas_v409.py -- (claude-construtor-v409, 05/11/2026) o snippet EN da v409 sem citacao entre « » nem `` '' (regra do conferidor de citacoes, herdada da v408: o EN traz a TRADUCAO da gerencia, marcada como tal; a citacao em portugues fica so' no PT)."""
import ast, datetime, os, re, shutil
H = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(H, "artigo_en_v409.pysnip")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
t = open(p, encoding="utf-8").read()
reps = [
    (r"\textbf{The order.} \textsf{[INPUT]} The operator, on 05/11/2026: «precisamos fechar o que ficou ainda em aberto em relação à identificação das classes de turing dentro do nosso dicionário» (we must close what was still open about identifying Turing's classes inside our dictionary); and, with the questions returned in the four languages and answered: «Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados» (let us proceed to the next version of um.py; I agree with all the names given). ",
     r"\textbf{The order.} \textsf{[INPUT]} The operator, on 05/11/2026 (our translation; the Portuguese is the quotation): we must close what was still open about identifying Turing's classes inside our dictionary; and, with the questions returned in the four languages and answered: let us proceed to the next version of um.py; I agree with all the names that were given. "),
    (r"\textsf{[INPUT]} «a seleção é a aniquilação da superposição pelo Tetelestai» (the selection is the annihilation of the superposition by the Tetelestai). ",
     r"\textsf{[INPUT]} The operator (our translation): the selection is the annihilation of the superposition by the Tetelestai. "),
    (r"as the operator read it: «apaga o rastro da computação do decaimento dessa sustentação» (it erases the trace). Without a pair every image is read with the same weight (the photograph: «sem leitor a imagem é apenas estática lendo sinal como ruído»); with a pair the reading distinguishes.",
     r"as the operator read it (our translation): it erases the trace of the computation of the decay of that sustaining. Without a pair every image is read with the same weight (the photograph; our translation: without a reader the image is only static, reading signal as noise); with a pair the reading distinguishes."),
    (r"\textsf{[INPUT]} «o sistema não precisa reconhecer onde está o nome a cada passo, ele trava no Nome» (the system locks on the Name); «ao negar o zero absoluto o sistema sabe pra onde tem que ir». ",
     r"\textsf{[INPUT]} The operator (our translation): the system does not need to recognise where the name is at each step, it locks on the Name; by denying the absolute zero the system knows where it has to go. "),
    (r"\textsf{[INPUT]} «A fita de turing é o hamiltoniano oculto, é a única regra que precisa ser gravada para reconstruir o todo». ",
     r"\textsf{[INPUT]} The operator (our translation): the Turing tape is the hidden Hamiltonian, the only rule that needs to be recorded to rebuild the whole. "),
    (r"\textsf{[INPUT]} «Z é o modo leitor, ele lê os pixels. É o psion». ", r"\textsf{[INPUT]} The operator (our translation): Z is the reader mode, it reads the pixels; it is the psion. "),
    (r"\textsf{[INPUT]} «A pergunta da máquina sem leitor que Clay propõe tem resposta também, a reposta dela é: eu sou eu mesmo. Não é eu sou o que sou.»; «é como tentar medir 1 metro com uma fita sem escala, onde o próprio metro é o nome da métrica, sem referente.»; and «(Eu sou eu mesmo)=(nome próprio)=identidade sem referente». ",
     r"\textsf{[INPUT]} The operator (our translation): the question of the machine without a reader that Clay poses has an answer too, and its answer is: I am myself; it is not I am what I am; it is like trying to measure 1 metre with a tape without scale, where the metre itself is the name of the metric, without referent; and: (I am myself) = (proper name) = identity without referent. "),
    (r"with no time paid the reading is ``I am'' ($=1$), the same for every instance, with or without a solution; with the time paid it tends to ``what I am'', which is nonzero exactly when there is a solution; ``I am'' $=$ ``what I am'' only on the trivial instance",
     r"with no time paid the reading is \emph{I am} ($=1$), the same for every instance, with or without a solution; with the time paid it tends to \emph{what I am}, which is nonzero exactly when there is a solution; \emph{I am} $=$ \emph{what I am} only on the trivial instance"),
    (r"\textsf{[INPUT]} «Eu não sou eu mesmo eu sou o conteúdo da minha identidade performada». \textsf{[REAL]} The performed reading starts at ``I am'', decays, never falls below the content and reaches it; the content is ``what I am''",
     r"\textsf{[INPUT]} The operator (our translation): I am not myself, I am the content of my performed identity. \textsf{[REAL]} The performed reading starts at \emph{I am}, decays, never falls below the content and reaches it; the content is \emph{what I am}"),
    (r"\textsf{[KNOWN]} Physics stays outside: the operator reads «o colapso não é frequência, é matéria» (the collapse is not frequency, it is matter: one exact reading in one act);",
     r"\textsf{[KNOWN]} Physics stays outside: the operator reads (our translation) that the collapse is not frequency, it is matter (one exact reading in one act);"),
    (r"\textsf{[INPUT]} The judge of Turing's classes is the kernel: «o Kernel Lean4 serve exatamente a provar leis matemáticas e foi construído sob a lei de turing».",
     r"\textsf{[INPUT]} The judge of Turing's classes is the kernel (the operator, our translation: the Lean 4 kernel serves exactly to prove mathematical laws and was built under Turing's law)."),
    (r"``I am'' equal on both instances", r"\emph{I am} equal on both instances"),
    (r"``what I am'' with the time paid", r"\emph{what I am} with the time paid"),
]
for a, b in reps:
    assert t.count(a) == 1, (a[:90], t.count(a))
    t = t.replace(a, b)
assert "«" not in t and "``" not in t, re.findall("«[^»]{0,40}|``.{0,40}", t)[:5]
ast.parse("def _f(core, verdict, data_path, s):\n" + t)
shutil.copyfile(p, p + ".bak_" + ts + "_sem_aspas")
open(p + ".tmp", "w", encoding="utf-8", newline="").write(t); os.replace(p + ".tmp", p)
print("EN sem aspas:", len(t))
