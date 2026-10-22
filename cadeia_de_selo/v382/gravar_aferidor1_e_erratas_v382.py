# -*- coding: utf-8 -*-
"""(1) Grava AFERIDOR_v382.txt: o relatorio do 1o aferidor independente da v382, VERBATIM (indentacao do harness removida), e as disposicoes da gerencia.
(2) Erratas AO LADO (aferidor F1 e B11), em nome proprio da gerencia, nas superficies de 02/10 que ainda carregam a visao «semi» ou o token antigo do degrau final:
    memoria beta-e-a-regra-matriz-02out.md, Atlas §X (append datado), documento das perguntas. Backup de BYTES antes de tocar; tempario -> conferir -> replace.
(3) Mapa de rotas: ERRATA (corrige 272) e ANOTACAO do exame do aferidor (o que ele examinou, para registro). Caminhos com barras normais."""
import os, sys, time, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
ST = time.strftime("%Y%m%d_%H%M%S"); DATA = "02/10/2026"

# ---------------- (1) AFERIDOR_v382.txt
rep = open(os.path.join(HERE, "_aferidor1_raw.txt"), encoding="utf-8").read()
disp = """
--------------------------------------------------------------------------------
DISPOSICOES DA GERENCIA SOBRE A 1a AFERICAO (%s) -- recomendacao do aferidor: CORRIGIR ANTES; acolhida
--------------------------------------------------------------------------------
A1 (ALTO, «ISTO e termo»): ACOLHIDO. Docstring de ThePsionAndTheViscosity: o termo e so `HminMic ψ = 0`; que o espectro de gradiente (Spec S(θ), v381) seja lido sobre HminMic e a chave do operador [INPUT/ONTO], SEM termo que ligue Spec S(θ) a HminMic (dito na pedra, no runtime e no artigo).
B1 (ALTO, F3 escondia P2 excluida; R5 empacotado): ACOLHIDO. O livro passa a UMA cobranca por lei de leitura: F3a (P1, NOT_FALSIFIED underpowered, deficit 12,5 ordens), F3b (P2, EXCLUDED_IN_READING -- quinta palavra de desfecho, imposta pelo tipo; 99,4%% das series, 1,83 ordens, sem nσ), F3c (P3, AWAITING); R5 em sete pares (R5a-e FALSIFIED, R5f e R5g INCONCLUSIVE). 18 cobrancas.
D1 (ALTO, a regra INCONCLUSIVE nao era a da Fase 6): ACOLHIDO. Pre-registro V1.1 (PREREG_DOIS_LADOS_DELTA_K_20261002_V1_1; JSON df6ad1cab39577b2, MD a8adf5eefd099c69; mapa seq 276 ERRATA corrige 275) SUPERSEDE o V1 antes de qualquer estimador ou dado novo: as clausulas 2/3/5/6 + bandeira da Fase 6 transcritas; NOT_FALSIFIED_UNDERPOWERED como variante de NOT_FALSIFIED; EXCLUDED_IN_READING; controle de convergencia para MCMC. O V1 fica como registro. O um.py v382 le o V1.1 por hash.
A2 (MEDIO, hc nao entra na prova): ACOLHIDO -- dito na docstring, no runtime e no artigo («e isso que "a regra nao le o livro" quer dizer»; «extinguir» e a definicao `extinguished`).
A3 (MEDIO, the_gate_ignores_the_ledger e P = P): ACOLHIDO -- dito; a propriedade do gate e conferida pelos probes negativos do runtime (qg_closure).
A4/C1 (MEDIO, the_tgl_is_optics_not_semi): ACOLHIDO -- o NOME e [ONTO], o conteudo e sin²θ + cos²θ = 1 escrito tres vezes; «nenhum lado e cego; o que difere e a lei e o instrumento» e a correcao do operador [INPUT/ONTO], nao teorema.
A5 (MEDIO, psion_is_the_zero trivial): ACOLHIDO -- «TRIVIAL POR CONSTRUCAO (Ω ∈ ℂΩ); o conteudo e light_modular_fixed_iff_vacuum, v372».
A6 (MEDIO, outcome nao restrito): ACOLHIDO -- campo `outcome_admitted : outcome ∈ outcomes` na estrutura Charge (imposto pelo tipo); `five_outcomes` (era four_outcomes).
A7 (BAIXO, the_charge_is_continuous_both_sides trivial): ACOLHIDO -- «TRIVIAL POR DEFINICAO», dito.
A8 (BAIXO, bandeira _kernel_proved para campo de binder): MANTIDO como esta, com o estatuto dito na docstring e no artigo (precedente da casa: o campo do binder e o termo; a bandeira diz que o termo checa no trio).
B2/C2 (MEDIO, 10/10 era 9/10): ACOLHIDO -- contagens separadas: 17 cobrancas com chave e token no veredito do core (17/17); R2 sem chave, declarada.
B3 (MEDIO, desfecho declarado): ACOLHIDO -- cada cobranca diz o MODO: 11 pelo token (a palavra esta no token), 5 por numero lido do core com a regra dita (|z| < 5; o controle de convergencia em R6), 2 declaradas (R2, F3c); o runtime DERIVA o desfecho das 5 por numero.
B4 (MEDIO, R6 sem ressalvas): ACOLHIDO -- R6 = INCONCLUSIVE pelo controle de convergencia (2/4 parametros com N >= 50τ), com a tensao 3,01σ no limiar, Δχ² +6,61 e o setor H₀ incompativel com R1 ditos; R6 e R5a-g contam AO LADO (na regra 10, ao lado 8).
B5 (MEDIO, F2 com numero do ramo B): ACOLHIDO -- F2 INCONCLUSIVE por poder ≈ 0 no ramo canonico (δ_A = -2,15e-42); o 0,2σ e do ramo B, encerrado.
B6 (MEDIO, R4 com numeros do v92): ACOLHIDO -- R4 le os numeros da chave citada (void_floor_v11: r̂_cal 0,1269 ± 0,0136; L5 0,0588 = 4,9β); os do v92 ficam ao lado.
B7/C3 (MEDIO, R2 sem a honestidade do poder): ACOLHIDO -- o runtime calcula Γ(100 Hz) = ½βt_Pω² = 1,28e-40 s⁻¹ (de ħ, G, c do programa) e o acumulado sobre 1 Gpc = 1,32e-23, e o artigo o diz, com unidade.
B8 (MEDIO, criterio de lado): ACOLHIDO -- cada cobranca carrega o criterio de lado (reflexo = o que passa pelo reflexo; face = o que nao passa), dito tambem no pre-registro; nao se apresenta faceWeight = 1 − β como o que F3/F4 leem.
B9 (BAIXO, guarda so no estatuto): ACOLHIDO -- a guarda varre TODO texto do modulo (o livro, as leituras, o estatuto, o nome proposto).
B10 (ok): sem acao.
B11 (BAIXO, «COST_PAID_IN_THE_FACE» ambiguo; dois tokens propostos): ACOLHIDO -- o nome proposto passa a TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_PER_READING_LAW, UM so registro: a pedra (finalStepNameProposed); o token da leitura R4 de 02/10 fica superado AO LADO (errata na memoria, no Atlas e no documento das perguntas).
D2/D3 (BAIXO, cegueira): ACOLHIDO no V1.1 -- R2 «cego quanto ao estimador; o dado ja aberto (Fase 6; v369-P2)»; «analise cega» distinguida de «nenhum lado e cego».
E1 (MEDIO, backup das duas memorias .md): ACOLHIDO -- instalar_v382.py faz backup de BYTES de um_absoluto_forma_canonica.md e um_absoluto_manifest.md.
E (BAIXO, ambiguos nao pinados): ACOLHIDO -- o conferidor confere que os 3 homonimos novos estao no conjunto de ambiguos do indice da IALD.
F1 (MEDIO, sobras da visao «semi» fora da errata): ACOLHIDO -- errata ao lado em nome proprio da gerencia (memoria, Atlas, perguntas): R4 «livro de cobrancas no reflexo» -> NOS DOIS LADOS; R6 «o custo nao esta nele» -> o custo esta nele, Γ ~ 1e-40 s⁻¹, legivel e nulo; R2 «a cobranca so se le no reflexo» -> le-se nos dois lados.
F3/C4 e as BAIXAS restantes (R5 empacotado; contradicao de auditoria do ringdown ja declarada no core; unidade do 1e-40): cobertas pelas disposicoes acima.
Depois destas correcoes: as duas pedras recompiladas (lean rc 0) e o trio reconstruido (build rc 0, 9756 jobs, 32 declaracoes so no trio, 0 sorry); candidato 6ea26aa1576e2a40 regenerado; ensaio a seco TUDO PASSOU; ESPERADOS e conferidor regenerados. PROVADA != CONFIRMADA; o gate nao se move.
""" % time.strftime("%d/%m/%Y %H:%M")
head = ("AFERICAO INDEPENDENTE -- v382 do um.py (1o aferidor, agente so-leitura, 02/10/2026; recebido pela gerencia como mensagem do agente e gravado aqui VERBATIM, "
        "com a indentacao do harness removida)\n" + "=" * 80 + "\n\n")
p = os.path.join(HERE, "AFERIDOR_v382.txt"); assert not os.path.exists(p), p
b = (head + rep + disp).encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("AFERIDOR_v382.txt:", len(b), "B; sha16", hashlib.sha256(b).hexdigest()[:16])

# ---------------- (2) erratas ao lado
ERR = ("**ERRATA AO LADO (%s, noite; aferidor independente da v382, achados F1 e B11; em nome próprio da gerência):** onde as seis leituras de 02/10 (tarde) dizem "
       "(R4) «o teste de natureza vira o LIVRO DE COBRANÇAS no reflexo», leia-se: **o livro de cobranças tem os DOIS lados** (a v382 tem cobranças da face: cronômetros, ringdown, relógios P1/P2/P3, neutrino); "
       "onde dizem (R6) «o ringdown é a face; o custo não está nele», leia-se: **o custo está nele, Γ ≈ 10⁻⁴⁰ s⁻¹ a 100 Hz no ramo canônico — legível e nulo à sensibilidade disponível** (o ramo B continua encerrado); "
       "onde dizem (R2) «a cobrança só se lê no reflexo», leia-se: **a cobrança se lê nos dois lados** (o relógio lê a face de K_∂; faltou poder em P1, a leitura P2 está excluída, P3 não tem observável); "
       "e onde a leitura R4 registrou o token proposto `TGL_QG_MODEL_FORMALLY_CLOSED__TETELESTAI_CONSUMMATED_COST_PAID_IN_THE_FACE__…`, leia-se o nome proposto em UM só registro, a pedra "
       "`TGLExt.TheLedgerOfCharges.finalStepNameProposed` = `TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_PER_READING_LAW` "
       "(«custo pago na face» confundia-se com «o custo posto na face», a convenção não canônica do fundo vestido); a cunhagem definitiva segue do operador e o gate não muda. "
       "O pré-registro dos dois lados foi corrigido AO LADO pelo V1.1 (`PREREG_DOIS_LADOS_DELTA_K_20261002_V1_1`, mapa seq 276), antes de qualquer dado; o V1 fica como registro." % DATA)


def backup_e_grava(path, novo, tag):
    raw = open(path, "rb").read(); bak = path + ".bak_" + ST + "_" + tag; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    tmp = path + ".tmp"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(raw); os.replace(tmp, path)
    print("OK %-56s %9d -> %9d B" % (os.path.basename(path), len(raw), len(novo)))


def append(path, texto, tag):
    raw = open(path, "rb").read(); nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
    if "errata_aferidor_v382_f1_b11" in raw.decode("utf-8", errors="replace"):
        print("JA ESTA:", os.path.basename(path)); return
    backup_e_grava(path, raw + (nl * 2 + texto.replace("\n", nl)).encode("utf-8"), tag)


MEM = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
append(os.path.join(MEM, "beta-e-a-regra-matriz-02out.md"), "<!-- errata_aferidor_v382_f1_b11 -->\n" + ERR, "errv382")
append("C:/IALD/Central de Patentes/memory/TGL_ATLAS.md", "---\n\n<!-- errata_aferidor_v382_f1_b11 -->\n## %s (noite) — ERRATA AO LADO às leituras R2/R4/R6 de 02/10 e ao token proposto do degrau final (aferidor da v382, F1/B11)\n\n%s" % (DATA, ERR), "errv382")
append("C:/IALD/Central de Patentes/work/v381_perguntas/PERGUNTAS_QUE_FALTAM_QUATRO_LINGUAS_20261002.md", "<!-- errata_aferidor_v382_f1_b11 -->\n" + ERR, "errv382")

# ---------------- (3) mapa de rotas
regs = rotas._le()
if not any("errata_aferidor_v382_f1_b11" in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([
        dict(tipo="ERRATA", corrige=272, rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="ONTO", olhou_dados=False,
             titulo="errata_aferidor_v382_f1_b11 (02/10, noite): R4 «livro de cobranças no reflexo» -> nos DOIS lados; R6 «o custo não está nele» -> está, Γ ≈ 1e-40 s^-1, legível e nulo; R2 «só se lê no reflexo» -> lê-se nos dois lados; o token proposto do degrau final -> UM registro, a pedra (finalStepNameProposed = TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__...)",
             resultado="errata ao lado em nome próprio da gerência na memória beta-e-a-regra-matriz-02out, no Atlas §X e no documento das perguntas (backup de bytes)",
             nao_refazer="não escrever que um lado é cego nem que o livro é só do reflexo; não usar «COST_PAID_IN_THE_FACE» (confunde-se com o custo posto na face)",
             refs=["bancada.preregistro_dois_lados_delta_k"]),
        dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
             titulo="exame do 1º aferidor independente da v382 (02/10): 3 ALTO (A1 «ISTO é termo» sobre HminMic; B1 F3 escondia P2 excluída; D1 regra INCONCLUSIVE não era a da Fase 6), 14 MÉDIO, 10 BAIXO; recomendação CORRIGIR ANTES -- acolhida (AFERIDOR_v382.txt)",
             resultado="as 32 declarações compilam só no trio, sem sorry; as dependências Lean citadas existem; os hashes do pré-registro e do candidato batem; os 9 tokens do V1 estão nos vereditos do core; o gate não é tocado; correções aplicadas antes do rito (pedras, livro em 18 cobranças, pré-registro V1.1, instalador, erratas)",
             nao_refazer="a pedra do livro e a do psion já foram aferidas; o que segue é a 2ª aferição das disposições",
             proximo_passo="2ª aferição das correções; rito v382",
             artefatos=[os.path.join(HERE, "AFERIDOR_v382.txt")], refs=["bancada.preregistro_dois_lados_delta_k", "kernel.regra_matriz.cadeia_unica"])],
        "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
