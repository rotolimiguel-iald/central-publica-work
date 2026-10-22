from pathlib import Path
import datetime
import hashlib
import json
import os

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt')
OUT = Path(__file__).resolve().parent
assert OUT == ROOT / 'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910'
sources = [
    OUT / 'TRANSLACAO_NORMAL_E_CURVATURA_BRST.md',
    OUT / 'MANIFESTO_HOMOTOPIA_NORMAL_074.json',
    ROOT / 'EQUIVALENCIA_BV_METRICA_VIELBEIN_070_20260909/EQUIVALENCIA_FORMAL_E_PARES_LORENTZ.md',
    ROOT / 'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
]

def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'mtime_ns': p.stat().st_mtime_ns}

def write_new(name, value):
    path = OUT / name
    assert not path.exists(), str(path)
    data = value.encode('utf-8')
    temp = OUT / (name + '.tmp_new')
    with temp.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes() == data and len(data) > 0
    temp.rename(path)
    assert path.read_bytes() == data
    return pin(path)

before = [pin(p) for p in sources]
note = r'''# Precisão: frame local e alcance métrico da translação074

10/09/2026. [DERIVED — correção de alcance, ao lado da fonte congelada]. A revisão da raiz identificou uma precisão material na alternativa “métrica ou vielbein” da seção2 da [nota074](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md>). A naturalidade comprovada para a inserção que anula o ghost Lorentz não inclui mudanças LOCAIS de frame com o ghost Lorentz convencional. Este adendo restringe expressamente essa leitura; a nota e seu manifesto anteriores permanecem intactos.

## 1. O termo inhomogêneo existe na convenção efetivamente adotada

A [equivalência070, equação5](<C:/IALD/Central de Patentes/Chatgpt/EQUIVALENCIA_BV_METRICA_VIELBEIN_070_20260909/EQUIVALENCIA_FORMAL_E_PARES_LORENTZ.md>) usa

\[
se=\mathcal L_c e+\lambda e,\qquad sA=0.
\]

Sob mudança externa de frame e′=A(x)e, com A Lorentz, a derivada de Lie atua também em A. Comparar s(Ae)=Ase com \(\mathcal L_c(Ae)+\lambda'Ae\) fornece

\[
\boxed{\lambda'=A\lambda A^{-1}
              -(c^\mu\partial_\mu A)A^{-1}.}
\tag{1}
\]

O ghost Lorentz convencional não transforma, portanto, como um tensor adjunto sob uma mudança local externa de frame quando o ghost difeomórfico é mantido explícito. A nota070 não omite esse fenômeno: sua variável que forma par contrátil é \(\upsilon=s\chi\), e não λ sozinho.

Com b_Nc=dx e b_Nλ=0, aplicar b_N a (1) dá

\[
b_N\lambda'=-dA\,A^{-1}.
\tag{2}
\]

Mas definir a mesma receita no frame primado imporia b′_Nλ′=0. Para dA≠0, os resultados diferem. A obstrução é de primeira derivada e não requer curvatura nem uma escolha específica de solução. Para A constante ela desaparece.

Logo a regra da nota074 não é natural sob essa classe de mudanças de frame. A demonstração de naturalidade da exponencial geodésica resolve mudanças de coordenadas de espaço-tempo; ela não elimina o termo misto (1) dos ghosts do produto semidireto difeomorfismos–Lorentz.

## 2. Teorema que permanece válido e suficiente para a apresentação Q2

A apresentação MÉTRICA mínima, com g,φ,c e seus antifields, não contém λ nem frame local independente. Nessa apresentação permanecem válidos a construção natural b_N, os comutadores da seção5, C_N(∇̄c)=−R̄, a conjugação exata s+E_N+C_N, o exemplo FRW e os controles locais/formais declarados. Sua naturalidade é conjunta sob difeomorfismos dos campos e fundos e sob mudanças de apresentação do alvo.

É nessa apresentação ambiente métrica que a [construção Q2_069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>) foi formulada: perturbações h da métrica, ξ do mapa sigma, ghosts difeomórficos e setor não mínimo associado. Não há necessidade de introduzir aqui um ghost Lorentz para aplicar o teorema de translação métrica.

Se a fórmula original é usada com vielbein e λ convencional, seus cálculos de geradores e BCH podem ser lidos numa trivialização de frame fixada, com naturalidade apenas quanto aos difeomorfismos que não acrescentem a transformação local (1), ou sob mudanças constantes de frame. Essa leitura não fornece um operador que cole naturalmente entre frames locais arbitrários.

Consequentemente, onde a nota074 fala em “subcomplexo natural”, sua conclusão deve ser tomada no subcomplexo MÉTRICO especificado acima, salvo uma extensão de frame demonstrada à parte. Nenhuma nulidade de cohomologia, primitiva admissível ou QME foi obtida apenas por essa restrição de apresentação.

## 3. Ghost covariantizado: a modificação exigida, sem herdar BCH

Uma conexão de fundo em frames Lorentz transforma, na convenção de D=d+ω̄, por

\[
\bar\omega'=A\bar\omega A^{-1}-dA\,A^{-1}.
\]

Portanto a combinação

\[
\vartheta=\lambda-\iota_c\bar\omega
\qquad\text{satisfaz}\qquad
\vartheta'=A\vartheta A^{-1}.
\tag{3}
\]

A verificação é direta: os termos \((c\cdot dA)A^{-1}\) de λ′ e \(\iota_c\bar\omega'\) cancelam. Se uma extensão pretende anular o ghost tensorial ϑ e manter b c=dx, deve satisfazer

\[
\boxed{b\vartheta=0\quad\Longrightarrow\quad b\lambda=\bar\omega.}
\tag{4}
\]

(4) transforma exatamente como a conexão; não é a regra b_Nλ=0 da nota congelada. Uma extensão efetiva deve também definir a ação nos jatos covariantes e verificar os comutadores das regras BRST reescritas em ϑ. A simples covariantização (3) não autoriza importar [b,[b,s]]=0 nem o truncamento BCH de074: a segunda inserção agora também alcança o setor Lorentz, incluindo o termo quadrático do ghost. Este adendo estabelece a transformação necessária, mas não reivindica a mesma álgebra de comutadores para esse operador modificado.

## 4. Uso delimitado da comparação070

A comparação070 já construiu, na vizinhança formal da identidade e para esta matéria Lorentz-escalar, a mudança canônica métrica mais pares (χ,υ) e seus antifields. Os pares e seus jatos podem ser contraídos modulo d_H; a naturalidade conjunta dessa contração foi tratada ali. Assim, uma análise feita inicialmente em vielbein pode primeiro usar aquela redução, dentro do seu espaço formal declarado, e só então aplicar o b_N MÉTRICO da seção2 deste adendo.

Isso não identifica, nos ghosts convencionais antes da redução, o operador resultante com a receita antiga b_Nλ=0. Também não transforma a equivalência formal070 numa equivalência global de todos os setores de frames, nem prova que uma primitiva possua os limites analíticos, de escala e contatos exigidos por Q2.

[DERIVED] A correção paga a tipagem: o teorema natural074 é mantido na apresentação métrica efetivamente usada por Q2. Sua extensão direta ao ghost Lorentz convencional sob frames locais estava ampliada indevidamente e fica explicitamente retirada por (1)–(2).

[OPEN] Uma extensão de frame por ghosts covariantizados, com seus jatos e novos comutadores, é outra construção; ela não é necessária para usar o resultado métrico aqui. Permanecem separados os problemas de exatidão cohomológica natural, admissibilidade causal e QME.

O manifesto deste adendo mede quatro fontes antes e depois. Nenhuma fonte anterior foi editada; nenhum um.py foi executado/importado; zero CAS/Lean novos.
'''
np = write_new('PRECISAO_FRAME_LOCAL_074.md', note)
after = [pin(p) for p in sources]
assert before == after, 'Frozen source changed'
manifest = {
    'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Corrects the frame-local scope of the frozen normal ghost translation; metric theorem retained, conventional Lorentz-ghost extension not established',
    'source_pins_before': before, 'source_pins_after': after, 'sources_unchanged': True,
    'outputs': [np], 'writer': pin(Path(__file__)),
    'new_cas': 0, 'new_lean': 0, 'um_executed_or_imported': False,
    'existing_source_modified': False,
    'material_scope_precision': 'b_N lambda=0 is not equivariant under lambda prime=A lambda A inverse-(c dot dA)A inverse for local frames; Q2 uses the metric presentation',
    'not_claimed': ['unchanged BCH for the covariantized Lorentz ghost', 'natural cohomological exactness', 'QME'],
}
mp = write_new('MANIFESTO_PRECISAO_FRAME_074.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'note': np, 'manifest': mp, 'source_count': len(sources), 'sources_unchanged': True}, ensure_ascii=False))
