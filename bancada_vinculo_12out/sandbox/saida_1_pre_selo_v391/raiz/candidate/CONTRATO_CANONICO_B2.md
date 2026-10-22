# Contrato de fidelidade da Bancada Um — B2 / NU3

[INPUT] Atualização solicitada diretamente pelo operador em 09/10/2026. Unidades F0.3.B2 (reivindicação 632) e F8.2.NU3 (633).

## Identidade em cada operação

O manifesto canonical_contracts.json pina o um.py canônico, o selo, os módulos, as interfaces e as fontes consumidas. A Bancada confere os bytes na entrada e na entrega; uma divergência recusa a operação. Não basta o valor numérico de beta coincidir. O recibo distingue versão do programa, contrato e fontes. Custódia de fonte não substitui sua admissão pelo operador.

Uma versão nova do um.py invalida o contrato instalado. Sua incorporação exige revisar as convenções afetadas, testar o candidato, registrar evidência e implantar uma geração nova com backup. A detecção é automática; a promoção científica não é automática. Nunca atualizar somente o hash para silenciar uma incompatibilidade.

## Contratos disponíveis

- Cosmologia: padrão TGL com mapa efetivo ratificado; reprodução selada é explícita. Curvas e resíduos recebem as mesmas opções. Sobreposição conhecida de conjuntos e dupla contagem de beta são recusadas. A tabela CAMB tem suporte instrumental finito; sua interseção não é o prior físico completo. Correlações DR1 transcritas sem artefato primário próprio permanecem [DECLARADO]. A convenção l_A e a adequação física têm o alcance dos registros existentes.
- N_eff: as duas linhas da fonte (Yp pela BBN e livre) aparecem separadas, com fonte e extração. A escolha X16/D8 permanece explícita.
- Neutrinos: os artigos do autor fornecem os contratos. As realizações de paridade, raiz modular e desfasamento por diferenças de massa são distintas. Tempo modular, tempo físico, tau_star e curvatura não são identificados por nome. A API sintética não calcula sigma experimental nem rendimento absoluto de uma supernova Ia.
- GW: consulta histórica ECO; formatos da série são validados. Um rito selado exige o executor e o despacho próprios. A bancada não promove o ECO a ensaio de ringdown nem abre a Fase 9.

## Interfaces

GET /api/contratos; GET /api/neutrino/contrato; POST /api/neutrino/sintetico. Todas as ferramentas MCP científicas atuais passam pelo serviço HTTP guardado. Adaptadores anteriores devem ser encerrados/reconectados: alterar arquivos no disco não atualiza módulos já em RAM.

GET /api/atividades informa cargas, requisições e tarefas. POST /api/maintenance/quiesce impede novas operações científicas para manutenção. A unidade de implantação registra o reinício e confere a identidade devolvida pela nova instância.

[DERIVED] Os testes sintéticos verificam implementação e recusas no domínio declarado. Não são confirmação da TGL. NOT_FALSIFIED não é CONFIRMED. Nenhum rito move o gate.
