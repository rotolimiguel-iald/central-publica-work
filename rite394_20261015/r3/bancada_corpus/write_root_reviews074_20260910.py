from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REVISOES_RAIZ_074_20260910'
SOURCES = [
    'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md',
    'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md',
    'NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md',
    'NATURALIDADE_E_CURVATURA_B0_074_20260910/PRECISAO_METRICA_E_FRAME_DE_REFERENCIA.md',
    'REVISAO_COMPLETACAO_REES_074_20260910_015708_288616/PARECER_COMPLETACAO_REES_074.md'
]


def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def new(name, content):
    path = OUT / name
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    raw = content.encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert raw and temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)


before = [pin(ROOT / relative) for relative in SOURCES]
assert not OUT.exists()
OUT.mkdir()
normal = r'''# Parecer da raiz — translação normal074 e correção de frame

10/09/2026. [DERIVED — revisão matemática escrita, delimitada]. Li integralmente a nota TRANSLACAO_NORMAL_E_CURVATURA_BRST e seu adendo PRECISAO_FRAME_LOCAL_074, pinados no recibo. Conferi a entrada de jatos normais em Jentsch, Teoremas1–3, no PDF primário https://arxiv.org/pdf/1509.08269v1. Não se trata de compilação Lean nem de uma auditoria de todas as entradas anteriores da teoria.

**Conclusão: favorável para a apresentação métrica mínima após a correção explícita de alcance.** A referência B0 é inerte por s; a naturalidade considerada transporta conjuntamente campos e referência. A leitura antes ampliada aos ghosts Lorentz convencionais sob frames locais foi retirada no adendo e não é aceita neste parecer.

## Cálculo revisto

A inserção pelo pushforward dos campos constantes do espaço tangente via Exp_x usa um centro a cada ponto. Sua naturalidade segue da equivariância da exponencial. Ela é diferente de transporte paralelo radial e de uma derivação evolutiva que prolongasse c→dx com todos os jatos derivados nulos. Essa diferença aparece nos segundos jatos covariantes e quando a derivada horizontal move o centro.

Com [∇̄_μ,∇̄_ν]v^ρ=R̄^ρ_{σμν}v^σ, os coeficientes −1/3 da derivada normal de Γ e −1/6 da parte simetrizada dão a ação escrita sobre ∇̄²c. O defeito C_N=d_Hb_N−b_Nd_H sobre Z=∇̄c é −R̄: b_NZ=0 em todo ponto, mas b_Nd_HZ contém a antissimetrização da derivada da conexão. A curvatura não desaparece com Γ(x)=0.

O segundo comutador com s anula-se porque duas inserções no termo quadrático sc são o colchete dos campos constantes empurrados pela MESMA carta normal do centro escolhido. Esses campos comutam com todos os seus jatos. As outras regras métricas mínimas têm no máximo um ghost difeomórfico. Os coeficientes da inserção são s-inertes.

C_N e b_N só inserem ghosts, e aniquilam os coeficientes de fundo um do outro; daí [b_N,C_N]=0 e C_N²=0. O BCH é finito e fornece s+E_N+C_N. Separar os bidegraus da quadratura confirma {s,E_N}=0, E_N²=−{s,C_N} e {E_N,C_N}=0. Portanto não se pode usar E_N como diferencial na álgebra antes de passar à cohomologia de s.

No fundo g0=dr²−a²γ, a=2cos(r/2), as conexões escritas dão R̄^r_{irj}=aa''γij=−a²γij/4. Assim C_N(∇̄_i c^r)=a²γij dr∧dy^j/4 é não nulo no interior. Isso é um controle escrito do termo que a conjugação tem de conservar, não um coeficiente de anomalia física.

A recorrência sT_q+E_NT_(q−1)+C_NT_(q−2)=Ω_q é consistente: depois de resolver as etapas anteriores, a obstrução U_q é s-fechada pelas relações acima. A existência de sua primitiva natural continua um antecedente. A filtração finita não transforma esse antecedente em conclusão.

## Correção material identificada nesta revisão

Na convenção se=L_c e+λe, a mudança e'=A(x)e com sA=0 força λ'=AλA⁻¹−(c·∂A)A⁻¹. Logo b_Nλ=0 implica b_Nλ'=−dA A⁻¹ e não satisfaz a mesma receita no frame primado. Solicitei que essa ampliação fosse retirada por adendo; o autor o fez sem alterar a nota congelada.

A apresentação métrica efetiva de Q2 não contém esse ghost adicional e conserva o teorema. A combinação tensorial ϑ=λ−ι_cω̄ exigiria bλ=ω̄ para que bϑ=0; isso é outro operador. Seus comutadores não foram aceitos por analogia. A comparação formal métrica–vielbein anterior pode fornecer uma rota separada, com suas próprias hipóteses.

## Limites

A parte de completação da nota é compatível com o teorema Rees e seu parecer independente, lido nesta revisão: preservar R_L não é preservar uma truncagem t≤N sem margem. A construção geométrica conserva jatos finitos e regularidade de suas entradas. Isso não paga os grupos naturais de cohomologia, a descida, os contratermos por aridade, os contatos, a carga interagente ou QME.

Parecer aceito somente junto com o adendo de frame. Fontes preservadas; os controles automáticos do recibo medem integridade, não substituem esta análise.
'''
natural = r'''# Parecer da raiz — normalização para s e obstrução de Euler074

10/09/2026. [DERIVED — revisão matemática escrita e delimitada]. Li integralmente NORMALIZACAO_S_E_OBSTRUCAO_EULER e PRECISAO_METRICA_E_FRAME_DE_REFERENCIA. Conferi a transgressão no artigo primário Chern–Simons, §3, e a separação por tipos no Apêndice C de BBH1995. As fontes locais estão pinadas no recibo.

**Conclusão: favorável nos escopos e com os antecedentes expressos na nota.** Não se demonstrou uma anomalia de ghost um nem a nulidade da cohomologia relativa natural em grau cinco.

## Transporte para s

Normalizar os jatos pela referência B0 comuta com s porque a transformação depende só de B0 e sB0=0. A avaliação da coordenada na origem também comuta com s, que não move x. Isso não afirma a mesma propriedade para d_H, que deriva o centro e os jatos de referência.

Depois da normalização, cada coeficiente formal polinomial tensorial possui um número finito de tipos de Lorentz. Coeficientes C∞ nos valores escalares do alvo não participam dessa ação. A projeção no tipo trivial é legítima nesse módulo semissimples e é natural quanto aos mapas equivariantes. Assim transporta α=sβ natural para α=sR_Nβ quando β já existe na mesma completação. A nota não aplica a projeção a uma função C∞ arbitrária da flutuação métrica antes de formalizá-la.

O adendo distingue corretamente o frame ortonormal da referência num ponto da mudança de gauge de um vielbein dinâmico. O enunciado aceito é o métrico mínimo, sem o ghost Lorentz cru. Isso resolve a mesma ambiguidade encontrada na nota da translação normal.

## Contraexemplo de Euler

A forma E(g0)=(Riem²−4Ric²+R²)dV admite uma Chern–Simons coordenada local. Se fosse sb⁻¹₄+d_Hb⁰₃ com primitivas naturais universais regulares na classe declarada, poderia ser avaliada em g=g0 de curvatura constante, Ric=Λg0, mapas sigma constantes e ghosts/antifields nulos.

Nesse jato de solução o vetor BRST é zero, inclusive nas componentes KT e em suas derivadas. A 3-forma restante teria de ser invariante pela isotropia Lorentz em cada ponto. Seu dual seria um vetor invariante: rotações eliminam a parte espacial e um boost elimina a temporal. Logo a 3-forma é identicamente zero nesse fundo.

Entretanto Riem²=24K², Ric²=36K² e R²=144K², com K=Λ/3, dão E(g0)=24K²dV≠0. O argumento é local Lorentziano, não depende de integrar uma variedade compacta nem de ressomar a expansão formal. A avaliação h=0 basta. A conclusão exige a classe universal que contém esses fundos e mapas constantes; uma categoria com inversos singulares de dφ não está coberta.

Assim há falha de injetividade no grau (ghost0,forma4) da inclusão natural→coordenada. Isso impede uma covariantização genérica que comute também com d_H. Não contradiz a exatidão ordinária073 de grau de anomalia, nem demonstra que a quebra efetiva de Q2 possua coeficiente não nulo.

## Transgressão e critério de grau cinco

Na vizinhança formal g=g0+h, S=(g0⁻¹g)^(1/2) é autoadjunto para g0 e identifica os dois fibrados métricos. Transportar ∇g por S fornece duas conexões métricas no mesmo fibrado. Sua diferença θ é tensorial. A identidade ∂_uP(R_u,R_u)=2dP(θ,R_u), obtida por invariância e Bianchi, integra-se à transgressão natural de E(g)−E(g0). O parâmetro u dessa integral é auxiliar; não é o t formal de Q2. Em cada grau de h a fórmula tem ordem finita e não remove E(g0) sozinho.

O critério espectral também é correto como proposição condicional. Após a conjugação natural, a diagonal total cinco tem três entradas elimináveis por H¹(s), H²(s), H⁵(s) e duas entradas E₂ com coeficientes H⁴(s), H³(s). Se todas forem nulas na mesma classe, páginas posteriores não as recriam. As nulidades e a descida natural não foram provadas por esse critério. O resultado Euler está em total quatro e não ocupa automaticamente uma dessas entradas de total cinco.

## Efeito sobre a continuação

O resultado positivo fornece um transporte de primitivas de s já existentes na classe correta. O resultado negativo obriga a calcular a parte horizontal com curvatura e coeficientes dinâmicos. A completação, a regularidade, a descida e a hierarquia causal mantêm seus próprios contratos. O alcance aceito não é uma QME nem uma prova de gravidade quântica.

Fontes web primárias verificadas: https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf e https://arxiv.org/pdf/hep-th/9505173v2. Nenhum original, fonte congelada ou gate foi alterado.
'''
outputs = [new('PARECER_TRANSLACAO_NORMAL_E_FRAME_074.md', normal),
           new('PARECER_NORMALIZACAO_E_EULER_074.md', natural)]
assert before == [pin(ROOT / relative) for relative in SOURCES]
record = {
    'status': 'PASS_LIMITED_WRITTEN_REVIEW__METRIC_SCOPE_WITH_FRAME_CORRECTIONS',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'inputs': before,
    'outputs': outputs,
    'source_bytes_unchanged': True,
    'new_cas_controls': 0,
    'new_lean_compilations': 0,
    'scope': 'Written review of the stated operator, naturalization and curvature results; not all-order anomaly removal, interacting QME or UV.'
}
receipt = new('REGISTRO_REVISOES_RAIZ_074.json', json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'outputs': outputs, 'receipt': receipt}, ensure_ascii=True))
