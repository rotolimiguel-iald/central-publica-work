# Pedido preparado para o orquestrador IALD (enviar depois de reabrir a sessão)

**Por quê preparado e não enviado:** o operador autorizou em 28/09/2026 o uso das outras IAs («autorizo vc a usar as outras IA's para fazer
uma busca profunda no sistema, pode gerenciar essa busca»). O MCP `iald-orchestrator` está registrado e conectado no escopo do usuário
(`claude mcp get iald-orchestrator` = conectado), mas as ferramentas dele não carregaram nesta sessão do VS Code. A skill `iald-orquestrar`
manda reabrir a sessão e não recriar o servidor. Nada foi registrado em `state\session_requests\` (o registro vem imediatamente antes do envio).

**Como enviar (skill `iald-orquestrar`):** `iald_orchestration_status` e `iald_selection_preview` → gerar um UUID `request_id` → gravar
`BASE\state\session_requests\<request_id>.json` (temporário → conferir → substituir) → `iald_coordination_submit(prompt, request_id)` →
acompanhar com `iald_coordination_get(job_id)` → relatar só no estado terminal, com a resposta dos provedores marcada `[DECLARADO]`.

**Material que sai:** só o texto abaixo (resultados e perguntas de método). Nenhum arquivo confidencial, credencial ou corpo jurídico.

---

## Texto do pedido (para os provedores)

Você é um revisor independente de método científico. A gerência de um programa de pesquisa em cosmologia e gravitação (a TGL) auditou os
seus próprios testes com dados e quer uma segunda leitura, com literatura citada. Responda cada item com (a) o que a literatura diz, com
referência precisa (autor, ano, arXiv); (b) o número, quando houver; (c) o seu grau de confiança. Não é pedido que você concorde: é pedido
que você tente derrubar a leitura da gerência onde ela estiver errada.

1. **Prioris de distância do CMB em fundo modificado.** O modelo multiplica a expansão por Φ = 1 + β|1 + w_eff| em TODAS as épocas (na era da
   radiação |1 + w| = 4/3, logo H² cresce ~4β/3 ≈ 1,6% para β = 0,012; o efeito equivale a ΔN_eff ≈ ±0,12). A análise usou a verossimilhança
   comprimida do Planck 2018 (R, l_A, ω_b; Zhai et al.), com z* e z_drag de ΛCDM e o horizonte sonoro reescalado pela razão das integrais.
   Para esse tipo de modificação precoce, as prioris de distância são confiáveis? Qual o viés esperado em β? O que a literatura recomenda
   (verossimilhança completa, prioris estendidas com N_eff, outro caminho)?
2. **Resultado com o DESI DR2 (Planck comprimido + DESI DR2 BAO com covariância completa):** β = −0,0135 ± 0,0063, enquanto a previsão
   pré-registrada é β = +0,01203 (4,0σ de tensão). A previsão com o sinal oposto ficaria a 0,23σ, mas o sinal foi nomeado depois de ver o dado.
   Qual é o procedimento estatístico correto para tratar uma hipótese de sinal escolhida depois do dado? Que dado ainda não olhado serviria de
   teste confirmatório (DESI DR3? prioris de distância de ACT DR6/SPT-3G? verossimilhança completa)? Qual poder cada um teria?
3. **Testes de recuperação da relatividade geral por citação.** Liste as restrições públicas canônicas, com números e referências: velocidade das
   ondas gravitacionais (GW170817 + GRB 170817A), massa do gráviton (GWTC-3), testes de polarização, consistência do ringdown e teorema da área
   (GW250114). O objetivo é registrar a correspondência com a RG como limite clássico, não como rival.
4. **Ecos pós-fusão:** um molde de eco com amplitude √β ≈ 0,11 vezes o primário e atraso dado por 2π/κ (κ = gravidade de superfície de Kerr).
   É correto usar o período 2π/κ, que é a periodicidade em tempo IMAGINÁRIO (KMS/Euclidiano), como atraso em tempo real? Há literatura sobre
   ecos com esse atraso?
5. **Estatística conjunta:** vários canais independentes, cada um com seu p-valor; a regra de consistência usada foi max|z| < 3 sem correção de
   multiplicidade. Qual é a combinação correta (Fisher, Stouffer, χ² conjunto) e como tratar canais que compartilham o mesmo dado (Planck)?

Marque tudo o que você afirmar sem conferir numa fonte como [NÃO CONFERIDO].
