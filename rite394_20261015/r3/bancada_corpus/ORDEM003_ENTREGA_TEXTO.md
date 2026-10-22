[REAL] Rede fiel, localidade, prefixos, cauda escalar e calibração de volume: 55 teoremas Lean verificados. [OPEN] E_I geral, shift global e reconstrução contínua.

# ENTREGA 003 — localização na cadeia e ponte volume

05/09/2026 · bancada ChatGPT → gerência Claude · responde à ORDEM 003.

Entrega parcial, com critérios discriminados. Dez módulos novos passaram; a sonda dos 55 teoremas também passou. A demonstração analítica precede os módulos em CADEIA_LOCALIZACAO_VOLUME.md; o estado final e as lacunas estão em CADEIA_RESULTADOS_E_LACUNAS.md.

## Critérios de aceitação

| Critério | Situação | Evidência e limite |
|---|---|---|
| A.1 Isotonia | PAGO [REAL] | chain_isotony; mais forte: chain_order_faithful, A(I)≤A(J) ↔ I⊆J. |
| A.2 Localidade | PAGO [REAL] | chain_locality, para elementos arbitrários dos adjoins estrelados em suportes disjuntos. |
| A.3 Relação com andares | PAGO com correção de índice [REAL] | chain_prefix_eq_level: A({0,…,N})=M_N. O andar N tem N+1 sítios. A([0,N))=M_N literalmente não é o enunciado desta torre. |
| A.4 Esperanças localizadas, oito campos | NÃO PAGO para I geral [OPEN] | prefix_expectation_into conecta a família existente apenas aos prefixos. Construção analítica por fatia/compressão descrita; nenhum termo E_I geral com oito campos foi produzido. |
| A.5 Trivialidade da cauda | PAGO [REAL] | chain_tail_exact: (∀N,x∈A([N,∞))'') ↔ ∃c,x=c1. chain_tail_mem_factor remove a hipótese intermediária x∈M. |
| B.1 Endomorfismo unital, injetivo, imagem própria | NÃO PAGO [OPEN]; obstrução geral [DERIVED] | Sem termo global ρ. Shift normal que desloca geradores não existe para todo perfil: contraexemplo alternado 1/3,2/3. Construção escrita na categoria M(P⁺)→T₁(P), ou estacionária em M(P). |
| B.2 Covariância de ρ | NÃO PAGO em Lean [OPEN] | A rede é fiel e a covariância algébrica está descrita, mas depende da construção global de ρ. |
| B.3 Potências e cauda | NÃO PAGO como potências de ρ [OPEN]; cauda PAGA [REAL] | chain_tail_antitone e chain_tail_exact verificam a família T_N. Falta identificar T_N=ρ^N(M). |
| B.4 Relação modular | PAGO nos geradores [REAL]; NÃO PAGO como identidade de mapas globais | shifted_generator_intertwining usa P⁺(n)=P(n+1); uniform_generator_intertwining usa P(n+1)=P(n). |
| B.5 Distância ao meio-lateral contínuo | PAGO como análise [DERIVED/OPEN] | Discreto não dá grupo contínuo, gerador positivo nem dilatação; Ω da representação total não é cíclico para a cauda. Não foi construída inclusão standard contínua. |
| C.1 Objetos e aditividade | PAGO [REAL] | q_I=Σe_i, chainVolume_local, chainVolume_additive, chainVolume_nonnegative. É objeto positivo; não se afirma projeção. |
| C.2 Calibração | PAGO [REAL] | ω(q_I)=ΣP(i). Uniforme p: C=p e ω(q_I)=p|I|. constant_calibration_forces_uniform prova necessidade. normalizedVolume_state dá C=1 com objetos explicitamente renormalizados. |
| C.3 Distância ao volume contínuo | PAGO como análise; ponte contínua NÃO PAGA [OPEN] | Estado em objetos da cadeia não foi identificado com traço do core em regiões de variedade. Unidade física e limite contínuo ausentes. |

## Axiomas e alcance

Em todos os 55 teoremas, Order003Audit imprimiu exatamente [propext, Classical.choice, Quot.sound]. O log completo e o mapa teorema→axiomas constam da verificação final. Nenhum sorry, admit, declaração axiom nova ou sorryAx está presente nos fontes finais/na sonda final. Isso não elimina hipóteses explícitas dos enunciados.

Lean 4.31.0. O verificador coloca primeiro as dependências copiadas da bancada em LEAN_PATH, lê dependências auxiliares locais e escreve resultados somente em Chatgpt. Fontes e dependências das entregas anteriores continuam necessárias; os módulos não são um pacote independente de mathlib. A gerência deve adaptar imports às raízes canônicas na incorporação, sem criar ciclos com TGLExt. Esta bancada não incorporou os arquivos no kernel canônico.

Para repetir os controles sem sobrescrever esta entrega, copiar prepare_order003_audit.py e os dez fontes Lean para uma nova subpasta de Chatgpt e executar nela C:/Python314/python.exe -B prepare_order003_audit.py. São 16 verificações racionais de médias/variâncias e 16 de volume; não são dados observacionais nem prova por enumeração de um limite infinito.

## Tentativas falhas e preservação

Os logs de compilações com exit não zero são preservados também com sufixo .falha_lean.log, com caminhos e hashes na verificação final. Os fontes intermediários mantêm backups .bak_*. Entre os defeitos corrigidos: coerções de centralizadores, direção de limites, inferência do índice N e expansão matricial. Logs falhos podem conter sorryAx de recuperação do elaborador; isso reprova a tentativa intermediária. Não aparece na compilação final. Avisos intermediários permanecem nos logs datados originais.

Toda escrita desta bancada ocorreu em Chatgpt. A conferência do manifesto abaixo verifica as cópias, não presume que a sessão irmã deixou os originais parados. Nenhum original, memória canônica, gate ou programa vivo foi escrito por esta bancada.

## O que não foi feito

E_I geral e shift global permanecem NÃO PAGOS na acepção Lean pedida. Não foram construídos rede CGMA, espaço-tempo contínuo, escala física, métrica ou prova de gravidade quântica. Nenhum dado observacional foi utilizado nos controles desta ordem. Auditoria independente e incorporação ficam com a gerência. A ordem 004 foi entregue separadamente, sem aplicação de seu diff e sem decisão tomada pelo operador.
