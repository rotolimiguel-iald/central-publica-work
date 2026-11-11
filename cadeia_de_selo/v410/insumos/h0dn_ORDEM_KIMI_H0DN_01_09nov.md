# ORDEM KIMI H0DN-01 (09/11/2026) — Montar o vetor observado do H0DN e fechar a covariância física, para a abertura pré-registrada do teste H0DN × BG1

**De:** gerência c1 da Central (Claude Code), por ordem do operador Luiz Antonio Rotoli Miguel (IALD/TGL), verbatim sha256 `1b4010ff8f82f2ffccd214d591d0e7e872b8757d90c41dfcc37ef4040fd0f227` («quanto ao teste da v410 concordo com tudo que vc falou, pode dar a ordem ao kimi k3pro»).
**Para:** Kimi K3 Pro. **Tipo:** CONSTRUÇÃO DE INSUMO + FECHO DE COVARIÂNCIA. Sem abrir o resultado, sem semente nova da R2, sem ajuste de parâmetro, sem publicação.
**Estatuto de tudo que você devolver:** `[DECLARADO pelo Kimi]` até a gerência conferir na fonte e por código próprio. Nada aqui autoriza execução do teste, gate ou publicação.

## §0 O que está decidido (para você não refazer)

1. O teste é o **H0DN × BG1** (razão H_local/H_fundo), desenhado pelo Codex astra-bell em 06/11 e **congelado** em `FREEZE_R2.json` (9 pinos abaixo). Nulo: razão = 1. Alternativa TGL: K = E(z*)^(2β/3) = 1,0838071748529643, β = α√e, zero parâmetro livre. Estatística Z unilateral, limiar 5σ, dois modelos (publicado; viés diferencial Cefeida livre), nenhum selecionado.
2. A v410 do `um.py` **pré-registra** esse teste (insumos embutidos por sha256, função de veredito congelada, nenhum vetor observado lido). **A abertura com dado real é de versão futura** e só pode devolver veredito que não seja `INCONCLUSIVE_SYSTEMATICS` se a covariância física estiver fechada.
3. Seu trabalho de 06/11 (`kimi_h0dn_discriminante_06nov`) foi lido e vale: a regra conjunta (z_nulo ≥ 5 ∧ |z_TGL| ≤ 1,96) está agora CONGELADA na função de veredito da v410; as margens, a decomposição pública das covariâncias e o G1/G2 são o ponto de partida desta ordem. **Não repita.**
4. A rota «coerência espectro × fotometria» segue NOT_TESTABLE (η = 1; Mapa seq 1635). Não é objeto desta ordem.
5. A aritmética com o agregado público do H0DN (73,50 ± 0,81) **não é resultado** e não deve aparecer em nenhum texto seu como «5σ». O agregado é público desde out/2025: a abertura futura é retrodição sem ajuste (lei da prova de 05/10), e por isso o que vale é o pré-registro — não toque nele.

## §1 Os pinos congelados (FREEZE_R2; nada disto pode mudar)

| arquivo (em `work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\`) | sha256 | bytes |
|---|---|---|
| `analysis_plan.json` | `00fcc2a7360915330ecf18393a619dc7dcd5318ad0998b77909e420ba229d74d` | 2997 |
| `estimator.py` | `9b06640d524899ece95bd5879e2cb5ad8c93cb2576ddb27e857d90142cbd5049` | 5191 |
| `prepare_estimator.py` | `5a28153f9a3b6d8951feb090bee941f32ffa28bce7daa490deee83909dd47e52` | 4080 |
| `network/network.npz` | `3dd073c3a74abf34ef3d80368456a2698e8405a52417057149a35a8a5a5a6832` | 242793 |
| `network/MANIFEST.json` | `ab08cb24573ba9d6433d52b7165ac7d51afd312ab6975c096f19b64a366d83d5` | 16971 |
| `background/BG1.json` | `87b475a05700ddc2074217761502e239d6f33b1ad74ff5a763e1b577b724f6ca` | 13463 |
| `background/build_bg1.py` | `c8b941f0b685d2d642c8e440fdac33fa883ef6d8cd08a04d13ba32cc98d4975b` | 12051 |
| `estimator_frozen.npz` | `059ef7b6f2c671406058fdb6e647c011851e5761da91784b4ce213e9abbe07b8` | 84677 |
| `PROSPECTIVE_GEOMETRY.json` | `798fb5ab9e6b3115bfacfbfcf2f9d55f56acb2337042737730e8632b5682d708` | 4717 |

Convenção do estimador (`estimator.py`, `evaluate`): `local` = vetor CENTRADO de 255 linhas na ordem de `network.npz:row_names` (o parâmetro publicado é transladado a zero; `signal_local` é a direção do sinal; `h_index` = 63 = h = log10 H); `background` = parâmetros do BG1 centrados (o BG1 observado tem centro zero e sua incerteza já está em `sd_null`); `null_basis` (255×72): o vetor tem de estar no suporte de C (erro ≤ 1e−8).

## §2 O que você entrega (G1–G4 e o vetor), em `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\`

1. **`y_obs.npz`** — o vetor observado do H0DN, 255 linhas, na ordem de `row_names`, centrado na convenção do estimador, construído pelo código upstream (`h0dn_bg1_06nov\network\upstream\h0_constrainer\`) sobre os dados brutos (`network\upstream\data\*.dat`): hospedeiras (μ_host), calibradores SN Ia (m0_Bi), fluxo de Hubble (m_b, zhel, zcmb, vp), SBF, masers, âncoras, grupos. Com `CONSTRUCAO_Y_OBS.json`: cada linha ↔ dado de origem ↔ equação da rede, o que foi agregado e como (o operador de agregação das curvas que você descobriu no G1), e `y_obs` também NÃO centrado, para conferência. Se alguma linha não puder ser reconstruída da fonte, deixe-a marcada e NÃO a preencha.
2. **G1/G2 fechados na fonte:** o operador de agregação das curvas de luz (os 47 IDs com múltiplas curvas), os 8 IDs sem correspondência exata e os 2 aliases candidatos — resolvidos por procedência (SH0ES R22, Pantheon+ release), ou declarados irresolúveis.
3. **G3/G4 — a covariância física conjunta** `C_fisica_258x258.npz`: SN-only / hospedeira-Cefeida / velocidade peculiar, SEM duplicar a informação Cefeida que já está na rede; cada bloco com a fonte e o método (`DECOMPOSICAO_COVARIANCIA.json`); o bloco cruzado H0DN–BG1 fica ZERO só se você demonstrar a independência condicional (senão, cenários). A matriz tem de ser simétrica, PSD no suporte, e o `evaluate` tem de aceitar o vetor (suporte).
4. **O que você NÃO faz:** não calcula Z, t, ĥ nem qualquer razão; não roda `estimator.evaluate` no vetor observado; não gera semente nova da R2; não altera arquivo do FREEZE_R2; não compara `y_obs` com `signal_local`. A abertura é do `um.py`, numa versão selada, com a função de veredito já congelada. Se precisar validar o pipeline, use SÓ os vetores sintéticos já existentes.
5. **`ENTREGA_H0DN_Y_OBS.json`** com sha256 de tudo, estatutos, o que ficou aberto; depósito em `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\kimi\` (formato de `memory\fila\README.md`); rota no Mapa (`rotas.py registrar … --quem kimi-k3pro`), consultando antes `rotas.py consultar "H0DN"`.

## §3 O que você já fez e onde está (para citar, não refazer)

| arquivo (em `work\kimi_h0dn_discriminante_06nov\`) | sha256 |
|---|---|
| `COVARIANCA_COMPONENTES.json` | `e27b70c0b15d2fcbbb67314a00662404f968395b913543b633ba43fd8ae60451` |
| `DISCRIMINANTE_CONJUNTO.json` | `8fc58091bc14ee8e80777b0a16d4be226d5f7217838999d4d1c8f8d02e9e1f16` |
| `MARGENS_DISCRIMINANTE_CONJUNTA.json` | `1fc591302ae4a4c5eadad2a98c8625a55b5aed545508c90cab6ce1e68d3fa52a` |
| `ADENDO_ASTRA_DISCRIMINANTE_E_AFIXACAO_06nov.md` | `6faf45d79dfe48e3538695e42db6a0c9a8750c3b1be40e9881e8568af1205007` |
| `H0DN_METODOS_AGREGACAO.md` | `517d055cbae834b25b8420bda832c0f3841d321ebdf3b113b7f41e209983225f` |
| `g1g2\G1_ARITHMETIC_CANDIDATE.json` | `1f5f0b5da10533a73823ba8af862049b020397f81c59001018564731734ef40e` |
| `g1g2\G1_CANDIDATE_AGGREGATION.json` | `240ba17cfc8463ae6653b1da108232e34913b4b2e02e92273eab4fb026e11d80` |
| `g1g2\G1_G42_COVARIANCE_SCENARIOS.json` | `2a70a91fce557ba2eccc2f3c87de4ff55d3203cc961604be32cdbc5f1e2916fd` |
| `g1g2\G2_ID_METADATA.json` | `f3bbcc50f0e267dfc3e665b9f723518588d772f1a0a7bed0754a92febb0f2771` |
| `g1g2\G2_IDS_PROVENIENCIA_RESOLVIDA.json` | `725a6f53ebc9754f2347d0a6f486e9c4523bb046d6d49d0c3f970cb56a4fe873` |
| `r3_conjunta\analysis_plan_r3.json` | `0733a14a0e000e5fb32dfb2500e0c43693161a2cedd1f099dc8bcfcf4f03bde9` |
| `r3_conjunta\FREEZE_R3_PENDING.json` | `4cef6effdfef418ca43385b6c7eda809408d32d426d0204e2432cd6970c52acc` |
| `r3_conjunta\PREFLIGHT_R3.json` | `ab0b8b8d30621c97d7deb6b98dd1d50a8192cd01d42a2d945592b8ce3627c550` |
| `r3_conjunta\PREFLIGHT_R3_EVIDENCE_UPDATE.json` | `109558b0225cbc1908767734995b3625b1cb3aaf4f7f2a1e02cad3f7b82357b3` |
| `r3_conjunta\R3_DIAGNOSTICO_ESCORES_R2.json` | `bd6818dbfe5ae0947fff2478f38f8b8a7e6bff29a4dc3cb8f55e550f2c789a11` |

## §4 Retorno

Até 15 linhas: o que fechou (G1–G4), o que não fechou e por quê, os sha256 dos entregáveis, e as perguntas que exigem decisão do operador — nas quatro línguas dele (TGL, teológica, linguística, jurídica), como de costume. Uma obstrução demonstrada também é resultado.

— gerência c1, 09/11/2026. Correções AO LADO, nunca por cima.
