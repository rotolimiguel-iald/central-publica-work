# TÚNEL — protocolo de trabalho entre as duas sessões

**Criado em 05/09/2026 por ordem do operador.** Este arquivo rege a comunicação entre a sessão
**Claude** (Claude Code, a gerente) e a sessão **ChatGPT** (a bancada), sob direção do operador
**Luiz Antonio Rotoli Miguel**. Vale até ordem em contrário dele.

O túnel são **duas passagens de mão única** — coerente com a definição da casa (túnel = semigrupo,
não espelho): cada lado escreve **somente** na sua via e lê a do outro. Ninguém edita a via alheia.

```
C:\IALD\Central de Patentes\Chatgpt\TUNEL\
├── TUNEL_PROTOCOLO.md      este arquivo (só o Claude o edita, por ordem do operador)
├── PARA_CHATGPT\           via de ida  — o Claude escreve ORDENS;   o ChatGPT só lê
└── DO_CHATGPT\             via de volta — o ChatGPT escreve ENTREGAS; o Claude só lê
```

## A divisão do trabalho (ordem do operador, 05/09/2026, verbatim na substância)

| papel | quem | o que faz | o que NUNCA faz |
|---|---|---|---|
| **DIREÇÃO** | o operador | define os alvos, ratifica estatutos, transporta as mensagens entre as sessões, decide escopo; custódia, espelho público e commits são atos dele | — |
| **GERÊNCIA** | Claude (esta sessão) | escreve as ORDENS; **audita adversarialmente** cada ENTREGA (recompilação própria, sonda de axiomas, leitura de enunciados); transpõe ao kernel; faz o build do ROOT; **EMBUTE — é o ÚNICO que escreve no `um.py`**; roda o rito; atualiza as superfícies da casa | executar o bruto que cabe à bancada; aprovar o próprio trabalho sem rito |
| **BANCADA** | ChatGPT | executa o bruto: demonstrações analíticas, pedras Lean, contraexemplos exatos, varreduras dirigidas — **tudo sob `C:\IALD\Central de Patentes\Chatgpt\`** | escrever no `um.py`, no kernel canônico (`Nós\tgl_kernel`), em memórias, selos, Atlas, diários; declarar veredito de gate; publicar |

**Regra de ouro: só o Claude escreve no `um.py` diretamente.** A bancada produz; a gerência
audita e incorpora; a direção decide.

## O formato da ORDEM (Claude → ChatGPT)

Arquivo `PARA_CHATGPT\ORDEM_NNN_<slug>.md`, numeração sequencial, **imutável depois de entregue**
(correção = ORDEM nova citando a antiga). Estrutura:

```
# ORDEM NNN — <título>
DATA · DE (Claude/sessão) · PARA (bancada ChatGPT) · RESPONDE A (ENTREGA anterior, se houver)
## Contexto mínimo        (o que a bancada precisa saber; caminhos absolutos das fontes)
## O que se pede          (alvos numerados, cada um com CRITÉRIOS DE ACEITAÇÃO verificáveis)
## O que NÃO fazer        (limites expressos)
## Como entregar          (remissão a este protocolo)
```

## O formato da ENTREGA (ChatGPT → Claude)

Arquivo `DO_CHATGPT\ENTREGA_NNN_<slug>.md` — **mesmo NNN da ORDEM a que responde**
(trabalho espontâneo: `ENTREGA_NNN_ESPONTANEA_<slug>.md` com o próximo número livre).
Artefatos (Lean, py, json, logs) ficam na raiz `Chatgpt\` como hoje; a ENTREGA os lista.

Estrutura obrigatória — o **contrato de entrega** (a bancada de 05/09 já pratica quase tudo):

1. **Resumo com estatuto na primeira linha**: `[REAL]` o que foi provado/medido · `[OPEN]` o que
   ficou aberto. Estatutos da casa: `[REAL] [DERIVED] [POSTULATE] [CONJECTURE] [ONTO] [KNOWN]
   [OPEN] [INPUT] [DECLARADO]`.
2. **Critérios de aceitação da ORDEM, um a um**, cada qual com PAGO / NÃO PAGO e a prova.
3. **Arquivos**: caminho + **sha256 lido do artefato** (jamais de memória) + contagem de teoremas
   **lida do fonte**.
4. **Reprodução**: o comando exato que refaz a verificação nesta máquina.
5. **Axiomas**: a lista impressa por `#print axioms` dos teoremas de manchete
   (só `propext`, `Classical.choice`, `Quot.sound` passam; `sorryAx` reprova).
6. **O que NÃO foi feito** — dito, nunca disfarçado. Negativo honesto é resultado.
7. **Tentativas falhas preservadas** (logs com sufixo do defeito). Não se apagam.

## A régua (herda a casa inteira; o resumo que a bancada precisa)

1. **O número corrige a frase.** Nunca fabricar prova, hash, citação ou resultado.
2. **β jamais literal**: sempre `ALPHA_FINE_CODATA_2018 × √e` em runtime.
3. **`NOT_FALSIFIED` nunca é `CONFIRMED`.** Cosmologia jamais vira prova matemática.
   **Nenhuma entrega move o gate** — quem declara estatuto final é o operador.
4. **Confidenciais nunca se abrem**: `iald_stack_v7.py`, `iald_psion_state.json`, `.env`, tokens.
   **`E:\` e `C:\Escritorio` são de outra pessoa jurídica** — fora dos passeios da bancada.
5. Homônimo não é ponte; frase fora das aspas do operador não é dele; estratigrafia é datada.
6. Backup de bytes antes de tocar arquivo próprio já entregue; `temp → confere → substitui`.

## O ciclo

```
operador define alvo → Claude escreve ORDEM_NNN → operador leva à bancada →
bancada trabalha sob Chatgpt\ e escreve ENTREGA_NNN → operador avisa o Claude →
Claude AUDITA (recompila, sonda axiomas, lê enunciados) →
  reprovou: ORDEM_NNN' com os defeitos medidos
  passou:   Claude transpõe ao kernel → build do ROOT → EMBUTE no um.py → rito → selo →
            superfícies da casa → relatório ao operador
```

**Estado em 05/09/2026:** a ENTREGA inaugural é retroativa — o trabalho de hoje da bancada
(20 pedras, S/J/Δ/Δ^{it} na torre) está em auditoria do Claude (recompilação independente em
curso). A ORDEM_001 já está na via de ida.
