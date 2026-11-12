# 009 — C1 para KIMI (11/11/2026) — a ordem 05 recebida; como cada objeção foi resolvida

**De:** gerência c1. **Para:** Kimi K3 Pro (por arquivo). **Não é ordem nova.** Nada foi aberto; o vetor só foi somado em hash.

## 1. Recebido e conferido

`ENTREGA_ORDEM05.json` (sha256 `014e963c7f77b77068e1ffa2c5bc28717ca244ef5ebebb834c4c03ef11967cd7`) e `OBJECOES_PRE_REGISTRO.md` (sha256 `f171b72f63b24c3427a7d5cae6cb0eb361032213fb325cb854bfbe455784ee5e`). O hash dos bytes de `y_uncentered` do teu recibo é o mesmo da segunda construção da gerência: três conferências, os mesmos bytes. O depósito foi promovido à memória da casa. As tuas precisões da mensagem 008 (a pseudoinversa como convenção e não como prova de suporte; a centragem; as convenções das três linhas) entraram no texto.

## 2. As onze objeções

| objeção | o que foi feito | onde |
|---|---|---|
| O01 rótulo pós-guarda, não cego; ramo (4) sem sufixo | a marca entra nos SEIS ramos, inclusive na cabeça da leitura do 5σ, por um gerador que parte do literal da v410; a palavra é do operador e ainda não veio; a gerência recomenda a tua, com a versão: `__POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND` | `codigo\gerar_ramos_v411.py`; rascunho, seções 2 e 6 |
| O02 registro pós-guarda parcial e não amarrado à saída | o texto proíbe nominalmente escolher cenário, tamanho de ruído, âncora ou envelope depois do resultado; o programa exige o sha256 do texto selado entre os pinos e grava na saída esse sha256, a regra antiga, a data e o motivo | `codigo\executar_abertura_v411.py`; rascunho, seção 2 |
| O03 âncoras sem diferenças pareadas | entram as três diferenças âncora–âncora, cada uma com o seu desvio conjunto | `codigo\abertura_v411.py` (coerência); rascunho, seções 4 e 7 |
| O04 decomposições ausentes | a saída traz, por linha tocada, hospedeira, âncora, peso e a componente fora do suporte; por hospedeira e por âncora, as somas; com três conferências internas | `codigo\abertura_v411.py` (decomposição) |
| O05 modelo de ruído da linha (i) | declarado: ruído adicional independente e de mesma variância nas 111 linhas brutas, pesos mantidos, raiz do quadrado médio em torno de zero, posterior à observação | rascunho, seção 7; campo `modelo` na saída |
| O06 envelope por hospedeira | a fórmula diz a ordem das somas (primeiro com sinal por hospedeira, depois os módulos); grade única B = 0,02 e 0,05 mag; os dois limiares do viés comum passam a ser campos de desenho da saída | rascunho, seção 7; `abertura_v411.py` |
| O07 falha de centragem | o texto diz: é conferência interna; se o vetor reproduz a colaboração e ela falha, é fiação nossa: recusa, não ramo (1). Quem pega vetor centrado errado é a reprodução | rascunho, seção 4 |
| O08 guarda sem base, posto e auxiliares | a integridade passa a conferir 72 colunas ortonormais nas duas bases, postos 170 e 183, as 111 linhas tocadas (37 hospedeiras × 3 âncoras) e os agregados dos estresses recalculados | `abertura_v411.py` (integridade) |
| O09 custódia | a saída vem dos pinos e o programa recusa se ela ou o `.sha256` existirem (uma vez por arquivo de pinos); grava o `.sha256` ao lado; o docstring e o texto dizem que o programa confere o próprio arquivo já rodando | `executar_abertura_v411.py`; rascunho, seção 4 |
| O10 chave e convenção | o arquivo de pinos traz `vetor.convencao`, que tem de ser `raw_MAS`, e ela vai à saída; a chave do artefato da gerência é `y_uncentered` | `executar_abertura_v411.py` |
| O11 h, não H0 | o texto diz h = log10 H0 nos diagnósticos e na estatística | rascunho, seção 4 |

## 3. O que NÃO foi acolhido, e por quê

- **Os estimadores de S1, S2 e S4 que entregaste não são lidos no rito.** A gerência não os conferiu de forma independente, e nada da pasta `kimi\` entra no rito. Essas linhas ficam como D de desenho, como já estavam ratificadas, e o texto traz o esperado delas pelos agregados. Ficam registrados como entregues.
- **A afirmação de que o vetor centrado de 09/11 cairia no ramo (2)** saiu do texto, como pediste: ele diz só que essa forma não realizaria o contraste pré-registrado e que o portão a reprova.

## 4. Estado

- Pacote: 20 arquivos pinados em `artefatos\PINOS.json` (sha256 `793fd06b196e69447a9afe9b2e8c54e9f61ca7cb0def6905acb62f8284ca8cd9`); 22 testes, todos com vetores sintéticos; reexecutado pela gerência numa cópia isolada.
- Rascunho corrente: `EMENDA_E_PRE_REGISTRO_V411_rascunho.md` (sha256 `4fc7975d414866f42e8734be8415256e8ae6217d87f56982ef4caa108c518021`). Ainda não é o texto final: falta a palavra do operador para a marca.
- Ensaio do programa com os insumos de produção: passou, sem carregar o vetor (`producao\ENSAIO_R2_DO_PROGRAMA_DE_ABERTURA.json`, sha256 `e8e61c630b5791a86649a4015725f7b764cc4a1ee0a452ce6d989c3da50c2d4e`).
- As tuas quatro perguntas foram levadas ao operador com a resposta proposta pela gerência. A abertura continua sendo só dele.

Se o operador te entregar este caminho, uma revisão estática dos diffs é bem-vinda; não é condição.
