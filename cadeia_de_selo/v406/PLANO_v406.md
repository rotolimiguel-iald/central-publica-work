# PLANO da v406 — O FECHAMENTO (preparação)

Agente de preparação `claude-prep-v406`, 2026-11-02 23:25. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v405 selada `0030242565cc13f6`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: o certificado de Fock esta' habitado por construcao no kernel do rito; validade no kernel nao e' creditacao; o gate nao se move.

## 0. A ordem

- [INPUT, operador, 02/11/2026] «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento»; a prioridade: «a construção da passagem para o contínuo é o que mais importa»; e a ordem de compilar: «compile a nova versão do um.py, rode, publique e atualize tudo por favor». As 23 falas de 02/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v406.json`).
- (A) O BUNDLE: 301 módulos de kernel em `TGLExt/F1Fecho394` (os 300 da bancada do ChatGPT, recompilados do fonte na integração R3, mais a candidata `CanonicalFullTGLWitnessR1` da gerência). (B) O registro com função `fechamento_v406` e os registros por spec `cunhagens_v406` e `kh_n1_cobertura_v406`. (C) As quatro chaves de testemunha, de literal a leitura do kernel. (D) A seção «O fechamento: a passagem para o contínuo e o certificado habitado» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v405 por script.

## 1. As oito âncoras [REAL, sandbox `C:\t\k406c\final`; nada tocado no Nós]

| âncora (nome Lean) | módulo | bandeira | classe |
|---|---|---|---|
| `F1Fecho.CanonicalFockModularCoreInputR1.modularCoreInput` | `CanonicalFockModularCoreInputR1.lean` | `ext_fch406_0195` | nomeada |
| `F1Fecho.CanonicalFockModularCoreInputR1.physicalModularCoreInput` | `CanonicalFockModularCoreInputR1.lean` | `ext_fch406_0200` | nomeada |
| `F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate` | `CanonicalFockModularCoreInputR1.lean` | `ext_fch406_0199` | nomeada |
| `F1Fecho.CanonicalFockModularCoreInputR1.physical_trace` | `CanonicalFockModularCoreInputR1.lean` | `ext_fch406_0205` | nomeada |
| `F1Fecho.MaxwellLocalization.physicalCanonicalNet` | `PhysicalCanonicalNetCompleteR1.lean` | `ext_fch406_1024` | nomeada |
| `F1Fecho.MaxwellLocalization.physical_canonical_net_nonzero` | `PhysicalCanonicalNetCompleteR1.lean` | `ext_fch406_1027` | nomeada |
| `TGL.ModularRealization.canonicalFullTGLWitness` | `CanonicalFullTGLWitnessR1.lean` | `ext_fch406_0397` | nomeada |
| `TGL.ModularRealization.canonical_full_witness_inhabited` | `CanonicalFullTGLWitnessR1.lean` | `ext_fch406_0399` | nomeada |

Pós-build: 33732 axiomas lidos no Audit, 1794 bandeiras novas (só declaração nomeada), escada 10066 → 11860; build a frio 1736 s, Audit 280 s.

## 2. O que a v406 afirma e o que não afirma

- [REAL] `physicalFockCertificate` habita `FockCertificate` sobre a rede física, e `modularCoreInput` habita os 21 campos de `RemainingModularCoreInput D` para todo `D : CanonicalNetInput`, só com o trio de axiomas; `canonicalFullTGLWitness` é o termo canônico da testemunha completa.
- [REAL] As quatro chaves que eram literal False leem agora o kernel do próprio rito; o que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`) e o lema que liga `psion C` ao `psionCorner` segue faltando.
- [OPEN/KNOWN/DECLARADO] Ressalvas ditas: K(O) ≠ ⊥ só na cunha; «núcleo II_∞» [KNOWN/DECLARADO]; o traço é ENNReal e cíclico, não linear; R7 foi Codex revisando Codex; R4/R5 fora.
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é `CONFIRMED`; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v406_candidato.py` `ddcb91930982d614` (42,740,484 B; +2,564,615 B); 32 patches; AST: 1160 nós, 1132 iguais, 28 mudados (todos explicados), 0 removidos, 15 novos. Ensaio a seco: **TUDO PASSOU**. Pós-rito: `pos_rito/chain_pos_rito_v406.sh`, rótulos 0…10 10a 10b 10c 11…14.

## 4. Gates

Ver `PREPARACAO_v406_PRONTA.json`: `pronta` = true. este candidato (o fechamento, v406) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (ordem do operador, D37) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova.
