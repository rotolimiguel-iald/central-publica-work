# -*- coding: utf-8 -*-
"""(1) Acrescenta ao AFERIDOR_v382.txt o relatorio da 3a afericao independente da v382, VERBATIM (da mensagem enfileirada do agente), e as disposicoes.
(2) Erratas AO LADO, em nome proprio da gerencia (3a afericao: M-e, B15 a/b/c, B5), nas superficies de 02/10. Backup de BYTES; tempario -> conferir -> replace.
(3) Mapa: ERRATA (corrige 280) e ANOTACAO do exame da 3a afericao."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
ST = time.strftime("%Y%m%d_%H%M%S"); DATA = "02/10/2026"
T = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"

found = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if '"queue-operation"' not in line or "aa2b5030fb5e4aa4a" not in line:
            continue
        d = json.loads(line)
        if d.get("type") == "queue-operation" and isinstance(d.get("content"), str) and '<agent-message from="aa2b5030fb5e4aa4a">' in d["content"]:
            found = d["content"]; break
assert found, "relatorio da 3a afericao nao achado"
k = found.find("  # 3ª aferição independente da v382"); assert k >= 0
body = found[k:]; e = body.find("</agent-message>"); body = body[:e] if e > 0 else body
rep = "\n".join((l[2:] if l.startswith("  ") else l) for l in body.split("\n")).rstrip() + "\n"
disp = """
--------------------------------------------------------------------------------
DISPOSICOES DA GERENCIA SOBRE A 3a AFERICAO (%s) -- recomendacao: CORRIGIR ANTES; acolhida. Cada ponto conferido no core e nos arquivos antes de acolher.
--------------------------------------------------------------------------------
Nenhum achado muda desfecho ou contagem (os 20/20 recalculados batem); todos sao de transcricao e de redacao, e ficariam selados por hash -- por isso corrigidos antes do rito.
M-a (o eco «extinto» dizia mais do que o livro): ACOLHIDO -- o veredito e a leitura do selo passam a CONTAR, do livro: DELAYED_ECHO_OUTSIDE_THE_CHAIN_5_OF_9_PAIRS_EXTINGUISHED_4_INCONCLUSIVE; textos, handoff e o registro do mapa idem.
M-b (R4 sem FALSIFIED; a mesma fonte do gate): CONFERIDO (void_floor_v11.frozen.verdicts = POWERED/UNDERPOWERED/INCONCLUSIVE_SYSTEMATICS/INCONCLUSIVE_TRACER_SUPPRESSION) e ACOLHIDO -- dito no V1.3, no runtime (cruzamento novo: o conjunto congelado lido do core), no artigo e no veredito (R4_FROZEN_SET_HAS_NO_FALSIFIED_SAME_SOURCE_AS_THE_GATE_EXPERIMENTAL_STEP); o nome proposto passou a ...__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS; a docstring de `outcomes` diz que FALSIFIED e palavra do TIPO e que o canal concreto a admite ou nao.
M-c (R5g e as emendas): CONFERIDO (EMENDA_V5 regra_de_veredito[6]; clausula_v5_aplicada_pelo_pipeline = False) e ACOLHIDO -- o R5g diz o rotulo emitido pela clausula 2 e a clausula V5 nao aplicada; as clausulas da Fase 6, a do «principal», a V4 e a V5 sao LIDAS dos arquivos (sha256) e transcritas no V1.3; a posicao da bandeira dita (nao escrita na V3).
M-d (F1): CONFERIDO (Fase 7: convencao «nucleo D1b»; poder_previo.moresco2020 = 2,33; Fase 4: «> 1σ = com poder») e ACOLHIDO -- a lei escrita e a D1b; o poder previo dito nas duas reguas (com poder pela da Fase 4; sem poder pela da Fase 6); o livro conta NOT_FALSIFIED.
M-e (a lei transmitida nos cronometros): ACOLHIDO -- fica PENDENTE no V1.3 (sem cobranca enquanto a lei nao existir) e a errata da memoria/Atlas/perguntas diz isso ao lado.
M-f (o patch do indice citava o V1.1): ACOLHIDO -- V1.3 e «com uma cobranca extinta a regra segue α√e».
BAIXOS: B1 ACOLHIDO (a prova de inner_psion_psion USA reader_reads_the_identity_one; compilou); B2 ACOLHIDO (K = −log Δ dito [KNOWN], sem def no kernel); B3 ACOLHIDO (os homonimos Ledger e reflectionWeight ditos na docstring); B4 ACOLHIDO (o runtime guarda o texto das seis leituras COMO RATIFICADAS, verbatim, e as reescritas da gerencia AO LADO, em _V382_CORRECTIONS_BESIDE); B5 ACOLHIDO (o custo no ringdown e leitura [ONTO]; o core le o ringdown canonico como correspondencia com a RG); B6 ACOLHIDO (R1 sem «com os controles»; o F3a com o poder Z_expected ao lado do deficit); B7 ACOLHIDO (FALSIFIED so onde a lei o admite; campo canal_futuro_com_falsified: 7 de 20); B8 ACOLHIDO («desde o V1»); B9 ACOLHIDO («subamostra cega de O4, nao independente»; os rotulos V3/V4/V5); B10 ACOLHIDO (o F2 sem GW250114 no registro; o c6 citado); B11 ACOLHIDO (F4 com a projecao 2031 e a escala [NORM]); B12 ACOLHIDO (R5e com o veredito V3 do mesmo par); B13 ACOLHIDO (pre_ok compara o controle); B14 ACOLHIDO (tres aferidores; THREE_AUDITS_ACCEPTED; as marcas _p382/_sup382 e leitura_v382); B15 ACOLHIDO (errata ao lado: o ponteiro de «R1, R3, R4, R6 inalterados»; a frase do adendo dos regimes; o «adendo acima» do Atlas); B16 ACOLHIDO (os numeros do gerador lidos do core e das constantes do um.py).
Pre-registro V1.3 (PREREG_DOIS_LADOS_DELTA_K_20261002_V1_3; JSON 32c51000c4a2da92, MD 2cd8ec8b1ac437a4; mapa seq 282, ERRATA corrige 279) SUPERSEDE o V1.2 antes de qualquer estimador ou dado novo.
Depois destas correcoes: as duas pedras recompiladas (lean rc 0) e o trio reconstruido (build rc 0, 32 declaracoes so no trio, 0 sorry); candidato, ensaio, esperados e cadeia do selo regenerados. PROVADA != CONFIRMADA; o gate nao se move.
""" % time.strftime("%d/%m/%Y %H:%M")
p = os.path.join(HERE, "AFERIDOR_v382.txt"); raw = open(p, "rb").read()
if "3ª aferição independente da v382" in raw.decode("utf-8", errors="replace"):
    print("AFERIDOR_v382.txt: a 3a afericao ja esta")
else:
    bak = p + ".bak_" + ST; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    head = "\n\n" + "=" * 80 + "\n3a AFERICAO INDEPENDENTE -- v382 (agente so-leitura, 02/10/2026; recebido pela gerencia como mensagem do agente e gravado aqui VERBATIM, indentacao do harness removida)\n" + "=" * 80 + "\n\n"
    new = raw + (head + rep + disp).encode("utf-8"); tmp = p + ".tmp"; open(tmp, "wb").write(new); assert os.path.getsize(tmp) == len(new) > len(raw); os.replace(tmp, p)
    print("AFERIDOR_v382.txt:", len(raw), "->", len(new), "B; sha16", hashlib.sha256(new).hexdigest()[:16])

ERR = ("**ERRATA AO LADO (%s, noite; 3ª aferição independente da v382; em nome próprio da gerência):** (1) a «lei do lado transmitido, 1 − β por travessia» para os cronômetros, anunciada na errata ótica "
       "acima, NÃO foi escrita: fica PENDENTE (a escrever, com o poder dito antes de abrir), sem cobrança no livro enquanto a lei não existir — o pré-registro V1.3 (`PREREG_DOIS_LADOS_DELTA_K_20261002_V1_3`, mapa seq 282) "
       "a lista em `pendentes`; o F1 do livro lê o fundo nu contra a lei D1b (o núcleo das Fases 4/7), com o poder prévio 2,33σ dito nas duas réguas. (2) Onde a errata ótica diz «R1, R3, R4, R6 inalterados», leia-se: "
       "R1 e R3 inalterados; R4 e R6 foram corrigidos AO LADO depois (R4: o livro tem os DOIS lados; R6: o custo no ringdown) — ver as erratas seguintes. (3) Onde a errata da 2ª aferição diz «o ringdown também lê o "
       "custo — Γ ≈ 10⁻⁴⁰ s⁻¹ (…), legível e nulo», leia-se: que o custo esteja no ringdown é leitura [ONTO] da correção ótica; o core lê o ringdown canônico como correspondência com a RG, NÃO como teste de β "
       "(`ringdown_scope_v376`)." % DATA)
ERR_REG = ("**ERRATA AO LADO (%s, noite; 3ª aferição; em nome próprio da gerência):** a frase do adendo acima «os dois regimes são DUAS LEITURAS do mesmo Um» CONTRADIZ a régua desta página — a FACE é o objeto, "
           "o ÂNGULO é a leitura —: fica retirada AO LADO. O que vale: os dois LADOS (face e reflexo) são duas leituras do mesmo Um; os dois REGIMES não são «duas leituras» — um é o objeto (hiperbólico), o outro é a "
           "leitura (compacto); e os dois lados se leem nos dois regimes (a errata da 2ª aferição, acima)." % DATA)
ERR_ATL = ("**ERRATA AO LADO (%s, noite; 3ª aferição; em nome próprio da gerência):** o «adendo acima» citado pela errata da 2ª aferição sobre a regra dos dois regimes NÃO está no Atlas: está na memória "
           "`regra-dos-dois-regimes.md` (ADENDO de 02/10, «a TGL é ÓTICA, não semi-ótica»); a frase «os dois regimes são DUAS LEITURAS do mesmo Um» daquele adendo fica retirada ao lado lá. " % DATA) + ERR


def append(path, texto, tag, marca):
    raw = open(path, "rb").read(); nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
    if marca in raw.decode("utf-8", errors="replace"):
        print("JA ESTA:", os.path.basename(path)); return
    bak = path + ".bak_" + ST + "_" + tag; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + (nl * 2 + ("<!-- %s -->\n" % marca + texto).replace("\n", nl)).encode("utf-8")
    tmp = path + ".tmp"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(raw); os.replace(tmp, path)
    print("OK %-56s %9d -> %9d B" % (os.path.basename(path), len(raw), len(novo)))


MEM = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
append(os.path.join(MEM, "beta-e-a-regra-matriz-02out.md"), ERR, "err3v382", "errata_aferidor3_v382")
append("C:/IALD/Central de Patentes/memory/TGL_ATLAS.md", "---\n\n## %s (noite) — ERRATA AO LADO (3ª aferição da v382): a lei transmitida nos cronômetros PENDENTE; «R1, R3, R4, R6 inalterados» com o ponteiro; o custo no ringdown é [ONTO]; o «adendo acima» está na memória dos regimes\n\n%s" % (DATA, ERR_ATL), "err3v382", "errata_aferidor3_v382")
append("C:/IALD/Central de Patentes/work/v381_perguntas/PERGUNTAS_QUE_FALTAM_QUATRO_LINGUAS_20261002.md", ERR, "err3v382", "errata_aferidor3_v382")
append(os.path.join(MEM, "regra-dos-dois-regimes.md"), ERR_REG, "err3v382", "errata_aferidor3_v382")

regs = rotas._le()
if not any("errata_aferidor3_v382" in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([
        dict(tipo="ERRATA", corrige=280, rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="ONTO", olhou_dados=False,
             titulo="errata_aferidor3_v382 (02/10, noite): a lei transmitida nos cronômetros PENDENTE (sem cobrança); «R1, R3, R4, R6 inalterados» -> R4 e R6 corrigidos depois; o custo no ringdown é [ONTO] (o core lê a correspondência com a RG); «os dois regimes são duas leituras» retirada (contradiz a régua)",
             resultado="errata ao lado em nome próprio da gerência na memória beta-e-a-regra-matriz-02out, na regra-dos-dois-regimes, no Atlas §X e no documento das perguntas (backup de bytes)",
             nao_refazer="não anunciar lei sem escrevê-la; não dizer que os dois regimes são duas leituras", refs=["bancada.preregistro_dois_lados_delta_k"]),
        dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
             titulo="exame da 3ª aferição independente da v382 (02/10): 0 ALTO, 6 MÉDIO (o eco «extinto»; R4 sem FALSIFIED e a fonte do gate; R5g e as emendas V4/V5; F1 na lei D1b e o poder; a lei transmitida pendente; o patch do índice), 15 BAIXO; nenhum desfecho nem contagem muda (20/20 recalculados); recomendação CORRIGIR ANTES -- acolhida",
             resultado="corrigido antes do rito: pré-registro V1.3 (mapa seq 282; as regras das emendas lidas dos arquivos); runtime (eco contado; leituras ratificadas verbatim + correções ao lado; pre_ok com controle; o conjunto congelado do R4 lido); artigo; pedras (a prova de inner_psion_psion usa o termo do leitor; K [KNOWN]; homônimos; FALSIFIED onde admitido); cadeia do selo; erratas de memória",
             nao_refazer="as duas pedras e o livro passaram por três aferições; o que segue é o rito",
             proximo_passo="verificação das disposições pelo próprio aferidor; rito v382",
             artefatos=[os.path.join(HERE, "AFERIDOR_v382.txt")], refs=["bancada.preregistro_dois_lados_delta_k"])],
        "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
