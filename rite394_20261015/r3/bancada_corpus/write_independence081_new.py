from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'INDEPENDENCIA_RESIDUO_E_IMAGEM_081_20260910'
OUT.mkdir(exist_ok=False)
sources = [
 ROOT / 'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md',
 ROOT / 'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json',
 ROOT / 'FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md',
 ROOT / 'TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md']

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temporary = path.with_name(path.name + '.tmp_new')
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == raw
    temporary.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

before = [pin(path) for path in sources]
note = r'''# Duas avaliações separam o resíduo da direção quadrática encontrada

10/09/2026, etapa081. [DERIVED — consequência algébrica escrita das fórmulas078–081]. Zero nova execução aritmética, CAS ou Lean; nenhum um.py ou original alterado/executado/importado.

**Resultado.** Na referência fixada das notas080–081, as classes

\[
a=[A_6],\qquad b=[s_1b_5],\qquad b_5=\kappa J\beta
\]

são linearmente independentes sobre Rher e geram um submódulo livre cindido de posto dois em H⁴(A6,s0), para Rher não nulo. A classe b pertence a δ(Kcal), mas a NÃO pertence à linha Rher b. Isso não decide se a pertence à imagem de outras classes de Kcal.

## 1. Domínio preservado

Trabalhamos no complexo métrico mínimo natural orientado, em dimensão quatro, com a referência espaço-forma K>0 FIXADA, φ0 constante e κ real não nulo fixado, conforme a [transferência080](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>). Rher é a mesma álgebra real unital de escalares inertes; não se introduz um anel universal de K variável ou tensores espectadores.

Os perfis h_k e h_−k, com seus quatro Killing, definem o [funcional ímpar079](<C:/IALD/Central de Patentes/Chatgpt/FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md>). Cada Lk anula fronteiras de s0 de todos os jatos finitos, incluindo antifields, e por isso define uma aplicação Rher-linear

\[
\ell_k:H^4(\mathcal A_6,s_0)\longrightarrow R_{\rm her}.
\]

Fixamos z0=ℓ>0. Alterar k muda somente a solução de teste; o fundo, a orientação, os dados iniciais f(z0)=0, f'(z0)=1 e os coeficientes da classe permanecem os mesmos. As soluções existem para todos os k reais não nulos usados abaixo. Essas avaliações são aplicações externas de teste sobre classes, não novos observáveis físicos declarados nem coeficientes dinâmicos acrescentados ao modelo.

## 2. Matriz explícita de avaliações

O certificado078–079 e a [construção081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>) fornecem, respectivamente,

\[
\ell_k(a)=-\frac{4k}{z_0},\qquad
\ell_k(b)=\kappa\left(\frac{24k^3}{z_0}-\frac{96k}{z_0^3}\right).
\tag{1}
\]

Não se reexecuta aqui o recibo que controla a segunda fórmula. Escolha duas frequências permitidas,

\[
k_1=z_0^{-1},\qquad k_2=2z_0^{-1},
\quad \ell_1:=\ell_{k_1},\quad\ell_2:=\ell_{k_2}.
\]

Substituindo em (1),

\[
\begin{pmatrix}\ell_1(a)&\ell_1(b)\\
\ell_2(a)&\ell_2(b)\end{pmatrix}
=
\begin{pmatrix}
-4/z_0^2&-72\kappa/z_0^4\\
-8/z_0^2&0
\end{pmatrix}=:M.
\tag{2}
\]

O segundo zero é a identidade 24·2³−96·2=0; o primeiro valor de b é 24−96=−72. O determinante é

\[
\det M=-576\kappa/z_0^6.
\tag{3}
\]

Como κ e z0 são números reais não nulos fixados, esse determinante é uma unidade em Rher. O argumento não depende de avaliações numéricas que supostamente separassem nilpotentes do anel.

## 3. Independência e retração explícita

Se λa+μb=0, aplicar ℓ2 dá −8λ/z0²=0, logo λ=0. Aplicar ℓ1 em seguida dá −72κμ/z0⁴=0, logo μ=0. Isso prova a independência sobre o próprio Rher.

Mais explicitamente, para qualquer classe x∈H⁴(A6,s0), defina

\[
r(x)=\left(
-\frac{z_0^2}{8}\ell_2(x),\;
\frac{z_0^4}{72\kappa}\left(\frac{\ell_2(x)}2-\ell_1(x)\right)
\right).
\tag{4}
\]

Se i:Rher²→H⁴(A6,s0) envia (λ,μ) a λa+μb, (2) dá

\[
r\circ i=\operatorname{id}_{R_{\rm her}^2}.
\tag{5}
\]

Logo i é injetiva e

\[
H^4(\mathcal A_6,s_0)\simeq i(R_{\rm her}^2)\oplus\ker r
\tag{6}
\]

como módulos, sem afirmar que o complemento seja livre, finito ou conhecido. Sobre Rher=R isso fornece a cota de dimensão pelo menos dois. A divisão por κ em (4) usa a referência fixada e define uma aplicação de teste; não foi inserida numa primitiva causal ou num novo contratermo sujeito a outras regras de admissibilidade.

## 4. Consequência para o próximo candidato

A construção081 prova b∈δ(Kcal) e b≠0. A independência acima reforça o limite dessa descoberta:

\[
a\notin R_{\rm her}b,\qquad -a\notin R_{\rm her}b.
\tag{7}
\]

Assim nenhum múltiplo escalar herdado do candidato κJβ cancela A6, nem após acrescentar fronteiras de s0. Sua imagem pode ser não nula sem ter a direção de classe exigida pelo resíduo.

Qualquer solução geral z5 precisa satisfazer, ao menos,

\[
\ell_2(d_1[z_5])=+8/z_0^2.
\tag{8}
\]

O candidato exibido não fornece essa parcela, pois ℓ2(b)=0. Não se demonstrou que ℓ2 anule d1 de TODOS os quadráticos de Weyl. Portanto (8) é um filtro para a próxima busca, e não um certificado de obstrução universal. Os outros candidatos, inclusive os com derivadas de Weyl, continuam permitidos no domínio declarado.

## 5. Estatutos e limites

[DERIVED] Duas classes independentes, retração explícita e exclusão da linha gerada por b para o cancelamento de A6. As fórmulas usadas são consequências das demonstrações anteriores, com todas as hipóteses mantidas.

[OPEN] A imagem inteira de d1E5, a pertença de −a a essa imagem, relações e geradores completos do módulo quadrático, prolongamentos superiores, anomalia/QME, admissibilidade causal, UV e reconstrução gravitacional geral. A existência do somando Rher² não é interpretação física adicional.

[REAL — documental] Fontes medidas antes/depois e preservadas. A nota não conta as substituições em (2) como nova execução do script081 nem como novos controles Lean. Investigação082 permanece separada e não é utilizada para ampliar (7) a outros candidatos.
'''
note_pin = emit(OUT / 'DUAS_AVALIACOES_E_SUBMODULO_LIVRE_E6.md', note.encode('utf-8'))
after = [pin(path) for path in sources]
assert before == after
manifest = {'created_utc': datetime.now(timezone.utc).isoformat(),
 'status': 'WRITTEN_TWO_EVALUATION_ARGUMENT_AWAITING_INDEPENDENT_REVIEW',
 'sources_before': before, 'sources_after': after, 'all_sources_unchanged': True,
 'note': note_pin, 'writer': pin(Path(__file__)), 'new_arithmetic_executions': 0,
 'new_lean_compilations': 0, 'um_executed_or_imported': False, 'originals_written': False,
 'scope': 'Split independence of [A6] and the constructed d1 image; no classification of the full d1 image.'}
manifest_pin = emit(OUT / 'MANIFESTO_INDEPENDENCIA_081.json',
 (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': note_pin, 'manifest': manifest_pin}, ensure_ascii=True))
