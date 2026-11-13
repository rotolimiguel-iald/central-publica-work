# ORDEM KIMI H0DN-04 (11/11/2026) — a montagem do vetor (A1), pelo protocolo do próprio Kimi; o desenho ratificado pelo operador

**De:** gerência c1 da Central (Claude Code), por decisão do operador de 11/11/2026 (verbatim sha256 `63b4bb056e4923a9a490009fa55cf41fd619eb7909868e47d657bd4d123ab7c9`).
**Para:** Kimi K3 Pro, na sessão de trabalho do operador (por arquivo; o operador é o túnel).
**Tipo:** RECONSTRUÇÃO DOCUMENTAL + MANIFESTO. **A conferência do vetor NÃO está autorizada nesta ordem.**
**Estatuto do retorno:** `[DECLARADO pelo Kimi]` até a gerência conferir.
**Estado:** `ORDEM_04__EMITIDA__ETAPA_1_AUTORIZADA__ETAPA_2_NAO_AUTORIZADA`.

## §0 O que mudou, e por quê

O operador perguntou o que falta para o teste ter poder discriminativo acima de 5σ e pediu a opinião da gerência. A opinião foi dada e ele a ratificou: «perfeito, concordo com tudo, inclusive com sua sugestão de teste, que em verdade, é terminar e rodar o que já estávamos fazendo. ótimo, vamos prosseguir»

O registro está em `DESENHO_RATIFICADO_H0DN_11nov.md` (sha256 `c62858c238efea54fdbabe38e3983a8ac4415bf3070d5238b48223996bf1f6d4`). Em resumo:

- **primário:** o modelo publicado, com a covariância publicada tratada por redução às 183 medidas ou pseudoinversa (o A1 que o Kimi fechou por álgebra);
- **ao lado, inseparável:** o modelo com o viés diferencial das Cefeidas livre;
- **independência local–fundo:** hipótese nomeada (BG1 é Planck comprimido mais DESI DR2, sem supernovas);
- **portão:** 90 % (D ≥ 6,282), avaliado no S0 do modelo publicado;
- **os 13:** fora (`EXTRA13_OUT`);
- **S1, S2, S4 e o modelo de Cefeidas livres** deixam de ser trava e passam a ser LINHAS DE ESTRESSE publicadas junto com o resultado. O estudo 03-C (`ESTUDO_CONDICIONAL_R3B.json`, sha256 `24d42026500d864d85685de6cb2825e873a4826bc7cd26c4d5e8128e635ed8e3`) segue sendo a fonte delas.

**Errata da gerência, em nome próprio:** a condição de abrir só com a covariância física fechada pelas fontes (D96; ordens 02 e 03) foi escrita pela gerência, não pelo operador, que pediu poder discriminante real. No juízo da gerência essa barra nenhuma análise publicada cumpre, e ela a retira. O fecho do Kimi continua ABERTO como ele o declarou (não há prova de dominação na matriz inteira); o que muda é que isso deixa de impedir a abertura e passa a ser dito ao lado do resultado.

Se o Kimi discordar do desenho por razão física ou estatística, que o diga na entrega: a gerência leva a objeção ao operador com as palavras dele. A tarefa abaixo não depende dessa resposta.

## §1 A tarefa: só A1, em duas etapas, com parada no meio

Vale o `PROTOCOLO_CONFERENCIA_FUTURA.md` do Kimi (sha256 `db74c3f866128276361abd932af721394126615903a899a8dae1880099e566f8`) e o `A1_HIPOTESES_DO_VETOR.md` (sha256 `e45a0f0dbe67dc502eaaf0674a9477466c2dd6b78c3627a6bd7cfe587878aeae`), inteiros.

**Etapa 1 (autorizada agora; NÃO lê o vetor observado):**

1. Reconstruir documentalmente a cadeia tabela → fit → MAS → centro compartilhado (hipótese H1) e a convenção de montagem (hipótese H2), só pelas fontes públicas.
2. Decidir, SÓ pela fonte, a convenção de centros da variante (`raw_MAS` ou `documented_MAS_corrected`), com a prova documental. Se a fonte não decidir, PARAR e dizer.
3. Fixar a precisão por célula, a regra de quantização e as 72 tolerâncias (§3 do protocolo); a tolerância numérica já está fixada em 1e-12 mag.
4. Escrever o código de montagem da variante e testá-lo SÓ nos fixtures sintéticos.
5. Gravar o MANIFESTO imutável do §2 do protocolo, com `variant_id = H0DN_PUBLICADO_REDUZIDO_183__EXTRA13_OUT__<convenção>`, e PARAR.

**Etapa 2 (NÃO autorizada agora):** a única conferência das 72 identidades. Só depois de a gerência conferir o manifesto e de o operador autorizar a variante nomeada (§1, item 1, do protocolo). Antes disso a gerência lê a partitura a ele: a conferência decide se o vetor montado cabe no molde publicado; não decide nada sobre H0, sobre a razão nem sobre β_TGL; se falhar, é parede de montagem desta variante, e o teste não abre com ela.

## §2 Entregas (em `kimi\ordem04\`)

- `RECONSTRUCAO_DOCUMENTAL_A1.md`: a cadeia, com fonte, página ou linha e sha256 de cada peça;
- `MANIFESTO_VARIANTE.json`: os campos do §2 do protocolo; sem o vetor;
- `montar_variante.py` e `VALIDACAO_FIXTURES.json`;
- `LINHAS_DE_ESTRESSE.md`: as linhas a publicar junto (Cefeidas livres; S1; S2; S4), cada uma com o D do estudo 03-C e a hipótese em uma frase;
- `ENTREGA_ORDEM04.json`, com as bandeiras e os sha256;
- depósito na fila da memória com `quem: kimi`.

## §3 Proibições

- Na Etapa 1: não ler `y_obs.npz` nem nenhum vetor observado; não chamar solver nem `evaluate`; nenhum Z, t, ĥ, H0 ou razão; nenhuma semente nem Monte Carlo; não tocar `FREEZE_R2`, a v410 nem o gate.
- Não reparar o vetor por projeção; não ajustar tolerância ao resultado; não escolher a convenção pelo resultado da conferência de 09/11 (0,0931 mag): a convenção sai da FONTE.
- Não reproduzir o H0 publicado com o vetor observado: essa reprodução é o primeiro portão do rito de abertura, não desta ordem.
- Nenhum contato externo: os pedidos às fontes são ato do operador.

## §4 O que fica com o operador

- autorizar a variante nomeada antes da Etapa 2;
- enviar ou não os pedidos às fontes (rascunho em `PEDIDOS_AS_FONTES_rascunho_11nov.md`);
- a ordem da v411, depois de ler o pré-registro.

## §5 De onde vem

| documento | sha256 |
|---|---|
| `ORDEM_KIMI_H0DN_03C_11nov.md` (executada; preservada) | `d0df9b4430ca9ff9d4fccb74ffcddc789819a5f29f7b030aa461a09c5a7c6836` |
| `kimi\ordem03B\ESTUDO_CONDICIONAL_R3B.json` | `24d42026500d864d85685de6cb2825e873a4826bc7cd26c4d5e8128e635ed8e3` |
| `kimi\ordem03B\PROTOCOLO_CONFERENCIA_FUTURA.md` | `db74c3f866128276361abd932af721394126615903a899a8dae1880099e566f8` |
| `kimi\ordem03B\A1_HIPOTESES_DO_VETOR.md` | `e45a0f0dbe67dc502eaaf0674a9477466c2dd6b78c3627a6bd7cfe587878aeae` |
| `kimi\ordem03B\PRODUTOS_A_PEDIR.md` | `3dc258d5dacbde3b9c8dc86e4a4c110beee132f4f8b068ab0953ab98243aa472` |
| `FREEZE_R2.json` (intocado) | `c40159977fc8d954bc6a65eb3fd4b85f72a9d07629897f265308aa20579a51ed` |
