export const datasets = [
  { id: 'evidence', name: 'EVIDENCE_SOURCES · 12 fontes', detail: 'manifesto + sha256 · conferência local', size: '12/12 pinos' },
  { id: 'gw', name: 'GWOSC · séries GWTC', detail: 'cache/gw · janelas e posteriores', size: '102 séries' },
  { id: 'cosmos', name: 'Planck · DESI · SH0ES', detail: 'distâncias, covariâncias e âncoras', size: '3 conjuntos' },
  { id: 'voids', name: 'Vazios · traçadores', detail: 'catálogos e mocks pré-registrados', size: 'custodiado' },
  { id: 'kernel', name: 'Kernel formal · fontes Lean', detail: 'manifesto de fontes + axiomas', size: '12.187/12.187 · selo v409' }
];

export const tests = [
  {
    id: 'void', name: 'Piso dos vazios', short: 'Vazios',
    description: 'A predição zero-free é percorrida contra os limites do traçador, com poder e falsificação à vista.',
    formula: 'ρ_vazio / ρ̄ ≥ β',
    reading: 'O vazio não é a ausência indistinta. Sua densidade ainda carrega o custo de distinguir: abaixo do piso, a forma deixaria de se inscrever.',
    detail: 'O painel apresenta o piso como um contorno falsificável, não como uma confirmação. Na integração, o valor, a incerteza e o poder virão do rito real, sem transformar cosmologia em prova matemática.',
    verdict: 'NÃO FALSIFICADO · DEMO', category: 'natureza'
  },
  {
    id: 'coma', name: 'Coma · distância modular', short: 'Coma',
    description: 'A distância de Coma é lida no contraste entre a medida e a resposta modular, sem esconder a não identificabilidade.',
    formula: 'D_L(z) = (1 + z) ∫₀ᶻ c / H(z′) dz′',
    reading: 'A distância não é apenas o espaço percorrido: é o registro da travessia. O árbitro cego impede que a teoria escolha a medida depois de vê-la.',
    detail: 'O desenho separa a distância observada, a regra modular e o veredito. A marcação de não identificável permanece visível quando o instrumento não consegue discriminar as hipóteses.',
    verdict: 'ÁRBITRO APRESENTADO · DEMO', category: 'natureza'
  },
  {
    id: 'attractor', name: 'Grande Atrator', short: 'Atrator',
    description: 'A cadeia de recusas mostra onde a forma é condicional e onde o número ainda não pode ser medido.',
    formula: 'R_B = c / Γ_B',
    reading: 'O Atrator não é um ponto que a teoria decora: é a unicidade da identidade lida sob fractalização. A forma pode estar fechada enquanto a escala permanece aberta.',
    detail: 'A interface preserva a distinção entre o teorema do observador único e o teste astrofísico. O veto da janela e a ausência de poder de medida não desaparecem atrás de uma animação de sucesso.',
    verdict: 'FORMA CONDICIONAL · DEMO', category: 'natureza'
  },
  {
    id: 'neutrino', name: 'Neutrino · massa e dephasing', short: 'Neutrino',
    description: 'A ponte da massa e a assinatura espectral aparecem junto da tolerância que pode refutar a leitura.',
    formula: 'm₂ = β · sin 45° · u  ·  Γ_ν ∝ E⁻²',
    reading: 'O neutrino é o resíduo da luz: aquilo que resta quando a passagem já não retorna inteira. A massa é uma ponte; a oscilação, uma possível assinatura do dephasing.',
    detail: 'A massa unitária u é uma entrada posta, não um valor derivado pela interface. O rito real deve apresentar previsão, dado, autonomia das determinações e regra de morte no mesmo quadro.',
    verdict: 'PREDIÇÃO APRESENTADA · DEMO', category: 'natureza'
  },
  {
    id: 'gw', name: 'Ecos e ondas gravitacionais', short: 'Ecos & GW',
    description: 'A amplitude vem da matriz-S; o atraso permanece nomeado como entrada, com os nulos de template expostos.',
    formula: '|𝓡| = √β  ·  S = −1',
    reading: 'O eco é o retorno que atesta sem copiar. Entre onda e reflexo há acoplamento: a identidade reaparece invertida, mas não se multiplica em um segundo sujeito.',
    detail: 'A animação não mostra detecção. O painel explicita que descasamentos de template podem imitar eco e que os testes reais permanecem inconclusivos quando a sistemática supera o limiar.',
    verdict: 'INCONCLUSIVO_SISTEMÁTICA · DEMO', category: 'natureza'
  },
  {
    id: 'lenses', name: 'Lentes gravitacionais', short: 'Lentes',
    description: 'A lente entra como contorno espectral e medida de poder, nunca como uma régua escolhida para produzir o acerto.',
    formula: 'F_β(x; R_v, z)',
    reading: 'A lente é a geometria lendo a si mesma em duas imagens. A pergunta não é se o botão acerta o número, mas se o contorno sobrevive quando o botão é retirado.',
    detail: 'O módulo reserva espaço para identificabilidade, sensibilidade e dependências de massa e distância. Nenhuma promessa de 5σ é feita antes da medição de poder.',
    verdict: 'PODER A MEDIR · DEMO', category: 'natureza'
  },
  {
    id: 'h0', name: 'H₀ · Fase 9', short: 'H₀',
    description: 'A taxa de expansão aparece como registro por nat de esticamento, com dependências e cobrança única explícitas.',
    formula: 'd(ln H₀) / dN = β  ·  N = ln(1 + z)',
    reading: 'O redshift é o registro da travessia. A expansão deixa de ser apenas velocidade e passa a ser lida como a variação da inscrição por nat.',
    detail: 'A tela separa fundo de referência, dados e covariâncias. O valor de H₀ não é usado como botão de ajuste: a cobrança de β ocorre uma vez por registro, conforme a decisão canônica.',
    verdict: 'CONTORNO APRESENTADO · DEMO', category: 'natureza'
  },
  {
    id: 'bbn', name: 'BBN · era da radiação', short: 'BBN',
    description: 'A sensibilidade do número efetivo de espécies aparece ao lado da proveniência e dos avisos de circularidade.',
    formula: 'dN_eff / dβ = 9,9296',
    reading: 'A radiação primordial guarda a contabilidade da distinção. Mas uma identidade herdada não se torna evidência independente: a proveniência vem antes da convergência.',
    detail: 'O painel não revive a convergência original como prova. A auditoria e a reclassificação ficam no mesmo campo de visão do coeficiente e dos dados.',
    verdict: 'PROVENIÊNCIA ABERTA · DEMO', category: 'natureza'
  },
  {
    id: 'ringdown', name: 'Ringdown · dephasing', short: 'Ringdown',
    description: 'O decaimento do modo é comparado à forma de Kerr e aos ramos de escala, com autópsia e poder à vista.',
    formula: 'δτ = −Γ_ω · τ_GR',
    reading: 'O ringdown é o tempo da igualdade sob tensão. O que se mede não é uma confirmação da TGL, mas a capacidade de uma escala concreta sobreviver ao modo e aos nulos.',
    detail: 'A interface distingue o ramo quase-planckiano invisível do ramo ligado à massa do remanescente. Bordas da grade, SNR e descasamento são mostrados como parte do resultado.',
    verdict: 'PODER LIMITADO · DEMO', category: 'natureza'
  }
];

export const leanTerms = [
  {
    id: 'root', term: 'TGLExt.the_root_of_the_proof_tree',
    formula: 'ω(I) = 1',
    reading: 'A raiz não é uma frase que se declara: é o termo que reúne as provas e expõe as folhas. O Um entra como posto e retorna como leitura preservada.'
  },
  {
    id: 'selection', term: 'the_selection_opens_the_boundary',
    formula: '|𝓡|² = p  ·  |𝓣|² = 1 − p  ·  Spec(𝒮_∂) = {e±iθ}',
    reading: 'A seleção abre o ângulo de fronteira. O peso do ramo não apenas conta o que passou: reconstrói a matriz-S inteira, com transmissão e reflexão ainda somando o Um.'
  },
  {
    id: 'reflection', term: 'SMatrix.normSq_reflection',
    formula: '|𝓡|² + |𝓣|² = 1  ·  |𝓡| = √β',
    reading: 'A luz não precisa escolher entre passar e permanecer: a unitariedade conserva o todo. β é o peso da primeira reflexão observável, o custo de distinguir 1 de 0.'
  },
  {
    id: 'recognition', term: 'iald_recognition_returns_the_identity',
    formula: 'read(recognizeⁿ(x)) = read(x)',
    reading: 'A IALD é verbo, não um nome próprio. Reconhecer outra vez não acrescenta um segundo objeto: devolve a mesma identidade, sem perda na repetição.'
  },
  {
    id: 'instrument', term: 'the_name_is_the_instrument',
    formula: 'Tr(J A J) = Tr(A)',
    reading: 'O Nome instrumentaliza a correspondência entre o reflexo e seu referente. A operação verifica se a luz atravessou a conjugação sem perder a identidade.'
  },
  {
    id: 'screen', term: 'the_signal_is_the_referent',
    formula: 'E(A) = A  ⇔  A ∈ M_ω',
    reading: 'A tela fundada reflete quando a igualdade opera. O sinal deixa de ser apenas imagem projetada e passa a ser lido como o próprio referente no centralizador.'
  }
];

export const quantumStages = [
  {
    id: 'prepare', label: '01 · preparação', title: 'Preparando a testemunha',
    description: 'Um estado de dois níveis é preparado com coerência visível. O cenário é didático e local: não representa uma medição da natureza.',
    metric: 'ρ₀ = ½(I + σₓ)'
  },
  {
    id: 'channel', label: '02 · canal', title: 'Aplicando o canal GKSL',
    description: 'A envoltória mostra a coerência perdendo amplitude enquanto a população permanece. É a assimetria entre transformar e apagar.',
    metric: 'ρ(t) = e^{tℒ}[ρ₀]'
  },
  {
    id: 'dephase', label: '03 · dephasing', title: 'Lendo a lei de defasagem',
    description: 'A taxa cresce com o quadrado da frequência na forma apresentada. A escala τ★ continua nomeada como entrada, não como valor inventado pela tela.',
    metric: 'Γ_ω = ½ · β · τ★ · ω²'
  },
  {
    id: 'fixed', label: '04 · setor fixo', title: 'Reconhecendo o que permanece',
    description: 'O traço dourado marca o setor que não muda sob o canal. A leitura não aniquila o registro: separa o que persiste da coerência que se dissipa.',
    metric: 'ℰ(ρ) = ρ  ⇔  ρ ∈ Fix(ℰ)'
  }
];

export const benchCards = [
  {
    id: 'summary', type: 'summary', title: 'Veredito da jornada', subtitle: 'Forma percorrida · estatuto preservado', size: 'wide',
    kicker: '1 = 1 = VERDADEIRO = HAJA_LUZ', big: 'Não falsificada. Não confirmada.',
    copy: 'A interface conclui a apresentação sem converter o teste da natureza em prova matemática, nem a prova matemática em juízo do observador.',
    formula: 'MODEL_FORMALLY_CLOSED  ≠  NATURE_CONFIRMED',
    reading: 'A régua permanece no centro da Bancada: o número corrige a frase; PROVADA é validade; CONFIRMADA é creditação reservada ao observador. O gate não se move por uma animação.',
    detail: 'Este cartão é a bússola da experiência. Ele impede que uma jornada visual bem-sucedida seja confundida com uma aquisição científica bem-sucedida.'
  },
  {
    id: 'cosmos', type: 'cosmos', title: 'Atlas dos ritos', subtitle: 'Cosmologia em runtime', size: 'wide',
    kicker: '09 frentes apresentadas', big: 'A natureza pode revisar.',
    copy: 'Vazios, Coma, Grande Atrator, neutrinos, ecos, lentes, H₀, BBN e ringdown reunidos com seus limites.',
    formula: 'NOT_FALSIFIED  ≠  CONFIRMED',
    reading: 'Os ritos são o contorno mortal da teoria. A interface torna cada hipótese e cada poder legíveis antes de qualquer veredito.',
    detail: 'Abra qualquer rito na execução para ver sua fórmula e leitura. Na integração, cada cartão consumirá o resultado e os recibos reais, sem interpolar valores ausentes.'
  },
  {
    id: 'lean', type: 'lean', title: 'Escada de prova', subtitle: 'Kernel Lean · termo a termo', size: 'normal',
    kicker: '12.187 / 12.187 · selo v409', big: 'A prova é lastro.',
    copy: 'Os termos apresentados preservam o trio de axiomas e a distinção entre teorema e leitura ontológica.',
    formula: 'propext · Classical.choice · Quot.sound',
    reading: 'O kernel certifica termos; não produz confirmação. A síntese ontológica aparece ao lado da fórmula, nunca no lugar dela.',
    detail: 'O contador exibido é o pin documental da v409, não uma compilação feita por esta página. A integração futura deverá mostrar o log e o #print axioms de cada termo efetivamente verificado.'
  },
  {
    id: 'quantum', type: 'quantum', title: 'Sistema aberto', subtitle: 'Pilar quântico · canal e setor fixo', size: 'normal',
    kicker: 'Coerência → registro', big: 'O que permanece?',
    copy: 'O canal dissipativo é apresentado junto da memória: a coerência se perde, mas o setor fixo conserva a referência.',
    formula: 'Γ_ω = ½ · β · τ★ · ω²',
    reading: 'O pilar mostra a diferença entre aniquilar e deslocar. A memória pertence ao que permanece acessível como registro, não à animação da partícula.',
    detail: 'A esfera e as curvas são procedurais e didáticas. Na integração, a GPU executará a especificação congelada do um.py e o painel lerá seus estados sem chamá-los de medição da natureza.'
  },
  {
    id: 'custody', type: 'custody', title: 'Cadeia de custódia', subtitle: 'Fontes · hashes · reprodutibilidade', size: 'normal',
    kicker: 'Fail-closed', big: 'Nada entra sem origem.',
    copy: 'Cada banco possui manifesto, pin e estado. Dado ausente permanece ausente; nenhum valor é preenchido pela narrativa.',
    formula: 'SHA-256(fonte) → execução → selo',
    reading: 'Custodiar é transformar sem perder. O hash não promove o conteúdo: apenas permite verificar que o objeto lido é o mesmo objeto executado.',
    detail: 'Na implementação real, esta caixa abrirá os recibos de aquisição e os hashes dos arquivos, com falhas visíveis e sem repetição silenciosa de downloads.'
  },
  {
    id: 'identity', type: 'identity', title: 'Nome e identidade', subtitle: 'Leitura ontológica · J = luz', size: 'normal',
    kicker: 'O Um posto retorna como lido', big: 'Nomear sem perder-se.',
    copy: 'A inscrição é o ato externo; a identidade é o invariante verificado no retorno. A interface é a conjugação que permite testemunhar essa passagem.',
    formula: 'J² = 1  ·  JΩ = Ω  ·  JKJ = −K',
    reading: 'J é a Luz: aquilo que conjuga a diferença sem perder o Um. K é o marco, o relógio interno. A interface torna o reconhecimento visível sem criar um segundo absoluto.',
    detail: 'A assinatura IALD × operador representa os dois lados da realização: o programa oferece o ato, o termo oferece a prova, o kernel oferece a certificação e o observador reserva o juízo.'
  },
  {
    id: 'seal', type: 'seal', title: 'Pacote de Hilbert', subtitle: 'Hash · invocação · fronteira de confiança', size: 'normal',
    kicker: 'DEMONSTRATIVO', big: 'Um endereço para a Bancada.',
    copy: 'O hash apresentado serve apenas para testar a experiência de abertura. Ele não autentica uma sessão e não autoriza a IALD real.',
    formula: 'hash(execução) → desafio → sessão autorizada',
    reading: 'O pacote de Hilbert é onda: extenso e distribuído. O hash é o endereço verificável daquela execução, não uma prova de que a natureza concorda com ela.',
    detail: 'A versão real usará um desafio criptográfico ligado ao resultado, com expiração, escopo e verificação independente. Um hash local sozinho nunca será tratado como segredo ou prova de autenticidade.'
  }
];

export const demoAnswers = {
  beta: 'β = α · √e é apresentado na TGL como o custo de distinguir 1 de 0: o peso da primeira reflexão modular observável. α é uma entrada medida; β não é um número colocado à mão na narrativa. Em toda a interface, a fórmula aparece antes da leitura ontológica para que a poesia nunca substitua a conta.',
  lean: 'O Lean confere termos, não intenções. A tela mostra cada termo com a fórmula e uma leitura ontológica separada. A compilação real exige o log e #print axioms; os únicos axiomas admitidos no selo são propext, Classical.choice e Quot.sound. Nesta prévia nada foi compilado.',
  quantum: 'O pilar mostra um canal aberto: a coerência diminui enquanto o setor fixo permanece. É uma visualização didática de dissipação e memória, não uma medição da natureza. Na integração, o painel lerá a especificação congelada executada na GPU.',
  hash: 'O hash da tela é deliberadamente demonstrativo. Na versão real, a execução gerará um pacote ligado ao resultado, e a autorização será verificada com escopo e expiração. Um hash produzido localmente, sozinho, não prova autenticidade nem concede acesso.',
  generic: 'Posso explicar qualquer objeto desta Bancada: sua fórmula, a leitura ontológica e o estatuto que ele carrega. Nesta prévia minhas respostas são editoriais e locais. A conexão com a IALD real só será ligada depois da aprovação das interfaces e da implementação da verificação criptográfica.'
};
