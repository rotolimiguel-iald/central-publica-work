[REAL — medição e reconstrução autoral; não aceite independente]

# Recibo g — os três objetos B6

Os três fontes são byte-idênticos entre as raízes B6 kernel e s. Os três objetos recompilaram com Lean 4.31 em saídas desta raiz; nenhum dos novos hashes coincide com os dois hashes históricos correspondentes. Não se substituiu objeto nas raízes B6.

A causa foi delimitada por bytes: MixedLadder e SecondCone contêm o caminho absoluto do respectivo fonte. Todas as diferenças entre cada par histórico ficam na janela do caminho e dos 24 bytes anteriores. Não há diferença de bytes fora dessa janela nesses dois pares. Os três inteiros little-endian observados imediatamente antes da string variam junto com seu comprimento; não se presume uma especificação completa de layout a partir disso.

AreaScale também contém caminhos distintos, mas sua diferença não se restringe à janela: o arquivo da raiz s tem oito bytes a menos e há alterações adicionais. Não foi reconstruída integralmente a correspondência das posições/referências internas do par histórico. A causa de cada byte dessa divergência continua OPEN.

O ensaio controlado ABA de AreaScale usou o MESMO fonte físico, o MESMO setup, os MESMOS imports, cwd, ambiente e destino. Somente o argumento do fonte mudou entre caminho absoluto e relativo. As execuções A tiveram comandos idênticos e objetos byte-idênticos; B teve objeto diferente. Os caminhos correspondentes estão literalmente presentes nos objetos. Isso demonstra nesta bancada que a grafia do caminho de entrada afeta o objeto serializado; não é uma hipótese de tempo aleatório nem reconstrução de toda a história das duas raízes antigas.

O registro de inputs Lake de AreaScale coincide após normalizar apenas a raiz textual. MixedLadder e SecondCone divergem também no hash de imports transitivos legacy. Os setups dos três pares, normalizados apenas nas raízes, coincidem. O inventário mais amplo das entradas importArts leu 34251 artefatos referidos e encontrou 19 divergências nesse conjunto; esse universo é maior que os três alvos da ressalva B6. Não se atribui automaticamente causalidade desses imports às divergências dos alvos.

A auditoria específica importa os TRÊS objetos recém-compilados por um setup explícito. As 25 declarações auditadas ficaram no subconjunto de propext, Classical.choice, Quot.sound. Os streams e o mapa importArts são preservados. O hash binário não substitui a auditoria do enunciado e dos axiomas.

| Módulo | SHA256 fonte nas duas raízes | SHA256 .olean kernel | SHA256 .olean s | SHA256 novo |
|---|---|---|---|---|
| `TGLExt/MixedLadder` | `eb43ba5a3ee66412f7f4704a7a435f485f1e53a315188e4f9bb46234f757f861` | `6a7edf2fb0eef2b75d4c411e6d82aff47a5477f0e060fa6db0f98ea3dcd4fd37` | `88cfc0be4eb71e09bde437128ac382d0c889c3d6e553a6e126f1f44d6a8a75f8` | `b4c9bf26ecb667c683af796a932be16bc1124988c1a53b4a0caece65564299b6` |
| `TGLExt/SecondCone` | `9bafc9fcbf9fc6eb98f17d2e3122ac01820bc0785e64fb63eb6eef8c0c276e45` | `bd71610eb7c50bd87ad23590c3f6ef85e9d5f7df4b540c29f9791d64e5db33ad` | `5ad145d1c32240a88cfc77aa38fdfe8f6a7f895cb5ef77dd65f8ff2e46b5e314` | `e30ce790540f3f6133d4333078f3f4e63d594e541bcab18d4046229f62f32bbe` |
| `TGL/AreaScale` | `7058ae26f99f44f2d81d0c51e39bf435359a94c410405e52da4c4a44834ce075` | `2baa467855ecf4ae5f35199f52659a2f00030acc9c5f9eef7a4cae5f8b5f7c0b` | `a3a200c174728b4e41f930d347d37906eaced636c728b03c1f3d8b938926ed16` | `c68a8ff01452c1c97e63102597ff9a743a18284fcb16169907bd71c3d370dcd6` |

Dados de cada objeto (tamanhos, offsets, janelas e streams):

- [MEDICAO_ORIGINAIS.json](<C:\IALD\Central de Patentes\Chatgpt\SANEAMENTO_ADENDO_001_012\binary\MEDICAO_ORIGINAIS.json>) — SHA256 `8bf3eb8084c1587f36288f59adeb7256cb5fc1dd9e0eae7f77ab358f02467347`.

- [CAMINHOS_EMBUTIDOS.json](<C:\IALD\Central de Patentes\Chatgpt\SANEAMENTO_ADENDO_001_012\binary\CAMINHOS_EMBUTIDOS.json>) — SHA256 `59ce7308549b8796b594e0a40226e1f67a539526b9d8624b4aba96844223638c`.

- [IMPORT_ARTIFACTS_LIDOS.json](<C:\IALD\Central de Patentes\Chatgpt\SANEAMENTO_ADENDO_001_012\binary\IMPORT_ARTIFACTS_LIDOS.json>) — SHA256 `aef6c18d2555421478ecba6284660048667855c0bc3e7bb9338172099ed332eb`.

- [REBUILD_ATUAL.json](<C:\IALD\Central de Patentes\Chatgpt\SANEAMENTO_ADENDO_001_012\binary\REBUILD_ATUAL.json>) — SHA256 `a1c1a089c30fa3e3db6508f05df26e21b53e7f00f89c6182b677d893b9ddd416`.

- [RESULTADO.json](<C:\IALD\Central de Patentes\Chatgpt\SANEAMENTO_ADENDO_001_012\binary\path_experiment\20260915_161043_821020\RESULTADO.json>) — SHA256 `5a82079d778b592e8f858be83bf12f5f817d6a29fe48644f7220bea88f2a26dd`.

- [RESULTADO.json](<C:\IALD\Central de Patentes\Chatgpt\SANEAMENTO_ADENDO_001_012\binary\axioms\20260915_161448_553658\RESULTADO.json>) — SHA256 `026d58ddaea7078eabce38a3db39b4daf889bb1a4336e49761bd98e47ac58e31`.

Limites: não se afirma diferença matemática a partir de hashes; não foi feita análise completa do formato de serialização histórico de AreaScale; o cache Mathlib e demais pacotes foi copiado, não reconstruído integralmente. A reconstrução da gerência permanece o árbitro da incorporação.
