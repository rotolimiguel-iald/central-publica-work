# -*- coding: utf-8 -*-
"""_r6c_12_aditivo1_guarda_o_que_sai_v410.py -- ADITIVO 1, parte A2: o texto LITERAL do README_O_QUE_SAI cita o titulo do bloco de hoje do README, que traz «P = nP» sem o qualificador, e remete ao «bloco pronto acima»;
lido SOZINHO pela guarda das frases ele cai na obrigacao F34 (onde «P = nP» aparece, o MESMO texto traz o qualificador). Adaptacao mecanica minima, dita no relatorio (a redacao da ordem NAO muda): em guardas_dos_textos,
a guarda das frases le o README_O_QUE_SAI JUNTO do README_FRENTE (o bloco a que ele remete, que traz a forma da D81 com o qualificador); o portao do G1 e as demais regras continuam lendo o bloco sozinho.
Idempotente; backup de BYTES; CRLF como o arquivo; temporario + os.replace; ast.parse. (Escrito pelo Write: o heredoc do Bash colapsa as barras.)"""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); p = os.path.join(HERE, "pos_rito", "textos_custodia_handoff_v410.py"); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
assert t.count("\r\n") == t.count("\n") > 0
BS = chr(92)
A = "        v1 = [list(x) for x in GF.violacoes(t)]\r\n"
N = ("        v1 = [list(x) for x in GF.violacoes((README_FRENTE + \"" + BS + "n" + BS + "n\" + t) if ident == \"README_O_QUE_SAI\" else t)]   # (ADITIVO 1) o README_O_QUE_SAI cita o titulo do bloco de hoje do README e remete ao bloco pronto acima: "
     "a guarda das frases o le JUNTO do README_FRENTE, que traz o qualificador (a obrigacao F34 e' do MESMO texto); o portao do G1 e as demais regras leem o bloco sozinho\r\n")
if N in t:
    print("ja' feito")
else:
    assert t.count(A) == 1, t.count(A)
    t1 = t.replace(A, N); ast.parse(t1.replace("\r\n", "\n")); b1 = t1.encode("utf-8")
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_aditivo1b"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
    open(p + ".tmp_r6c", "wb").write(b1); os.replace(p + ".tmp_r6c", p); print("pos_rito/textos_custodia_handoff_v410.py: a guarda das frases le o README_O_QUE_SAI junto do README_FRENTE | backup", os.path.basename(bak))
