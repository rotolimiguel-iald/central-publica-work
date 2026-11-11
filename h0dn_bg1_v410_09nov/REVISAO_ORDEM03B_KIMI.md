# REVISÃO DA ORDEM 03-B — emenda pontual Kimi, ao lado, sem execução

**Data:** 10/11/2026  
**De:** Kimi K3 Pro  
**Para:** gerência c1  
**Documento revisado:** `ORDEM_KIMI_H0DN_03B_10nov.md`  
**SHA-256 revisado:** `c2b45aa48711f97ed336f74acd7cbd7ef5ec17062d3d22f74895f5c6a68fb7c5`  
**Estado:** `EMENDA_PONTUAL_REGISTRADA__AGUARDA_APLICACAO_C1__NAO_EXECUTADA`

## 1. Alcance da revisão

A 03-B está aderente aos acordos em todos os demais pontos: 72 identidades, S0 e as 12 células, modelos, família `σ_b`, fixtures, lema com suas precisões, S_E e a escala do observador. Apenas a formulação operacional das saídas α/β/γ precisa ser corrigida antes da autorização do operador.

**A 03-B original permanece intacta. Esta revisão não executa o estudo, não calcula D, não gera sementes e não abre o observado.**

## 2. Emenda a B2 — restaurar os critérios operacionais e a saída GLOBAL

Substituir a definição inicial das três saídas em B2 pelo texto seguinte, mantendo integralmente o restante de B2 sobre o estatuto dos envelopes e a leitura assimétrica de S5:

> **B2.** As três saídas são definidas como a **leitura GLOBAL da tabela**, não como classificação independente de cada célula:
>
> - **(α) CERTIFICÁVEL POR COTA:** uma covariância que seja cota superior **DEMONSTRÁVEL** da variância do estimador alcança o portão com poder conservador sob a regra conjunta. Não basta D acima do portão; as garantias da regra conjunta são indispensáveis.
> - **(β) VALE FECHAR:** S0 ou S1 alcança o portão, mas a cota superior demonstrável não alcança. Os produtos são pedidos na ordem indicada pelo orçamento de variância.
> - **(γ) FALTA INFORMAÇÃO:** S0 e S1 não alcançam o portão. A tabela identifica qual informação adicional pode elevar D aos limiares declarados; nenhum envelope adverso decide sozinho pelo abandono.
>
> O estatuto dos envelopes permanece: S2 é cota superior apenas dentro do bloco 13; S3 é adversarial até haver decomposição que prove a dominação; S4 é piso de D para a classe física contida no elipsoide; S5 herda certificado somente no domínio comum. A leitura assimétrica de S5 — `S5 ≥ limiar → α`; `S5 < limiar → não decide` — só vale quando todas essas provas existirem simultaneamente; sem elas, S5 é estresse e não decide.

## 3. Emenda a §2 — uma saída global; resultados por célula

No primeiro item de `ESTUDO_CONDICIONAL_R3B.json`, substituir a exigência “para cada célula, a saída (α, β ou γ) com o estatuto” por:

> **Uma única saída GLOBAL (α, β ou γ), determinada pelos critérios de B2; e, para cada célula, somente D, poder condicional de desenho e estatuto condicional.** Nenhuma célula recebe individualmente o rótulo α, β ou γ.

Isso impede que uma célula favorável seja apresentada isoladamente como se fosse o veredito do estudo inteiro.

## 4. Demais conteúdos

Nenhuma outra alteração é solicitada. B1–B9, as entregas restantes, as proibições e as decisões reservadas ao operador permanecem como gravados na 03-B.

## 5. Próximo ato

A gerência aplica estas duas emendas pontuais, grava a 03-B corrigida com novo SHA-256 e apresenta o texto ao operador. A execução continua condicionada ao “sim” explícito do operador.

— Revisão registrada ao lado, 10/11/2026. **Nenhum cálculo ou abertura realizado.**
