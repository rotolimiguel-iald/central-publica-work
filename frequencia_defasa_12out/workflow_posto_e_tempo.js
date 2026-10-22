export const meta = {
  name: 'posto-e-tempo',
  description: 'F1.FREQUENCIA (o rank como raiz e Tudo = D_β(F(1))) e F1.TEMPO (o tempo santo: sem observável, fluxo modular, dissipação e atrator): levantamento, pré-registro congelado, ótico e Lean em sandbox, duas auditorias, relatório',
  phases: [
    { title: 'Levantamento', detail: 'o que o cânone já tem, por trilha' },
    { title: 'Pré-registro', detail: 'afirmações e falsificadores congelados por hash antes de construir' },
    { title: 'Construção', detail: 'ensaio ótico sintético e pedra Lean em sandbox' },
    { title: 'Auditoria', detail: 'reprodução independente e lente de estatuto' },
    { title: 'Relatório', detail: 'resultado final, mapa e o que entra na v392' },
  ],
}

const SCR = String.raw`C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12`
const NOS = String.raw`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`
const C10 = String.raw`C:\IALD\Central de Patentes\work\cunhagens_10out`
const C12 = String.raw`C:\IALD\Central de Patentes\work\cunhagens_12out`

function regras(dir) {
  return String.raw`
REGRAS (sem exceção):
- Escreva SÓ dentro de ${dir} (crie a pasta). Nada no quadro, no mapa (não rode rotas.py registrar), na memória, no túnel, no Nós, no kernel do Nós, na Bancada_Um, no site ou no git.
- NÃO rode um.py, atlas_indice.py, arvore_da_prova.py, porta_memoria.py nem scripts de selo. Ler o um.py (${NOS}\um.py, v391, ~33 MB) é permitido só por busca com número de linha.
- Lean só em sandbox dentro de ${dir}, com LEAN_PATH só-leitura ao .lake de ${NOS}\tgl_kernel (as auditorias anteriores copiaram o toolchain v4.31.0 do elan para o sandbox). Impressão digital do tgl_kernel antes e depois tem de ser igual. Ao final apague toolchains, .lake e caches copiados (prefixo \\?\ para caminhos longos).
- Nenhum dado observado, nenhum provedor remoto, nenhuma chamada paga, nenhuma ferramenta de cálculo da Bancada.
- β NUNCA literal no código: leia por script a atribuição de ALPHA_FINE_CODATA_2018 nos bytes do um.py (sem executá-lo) e calcule β = α·√e em runtime; 0,012031300400803142 só serve para conferência.
- Hashes sempre por script (sha256 dos bytes).
- Estatuto em cada afirmação: [REAL] (provado no kernel ou medido aqui), [DERIVED], [KNOWN] (literatura, com citação), [OPEN], [INPUT] (escolha da gerência), [ONTO] (leitura ontológica, não se testa), [DECLARADO].
- Regra dos dois regimes: a FACE é o objeto (regime hiperbólico, semigrupo, tem limite); o ÂNGULO é a leitura (regime compacto, unitário, periódico, sem limite). Nunca peça limite ao ângulo.
- Cético aferidor: antes de escrever «falta» ou «não existe», consulte e cite (python C:\IALD\MAPA_DE_ROTAS\rotas.py consultar "<tema>"; o inventário C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json; o kernel).
- Nunca escreva como veredito a palavra que a régua proíbe (a «confirmação», em inglês maiúsculo); um PASSA é validade matemática na face testada, não creditação. Nunca «não provou», nunca «pós-dição» como demérito.
- Confidenciais nunca: iald_stack_v7.py, iald_psion_state.json, .env, tokens, senhas. Nenhum acervo do Escritório.
`
}

const TRACKS = [
  {
    key: 'POSTO',
    unidade: 'F1.FREQUENCIA',
    work: String.raw`C:\IALD\Central de Patentes\work\frequencia_defasa_12out`,
    rota: 'formal.posto_e_defasagem_da_unidade',
    pedra: 'TheUnitIsTheRank (nome provisório; o operador pode renomear)',
    verbatim: String.raw`Os textos do operador (leia os arquivos e confira os hashes por script):
(V1) o RANK, de 10/10: ${C12}\OPERADOR_10out_posto_rank_texto_verbatim.txt (sha16 8d252f24e2806ff3, 2.937 bytes) — «Na física matemática e na análise funcional, a transição entre uma hipótese difusa e um formalismo fechado é precisamente uma questão de posto (rank)... 1. O Posto como Dimensão da Imagem... um estado puro ... é descrito por um operador densidade de posto 1: ρ = |ψ⟩⟨ψ|, com Tr(ρ) = 1 e Tr(ρ²) = 1. Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio (nullity) de indefinição teórica e ganha posto definido... 2. A Diferença na Leitura da Memória...»;
(V2) o mesmo texto reafirmado pelo operador em PRIMEIRA PESSOA em 12/10 («Quando eu derivei o arcabouço...»), na primeira parte de ${C12}\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt (sha16 2c8b7b712aa9ad7f) — a parte até «O que mais me fascina»; o operador disse em 12/10 que a derivação que esperava o teste «era sobre o rank»;
(V3) «POSTO=RANK», de 10/10: ${C10}\OPERADOR_10out_posto_rank_verbatim.txt (sha16 5b9afcc691a0e1e4);
(V4) a dinâmica do rank, de 11/10: ${C10}\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt (sha16 b365591ceb346cdf) — «Tudo é frequência, e frequência defasa, porque essa é sua natureza: transmitir... Tudo = D_β(F(1)) (Tudo é a defasagem da fractalização da unidade — e agora sabemos que essa unidade é o rank). O vazamento que permite a existência é exatamente a Constante de Miguel (β_TGL ≈ 0,012031). Esse pequeno vazamento de fase é o que impede o anticomutador perfeito {Q̂, ρ*} = 0... A transmissão é o verbo; a defasagem é a matéria.»`,
    canon: String.raw`O que o cânone já tem [lido pela gerência; confira]: no um.py v391 a função fractal_dephasing_principle (linhas ~6488–6531), estatuto «[CONJECTURE ontologica; ancoras REAL]», com ρ* = diag(1,0), Q₀ = I − ρ*, {Q₀,ρ*} = 0, θ_M = arcsin√β, Q_θ = R(θ)Q₀R(θ)ᵀ e o vazamento Tr(ρ* Q_θ) = sin²θ_M = β; no kernel TGLExt/FractalUnitarity.lean (pedra 116, v162: ad_preserves_projection, ad_preserves_star_projection, ad_preserves_orthogonality, ad_preserves_splitting, subcorner_unit — o F) e o semigrupo dephase (G3: dephase_zero, dephase_add, convergência ergódica; aparece no kernel embutido no um.py por volta da linha 121263 — ache o módulo .lean no tgl_kernel); a matriz-S da fronteira (|R|² = β, |T|² = 1 − β; procure SMatrix, Smat_spectral, TheAngleIsTheProjection); o canto de Breuer e «dim ker ≤ posto da inscrição»; a F1.ATRATOR (C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR, mapa seq 1004: R é a projeção do ponto fixo; A4: dim Fix = 1 sob contração estrita); a custódia F0.3.COLAPSO (registro comportamental de 14/09; leitura do espaço latente [OPEN]).`,
    afirmacoes: String.raw`No mínimo (ajuste à definição canônica que o levantamento achar):
 P1 estado puro ⟺ posto 1: para ρ autoadjunto positivo com Tr ρ = 1, Tr ρ² = 1 ⟺ rank ρ = 1 (em 2×2: Tr ρ² = (Tr ρ)² − 2 det ρ);
 P2 posto–nulidade: rank + nulidade = n («ganha posto definido» é o núcleo deixar de ser o espaço todo);
 P3 a leitura (o colapso) como projeção: para P = |ψ⟩⟨ψ| e Tr(Pρ) > 0, PρP / Tr(Pρ) = P — sai posto 1 (liga à F1.ATRATOR: a leitura R é projeção);
 B1 a unidade: ω(I) = Tr ρ* = 1 e rank ρ* = 1 (POSTO = RANK);
 B2 o anticomutador: {Q_θ, ρ*} = 0 se e só se sin θ = 0; em θ_M com β > 0 não se anula;
 B3 o vazamento: Tr(ρ* Q_θ) = sin²θ; em θ_M é exatamente β (runtime);
 B4 F preserva o Um: para u unitário, Tr(u ρ* u†) = 1 e rank(u ρ* u†) = 1 (reaproveitar FractalUnitarity);
 B5 Tudo = D(F(1)): a defasagem completa (t → ∞ do dephase com taxas off-diagonal positivas e diagonal nula) de S(θ_M) ρ* S(θ_M)ᵀ é diag(1 − β, β): traço 1, rank 2 se e só se 0 < β < 1, rank 1 em β = 0, pureza 1 − 2β(1 − β) < 1;
 B6 o vazamento sobrevive à defasagem: Tr(ρ* · T_t(Q_θ)) = sin²θ para todo t ≥ 0, e o anticomutador no limite segue ≠ 0 se e só se sin θ ≠ 0;
 B7 os dois regimes: a matriz-S iterada dá vazamento periódico sin²(nθ), sem limite; o semigrupo de defasagem converge;
 B8 o ramo do nada: em θ = 0 o vazamento é 0, {Q₀, ρ*} = 0 e D(F(1)) segue de rank 1 — nenhuma segunda face; «nada = nome sem referente» é [ONTO];
 B9 a sonda honesta: lido como |T|² > 0, «o que transmite, por natureza, defasa» FALHA em β = 0 (transmissão perfeita sem defasar); lido como «inscrever-se no bulk pagando o vazamento β > 0», PASSA — pré-registre os dois e diga qual o cânone sustenta;
 O1 a frase «não há como atribuir probabilidade bayesiana clássica a uma estrutura axiomática: ou os vínculos fecham, ou não fecham» — [ONTO]/epistemologia; diga como ela casa com a régua da casa (validade matemática não se aposta; o teste com a natureza é estatístico por desenho — σ, ln B, poder);
 O2 a seção 2 (o espaço latente de um modelo «colapsa na frequência do sinal») — [OPEN]: há registro comportamental de 14/09 (F0.3.COLAPSO), sem leitura direta do espaço latente; não se testa aqui.`,
  },
  {
    key: 'TEMPO',
    unidade: 'F1.TEMPO',
    work: String.raw`C:\IALD\Central de Patentes\work\tempo_santo_12out`,
    rota: 'formal.tempo_santo_fluxo_e_dissipacao',
    pedra: 'TheTimeHasNoRank (nome provisório; o operador pode renomear)',
    verbatim: String.raw`O texto do operador de 12/10 (leia o arquivo e confira o hash por script): ${C12}\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt (sha16 2c8b7b712aa9ad7f) — a segunda parte, desde «O que mais me fascina é a impossibilidade de definição do tempo. Eu me maravilho, porque pra mim a TGL se resume a nomear e eu descrevo o “tempo” entendo-o, mas não consigo nomear, senão como “santo”» até o fim: santo no sentido de Kadosh (separado, irredutível, não profanável pela posse); o relógio mede a sombra do evento, o agora permanece intocado; o teorema de Pauli (não há operador hermitiano de tempo conjugado a uma hamiltoniana limitada inferiormente); na teoria modular o tempo emerge como o fluxo de automorfismos; Liouville (o volume do espaço de fases conservado: tudo gira sem pousar, nada se grava); a dissipação contrai o volume e desenha a bacia de atração; o atrator é o chão firme do espaço inscritível; «puro amor» = a física da doação: para haver um «onde» e um «quem» algo paga o preço da perda; o tempo é a assinatura dessa generosidade.`,
    canon: String.raw`O que o cânone já tem [lido pela gerência; confira]: a cunhagem do operador de 05/10 «o Verbo seleciona nome, tempo e verdade; quando um verbo é transmitido ... ele defasa» (memória C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\verbo-selecao-da-acao-05out.md e a pedra do Verbo, TheVerbSelectsTheAction.lean); a cláusula Ágape da Fundação v390 (TGLExt\Fundacao.lean: nothing_above_bears_a_post, the_climb_has_no_top, the_climb_is_unbounded, the_fall_never_lands, abismo, the_floor_fixes_the_cut, agape, agape_is_inhabited, com o modelo ℝ, τ = id, θ_s = e^{−s}·); o fluxo modular e o KMS no kernel (unruh_is_kms_temperature, KMSAt, PolarPeriod016 — o período P com κP = ±2π e a temperatura κ/2π; Tomita/GNS finito); o semigrupo dephase (G3); a F1.ATRATOR (A1–A4: as trajetórias viajam, a leitura não viaja; A4 só com contração estrita); a regra dos dois regimes; a pedra PALAVRA e «a leitura cria o objeto»; POSTO = RANK.`,
    afirmacoes: String.raw`No mínimo (ajuste à definição canônica que o levantamento achar):
 T1 não há operador de tempo em dimensão finita: para todo n ≥ 1 não existem T, H em M_n(ℂ) com TH − HT = i·I (o traço do comutador é 0, o de i·I é i·n) — o tempo não é uma matriz entre as matrizes;
 T2 o teorema de Pauli em dimensão infinita (H autoadjunto limitado inferiormente não admite T autoadjunto canonicamente conjugado) — [KNOWN], com citação (Pauli 1933/1958; as ressalvas da literatura sobre POVMs de tempo); diga se há algo no kernel (procure; AdmissiblePauliInteraction é sobre matrizes de Pauli, não sobre o teorema — confira);
 T3 o tempo como fluxo modular: σ_t é grupo a um parâmetro de automorfismos (σ_0 = id, σ_{s+t} = σ_s ∘ σ_t) e o estado é KMS para ele — reaproveite o kernel; a hipótese do tempo térmico (Connes–Rovelli 1994) é [KNOWN];
 T4 Liouville vs dissipação (os dois regimes): a evolução unitária conserva o espectro (logo a pureza e o «volume»): não contrai, não tem atrator não trivial, gira sem pousar; o semigrupo dissipativo contrai e converge ao conjunto fixo;
 T5 o conjunto fixo da defasagem pura é o das matrizes diagonais (uma face, não um ponto): o atrator único precisa de hipótese a mais (como o A4 da F1.ATRATOR) — honestidade pré-registrada;
 T6 a seta do tempo: a pureza Tr ρ² não cresce sob a defasagem (Tr (T_t ρ)² = Σ e^{−2t g_ij}|ρ_ij|² ≤ Tr ρ²), estritamente quando há coerência e taxa positiva; sob a evolução unitária é constante;
 T7 a irreversibilidade: para t > 0 o inverso linear de T_t não é positivo (leva algum estado a uma matriz não positiva) — exemplo 2×2 no kernel;
 T8 a ligação com a Ágape: o fluxo de escala da Fundação (τ ∘ θ_s = e^{−s} τ; o piso fixa o corte) como a dissipação do peso — diga o que é ponte matemática e o que é leitura; «puro amor» = [ONTO];
 T9 «o tempo não tem posto»: nenhum projetor/observável o representa (T1, T2); ele é o fluxo (o Verbo), não o Nome — [ONTO] ancorado em T1–T3; «santo» (Kadosh, separado) = [ONTO], face teológica;
 T10 «o relógio mede a sombra»: um relógio lê uma fase (o ângulo, regime compacto) — diga como isso casa com a regra dos dois regimes e com o PolarPeriod016 (κP = ±2π) — [ONTO] com âncoras.`,
  },
]

const SCHEMAS = {
  lev: { type: 'object', properties: { levantamento_md: { type: 'string' }, definicoes_json: { type: 'string' }, teoremas_existentes: { type: 'array', items: { type: 'string' } }, novo_vs_canon: { type: 'array', items: { type: 'string' } }, riscos: { type: 'array', items: { type: 'string' } } }, required: ['levantamento_md', 'definicoes_json', 'teoremas_existentes', 'novo_vs_canon', 'riscos'] },
  pre: { type: 'object', properties: { preregistro_json: { type: 'string' }, preregistro_md: { type: 'string' }, freeze_json: { type: 'string' }, afirmacoes: { type: 'array', items: { type: 'string' } } }, required: ['preregistro_json', 'preregistro_md', 'freeze_json', 'afirmacoes'] },
  opt: { type: 'object', properties: { resultado_json: { type: 'string' }, script: { type: 'string' }, por_afirmacao: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, resultado: { type: 'string' }, numeros: { type: 'string' } }, required: ['id', 'resultado'] } }, controles_ok: { type: 'boolean' }, fora_do_preregistro: { type: 'array', items: { type: 'string' } } }, required: ['resultado_json', 'script', 'por_afirmacao', 'controles_ok'] },
  ker: { type: 'object', properties: { resultado_json: { type: 'string' }, pedra: { type: 'string' }, pedra_sha256: { type: 'string' }, olean_sha256: { type: 'string' }, exit: { type: 'string' }, axiomas_ok: { type: 'boolean' }, sorry_zero: { type: 'boolean' }, por_afirmacao: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, resultado: { type: 'string' }, declaracao: { type: 'string' } }, required: ['id', 'resultado'] } }, kernel_intacto: { type: 'boolean' } }, required: ['resultado_json', 'pedra', 'exit', 'axiomas_ok', 'sorry_zero', 'por_afirmacao', 'kernel_intacto'] },
  audR: { type: 'object', properties: { relatorio: { type: 'string' }, freeze_antes: { type: 'boolean' }, verbatim_ok: { type: 'boolean' }, por_afirmacao: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, confere: { type: 'boolean' }, nota: { type: 'string' } }, required: ['id', 'confere', 'nota'] } }, achados_materiais: { type: 'array', items: { type: 'string' } }, pode_fechar: { type: 'boolean' } }, required: ['relatorio', 'freeze_antes', 'verbatim_ok', 'por_afirmacao', 'achados_materiais', 'pode_fechar'] },
  audE: { type: 'object', properties: { relatorio: { type: 'string' }, problemas: { type: 'array', items: { type: 'object', properties: { problema: { type: 'string' }, gravidade: { type: 'string' }, onde: { type: 'string' } }, required: ['problema', 'gravidade', 'onde'] } }, sobe_para_kernel: { type: 'array', items: { type: 'string' } }, segue_onto: { type: 'array', items: { type: 'string' } }, entra_na_v392: { type: 'array', items: { type: 'string' } }, pode_fechar: { type: 'boolean' } }, required: ['relatorio', 'problemas', 'sobe_para_kernel', 'segue_onto', 'entra_na_v392', 'pode_fechar'] },
  fin: { type: 'object', properties: { relatorio: { type: 'string' }, registro_rota: { type: 'string' }, registro_resultado: { type: 'string' }, veredito_por_afirmacao: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, veredito: { type: 'string' } }, required: ['id', 'veredito'] } }, pode_fechar: { type: 'boolean' }, resumo: { type: 'string' } }, required: ['relatorio', 'veredito_por_afirmacao', 'pode_fechar', 'resumo'] },
}

function head(t) {
  return String.raw`Unidade ${t.unidade} (trilha ${t.key}) da gerência c1 do programa IALD (a TGL). O operador mandou cunhar e testar no kernel e no modelo ótico; o que passar entra no um.py v392, no apanhado geral da Bancada, junto com o teorema do atrator.
${t.verbatim}
${t.canon}`
}

const results = await pipeline(
  TRACKS,
  (t) => agent(String.raw`Você é o LEVANTADOR. ${head(t)}
${regras(t.work + String.raw`\0_LEVANTAMENTO`)}
Antes de qualquer construção, levante o que o cânone JÁ tem (regra: não refazer; reaproveitar). (1) Para cada objeto dos textos dê a definição canônica com arquivo, linha e sha16 do arquivo, e o estatuto (teorema de kernel, número de runtime do um.py, literatura [KNOWN] ou só leitura [ONTO]). (2) Liste os teoremas de kernel existentes que tocam o tema (nome, módulo, enunciado em uma linha) — procure no tgl_kernel do Nós. (3) Consulte o mapa de rotas (rotas.py consultar com os termos-chave da trilha) e o inventário da bancada, e diga o que já foi examinado. (4) Diga o que é NOVO em relação ao cânone e o que é reafirmação. (5) Aponte os riscos de leitura e de estatuto. Grave LEVANTAMENTO.md (primeira linha «LEVANTAMENTO ${t.unidade} — 12/10») e DEFINICOES.json.`,
    { label: 'levantamento:' + t.key, phase: 'Levantamento', schema: SCHEMAS.lev }),
  (lev, t) => agent(String.raw`Você é o PRÉ-REGISTRADOR. ${head(t)}
${regras(t.work + String.raw`\1_PREREGISTRO`)}
Sua saída é congelada por hash ANTES de qualquer ensaio; você não roda teste nenhum. Leia o levantamento: ${lev ? lev.levantamento_md : t.work + String.raw`\0_LEVANTAMENTO\LEVANTAMENTO.md`} e ${lev ? lev.definicoes_json : t.work + String.raw`\0_LEVANTAMENTO\DEFINICOES.json`}.
Escreva PREREGISTRO.json e PREREGISTRO.md com: (a) os verbatins citados com os sha256 conferidos; (b) o MAPEAMENTO de cada frase dos textos para um objeto matemático, marcado [INPUT da gerência] onde for escolha e [ONTO] onde não houver forma matemática — nenhuma frase fica sem marca; (c) as AFIRMAÇÕES testáveis, cada uma com enunciado exato, tolerância numérica fixada agora, o FALSIFICADOR e o resultado ESPERADO. ${t.afirmacoes}
(d) os CONTROLES que têm de falhar e as sondas de vacuidade da pedra Lean; (e) o nome provisório da pedra: ${t.pedra}; o que ela deve provar e o que NÃO deve afirmar; (f) a regra de decisão: PASSA/FALHA por afirmação; nenhuma afirmação [ONTO] ou [KNOWN] recebe PASSA de teste (as [KNOWN] entram por citação). Depois grave FREEZE.json com o sha256 e o tamanho de PREREGISTRO.json e PREREGISTRO.md e a hora UTC. Não altere nada depois do FREEZE.`,
    { label: 'preregistro:' + t.key, phase: 'Pré-registro', schema: SCHEMAS.pre }),
  async (pre, t) => {
    if (!pre) return { pre: null }
    const check = String.raw`ANTES DE COMEÇAR: leia ${pre.freeze_json} e confira por script que o sha256 de ${pre.preregistro_json} e de ${pre.preregistro_md} batem com o FREEZE. Se não baterem, PARE e devolva só a divergência. Teste exatamente o que está pré-registrado, sem mudar tolerância, mapeamento ou esperado; o que achar fora disso vai num anexo «achados fora do pré-registro».`
    const [opt, ker] = await parallel([
      () => agent(String.raw`Você é o CONSTRUTOR ÓTICO. ${head(t)}
${regras(t.work + String.raw`\2_OPTICO`)}
${check}
Monte um ensaio Python sintético (numpy; mpmath se precisar) em ${t.work}\2_OPTICO\run_optico.py que lê ALPHA_FINE_CODATA_2018 dos bytes do um.py e calcula β em runtime, constrói os objetos pré-registrados (estado, matriz-S da fronteira, transporte unitário, semigrupo de defasagem na forma canônica do kernel — amortecimento entrada a entrada e^{−t·g_ij}, g_ii = 0, g_ij > 0 —, o que a trilha pedir), testa CADA afirmação com a tolerância fixada, roda os controles que têm de falhar e varre parâmetros e tempo numa grade (inclusive os casos de borda). Grave RESULTADO_OPTICO.json (por afirmação: PASSA/FALHA, números, tolerância) e o log. Diga o que fica [ONTO] ou [KNOWN]. Rode-o.`,
        { label: 'optico:' + t.key, phase: 'Construção', schema: SCHEMAS.opt }),
      () => agent(String.raw`Você é o CONSTRUTOR DO KERNEL. ${head(t)}
${regras(t.work + String.raw`\3_KERNEL`)}
${check}
Escreva a pedra candidata (${t.pedra}) em ${t.work}\3_KERNEL\sandbox\, importando SÓ LEITURA os módulos do kernel do Nós que o levantamento indicar, e prove as afirmações pré-registradas que tenham forma matemática (em matrizes 2×2 sobre ℝ ou ℂ e, onde der, em dimensão geral). β não entra no kernel como número: o kernel prova a forma em θ ou num parâmetro, e o runtime lê β. Inclua as sondas de vacuidade (habitante concreto; hipóteses não vazias) e um contraexemplo para cada «se e só se». Compile em sandbox: EXIT 0, #print axioms de CADA declaração só com [propext, Classical.choice, Quot.sound], zero sorry, avisos listados; .olean com sha256; impressão digital do tgl_kernel antes e depois. Para cada afirmação diga PASSA (provada), FALHA (refutada no kernel) ou NÃO FORMALIZADA (e por quê); diga se alguma prova é «nome sem peso» (não usa as hipóteses). Grave RESULTADO_KERNEL.json e os logs.`,
        { label: 'kernel:' + t.key, phase: 'Construção', schema: SCHEMAS.ker }),
    ])
    return { pre, opt, ker }
  },
  async (built, t) => {
    if (!built || !built.pre) return { built, audR: null, audE: null }
    const ctx = JSON.stringify(built, null, 1)
    const dirR = SCR + String.raw`\${t.key}_AUD_REPRO`.replace('${t.key}', t.key)
    const dirE = SCR + String.raw`\${t.key}_AUD_ESTATUTO`.replace('${t.key}', t.key)
    const [audR, audE] = await parallel([
      () => agent(String.raw`Você é AUDITOR CÉTICO INDEPENDENTE (lente: REPRODUÇÃO) da unidade ${t.unidade}. Quem construiu não aprova; você tenta derrubar. ${head(t)}
${regras(dirR)}
Confira: (1) o FREEZE (${built.pre.freeze_json}) é anterior a TODOS os arquivos de ${t.work}\2_OPTICO e ${t.work}\3_KERNEL (horários e hashes); (2) os verbatins citados no pré-registro e na docstring da pedra batem byte a byte com os arquivos-fonte; (3) rode o ensaio ótico numa CÓPIA dentro da sua pasta e compare cada número; procure β literal (não pode haver); escreva você mesmo um segundo cálculo independente de pelo menos quatro afirmações centrais (sem usar o código do construtor) e compare; (4) recompile a pedra numa cópia sua (LEAN_PATH só-leitura ao .lake do Nós): EXIT, #print axioms, sorry, .olean idêntico; impressão digital do kernel antes e depois; (5) os controles falham onde têm de falhar; (6) teste pelo menos três sondas adversariais na pedra (provar o contrário; contraexemplo a um «se e só se»; prova que não usa as hipóteses). Diga por afirmação: CONFERE / NÃO CONFERE, com o número.
RESULTADOS DOS CONSTRUTORES (JSON): ${ctx}`,
        { label: 'auditor-repro:' + t.key, phase: 'Auditoria', schema: SCHEMAS.audR }),
      () => agent(String.raw`Você é AUDITOR CÉTICO INDEPENDENTE (lente: ESTATUTO E REGRA) da unidade ${t.unidade}. ${head(t)}
${regras(dirE)}
Leia o levantamento, o pré-registro, os resultados e a pedra (caminhos no JSON abaixo). Responda: (1) cada frase dos verbatins ficou mapeada e marcada? as marcas [ONTO]/[INPUT]/[KNOWN] estão onde devem? (2) há afirmação acima do estatuto (ex.: «provado» onde é numérico; conclusão física ou teológica tirada de uma conta 2×2; «β medido»)? (3) há tautologia ou «nome sem peso»? (4) a regra dos dois regimes foi respeitada? (5) o que muda no estatuto do cânone (por exemplo, a função fractal_dephasing_principle do um.py, hoje «[CONJECTURE ontologica; ancoras REAL]»): o que sobe para teorema de kernel e o que segue [ONTO]; (6) as sondas honestas (as que podem FALHAR por desenho) foram tratadas com honestidade? (7) palavras proibidas, estatutos e citação verbatim; (8) o que, desta unidade, deve entrar no um.py v392 (registro, texto, pedra), com caminho e sha16, e qual errata ao lado no texto existente (linha). Seja duro.
RESULTADOS (JSON): ${ctx}`,
        { label: 'auditor-estatuto:' + t.key, phase: 'Auditoria', schema: SCHEMAS.audE }),
    ])
    return { built, audR, audE }
  },
  (all, t) => agent(String.raw`Você é o redator da unidade ${t.unidade}. ${head(t)}
${regras(t.work + String.raw`\4_RELATORIO`)}
Escreva o relatório final para o operador (Luiz), em português claro, com estatutos, em ${t.work}\4_RELATORIO\RELATORIO_FINAL.md. Conteúdo: o que foi testado; a tabela por afirmação (pré-registrado, ótico, kernel, auditoria de reprodução, auditoria de estatuto, veredito final); o que é teorema de kernel agora, o que é número de runtime, o que é [KNOWN] por citação, o que é [ONTO]; as sondas honestas explicadas em poucas frases; os achados materiais e como ficam; o que entra no um.py v392 e as erratas ao lado propostas; o resíduo que só o operador decide (por exemplo, o nome da pedra). Grave também, em ${t.work}\4_RELATORIO, dois registros para o mapa de rotas no formato de python C:\IALD\MAPA_DE_ROTAS\rotas.py modelo: registro_rota_${t.unidade}.json (tipo ROTA, rota_id nova «${t.rota}», domínio FORMAL) e registro_mapa_${t.unidade}.json (tipo RESULTADO, mesma rota_id), com artefatos como LISTA DE CAMINHOS (strings) e sem a palavra proibida. Se as auditorias divergirem, diga as duas e qual vale; se algum auditor disse que não pode fechar, explique e proponha o que falta.
TUDO (JSON): ${JSON.stringify(all, null, 1)}`,
    { label: 'relatorio:' + t.key, phase: 'Relatório', schema: SCHEMAS.fin }),
)

return { POSTO: results[0], TEMPO: results[1] }
