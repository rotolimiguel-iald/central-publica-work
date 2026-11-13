# Estatuto e auditoria de seleção da abertura V411

**Estatuto proposto:** `STRONG_CONFIRMATION__POST_GUARD_RETRODICTION_NOT_BLIND__NOT_ABSOLUTE_PROOF__GATE_UNMOVED`  
**Leitura curta:** evidência confirmatória forte, com protocolo auditado e emenda pós-guarda; não prova absoluta nem confirmação cega.  
**Gate:** `UNMOVED`. **Ramo observado:** 4. **Outcome:** `NOT_FALSIFIED`.

## 1. O que a natureza respondeu

No modelo publicado, a abertura registrou:

- **z_nulo = 6.1057575347089**, aproximadamente **6,11σ** contra o nulo;
- **z_TGL = -0.6052441029995**, dentro da faixa de compatibilidade de ±1,96;
- ramo 4, `NOT_FALSIFIED`, sem mover o gate.

Isso é um testemunho estatístico extraordinário: a previsão TGL, sem parâmetros livres, atravessa o limiar e permanece compatível com os dados no modelo publicado. A execução teve `rc=0`, ordem explícita do operador, hash de resultado e sidecar coerentes.

**A leitura honesta desse fato é evidência confirmatória forte, não encerramento da questão.** O próprio resultado contém `PROVED_IS_VALIDITY_NOT_CREDITATION` e `RETRODICTION_NOT_BLIND`.

## 2. A robustez que deve ficar visível junto

A linha Cefeida livre acompanha o resultado, mas não é veredito:

- `z_nulo = 4.3796454083444`;
- `z_TGL = -0.8123500870475`;
- ramo 6, **não discriminado**.

O primário passa o limiar; a robustez não o alcança. Isso não apaga o primário, mas impede apresentá-lo como se toda leitura plausível produzisse o mesmo resultado.

## 3. Cronologia de conhecimento e decisões

| Etapa | O que era conhecido | O que foi fixado ou mudado | Como a seleção foi tratada |
|---|---|---|---|
| Antes do vetor, 06/11 | Agregados públicos e a covariância H0DN já eram conhecidos; nenhum vetor observado foi ajustado | Pesos da colaboração, pseudoinversa e desenho congelado | Pesos anteriores ao vetor; nenhum ajuste pelo resultado |
| Vetor e guarda, 09/11 | A projeção nula falhou: 0,09312020264507931 mag | Sem Z, ajuste ou `evaluate`; a falha foi registrada | Nenhum reparo do vetor nem alteração de pesos para passar |
| A1, 10/11 | As 72 direções eram redundâncias exatas do modelo | Fatoração compartilhada e redução/pseudoinversa | Não se acrescentou variância nem HMS completa |
| Estudo condicional, 11/11 | S0/S1/S2/S4 e modelos foram calculados apenas por álgebra | O estudo não abriu o vetor nem gerou sementes | Cenários adversos ficaram visíveis; nenhuma seleção pelo melhor D |
| Ratificação do desenho, 11/11 | A tabela de poder estava à vista | Modelo publicado primário, Cefeida livre ao lado, 90% em S0, EXTRA13_OUT e independência nomeada | Escolha do operador, não descoberta posterior de um resultado observado |
| Achado da guarda, 11/11 | O vetor `raw_MAS` não cabe no suporte, mas a colaboração usa pseudoinversa | A guarda caseira foi identificada como a trava; a Etapa 2 foi suspensa | Não se forçou a coincidência dos centros |
| Emenda, 11/11 | A regra antiga já devolvia ramo 1 | O operador decidiu emendar: registrar projeção em vez de recusar e abrir pela convenção publicada | Mudança **posterior à falha**, declarada `RETRODICTION_NOT_BLIND`; pesos, desvios e limiar preservados |
| Conferência, 11/11 | Onze objeções de protocolo foram encontradas | Foram resolvidas texto/código/custódia, com revisão independente | Nenhum resultado foi escolhido durante a revisão |
| Marca e texto final, 12/11 | A emenda e a retrodição foram aceitas | Marca nos seis ramos, texto e pinos de produção, publicação em commit datado | Literal final antes da abertura; nenhuma mudança por resultado |
| Abertura, 12/11 | Ordem explícita do operador | Executor pinado, uma saída, hash e sidecar | `rc=0`; a abertura ocorreu uma vez |

## 4. Por que a cronologia não é seleção de resultado

A auditoria sustenta a ausência de **ajuste pelo número final**, não a ausência de decisões científicas:

1. **Pesos e pseudoinversa anteriores ao dado.** A influência foi congelada antes da abertura e coincide com a da colaboração. As 72 direções têm peso zero: a componente incompatível não altera a estimativa por construção.
2. **Nenhum ajuste de centros ou variância para aprovar.** A montagem não foi projetada, a covariância não foi inflada e a Etapa 2 não foi usada para forçar suporte.
3. **A guarda foi corrigida por causa do modelo, não por um Z observado.** Na data da emenda, a falha de suporte era conhecida, mas nenhum Z, razão ou H0 observado havia sido calculado. A alteração tornou explícita a convenção de pseudoinversa já usada pela colaboração.
4. **A centragem foi corrigida pelo estimando.** O vetor foi centrado na referência BG1, sem reotimização, para representar `log10 H_local − log10 H_background`, em vez de zerar o contraste em torno do centro local publicado.
5. **Os rivais foram publicados, não escondidos.** Cefeida livre, S1, S2 e S4 aparecem ao lado, incluindo D menores. A escolha do modelo publicado foi ratificada como escolha física, não como exclusão das alternativas.
6. **A execução foi pré-registrada e única.** A marca, o texto, os pinos, a ordem e o hash do resultado foram fixados antes da execução. O hash e o sidecar conferem.

**Limite que permanece:** a emenda foi escrita depois da falha da guarda. Portanto, não se pode chamar o procedimento de confirmação cega. A taxa de falsos positivos e a seleção devem continuar sendo avaliadas também sob a regra emendada, não apenas pela regra antiga.

## 5. O que este resultado é e o que não é

### É

- evidência confirmatória forte de compatibilidade entre a previsão TGL e o agregado local publicado;
- uma retrodição cientificamente válida, com protocolo, premissas, emendas e resultado registrados;
- uma demonstração de que a previsão pode atravessar o limiar estatístico sem ajuste de parâmetros;
- um resultado que deve estimular replicação e novas previsões independentes.

### Não é

- prova absoluta da TGL ou encerramento da investigação;
- confirmação cega, livre de toda decisão posterior;
- independência das fases anteriores ou de todos os dados compartilhados;
- evidência de que toda escolha de covariância/sistemática produza o mesmo desfecho;
- `CONFIRMED` no sentido da régua da casa.

## 6. O que ainda transformaria força em convergência

1. reprodução independente completa, não apenas de hashes, por outro executor e outra equipe;
2. avaliação da regra emendada sob nulo e alternativa, com a contabilidade de seleção pós-guarda explicitada;
3. robustez diante da Cefeida livre, decomposição PV, dos 13 e da covariância local–BG1;
4. previsões em dados/canais que não compartilhem os mesmos calibradores;
5. manutenção das linhas de estresse e da crítica de seleção em toda publicação posterior.

A sentença empírica, se vier, será uma convergência de testemunhas independentes, não um único número.

## 7. Declaração recomendada para o registro

> **A abertura V411 registra evidência confirmatória forte a favor da previsão TGL no modelo publicado: z_nulo = 6,105757534709, aproximadamente 6,11σ, com z_TGL = −0,605244103000, compatível com a previsão. O resultado é uma retrodição pós-guarda, não cega, obtida com pesos e pseudoinversa da colaboração, centragem BG1 e protocolo auditado. A linha Cefeida livre não discrimina. `NOT_FALSIFIED` não é `CONFIRMED`; o gate permanece imóvel e a teoria continua aberta a falsificação e confirmação independentes.**

## 8. Fontes e pinos

- `RESULTADO_DA_ABERTURA_V411.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v411_emenda_11nov\producao\RESULTADO_DA_ABERTURA_V411.json`  
  SHA-256 `573fbf87db2ccfe836e7672a3fd6b3bfc98d9fcb4d2ebce1d7cdb30d42abfbed`; bytes `51049`.
- `RECIBO_DA_ABERTURA_V411.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v411_emenda_11nov\producao\RECIBO_DA_ABERTURA_V411.json`  
  SHA-256 `57cc9a76ea83c40a52b2df1a8f4cc7c56eb226b2993441f17fe8ece9ec8ed2b9`; bytes `1696`.
- `EMENDA_E_PRE_REGISTRO_V411.md`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v411_emenda_11nov\EMENDA_E_PRE_REGISTRO_V411.md`  
  SHA-256 `06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8`; bytes `35322`.
- `REVISAO_FINAL_V411.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\ordem05\REVISAO_FINAL_V411.json`  
  SHA-256 `ce7f51b3d477d11e91d609a17f5127738b93c237b5b4a59c492ee0b56fb49fb9`; bytes `17613`.
- `ESTUDO_CONDICIONAL_R3B.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\ordem03B\ESTUDO_CONDICIONAL_R3B.json`  
  SHA-256 `24d42026500d864d85685de6cb2825e873a4826bc7cd26c4d5e8128e635ed8e3`; bytes `39871`.
- `DESENHO_RATIFICADO_H0DN_11nov.md`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\DESENHO_RATIFICADO_H0DN_11nov.md`  
  SHA-256 `c62858c238efea54fdbabe38e3983a8ac4415bf3070d5238b48223996bf1f6d4`; bytes `5231`.
- `ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md`  
  SHA-256 `0ad5b0286fe56dce1c76a0e3febab96f91cc38146e90a3dc6e4e26a15d86808b`; bytes `11965`.

**Nenhum novo teste, ajuste, abertura ou alteração de gate foi executado para preparar este estatuto.**
