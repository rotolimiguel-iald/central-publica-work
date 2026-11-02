# HANDOFF v405 — ADENDO 6 (01/11/2026): OS NOMES DO OPERADOR e a ordem «tudo derivado» — as hipóteses nomeadas descarregadas

**De:** gerência c1, em nome próprio. **Verbatim do operador** (sha256 `1f16a74c05d9d4cb43937fc4e490fb95e8e1e36c0bc411fea936757aee9b9043`): «segue a nomeação, mas eu não gostaria que ainda restasse hipóteses nomeadas, é preciso que esteja tudo derivado» e os sete nomes. **Build:** `lake build` dos seis módulos no sandbox k404c, BUILD_RC=0, 9402 jobs, 0 sorry, todos os teoremas no trio (saída sha256 `ea796b61bdd32ba3b1b3c3dd003dc600a2b936645f033a5966c58bf11a48c692`; recibo `RECIBO_NOMEACAO_E_DERIVACAO_01nov.json`, sha256 `8881ea618bd897f43471dad1ee3fb0bb5e017d2aa0cff571b36519b349070f0d`).

## As sete pedras, com os nomes dele

| módulo | nome do operador | antes | teoremas | sha16 |
|---|---|---|---|---|
| `TGLExt.PonteDaMassa` | Ponte da Massa | PonteDaMassaTransversal | 21 | 4eb0ac9da9b8df07 |
| `TGLExt.MassaTensaoPura` | Massa = tensão pura | EmprestimoDaMassa | 15 | c2e7f793d2668087 |
| `TGLExt.ObservadorTerminal` | Observador = terminal | ObservadorTerminal (nome confirmado pelo operador; arquivo r2 intocado) | 26 | 959aaf88ea811e4d |
| `TGLExt.TonicaDoHamiltoniano` | Tônica do Hamiltoniano | E0LiberdadeDeEscala | 13 | 989fc3c38ae6a49a |
| `TGLExt.LeiDoDiminuto` | Lei do diminuto | LeiDoMeioTom | 19 | 832362b70cfb0256 |
| `TGLExt.DiscoDeEuler` | Disco de Euler | DiscoDeEuler (r2) | 12 | 00868b3de68c5663 |
| `TGLExt.PontoZeroDoPsion` | Ponto Zero do Psion | PontoZeroDoPsion (r3) | 6 | f45e0e6a804339a0 |

## O que era hipótese nomeada e o que virou
- **autoconjugação** (pontes e lei) → teorema do kernel `absolute_faces_half` (no estado absoluto, Gibbs do Hamiltoniano nulo, cada face de paridade pesa ½) + `forty_five_unique` (θ = π/4); `transicaoDerivada` e `leiDerivada` habitam as estruturas por construção; `nenhuma_hipotese_resta` exibe a transição com E₀ = 1, θ = π/4, m = β·√2/2 para todo acoplamento.
- **período fiel** (segunda ponte) → `emprestimoDerivado` com P = 2π/κ e `one_turn_gives_faithful_period`.
- **a tônica** (lei) → `tonica c u := (β/α)·u = √e·u`, lida do acoplamento; `leiDerivada_E0`: o diminuto pousa em E₀ = u; `the_tonic_fixes_what_the_form_leaves_free` (Tônica do Hamiltoniano).
- **β como campo do disco** → `Disco.doAcoplamento`. **Positividades** → do kernel ou do 1 posto.
- **«Massa = tensão pura»** ganhou teorema (`massa_e_tensao_pura`): o principal é a energia RETIDA, β·u, projetada no transversal — leitura da gerência do nome dele [ONTO].

## O que resta e NÃO é hipótese (pela régua do próprio operador)
O Um POSTO (u = 1, o `echo 1`; 05/10); α medido por dentro (13/10), dentro de β = α√e; os dados do sistema que lê (g, κ; no disco K, τ, E₀); a dispersão do psíon como definição [KNOWN, Tratado].

## O que entra na v405
- Os sete módulos com os nomes acima (`TGLExt/<Modulo>.lean`), na ordem: PonteDaMassa → MassaTensaoPura → Identidade (por escrever) → ObservadorTerminal → TonicaDoHamiltoniano ← LeiDoDiminuto → DiscoDeEuler → PontoZeroDoPsion (TonicaDoHamiltoniano importa LeiDoDiminuto; MassaTensaoPura, LeiDoDiminuto e TonicaDoHamiltoniano importam PonteDaMassa).
- Registros com os nomes dele; os adendos 1–5 citam os nomes provisórios: errata AO LADO, nunca por cima.
- Avisos de linter (ramos `first` nunca executados) são só avisos; não há erro.

## O que NÃO entra
- Nenhum número novo; o veredito do rito não se move; nada instalado antes do treino e da revisão independente.
