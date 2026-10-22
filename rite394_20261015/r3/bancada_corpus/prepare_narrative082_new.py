from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_082_20260910'
CE_REVIEW_DIR = (ROOT / sys.argv[1]).resolve()
CURRENT_REVIEW_DIR = (ROOT / sys.argv[2]).resolve()
assert all(p.is_relative_to(ROOT) and p.is_dir() for p in [CE_REVIEW_DIR, CURRENT_REVIEW_DIR])
def report_in(directory):
    found = list(directory.glob('PARECER*.md'))
    assert len(found) == 1
    return found[0]
CE_REVIEW = report_in(CE_REVIEW_DIR)
CURRENT_REVIEW = report_in(CURRENT_REVIEW_DIR)
FINITE = ROOT / 'SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779'
CE = ROOT / 'COMPLEXO_CE_QUADRATICO_082_20260910'
CURRENT = ROOT / 'OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910'
FINITE_REVIEW = ROOT / 'REVISAO_SETOR_FINITO_082_20260910_052417_739397/PARECER_SETOR_FINITO_SEM_DERIVADAS_082.md'

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def emit(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)
def md(path, text):
    return emit(path, text.encode('utf-8'))
def subst(text):
    return text.replace('__CE_REVIEW__', CE_REVIEW.as_posix()).replace('__CURRENT_REVIEW__', CURRENT_REVIEW.as_posix())

sources = [FINITE / 'IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md',
           FINITE / 'compute_zero_derivative_sector082.py',
           FINITE / 'CONTROLES_SETOR_SEM_DERIVADAS_082.json',
           FINITE_REVIEW, CE / 'IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md',
           CE_REVIEW, CURRENT / 'CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md',
           CURRENT_REVIEW]
before = [pin(p) for p in sources]
review_out = ROOT / 'REVISOES_RAIZ_082_20260910'
review_out.mkdir(exist_ok=False)
root_review = subst(r'''# Revisão da raiz082 — setor finito e diferencial CE

10/09/2026. [DERIVED — revisão matemática escrita] [REAL — leitura e integridade das fontes]. A raiz leu integralmente as notas do setor finito e da identificação CE, o script e o recibo finitos, e os pareceres independentes indicados abaixo. Não detectou erro material no alcance declarado. Esta revisão não substitui execução matemática ou compilação Lean; não houve rerun.

No setor sem derivadas, conferi Sym²[(4,0)+(0,4)] e o emparelhamento com Λ³G: dois escalares vezes quatro cúbicas, mais dois tipos Weyl, total dez contrações. O resultado usa esse espaço representacional, não uma dimensão de H³(s0)E5. Os dois produtos de tipo Weyl admitem tensores quadráticos S e seu dual. T_abcd C^a C^b m^cd se anula por T_[abc]d=0 na substituição m=n∧C/z0 para todo h; prolongar a ação em h e usar o fechamento da subálgebra dos quatro Killing paga também a variação. A nulidade não foi inferida apenas de uma solução TT particular.

Conferi os sinais Mfin=g0⁻¹m=−antisym(∇C), βo=−6θ012/z0, γo=+6θ012/z0³ e dθ(θ012)=3θ0123/z0. Para X=I ou J_W, s1X+s0X3=C·∂X é mantido antes da avaliação. A resposta bT(3X/z0−∂zX) vem da reordenação θ3θ012=−θ0123. I e sua derivada são pares em k; as únicas respostas ímpares são R(k) e −K R(k), com R=24k³/z0−96k/z0³. O fator conforme é derivado antes de impor ℓ=z0. Em k=2/z0 todos os dez candidatos dão zero, mas o alvo exige +8/z0². Isto exclui o setor inteiro, preservando a possibilidade de candidatos com derivadas.

O script foi lido estaticamente: Fraction, somas Laurent e produto exterior com índices repetidos nulos; especialização posterior à derivada; oito produtos escalares; dez Weyl construídos de E/B simétricos sem traço. O controle dghost de uma contração já nula não é vendido como prova independente da variação em todo h. O recibo tem dezoito controles algébricos e um de preservação das quatro fontes. A derivação geométrica e a completude tensorial são argumentos escritos. O parecer externo confere a cópia AST e os pins; a raiz não reexecutou essas funções.

Na identificação CE, a diagonal E=q+2 permite dois fatores de ghost0 ou um de ghost−1; H⁻¹(L)=0 elimina o segundo padrão, deixando Sym²Mcal⊗ΛqG. A mesma raiz métrica S e o ghost transportado dão s1p+s0p2=−Mghost p e s1Mghost+s0k2=−Mghost²+Kpp♭. O completion tensorial de cada (∇g)^rWg dá s1W_r=p∇W_r+𝔯(Mghost)W_r−s0(T_r,2−𝔯(H/2)W_r), com todos os índices de derivadas presentes.

Refiz o dicionário dos sinais: X↦v_X=Xq é anti-homomorfismo; δ_v h=Lie_v h com coeficientes de v inertes é também anti. Portanto ρ_X=δ_vX é representação, e o ghost matricial obedece dθ=−[θ,θ]/2. A ação preserva gauge, Hessiano e adjuntos por naturalidade sob isometrias de g0, logo desce às relações de Mcal. O comutador das transvecções é −K𝔯(Jab) também nos índices que marcam derivadas. Não se aplica uma derivada plana a um jato tensorial curvo.

A fonte de Khavkine foi conferida novamente na seção3, equações22–25 e seção3.1: a conexão de transporte de Killing é plana em curvatura constante. Esse é o único papel atribuído à fonte externa aqui; ela não prova a identificação CE quadrática deste projeto. [Fonte primária](https://arxiv.org/pdf/1805.03751).

O resultado é o CE INVARIANTE pela isotropia, não o relativo: Mghost ainda pode entrar nos cochains. Finitude de jatos por elemento não dá local finitude para toda g nem permite Whitehead. O módulo Mcal continua quociente, sem liberdade ou dimensão finita assumidas. A raiz aceita a identificação do operador, sem calcular sua cohomologia por esse ato.

Pareceres externos lidos: [setor finito](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SETOR_FINITO_082_20260910_052417_739397/PARECER_SETOR_FINITO_SEM_DERIVADAS_082.md>), [CE](<__CE_REVIEW__>). A nota da própria raiz sobre o cociclo alvo e a corrente gradiente tem [revisão independente própria](<__CURRENT_REVIEW__>); esta revisão não é contada como aprovação independente dessa construção.

As três notas, juntas, localizam a obrigação em [J_Wν]_CE. A corrente gradiente produz □bar J_W, e nenhuma igualdade desse resultado com o alvo foi pressuposta. Investigação083 excluída. Zero Lean ou um.py executado/importado, nenhuma escrita fora de Chatgpt ou mudança de gate.
''')
review_pin = md(review_out / 'PARECER_SETOR_FINITO_E_CE_082.md', root_review)
after = [pin(p) for p in sources]
assert before == after
receipt_pin = emit(review_out / 'REGISTRO_RAIZ_SETOR_FINITO_E_CE_082.json',
    (json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(),
      'status': 'ROOT_READ_AND_REVIEW_ACCEPTED_WITH_STATED_SCOPE',
      'sources_before': before, 'sources_after': after, 'all_sources_unchanged': True,
      'report': review_pin, 'new_algebraic_executions': 0, 'new_lean_compilations': 0,
      'scope': 'Written root review of finite sector and CE operator; own current proof approved by the separate external review linked.'}, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

report = subst(r'''# Suficiência082 — exclusão do setor sem derivadas e identificação do próximo diferencial

10/09/2026. [DERIVED — demonstrações escritas revisadas] [REAL — controles algébricos e custódia documental].

**Todos os dez candidatos quadráticos sem derivadas de Weyl foram excluídos como solução do cancelamento.** Para investigar os candidatos com derivadas, identificamos o diferencial completo com o de Chevalley–Eilenberg, atuando nos jatos de Weyl com suas relações. O alvo é um cociclo nesse complexo. Uma corrente gradiente fornece uma imagem explícita, mas a nulidade da classe alvo continua aberta.

## 1. Estado canônico e domínio conservado

A [captura082](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_082_20260910/ESTADO_CANONICO_082.json>) confirma os mesmos quatro arquivos canônicos da081: v338, 683 arquivos embutidos e 77 dos 98 módulos acompanhados presentes; 21 permanecem ausentes. O selo corresponde aos bytes de um.py. Foi leitura por bytes e AST, sem executar/importar o programa ou repetir sua rodada. A parede UV continua aberta na própria fonte. H3 interno, fase/ramo e falsificadores já reconhecidos permanecem preservados.

As provas usam o complexo métrico mínimo de zeroformas naturais orientadas, referência espaço-forma fixa em quatro dimensões, K>0, κ real não nulo fixado, φ0 constante projetada e escalares inertes herdados. Cada elemento tem ordem finita de jatos. Não se afirma comparação pronta com φ=id, outros fundos, tensores espectadores ou um anel restrito com K variável.

## 2. O setor sem derivadas não fornece o cancelamento

Sym²W tem dois escalares, dois tipos Weyl e outros tipos sem emparelhamento com Λ³G. Assim o setor sem derivadas tem dez contrações: oito produtos dos dois escalares I,J_W com as quatro cúbicas de ghosts e duas contrações de tipo Weyl quadrático com CCm.

Na avaliação Killing/TT já usada079–081, as cúbicas ímpares têm valores

βo=−6θ012/z0,   γo=+6θ012/z0³,
ev(s1γo)=−K ev(s1βo),   K=1/z0².

Essa proporcionalidade vale na avaliação; não identifica as cocadeias universais. Os produtos com I são pares em k, e os dois tipos Weyl são invisíveis por Bianchi. Para qualquer combinação do setor,

Lk(s1Q)=A R(k),
R(k)=24k³/z0−96k/z0³,
A∈Rher independente de k.

Em k=2/z0, R(k)=0; o cancelamento exigiria +8/z0². Logo nenhuma combinação desse setor resolve. A conclusão conserva os coeficientes herdados, inclusive nilpotentes, e a possibilidade de somar fronteiras s0. A contribuição direta de antifields h*C⁴ continua invisível pelo detector079. A exclusão não alcança todos os termos com derivadas.

[Prova do setor](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SETOR_FINITO_082_20260910_052417_739397/PARECER_SETOR_FINITO_SEM_DERIVADAS_082.md>).

## 3. O diferencial sobre todos os jatos foi identificado

Se Mcal é o módulo linear de Weyl modulo EOM e N=Sym²Mcal, a diagonal E=q+2 torna-se

(H^q(s0)_(E=q+2),d1) ≅ Rher ⊗ (C^q(g,N)^h,dCE),
h=so(1,3), g=álgebra matricial de Killing.

O lado direito é o subcomplexo invariante pela isotropia, não o CE relativo. As fórmulas sobre os geradores são

d1p=−Mghost p,
d1Mghost=−Mghost²+Kpp♭,
d1W_r=p^a∇bar_aW_r+𝔯(Mghost)W_r.

Aqui Mghost=antisym(∇C)=−g0⁻¹m. A matriz chamada M na nota do setor finito é g0⁻¹m, com o sinal oposto. Mcal é um terceiro objeto: o módulo de coeficientes. J_W é o pseudoscalar quadrático local, e βo uma cúbica de ghosts; não se confundem com a involução J=Luz ou a constante β_TGL.

As igualdades acima são sobre classes: as fórmulas completas conservam s0p2, s0k2 e s0(T_r,2−𝔯(H/2)W_r). O tensor T_r=(∇g)^rWg completa naturalmente cada jato. O comutador de transvecções mantém a curvatura e todos os índices adicionais dos jatos. As relações de EOM/Bianchi são preservadas.

Não foi provada local finitude sob g: transvecções podem aumentar a ordem indefinidamente. A dimensão dez de g não torna N finito nem autoriza Whitehead. O operador foi identificado; sua imagem completa ainda precisa ser calculada.

[Demonstração CE](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) · [Revisão independente](<__CE_REVIEW__>).

## 4. A obrigação agora é a classe seguinte; uma corrente explícita

Defina ν(p)=ε_abcd p^ap^bp^cp^d/4!. O alvo a=[A6] corresponde a J_Wν(p), incluindo o fator volume da referência. Ele é fechado por dCE: a ação de isotropia tem traço zero e o termo de transporte teria cinco p em dimensão quatro.

Pela transferência080,

−[A6]∈im d1E5  ⇔  [J_Wν(p)]_CE=0 em H⁴(Cnat,dCE).

A não nulidade de [A6] em H⁴(s0) não decide a classe na cohomologia seguinte. A imagem não nula encontrada081 tampouco decide sua nulidade.

Uma família horizontal, permitida sem retirar os demais cochains, é

q_V=ε_abcd V^a p^bp^cp^d/3!,
dCE q_V=(div_bar V)ν(p).

Para V=∇bar J_W, a corrente gradiente q_grad satisfaz dCE q_grad=(□bar J_W)ν(p). Há realização finita antes da cohomologia:

s1q_grad+s0q6=(□bar J_W)ν(C),
q6=[t⁶]{ι_(grad_g 𝒥(g))vol_g evaluated on (tC)³/3!},
g=g0+t h,  𝒥(g)=tr(W(g)∧W(g))/vol_g.

q6 é da espécie h³C³ e tem ordem finita de jatos. Para engenharia zero, multiplicar a identidade inteira por κ. Essa imagem é □bar J_W, ainda não −J_W: nenhum cancelamento foi declarado. A nota não calcula seu perfil TT.

[Cociclo e corrente](<C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md>) · [Revisão independente](<__CURRENT_REVIEW__>).

## 5. Evidência e pendências

O [recibo finito082](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/CONTROLES_SETOR_SEM_DERIVADAS_082.json>) registra 18 controles algébricos exatos e um de integridade de fontes, numa execução de Python com biblioteca padrão. Aritmética e proveniência tiveram revisão estática; zero rerun e zero Lean novo. A completude tensorial, a identificação CE e a corrente gradiente são demonstrações escritas revisadas, não resultados de uma amostragem numérica.

A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_082_20260910/PARECER_SETOR_FINITO_E_CE_082.md>) separa esses alcances. A aprovação da corrente construída pela raiz está em parecer externo próprio. As notas de origem que registravam revisão pendente devem ser lidas junto dos pareceres posteriores, preservando a história.

[OPEN] Calcular a imagem CE no módulo completo com derivadas, decidir a classe alvo e construir uma primitiva finita admissível, ou provar uma exclusão geral. Passar num detector é necessário, mas não prova a identidade universal. A investigação083 fica excluída desta entrega.

Continuam também a torre real e demais canais de anomalia, contratermos causais e QME, corrente/carga interagentes, compatibilidade entre fundos/estados/cortes, reconstrução gravitacional geral pelos mesmos dados selecionados, justificação UV e integração formal das construções aprovadas. A fase/ramo já paga não é reaberta.

Somente arquivos novos sob Chatgpt foram escritos. Originais, Atlas, índice, memórias canônicas, selo e gate continuam intactos. Nenhum teste de natureza foi realizado.
''')
report_pin = md(OUT / 'REEXAME_SUFICIENCIA.md', report)
memory_pin = md(OUT / 'MEMORIA_DE_TRABALHO_082.md', r'''# Memória de trabalho082 — 10/09/2026

[REAL — captura e controles] [DERIVED — demonstrações escritas revisadas]. A entrega081 foi progresso: imagem E5 não nula e direção independente de A6. Esta entrega082 preserva esse resultado e acrescenta a exclusão de TODO o setor sem derivadas, a identificação CE em todos os jatos e a corrente gradiente finita. Esta memória é nova em Chatgpt; não substitui ou bifurca o Atlas canônico.

Canônico: v338, quatro pins iguais081, 683 embutidos, 77/98 módulos acompanhados presentes e 21 ausentes. Leitura por AST e bytes, sem execução/importação. H3 interno, fase/ramo e falsificadores continuam reconhecidos; UV aberta na fonte.

Setor sem derivadas: dez contrações = oito produtos escalares + dois tipos Weyl. Imagem do detector Rher·R(k), R=24k³/z0−96k/z0³. Toda ela anula k=2/z0, mas o alvo exige +8/z0². Derivadas não classificadas. Rher é o anel da referência FIXADA com escalares inertes; não promover a outros fundos, K variável ou tensores espectadores.

Todos os jatos: diagonal E=q+2 ≅ CE(g,Sym²Mcal)^h. Mcal é quociente Weyl/EOM; Mghost=antisym∇C=−g0⁻¹m. Na nota finita o símbolo M tem o sinal oposto. Fórmulas d1p=−Mghost p; d1Mghost=−Mghost²+Kpp♭; d1W_r=p∇W_r+𝔯(Mghost)W_r. Fronteiras s0 e curvatura nos índices adicionais são conservadas. Invariante pela isotropia não significa relativo. Não usar Whitehead para N infinito sem hipótese nova.

Alvo: a=J_Wν(p) é cociclo CE. [A6]≠0 em H(s0) não decide [a]_CE. A obrigação −[A6]∈im d1 equivale a [a]_CE=0. q_grad=ι_grad(J_W)vol avaliada em C³ dá s1q_grad+s0q6=(□J_W)ν(C); q6 é o coeficiente finito da forma natural ativa. Engenharia zero exige κ. Nenhuma igualdade □J_W=−J_W foi usada.

Evidência nova: 18 controles algébricos + 1 de integridade, uma execução; revisão estática sem rerun; zero Lean. A matemática geral é escrita revisada.083 excluída. Persistem classe CE completa, admissibilidade causal, torre/anomalias, QME, estados/fundos/cortes, reconstrução pelos mesmos dados e UV.
''')
design_pin = md(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_082.md', r'''# Adendo082 ao desenho do fechamento — 10/09/2026

[DERIVED — no domínio métrico fixado]. Registro novo sob Chatgpt, aditivo; nenhum desenho canônico foi alterado.

O caminho crítico passa de “buscar um quadrático de Weyl” para uma obrigação cohomológica com operador explícito:

redução E4/E5 → CE(g,Sym²Mcal)^h → [J_Wν]_CE → primitiva finita admissível → levantamento C6 → torre real e demais canais.

Pago082: os dez candidatos sem derivadas não cancelam A6; todos têm resposta zero em k=2/z0. Isso exclui um setor inteiro, mantendo a imagem não nula081 em outras frequências. Pago082: d1 é CE com ação nas transvecções e em todos os jatos, respeitando as relações. Pago082: o alvo é cociclo CE e q_grad produz □J_W com uma correção BRST finita q6.

Não pago: nulidade da classe CE, identidade universal r6+s1Q=s0a6, admissibilidade do contratermo e levantamento em ordens posteriores. A corrente gradiente é um candidato fora do setor excluído; não é declarada solução. Finitude por elemento não implica corte finito estável sob g, nem ML ou lim¹ nulo.083 fica fora desta entrega.

O fechamento geral ainda precisa da reconstrução gravitacional pelos mesmos dados selecionados e suas compatibilidades, da teoria quântica interagente com QME e dos argumentos da rota UV. H3 interno, fase/ramo e falsificadores permanecem reconhecidos. Integração dos 21 módulos acompanhados ausentes é pendência separada.

Validação: 18 controles algébricos exatos + 1 de fontes, sem rerun; demonstrações escritas e revisões independentes, zero Lean novo. Canônico v338 relido e igual081. Nenhum original, memória canônica, selo ou gate modificado.
''')
print(json.dumps({'root_review': review_pin, 'root_receipt': receipt_pin,
                  'report': report_pin, 'memory': memory_pin, 'design': design_pin}, ensure_ascii=True))
