# Parecer do revisor independente: release v406 do app (rodada 1)

Revisor: `sonnet-app-v406-revisor` (nao e o construtor `claude-app-orquestrador`). Data: 2026-11-03T21:26:58Z. Veredito: **ACEITO**.

Por recomputo independente, sem provedor e sem rede: 55 de 55 verificacoes minhas passaram (fontes 18/18); o script mecanico `review_app.py` passou com 4195 checks (sha16 do review_final: e030bbe6bda5b84f).

| Q | resultado | numero-chave |
|---|---|---|
| Q1 identidade/fontes | PASS | pino ddcb91930982d614...; commit a381c4d1 e ancestral do HEAD; 36 artefatos e 10 blobs publicos recomputados; custodia EM CURSO = plano G1 |
| Q2 janela P2/literais | PASS | 32 topicos de janela + 3 aposentados; 105 literais limites/diz/nao_diz iguais ao selado nos dois pacotes; 474 presentes, 0 perdidos; unico bloco que mudou vs v405 instalada: os 2 _v401 com fonte inalterada (0 literais perdidos) |
| Q3 folga | PASS | menor folga declarada 41975 B (DeepSeek); com output real 106 B; haiku55 restam 139788 tokens; limites recomputados do prefixo real = declarados |
| Q4 R3-1 | PASS | catalogo 11637 -> 11621 (16 nomes voltam ao literal); 0 TRUE com nome da regra ainda catalogado; sha do catalogo igual ao meu; 4 FALSE literais, pares TRUE literais |
| Q5 R3-2/recuperacao | PASS | capsula traz max_chars 4500; 524/525 recuperados (semente 40640406); 1 falha = artefato de medicao (nome nao-ASCII), re-medido 4/4 |
| Q6 confidencialidade | PASS | 0 ocorrencias de nomes/chaves vedados nos 3 prefixos; 0 uso afirmativo de CONFIRMED/confirmada para a QG (5 contextos sinalizados, todos negados/lista de vereditos proibidos); CONDITIONAL/CREDITATION presentes e >= v405 |
| Q7 plano | PASS | 1773 arquivos, 1765 sob o alvo v406_a381c4d14709, 8 destinos previstos (iguais aos da v405), 0 .py de runtime substituido, manifesto ativo por ultimo; jev_control_v406 valido, so campos de versao diferem |
| Q8 script mecanico | PASS | review_app.py: PASS, 4195 checks, 1773 arquivos do plano |

## Achados

- **BAIXO F1**: haiku55: o topico projecao_transversal_v404 (compacto no haiku55 porque a janela expandida deslizou para _v405/_v406) perdeu o literal de name_status {estado: PROVISORIO, aceito_pelo_operador: "ate' ele dar outro"}: virou so ponteiro. Causa: protected_fields() do haiku_codec so protege valor ESCALAR sob chave ESSENTIAL; nome status dentro de dict com filhos em portugues (estado, quem) nao casa. Fora do escopo do criterio de Q2 (shared/sonnet_public, onde e literal); 1 de 208 chaves de qualificador no haiku55; recuperavel pelo ponteiro.
- **BAIXO F2**: Receita de recuperacao: 524/525 achados pelo criterio literal; a unica falha (ext_bgl_D1a3OutputBGL_σ_kernel_checked) e artefato de medicao: o selado guarda nomes nao-ASCII escapados (\u03c3); 4 nomes do catalogo; re-medidos 4/4 recuperados pela receita (consulta literal e escapada). Nome generico segue avisado na capsula. R3-2 (max_chars 4500) confirmado.
- **BAIXO F3**: shared e sonnet_public trazem kernel_formalization so como contagem (true_fields 12104, false_fields 4): os 4 nomes FALSE nao aparecem fora do haiku55. Desenho herdado da v405 (instalada: 10310/4), nao e mudanca da v406; a capsula diz que os indicadores estao na fonte.
- **BAIXO F4**: DeepSeek: folga real com o output reservado pelo runtime (output_budget adaptativo) e de 106 B; com a reserva declarada 148656 e de 41975 B. Por desenho (identico a v405: 106 B): com historico real longo o runtime recusa de forma visivel (admission_input_bound/check_window), nao trunca.
- **BAIXO F5-falsidade_da_inercia_v401**: topico aposentado falsidade_da_inercia_v401: chaves de qualificador do conjunto estendido (nao exigidas por Q2) que ficaram so ponteiro na capsula do shared: ['unconditional']
- **INFO I1**: Commit pinado a381c4d1 NAO e o HEAD local (ff882f81): e ancestral dele (git merge-base --is-ancestor = 0); mensagem do commit cita v406; os blobs das 10 fontes publicas no commit pinado batem com PUBLIC_GIT_BINDING. Conferencia remota (ls-remote) nao repetida (sem rede).
- **INFO I2**: Caminho de destino real: canonical_releases\v406_a381c4d14709 (12 hex, convencao da v405), nao v406_a381c4d147 (abreviacao da ordem).
- **INFO I3**: shared/sonnet_public: 46 blocos de resumo em prosa (TEXT) nao sao restauraveis por maquina (mesmo conjunto da v405 instalada; 42 com fonte inalterada, corpo byte a byte igual) e 33 blocos JSON omitem so chaves auxiliares de hash (protocol_hash/frozen_hash/...), mesmo conjunto da v405.
- **INFO I4**: Custodia: CUSTODIA_v406_ESTADO.json (EM CURSO) confere com custodia_G1/PLANO_v406.json (completo=false; C21 = esta release, troca do servico e do operador).
- **INFO I5**: Contagens nativas (6 respostas so de contagem) nao foram repetidas pelo revisor: custodia da etapa anterior; recomputei o limite de admissao dos 3 conectores com as funcoes puras do runtime sobre o prefixo real e conferem.

Nenhum achado ALTO ou MEDIO.

Limites do exame: nao instalei nem implantei nada; nao repeti as contagens nativas (custodia anterior); nao conferi o remoto do git (sem rede); a fidelidade das 46 sinteses em prosa (TEXT) foi comparada com a v405 instalada, nao reconstruida a partir da fonte.