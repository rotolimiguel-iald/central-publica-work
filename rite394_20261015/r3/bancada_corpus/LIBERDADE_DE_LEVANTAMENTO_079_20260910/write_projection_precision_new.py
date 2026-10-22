from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
OUT = ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910'
REVIEW = ROOT / 'REVISAO_LIBERDADE_LEVANTAMENTO_079_20260910_040031_574533'
SOURCES = [
    OUT / 'CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md',
    OUT / 'MANIFESTO_LIBERDADE_LEVANTAMENTO_079.json',
    REVIEW / 'PARECER_LIBERDADE_E_PROJECAO_SIGMA_079.md',
    REVIEW / 'REGISTRO_REVISAO_LIBERDADE_079.json',
    ROOT / 'COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md',
]
NOTE = r'''# Adendo079: ideal fechado e coeficientes herdados na projeção sigma

10/09/2026. [DERIVED — precisão aditiva de domínio]. Este adendo complementa os §§5 e 7 da [nota079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md>), sem alterar seus bytes. Responde às duas precisões do [parecer independente de selected_geometry_design](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_LIBERDADE_LEVANTAMENTO_079_20260910_040031_574533/PARECER_LIBERDADE_E_PROJECAO_SIGMA_079.md>), lido integralmente, e do [registro correspondente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_LIBERDADE_LEVANTAMENTO_079_20260910_040031_574533/REGISTRO_REVISAO_LIBERDADE_079.json>). O parecer é favorável à dedução079 no alcance anunciado; não é uma decisão sobre o cancelamento ainda aberto.

## 1. Na completação, a projeção age em cada coeficiente

Seja R_her o anel de coeficientes herdado da categoria original e P_E o espaço de polinômios de valência E nos jatos normalizados, com as condições de naturalidade, regularidade e ghost adotadas. Cada elemento de P_E usa somente um número finito de jatos, mas a ordem pode crescer com E. Suprimindo apenas os fatores formais de Rees, a completação pertinente é

\[
\widehat{\mathcal A}=\prod_{E\ge0}P_E.
\tag{A1}
\]

Em cada P_E, defina π_E pela substituição de TODOS os jatos de ξ e ξ* por zero, mantendo os demais geradores e coeficientes. O mapa completo é

\[
\widehat\pi((F_E)_{E\ge0})=(\pi_EF_E)_{E\ge0}.
\tag{A2}
\]

Nenhum coeficiente de saída precisa de uma soma sobre outras valências. Portanto o mapa é contínuo na topologia de produto/valência e preserva os pesos t^(E+2L−2) da [classe Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>). Não se faz uma avaliação em t numérico.

Se Iσ,alg é o ideal diferencial algébrico gerado pelos jatos de ξ e ξ*, denote I_E=ker π_E. Cada monômio de um polinômio de I_E contém pelo menos um desses jatos. Na completação, vale precisamente

\[
\boxed{\ker\widehat\pi=\prod_{E\ge0}I_E
=\overline{I_{\sigma,\mathrm{alg}}}.}
\tag{A3}
\]

A barra é o FECHO por valência. Com efeito, uma série no núcleo tem todos os seus truncamentos finitos no ideal algébrico; esses truncamentos convergem para a série. Reciprocamente, π é contínua e anula o ideal algébrico, logo anula seu fecho. Não se identifica esse conjunto de séries com o ideal formado somente por somas finitas de múltiplos de geradores: o número e a ordem de jatos sigma que aparecem ao longo da série podem crescer sem limite.

## 2. A estabilidade BRST é entendida no mesmo domínio

A prova da nota079 mostra que a transformação de ξ/ξ* e a contribuição sigma às demais equações desaparecem na substituição ξ=ξ*=0, em cada coeficiente. Em cada truncamento C_N, o ideal correspondente é estável e π_N é um mapa de complexos. As projeções π_N são compatíveis com C_(N+1)→C_N.

No complexo completo, use s=s0+t s1+… na organização por valência. Cada coeficiente de sF recebe um número finito de contribuições dos coeficientes de F; os operadores s_j preservam a presença do setor sigma no sentido do ideal correspondente. Assim

\[
s(\overline{I_{\sigma,\mathrm{alg}}})
\subset\overline{I_{\sigma,\mathrm{alg}}},
\qquad
\widehat\pi s=s_{\mathrm{grav},R_{\mathrm{her}}}\widehat\pi.
\tag{A4}
\]

Quando s é uma série formal não polinomial nos campos, não é necessário alegar que ele envie cada expressão polinomial finita a outra expressão polinomial finita. A estabilidade usada em (A4) é a dos truncamentos e do ideal FECHADO. Isso evita uma afirmação algébrica mais forte que a construção realmente fornece.

O quociente adequado é, portanto,

\[
\widehat{\mathcal A}/\overline{I_{\sigma,\mathrm{alg}}}
\simeq\widehat{\mathcal A}_{\mathrm{grav},R_{\mathrm{her}}},
\tag{A5}
\]

onde o lado direito é a álgebra de chegada efetivamente obtida pela projeção, com os mesmos coeficientes permitidos. A afirmação não usa exatidão de limite inverso em cohomologia: é a descrição explícita de um mapa e de seu núcleo nos coeficientes, antes de calcular H(s).

## 3. O alvo gravitacional conserva o anel herdado

A expressão “Einstein puro” na nota original significa que os CAMPOS DINÂMICOS sigma e seus antifields foram retirados pela projeção. Não significa que o anel de coeficientes tenha sido substituído automaticamente por outro menor.

R_her conserva os dados de referência e acoplamentos permitidos na origem, incluindo seus valores ou relações já fixados consistentemente. Isso pode incluir o ponto alvo φ0, tensores do alvo avaliados nele, κ, c, Λ e outros parâmetros admitidos pela classe. Embora a ação projetada não contenha a cinética sigma, isso não autoriza apagar c ou uma dependência admissível de parâmetros nos coeficientes de uma possível correção.

A naturalidade simultânea é mantida tratando os dados de referência remanescentes como parâmetros que transformam conforme a categoria de origem. Fixar seus valores exige fazê-lo de modo compatível com as relações e a naturalidade que se deseja conservar. Exigir invariância adicional, eliminar parâmetros ou passar a um subanel gravitacional menor requer outro argumento.

Em particular, uma primitiva com coeficientes em R_her não foi demonstrada pertencente a um subanel R_menor. Tampouco se demonstrou que um cálculo cohomológico realizado sobre R_menor se estenda ou se reflita automaticamente em R_her. Nenhuma hipótese de mudança plana de base, comparação de cohomologias ou eliminação de espectadores foi acrescentada por esta projeção.

## 4. Leitura precisa da condição necessária e dos limites

Defina K_full e K_grav,Rher como os núcleos da restrição H³(C5)→H³(C3) nos respectivos complexos. A implicação da nota079 passa a ser escrita com o anel visível:

\[
-[A_6]\in\delta(K_{\mathrm{full}})
\quad\Longrightarrow\quad
-[A_6]\in\delta(K_{\mathrm{grav},R_{\mathrm{her}}}).
\tag{A6}
\]

Ela vem da projeção compatível dos truncamentos e dos diferenciais de conexão. Não há uma substituição do alvo por K_grav,Rmenor. A recíproca continua sem prova, pois uma correção gravitacional que usa h* pode recuperar termos sigma quando reinserida na teoria completa.

[DERIVED] As precisões (A2–A6) preservam a redução e delimitam seu domínio correto na completação. As espécies, o sistema local e o controle de corrente079 não mudam.

[OPEN] Não foi decidido se −[A6] pertence a δ(K), nem se existe cancelamento universal ou obstrução de toda a linha cúbica. Não há nova classificação cohomológica, QME ou conclusão física geral neste adendo. O teste de mapa sigma constante não é uma redução do fundo físico não constante φ=id a matéria zero.

[REAL — documental] O recibo deste adendo mede as fontes antes/depois e confronta os pins da nota e do parecer presentes no registro independente. O parecer anterior permanece um artefato separado; não é reescrito nem reinterpretado como aprovação deste novo adendo. Somente arquivos novos079 foram criados, com escrita exclusiva, sem tocar078 ou memórias canônicas e sem executar CAS, Lean ou um.py.
'''


def pin(path):
    data = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def emit(path, data):
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + '.tmp_new')
    with tmp.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if tmp.read_bytes() != data:
        raise RuntimeError('TEMP_BYTE_MISMATCH')
    if path.exists():
        raise FileExistsError(path)
    tmp.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError('FINAL_BYTE_MISMATCH')


before = [pin(path) for path in SOURCES]
review_record = json.loads(SOURCES[3].read_bytes())
if review_record['reviewed_note'] != before[0] or review_record['report'] != before[2]:
    raise RuntimeError('REVIEW_RECORDED_PIN_MISMATCH')
note_path = OUT / 'ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md'
emit(note_path, NOTE.encode('utf-8'))
after = [pin(path) for path in SOURCES]
if before != after:
    raise RuntimeError('SOURCE_CHANGED')
links = re.findall(r'\]\(<(C:/[^>]+)>\)', NOTE)
if not all(Path(p).is_file() for p in links):
    raise RuntimeError('MISSING_LOCAL_LINK')
record = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'kind': 'additive_domain_precision_after_independent_review',
    'author': '/root/prepare_integration_83',
    'status': 'DERIVED_ADDITIVE_PRECISION__ORIGINALS_PRESERVED',
    'precision_completion': 'coefficientwise continuous projection; kernel is closure by valence of the differential sigma ideal',
    'precision_coefficients': 'gravitational target retains inherited coefficient ring or consistent fixed values; no comparison with smaller coefficient category',
    'source_pins_before': before,
    'source_pins_after': after,
    'sources_unchanged': True,
    'recorded_review_pins_match_actual': True,
    'independent_review_status_read': review_record['status'],
    'note': pin(note_path),
    'creator': pin(Path(__file__).resolve()),
    'local_links': [{'path': p, 'exists': True} for p in links],
    'executions': {'CAS': 0, 'Lean': 0, 'um_py_execution_or_import': 0},
    'existing_files_modified': False,
    'files_078_modified': False,
    'canonical_memories_modified': False,
    'not_claimed': ['membership decision for -[A6] in delta(K)', 'universal cancellation or obstruction', 'QME', 'independent review of this new adendum already received'],
}
record_path = OUT / 'REGISTRO_ADENDO_IDEAL_FECHADO_079.json'
emit(record_path, (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': pin(note_path), 'record': pin(record_path),
                  'source_count': len(before), 'sources_unchanged': True,
                  'local_links_existing': len(links)}, ensure_ascii=False))
