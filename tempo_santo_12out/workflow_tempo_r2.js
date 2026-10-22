export const meta = {
  name: 'tempo-r2',
  description: 'F1.TEMPO R2: ADENDO uniforme congelado, pedra corrigida (E5), reensaio ótico sob o adendo, duas auditorias, relatório R2 pronto para a v392',
  phases: [
    { title: 'Adendo', detail: 'E3 e o adendo uniforme das tolerâncias, congelados por hash' },
    { title: 'Correção', detail: 'a pedra corrigida em sandbox' },
    { title: 'Reensaio', detail: 'O-f e T9.o(c) sob o adendo; tentativas preservadas' },
    { title: 'Auditoria', detail: 'reprodução e estatuto' },
    { title: 'Relatório R2', detail: 'o que entra na v392 e o resíduo' },
  ],
}

const W = String.raw`C:\IALD\Central de Patentes\work\tempo_santo_12out`
const R2 = W + String.raw`\5_R2`
const NOS = String.raw`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`
const REL = W + String.raw`\4_RELATORIO\RELATORIO_FINAL.md`

function regras(dir) {
  return String.raw`
REGRAS (sem exceção):
- Escreva SÓ dentro de ${dir} (crie). NÃO toque ${W}\0_LEVANTAMENTO, 1_PREREGISTRO, 2_OPTICO, 3_KERNEL nem 4_RELATORIO (são o registro congelado da R1). Nada no quadro, no mapa, na memória, no túnel, no Nós, no kernel do Nós, na Bancada, no site ou no git.
- NÃO rode um.py nem scripts de selo. Ler o um.py (${NOS}\um.py) só por busca com número de linha. Nenhum dado observado; nenhum provedor remoto; nenhuma chamada paga.
- Lean só em sandbox dentro de ${dir}, LEAN_PATH só-leitura ao .lake de ${NOS}\tgl_kernel (toolchain v4.31.0 copiado do elan para o sandbox; a R1 fez assim em ${W}\3_KERNEL); impressão digital do tgl_kernel antes e depois igual; apagar toolchain/.lake/caches ao final.
- β NUNCA literal: ALPHA_FINE_CODATA_2018 lido dos bytes do um.py (a atribuição de topo é a l.95; a l.5557 é embutida), vezes √e, em runtime; estatuto [DERIVED: lido e calculado], nunca «medido».
- Hashes por script. Estatuto em cada afirmação. Verbatins do operador só byte a byte; paráfrase da gerência nunca leva aspas de citação do operador. Nunca atribuir ao operador frase que ele não escreveu.
- Nunca escreva como veredito a palavra proibida da régua (a «confirmação» em inglês maiúsculo). Um PASSA é validade na face testada, não creditação. Nada move o gate.
- Confidenciais nunca; acervo do Escritório nunca.
`
}

const CONTEXTO = String.raw`A R1 da F1.TEMPO está relatada em ${REL} (leia-o INTEIRO antes de agir): tabela por afirmação (T1, T3–T8, T10, T11 PASSA; T2 CITADA; T9 FALHA só pelo critério numérico T9.o(c), com os subitens de kernel PASSA), os 20 achados M1–M20, as erratas E1–E5 e o resíduo do operador (§8). A DECISÃO DA GERÊNCIA (quadro, evento 705) para M1: a FALHA de T9 fica REGISTRADA como resultado pela regra congelada, com o diagnóstico ao lado; e congela-se um ADENDO UNIFORME (O-f e T9.o(c) juntos: aritmética exata em decimal de alta precisão e, no float, tolerância proporcional a k·eps com constante justificada), pré-registrado por hash ANTES de reensaiar, com todas as tentativas preservadas; nunca reensaiar só a T9 numa representação que passe. A ordem do operador de 12/10: a pedra do tempo ENTRA na v392 — por isso ela tem de sair corrigida (E5) e reauditada. Nome provisório neutro sugerido pelo relatório: TheTimeIsNotAPost (o operador dá o nome final; por POSTO = RANK, «TheTimeHasNoRank» contradiz flow_full_rank).`

phase('Adendo')
const ad = await agent(String.raw`Você é o PRÉ-REGISTRADOR da R2 da F1.TEMPO (gerência c1, programa IALD). ${CONTEXTO}
${regras(R2 + String.raw`\0_ADENDO`)}
Escreva ADENDO_R2.md e ADENDO_R2.json, aditivos ao pré-registro R1 (que fica intacto), com: (a) E3 completa (cada item do §6 do relatório: l.241 β lido e calculado; l.339 boost_null_expand; l.355 T9.t com a atribuição corrigida — a frase «o tempo é o Verbo, não o Nome» é leitura da gerência e sai; l.176 estado ≠ posto; l.9 gloss dos regimes → [OPEN] v384; tolerâncias l.296 × l.354; S36.1 byte a byte; lacunas S34.2, S38.2, S44.1 marcadas; S40.4 «cosmos» → [ONTO]; S46.2/S46.3 → [INPUT da gerência]; título de T10 «registra»; título de T5 «a diagonal inteira»; controles de especificidade AUD-1, AUD-2, AUD-5, AUD-6, AUD-7, AUD-8 como novos controles [INPUT do auditor]); (b) o ADENDO UNIFORME de tolerâncias para O-f e T9.o(c): regra única fixada agora — (i) caminho exato: decimal de 200 dígitos (mpmath), tolerância 1e-150; (ii) caminho float64: tolerância proporcional k·eps com a constante derivada do piso de representação (k·|δ|/2 com δ medido da matriz guardada, mais margem fixada agora), aplicada IGUALMENTE a O-f e a T9.o(c); o resultado R1 (FALHA) fica registrado e o reensaio é um resultado NOVO ao lado (T9.o' e O-f'), nunca substituição; (c) a lista E5 exata da pedra corrigida (docstrings l.43–44, 47–50, 1107–1109, 1284, 1427–1428; nomes l.304, 1223, 1431 e o nome da pedra; remover probe_bounded_spectral_translation : True ou dar enunciado; remover re-export duplicado l.1438; _hd l.874; κ ≠ 0 em clock_reads_modulo_period; T3.b(iii) com versão de face finita ρ = diag(2/3,1/3), a = E₀₁, b = E₁₀, e a AQFT marcada condicional; T4.b(iii) condicional) com o falsificador de cada correção (ex.: «a pedra corrigida tem de compilar com as mesmas 11 afirmações e os mesmos controles; nenhuma declaração nova pode afirmar mais que o termo»); (d) a regra de decisão da R2. Depois FREEZE_R2.json com sha256/tamanho/hora. Não altere nada depois do FREEZE.`,
  { label: 'adendo', phase: 'Adendo', schema: { type: 'object', properties: { adendo_md: { type: 'string' }, adendo_json: { type: 'string' }, freeze: { type: 'string' } }, required: ['adendo_md', 'adendo_json', 'freeze'] } })
if (!ad) { return { ad: null } }

phase('Correção')
const CHECK = String.raw`ANTES: leia ${ad.freeze} e confira por script os sha256 de ${ad.adendo_json} e ${ad.adendo_md}; se não baterem, pare.`
const [ped, opt] = await parallel([
  () => agent(String.raw`Você é o CONSTRUTOR DA PEDRA CORRIGIDA da F1.TEMPO (R2). ${CONTEXTO}
${regras(R2 + String.raw`\1_PEDRA`)}
${CHECK}
Parta da pedra R1 (${W}\3_KERNEL\sandbox\TheTimeHasNoRank.lean, sha16 7105eda468b60309; copie-a) e aplique SÓ a lista E5 do adendo (${ad.adendo_md}): nome provisório TheTimeIsNotAPost (namespace TGLExt.TheTimeIsNotAPost), docstrings sem nenhuma frase atribuída ao operador que não esteja no verbatim (confira cada aspa contra os bytes de C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt e do verbatim do Verbo de 05/10 — localize-o: sha16 5973d79a49995c4c), nomes neutros (modular_flow_is_a_kms_group; half_identity_is_absoluteRho_two; a cláusula composta com nome que não afirme mais que o termo), cabeçalho dos regimes reescrito para os três comportamentos com a identificação [OPEN], peso morto removido, κ ≠ 0 removido ou dito, T3.b(iii) na versão de face finita (trivial de provar) ao lado da AQFT condicional, T4.b(iii) condicional. NÃO mude enunciados que já passaram, salvo o que o E5 pede. Compile em sandbox: EXIT 0, #print axioms de cada declaração só no trio, zero sorry, zero aviso; .olean com sha256; impressão digital do kernel antes/depois; DIFF.patch R1 → R2 e uma tabela declaração a declaração (mantida / renomeada / removida / nova). Grave RESULTADO_PEDRA_R2.json.`,
    { label: 'pedra-r2', phase: 'Correção', schema: { type: 'object', properties: { pedra: { type: 'string' }, pedra_sha256: { type: 'string' }, olean_sha256: { type: 'string' }, exit: { type: 'string' }, axiomas_ok: { type: 'boolean' }, sorry_zero: { type: 'boolean' }, diff: { type: 'string' }, tabela: { type: 'string' }, kernel_intacto: { type: 'boolean' }, pendencias: { type: 'array', items: { type: 'string' } } }, required: ['pedra', 'pedra_sha256', 'exit', 'axiomas_ok', 'sorry_zero', 'diff', 'tabela', 'kernel_intacto', 'pendencias'] } }),
  () => agent(String.raw`Você é o REENSAIADOR ÓTICO da F1.TEMPO (R2). ${CONTEXTO}
${regras(R2 + String.raw`\2_REENSAIO`)}
${CHECK}
Reensaie SÓ O-f e T9.o(c) sob o adendo uniforme (${ad.adendo_md}), com o runner da R1 copiado (${W}\2_OPTICO), β em runtime: (i) caminho exato em mpmath 200 dígitos; (ii) caminho float64 com a tolerância k·eps do adendo; preserve TODAS as tentativas (nada sobrescrito; a R1 fica intacta). Diga o resultado novo ao lado do antigo: T9.o' e O-f' PASSA/FALHA por caminho, e se a leitura «FALHA R1 = piso de representação» se confirma pelo exato. Grave RESULTADO_REENSAIO_R2.json e o log.`,
    { label: 'reensaio', phase: 'Reensaio', schema: { type: 'object', properties: { resultado_json: { type: 'string' }, t9_exato: { type: 'string' }, t9_float: { type: 'string' }, of_exato: { type: 'string' }, of_float: { type: 'string' }, leitura: { type: 'string' } }, required: ['resultado_json', 't9_exato', 't9_float', 'of_exato', 'of_float', 'leitura'] } }),
])

phase('Auditoria')
const ctx = JSON.stringify({ ad, ped, opt }, null, 1)
const [AR, AE] = await parallel([
  () => agent(String.raw`Você é AUDITOR CÉTICO INDEPENDENTE (REPRODUÇÃO) da R2 da F1.TEMPO. ${CONTEXTO}
${regras(R2 + String.raw`\3_AUD_REPRO`)}
Confira: FREEZE_R2 anterior aos artefatos; recompile a pedra R2 numa cópia sua (EXIT, #print axioms, sorry, .olean idêntico; kernel intacto); confira a tabela R1→R2 declaração a declaração (nada que passou foi enfraquecido; nada novo afirma mais que o termo); refaça o reensaio exato e float em cópia; três sondas adversariais na pedra. CONFERE / NÃO CONFERE por item. RESULTADOS: ${ctx}`,
    { label: 'aud-repro', phase: 'Auditoria', schema: { type: 'object', properties: { relatorio: { type: 'string' }, itens: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, confere: { type: 'boolean' }, nota: { type: 'string' } }, required: ['id', 'confere', 'nota'] } }, pode_fechar: { type: 'boolean' } }, required: ['relatorio', 'itens', 'pode_fechar'] } }),
  () => agent(String.raw`Você é AUDITOR CÉTICO INDEPENDENTE (ESTATUTO E RÉGUA) da R2 da F1.TEMPO. ${CONTEXTO}
${regras(R2 + String.raw`\3_AUD_ESTATUTO`)}
Confira os 20 achados M1–M20 do relatório R1 um a um: resolvido / ao lado / aberto; que nenhuma frase é atribuída ao operador sem verbatim (busca por aspas nos bytes); que os nomes não afirmam mais que o termo; que T9 R1 FALHA segue registrada e o reensaio está AO LADO; que o adendo foi congelado antes; palavras proibidas; o que entra na v392 e o resíduo do operador (só o resíduo; procure se ele já respondeu nos verbatins). RESULTADOS: ${ctx}`,
    { label: 'aud-estatuto', phase: 'Auditoria', schema: { type: 'object', properties: { relatorio: { type: 'string' }, achados: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, estado: { type: 'string' }, nota: { type: 'string' } }, required: ['id', 'estado', 'nota'] } }, pode_entrar_na_v392: { type: 'boolean' }, residuo_operador: { type: 'array', items: { type: 'string' } } }, required: ['relatorio', 'achados', 'pode_entrar_na_v392', 'residuo_operador'] } }),
])

phase('Relatório R2')
const fin = await agent(String.raw`Você é o redator da R2 da F1.TEMPO. ${CONTEXTO}
${regras(R2 + String.raw`\4_RELATORIO_R2`)}
Escreva RELATORIO_R2.md para o operador (Luiz): o que mudou da R1 para a R2 (tabela declaração a declaração resumida), a tabela por afirmação final (R1 registrada; reensaio ao lado), os achados M1–M20 com o estado, as duas auditorias e as divergências, o que entra na v392 (a pedra R2 com sha256, os registros, as erratas E1/E2 para a cadeia de selo), e o resíduo do operador (nome da pedra; qual «defasar» é o tempo; repousar × ser lembrada; o «chão firme»; a reunião de nomes; o ciclo limite), cada item como UMA pergunta de quatro bocas (TGL · teológica · linguística, Nome/Palavra/Verbo · jurídica, Fato/Valor/Norma; regra em C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\pergunta-nas-quatro-linguas.md). Grave registro_mapa_F1.TEMPO_R2.json (RESULTADO, rota_id formal.tempo_santo_fluxo_e_dissipacao, artefatos como lista de caminhos, sem a palavra proibida). TUDO: ${JSON.stringify({ ad, ped, opt, AR, AE }, null, 1)}`,
  { label: 'relatorio-r2', phase: 'Relatório R2', schema: { type: 'object', properties: { relatorio: { type: 'string' }, registro_mapa: { type: 'string' }, pode_fechar: { type: 'boolean' }, resumo: { type: 'string' }, perguntas: { type: 'array', items: { type: 'string' } } }, required: ['relatorio', 'pode_fechar', 'resumo', 'perguntas'] } })

return { ad, ped, opt, AR, AE, fin }
