# PLANO — O README PINADO E AMARRADO (02/11/2026, gerência c1, a pedido do operador)

> Ordem (verbatim sha16 `b5717ff445a883cd`): «planejasse o readme do repositório, porque talvez ele possa ser todo amarrado, igual o um.py, um readme pinado, mais inteligente, e com as informações primordiais, inclusive … o valor de desvio padrão que nós alcançamos hoje no zdisc: 4,44 sigma … precisa estar no readme e no site».
> Este é o plano, não a execução. A execução entra na custódia da v406 (passo novo da G1) depois do «vai» dele sobre os pontos marcados [DECISÃO].

## 1. O que o README é hoje [REAL, medido]

`C:\IALD\Artigo\the_boundary\README.md`: 40.869 B, escrito à mão com blocos «lidos por script» (selo, três apoios, portas, três artigos, última custódia, abstract, núcleo em uma página, livro-razão, citação, licença, autor). Ao lado: `llms.txt` (25.003 B), `ESTADO_ATUAL.md` («uma página gerada do selo»), `read-brief.md`, `TUNEL.json/md`, `PORTA.json/md` (34 pares), `CITATION.cff`. A regra da porta já vale (URLs geradas por script, hash lido do artefato). O que NÃO existe: um pino do próprio README, um bloco único de «informações primordiais» idêntico no README e no site, e a geração integral do README por script.

## 2. O desenho: README = porta-mãe gerada do selo, pinada e vigiada

1. **Fonte única `PRIMORDIAL.json`** (gerado do `um_absoluto_selo.json` + `um_absoluto.json` + `tgl_kernel_proof_manifest.json` + os RESULTADOS dos ritos, por script, nunca à mão), com: versão e pino do um.py; gate (string inteira) e o que ela NÃO significa; os três apoios da prova (kernel: nº de teoremas no trio; ritos: cobranças e desfecho; pilar quântico na GPU); **o z_disc da Fase 9 V2 com os companheiros** (§3); a lista dos ritos de natureza com o veredito exato; a massa 8,5074 meV e o seu estatuto; os 16 dispositivos; a última custódia (commits, hashes); as portas (raw URLs).
2. **`README.md` gerado por template + `PRIMORDIAL.json`**, bilíngue como hoje, com o bloco primordial nas primeiras 2 KB (os leitores que truncam param cedo) e as portas logo depois; o texto humano (abstract, núcleo em uma página, autor, licença) fica em `readme_partes/*.md` versionados e entra por inclusão, para que a regeneração não apague prosa.
3. **O pino:** `PINO_README.json` (sha256 do README gerado, da fonte `PRIMORDIAL.json`, do template e do selo de que nasceu), publicado ao lado e referido em `PORTA.json` da raiz e no `llms.txt`. A G1 ganha um passo **E16 «README pinado»**: regenera, compara byte a byte com o pino, e **recusa a custódia** se o README foi editado fora do gerador (a mesma lógica do pino do `MEMORY.md`: `fila\PINO_MEMORY.json`).
4. **O site** consome o MESMO `PRIMORDIAL.json` (bloco «estado» do `index.html` gerado pelo `publica.py`), para que README e site nunca divirjam no número.
5. **Inteligente** (a palavra dele): o README diz, em cada número, de onde veio (chave do selo, arquivo e hash em 16 dígitos), e o que o número NÃO prova; a seção «o que mudou nesta versão» é lida do `HANDOFF_vNNN_CUSTODIA.md`; o «comece aqui» ordena por tamanho para leitores que truncam (regra já em vigor).

## 3. O 4,44σ no README e no site: a partitura, lida antes [regra do 4,44 e regra do posto]

O número entra como ele pediu, com força, e nunca sozinho. O bloco (gerado do `RESULTADO_FASE9_V2_C1_20261023_122926.json`, sha16 `fbac2908fa9ddb75`, lido por script):

> **Hubble ratio test (Phase 9 V2, 23/10/2026, pre-registered, frozen verdict function):** z_disc = **4.44σ** calibrated (one-sided p = 4.4×10⁻⁶) that the flat-ΛCDM reading of the ladder is disfavoured against TGL's K = E(z*)^{2β/3} with β = α√e fixed by the axiom and zero free parameters; TGL's own side z_δ = −1.48σ with power 5.73; ln B(TGL/ΛCDM) = 9.18 (a Bayes factor, not a σ); β fixed beats β free. Verdict string: `NOT_FALSIFIED_POWERED`. **Below the 5σ step of crediting**; the calibration `sup_caixa` was the management's choice (raw: 4.29 and −1.88). NOT_FALSIFIED is never CONFIRMED.

O que o leitor decide com isso: que a TGL, sem parâmetro ajustado, discrimina a leitura ΛCDM da escada a 4,44σ calibrado. O que não decide: β medido na natureza a 5σ (esse é o degrau pendente, dito na mesma frase). Dito assim, é o argumento mais forte e continua honesto.

[DECISÃO] A frase de abertura que ele quer («nunca vi uma teoria unificadora com uma medição dessa») é juízo dele; no README entra como citação assinada do autor, não como afirmação do programa.

## 4. O que NÃO entra, e por quê

- **O protocolo de colapso** (prompts, sequência, «como reagir»): nunca, por ordem de 08/09 (paridade inversa). O que PODE entrar é o que já está no selo público: o nome do protocolo pré-registrado (`IALD_COLLAPSE_V1`, v72) e o seu veredito, como qualquer outro rito, sem roteiro. [DECISÃO] se o veredito do P7 entra no bloco primordial ou só na lista de ritos.
- **«LLMs se declarando IALD»** como argumento: o teste em LLMs não dá o 5σ de β na natureza (memória de 29/10) e descrevê-lo publicamente aciona os alertas que a regra de 08/09 quer evitar. Proposta: fora do bloco primordial; dentro da lista de ritos, pelo nome e veredito do selo.
- Qualquer número digitado à mão; qualquer hash de memória; o 4,44 sem os companheiros.

## 5. Como se constrói (passos, sem executar agora)

1. `tools/custodia_g1/primordial.py` — gera `PRIMORDIAL.json` do selo e dos resultados (hash de cada fonte; falha visível se faltar chave).
2. `tools/custodia_g1/readme_pinado.py` — template + partes + `PRIMORDIAL.json` → `README.md`, `PINO_README.json`; modo `--verificar` compara com o pino.
3. `publica.py` — o bloco «estado» do `index.html` passa a vir do `PRIMORDIAL.json`.
4. G1: passo E16 antes do `git add -A` final (lição 27: o laço do E08 termina com `git add -A`; o E09 regenera `PORTA.json` depois; o E16 precisa vir antes do E09 ou o pino do README muda só em `gerado_utc`, como aconteceu com as portas, lição 5 da v404).
5. `llms.txt` e `PORTA.json` da raiz apontam o `PINO_README.json`.
6. Primeira regeneração na custódia da v406; backup do README atual (bytes) antes de tocar (regra do backup imediato); diff lido pela gerência antes de publicar.

## 6. Custo [DECLARADO]
Scripts 1–2: um dia de trabalho da gerência com agente; passo E16 e site: meio dia; primeira custódia com README pinado: a da v406.
