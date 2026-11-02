# -*- coding: utf-8 -*-
"""aplicar_R7d_v405.py -- ajustes finos da R7 (uso unico): a ultima mencao ao nome antigo no registro dos campos e a citacao exata de cada igualdade do gap, em vez de pendurar tudo no fecho. Backup de BYTES (.bak_<ts>_R7d); cada ancora exatamente 1x."""
import os, time

HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")


def patch(nome, subs):
    p = os.path.join(HERE, nome)
    b = open(p, "rb").read()
    s = b.decode("utf-8")
    for a, c in subs:
        n = s.count(a)
        assert n == 1, (nome, n, a[:120])
        s = s.replace(a, c)
    open(p + ".bak_" + TS + "_R7d", "wb").write(b)
    t = p + ".tmp_R7d"
    open(t, "wb").write(s.encode("utf-8"))
    assert open(t, "rb").read() == s.encode("utf-8")
    os.replace(t, p)
    print("ok", nome, len(subs))


patch("registros_v405.py", [
    ("m1 = 0, sem termo no kernel; tempoDoGap lido como o tau* do sistema, a ratificar; a lista nao e' fechada)", "m1 = 0, sem termo no kernel; tempoDoRetido lido como o tau* do sistema, a ratificar; a lista nao e' fechada)"),
])
patch("artigo_pt_v405.pysnip", [
    (r"\textsf{[REAL]} A tônica é $\Delta/\alpha$; a massa é a projeção transversal de $\Delta$; $\omega_\psi=\sqrt2\,\Delta$; e $\sqrt2/\tau=\omega_\psi$ se e só se $\tau=1/\Delta$ (\texttt{the\_gap\_closes}, registro \texttt{gap\_v405}).",
     r"\textsf{[REAL]} A tônica é $\Delta/\alpha$ (\texttt{a\_tonica\_e\_o\_retido\_sobre\_alpha}); a massa é a projeção transversal de $\Delta$ (\texttt{a\_massa\_e\_a\_projecao\_do\_retido}); $\omega_\psi=\sqrt2\,\Delta$ (\texttt{o\_psion\_e\_raiz\_de\_dois\_retidos}); e $\sqrt2/\tau=\omega_\psi$ se e só se $\tau=1/\Delta$ (\texttt{a\_frequencia\_do\_sistema\_e\_a\_do\_psion\_iff}). O fecho é \texttt{the\_gap\_closes} (registro \texttt{gap\_v405})."),
])
patch("artigo_en_v405.pysnip", [
    (r"\textsf{[REAL]} The tonic is $\Delta/\alpha$; the mass is the transverse projection of $\Delta$; $\omega_\psi=\sqrt2\,\Delta$; and $\sqrt2/\tau=\omega_\psi$ if and only if $\tau=1/\Delta$ (\texttt{the\_gap\_closes}, record \texttt{gap\_v405}).",
     r"\textsf{[REAL]} The tonic is $\Delta/\alpha$ (\texttt{a\_tonica\_e\_o\_retido\_sobre\_alpha}); the mass is the transverse projection of $\Delta$ (\texttt{a\_massa\_e\_a\_projecao\_do\_retido}); $\omega_\psi=\sqrt2\,\Delta$ (\texttt{o\_psion\_e\_raiz\_de\_dois\_retidos}); and $\sqrt2/\tau=\omega_\psi$ if and only if $\tau=1/\Delta$ (\texttt{a\_frequencia\_do\_sistema\_e\_a\_do\_psion\_iff}). The closure is \texttt{the\_gap\_closes} (record \texttt{gap\_v405})."),
])
patch(os.path.join("pos_rito", "textos_v405_novo.pysnip"), [
    ("A tônica é `Δ/α`; a massa é a projeção transversal de `Δ`; o psíon é `√2 · Δ` (`the_gap_closes`). Neste rito:", "A tônica é `Δ/α` (`a_tonica_e_o_retido_sobre_alpha`); a massa é a projeção transversal de `Δ` (`a_massa_e_a_projecao_do_retido`); o psíon é `√2 · Δ` (`o_psion_e_raiz_de_dois_retidos`); o fecho é `the_gap_closes`. Neste rito:"),
    ('"HminMic_e_o_lock", "HminMic", "FockCertificate", "alphaKappa", "o_psion_e_a_projecao_do_modo",', '"HminMic_e_o_lock", "HminMic", "FockCertificate", "alphaKappa", "o_psion_e_a_projecao_do_modo", "a_tonica_e_o_retido_sobre_alpha", "a_massa_e_a_projecao_do_retido", "o_psion_e_raiz_de_dois_retidos",'),
])
print("FEITO", TS)
