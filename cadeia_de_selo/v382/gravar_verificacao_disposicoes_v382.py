# -*- coding: utf-8 -*-
"""(1) Acrescenta ao AFERIDOR_v382.txt o relatorio da VERIFICACAO DAS DISPOSICOES da 3a afericao (o mesmo agente, so leitura), VERBATIM (da mensagem enfileirada
do agente), e as disposicoes da gerencia sobre os seis BAIXOS (R-1 a R-6) e as duas notas opcionais.
(2) Errata AO LADO, em nome proprio da gerencia (R-1), nas tres superficies de 02/10 que registram o nome proposto do degrau final: os DOIS nomes LIDOS por script
(o velho da propria errata da 1a afericao; o novo da pedra no sandbox, conferido igual ao do runtime). Backup de BYTES; temporario -> conferir -> replace.
(3) Mapa: ERRATA (corrige 283) e ANOTACAO do exame da verificacao."""
import os, re, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
ST = time.strftime("%Y%m%d_%H%M%S"); DATA = "02/10/2026"
T = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
HDR = "# Verificação das disposições da 3ª aferição da v382"
MARCA = "errata_verificacao_aferidor3_v382"
MEM = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
SUPS = [os.path.join(MEM, "beta-e-a-regra-matriz-02out.md"), "C:/IALD/Central de Patentes/memory/TGL_ATLAS.md",
        "C:/IALD/Central de Patentes/work/v381_perguntas/PERGUNTAS_QUE_FALTAM_QUATRO_LINGUAS_20261002.md"]

# ---- o relatorio, verbatim, da mensagem enfileirada do agente (nunca da minha propria chamada)
found = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if '"queue-operation"' not in line or "aa2b5030fb5e4aa4a" not in line:
            continue
        d = json.loads(line)
        c = d.get("content")
        if d.get("type") == "queue-operation" and isinstance(c, str) and '<agent-message from="aa2b5030fb5e4aa4a">' in c and HDR in c:
            found = c; break
assert found, "relatorio da verificacao nao achado na fila"
k = found.find("  " + HDR); assert k >= 0
body = found[k:]; e = body.find("</agent-message>"); body = body[:e] if e > 0 else body
rep = "\n".join((l[2:] if l.startswith("  ") else l) for l in body.split("\n")).rstrip() + "\n"
assert "**Recomendação: INSTALAR.**" in rep and "R-6" in rep

# ---- os dois nomes, LIDOS (nunca digitados)
OLD_RE = re.compile(r"TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__[A-Z_]*?FALSIFIABLE_PER_READING_LAW")
olds = set()
for p in SUPS:
    olds |= set(OLD_RE.findall(open(p, encoding="utf-8").read()))
assert len(olds) == 1, olds
OLD = olds.pop()
stone = open(os.path.join(os.path.dirname(HERE), "v376", "kernel_src", "TGLExt", "TheLedgerOfCharges.lean"), encoding="utf-8").read()
NEW = re.search(r'def finalStepNameProposed : String :=\s*"([^"]+)"', stone).group(1)
rt = open(os.path.join(HERE, "v382_runtime.py"), encoding="utf-8").read()
assert re.search(r'^_V382_FINAL_STEP_NAME = "([^"]+)"', rt, re.M).group(1) == NEW, "o nome da pedra != o do runtime"
assert NEW.endswith("FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS") and NEW != OLD
PJ = json.load(open("C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.json", encoding="utf-8"))
NCF = PJ["n_canal_futuro_com_falsified"]; NC = len(PJ["cobrancas"])
assert NCF == sum(1 for x in PJ["cobrancas"] if x.get("canal_futuro_com_falsified") is True)

disp = """
--------------------------------------------------------------------------------
DISPOSICOES DA GERENCIA SOBRE A VERIFICACAO (%s) -- recomendacao: INSTALAR; acolhida, com os seis BAIXOS e as duas notas corrigidos ANTES do rito
(a regra da casa: nada selado com residuo). Cada ponto conferido no core e nos arquivos antes de acolher.
--------------------------------------------------------------------------------
R-1 (o nome proposto velho nas memorias): ACOLHIDO -- errata ao lado nas tres superficies (memoria beta-e-a-regra-matriz-02out, Atlas, documento das perguntas), marcador %s, com os dois nomes LIDOS por script (o velho da propria errata da 1a afericao; o novo da pedra, igual ao do runtime); backup de bytes.
R-2 (a leitura do selo dizia «FALSIFIED possivel»): ACOLHIDO -- a leitura passa a ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME__FALSIFIED_WHERE_THE_READING_LAW_ADMITS_%d_OF_%d_CHANNELS__NONE_MOVES_THE_RULE (a contagem lida do V1.3 pelo gerador, n_canal_futuro_com_falsified, conferida contra as cobrancas) e a THREE_AUDITS_AND_THE_VERIFICATION_OF_THE_DISPOSITIONS_ACCEPTED.
R-3 (o artigo resumia R5 pela forma corrigida): ACOLHIDO -- PT e EN: o estimando e delta<K_d>, lido no reflexo, e nos dois lados pela correcao otica que segue.
R-4 (comentarios do runtime sem o V1.2): ACOLHIDO -- «supersede o V1.2, o V1.1 e o V1» nas duas linhas.
R-5 (mensagens de falha com «V1.2»): ACOLHIDO -- no fabricante (_fazer_selo_v382.py) e no leitor refabricado: o rotulo pr_label LIDO do identificador (problema visivel se o formato falhar); os outros cinco scripts fabricados sairam identicos byte a byte.
R-6 («V1.3» digitado): ACOLHIDO e estendido -- o rotulo lido em todos os textos da cadeia (textos, handoff, registrar, patch do indice); e as contagens digitadas das pedras e do livro trocadas por valores lidos (n_loc e n_psv do AUDIT_NOMES, kf_n, n_ledger); todo campo dos textos conferido estaticamente contra as chaves do leitor: nenhum sem chave.
Nota opcional 1 (a mesma fonte do gate): ACOLHIDA -- o runtime confere no core que cada bandeira do experiment_feed do V11 esta no degrau experimental do gate com o mesmo valor (o codigo do gate as le de la: independent_rite = void_floor_v11), e devolve as chaves do alimentador e as bandeiras do degrau que nao vem dele.
Nota opcional 2 (os dois numeros digitados): ACOLHIDA -- saem das strings; o R3 le do core a referencia de Coma (valor, sigma, fonte) e a D_L TGL mediana, num cruzamento novo; o F4 le a exposicao em fonte_juno; e o limite do R2 passa a conferir a ordem ~1e-40 s^-1 que a correcao do R6 diz.
Depois: candidato, ensaio a seco e esperados regenerados; o mesmo aferidor confere a diferenca entre o candidato anterior (copia guardada ao lado) e o novo. PROVADA != CONFIRMADA; o gate nao se move.
""" % (time.strftime("%d/%m/%Y %H:%M"), MARCA, NCF, NC)
p = os.path.join(HERE, "AFERIDOR_v382.txt"); raw = open(p, "rb").read()
if HDR in raw.decode("utf-8", errors="replace"):
    print("AFERIDOR_v382.txt: a verificacao ja esta")
else:
    bak = p + ".bak_" + ST; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    head = ("\n\n" + "=" * 80 + "\n4a PASSADA -- VERIFICACAO DAS DISPOSICOES DA 3a AFERICAO -- v382 (o mesmo agente, so leitura, 02/10/2026; recebido pela gerencia como mensagem do agente "
            "e gravado aqui VERBATIM, indentacao do harness removida)\n" + "=" * 80 + "\n\n")
    new = raw + (head + rep + disp).encode("utf-8"); tmp = p + ".tmp"; open(tmp, "wb").write(new); assert os.path.getsize(tmp) == len(new) > len(raw); os.replace(tmp, p)
    print("AFERIDOR_v382.txt:", len(raw), "->", len(new), "B; sha16", hashlib.sha256(new).hexdigest()[:16])

ERR = ("**ERRATA AO LADO (%s, noite; verificação das disposições da 3ª aferição da v382, R-1; em nome próprio da gerência):** onde a errata da 1ª aferição diz que o nome proposto do degrau "
       "final tem UM só registro, a pedra, e o escreve como `%s`, leia-se: o registro único continua a pedra (`TGLExt.TheLedgerOfCharges.finalStepNameProposed`), e o nome que ela traz passou, "
       "pela 3ª aferição (M-b: FALSIFIED só onde a lei do canal o admite), a `%s` (lido da pedra por script). O token da leitura R4 ratificada fica como foi ratificado. O nome segue PROPOSTO "
       "ao lado; o gate não muda; renomear é ato do operador." % (DATA, OLD, NEW))


def append(path, texto, tag, marca):
    raw = open(path, "rb").read(); nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
    if marca in raw.decode("utf-8", errors="replace"):
        print("JA ESTA:", os.path.basename(path)); return
    bak = path + ".bak_" + ST + "_" + tag; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + (nl * 2 + ("<!-- %s -->\n" % marca + texto).replace("\n", nl)).encode("utf-8")
    tmp = path + ".tmp"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(raw); os.replace(tmp, path)
    assert open(path, "rb").read()[:len(raw)] == raw, "o prefixo mudou -- restaurar do backup " + bak
    print("OK %-56s %9d -> %9d B" % (os.path.basename(path), len(raw), len(novo)))


append(SUPS[0], ERR, "ver3v382", MARCA)
append(SUPS[1], "---\n\n## %s (noite) — ERRATA AO LADO (verificação das disposições da v382): o nome proposto do degrau final, na pedra, termina em FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS\n\n%s" % (DATA, ERR), "ver3v382", MARCA)
append(SUPS[2], ERR, "ver3v382", MARCA)

regs = rotas._le()
if not any(MARCA in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([
        dict(tipo="ERRATA", corrige=283, rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
             titulo="%s (02/10, noite): o nome proposto do degrau final, dito na errata da 1ª aferição como ...FALSIFIABLE_PER_READING_LAW, passou na pedra (3ª aferição, M-b) a ...FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS; o registro único continua a pedra" % MARCA,
             resultado="errata ao lado em nome próprio da gerência na memória beta-e-a-regra-matriz-02out, no Atlas §X e no documento das perguntas (backup de bytes); os dois nomes lidos por script",
             nao_refazer="não copiar o nome do degrau final para a memória sem lê-lo da pedra", refs=["bancada.preregistro_dois_lados_delta_k"]),
        dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
             titulo="verificação das disposições da 3ª aferição da v382 (02/10, o mesmo agente, só leitura): M-a…M-f e B1…B16 FEITOS; os 20 desfechos recalculados contra o V1.3 campo a campo, sem diferença; 0 ALTO, 0 MÉDIO, 6 BAIXOS (R-1…R-6) e 2 notas; recomendação INSTALAR -- acolhida, com os seis e as duas notas corrigidos antes do rito",
             metodo="o runtime da v382 rodado em memória sobre o core v381; recálculo independente dos 20; comparação campo a campo com o V1.3; as fontes da Fase 6 e das emendas V4/V5 (sha256 e texto); o build de 17:04; as erratas err3 e os seus backups; a busca dos dois nomes propostos nas superfícies de memória",
             resultado="corrigido antes do rito: a leitura do selo (FALSIFIED onde a lei de leitura admite, contado do V1.3); o resumo do R5 no artigo; os comentários e as mensagens do V1.2; o rótulo e as contagens lidos nos textos da cadeia; a mesma fonte do gate conferida no runtime; a referência de Coma e a exposição do JUNO lidas do core; a errata do nome proposto nas memórias",
             nao_refazer="as disposições da 3ª aferição foram verificadas pelo próprio aferidor; o que segue é a conferência da diferença do candidato e o rito",
             proximo_passo="o mesmo aferidor confere a diferença do candidato; rito v382",
             artefatos=[os.path.join(HERE, "AFERIDOR_v382.txt")], refs=["bancada.preregistro_dois_lados_delta_k"])],
        "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")
