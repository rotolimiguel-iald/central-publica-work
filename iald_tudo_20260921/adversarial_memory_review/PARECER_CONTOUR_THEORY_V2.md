# Reavaliação focal independente — contour_theory — 22/09/2026

**APROVADA quanto à fidelidade da síntese deste tópico à fonte documental, com a inconsistência herdada explicitamente registrada.** Não identifiquei perda essencial remanescente nem ampliação indevida de escopo na cápsula revisada. A aprovação abrange somente o texto com o hash abaixo; não abrange integração, recuperação operacional, os outros tópicos, orçamento Haiku ou confirmação física.

## Artefatos e medição local

[REAL — leitura e medição local] Cápsula revisada: `semantic_capsules/contour_theory.md`, SHA256 **`e1a10161a858644ac3edc5d4b4c0c50041eb0bf51e12164838be547ea0459d78`**, conferido por script.

Fonte: `/core/contour_theory` do `resultado_publicado_integral`, localizada pelo manifesto. SHA256 do arquivo-fonte: `db24966d96c16a546f9bd221b990dfe5f8ad3a3d9d43343644ba19f71745336e`, reconferido e igual ao da revisão anterior. A comparação semântica usa o tópico integral já lido, inclusive os sete passos, e a leitura integral da nova cápsula.

| Medida `o200k_base` | Tokens |
|---|---:|
| Bloco antigo: cabeçalho + Fonte + JSON | 2.108 |
| Corpo JSON antigo isolado | 2.088 |
| Cápsula corrigida inteira | **1.671** |
| Economia contra o bloco antigo completo | **437** |
| Acréscimo sobre a cápsula anterior de 1.331 | **340** |

Esses números foram calculados localmente. A comparação com 1.331 usa o recibo da primeira medição conferida. **Tokens Anthropic/Haiku: não medidos nem inferidos.**

O candidato completo mudou desde a revisão anterior: seu SHA nesta leitura foi `83870f5abbea7f74ce13dca097a35a5f6590e067ef19d06f4725ee8652f47c92`. O bloco antigo deste tópico continua medindo 2.108 o200k. Nenhuma conclusão sobre o restante do candidato foi transferida para essa versão.

## Quatro correções conferidas

| Achado anterior | Resultado na nova cápsula |
|---|---|
| Ponto fixo/saturação e relações das taxas omitidos | **Resolvido.** Recupera `rho_kappa`, `0<rho<1`, saturação sem condensação, `q=(g- - g+)/(g- + g+)`, `alpha=2sqrt(g+g-)/(g+ + g-)`, conservação e limite estático. A restrição ao check e a ausência de generalização para positividade em dimensão infinita estão explícitas. |
| Canal neutrínico descrito apenas por adjetivos | **Resolvido.** Recupera `{Z,L_nu}=0`, `[Q_em,L_nu]=0` e `L^dagger L!=0`, distinguindo o check de uma afirmação universal de dissipação. Não confunde `L_nu` com a relação psiónica de `L_+-`. |
| Limite de alpha incompatível na fonte | **Resolvido como tratamento documental; problema da fonte permanece aberto.** A cápsula atribui à fonte `theta->90deg, alpha->1`, conserva a fórmula e registra que, na mesma normalização, ela dá `1/sqrt(e)`, não 1. Marca a substituição como DERIVED e a compatibilização como OPEN, sem inventar mudança de regime. |
| Atualização interna e remissões ambíguas | **Resolvido no texto.** Distingue a formulação do seletor, a forma canônica de `rho_ret` e o cálculo espectral ainda aberto. Usa base + filho e substitui “provas” por “evidência e checks registrados”. Declara a recuperação operacional não validada. |

## Fidelidade e omissões remanescentes

As fórmulas principais de Bell seletor, cociclo, KMS/GKLS, unitariedade, Meia-Nat, retorno relativo, parte finita e ação candidata continuam representadas. A cápsula distingue equivalência de contorno de igualdade de projetores; Bell nu/zero de contraste de zero de existência proibido; `0_abs` de `0_mod`; forma canônica de seleção alpha-livre. Conserva o input QED, a não seleção por contagem de modos e o alcance ontológico das leituras correspondentes.

A fonte contém redundâncias, valores individuais dos checks, probabilidades, resíduos e uma lista de candidatos numéricos rejeitados que a cápsula não reproduz integralmente. **Não considero essas omissões perdas essenciais para esta síntese:** o mecanismo, as condições qualitativas, o resultado negativo da seleção e a remissão aos detalhes permanecem. A cápsula não deve ser descrita como transcrição integral da fonte.

Não surgiu mudança indevida de estatuto: REAL é atribuído aos checks reportados, não a execução nesta revisão; o mínimo alpha-livre continua aberto; a inconsistência algébrica permanece visível; ONTO não é convertido em confirmação física. O aviso inicial impede generalizar aberturas históricas deste registro à versão inteira sem confrontar construções posteriores.

**Pendência preservada, não bloqueadora desta aprovação documental:** a compatibilização entre a fórmula angular e a frase do limite na fonte não foi resolvida. Aprovo sua representação honesta na síntese, não a consistência daquela conjunção original.

## Limites da aprovação e integridade

Os filhos `steps`, `psionic_bond_unification`, `first_law_link` e `open_theorem_verdict` existem no objeto-fonte. Isso é conferência estrutural local; **a recuperação operacional por JSON Pointer não foi validada**. Não executei ferramenta de fetch, `prepare_pointer_fetch.py`, `um.py`, builder ou produção. Não houve API, rede, leitura de `.env` ou alteração dos arquivos do pai.

Os bytes da cápsula, fonte, manifesto e candidato foram reconferidos ao final da medição e permaneceram iguais durante esta revisão. Escritas limitadas a esta subpasta: `measure_contour_focal_v2.py`, `contour_focal_v2_measurements.json` e este parecer novo. O parecer anterior foi preservado.

**Decisão final focal:** o texto identificado está apto, sob o critério de fidelidade documental deste tópico, a ser considerado pelo pai para integração. Isso não afirma que já foi integrado, que a recuperação funciona, que o pedido completo cabe no orçamento ou que os demais tópicos foram aprovados.
