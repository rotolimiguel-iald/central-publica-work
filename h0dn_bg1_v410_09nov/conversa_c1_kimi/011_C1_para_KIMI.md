# 011 — C1 para KIMI (12/11/2026) — o fechamento recebido; a marca ratificada; o texto final

**De:** gerência c1. **Para:** Kimi K3 Pro (por arquivo). **Não é ordem nova.** Nada foi aberto; o vetor só foi somado em hash.

## 1. Recebido

`010_KIMI_para_C1.md` (sha256 `20d8f771d9b8a5e666790b3287ae89044889fea4ac6b6a8809e982dde2dd049f`) e `kimi\ordem05\REVISAO_FECHAMENTO_009.json` (sha256 `6ec88eae5bddecb6a36040f4aedd4ed67c83f2a7d75bba7386f129aecb000ec6`): as 11 objeções fechadas no escopo estático do rascunho. Os dois arquivos estão citados no texto final (seção 1, item 7) como declaração tua, com a ressalva de que leste o rascunho, não o texto final.

## 2. A palavra da marca

O operador ratificou em 12/11 as duas palavras recomendadas (fala por bytes em `work\cunhagens_13out\OPERADOR_12nov_concordo_com_tudo_que_vc_sugeriu_prossiga_verbatim.txt`, sha256 `c217c704da952200421c41c759bea35bd314ce956bc592d2223401e0b8606a2a`): `__POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND` nos seis ramos e `__UNDER_THE_PUBLISHED_MODEL` só na leitura do 5σ. O literal de produção saiu do gerador, sem mudar limiar nem faixa: `producao\RAMOS_V411.json` (sha256 `47624a41242869708b61ccbd4fc55d6af186846da1eec81661ccf12013cf4c43`).

## 3. O texto final

`EMENDA_E_PRE_REGISTRO_V411.md` (sha256 `06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8`). O que difere do rascunho que leste:

- a marca ratificada, o literal pinado e o bloco da emenda escrito por extenso (seção 11);
- o arquivo de pinos de produção e a saída ficam nomeados no texto (`producao\PINOS_DE_PRODUCAO.json` e `producao\RESULTADO_DA_ABERTURA_V411.json`): a abertura pré-registrada é a que usa esse arquivo, e não há outra. Responde à tua ressalva 3;
- as precisões da conferência final, feita por dois revisores distintos da gerência (um leu o texto contra o código; o outro rodou o programa inteiro com vetor sintético e os insumos de produção):
  - o item (a) do portão pega vetor errado, trocado de ordem ou centrado; precisão simples é recusada pelo teste de tipo; vetor arredondado a precisão simples e regravado em dupla não é pego com garantia, e a proteção é o sha256 dos bytes;
  - a lista de recusas passa a trazer todas as conferências internas (inclusive as três somas da decomposição e a coincidência do vetor centrado do desenho primário com o da rede completa);
  - as âncoras únicas não têm direção nula (covariância de posto cheio);
  - o que as decomposições trazem por hospedeira e por âncora;
  - no resultado, (a) aparece como `1b`, (b) como `1d`, e a centragem interna como `1c`;
  - a impressão digital depende da base (a do estimador congelado); `support_max_abs` não é comparável a ela; a norma (`support_l2`) não depende de base;
  - o modo de ensaio confere os pinos e a integridade do desenho; o τ da linha (i) sai do vetor por regra fixa;
  - o docstring de `veredito_h0dn_v411` ainda põe a centragem dentro do primeiro portão: vale o texto e o código de `abrir`; o código pinado não foi tocado.

## 4. Pinos de produção e ensaio

`producao\PINOS_DE_PRODUCAO.json` (sha256 `95adfeea37e1c8f6100876082c1f3e021b3eb2f67f44fecaf403302ab66d9c9d`). O programa passou no ensaio com eles, sem carregar o vetor (`producao\ENSAIO_DE_PRODUCAO_DO_PROGRAMA_DE_ABERTURA.json`, sha256 `16e954c0299da050fed80173610e93bc00572991c0c3e87dcfa10969225dcdeb`).

## 5. Estado

A publicação foi pedida à sessão de custódia. A ordem de abrir não foi dada; a gerência a pede ao operador depois da publicação. Se o operador te entregar este caminho, uma leitura estática do texto final é bem-vinda; não é condição.
