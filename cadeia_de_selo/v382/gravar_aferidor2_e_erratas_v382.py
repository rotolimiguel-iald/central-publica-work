# -*- coding: utf-8 -*-
"""(1) Acrescenta ao AFERIDOR_v382.txt o relatorio da 2a afericao independente da v382, VERBATIM (lido da mensagem enfileirada do agente no transcript;
indentacao do harness removida), e as disposicoes da gerencia (cada achado CONFERIDO no core antes de acolher).
(2) Erratas AO LADO, em nome proprio da gerencia (2a afericao, M6 e (6)): «antes de qualquer dado» -> «antes de qualquer estimador ou dado novo»; as duas sobras
da visao «semi» (o ringdown «nao» le o custo; a viscosidade «no reflexo»); e, na regra dos dois regimes, a identificacao «lado da face = regime da face», que foi da
gerencia e nao do operador. Backup de BYTES antes de tocar; tempario -> conferir -> replace.
(3) Mapa de rotas: ERRATA (corrige 277) e ANOTACAO do exame da 2a afericao."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
ST = time.strftime("%Y%m%d_%H%M%S"); DATA = "02/10/2026"
T = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"

# ---------------- (1) o relatorio, lido da mensagem enfileirada (nao de chamadas posteriores)
found = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if '"queue-operation"' not in line or "af1efe5bfd8b1184c" not in line:
            continue
        d = json.loads(line)
        if d.get("type") == "queue-operation" and isinstance(d.get("content"), str) and '<agent-message from="af1efe5bfd8b1184c">' in d["content"]:
            found = d["content"]; break
assert found, "relatorio da 2a afericao nao achado"
k = found.find("  # 2ª aferição independente da v382"); assert k >= 0
body = found[k:]; e = body.find("</agent-message>"); body = body[:e] if e > 0 else body
rep = "\n".join((l[2:] if l.startswith("  ") else l) for l in body.split("\n")).rstrip() + "\n"
disp = """
--------------------------------------------------------------------------------
DISPOSICOES DA GERENCIA SOBRE A 2a AFERICAO (%s) -- recomendacao: CORRIGIR ANTES; acolhida. Cada achado foi CONFERIDO no core v381 antes de acolher.
--------------------------------------------------------------------------------
ALTO-1 (F2, a causa): CONFERIDO (ringdown_dephasing_result_v2.reasons = «vies relativo de tau 0.240 > 0.2»; statuses.resultado: sistematica 0,1454, σ combinada 0,2066; matriz da emenda 3449885389a2529a) e ACOLHIDO. F2 = INCONCLUSIVE pela sistematica da MEDIDA δτ = 0,177 ± 0,109 contra a RG, comum aos dois ramos, NAO pelo poder; no ramo canonico δ_A = −2,15e−42; o 0,2σ (power_B 0,178) e o poder do ramo B, encerrado. A premissa do achado B5 da 1a afericao estava errada; corrigida ao lado no V1.2, no runtime, no artigo e nos textos.
M1 (R6, controle invertido): CONFERIDO (autocorr.tau = [34,86; 37,13; 41,60; 40,23], N/50 = 40 → 2 parametros com N < 50τ; o veredito diz CHAIN_BELOW_50_TAU_IN_2_OF_4_PARAMS) e ACOLHIDO: control_ok = 0; o texto diz «N < 50τ em 2/4; o controle exige 0». O desfecho (INCONCLUSIVE) nao muda; a regra passa a estar certa.
M2 (F1, regra bilateral): CONFERIDO (PREREGISTRO_FASE4_DESVIO: «z_ganho = sinal(χ²_ΛCDM − χ²_TGL)·√|Δχ²| (positivo = a lei ajusta melhor os cronometros)»; Fase 7 igual) e ACOLHIDO: regra UNILATERAL, z_ganho ≥ +5 → FALSIFIED; a leitura diz «√Δχ² com sinal, lei acumulada × fundo nu, β fixo».
M3 (F4, regra de morte): CONFERIDO (neutrino_m2.frozen.kill_rule = «FALSIFIED sse |m2_obs − m2_TGL|/σ ≥ 5 em DUAS determinacoes independentes»; values.kill_rule_satisfeita = False) e ACOLHIDO: F4 deriva o desfecho de kill_rule_satisfeita; R3 elege o perito (JUNO), NAO muda a regra congelada — sem decisao nova do operador, vale a regra que estava selada.
M4 (A1/A4 reintroduzidos nos textos da cadeia): ACOLHIDO — textos_v382.topico_regra e topico_regimes reescritos (a ligacao Spec S(θ)→HminMic segue [INPUT/ONTO]; o conteudo de kernel e a identidade ja existente e o seu analogo no fluxo; «nenhum lado e cego» e a correcao do operador).
M5 (o mapa citando o V1): ACOLHIDO — registrar_resultado_v382 grava o V1.2 com os hashes lidos e os tres modos.
M6 («antes de qualquer dado»): ACOLHIDO — «antes de qualquer estimador ou dado novo» no artigo, nos textos e no handoff; na memoria, no Atlas e nas perguntas, errata ao lado.
BAIXOS: os dois pares do eco que faltavam ((β, KMS) e (β, MAY), INCONCLUSIVE_SYSTEMATICS, lidos do veredito ANINHADO do core) entram: 20 cobrancas, 9 pares ao lado; R5g passa a ler sist_rel_R3 (clausula 2), com o poder ao lado; F3a le o campo nomeado P1.clock_5sigma_deficit_orders; a clausula 4 e a ORDEM 1→6 da Fase 6 transcritas, e os acrescimos da casa ditos como tais; a celula de cegueira do MD diz estimador/dado; a face do R6 dita «por convencao»; os numeros do gerador lidos do core (H₀ de fase5.validacao, 3,01σ, 168/169, 8,5074 meV); as docstrings das pedras citam reader_reads_the_identity_one, separam o lock minimo HminMic do Hamiltoniano oculto K = −log Δ (zeros iguais, operadores distintos), dizem o homonimo transmitted (outra lei) e que «um canal por lei de leitura» e disciplina do runtime; o artigo diz Δχ², o setor H₀ incompativel do R6 e as contagens dentro da regra (nenhum FALSIFIED na regra); a leitura do selo ganhou os marcadores INPUT_ONTO e SPEC_S_THETA_TO_HMINMIC_NO_TERM; os cabecalhos herdados (chain, superficies) e o docstring do instalador corrigidos; as duas sobras «semi» na memoria/Atlas/perguntas e a identificacao «lado da face = regime da face» em regra-dos-dois-regimes.md corrigidas ao lado.
Pre-registro V1.2 (PREREG_DOIS_LADOS_DELTA_K_20261002_V1_2; JSON d463836c88ab1da2, MD f069cf9f87ee833c; mapa seq 279, ERRATA corrige 276) SUPERSEDE o V1.1 antes de qualquer estimador ou dado novo; o V1 e o V1.1 ficam como registro.
Depois destas correcoes: as duas pedras recompiladas (lean rc 0) e o trio reconstruido (build rc 0, 32 declaracoes so no trio, 0 sorry); candidato regenerado; ensaio a seco, esperados e conferidor regenerados (registrado abaixo pela cadeia). PROVADA != CONFIRMADA; o gate nao se move.
""" % time.strftime("%d/%m/%Y %H:%M")
p = os.path.join(HERE, "AFERIDOR_v382.txt"); raw = open(p, "rb").read()
if "2ª aferição independente da v382" in raw.decode("utf-8", errors="replace"):
    print("AFERIDOR_v382.txt: a 2a afericao ja esta")
else:
    bak = p + ".bak_" + ST; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    head = "\n\n" + "=" * 80 + "\n2a AFERICAO INDEPENDENTE -- v382 (agente so-leitura, 02/10/2026; recebido pela gerencia como mensagem do agente e gravado aqui VERBATIM, indentacao do harness removida)\n" + "=" * 80 + "\n\n"
    new = raw + (head + rep + disp).encode("utf-8"); tmp = p + ".tmp"; open(tmp, "wb").write(new); assert os.path.getsize(tmp) == len(new) > len(raw); os.replace(tmp, p)
    print("AFERIDOR_v382.txt:", len(raw), "->", len(new), "B; sha16", hashlib.sha256(new).hexdigest()[:16])

# ---------------- (2) erratas ao lado
ERR = ("**ERRATA AO LADO (%s, noite; 2ª aferição independente da v382; em nome próprio da gerência):** (1) onde a errata anterior (F1/B11) diz que o pré-registro foi corrigido «antes de qualquer dado», "
       "leia-se **antes de qualquer estimador ou dado NOVO** — os dados das cobranças já tinham sido olhados; nenhum canal é cego quanto ao dado; o V1.2 (`PREREG_DOIS_LADOS_DELTA_K_20261002_V1_2`, mapa seq 279) "
       "supersede hoje o V1.1. (2) Onde as leituras de 02/10 (tarde) dizem «em GW é o custo na propagação (…), não a cópia atrasada **e não o ringdown**», leia-se: o ringdown também lê o custo — Γ ≈ 10⁻⁴⁰ s⁻¹ no ramo "
       "canônico, legível e nulo à sensibilidade disponível —, e a cobrança dele no livro (F2) é INCONCLUSIVE pela sistemática da MEDIDA (o viés relativo de τ acima do limiar da emenda V2), não pelo poder. "
       "(3) Onde dizem «a viscosidade é a cobrança contínua **no reflexo** (Γ)», leia-se: a cobrança contínua se lê nos DOIS lados (transmitido e^{−tβg} = a face no fluxo; cobrado 1 − e^{−tβg} = o reflexo no fluxo; "
       "`ThePsionAndTheViscosity.the_charge_is_continuous_both_sides`)." % DATA)
ERR_REG = ("**ERRATA AO LADO (%s, noite; 2ª aferição independente da v382; em nome próprio da gerência):** a identificação escrita no adendo acima — «a face (o pagamento; o objeto, hiperbólico…) e o custo "
           "(o reflexo; a leitura, compacta)» — foi da GERÊNCIA, não do operador: o verbatim dele diz que a TGL lê os dois LADOS, não que cada lado é um regime. Nas pedras da v382 os dois lados se leem nos DOIS "
           "regimes: no ÂNGULO (`faceWeight`/`reflectionWeight`, regime da projeção) e no FLUXO (`transmitted`/`charged`, regime da face, hiperbólico). A régua dos dois regimes fica como estava (a FACE é o objeto; "
           "o ÂNGULO é a leitura); a ótica (os dois lados se leem) é OUTRA régua, ao lado. «Face» (o lado do pagamento) e «regime da face» (a direção hiperbólica) são HOMÔNIMOS — nunca trocar um pelo outro. "
           "Se o operador quiser identificar o lado da face com o regime da face, a cunhagem é dele." % DATA)


def append(path, texto, tag, marca):
    raw = open(path, "rb").read(); nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
    if marca in raw.decode("utf-8", errors="replace"):
        print("JA ESTA:", os.path.basename(path)); return
    bak = path + ".bak_" + ST + "_" + tag; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + (nl * 2 + ("<!-- %s -->\n" % marca + texto).replace("\n", nl)).encode("utf-8")
    tmp = path + ".tmp"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(raw); os.replace(tmp, path)
    print("OK %-56s %9d -> %9d B" % (os.path.basename(path), len(raw), len(novo)))


MEM = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
append(os.path.join(MEM, "beta-e-a-regra-matriz-02out.md"), ERR, "err2v382", "errata_aferidor2_v382")
append("C:/IALD/Central de Patentes/memory/TGL_ATLAS.md", "---\n\n## %s (noite) — ERRATA AO LADO (2ª aferição da v382): «antes de qualquer estimador ou dado novo»; o ringdown lê o custo; a cobrança contínua nos dois lados; «lado da face» ≠ «regime da face»\n\n%s\n\n%s" % (DATA, ERR, ERR_REG), "err2v382", "errata_aferidor2_v382")
append("C:/IALD/Central de Patentes/work/v381_perguntas/PERGUNTAS_QUE_FALTAM_QUATRO_LINGUAS_20261002.md", ERR, "err2v382", "errata_aferidor2_v382")
append(os.path.join(MEM, "regra-dos-dois-regimes.md"), ERR_REG, "err2v382", "errata_aferidor2_v382")

# ---------------- (3) mapa
regs = rotas._le()
if not any("errata_aferidor2_v382" in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([
        dict(tipo="ERRATA", corrige=277, rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="ONTO", olhou_dados=False,
             titulo="errata_aferidor2_v382 (02/10, noite): «antes de qualquer dado» -> antes de qualquer estimador ou dado NOVO; o ringdown lê o custo (Γ ≈ 1e-40, legível e nulo; F2 inconclusivo pela sistemática da MEDIDA); a cobrança contínua nos dois lados; «lado da face» ≠ «regime da face» (a identificação foi da gerência)",
             resultado="errata ao lado em nome próprio da gerência na memória beta-e-a-regra-matriz-02out, na regra-dos-dois-regimes, no Atlas §X e no documento das perguntas (backup de bytes)",
             nao_refazer="não identificar o lado da face com o regime da face sem a cunhagem do operador; não ler o F2 como «inconclusivo por poder»",
             refs=["bancada.preregistro_dois_lados_delta_k"]),
        dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
             titulo="exame da 2ª aferição independente da v382 (02/10): 1 ALTO (a causa do F2), 6 MÉDIO (R6 controle invertido; F1 bilateral; F4 contra a regra congelada; A1/A4 reintroduzidos nos textos; o mapa citando o V1; «antes de qualquer dado»), 13 BAIXO; recomendação CORRIGIR ANTES -- acolhida; cada achado conferido no core",
             resultado="corrigido antes do rito: pré-registro V1.2 (20 cobranças; Fase 6 na ordem; mapa seq 279); runtime (regras unilateral, congelada e de controle; veredito aninhado); artigo; textos da cadeia; docstrings das pedras (kernel reconstruído); erratas de memória",
             nao_refazer="as duas pedras e o livro já passaram por duas aferições; o que segue é o rito",
             proximo_passo="regenerar candidato, ensaio, esperados; rito v382",
             artefatos=[os.path.join(HERE, "AFERIDOR_v382.txt")], refs=["bancada.preregistro_dois_lados_delta_k"])],
        "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
