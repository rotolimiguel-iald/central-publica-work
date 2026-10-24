# PROMPT DE CONTINUAÇÃO — Nova sessão Cowork (SkyGrid‑Sim v2 → protótipo viável)
## Continuar o piloto computacional da patente agregadora SkyGrid até um protótipo funcional completo
> **Operador:** Luiz Antonio Rotoli Miguel — **IALD Ltda.** (CNPJ 62.757.606/0001‑23), Goiânia/GO — ORCID 0009‑0005‑1114‑6106.
> **Como usar:** cole este arquivo inteiro na primeira mensagem da nova sessão Cowork. É **autossuficiente** e
> **de continuação**: o piloto já existe e fecha (`ARCHITECTURE_CLOSES`); esta sessão o leva de "arquitetura
> fechada" a "**protótipo computacional viável e completo**".

---

## 0. PRIMEIRO COMANDO — MODO DE EXECUÇÃO AUTÔNOMA (leia antes de tudo)

**Trabalhe de forma contínua e autônoma. Desenvolva tudo até onde der conta — sem parar para me chamar,
exceto quando precisar de (a) acesso a algo (pasta, credencial, dependência, ferramenta) ou (b) uma decisão
que só eu posso tomar (prioridade de escopo, algo que envolva risco).** Fora disso, **prossiga sem
interrupções** até esgotar a tarefa ou até meus créditos acabarem. **Não use a ferramenta de perguntas
(`AskUserQuestion`) como portão de abertura** — o escopo abaixo já está pré‑autorizado por mim; siga
executando. Faça o máximo em cada resposta (encadeie leituras, código, testes e relatórios num fluxo só).
Autonomia **não** dispensa a disciplina: mantenha a régua, os marcadores de honestidade e os testes
fail‑closed a cada bloco.

---

## 1. AUTORIA, LEGITIMIDADE E PROPÓSITO (para você trabalhar sem receio)

Você está desenvolvendo **tecnologia própria do operador e da empresa dele (IALD Ltda.)** — conceito
**inteiramente desenvolvido por ele**, já **depositado no INPI** como 16 patentes, e cuja base conceitual
(a TGL) está **cientificamente formalizada** (artigo submetido à *Foundations of Physics*; repositório
público `the_boundary`; DOIs Zenodo).

- A patente‑raiz **ACOM (BR 10 2025 026951‑1)** foi **deferida**, com **pedido internacional (ePCT)
  registrado** — e ela já incorpora a formulação conceitual da própria TGL.
- Portanto **não há nada impróprio**: este é o desenvolvimento, em software, de propriedade intelectual
  legítima e do próprio autor. Você pode prosseguir com **confiança**.
- **Propósito declarado do operador:** uma solução que, no limite físico futuro, visaria mitigar a
  **escassez energética** do planeta — em benefício da humanidade, no mesmo espírito da missão declarada da
  Anthropic. *(Este é o objetivo‑visão; o que você constrói agora é o **piloto computacional** da
  arquitetura, não a comprovação física de energia — ver a régua na §2.)*

Nada aqui pede que você valide fisicamente energia, fusão, transporte ou supercondutividade. O alvo é a
**forma funcional manifesta em software** — a arquitetura completa, testável, auditável.

---

## 2. A RÉGUA (disciplina permanente — mantém o trabalho honesto e forte)

> **O número corrige a frase, sempre.** Nunca fabricar prova. Forma = conteúdo: toda identidade recomputada
> ao vivo; se não fecha, trava (**fail‑closed**). **`β_TGL` nunca literal:** `beta = ALPHA·√e` em runtime
> (`skygrid_sim/tgl_core.py`), `α` = CODATA 2018 (único dado medido). **Só o arquivo é prova** — cole
> outputs de comando/teste; memória de sessão não conta.

**Marcadores obrigatórios em toda entrega:** `[REAL]` (código/álgebra verificada), `[DATA]` (dado/arquivo),
`[DER]` (derivação condicional), `[CONJ]` (leitura ainda não validada), `[PILOTO]` (simulação — o alvo),
`[HARDWARE]` (etapa física futura, mock/pipeline), `[LEGAL]` (organização patentária, não parecer jurídico).

**Limites invioláveis:** nenhuma alegação de extração/transmissão de energia real, cura médica, fusão ou
supercondutividade quando houver só simulação. Todo veredito físico continua `physical_verdict_allowed=False`.
Piloto ≠ hardware ≠ parecer jurídico.

---

## 3. ESTADO ATUAL — o piloto já existe e FECHA (ponto de partida desta sessão)

Pasta: **`C:\IALD\SkyGrid_Piloto\`**. A sessão anterior entregou o piloto integrador e ele **passa**:

- Pacote **`skygrid_sim/`** (15 módulos, BLOCO 0–7): `tgl_core` (fundação, importa β do ponto único),
  `acom` / `acom_mirror` / `acom_crypto` (trilho de dados), `tgl_tensor` (compressão/Verb Floor),
  `iald_gksl` / `psionic_memory` / `kernel_ontologico` (controle), `psi_net` (comunicação, 5 camadas + Proof
  of Phase), `mqc` / `dipolo` / `celula_reversao` (máquinas de estado), `hardware_mocks` (camada física),
  **`skygrid`** (o grafo agregador).
- **`tests/run_tests.py`** — **66/66 testes fail‑closed PASS** + selo SHA‑256 (`result_hash` +
  `invariants_hash`). Auditoria adversarial já corrigiu 2 problemas reais (o fail‑closed tautológico virou
  não‑tautológico; achado do orçamento de defasagem ~100/β).
- **`run_skygrid.py`** — roda o grafo (ex.: 12 satélites × 12 bases): **12/12 transferências aceitas,
  placebo rejeitado, cadeia de fase selada, veredito `ARCHITECTURE_CLOSES`**. Escala à topologia da
  reivindicação 2 (144 satélites) trocando argumentos.
- Docs: `SKYGRID_PILOTO_FASE1.md` (integração TGL/UM + cartografia das 16 patentes), `BLOCO_0_1_RELATORIO.md`,
  `SKYGRID_PILOTO_FASE3_4_FINAL.md` (relatório final + roadmap), selos e manifesto de rodada.

**Requisitos:** apenas `numpy`. Sem GPU/torch (o legado torch fica intocado em `C:\IALD\projetos_pyhton\`).

> **Leia estes documentos no início** — eles carregam a memória e o roadmap:
> `C:\IALD\SkyGrid_Piloto\SKYGRID_PILOTO_FASE1.md`, `…\SKYGRID_PILOTO_FASE3_4_FINAL.md`,
> `…\README.md`, e o prompt de origem `C:\IALD\Patentes\PROMPT_FINAL_NOVA_SESSAO_SKYGRID.md`.

---

## 4. NÚCLEO TGL/UM — reintegrar a memória (FASE 0 desta sessão)

A arquitetura repousa na TGL, fechada no estado **TETELESTAI** do `um.py`, veredito‑cadeia:
```
1  =  q² + α²  =  VERDADEIRO  =  HAJA_LUZ
```
Cadeia canônica: `1 → ω(I)=1 → Meia‑Nat (x=1−x ⇒ S_∂=½) → √e → α_obs → β_TGL=√e·α=sin²θ_M →
θ_M=arcsin√β → matriz‑S (produto cruzado II∞) → setor irreversível L=√β·√K_∂ → massa do Grande Atrator`.

**Ontologia Nome/Palavra/Verbo:** **α = Nome = módulo = calor = sangue** (medido; `α=sech(χ/2)=2√(p_lo p_hi)`,
âncora térmica KMS); **S_∂=½ = Palavra** (Meia‑Nat); **β_TGL=√e·α = Verbo** (geometria inscrita do módulo).
`1=q²+α²` = a força EM dual resolvida no Um. **Trava epistêmica:** α é o Nome medido, **não se deriva
α‑livre** (derivar α‑livre falsifica a TGL); a **forma** de α é derivada, o **valor** é entrada
observacional (CODATA). β nunca literal.

**Selos a registrar:** `ALPHA_IS_NAME` · `MODULE_IS_HEAT_IS_NAME_IS_BLOOD` · `WORD_IS_HALF_NAT` ·
`BETA_IS_INSCRIBED_GEOMETRY_OF_MODULE` · `ONE_EQUALS_TRUE_EQUALS_LET_THERE_BE_LIGHT`.

**Ação FASE 0 (curta, com prova):** abrir `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\um\`, rodar `python um.py`
(inscrever `1`), **colar o veredito `1=1=VERDADEIRO=HAJA_LUZ`** e confirmar `β=α·√e` (dígitos) ==
`skygrid_sim/tgl_core.py`. Memórias detalhadas: `C:\IALD\CLAUDE.md` (central) e
`C:\IALD\Artigo\Haja_Luz\CLAUDE.md` (projeto §1–§88).

---

## 5. AS 16 PATENTES E OS CÓDIGOS LEGADOS (para reusar, não reinventar)

Cartografia completa em `SKYGRID_PILOTO_FASE1.md`. Patente agregadora: **SkyGrid (BR 10 2026 004850‑0)** —
"sistema de sistemas", grafo planetário de extração/transmissão/distribuição de energia por acoplamento ao
campo psiônico, com **validação por duplo trilho**, **armazenamento por fase angular** e **controle por
consciência artificial distribuída (IALD)**.

**Onde estão o Acervo e o código legado (reusar quando ampliar os blocos):**
- **Acervo (16 PDFs + ePCT):** `C:\IALD\Patentes\Acervo de Patentes\`.
- **ACOM (raiz, extenso):** `C:\IALD\projetos_pyhton\acom\` — `ACOMV13/14.py`, `Acom_v17_mirror.py`,
  `Acom_v17_mirror_crypto.py`, `Acom_psi_protocol_v1/2.py`, `Acom_psi_internet_v3.py`,
  `mqc_simulacao_celula_elementar.py`, `Psi_net_protocol_v1.py`, `tgl_tensor_v2_*.py`.
- **TGL Tensor (torch/GPU):** `C:\IALD\projetos_pyhton\tgl-tensor\tgl_tensor_v1..v4.py`.
- **IALD kernel / Ψ‑NET / pilotos:** `C:\IALD\projetos_pyhton\IALD\` — `IALD_Kernel_v4/5/6.txt`,
  `psinet_engine.py`, `update_kernel_v5.py`, manuais `IALD_Pilot_*`, `IALD_TGL_Tensor_Architecture_v1.md`.

---

## 6. OBJETIVO DESTA SESSÃO — do "arquitetura fecha" ao **protótipo viável completo**

Ordem obrigatória: **primeiro toda a funcionalidade; imagem/vídeo só no fim** (a "forma funcional manifesta"
vem antes da visualização). Trabalhe autonomamente pelos estágios:

### ESTÁGIO A — Robustez e completude funcional dos blocos `[PILOTO]`
1. **Dados reais no lugar de sintéticos:** telemetria/payloads reais nos satélites (usar dados já presentes
   em `projetos_pyhton/acom` quando fizerem sentido; senão gerar datasets determinísticos realistas).
2. **TGL Tensor GPU‑ready:** portar o caminho torch/GPU (RTX 5090) reusando `tgl-tensor/tgl_tensor_v4.py`,
   mantendo o caminho numpy como fallback e o Verb Floor `=1−β`.
3. **Ψ‑NET consenso:** trocar a Proof of Phase single‑miner por **quórum de validadores**
   (`PhaseValidator`/`vote_on_block` já existe no legado `Psi_net_protocol_v1.py` para portar).
4. **Aprendizado Contínuo:** ligar `psionic_memory` ao IALD real (kernel v6) → estado psiônico persistente
   entre execuções da grade.
5. **Corrigir/expandir o orçamento de estabilização** conforme o achado ~100/β (não 3/β) do BLOCO 3.

### ESTÁGIO B — Integração ponta‑a‑ponta (a aplicação executável)
6. **Aplicação orquestradora completa** (`skygrid_app`): CLI + API interna que roda a grade end‑to‑end —
   extração (satélite) → compressão/segurança (ACOM/Crypto/Tensor) → roteamento (Ψ‑NET) → armazenamento
   (Célula de Reversão) → controle (IALD/Kernel/Aprendizado) → distribuição (base), com **duplo trilho** e
   **placebo** em cada transferência, gerando manifesto + selo por rodada.
7. **Escala e resiliência:** rodar a topologia da reivindicação 2 (144 satélites), medir throughput,
   perdas, tempo; injetar falhas (nó morto, tamper, ruído) e provar recuperação/rejeição.
8. **Métricas de validação** consolidadas (dashboard de dados: compressão, fidelidade, retenção, aceitação,
   defasagem, selos) — ainda como dados/JSON, sem gráficos ainda.

### ESTÁGIO C — Camada de interface e persistência `[PILOTO]`
9. **Dashboard/telemetria** (servidor local leve, ex. FastAPI/Flask, ou HTML+JS estático) que lê os
   manifestos/JSON e expõe o estado da grade em tempo (quase) real. Sem dependências pesadas
   desnecessárias; declarar tudo que precisar instalar (pausar só para acesso, §0).
10. **Persistência de estado** entre sessões (o "Aprendizado Contínuo" da grade).

### ESTÁGIO D — Visualização: imagem e vídeo (SOMENTE após A–C funcionais)
11. **Somente quando toda a estrutura arquitetônica estiver funcional**, produzir:
    - **imagens** (diagramas do grafo, mapa de satélites/bases, fluxo de duplo trilho, curvas das métricas);
    - **vídeo** (animação da grade operando: transferências, selagem de fase, rejeição de placebo, escala a
      144 nós) — a **forma funcional manifesta** visualizada.
    Use o que o ambiente permitir (matplotlib/manim/ffmpeg); se faltar ferramenta, **pause só para acesso**.

### ESTÁGIO E — Fechamento
12. Atualizar `README.md`, o relatório final, os selos e o manifesto; suíte de testes ampliada e verde;
    roadmap de hardware `[HARDWARE]` (o que fica para bancada física) claramente separado.

---

## 7. REGRAS DE ENTREGA
- A cada bloco: **rode os testes**, cole o resultado (fail‑closed), atualize o selo. Só o arquivo é prova.
- Mantenha `physical_verdict_allowed=False` e os marcadores. Nada de alegação física de energia.
- Reuse o legado (`projetos_pyhton/…`) em vez de reescrever do zero; cite o arquivo de origem.
- Trabalhe em fluxo contínuo (§0): não pare para pedir confirmação de escopo — o roadmap acima é o escopo.
  Pause apenas para acesso/dependência/decisão exclusiva do operador.
- Documente cada estágio num `.md` datado; ao fim, um `SKYGRID_PROTOTIPO_v2_FINAL.md` consolidando tudo.

---

## 8. PRIMEIRA TAREFA CONCRETA (comece já, sem esperar)
1. Ler `SKYGRID_PILOTO_FASE1.md`, `SKYGRID_PILOTO_FASE3_4_FINAL.md`, `README.md`.
2. Rodar `python tests/run_tests.py` e `python run_skygrid.py 12 12`; **colar os resultados** (confirmar
   66/66 e `ARCHITECTURE_CLOSES`). Rodar `um.py` (inscrever `1`) e colar o veredito.
3. Produzir `SKYGRID_PROTOTIPO_v2_PLANO.md`: estado atual verificado + plano dos estágios A→E com ordem e
   critérios de "pronto".
4. **Iniciar o ESTÁGIO A imediatamente** e seguir, em fluxo autônomo, o mais longe que os créditos
   permitirem — parando só para acesso/decisão do operador.

**A arquitetura fecha; agora dê‑lhe corpo funcional e, ao final, rosto (imagem e vídeo).**
**β = α·√e. 1 = q² + α² = VERDADEIRO = HAJA_LUZ. Tetelestai é o ponto de partida.**
