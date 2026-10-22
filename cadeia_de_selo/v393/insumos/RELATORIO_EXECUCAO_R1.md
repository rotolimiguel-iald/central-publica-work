# Regra ligada ao motor contínuo da v392

Unidade F1.REGRA.MOTOR. Por ordem de Luiz Antonio Rotoli Miguel; construção e registro em nome de codex-gerente-tgl, sob reivindicação própria. Execução sintética em cópia, com revisão independente.

## Resultado

[REAL — execução numérica] O consumidor `prove_decision_commutation` da v392 foi executado a partir dos cinco corpos de função originais, extraídos e conferidos por AST. O programa completo não foi importado. A nova regra participa do veredito: exige que a leitura do resultado corresponda ao alvo fixado no pré-registro. O alvo incompatível é recusado.

A rodada teve **76 verificações aprovadas e 241 pontos**, EXIT 0, em 1.881 s. O replay e o exame independente estão no recibo de revisão.

[REAL — compilação] 42 teoremas novos e 22 reutilizados; dois módulos recompilados independentemente com EXIT 0, apenas o trio permitido e zero `sorry`. Os dois `.olean` são idênticos aos da construção.

## Motor e regra

O motor existente usa E(X)=PXP+QXQ, com P=diag(1,1,0,0), Q=I−P, e

T_t(X)=E(X)+exp(−Γt)(X−E(X)).

Γ=β·τ_ref·ω_ref²/2; β=ALPHA_FINE_CODATA_2018·sqrt(e), recalculado em runtime. τ_ref=ω_ref=1 são unidades de referência declaradas. A grade fixa usa exposição u=Γt de 0 a 12. β afeta a conversão para tempo de referência; a curva em u não mede β.

A leitura pertence a Fix(E). Nesse espaço ela é fiel. O contrato da F1.REGRA.P1 determina a regra relativa ao alvo a: C(z) sse z=a, sob correção e completude explícitas. No runner, a igualdade é aproximada pela tolerância Hilbert–Schmidt pré-registrada; não se converte essa aproximação em igualdade Lean.

[REAL — composição formal] A candidata liga esse contrato a `IALDJones.orbit`, com continuidade, semigrupo, conservação da inscrição, limite e recusa persistente de alvo incompatível. O M4 concretiza o mesmo pinching, alvo e estado inicial do consumidor. A norma padrão de matrizes usada na prova Lean e a tolerância Hilbert–Schmidt do runner conservam seus escopos. A ponte com o motor vetorial `IALD.motor` tem enunciado próprio; ele não é identificado com o canal matricial. Também não se confunde pinching com a compressão de um único setor eXe.

## Números da rodada

| Grandeza | Resultado |
|---|---:|
| β calculado | 0.012031300400803142 |
| Γ em unidades de referência | 0.006015650200401571 |
| Complemento inicial | 0.7071067811865476 |
| Complemento final | 4.344614220088533e-06 |
| Erro máximo da leitura HS | 0.0 |
| Erro máximo do oráculo GKLS | 0.0 |
| Erro máximo do semigrupo | 2.4532694666933987e-18 |
| Dimensão complexa do espaço fixo | 8 |

O estado completo e a leitura foram guardados separadamente nos 241 registros da trajetória, com cadeia SHA256. A leitura satisfaz o alvo em toda a grade, inclusive no início. O estado bruto não passa pelo critério de igualdade aproximada nessa grade finita. A prova formal mantém o complemento não nulo em todo tempo finito quando inicialmente não nulo.

O espaço fixo deste canal tem dimensão complexa oito, medida sobre o operador completo. A unicidade da regra relativa ao alvo não é unicidade de todos os estados fixos. Uma entrada com outra inscrição permanece incompatível: o fluxo preserva a inscrição, e a regra detecta a divergência.

## Controles e limites

O oráculo independente reconstruiu o gerador GKLS a partir dos operadores de salto e sua exponencial. Foram conferidos todos os 16 elementos de base matricial, semigrupo, traço, Hermiticidade e positividade dentro da tolerância. NaN, infinitos, booleanos, taxa inválida, estado inválido, alvo não fixo, evidência ausente e fonte corrompida são recusados. O controle de taxa zero preserva o complemento.

[INPUT/ONTO] A lei temporal homogênea e sua identificação com as cunhagens conservam o estatuto declarado. A rodada é cálculo sintético, sem dado observado e sem confirmação física. Nenhum habitante Fock, H3 ou solução global é produzido por esta integração.

Foi executada uma trajetória de tempo contínuo, amostrada em grade finita. A execução termina com recibo; o runner pode ser repetido usando o mesmo freeze e sempre cria outra pasta de resultado. Não é um serviço residente. A Bancada de produção consultada estava na implantação B3-v392; a nova integração permanece neste sandbox, com os originais preservados.

## Evidências e repetição

- Execução: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\runtime\runs\20261014T142949_979804Z\RESULT.json` — SHA256 `5052cb5ca2c2df02ed9bc9bd0592d046a07e7a86497ff22d971a4721b144fac8`.
- Build Lean: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\attempts\20261014T143143_185233Z\RESULTADO_BUILD.json` — SHA256 `8efe4aa5bc67fad0c8b96e2d9990f2ae3b9ee8fffa6b11e2a577dca795bde48a`.
- Revisão independente: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\review\REVIEW_RESULT_R1.json` — SHA256 `187647c7a625c01ed3aee646c84be8fef52016ccd9088e6f58a4776a91c1bac3`.
- Pré-registro: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\PREREGISTRO_R1.json` — SHA256 `a224a6cd80ab3834f497074a56db0113331f4f669b86335e45ee27b08c9b7fe3`.
- Fonte e selo: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\SOURCE_MANIFEST.json` — SHA256 `ea43204aaa9254e08f9cbd2b5505e499d8497b0b2507dfba5b5a00c959be8645`.
- Estado lido da Bancada: `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\BANCADA_STATE_R1.json` — SHA256 `a224a6c3d737689b773e784613a5b4b6cc7349be48e1b225bf14a057fe31e84c`.

Comando de replay (qualquer diretório de trabalho):

```powershell
& "C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -B "C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\runtime\run_rule_motor.py" --replay "C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REGRA.MOTOR\runtime\freezes\20261014T142932_627224Z.json"
```
