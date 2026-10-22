[REAL — Lean] Família de esperanças dos andares construída e verificada. [DERIVED] Obstrução à determinação da escala métrica. [OPEN] Esperança sobre o centralizador e rede CGMA da torre.

# ENTREGA 001 — esperança condicional e escala

05/09/2026 · DE: bancada ChatGPT · PARA: sessão irmã Claude/gerência · RESPONDE À ORDEM 001.
Entrega imutável para auditoria; nenhuma aprovação adversarial ou mudança de gate é declarada.

## Resultado

Foram construídos oito módulos, com **42 teoremas**, todos compilados com saída 0, sem avisos, `sorry` ou novos axiomas. `constructedLevelExpectations P` é um termo de `LevelExpectationFamily P`; seus campos são preenchidos por provas, não assumidos. `E_N` é definido a partir de p_N xΩ, decodificado no andar e representado em H.

`expectation_step_slice` identifica essa construção com a fatia ponderada no passo N+1→N. A compatibilidade da torre permite iterar os passos. A demonstração escrita foi criada antes do Lean em `ESPERANCA_CONDICIONAL_TORRE.md`.

## Critérios da ordem

| Alvo A | Estatuto | Evidência |
|---|---|---|
| 1. Mapa linear limitado, imagem no andar | PAGO [REAL — Lean] | `expectationCLM; expectation_bounded; expectation_into` |
| 2. Idempotência | PAGO [REAL — Lean] | `expectation_idempotent` |
| 3. Restrição ao andar | PAGO [REAL — Lean] | `expectation_fixes` |
| 4. Preservação de ω | PAGO [REAL — Lean] | `expectation_preserves_state` |
| 5. Bimodularidade sobre M | PAGO [REAL — Lean] | `expectation_bimodular` |
| 6. Positividade sobre M | PAGO [REAL — Lean] | `expectation_positive (ordem de Loewner)` |
| 7. Comutação com σ_t | PAGO [REAL — Lean] | `expectation_flow_commutes` |
| 8. Cadeia E_M E_N = E_min(M,N) | PAGO [REAL — Lean] | `expectation_tower` |
| 9. Distância exata ao contrato importado | PAGO [REAL — Lean] | `expectation_not_imported_contract; ver ressalva abaixo` |

**Ressalva do item 9:** o pagamento é a alternativa expressamente permitida na ordem: medir a distância entre tipos. `ExpectationInput` exige imagem no centralizador inteiro, não em um andar. Para P.w(0)≠1/2, a impossibilidade de identificar os dois mapas sobre M é teorema Lean. Não foi produzido `TakesakiInput` nem uma esperança sobre `omegaCentralizer`.

**Positividade completa:** demonstrada por compressões/amplificações no texto [DERIVED]; NÃO PAGO em Lean. A positividade simples exigida pelo item 6 está integralmente verificada. Normalidade, fidelidade e norma 1 da restrição a M estão justificadas no texto, sem formalização adicional. O mapa limitado foi construído em B(H); a positividade e a bimodularidade são afirmadas com a hipótese x∈M, como requer a ordem.

| Alvo B | Estatuto | Resultado |
|---|---|---|
| 1. Rede pretendida | PAGO como especificação escrita | Obrigações de localização, cunhas, interseções, standardness, dualidade e ação modular explicitadas. Rede CGMA da torre ainda [OPEN]. |
| 2. Cones + escala dual determinam métrica | PAGO como refutação da suficiência | A mudança g↦c²g preserva cones, as mesmas ações geométricas e os dados do core sem uma ponte métrica. Controle exato: R(g)=12 e R(4g)=3, logo não isométricas. |
| 3. Dado ausente | PAGO | Medida geométrica localizada e calibrada; mapa demonstrado ligando τ a volumes/áreas. Uma densidade de volume positiva fixa o representante conforme. |

`BisognanoWichmann.lean` fornece a forma exponencial do boost, sem identificar a ação dual no core com esse boost. O molde de escala lido está em `GlobalLiftLadder.DualScalingData`. A rede `WedgeNet` tem translações triviais e não distingue posições de cunhas direitas; seu contrato fraco não resolve a localização CGMA. O contraexemplo de escala não pretende construir uma rede de de Sitter a partir da torre.

## Arquivos, SHA256 e contagens lidos por script

| Fonte Lean — caminho absoluto | Teoremas | SHA256 |
|---|---:|---|
| `C:\IALD\Central de Patentes\Chatgpt\TowerExpectation.lean` | 12 | `8831E132B3F4F7124B7F606B25C9FB9F2E720AA6EDB0D06A0815BFA38922082F` |
| `C:\IALD\Central de Patentes\Chatgpt\ExpectationProjection.lean` | 8 | `6C5C91A28B6FC09E99893311B8A3CCAFAEDEAA4DB59078528FC310F48B064869` |
| `C:\IALD\Central de Patentes\Chatgpt\ExpectationBounded.lean` | 1 | `F2EDC8107FE0A4AEF2B0BB290C1E46CDDD45470CE0F8A964CA3A43356FDA28B0` |
| `C:\IALD\Central de Patentes\Chatgpt\ExpectationBimodule.lean` | 8 | `11D08847439D90CA1BBFC20785258DE29ABF871871BA304AE580E6414DE10B77` |
| `C:\IALD\Central de Patentes\Chatgpt\ExpectationPositive.lean` | 7 | `A04C1F255A529FBBD549F2CC3A413D0489B1C1CDB956E65B7227710DA3A0FB55` |
| `C:\IALD\Central de Patentes\Chatgpt\ExpectationSlice.lean` | 2 | `448A6E323AE6AF6C2F149E7CC8700B4CF84DAD5C7251B031F753E6C0007EA3FD` |
| `C:\IALD\Central de Patentes\Chatgpt\ExpectationContractGap.lean` | 3 | `B89DC982392F0D7B2FFE67296997E6AB7F5F9EB97A8DCCD468D58DC31DE0A69D` |
| `C:\IALD\Central de Patentes\Chatgpt\LevelExpectationFamily.lean` | 1 | `EEF13EEBD904FE1713C6DDA8A62670FC440C36269F1260D9D7E625D5658644D4` |

Outros artefatos:

- `C:\IALD\Central de Patentes\Chatgpt\ESPERANCA_CONDICIONAL_TORRE.md` — `F959C835C432088C84E3BDBC5A876D82C962C60398D564B9FE8895989690A30F`
- `C:\IALD\Central de Patentes\Chatgpt\ESCALA_CONFORME_TAKESAKI.md` — `5CBACF7E7D39FA1D438E61DDB9BE07526E3F368C091B21FBAB82ACAA82B5F7A4`
- `C:\IALD\Central de Patentes\Chatgpt\check_scale_obstruction.py` — `2D33502BC2D1A3A6CC5ABDF87E7600C37FC713FA0DF9926A71F9400F19464F7C`
- `C:\IALD\Central de Patentes\Chatgpt\reproduce_order001.ps1` — `22F2DD1016559AE61E604F2B98B591E28BF1EAE5C49DE4C5829F95680B808AF8`
- `C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1` — `B882654A42E31A2BDE50C8538009C1FD8373F50DDEEAE14A683CD32445E4A923`
- `C:\IALD\Central de Patentes\Chatgpt\finalize_order001.py` — `6BBDF0357BC2E40694649761C35CE2AD54D6D06527BA3B3B61D565AF05627801`
- `C:\IALD\Central de Patentes\Chatgpt\escala_controle_20260905_120327.json` — `AE5C0388AD05A72E4D4CBF780C70EF45F8CE0C1C77AA6F25410D0F69C6998F7E`
- `C:\IALD\Central de Patentes\Chatgpt\preservacao_ordem001_20260905_122502.json` — `4FBC494E3C34A1B9D9BA9F6E2949894F47E40E8F7ECAFFB4FBF0EB4C3A560304`
- `C:\IALD\Central de Patentes\Chatgpt\dependencias_ordem001_20260905_122502.json` — `FA0E9863F189C542CD3069AF7A71B9C37FCC3C8D63D42A4611303BF5C7A6B0A8`
- `C:\IALD\Central de Patentes\Chatgpt\verificacao_ordem001_20260905_122502.json` — `34D453D3B313E3483B6A96D6AE2FE46104396DA54C158AC77798EC1356C7560D`

## Reprodução nesta máquina

```powershell
& 'C:\IALD\Central de Patentes\Chatgpteproduce_order001.ps1'
```

O script recompila os oito módulos em ordem e repete o cálculo simbólico. Usa Lean 4.31.0, as provas anteriores da bancada, o snapshot binário dos módulos TGL/TGLExt e a mathlib instalada. Não é um build limpo da biblioteca inteira. Os arquivos de entrada TGL.lean/TGLExt.lean foram copiados da fonte preservada; as dependências binárias foram copiadas para a bancada após colisão com incorporações simultâneas da sessão irmã. O manifesto de dependências registra o snapshot usado.

## Axiomas efetivamente impressos

`TowerExpectation` — log `C:\IALD\Central de Patentes\Chatgpt\TowerExpectation.20260905_120646.log`, SHA256 `51DC1C5F07BA7ED558D4DB457A232F7E17C53E313F31BCCDE39333B124D36FE0`:

```text
'ChatgptAudit.expectation_fixes' depends on axioms: [propext, Classical.choice, Quot.sound]
'ChatgptAudit.expectation_idempotent' depends on axioms: [propext, Classical.choice, Quot.sound]
'ChatgptAudit.expectation_preserves_state' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`ExpectationProjection` — log `C:\IALD\Central de Patentes\Chatgpt\ExpectationProjection.20260905_120737.log`, SHA256 `66D7C6E2E0346D5EBDB91E0AFA5931ABBEC016AD0CC034242FB6A4E11412E527`:

```text
'ChatgptAudit.expectation_tower' depends on axioms: [propext, Classical.choice, Quot.sound]
'ChatgptAudit.expectation_flow_commutes' depends on axioms: [propext, Classical.choice, Quot.sound]
'ChatgptAudit.expectation_omega_limit' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`ExpectationBounded` — log `C:\IALD\Central de Patentes\Chatgpt\ExpectationBounded.20260905_120740.log`, SHA256 `EA00F4641B5F58586988C403C0AD08594EB34B3B38313DE6F9B6D53569BFC591`:

```text
'ChatgptAudit.expectation_bounded' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`ExpectationBimodule` — log `C:\IALD\Central de Patentes\Chatgpt\ExpectationBimodule.20260905_120907.log`, SHA256 `500A6CFB56933286BCBD6550B9256BF04E71D2F2C5E304805C88B98194C3D98F`:

```text
'ChatgptAudit.expectation_compression' depends on axioms: [propext, Classical.choice, Quot.sound]
'ChatgptAudit.expectation_bimodular' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`ExpectationPositive` — log `C:\IALD\Central de Patentes\Chatgpt\ExpectationPositive.20260905_121935.log`, SHA256 `47F97AEC297D7476B68622BE8112707954C76CFF9C12BDF45F916302B090CA4B`:

```text
'ChatgptAudit.expectation_star' depends on axioms: [propext, Classical.choice, Quot.sound]
'ChatgptAudit.expectation_positive' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`ExpectationSlice` — log `C:\IALD\Central de Patentes\Chatgpt\ExpectationSlice.20260905_121800.log`, SHA256 `453C1D15EF8E5CD13B4F3C9FC9B5C8FE4FEAE7DA4B35B4B97EBF456F011F8359`:

```text
'ChatgptAudit.expectation_step_slice' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`ExpectationContractGap` — log `C:\IALD\Central de Patentes\Chatgpt\ExpectationContractGap.20260905_121325.log`, SHA256 `24466B5FDDA6C3B7C47B2309B05935606FA6256C2680A4EC9C20B54D9D6A9D20`:

```text
'ChatgptAudit.expectation_not_imported_contract' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`LevelExpectationFamily` — log `C:\IALD\Central de Patentes\Chatgpt\LevelExpectationFamily.20260905_122049.log`, SHA256 `B02E6A20608CA891C8C1C6F7BA485312B36D4AF6035E2EBE115E1474341EEB33`:

```text
'ChatgptAudit.constructedLevelExpectations' depends on axioms: [propext, Classical.choice, Quot.sound]
'ChatgptAudit.level_expectation_family_exists' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Preservação e limites

As 290 cópias-fonte preservadas em `fontes` continuam byte a byte iguais ao manifesto inicial. A comparação dos caminhos originais registrou **2 divergências ou falhas de leitura** em relação àquela linha de base; o JSON lista cada estado. Hashes não identificam autoria, e há incorporação concorrente pela sessão irmã. Esta bancada escreveu somente sob Chatgpt; não editou um.py, kernel canônico, Atlas, selos, diários ou a via PARA_CHATGPT.

Não foram feitos: prova Lean de positividade completa/normalidade, construção do core contínuo com traço, esperança do centralizador, identificação modular com tempo próprio, rede CGMA fiel da torre, reconstrução gravitacional geral ou avaliação física. Não se alterou nem se declarou gate.

## Tentativas falhas preservadas

As tentativas de elaboração, imports indisponíveis, colisão de nomes, timeouts e avisos estão preservadas por cópias de bytes com sufixo do defeito. Elas não são os logs aprovados acima.

- `C:\IALD\Central de Patentes\Chatgpt\TowerExpectation.20260905_115550.log.falha_elaboracao` — `27F23482A0F4EF0AEA343CC6DA4BED1AD759B318E4300B6DB60C6F2FF5BD8B84` (elaboracao).
- `C:\IALD\Central de Patentes\Chatgpt\TowerExpectation.20260905_115658.log.falha_dependencia_ausente` — `8A24EEB93F10F30C7B8D9A34AB656F62FA1A73257B4BA3E5434438DAB2650835` (dependencia_ausente).
- `C:\IALD\Central de Patentes\Chatgpt\TowerExpectation.20260905_115945.log.falha_colisao_imports` — `A91F9E9CF922B751D6DF2824D875F92FD1D2EE06D245239D9878D5A589FB3B45` (colisao_imports).
- `C:\IALD\Central de Patentes\Chatgpt\TowerExpectation.20260905_120522.log.falha_elaboracao` — `2635FB8A83F030046C6783F03F63A4CA7352CA9FFE4145D80FE743DCCB2295AC` (elaboracao).
- `C:\IALD\Central de Patentes\Chatgpt\ExpectationPositive.20260905_121051.log.falha_elaboracao` — `1E52D6876744144FBD332936E433711BE4A3C4699F009484E36736CBBBB78B97` (elaboracao).
- `C:\IALD\Central de Patentes\Chatgpt\ExpectationPositive.20260905_121230.log.falha_timeout` — `E5A36D35394CFD24EFD91D2B069FA134FD3AC25A56F9B6A1A3294AC12572E0AD` (timeout).
- `C:\IALD\Central de Patentes\Chatgpt\ExpectationPositive.20260905_121540.log.falha_timeout` — `4A7E49205292D905B82B1F9763A3A8457DCA3489C4A5D9F792C5FE4D20D223E9` (timeout).
- `C:\IALD\Central de Patentes\Chatgpt\ExpectationPositive.20260905_121756.log.falha_elaboracao` — `B63ED9269818DDC02FDBC4193C3F3D11F17C19FD2C22BE374232141DE7A977CF` (elaboracao).
- `C:\IALD\Central de Patentes\Chatgpt\ExpectationSlice.20260905_121442.log.falha_elaboracao` — `93CF6425B7DA9DAE759A028FEA9AE8A229C27D2BA208C045A247156E50323A2B` (elaboracao).
- `C:\IALD\Central de Patentes\Chatgpt\ExpectationSlice.20260905_121613.log.falha_aviso_linter` — `A871D9AFB4B427371BDDD33CA763ECC294C0555A363E5600C86FE9D586F60E08` (aviso_linter).
- `C:\IALD\Central de Patentes\Chatgpt\TGLExt.20260905_120311.log.falha_dependencia_ausente` — `EAA9EF3D427C2DE135232C9A7F6473195210DF83D9D5AE8760ED43D885C8E449` (dependencia_ausente).

Houve ainda uma execução sem acesso ao SymPy no sandbox: `ModuleNotFoundError`. A execução posterior com acesso ao runtime instalado passou; o resultado JSON exato está listado acima. Esta anotação é um registro da ocorrência, não um log fabricado.
