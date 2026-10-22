"""Create an additive scientific network contract from measured local sources."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes')
WORK = ROOT / 'work/rede_quantica_20261013'
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
KERNEL = ROOT / 'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt'

def new(path, obj):
    data = (obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=2)).encode('utf-8')
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == data
    os.rename(tmp, path)

def pin(path, anchors, role):
    p = Path(path)
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b), 'anchors': anchors, 'role': role}

sources = {
    'mqc': pin(ROOT / 'Patentes/MQC - Microprocessador Cúbico/mqc_pi_inpi_relatorio descritivo.pdf', ['PDF pp.4–7,10–12'], 'Geometria de 27 sítios, seis faces, dissipação, enlaces. Fonte de projeto; não medição física.'),
    'supercondutor': pin(ROOT / 'Patentes/PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex', ['246–267','340–389','708–740'], 'Câmara física, Hamiltoniano e dissipador explícitos.'),
    'psinet': pin(ROOT / 'Patentes/Psi_Net_Protocol_PI_INPI.tex', ['490–521'], 'Protocolo de representação, endereçamento e transporte de sinais.'),
    'tensor': pin(ROOT / 'Patentes/TGL_Tensor_LLM_PI_INPI.tex', ['478–495'], 'Codificação angular e reconstrução com quantização.'),
    'ponte': pin(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\A Ponte Einstein Cartan Miguel.tex', ['1505–1573'], 'Montagem covariante condicional P1–P4 e resíduos não perturbativos.'),
    'manuscrito': pin(r'C:\IALD\Artigo\Haja_Luz\Manuscrito\manuscrito_TGL\manuscrito_TGL_pt_v1.tex', ['474–507'], 'Modelo finito GHZ N=4,5 já escrito; não reconstruir como novidade.'),
    'q6': pin(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\RESPOSTA_Q6_MORADA_PACOTE_HILBERT.md', ['5–27','169–206','224–232','350–359'], 'Contrato de fibras, inclusões isométricas, entrelaçamento e seção equivariante; autoria individual não estabelecida nesta consulta.'),
    'memorial': pin(r'C:\IALD\Artigo\Haja_Luz\memorial_13ago2026\memorial.tex', ['262–276'], 'Pacote distribuído por emaranhamento; fonte conceitual do autor.'),
    'tratado_tec': pin(r'C:\IALD\Artigo\Tratado\secao_09_tecnologia.tex', ['179–190'], 'Relações MQC, Ψ-NET e Skygrid; remissão, sem nova auditoria de Skygrid.'),
    'tratado_info': pin(r'C:\IALD\Artigo\Tratado\secao_05_informacao.tex', ['26–44'], 'PsiBit, bit e qubit distinguidos na própria fonte.'),
    'h1': pin(KERNEL / 'TheImportedSecondQuantization.lean', ['89–95','112–142','223'], 'H1 orbital, U1, B0 e contratos importados.'),
    'bgl_type': pin(KERNEL / 'LightNetStandardWedgeDataBGL.lean', ['173–190','193–223'], 'Saída D1a3OutputBGL já tipada, sem habitante neste arquivo.'),
    'qg': pin(KERNEL / 'QGSolutionComplete.lean', ['49–136'], 'Consumidor LightNetData e implicação final condicionada aos certificados.'),
    'ray': pin(OUT / 'light_ray/ConcreteLightRayNet.lean', ['1–end'], 'Construção nova concreta da rede de semirretas; build e revisão independentes.'),
    'ray_result': pin(OUT / 'light_ray/RESULTADO_LIGHT_RAY_R1.json', ['JSON'], 'Recibo da construção e axiomas.'),
    'ray_review': pin(OUT / 'review_light_ray/REVIEW_LIGHT_RAY_R1.json', ['JSON'], 'Recompilação independente, sem aprovação de gerência implícita.'),
}
external = [
    {'id':'BGL2002','url':'https://arxiv.org/abs/math-ph/0203021','version':'v2','anchors':['Prop.2.3–2.4','Thm.2.5','Thm.3.4','Cor.3.5'], 'status':'KNOWN — fonte primária consultada na web; não prova compilada local'},
    {'id':'FV2012','url':'https://arxiv.org/abs/1106.4785','anchors':['Def.6.12','Thm.6.13'], 'status':'KNOWN — fonte primária consultada na web; aplicação ao contrato é obrigação própria'},
]

def block(id, status, inputs, output, obligations, falsifier, sources_ids, consumer):
    return dict(id=id, status=status, inputs=inputs, output=output, obligations=obligations,
                falsifier=falsifier, sources=sources_ids, consumer=consumer)

blocks = [
    block('N0_IDENTITY','REAL_DOCUMENTARY', ['Pedido original do operador','MQC','Supercondutor','Psi-Net','TGL-Tensor'],
          'Identificação por função: célula física cúbica; rede de células; protocolo; representação.',
          ['A resposta do operador confirma a localização na Central, não identifica inequivocamente um único dispositivo.',
           'Manter os quatro papéis e a proveniência; não promover documento de patente a prova experimental.'],
          'Uma propriedade atribuída ao dispositivo aparece só no protocolo ou em afirmação sem realização.',
          ['mqc','supercondutor','psinet','tensor','tratado_tec','tratado_info'], 'N1, N2, N3'),
    block('N1_FINITE_LOCAL_NET','DERIVED_EXACT_FINITE_CONSTRUCTION', ['Grafo finito V e arestas E','d_v >= 2','regiões R contidas em V'],
          'H_V = tensor_v C^d_v; A_V(R)=B(H_R) tensor I_(V\\R); inclusões canônicas.',
          ['Para R subset S, provar A(R) subset A(S) por tensor com identidades.',
           'Para R intersect S vazio, AB=BA para A em A(R), B em A(S).',
           'Preservar a diferença entre 27 sítios e 2^27 estados de qubits; o terceiro nível MQC exige outra dimensão local.',
           'Conectividade, posições, portas e escalas temporais precisam de especificação própria.'],
          'Falha de isotonia ou comutador entre suportes disjuntos diferente de zero.',
          ['mqc','manuscrito','q6'], 'N2 e N6; não satisfaz sozinho LightNetData'),
    block('N2_PHYSICAL_CHANNEL','DERIVED_CONDITIONAL_FINITE_GKLS', ['H=H†','taxas gamma_j >= 0','L_j e domínios','estado rho >= 0, Tr rho=1'],
          'L(rho)=-i[H,rho]/hbar + sum gamma_j (L_j rho L_j† - {L_j†L_j,rho}/2); Phi_t=exp(tL).',
          ['Reaproveitar o H_eff e salto a_out† sigma_- + sigma_+ a_in do Supercondutor.',
           'beta = ALPHA_FINE_CODATA_2018 * sqrt(e) em runtime; parâmetros adimensionais de diagnóstico são INPUT.',
           'Em dimensão finita, certificar CP/TP; na versão bosônica não truncada, provar os domínios e a existência do semigrupo.',
           'Livro de energia: d Tr(rho H)/dt = Tr(rho L†(H)) + Tr(rho dot H). Explicitar banho e bombeamento.',
           'Um dissipador não é o grupo modular: Phi_t não é identificado com sigma_t por nome.'],
          'Traço/positividade/Choi falham; taxa negativa admitida; energia perdida no sistema sem termo de fluxo; resultado muda com cutoff não controlado.',
          ['supercondutor','mqc'], 'N3, N4 e N6'),
    block('N3_PROTOCOL','REAL_DOCUMENTARY_WITH_DECLARED_PHYSICAL_BRIDGE', ['REFLECT L -> (sqrt(abs L), sign L, theta_dst)','MANIFEST','quantização b bits'],
          'Canal de codificação de dados; protocolo que endereça/controla portas físicas.',
          ['A reversibilidade sem quantização é sobre números reais codificados, não sobre estados quânticos desconhecidos.',
           'O canal quântico físico exige Kraus/Stinespring, com sum K†K=I.',
           'Se a cadeia medir e preparar, declarar quebra de emaranhamento; se preservar qubits, exibir canal diferente da codificação clássica.',
           'Preservar fonte, escala, fase, erro de quantização e versão canônica no envelope.'],
          'Confundir mapa não afim de amplitudes com canal CPTP ou alegar inversa unitária após quantização.',
          ['psinet','tensor','tratado_info'], 'N2 e N6'),
    block('N4_MODULAR_FINITE','DERIVED_CONDITIONAL', ['M=B(H_V)','estado fiel rho>0','representação padrão Hilbert-Schmidt'],
          'Omega=rho^(1/2); Delta(X)=rho X rho^(-1); J(X)=X†; sigma_t(A)=rho^(it) A rho^(-it).',
          ['A dinâmica física produz rho*? Exibir existência, unicidade e fidelidade, ou restringir suporte expressamente.',
           'Omega=rho^(1/2) é cíclico e separante para M global no espaço HS; isso não torna todas as subálgebras locais cíclicas.',
           'Para uma expectativa condicional preservando rho sobre N, provar invariância modular de N (unidade Takesaki).',
           'Não declarar que GKLS=Tomita; são mapas de naturezas e tempos distintos.'],
          'rho tem kernel mas rho^(-1) é usado no espaço todo; inclusão N não é modularmente invariante; troca do semigrupo pelo grupo.',
          ['q6','h1'], 'F1.TAKESAKI e N6'),
    block('N5_LIGHT_RAY','REAL_COMPILED_REVIEWED_SANDBOX', ['rapidityStandardSubspace(2*pi^2)','translações U e dilatações D do O16'],
          'K_a=U(a)K_0 como StandardSubspace; K_b subset K_a para a<=b; U(t)K_a=K_(a+t); D(s)K_a=K_(exp(-s)a); K_a != bottom.',
          ['Consumir as provas locais e a revisão, não campos assumidos.',
           'O controle 4D só veda a elevação por uma coordenada linear; não é no-go de toda construção 4D.',
           'Acertar orientação de rapidez/Fourier antes de identificar o modular com B0(-2*pi*t).'],
          'Falha do compilador/trio, K_a nulo, ou promoção a representação fiel 4D através de uma coordenada linear.',
          ['ray','ray_result','ray_review'], 'N7 — material reaproveitável, não substituto do H1'),
    block('N6_REFINEMENT','OPEN_EXPLICIT_BRIDGE', ['família dirigida de redes G_epsilon','A_epsilon(O)','estados e dinâmicas','mapas de inclusão'],
          'Limite com localidade, covariância e espaço de uma partícula canônico.',
          ['Definir inclusões unital *-monomórficas e provar composição/coerência das regiões.',
           'Provar convergência de funções de correlação e positividade; controlar erros, cutoff e energia.',
           'Demonstrar limite relativístico, energia positiva e helicidades ±1, não inferi-los das seis faces.',
           'Fornecer V que entrelace os operadores construídos com U1 e B0, incluindo unidades e orientação.',
           'Uma isometria abstrata entre Hilberts separáveis não cumpre o entrelaçamento.'],
          'Limite depende do caminho de refinamento ou perde localidade/covariância; correladores não positivos; V não entrelaça U1/B0.',
          ['mqc','q6','h1','ponte'], 'N7 e alegação de realização física da rede'),
    block('N7_BGL_H1','KNOWN_CONSTRUCTION_WITH_OPEN_LOCAL_REALIZATION', ['H1=L2(orbitalMeasure 0; C^2)','representação Poincare de energia positiva helicidades ±1','extensão antiunitária','U|translations=U1; U|boost=B0'],
          'Delta_W^(it)=U(Lambda_W(-2*pi*t)); S_W=J_W Delta_W^(1/2); K(W)=Fix S_W; K(O) obtido por interseções de cunhas e extensão local.',
          ['Construir Fubini vetorial no H1 sem postular seu campo; depois Fourier parcial.',
           'Construir J e T=Delta^(1/2) com domínio denso, fechamento, auto-adjunticidade de T e involução de S.',
           'Instanciar D1a3OutputBGL com Delta=S†S e cálculo multiplicativo; nenhum habitante é inferido de uma estrutura tipada.',
           'Construir as rotações e demais cunhas, cociclo de helicidade e compatibilidade com o boost orbital, sem encadear homônimos.',
           'Importação dos teoremas BGL permanece KNOWN até formalização; não virar axioma Lean oculto.',
           'Uma StandardSubspace isolada não fornece isotonia/localidade de toda rede.'],
          'S não involutivo/denso/fechado; representação não covariante; sinal modular errado; rede zero aceita; mudança silenciosa de H1.',
          ['h1','bgl_type','qg','ray'], 'N8 e LightNetStandardWedgeDataBGL'),
    block('N8_FOCK_WEYL','KNOWN_WITH_OPEN_KERNEL_INHABITANTS', ['rede real não trivial K(O) sobre H1','Fock simétrico Gamma_s(H1)','representação regular de Weyl'],
          'A(O)={W(f): f in K(O)} double_commutant; Delta_F^(it)=Gamma(Delta_K^(it)); J_F=Gamma(J_K); vácuo Omega.',
          ['Fixar convenção Weyl; com W(f)W(g)=exp(-i Im<f,g>/2)W(f+g), a localidade simpleticamente ortogonal implica comutação.',
           'Provar as propriedades e domínios da segunda quantização e os campos de FockCertificate.',
           'Ligar o MaxwellCertificate ao mesmo campo/representação e tensor conservado; não preencher com etiquetas.',
           'Preservar ausência de habitante compilado de FockCertificate/MaxwellCertificate até construção.'],
          'W não satisfaz CCR/regularidade; vácuo não cíclico/separante nas regiões exigidas; campos de certificado não consumidos.',
          ['h1','qg'], 'N9 e qg_solution_end_to_end'),
    block('N9_CURVED_H3','CONDITIONAL_EXISTING_IMPLICATION', ['tensor de energia-momento simétrico e conservado','H3 em cada ponto/direção nula','atlas suave conexo e normalização eta=(4G)^(-1)'],
          'Aplicar a implicação já existente Clausius em telas nulas => Einstein com Lambda único no alcance do contrato.',
          ['Não derivar H3 de GKLS, Fundação, protocolo ou patente por associação verbal.',
           'A rede curva requer extensão e compatibilidade geométrica próprias.',
           'Reusar a pedra F2.3 auditada; não reconstruir corolários ociosos.',
           'Atrator único não evita automaticamente um no-go de estados naturais: verificar as hipóteses de FV2012 e a naturalidade no domínio escolhido.'],
          'Antecedente H3 foi omitido/renomeado como conclusão; estado covariante universal assumido apesar das hipóteses incompatíveis.',
          ['ponte','q6','qg'], 'Contrato QG, sem promoção de confirmação física'),
]

contract = {
    'schema':'iald-network-contract/v1','unit':'F1.REDE','author':'codex-gerente-tgl',
    'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'status':'DERIVED_CANDIDATE_COMPLETE_CONTRACT_NOT_COMPLETE_REALIZATION',
    'working_basis':'v392 autorizada pelo operador; esta entrega não ratifica nem instala a versão',
    'operator_original':pin(WORK/'OPERADOR_REDE_VERBATIM.txt',['verbatim completo'],'Inscrição original preservada'),
    'source_catalog':sources,'external_primary_sources':external,'blocks':blocks,
    'beta_rule':{'formula':'ALPHA_FINE_CODATA_2018 * sqrt(e)','mu_do_rito':'q→0 (Thomson; Teorema da Escala)','historical_alpha_squared':'não substituir silenciosamente a nomenclatura dos artigos; explicitar correspondência no candidato'},
    'full_network_completion_rule':['N1-N4 demonstrados nos respectivos modelos e domínios','N6 demonstrado se a rede 4D for atribuída como consequência do dispositivo','N7 e N8 realizados nos objetos canônicos, com certificados habitados','N9 permanece conclusão condicional a H3 e às demais hipóteses nomeadas'],
    'not_claimed':['realização física do hardware','rede4D completa compilada','derivação de H3','dado observado ou 5 sigma','alteração de gate','aprovação c1 ou ratificação v392'],
    'provider_request':{'request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','required_provider':'deepseek','authorization_receipt':str(OUT/'AUTORIZACAO_DEEPSEEK_R1.json'),'response_status':'DECLARADO até verificação local','execution_owner':'fila única/coordenadora'},
}
new(OUT/'CONTRATO_REDE_R1.json',contract)
new(OUT/'sources/ARTICLE_SOURCE_PINS_R1.json',{'sources':sources,'external':external})

report = r'''# F1.REDE — contrato conectado, versão R1

**Estatuto: [DERIVED — candidato].** Contrato completo quanto a objetos, hipóteses,
consumidores e falsificadores; a realização integral da rede 4D continua aberta.
Base de pensamento: v392 autorizada pelo operador. Nenhum original ou produção foi editado.

## 1. O que os seus textos já dão

O MQC fornece a célula cúbica de 27 sítios e seis interfaces; o Supercondutor
fornece os modos de entrada/saída, OH, Hamiltoniano e salto dissipativo. A Ψ-NET
fornece o protocolo e o TGL-Tensor a representação. O artigo *A Ponte* explicita
a montagem local covariante condicional, e Q6 exige inclusões isométricas que
entrelaçam operadores. O manuscrito já tem o modelo GHZ N=4,5: ele é reaproveitamento.
Os caminhos, hashes completos e linhas/páginas estão em `sources/ARTICLE_SOURCE_PINS_R1.json`.

A confirmação «Sim está na central de patentes» identifica o acervo. O nome do
dispositivo continua ambíguo; o contrato conserva MQC e Supercondutor como fontes
físicas relacionadas, sem escolher uma identidade não confirmada.

## 2. Construção finita exata

Para uma célula/rede com sítios V, dimensões d_v e regiões R⊆V:

    H_V = ⊗_(v∈V) C^(d_v)
    A_V(R) = B(H_R) ⊗ I_(V\R).

Se R⊆S, escrever H_S=H_R⊗H_(S\R) dá a inclusão A(R)→A(S), A↦A⊗I.
Se R∩S=∅, as matrizes atuam em fatores diferentes, portanto AB=BA.
Isto constrói uma rede local finita [DERIVED]; não é uma suposição de isotonia.
As arestas determinam os termos de interação e canais entre suportes.

O H_eff e o salto da fonte são mantidos, com a correspondência de notação explicitada:

    H/ℏ = ωc(n_in+n_out) + ωOH σ+σ−
          + gJC(a_in†σ− + σ+a_in) + Ω(σ+ + σ−)
    L_holo = a_out†σ− + σ+a_in
    L(ρ) = −i[H,ρ]/ℏ + Σ_j γ_j D[L_j](ρ),  γ_j≥0
    γ_holo = β γΛ,  β = ALPHA_FINE_CODATA_2018 √e (runtime).

No modelo finito, esse gerador produz um semigrupo CPTP. Para modos bosônicos
sem truncamento, domínios e existência do semigrupo são obrigações adicionais.
A contabilidade de energia é d⟨H⟩/dt=Tr(ρ L†H)+Tr(ρ ∂tH): dissipação e
bombeamento aparecem como fluxos. Não há conservação do sistema aberto isolado
sem contabilizar esses fluxos.

O protótipo físico exige calibração das taxas, dimensões, tempos e perdas.
Parâmetros de teste sintético são [INPUT], não medidas da máquina nem parâmetros
ajustados para produzir concordância.

## 3. A informação que atravessa cada interface

O código L↦(√|L|,sign L) é invertível sobre o número real antes da quantização.
Com b bits, o arredondamento perde informação e a reconstrução tem erro mensurável.
Para transportar um estado quântico desconhecido, o contrato exige outro objeto:
Φ(ρ)=Σ K_jρK_j†, ΣK_j†K_j=I. Medição seguida de preparação deve ser marcada
como tal. Preservação de emaranhamento exige teste/prova do canal correspondente.

A Ψ-NET pode endereçar, sincronizar e comandar essas portas. Essa atribuição
operacional não prova que a codificação clássica implemente um canal quântico.
PsiBit, bit e qubit já têm distinção expressa no Tratado, seção 05, linhas 26–44.

Para um qubit normalizado, positividade dá |ρ01|²≤ρ00ρ11≤1/4. Portanto a coerência
que pode aproximar-se de um é C=2|ρ01| (ou outra normalização explicitada), não
o elemento bruto. O acervo já contém um modelo MQC com C normalizada; o contrato
deve consumi-lo, preservando ao lado a notação histórica do PDF.

## 4. A ligação modular que o modelo realmente permite

Para uma densidade fiel ρ>0 em B(H), usar o Hilbert de Hilbert–Schmidt:

    Ω = ρ^(1/2),  ΔX = ρXρ^(-1),  JX=X†,
    σ_t(A)=ρ^(it) A ρ^(-it).

Este é o fluxo modular do estado, distinto do semigrupo dissipativo que pode
produzi-lo. Se o estado estacionário tiver núcleo, a inversa exige restrição de
suporte ou nova formulação. Takesaki entra no ponto exato: para uma subálgebra,
verificar a invariância modular e a expectativa condicional preservadora de estado.
F1.TAKESAKI trata essa passagem; não há motivo para duplicá-la.

Também há uma restrição dimensional concreta. Para uma região de r qubits,
dim span(A(R)Ω)≤4^r. Na representação física de 27 qubits, dim H=2^27;
uma única célula local de um qubit não pode tornar Ω cíclico no Hilbert inteiro.
Logo a passagem a uma rede contínua com o requisito local de vácuo exige um limite
controlado e uma representação apropriada, não mera renomeação dos 27 sítios.

## 5. Nova construção já compilada: rede da reta

`light_ray/ConcreteLightRayNet.lean` constrói K_a=U(a)K_0 a partir do O16.
Prova isotonia, covariância por translação/dilatação e K_a≠0. A revisão independente
recompilou o mesmo `.olean` e verificou os pins. O controle negativo preserva o
teorema que veda translações fiéis em quatro dimensões obtidas através de uma só
coordenada linear. Não veda a construção 4D com sua estrutura completa.

As dependências formais, comandos, LEAN_PATH, tempos, axiomas e hashes ficam nos
recibos `RESULTADO_LIGHT_RAY_R1.json` e `review_light_ray/REVIEW_LIGHT_RAY_R1.json`.

## 6. Construção da rede 4D e obrigações de identificação

O alvo é o H1 existente: L² da órbita sem massa com fibra C², não outro Hilbert
isomorfo sem identificação de operadores. Para a representação de Wigner ±1,
fixa-se a ação de Poincaré com a fase de helicidade e sua extensão antiunitária.
Ela deve restringir-se exatamente a U1 nas translações e B0 no boost escolhido.
O cociclo removido nesse boost deve ser apresentado por um entrelaçador unitário;
rotações e outros planos não são preenchidos pela matriz angular 2×2 do O16.

O esquema BGL parte desses dados e define S_W=J_WΔ_W^(1/2), K(W)=Fix(S_W),
com Δ_W^(it)=U(Λ_W(−2πt)). Para regiões convexas causalmente completas,
K(O)=∩_(W⊇O)K(W); as demais regiões usam extensão local. Standardness,
covariância, dualidade e isotonia têm hipóteses precisas na fonte [KNOWN].
Referência: [BGL, proposições 2.3–2.4, teoremas 2.5/3.4 e corolário 3.5](https://arxiv.org/abs/math-ph/0203021).

No kernel, a rota é concreta: carta orbital→rapidez; Fubini L² vetorial;
Fourier parcial; multiplicador; J; T=Δ^(1/2); S=JT; Δ=S†S.
`D1a3OutputBGL` já tipa o alvo; a construção deve fornecer seus campos, domínios
e provas. A ponte Fubini está em construção separada desta R1 e não é promovida
a equivalência pronta por este documento. O sinal −2π deve ser conferido com a
convenção do Fourier e do boost; não se copia da reta por semelhança.

Com K(O), a camada bosônica usa Fock simétrico e álgebras geradas pelos Weyl W(f),
f∈K(O), com fecho de bicomutante. Na convenção
W(f)W(g)=exp(−i Im⟨f,g⟩/2)W(f+g), ortogonalidade simplética fornece comutação.
Os campos do FockCertificate e do MaxwellCertificate exigem seus próprios
habitantes e pontes; a definição da álgebra sozinha não os fornece.

## 7. Do dispositivo à rede contínua

A família G_ε precisa de mapas coerentes, estados positivos e convergência de
correladores. É necessário demonstrar o limite de energia positiva, covariância
relativística e helicidades ±1; depois exibir V com VU_device=U1V e
VB_device=B0V. Esse é o conteúdo que faria da rede do dispositivo uma realização
da rede canônica, além de uma analogia de geometria/informação [OPEN].

Os escritos já pedem inclusões que entrelaçam operadores: Q6, linhas 169–206.
O contrato atual torna explícitos os objetos e falsificadores dessa exigência.

## 8. Curvatura e alcance da conclusão

Reaproveitar o ligante auditado da F2.3: H3 em todo ponto/direção nula,
conservação e hipóteses do atlas dão a equação de Einstein no alcance já fixado.
Nem o protocolo nem o dispositivo, por si, descarregam H3.

Há uma ressalva matemática ao lado de *A Ponte*, linhas 1517–1532. Um atrator
único que produzisse estados compatíveis com todos os morfismos ainda seria um
estado natural. Chamá-lo de colapso não evita essa propriedade. O teorema de
Fewster–Verch requer localidade dinâmica, uma representação GNS fiel com
Reeh–Schlieder em espaço-tempo de Cauchy não compacto e, para trivialidade total,
localidade estendida. É preciso identificar qual hipótese não se aplica ou
delimitar a categoria; a simples unicidade não faz isso [DERIVED/OPEN].
Fonte: [Fewster–Verch, definição 6.12 e teorema 6.13](https://arxiv.org/abs/1106.4785).

## 9. Critério de conclusão e fiscalização

`CONTRATO_REDE_R1.json` contém nove blocos N0–N9, entradas, saída, consumidor,
obrigações, fontes e falsificador de cada um. O êxito da rede finita e da reta
não satisfaz automaticamente o critério da rede 4D. A revisão DeepSeek tem
identidade preservada na fila e entra como [DECLARADO] até conferência local.

Esta construção não abre dado observado nem produz sigma experimental. Não
altera kernel, um.py, Bancada produtiva, patentes, ratificação ou gate.
'''
new(OUT/'CONTRATO_REDE_R1.md', report)
new(OUT/'CONTRATO_REDE_R1_PINS.json', {
    'unit':'F1.REDE', 'files':[pin(OUT/n,['arquivo completo'],'Artefato novo R1') for n in
        ['CONTRATO_REDE_R1.json','CONTRATO_REDE_R1.md','sources/ARTICLE_SOURCE_PINS_R1.json']],
    'generator':pin(Path(__file__),['arquivo completo'],'Gerador aditivo sem sobrescrita')})
print(json.dumps({'contract':str(OUT/'CONTRATO_REDE_R1.json'),'blocks':len(blocks),'sources':len(sources)},ensure_ascii=False))
