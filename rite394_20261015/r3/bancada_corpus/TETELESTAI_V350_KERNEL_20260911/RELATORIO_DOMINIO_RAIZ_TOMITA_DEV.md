# Igualdade exata D(B)=D(S) e energia no domínio inteiro — DEV

2026-09-12T12:34:57-03:00. [REAL — seis módulos/25 alvos compilados; revisão independente e integração pendentes]

O operador continua sendo S, fecho do gráfico original A↦A* no H_I construído
para o ideal finito. Seu adjunto máximo fornece A=S†S e a etapa anterior fornece
a raiz positiva auto-adjunta B com B²=A como mapas parciais. Não se troca peso,
representação, suporte ou modelo espectral para obter a igualdade de domínios.

1. No gráfico REAL fechado de um mapa real-linear, uma família resolvente fraca
   com valores em C mostra que o gráfico restrito a C tem complemento ortogonal
   zero no gráfico inteiro. Seguem sequências convergentes em ambas as coordenadas.
2. Para S, a equação u+Au=z e o pareamento com o adjunto provam que D(A) é núcleo
   do gráfico de S. Não se usa somente densidade na norma de H_I.
3. Para B, simetria e B²=A fornecem o pareamento contra TODO D(B); a mesma família
   resolvente mostra que D(A) é núcleo do gráfico de B.
4. As normas de S e B em D(A) são iguais, pelo quadrado da energia já provado.
   Em cada aproximação de gráfico, a sequência de imagens pelo outro operador
   é Cauchy porque as normas de todas as diferenças coincidem. Completude de H_I
   e fechamento do gráfico do outro operador dão a inclusão de domínios.
5. Aplicado nos dois sentidos, isso dá D(B)=D(S). A continuidade da norma e a
   unicidade dos limites dão ‖Bx‖=‖Sx‖ e ‖Bx‖²=‖Sx‖² em TODO esse domínio.

Todos os 25 alvos usam apenas propext, Classical.choice e Quot.sound. Os lemas
genéricos exibem suas hipóteses; os seis alvos finais de ScalarTomitaRootDomain
usam somente P e os vetores tipados. Não recebem a igualdade final como premissa.
Os domínios são submódulos, com inclusões e igualdade de subtipos explícitas.

[OPEN] O fator antiunitário polar ainda não foi construído neste pacote. KMS,
identificação com o peso e seu domínio máximo, traço canônico e escala dual,
canto contínuo/Three Locks, H1/H2/H3 físicos compatíveis, setor quântico interagente,
contrato completo consumido pelo gate e runtime integral continuam pendentes.
D(B)=D(S) não afirma D(B)=H_I, invariância de D(B) sob B ou gap espectral.

Os relatórios anteriores que registravam esta igualdade como aberta permanecem
históricos. `graph_core_draft_status.json` era o corte de dois módulos/10 alvos;
este manifesto novo amplia esse corte sem editar seus bytes. O novo pacote não
foi incorporado às contagens integradas de cinco/30 da raiz.

Tentativas rc1 preservadas: colisão de nome de instância real, sentido de uma
identidade de produto interno, coerção de subtipo, inclusão explícita de uma
hipótese de seção e timeout de reescrita no tipo concreto. O timeout foi resolvido
com termos explícitos de igualdade, sem elevar a conclusão a axioma. Logs com
sorryAx ou sem binário válido não compõem a evidência aceita.

Cópia integrada antecedente: `7ec13a8b82350390c7ef32d9319910398541b8966ecf5f28e928c492a626eb6a`.
Mãe de custódia: `c2d6675fffdd6d96e2a8196d25b9170f69549dd75f7e411b633013c04c54dffe`. Nenhuma promoção de gate ou execução do monólito.
