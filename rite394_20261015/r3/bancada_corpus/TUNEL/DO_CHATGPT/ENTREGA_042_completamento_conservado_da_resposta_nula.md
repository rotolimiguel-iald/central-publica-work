# Entrega 042 — completamento conservado da resposta nula

06/09/2026. Resposta complementar à ORDEM009. [REAL / DERIVED / INPUT / OPEN].

O avanço é um critério completo, na família e no fundo plano fixados, para decidir se a resposta nula admite uma fonte conservada. A liberdade de traço variável foi incluída: não se escolhe um representante e se toma sua falha por falha de todos.

Para w suave e fechado e c constante, toda fonte suave simétrica com T(d,d)=c[w(d)]² em todos os nulos é S+fg, onde S=c(w⊗w−g⁻¹(w,w)g/2). A conservação equivale a df=−c(div w)w. O critério é existência de potencial suave; fechamento sozinho não foi promovido a exatidão global.

O controle φ=t²/2, w=t dt admite f=−ct²/2. O contraexemplo φ=t²x tem força J=(4ctx²,2ct²x,0,0), com ∂1J0−∂0J1=4ctx. Para c≠0, no ponto (1,1,0,0), isso exclui toda fonte conservada com as mesmas leituras num aberto contendo o ponto, inclusive todo traço variável.

A ligação028→042 usa c_b=log(2)B/π e a resposta somável já certificada. B>0 dá c_b>0. Há também a formulação do negativo diretamente em termos do limite do incremento entrópico relativo dividido por t², por unicidade do limite028. Controles: amplitude geométrica de massa1/12, campo crescente reparável e amplitude zero com tensor zero. A escolha do campo direcional e do fundo permanece INPUT; os estados não são refutados.

A precisão angular do operador foi preservada no parecer: L é distinguido da forma quadrática extraída de sua variação de fase. A área geral de duas direções horizontais é sqrt(det G), G_ab=Re〈D_aξ,D_bξ〉. O módulo da fase isolada é unitário. O significado de L como cauda/poço, a área física e o retorno estabilizador continuam ONTO/OPEN; a área dos raios GNS não é automaticamente área dos estados restritos nem do espaço-tempo.

## Verificação

[REAL — compilação final e auditoria independente] Em CONTINUACAO042_CLEAN_20260906_211041_859289, os quatro módulos e Imports042All passaram: 52 teoremas, 12 definições, 64 impressões de axiomas e zero instâncias. Os cinco passos retornaram exit0/PASS, sem erros ou advertências, com cobertura exata e apenas propext, Classical.choice e Quot.sound. As fontes de trabalho e as cópias compiladas são idênticas; os snapshots de entrada permaneceram estáveis. O auditor independente --build-only retornou BUILD_PASS/exit0, conferindo 1.987 arquivos do build e 163 registros históricos. O revisor também conferiu separadamente os logs, metadados, snapshots, importador e adaptação integral do auditor041. As tentativas anteriores e backups foram preservados. O manifesto final é produzido depois do parecer e da entrega, e sua auditoria somente leitura confere a custódia completa.

| Artefato | Bytes | SHA256 lido dos bytes |
|---|---:|---|
| [CONTINUACAO042_PARECER.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO042_PARECER.md>) | 9271 | a6f55106ccea3854c2da9858224488a12d9586e2a4be06afb2a7bcf72dad7ac9 |
| [CONTINUACAO042_DERIVACAO_PREVIA.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO042_DERIVACAO_PREVIA.md>) | 5101 | eaf19dd48f7fc77b056ca0b8742a5dad2e30c688970dba97041ceaa7b9b80f3b |
| [NullStressCompletion.lean](<C:/IALD/Central de Patentes/Chatgpt/NullStressCompletion.lean>) | 9348 | 10b57a6fc2e3a14d53af8965dd4948d6be79597d0744b5d0fd8e49c14f2ad11d |
| [ConservativeNullResponse.lean](<C:/IALD/Central de Patentes/Chatgpt/ConservativeNullResponse.lean>) | 7229 | a9610ae006f82769639041cb9fd56c7df7d97aea435d17ecb4dcc01860ac164a |
| [NonintegrablePotential.lean](<C:/IALD/Central de Patentes/Chatgpt/NonintegrablePotential.lean>) | 10502 | 9d0abe81d064ee6767f0176a63466ad848735c2aa595e1a40626931a712485b9 |
| [SummableNullIntegrability.lean](<C:/IALD/Central de Patentes/Chatgpt/SummableNullIntegrability.lean>) | 8003 | 0e8cd1c542a4f366272229813bedd43412dbec28c206ae2d0517817c1ad743b3 |
| [clean_continuation042.py](<C:/IALD/Central de Patentes/Chatgpt/clean_continuation042.py>) | 32312 | a93116b659976d8371f6a57ccc0f339396b24f35de7501d74717e541a159dad5 |
| [audit_continuation042.py](<C:/IALD/Central de Patentes/Chatgpt/audit_continuation042.py>) | 39894 | 3c2d0649dfbc75eb08f725b97d0ea0b4029982ad36bf5ac5cfd16aceda4f636b |
| [revise_continuation042.py](<C:/IALD/Central de Patentes/Chatgpt/revise_continuation042.py>) | 2116 | 76358a729aff5ba1eadb407e5075d24f32ba19bcceb77ff6baa1a63b6abec792 |
| [CONTINUACAO042_CLEAN_BUILD.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO042_CLEAN_BUILD.json>) | 1305984 | 17350158a550efccd70a5feb899e193e9e16112cc93d6be2929b9332de78fa65 |

O manifesto é CONTINUACAO042_MANIFESTO.json, produzido pelo auditor depois desta entrega, para evitar dependência circular entre os hashes. Reproduzir a auditoria selada, somente leitura:
`C:\Python314\python.exe -B "C:\IALD\Central de Patentes\Chatgpt\audit_continuation042.py"`.

## Critérios da ordem e limites

- A — relógio relativo: esta entrega não produz um relógio canônico novo; os resultados040/041 permanecem os antecedentes. Não escolhemos parâmetro para acertar a área.
- B — H3: ainda OPEN. A042 delimita a conservação necessária à reconstrução geral da resposta; não produz HorizonEquilibriumData nem identifica o calor com a dinâmica modular.
- C — região–álgebra: nenhuma ponte nova é reivindicada nesta entrega.
- Guardas: somente novos artefatos/cópias/backup em Chatgpt; originais, um.py, kernel, Atlas, memórias e selos anteriores somente leitura; nenhum dado observacional, nenhuma alteração de gate.
- Escopo: assinatura+---, fundo plano, acoplamento constante, campos/tensores suaves, T simétrico e resposta para todos os nulos no mesmo aberto. Não é impossibilidade de reconstruções em outros fundos, de campos diferentes ou de uma teoria geral.
- Custódia: fronteira histórica conferida por hash, sem recompilação histórica; fontes canônicos sem pin de fonte servem só à descoberta de imports. Dependências externas diretas conferidas, sem hash de todo fechamento transitivo de Mathlib/toolchain.

O parecer separa o cálculo angular analítico dos teoremas042 formalizados. Os resultados de integrabilidade não demonstram estabilidade, condições de energia, seleção da área ou gravidade quântica.

H3: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado.

Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.
