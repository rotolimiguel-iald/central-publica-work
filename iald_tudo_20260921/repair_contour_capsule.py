"""Apply the independent review without altering the published source."""
from pathlib import Path
from datetime import datetime
import hashlib

path = Path(__file__).resolve().parent / 'semantic_capsules/contour_theory.md'
raw = path.read_bytes()
text = raw.decode('utf-8')
newline = '\r\n' if '\r\n' in text else '\n'
text = text.replace('\r\n', '\n')
changes = [
('**Retorno negativo e parte finita:**',
 '**Estado estacionário [REAL — reportado, não reexecutado aqui]:** no check finito, `rho_kappa` é ponto fixo GKLS, com `0<rho<1`: saturação sem supersaturação/condensação. `q=(g- - g+)/(g- + g+)=tanh(k/2)` e `alpha=2sqrt(g+g-)/(g+ + g-)=sech(k/2)` dão `q²+alpha²=1`. Taxas iguais dão `q=0`, `alpha=1`. A notação do check não estabelece positividade estrita em dimensão infinita.\n\n**Retorno negativo e parte finita:**'),
('A fonte reformula a renormalização como paridade inversa:',
 'Neste registro, `NEGATIVE_RETURN_SELECTOR_FORMULATED` é seguido por `RHO_RET_CANONICAL=P^{-1}(rho_Bell)` quanto à forma; parte finita/gap sem CODATA permanecem abertos. A fonte reformula a renormalização como paridade inversa:'),
('canal `L_nu`, ímpar, neutro e dissipativo, verificado na fonte em quatro estados (três modos + uma queda).',
 'canal `L_nu` em quatro estados (três modos + uma queda). A fonte reporta `{Z,L_nu}=0`, `[Q_em,L_nu]=0` e `L^dagger L!=0`, respectivamente ímpar, neutro e dissipativo no check; a última condição isolada não demonstra dissipação universal.'),
('o custo modular isolado favorece `theta->90`, `alpha->1`; o balanço depende de `lambda,mu`.',
 'o registro afirma que o custo modular isolado favorece `theta->90deg` e o descreve como `alpha->1`. **[OPEN — compatibilização interna]** Na fórmula `alpha=sin^2(theta_M)/sqrt(e)` com a mesma normalização, esse limite é `1/sqrt(e)`, não 1 [DERIVED — substituição algébrica]. Este campo não explicita mudança de regime/normalização. O balanço depende de `lambda,mu`; não foi estabelecido aqui um mínimo alpha-livre.'),
('Para provas, resíduos, candidatos numéricos rejeitados e redação literal dos vereditos, consultar `/core/contour_theory/steps`, `/psionic_bond_unification`, `/first_law_link` e `/open_theorem_verdict` relativos ao tópico.',
 'Para a evidência e os checks registrados, resíduos, candidatos numéricos rejeitados e vereditos literais: fonte-base `/core/contour_theory`, filhos `steps`, `psionic_bond_unification`, `first_law_link` e `open_theorem_verdict`; caminho = base + `/` + filho. Estes caminhos identificam a fonte; recuperação operacional por JSON pointer ainda não validada.')]
for before, after in changes:
    assert text.count(before) == 1, before
    text = text.replace(before, after)
updated = text.replace('\n', newline).encode('utf-8')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
backup = path.with_name(path.name + '.bak_' + stamp)
with backup.open('xb') as f:
    f.write(raw)
assert backup.read_bytes() == raw
temp = path.with_name(path.name + '.tmp_' + stamp)
with temp.open('xb') as f:
    f.write(updated)
assert temp.read_bytes() == updated and len(updated) > len(raw)
assert path.read_bytes() == raw
temp.replace(path)
assert path.read_bytes() == updated
print(hashlib.sha256(updated).hexdigest())
