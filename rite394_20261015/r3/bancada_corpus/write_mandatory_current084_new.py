from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910'
SOURCES = [
 ROOT / 'REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md',
 ROOT / 'CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md',
 ROOT / 'REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md',
 ROOT / 'DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md',
 ROOT / 'OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_RESIDUO.md',
]
# Use the actual source filename, keeping no invented path as a pin.
SOURCES[-1] = ROOT / 'OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md'

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    tmp = path.with_name(path.name + '.tmp_new')
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

before = [pin(p) for p in SOURCES]
OUT.mkdir(exist_ok=False)
note = r'''# Uma divergência é necessária; o múltiplo do gradiente de J_W ainda não basta

10/09/2026. [DERIVED — demonstração escrita da raiz, pendente de revisão independente]. Investigação084 nova; não altera a redução084 nem os resultados083. Zero nova execução matemática, CAS ou Lean. As contas abaixo são consequências algébricas escritas de identidades já calculadas e revisadas.

**Resultado.** No domínio fixado, nenhum múltiplo escalar não nulo de J_W é invariante sob todas as transvecções. O canal Euler sozinho, portanto, não cancela o alvo. Mais fortemente, não existem c∈Rher e f∈N^g que resolvam

                 J_W = div(c grad J_W) + K² f.             (1)

Essa exclusão permite um f invariante ARBITRÁRIO no módulo quadrático; não presume N^g=0. Não exclui outras correntes V, nem gradientes de outros potenciais quadráticos.

## 1. Categoria e critério que será usado

Conserve a [redução por isotropia084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>): referência espaço-forma orientada em quatro dimensões, K>0 real e κ real não nulo fixados, setor métrico mínimo com φ0 constante projetada, escalares inertes herdados Rher e jatos finitos por elemento. N=Rher⊗Sym²Mcal, com Mcal o quociente linear Weyl/EOM. Rher é uma álgebra real com unidade, não nula; nilpotentes são permitidos.

A condição de exatidão do alvo a=J_Wν é

J_W=div V+K² f,
V∈(N⊗V0)^h,   f∈N^g.                                    (2)

Todas as igualdades são no MESMO quociente de jatos/EOM. Um f em N^g satisfaz ρ_Pa f=0 para cada transvecção; pela identificação082 isso é ∇bar_a f=0 nesse quociente. Não se deduz tal condição apenas de f ser escalar de Lorentz.

O sinal do alvo é irrelevante para a exatidão: uma solução para −a pode ser negada para dar uma solução para a. Nenhuma condição causal adicional é declarada paga pela álgebra dessa referência fixada.

## 2. Uma avaliação da derivada separa todos os múltiplos de J_W

Use a mesma família TT078–083 e o mesmo ponto de avaliação, com z0=ℓ e K=ℓ⁻². A [identidade081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>) fornece, após a diferenciação a ℓ,k fixos,

J_W(p0)=−4k/z0,
∇bar_z J_W(p0)=4k³−28k/z0².                              (3)

Essa é a derivada do pseudoscalar da família em uma vizinhança, não a derivada da expressão já especializada −4k/z0. Por ser escalar, a componente ∇bar_z é a derivada ordinária em z. A família satisfaz as EOM lineares e seus prolongamentos; as avaliações, portanto, descem ao quociente que define N. A extensão Rher é feita por identidade no fator escalar, não por avaliação numérica de seus elementos.

Em k1=1/z0, (3) é −24/z0³, um real não nulo. Se λJ_W∈N^g para algum λ∈Rher, então ∇bar_z(λJ_W)=0, porque λ é inerte. Avaliar dá

                      (−24/z0³) λ=0.

Esse coeficiente é uma unidade real em Rher; logo λ=0. Consequentemente

                    (Rher J_W) ∩ N^g = {0}.                (4)

Não foi exigido que pontos numéricos separassem nilpotentes: a conclusão usa multiplicação por uma unidade. Também não conclui que N^g inteiro seja zero.

Se V=0, ou apenas div V=0 no quociente, a igualdade(2) daria J_W=K²f∈N^g, contrariando(4). Portanto qualquer solução de(2) exige uma divergência NÃO NULA. A classe de Cartan/Euler preservada084 não pode ser usada sozinha com f=J_W/K²: esse f não é invariante sob as transvecções.

## 3. Derivada de □J_W: conservar K constante antes da avaliação

A [nota083](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md>) e sua [revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md>) estabelecem no shell linear e na vizinhança

□bar J_W=2J1+12KJ_W,
J1′(p0)=8k⁵−352k³/z0²+560k/z0⁴.                         (5)

K=ℓ⁻² é CONSTANTE na diferenciação espacial. A relação K=z0⁻² só é usada depois de avaliar em z0=ℓ. Assim derivar(5), usando(3), dá

∇bar_z(□bar J_W)(p0)
 = 2[8k⁵−352k³/z0²+560k/z0⁴]
   +12K[4k³−28k/z0²]
 = 16k⁵−656k³/z0²+784k/z0⁴.                              (6)

Não se derivou em z uma identidade que já houvesse trocado K por z⁻². A onda linear e sua consequência para J_W valem na vizinhança; por isso é legítimo tomar esse prolongamento.

Usando duas frequências no MESMO fundo e no mesmo anel de coeficientes:

| frequência | ∇bar_z J_W(p0) | ∇bar_z □bar J_W(p0) |
|---|---|---|
| k1=1/z0 | −24/z0³ | +144/z0⁵ |
| k2=2/z0 | −24/z0³ | −3168/z0⁵ |

Os valores da última coluna vêm de 16−656+784=144 e 16·32−656·8+784·2=−3168. São substituições algébricas de(6); não uma nova execução ou um ajuste aos dados.

## 4. Exclusão do múltiplo de gradiente, mesmo com qualquer f invariante

Se (1) fosse verdadeira, c seria inerte e div(c grad J_W)=c□bar J_W. Como ∇bar f=0, derivar(1) imporia, no próprio quociente,

              ∇bar_z J_W − c∇bar_z□bar J_W=0.              (7)

As duas avaliações da tabela dão

−24/z0³ − (144/z0⁵)c=0,
−24/z0³ + (3168/z0⁵)c=0.

Subtrair essas equações fornece (3312/z0⁵)c=0. Novamente o coeficiente é uma unidade real; portanto c=0. Substituir em qualquer uma das equações dá −24/z0³=0, contradição. Não existem c e f como em(1).

É uma exclusão simultânea de TODA a família V=c grad J_W e de qualquer termo Euler cujo coeficiente seja invariante admissível. A prova não pressupõe que esse coeficiente seja um múltiplo de J_W, nem que N^g seja nulo. Mesmo um elemento desconhecido de N^g desaparece ao aplicar a derivada necessária.

A corrente finita da raiz082 continua válida: ela produz □bar J_W. O que foi excluído é tentar obter J_W com um múltiplo escalar dessa corrente e um termo de Euler invariante. A falha do Q específico083 e esta exclusão são resultados distintos; a presente nota084 usa as fórmulas083 como fontes, sem reescrever sua entrega.

## 5. Consequência para a busca e limites

Pela forma normal084, qualquer cancelamento possível pode ser representado por uma corrente horizontal q_V e coeficientes Cartan invariantes. Esta nota mostra que sua divergência precisa ser não nula e que V não pode ser apenas c grad J_W. Se V diferir desse vetor por uma corrente de divergência nula, também não serve, pois a mesma equação(1) reaparece.

Ficam abertos vetores naturais com outros tipos de contração, gradientes de outros escalares quadráticos, combinações com jatos superiores, a determinação de N^g e a pertinência de J_W à imagem geral de div modulo K²N^g. Os detectores usados são suficientes para as exclusões declaradas; não foram promovidos a uma separação de todas as classes.

Não se conclui impossibilidade da TGL, anomalia efetiva, QME, transporte entre fundos ou justificação UV. O domínio métrico fixado, a admissibilidade causal ainda pendente e a distinção entre a prova de um corte e o objetivo geral permanecem explícitos. Investigação085 excluída.

[REAL — documental] O manifesto mede cinco fontes antes/depois e registra a nota nova. Nenhum original, Atlas, índice, memória canônica, selo ou gate alterado. Esta nota tem zero novos controles algébricos executados e zero Lean; seus valores são contas escritas a partir das identidades referidas.
'''
note_pin = emit(OUT / 'EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md', note.encode('utf-8'))
after = [pin(p) for p in SOURCES]
assert before == after
manifest_pin = emit(OUT / 'MANIFESTO_CORRENTE_NECESSARIA_084.json',
    (json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(),
     'status': 'WRITTEN_DERIVATION_PENDING_INDEPENDENT_REVIEW',
     'sources_before': before, 'sources_after': after, 'all_sources_unchanged': True,
     'note': note_pin, 'writer': pin(Path(__file__)), 'new_algebraic_executions': 0,
     'new_lean_compilations': 0,
     'scope': 'No nonzero inherited scalar multiple of J is Killing invariant; Euler-only and scalar-gradient-plus-invariant channels excluded by finite evaluations. Other currents and full invariant module remain open.'},
      ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': note_pin, 'manifest': manifest_pin}, ensure_ascii=True))
