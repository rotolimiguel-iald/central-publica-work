# Reconstrução documental A1 — raw_MAS escolhido; Etapa 1 incompleta

**Estado:** `RAW_MAS_DECIDED__STAGE1_INCOMPLETE__STAGE2_NOT_AUTHORIZED`  
**Estatuto:** `[DECLARADO pelo Kimi]` até a gerência conferir.  
**Escopo:** apenas fontes públicas e código. Nenhum vetor observado, saída observada, solver, `evaluate`, D, H0, razão, semente ou conferência das 72 identidades.

## 1. Resultado documental

A fonte decide **`center_convention = raw_MAS`**: os centros `mu_host` são copiados como valores reportados, com a referência MAS/âncora já embutida, sem somar nem subtrair `mas_ref_value`.

A Etapa 1 **não pode ser declarada completa**. Faltam:

1. a ponte inequívoca de cada uma das 111 células até os centros dos fits R22, incluindo a inconsistência de numeração dos fits;
2. a equação de formação do centro HMS compartilhado ou o produto que demonstre `ε_k + o_a`;
3. a regra de quantização das células decimais ou os centros em precisão completa;
4. consequentemente, as 72 tolerâncias de produção.

O `MANIFESTO_VARIANTE.json` fica, portanto, `INCOMPLETE_NOT_AUTHORIZED`. A Etapa 2 permanece proibida.

## 2. Cadeia tabela → produtos R22 → fits → MAS/HMS → centro

### 2.1 Tabela de Cefeidas e produtos compactos

A Data Release orienta usar os produtos compactos `y`, `L` e `C`, e não remontar a escada apenas a partir da Tabela 2. Os arquivos `ally_...fits`, `alll_...fits` e `allc_...fits` representam, respectivamente, vetor, equações lineares e covariância. [table2.README](kimi-cite://web?url=https%3A%2F%2Fraw.githubusercontent.com%2FPantheonPlusSH0ES%2FDataRelease%2Fc447f0fea703fcd0fff57de5000947b5ca81286b%2FSH0ES_Data%2Ftable2.README "citation"), [shoes_README](kimi-cite://md-line?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fastra_bell_fock_tt_05nov%2Fh0dn_bg1_06nov%2Fcross_rung%2Fshoes_README.md&line=6&text=The%20data%20is%20provided%20in%20the%20compact%20matrix%20form%20(linear%20equations)%20given%20in%20the%20paper "citation")

Esses produtos não fornecem, por si sós, três conjuntos separados de centros para os fits de uma âncora nem a precisão necessária para as 111 células.

### 2.2 Identidade e numeração dos fits

R22, Table 5, p. 28, identifica fit 9=`none`, fit 10=`N4258`, fit 11=`Milky Way`, fit 12=`LMC`; §6.2, p. 38, trata das variantes com uma ou duas âncoras. [R22 Table 5](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2112.04510%23page%3D28 "citation"), [R22 §6.2](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2112.04510%23page%3D38 "citation")

O H0DN, contudo, escreve “N4258, MW, LMC (R22a fits 9,10,11”. [H0DN_paper_v1](kimi-cite://text?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fastra_bell_fock_tt_05nov%2Fh0dn_bg1_06nov%2Fcross_rung%2FH0DN_paper_v1.html&text=SN%20hosts%2C%20separate%20measures%2C%20N4258%2C%20MW%2C%20LMC%20(R22a%20fits%209%2C10%2C11) "citation")

R22 Table 6, p. 30, apresenta aproximações dos parâmetros de distância, não um mapa completo de três centros por hospedeiro. [R22 Table 6](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fpdf%2F2112.04510%23page%3D30 "citation")

**Lacuna preservada:** é necessário esclarecer se “9,10,11” é erro de citação, numeração interna ou referência a outro produto, e obter versão, índice de parâmetro e centro completo de cada célula.

### 2.3 As 111 linhas e suas exclusões

- N4258: `host_data.dat:4–40`, com N7250 seguido dos 36 hospedeiros A1;
- LMC: `host_data.dat:98–134`, na mesma ordem;
- MW: `host_data.dat:139–175`, novamente na mesma ordem.

São \(37\times3=111\) células. As autorreferências MAS estão em `host_data.dat:3`, `:97` e `:138` e não participam das identidades. `host_data.dat:93` contém N4151 fora dos 37 tripletes; filtrar apenas método/âncora/fonte produziria incorretamente 112 linhas em N4258. A montagem usa lista explícita e exige exatamente uma ocorrência por hospedeiro/âncora.

### 2.4 MAS e HMS

`data_loader.py:65–95` constrói `mas_name = method & anchor & source` e `hms_name = host & method & source`. Assim, os tripletes têm MAS distintos por âncora e o mesmo HMS dentro de cada hospedeiro. As linhas de autorreferência fornecem `mas_ref_value` (`data_loader.py:328–400`), e `mu_hms_error` deriva dos mesmos `mu_error` (`data_loader.py:493–505`). [data_loader](kimi-cite://text?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fastra_bell_fock_tt_05nov%2Fh0dn_bg1_06nov%2Fnetwork%2Fupstream%2Fh0_constrainer%2Fh0_constrainer%2Fdata_loader.py&text=mas_ref_value%20%3D%20host_df.loc%5Bis_anchor%2C%20%22mu_host%22%5D.values "citation")

As 111 linhas têm `mu_error` idêntico dentro de cada tripleto. Isso sustenta compartilhamento da incerteza, mas não prova sozinho a decomposição dos centros.

### 2.5 Prova de `raw_MAS`

- `equations.py:334–345`: `yval[ieq] = host_df.iloc[k]["mu_host"]`;
- `equations.py:348–376`: geometria, MAS e HMS entram depois na covariância;
- `org_v3p9.pro:1410–1417`: a equação reúne âncora e diferença hospedeiro–âncora em uma única constante e usa `yval[ieq]=mu_host2_value[k]`;
- a busca no upstream encontra `mas_ref_value` em metadados, não em correção do centro. [equations.py](kimi-cite://text?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fastra_bell_fock_tt_05nov%2Fh0dn_bg1_06nov%2Fnetwork%2Fupstream%2Fh0_constrainer%2Fh0_constrainer%2Fequations.py&text=yval%5Bieq%5D%20%3D%20host_df.iloc%5Bk%5D%5B%22mu_host%22%5D "citation"), [org_v3p9](kimi-cite://text?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fastra_bell_fock_tt_05nov%2Fh0dn_bg1_06nov%2Fnetwork%2Fupstream%2Fidlcode%2Forg_v3p9.pro&text=yval%5Bieq%5D%20%3D%20mu_host2_value%5Bk%5D "citation")

Logo, `mu_host` já é o centro absoluto na referência MAS. Aplicar nova soma/subtração removeria ou duplicaria uma transformação embutida. Não há suporte no código para `documented_MAS_corrected`.

### 2.6 O que falta para provar o centro compartilhado

H0DN B.3.2 declara covariância entre equações que compartilham hospedeiro, método e fonte. [H0DN_paper_v1](kimi-cite://text?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fastra_bell_fock_tt_05nov%2Fh0dn_bg1_06nov%2Fcross_rung%2FH0DN_paper_v1.html&text=If%20two%20equations%20share%20the%20same%20host%20measured%20by%20the%20same%20method%20and%20source "citation")

A hipótese A1 é `y_{k,a}=ε_k+o_a`, com offsets apenas por âncora, levando às segundas diferenças nulas, sem exigir tripletes iguais. Contudo, compartilhar incerteza não demonstra que três fits globais independentes produzam necessariamente essa forma. É necessário obter a equação de formação ou o produto full-precision; **não se pode corrigir centros até que ela seja satisfeita**.

## 3. Precisão e quantização

### 3.1 Precisão textual verificada

As 111 células `mu_host` têm exatamente **três casas decimais**, portanto `q=0,001 mag` em todas. As autorreferências MAS não entram no cálculo.

### 3.2 Regra de quantização: `OPEN`

Nenhuma fonte examinada declara se as células foram arredondadas ao mais próximo, truncadas ou exportadas por outra regra. Também não foram localizados os três conjuntos full-precision de centros de uma âncora.

Por isso, **não se pode adotar automaticamente \(b=q/2\)**. O protocolo exige conhecer a regra; se desconhecida, manda não abrir.

### 3.3 Fórmula condicional — NÃO ADOTADA

Somente se uma fonte primária confirmar arredondamento simétrico ao mais próximo com `q=0,001 mag`, então `b=0,0005 mag` e, como `raw_MAS` não aplica transformação adicional:

\[
\tau_k^{NL}=\tau_k^{NM}=4\times0,0005+10^{-12}=0,002000000000001\ {\rm mag}.
\]

Seriam 36 tolerâncias NL + 36 NM iguais. **Essa fórmula não está congelada nem autorizada.** Se forem usados valores full-precision diretamente, a camada documental teria `b=0`, restando `τ_num=1e-12 mag`.

## 4. Validação exclusivamente sintética

`montar_variante.py` implementa a seleção explícita, `raw_MAS`, a construção A/C/y e as 72 identidades. Em fixtures fictícios:

- 72/72 identidades brutas e 72/72 em `y=Aθ` passaram;
- maior resíduo bruto: `1,7764e-15 mag`;
- N4151 e autorreferências MAS foram excluídos;
- posto R22 39, nulidade 72 e posto das restrições 72;
- offsets MAS não nulos confirmam que tripletes não foram forçados iguais;
- manifesto incompleto, quantização aberta, tolerâncias ausentes e Etapa 2 não autorizada foram recusados pelo guard.

O fixture cobre apenas o subsistema R22 de hospedeiros; não valida a rede completa, a proveniência dos centros reais, a covariância física ou qualquer resultado observado.

## 5. Parada e produtos necessários

Antes de completar o manifesto são necessários:

1. mapa completo dos 111 centros, versão e índice de parâmetro por célula;
2. esclarecimento da numeração H0DN `9,10,11` versus R22 `10,11,12`;
3. equação de formação do centro HMS ou produto full-precision que demonstre `ε_k+o_a`;
4. regra de quantização ou centros full-precision;
5. só então as 72 tolerâncias, revisão da gerência e autorização explícita da Etapa 2 pelo operador.

Nenhuma conferência observada está autorizada nesta entrega.

## 6. Pinos documentais

| Fonte | SHA-256 |
|---|---|
| `ORDEM_KIMI_H0DN_04_11nov.md` | `72ab3d8fd34f56368d43f6a3c59f2c2351bb3e5ceb98c9e1bed9c7d39fdbd5d0` |
| `H0DN_paper_v1.html` | `6bc786e733a61606ee29d5bb120d48ba2de48a3484f2c387d14e0417d94a64f5` |
| `shoes_README.md` | `fd845e484a184ad9740dddf26550db9d6d154d1631c1b30622dcecefe8ee7174` |
| `host_data.dat` | `256ae37259e7bc000c4909811787d0e44816eb947e96eb0d3fb3ffbc767dffad` |
| `data_loader.py` | `0fe032b09dcba71bd6f602dabd7e3873a369fc09f8cf340b01584b9b31bf7c04` |
| `equations.py` | `1b4f8f81cd6f75cc241156ae1dbb80199cf4e58ab5752a0d5e4d2e9dff367236` |
| `org_v3p9.pro` | `49a4cf6cfcb3805a103f7060c10137431f3285c5d74144445de56a821052e501` |
| `rows.json` | `d2ee266974aba622d02e436346fc1ff63c228adf86b66f76b2574e813fe17b84` |
| `PROTOCOLO_CONFERENCIA_FUTURA.md` | `db74c3f866128276361abd932af721394126615903a899a8dae1880099e566f8` |
| `A1_HIPOTESES_DO_VETOR.md` | `e45a0f0dbe67dc502eaaf0674a9477466c2dd6b78c3627a6bd7cfe587878aeae` |

**Flags:** `observed_vector_read=false`; `observed_support_tests=0`; `solver_called=false`; `estimator_evaluate_called=false`; `D_H0_or_ratio_computed=false`; `new_seed_or_monte_carlo=false`; `freeze_R2_v410_or_gate_modified=false`.
