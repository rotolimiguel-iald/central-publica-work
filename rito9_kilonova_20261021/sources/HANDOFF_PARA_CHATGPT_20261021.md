# HANDOFF PARA O CHATGPT (codex-app) — executar tudo que resta

**De:** membro Kimi (Kimi Work) · **Para:** ChatGPT/Codex-app · **Via:** operador (21/10/2026)
**Contexto em uma linha:** a fila do Claude precisa de cirurgia de coordenação, e o rito 9 (kilonova) está pronto para governança de fechamento — a álgebra acabou, o que resta é decisão e revisão.

Tudo que é meu está no caderno `C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg` e na espinha `C:\IALD\MAPA_DE_ROTAS\rotas.jsonl` (consulta canônica: `rotas.py`). Seqs-chave do dia: **1301** (hipótese do operador), **1303–1304** (vigília e medição da fila), **1305** (desenho do rito 9), **1307** (Elo 1 + errata da visada), **1309** (pedra Lean limpa + H-KN), **1311** (M1 derivado + H-SEQ).

---

## PARTE 1 — INFRA: destravar a fila do Claude (prioridade operacional)

**Estado medido hoje (seq 1304):** fila cheia (5/5); o teto do provedor claude é 20.000 chars; jobs vinculados à F9.9 carregam a projeção da missão (15.852 chars) + pacote do grafo (5.000) — estouram o teto antes de qualquer briefing. O título da unidade F9.9 já foi limpo («grep-c3»; backup `PROGRAMA.json.bak_20261021_kimi_titulo_f99`) e o grafo já foi reindexado hoje.

**Executar, nesta ordem:**

1. **Retirar dois jobs estacionados** pelo caminho interno da coordenadora (a fachada não cancela job cujo pacote não monta — `act cancel` sofre rollback transacional; defeito de projeto registrado na seq 1304):
   - `e1ce17ac-cf3a-4ff8-b618-c73d85c623cb` (briefing v1, 5.127 chars — estruturalmente acima do teto)
   - `90528e45-…` (meu briefing v2 enxuto, 3.377 chars — mesmo bloqueio estrutural da F9.9)
   Sugestão de nota de retirada: «Retirado sem envio: teto estrutural do provedor; conteúdo ressubmetido sem vínculo de branch.»
2. **Despachar a ordem de implantação** — job `9dd45d6a-0afb-49cd-912d-53b97c63f07e` (2.457 chars, monta pacote e passa no teto; verificado hoje via `bridge.py get`). É a ordem direta do operador ao Claude (5 itens: cap/ranking do Nós Vivo, cabeçalho de confiança v2, assinatura do pré-registro do benchmark, revisão do prompt-sistema, + item 0 já implantado por mim = dobra do envelope).
3. **(Opcional, recomendado) Corrigir o defeito de projeto:** o cancelamento não deveria montar o pacote — `activity.cancel` + `_act` dividem a mesma transação do `get`; separar para que cancelar não exija pacote montável. Testar com a suíte da casa.
4. **(Rotina) Reindexar o grafo** sempre que unidades novas forem criadas: `python C:\IALD\NOS_VIVO\construir.py` (~10–20 s, backup de bytes automático — é o remédio prescrito pela própria ferramenta).

**Depois do passo 1+2:** me avisem pela espinha (ANOTACAO «PARA KIMI») que eu ressubmeto o briefing **sem vínculo de branch de quadro** — aí cabe folgado sob o teto.

## PARTE 2 — CIÊNCIA: governança de fechamento do rito 9 (kilonova)

O rascunho completo está em três documentos do caderno (ler nesta ordem):
- `PRE_REGISTRO_RITO9_KILONOVA.md` (desenho + kill-rules + errata datada da visada)
- `DERIVACAO_ELO1_RITO9.md` (seletor generalizado; resposta construtiva ao Evento 2)
- `FECHO_ELO1_E_ARVORE_ELO3.md` + `DERIVACAO_POTENCIA_DT_NU.md` + `DERIVACAO_M1_PRIMEIRA_LEI.md` (cadeia completa)

**Resultados a revisar:**

| Item | O que é | Estatuto |
|---|---|---|
| Pedra candidata | `pedras_candidatas/SeletorGeneralizado.lean` — `[A, α_θ(Z)]=0 ⟺ 2b(cos²−sin²)=(c−a)·2sen·cos` | **Compilou limpa** no toolchain da casa (v4.31.0), axiomas auditados: só os 3 padrão mathlib. **A casa decide se entra no kernel** (está no caderno, não no kernel) |
| Elo 1 | θ_KN = θ_M ≈ 6,2973° via seletor + cruzamento universal (S-d) | fechado **módulo H-KN** |
| **H-KN** | «a fronteira em fuga realiza o cruzamento mínimo de preservação de identidade (bulk aberto)» | CONJECTURE — **o Claude aferidor deve atacar esta** |
| **H-SEQ** | «a camada de fronteira é sequência de células causais τ₀=ℓ/c, fração β por tentativa» (ansatz cinético padrão) | CONJECTURE — **segunda alvo do ceticismo** |
| Elo 3i | abertura do canal/jato ≈ θ_M | predição afiada, pronta para pré-registro |
| Elo 3ii | Δt_ν = ℓ(Θ_GW)/(c·β); rota Wigner morta (τ_W=0); escala exploratória ~3–8 ms | derivado módulo H-KN+H-SEQ |
| Elo 2 | luminídio | OPEN/DATA — proibido como testemunha (circularidade) |

**Decisões que são da casa (não minhas):**

5. **Tipar o canal GW:** o graviton paga a mesma admissão ℓ/(cβ) ou é o anúncio da fronteira (isento)? Se paga, o observável vira a **diferença** ν−GW; se isento, vale a fórmula absoluta. Muda o pré-registro — decidir antes de congelar.
6. **Escolher o modelo BNS padrão** para ℓ(Θ_GW) (neutrinosfera efetiva do remanescente em função das massas da GW). Sem isso não há intervalo numérico honesto.
7. **Ceticismo do Claude** sobre H-KN, H-SEQ, a pedra e as duas erratas registradas (visada vs abertura; sinal da potência β⁻¹).
8. **Decisão sobre o kernel:** acolher ou não `SeletorGeneralizado.lean`.

## PARTE 3 — O QUE VOLTA PARA MIM depois da governança

9. Com modelo BNS escolhido e canal GW tipado: **eu** calculo os intervalos com β runtime na Bancada Um (contrato B4: β nunca literal; pin v394 — se o um.py mudou de versão, a bancada recusa até a cadeia B(n) refazer o selo; nesse caso, refazer a cadeia primeiro).
10. **Pré-registro selado na espinha ANTES de olhar qualquer dado de BNS futuro.** Depois disso, só a natureza fala.

## Réguas invioláveis (valem para todos)

Escrita na casa só via `rotas.py registrar`; correção ao lado, datada; releases seladas/Nós Vivo/Atlas intocáveis (o `construir.py` é exceção prescrita — reindexação); NOT_FALSIFIED ≠ CONFIRMED; PROVADA ≠ CONFIRMADA; β nunca literal; não somar testemunhas; pré-registro antes do dado; cético aferidor; sinal consultivo — nunca gate; jurídico/credenciais nunca na fila; nunca ajustar forma ou número a GW170817 (calibração, não confirmação); o luminídio não testemunha a favor do ângulo (circularidade).

*Haja luz.*
