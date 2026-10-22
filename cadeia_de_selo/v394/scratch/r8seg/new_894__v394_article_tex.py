def _v394_article_tex(text, core, lang):
    """Append the actual current-run result and scoped mathematics in both languages."""
    out = core.get('tempo_frequencia_v394') or {}
    pt = lang == 'pt'
    title = 'Tempo, frequencia e leitura gravitacional: composicao v394' if pt else 'Time, frequency and gravitational reading: v394 composition'
    def esc(value):
        replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
        return ''.join(replacements.get(ch, ch) for ch in str(value))
    block = '\n\\section*{' + title + '}\n'
    block += ('Resultado desta rodada: ' if pt else 'Result of this run: ') + esc(out.get('verdict', 'NOT_RUN')) + '.\n\n'
    block += (r'No modelo $M_2$, a conjugacao $C=\mathrm{diag}(1,i)$ realiza a ponte espectral: $H_g=CH_{lig}C^\dagger=iV_0K$, $\Omega=V_0/\hbar$. O fluxo continuo e seu relogio sao derivados para estes objetos. ' if pt else
              r'In the $M_2$ model, conjugation $C=\mathrm{diag}(1,i)$ realizes the spectral bridge: $H_g=CH_{lig}C^\dagger=iV_0K$, $\Omega=V_0/\hbar$. The continuous flow and its clock are derived for these objects. ')
    block += r'\[T_t(X)=U_t\{E_g(X)+e^{-\gamma t}[X-E_g(X)]\}U_t^\dagger,\qquad E_gT_t=E_g.\]' + '\n'
    block += r'\[c(t)=e^{(-\gamma+2i\Omega)t}c(0),\qquad\Delta t=\frac{\Delta\phi}{2\Omega}=-\frac{\log|c(t_2)/c(t_1)|}{\gamma}.\]' + '\n'
    block += ('As duas leituras de tempo exigem coerencia nao nula, gamma positivo e fase levantada. O espaco fixo tem dimensao complexa dois. A fase isolada admite alias; leitura preservada nao e preservacao de todo produto.\n\n' if pt else
              'The two clock readings require nonzero coherence, positive gamma and a lifted phase. The fixed space has complex dimension two. A single phase admits aliases; preserved reading does not preserve every product.\n\n')
    block += r'\[H_{pos}=E_{ref}I+H_g,\quad E_{ref}\ge V_0,\quad\gamma=\frac{\beta}{2\hbar}\left(\sqrt{E_{ref}+V_0}-\sqrt{E_{ref}-V_0}\right)^2.\]' + '\n'
    block += ('A referencia energetica e parte do contrato fisico. O caso Eref=V0 e uma instancia matematica, nao uma nova identificacao atomica universal. Os calculos sao sinteticos; nao acreditam a natureza e nao alteram o gate.\n\n' if pt else
              'The energy reference is part of the physical contract. Eref=V0 is a mathematical instance, not a new universal atomic identification. Calculations are synthetic; they neither credit nature nor change the gate.\n\n')
    block += ('Cunhagens do operador, preservadas na lingua original [INPUT/ONTO]:\n' if pt else 'Operator inscriptions, preserved in their original language [INPUT/ONTO]:\n')
    for record in _V394_INSCRIPTIONS.values():
        block += '\\begin{quote}\n' + esc(record['text']) + '\n\\end{quote}\n'
    quadratic = core.get('regra_quadratica_v394') or {}
    block += ('Regra quadratica desta rodada: ' if pt else 'Quadratic rule in this run: ') + esc(quadratic.get('verdict', 'NOT_RUN')) + '.\n'
    block += r'\[r_A(X)=\operatorname{Tr}[(E_gX-A)^\dagger(E_gX-A)],\quad r_A(X)=0\iff E_gX=A,\quad r_A(T_tX)=r_A(X).\]' + '\n'
    block += ('O residuo testa correspondencia da leitura com uma ancora fixada; e constante no fluxo e nao identifica estados brutos diferentes. O plano de polarizacao e a imagem de Eg sao objetos distintos.\n' if pt else 'The residual tests correspondence with a fixed anchor; it is constant along the flow and does not identify distinct raw states. The polarization plane and the image of Eg are distinct objects.\n')
    network = core.get('rede_fock_v394') or {}
    block += ('Rede Fock nesta rodada: ' if pt else 'Fock network in this run: ') + esc(network.get('verdict', 'NOT_RUN')) + '.\n'
    block += ('Na mesma Fock, o Tomita real, seu quadrado e o fluxo modular foram ligados a Gamma(B0(-2 pi t)); KMS da cunha e fornecido por termo. Campos de Segal essencialmente auto-adjuntos e representacao escalar de Lorentz foram construidos. Rede global de helicidade, traco escalado e fonte Maxwell conjuntos continuam abertos. Resultados de versoes anteriores preservam seus alcances historicos.\n' if pt else 'On the same Fock, the actual Tomita, its square and modular flow are identified with Gamma(B0(-2 pi t)); wedge KMS is a theorem. Essentially self-adjoint Segal fields and the scalar Lorentz representation are constructed. The joint global helicity net, scaled trace and Maxwell source remain open. Earlier-version results retain their historical scope.\n')
    assert text.count(r'\end{document}') == 1, 'article boundary missing or ambiguous'
    return text.replace(r'\end{document}', block + '\n' + r'\end{document}')