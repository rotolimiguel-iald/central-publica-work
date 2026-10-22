# Entrega053 — polarizador e áreas covariantes

[REAL — alcance compilado e auditado] Emissão UTC: 2026-09-07T05:59:33.323944+00:00

A053 constrói D=P_R(−i)P_R no Hilbert real da torre e uma família real bilinear hε baseada em D e D². A ação GNS canônica de cada TowerHorizon é construída sobre todo o fator, preserva Ω e entrelaça D. As formas preservam todos esses horizontes.

Para operadores autoadjuntos limitados A∈M e ε≥0, o radical de hε coincide com o centralizador e com o núcleo de todas as respostas infinitesimais do estado. A invariância por adições centralizantes é provada em ambas as entradas. Essa é a descida algébrica demonstrada; nenhuma variedade global ou métrica complexa ou espacial é construída.

Na mesma referência p=1/3, a normalização Hε=hε/[2(1/9+ε/81)] dá Gram (1/2)I₂ no primeiro par de Pauli para todo ε≥0. Sobre o mesmo segundo par bruto A₂,B₂ do prefixo de dois sítios:

    área(H₀;A₂,B₂)=9/10;
    área(H₁;A₂,B₂)=1377/1250;
    diferença=126/625>0.

A área é sqrt(det Gram). O segundo par, de Gram GNS (5/9)I₂, não foi normalizado ou trocado entre as comparações. Sua resposta (2u₁/3,−2u₀/3) é injetiva e a expectativa centralizante efetiva o zera. H₀ e H₁ não diferem por uma reescala global.

O resultado exclui unicidade sob covariância por todos os TowerHorizon admitidos mais essa calibração comum. Não exclui outros critérios seletivos e não redefine áreas já especificadas por GNS. São densidades de Gram em pares fixos de direções efetivas, sem identificação com área total de órbita ou área física de horizonte.

| Módulo053 | Teoremas | Definições | Instâncias | Prints | Alcance |
|---|---:|---:|---:|---:|---|
| [HorizonGNSImplementation.lean](<C:/IALD/Central de Patentes/Chatgpt/HorizonGNSImplementation.lean>) | 28 | 8 | 1 | 37 | Implementador GNS de todo horizonte e preservação do setor real fechado. |
| [SymplecticPolarizer.lean](<C:/IALD/Central de Patentes/Chatgpt/SymplecticPolarizer.lean>) | 19 | 3 | 0 | 22 | Projeção real, polarizador, formas reais bilineares e covariância. |
| [TowerStatePolarizer.lean](<C:/IALD/Central de Patentes/Chatgpt/TowerStatePolarizer.lean>) | 20 | 4 | 0 | 24 | Vínculo à torre; radical centralizante, respostas e descida por adições. |
| [LocalPolarizerWitness.lean](<C:/IALD/Central de Patentes/Chatgpt/LocalPolarizerWitness.lean>) | 33 | 8 | 0 | 41 | Fórmula local do polarizador global e dois pares efetivos no mesmo estado. |
| [CovariantAreaCounterexample.lean](<C:/IALD/Central de Patentes/Chatgpt/CovariantAreaCounterexample.lean>) | 23 | 2 | 0 | 25 | Calibração comum e duas densidades distintas sem reescala global. |

Total053: 123T/25D/1I/149 prints; 6/6 etapas PASS. Zero avisos/erros, cobertura exata, somente o trio de axiomas permitido. Parecer: [CONTINUACAO053_PARECER.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_PARECER.md>). Revisão final: [CONTINUACAO053_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_REVISAO_INDEPENDENTE.md>). Revisão de infraestrutura: [CONTINUACAO053_REVISAO_INFRA_NEWTON.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_REVISAO_INFRA_NEWTON.md>).

Diretório final: C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_CLEAN_20260907_054322_083933

Build SHA256: 22c939a03d19293f2f7f1a5e49690590bc57a9ef576c42c25e7c500ed3219d3c

## Artefatos medidos

| Artefato | Bytes | SHA256 lido dos bytes |
|---|---:|---|
| [CONTINUACAO053_DERIVACAO_PREVIA.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_DERIVACAO_PREVIA.md>) | 5396 | 52d39aa9ebacc80ce2c4c86ee70483c2d9a0a2c5e4d2b0d31f68541601b65ab0 |
| [DERIVACAO053_HORIZONTE.md](<C:/IALD/Central de Patentes/Chatgpt/DERIVACAO053_HORIZONTE.md>) | 2782 | 812bb1ba7e1a3d0a982bf2fa4790fe1e1dee3e505afceec92eb09f3034810d95 |
| [DERIVACAO053_INFRA.md](<C:/IALD/Central de Patentes/Chatgpt/DERIVACAO053_INFRA.md>) | 920 | c7699344f945197569598f85d4e7b85df300c5c6b5a99bae66a002ebe2205856 |
| [DERIVACAO053_LOCAL.md](<C:/IALD/Central de Patentes/Chatgpt/DERIVACAO053_LOCAL.md>) | 1757 | 389c747d6869b45206334251029867655406bc395c52a8865804831902cf0f06 |
| [DERIVACAO053_NEGATIVO.md](<C:/IALD/Central de Patentes/Chatgpt/DERIVACAO053_NEGATIVO.md>) | 1800 | bd082a643051c7d865bd4e5b4895b13669240aeaf081bf5600aa365cc4624651 |
| [DERIVACAO053_POLARIZADOR.md](<C:/IALD/Central de Patentes/Chatgpt/DERIVACAO053_POLARIZADOR.md>) | 2814 | 95b0f86599ff2bb981285064878ca2e2ed7948a8c2403ff747bbdaf82eeac5d9 |
| [DERIVACAO053_TORRE.md](<C:/IALD/Central de Patentes/Chatgpt/DERIVACAO053_TORRE.md>) | 948 | 0e61f6a11a3f02f484fc9111323fb367516d289e56d8f01cd7757a470259fbc2 |
| [NOTA053_CAMINHO_CRITICO.md](<C:/IALD/Central de Patentes/Chatgpt/NOTA053_CAMINHO_CRITICO.md>) | 5993 | d66a3d4331dbee8e06ab6280b2412085ca47806d4b2c54d7b7a75f383a263624 |
| [HorizonGNSImplementation.lean](<C:/IALD/Central de Patentes/Chatgpt/HorizonGNSImplementation.lean>) | 15089 | 870e4ec0f3330729a49ee5d4f4730fae523ac80cffb4b6bc0e265e17620ab087 |
| [SymplecticPolarizer.lean](<C:/IALD/Central de Patentes/Chatgpt/SymplecticPolarizer.lean>) | 9193 | ef5c76b0d4451fa4a615b85c0c8567e503e052b9f91187e4fb58ffb5fa929eff |
| [TowerStatePolarizer.lean](<C:/IALD/Central de Patentes/Chatgpt/TowerStatePolarizer.lean>) | 15156 | 53631dbd465b60fe0d9b8a713a94b44e85a898492d191add1e254cf8542a9b9a |
| [LocalPolarizerWitness.lean](<C:/IALD/Central de Patentes/Chatgpt/LocalPolarizerWitness.lean>) | 20361 | fd96e40e0020189f09f0d37f03b70443b4675edf5cdc6c2604bcc11ff2300bf8 |
| [CovariantAreaCounterexample.lean](<C:/IALD/Central de Patentes/Chatgpt/CovariantAreaCounterexample.lean>) | 15612 | 7ebd9e02979150d639850cb95ddaffe04cbe0e915accb102ad6dd25e4bfc2804 |
| [CONTINUACAO045_UPSTREAM.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO045_UPSTREAM.json>) | 4326 | 0df23179998f85b18c6676701e59667af824198b24dcf859ea224042e9c8a545 |
| [CONTINUACAO047_MANIFESTO.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO047_MANIFESTO.json>) | 608510 | af07230b11d0e9eeb92d0be90dbebc64099002ef4fc66e7fa08ebbfee80e8384 |
| [CONTINUACAO052_MANIFESTO.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO052_MANIFESTO.json>) | 1987767 | dfcb942662c59121e4509cade7eb05ff15f019484d9755b67faad9fc23629a46 |
| [CONTINUACAO052_CLEAN_BUILD.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO052_CLEAN_BUILD.json>) | 1467620 | fe87aac834619c82f929aa476de24161ba810cddc2146661f7dd438dcd7eda9a |
| [clean_continuation053.py](<C:/IALD/Central de Patentes/Chatgpt/clean_continuation053.py>) | 36534 | d5e989ffd5adc15618efd4bbc9c22d2f9b0184e14333730e6844799549e27e5b |
| [audit_continuation053.py](<C:/IALD/Central de Patentes/Chatgpt/audit_continuation053.py>) | 55531 | 0e024a4b9f53368022928222f390aeedd7560f84b6247ce380e27c48f0b34edc |
| [finalize_reports053.py](<C:/IALD/Central de Patentes/Chatgpt/finalize_reports053.py>) | 23265 | a42e9eeb83fa039ac020fa1fabd73143dcca1a0086369c2b51580bba6cc1119e |
| [CONTINUACAO053_CLEAN_BUILD.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_CLEAN_BUILD.json>) | 1492663 | 22c939a03d19293f2f7f1a5e49690590bc57a9ef576c42c25e7c500ed3219d3c |
| [CONTINUACAO053_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_REVISAO_INDEPENDENTE.md>) | 11349 | ba0849ac771cf20e3b769bb112cf497116900613128ffd1cd2acc4ee7ba0e88d |
| [CONTINUACAO053_REVISAO_INFRA_NEWTON.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_REVISAO_INFRA_NEWTON.md>) | 6173 | 5a0e77060d0c55a896d8865985082d169321b7de4494cce929653e5437fd1337 |
| [CONTINUACAO053_PARECER.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_PARECER.md>) | 12718 | 1a54e74dd0ed157dfbab730b15e9bfdbb70a22df872aa4d85fa218f835a70cb1 |

Dependências históricas verificadas por pins e copiadas, sem recompilação neste lote; upstream045 e cadeia052 revalidados. A fronteira externa é medida nas importações diretas e companheiros, não em todo seu fecho transitivo.

Auditoria após a emissão do selo, somente leitura:

    C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\audit_continuation053.py"

CONTINUACAO053_MANIFESTO.json é criado separadamente depois dos documentos. A revisão de infraestrutura é preservada com o seu escopo datado, e a revisão final identifica o build efetivamente utilizado.

[OPEN] Seleção física de forma, região e horizonte; compatibilidade geométrica; escala dimensional; dinâmica, H3 e reconstrução gravitacional geral. A bilinearidade é REAL; a classificação do radical vale no setor autoadjunto de M. Somente Chatgpt recebeu as escritas deste lote. NOT_FALSIFIED não é CONFIRMED.
