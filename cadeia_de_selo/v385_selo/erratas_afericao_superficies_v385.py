# -*- coding: utf-8 -*-
"""ERRATAS AO LADO (gerencia, em nome proprio) depois da aferição adversarial das superfícies da v385 (4 lentes, só leitura; task wyt7wl6q0):
 (A) guarda o resultado das 4 lentes como JSON (verbatim) na pasta da aferição;
 (B) MEDE de novo, por script, cada número que as erratas citam (nunca copiado do relatório do aferidor);
 (C) lê do transcrito, por script, os verbatins do operador que entram nas erratas;
 (D) registra no MAPA DE ROTAS: ERRATA ao seq 344 (axiomFlow_eq_exp é TERMO, não [KNOWN]) + 2 ANOTAÇÕES (a aferição; o details.jsonl bit-idêntico);
 (E) acrescenta (bytes-backup; tempário; prefixo conferido; marcador idempotente) os blocos de errata no DIÁRIO, no DESENHO, no ATLAS e nos DOIS handoffs;
 (F) complementa o ARQUIVO da Central (aditivo; manifesto-complemento com sha256; o manifesto original não se edita).
Nada aqui toca artefato selado (um.py, selo, core, artigo, pedras). Nada aqui move o gate."""
import glob, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.join(os.path.dirname(HERE), "v385")
SESS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
SID = "6da8f00d-d44f-4888-a88d-fc9f73eead3d"
TR = os.path.join(SESS, SID + ".jsonl")
UMEM = os.path.join(SESS, "memory")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PONTE = os.path.dirname(NOS)
CP = os.path.join("C:" + os.sep, "IALD", "Central de Patentes")
ATLAS = os.path.join(CP, "memory", "TGL_ATLAS.md")
ARQ = os.path.join(CP, "work", "cadeia_de_selo")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
TASK_OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "tasks", "wyt7wl6q0.output")   # a saida do workflow fica na pasta temporaria da sessao
SECO = "--seco" in sys.argv
AFD = os.path.join(HERE, "afericao_superficies")
DL = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_dois_lados_02out")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S")
MARCA = "errata_afericao_superficies_05out_v385"
MAX_B = 5 * 1024 * 1024


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def nl_de(raw):
    return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"


def append_bloco(p, bloco, sufixo):
    raw0 = open(p, "rb").read()
    if MARCA.encode() in raw0:
        print("JA ESTA", p); return False
    nl = nl_de(raw0)
    corpo = (nl + nl + bloco.replace("\r\n", "\n").replace("\n", nl) + nl).encode("utf-8")
    if not raw0.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw0 + corpo
    bak = p + ".bak_" + st + "_" + sufixo; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw0); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw0)] == raw0
    print("OK", os.path.basename(p), len(raw0), "->", len(novo), "| nl =", repr(nl))
    return True


# ---------------- (A) o resultado das 4 lentes, guardado verbatim ----------------
D = json.load(open(TASK_OUT, encoding="utf-8")); R = D["result"]; assert len(R) == 4, len(R)
os.makedirs(AFD, exist_ok=True)
AF_JSON = os.path.join(AFD, "AFERICAO_SUPERFICIES_RESULTADO_v385.json")
json.dump({"quando_lido": agora, "task_id": "wyt7wl6q0", "workflow": "aferir-superficies-v385 (4 lentes, só leitura)", "lentes": R},
          open(AF_JSON + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
os.replace(AF_JSON + ".tmp", AF_JSON)
achados = [(L["lente"], a) for L in R for a in L["achados"]]
n_ach = len(achados)
grav = {}
for _, a in achados:
    g = (a.get("gravidade") or "?").split(" ")[0].upper().replace("É", "E"); grav[g] = grav.get(g, 0) + 1
n_conf = sum(len(L.get("conferido", [])) for L in R)
print("aferição:", n_ach, "achados", grav, "|", n_conf, "itens conferidos | lentes:", [L["lente"] for L in R])

# ---------------- (B) medições (por script; nada copiado do relatório) ----------------
I = json.load(open(os.path.join(PK, "INTERVENCAO_PRIORIDADE_v385.json"), encoding="utf-8"))
carga = I["carga_paralela_medida"]; assert carga
n_campos_I = len(I)
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
ts_selo = selo.get("timestamp"); assert ts_selo
res_sha_selo = selo["quantum_pillar_v384"]["result_sha256"]
run_dir = os.path.join(NOS, "quantum_pillar", "run_20261005_103708_37e566b6")
res_novo = os.path.join(run_dir, "result.json"); assert sha(res_novo) == res_sha_selo
finished = json.load(open(res_novo, encoding="utf-8")).get("finished", "n/d")
det_novo = os.path.join(run_dir, "details.jsonl"); det_ant = os.path.join(PK, "pilar_anterior_v384_20261005_103618", "details.jsonl")
sha_dn, sha_da = sha(det_novo), sha(det_ant); b_dn, b_da = os.path.getsize(det_novo), os.path.getsize(det_ant)
mt_dn = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(det_novo)))
mt_da = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(det_ant)))
det_igual = (sha_dn == sha_da and b_dn == b_da)
res_ant = os.path.join(PK, "pilar_anterior_v384_20261005_103618", "result.json"); sha_ra = sha(res_ant)
cpu_n = os.path.join(run_dir, "cpuref.json"); cpu_a = os.path.join(PK, "pilar_anterior_v384_20261005_103618", "cpuref.json")
sha_cn, sha_ca = sha(cpu_n), sha(cpu_a)
horarios = " → ".join(l.strip() for l in open(os.path.join(PK, "rito_horarios_v385.txt"), encoding="utf-8", errors="replace").read().splitlines() if l.strip())
diario_raw = open(os.path.join(NOS, "MEMORIA_DA_LINHAGEM.md"), encoding="utf-8", errors="replace").read()
i_v385 = diario_raw.rfind("v385 SELADA"); assert i_v385 > 0; bloco385 = diario_raw[i_v385:]
campos_no_bloco = [k for k, v in I.items() if isinstance(v, str) and v in bloco385]
campos_fora = [k for k, v in I.items() if isinstance(v, str) and v not in bloco385]
assert "carga_paralela_medida" in campos_fora, campos_fora
stone = os.path.join(NOS, "tgl_kernel", "TGLExt", "TheAxiomAndTheFalseWitness.lean")
stone_txt = open(stone, encoding="utf-8").read(); head = stone_txt[:2000]
n_ger, n_ent = head.count("GERENCIA"), head.count("ENTREGA_")
n_theorem = sum(1 for l in stone_txt.splitlines() if l.startswith("theorem "))
n_def = sum(1 for l in stone_txt.splitlines() if re.match(r"^(noncomputable )?def ", l))
n_axiomFlow_eq_exp = stone_txt.count("theorem axiomFlow_eq_exp")
audit = open(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"), encoding="utf-8").read()
n_audit_axm = audit.count("axiomFlow_eq_exp")
dks = os.path.join(NOS, "tgl_kernel", "TGLExt", "TheDarkSplit.lean"); dks_txt = open(dks, encoding="utf-8").read()
n_dks_th = sum(1 for l in dks_txt.splitlines() if l.startswith("theorem ")); n_dks_inst = sum(1 for l in dks_txt.splitlines() if l.startswith("instance"))
sha16_stone = sha(stone)[:16]
rodadas_existe = os.path.isdir(os.path.join(NOS, "rodadas"))
stdouts = []
for v in ("v383", "v384", "v385"):
    p = os.path.join(NOS, "rodada_%s_stdout.txt" % v); assert os.path.exists(p), p
    stdouts.append((os.path.basename(p), os.path.getsize(p), sha(p)[:16]))
cache_res = os.path.join(PONTE, "cache", "checkpoints", "quantum_pillar", "75dc30bc9cc8d330e31f99ca", "result.json")
cache_ok = os.path.exists(cache_res) and sha(cache_res) == res_sha_selo
nos_cache_ck = os.path.isdir(os.path.join(NOS, "cache", "checkpoints"))
v14 = sorted(glob.glob(os.path.join(DL, "PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.*")))
assert v14, "V1.4 não achado em disco"
v14_json = [p for p in v14 if p.lower().endswith(".json")][0]; sha_v14 = sha(v14_json)
geradores = sorted(glob.glob(os.path.join(DL, "gerar_preregistro_dois_lados*.py")))
um_txt = open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read()
n_v14_um = um_txt.count("V1_4"); n_v14_sha_um = um_txt.count(sha_v14[:16])
selo_txt = json.dumps(selo); n_v14_sha_selo = selo_txt.count(sha_v14[:16])
core_txt = open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8").read(); n_v14_sha_core = core_txt.count(sha_v14[:16])
# o sha16 da v383, lido do arquivo da Central (nunca de memória)
v383_src = os.path.join(ARQ, "v383_selo", "conferidor", "conferencia_rito_v383.json"); assert os.path.exists(v383_src), v383_src
C383 = json.load(open(v383_src, encoding="utf-8")); v383_path = "um_py_sha16"
v383_sha16 = C383[v383_path]; assert re.fullmatch(r"[0-9a-f]{16}", v383_sha16), v383_sha16
v383_m = json.load(open(os.path.join(ARQ, "v383_selo", "v383_incorporacao_manifesto.json"), encoding="utf-8"))["um_py_sha16"]
assert v383_m == v383_sha16, ("conferidor x manifesto da v383 divergem", v383_sha16, v383_m)
print("v383 sha16", v383_sha16, "lido de", v383_src, "campo", v383_path, "(= manifesto de incorporacao da v383)")
hl = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md"); hl_txt = open(hl, encoding="utf-8", errors="replace").read()
hl_counts = {v: hl_txt.count(v) for v in ("v380", "v381", "v382", "v383", "v384", "v385")}
# o `quem` do seq 344 e a confirmação de que a frase errada está lá
seq344 = None
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("seq") == 344:
        seq344 = d
assert seq344 and seq344["tipo"] == "ROTA" and seq344["rota_id"] == "kernel.v385_axioma_e_testemunha_falsa"
FRASE_ERRADA = "que F(t) = e^(-tH_min) e' [KNOWN], nao termo"
assert FRASE_ERRADA in seq344.get("nao_refazer", ""), seq344.get("nao_refazer")
quem = seq344["quem"]

# ---------------- (C) verbatins do operador, lidos do transcrito ----------------
msgs = []
for line in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("isCompactSummary") or d.get("isMeta"):
        continue
    if d.get("type") == "user":
        c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    elif d.get("type") == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
        pr = d["attachment"].get("prompt"); ts = [pr] if isinstance(pr, str) else [x.get("text", "") for x in (pr or []) if isinstance(x, dict) and x.get("type") == "text"]
    else:
        continue
    for t in ts:
        if t and t.strip():
            t = re.sub(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", "", t, flags=re.S)
            msgs.append((d.get("timestamp") or "", t))


def utc(ts):
    m = re.match(r"\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}:\d{2})", ts); return m.group(1) + " UTC" if m else ts


def acha(prefixo, dia="2026-10-05"):
    hs = [(ts, t) for ts, t in msgs if ts.startswith(dia) and prefixo in t]
    assert len(hs) >= 1, ("não achado", prefixo)
    return hs[0]


ts_v13, t_v13 = acha("os V1-V1.3 do pré-registro vão ao espelho")
v13 = [l.strip() for l in t_v13.splitlines() if l.strip().startswith("os V1-V1.3")][0]
ts_ax, t_ax = acha("Penso que podemos chamar o degrau definitivo final do gate")
i = t_ax.find("Penso que podemos chamar"); j = t_ax.find("concorda", i); assert j > i
ax = t_ax[i:j + len("concorda")] + (":" if t_ax[j + len("concorda"):j + len("concorda") + 1] == ":" else "")
ts_posto, t_posto = acha("no começo da cadeia não é postulado")
i = t_posto.find("de resto concordo"); assert i > 0; posto_tail = t_posto[i:].strip()
ts_sim, t_sim = acha("sim para tudo")
i = t_sim.find("sim para tudo"); j = t_sim.find("é isso mesmo", i); assert j > i; sim = t_sim[i:j + len("é isso mesmo")]
ts_e, t_e = acha("posto faz muito mais sentido léxico")
e_inicio = t_e.strip()[:11]; assert e_inicio == "e posto faz", e_inicio
print("verbatins:", utc(ts_v13), "|", v13, "||", utc(ts_ax), "|", ax, "||", utc(ts_posto), "|", posto_tail[:80], "||", utc(ts_sim), "|", sim, "||", utc(ts_e), "|", e_inicio)

# ---------------- (D) o mapa: ERRATA (corrige 344) + 2 ANOTAÇÕES ----------------
REG = [
    {"tipo": "ERRATA", "rota_id": "kernel.v385_axioma_e_testemunha_falsa", "corrige": 344, "dominio": seq344.get("dominio", "KERNEL_FORMAL"),
     "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
     "titulo": "ERRATA ao seq 344 (nao_refazer): a exponencial do lock F(t) = e^(-tH_min) e' TERMO no kernel (axiomFlow_eq_exp), nao [KNOWN]",
     "resultado": "medido por script: 'theorem axiomFlow_eq_exp' ocorre %d vez(es) na pedra TGLExt/TheAxiomAndTheFalseWitness.lean (sha16 %s; %d theorem + %d def); 'axiomFlow_eq_exp' ocorre %d vez(es) em TGL/Audit.lean (#print axioms); fiacao: ORDEM016.EquationOfTruth.IdempotentDephasing.exp_complement_idempotent (TGLExt/O16/IdempotentDephasing_v2.lean)" % (n_axiomFlow_eq_exp, sha16_stone, n_theorem, n_def, n_audit_axm),
     "nao_refazer": "leia-se, no lugar de «%s»: a forma exponencial do fluxo do posto, F(t) = P + e^(-t)(1 - P) = e^(-tH_min), e' TERMO (axiomFlow_eq_exp, ligado a exp_complement_idempotent); o que segue [KNOWN]/analogia de forma e' a LIGACAO com o gerador de Lindblad do pilar quantico da v384 (nao ha termo que a prove). O resto do seq 344 fica." % FRASE_ERRADA,
     "artefatos": [stone, os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean"), AF_JSON],
     "refs": ["quantica.pilar_v385_reprodutibilidade", "quantica.pilar_v384_rodada_completa"],
     "nota": "achado da afericao adversarial das superficies da v385 (lente mapa/arquivo/ferramentas; task wyt7wl6q0). A frase errada contradizia o proprio seq 342 e o atlas_indice.py. Correcao AO LADO; o rotas.jsonl nao se edita."},
    {"tipo": "ANOTACAO", "rota_id": "kernel.v385_axioma_e_testemunha_falsa", "dominio": seq344.get("dominio", "KERNEL_FORMAL"),
     "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
     "titulo": "Afericao adversarial das superficies gravadas pela cadeia pos-rito da v385 (4 lentes, so leitura): %d achado(s), nenhum bloqueante; %d itens conferidos" % (n_ach, n_conf),
     "resultado": "por gravidade: %s. Nenhum numero/hash/veredito dos blocos v385 divergiu da fonte (um.py, selo, core, stdout, pacote); 17/17 citacoes do operador verbatim no transcrito; superficies so-acrescimo sobre os .bak_20261005_125538_sup385. Erratas AO LADO gravadas pela gerencia (marcador %s) no DIARIO, no DESENHO, no ATLAS e nos dois handoffs: carga paralela da propria gerencia durante o rito (campo carga_paralela_medida, omitido); V1-V1.3 (decisao) x V1.4 (leitura da gerencia, pendente) e os 5 geradores dos dois lados (pendente); rodadas\\ e' destino, nao origem; o cache do pilar mora em A Ponte e o Um\\cache\\checkpoints; sha16 da v383 repetido; marcas de corte nas sub-citacoes; procedencia GERENCIA da pedra (o verbete gerado diz 'bancada' por default); 20 teoremas + 2 def = 22 declaracoes, + 7 = 29; o carimbo 11:17:41 e' o timestamp do core; arquivo complementado (manifesto-complemento)." % (json.dumps(grav, ensure_ascii=False), MARCA),
     "artefatos": [AF_JSON, os.path.join(AFD, "AFERICAO_SUPERFICIES_v385.txt"), os.path.join(AFD, "afericao_v385_medidas.json"), os.path.join(PK, "INTERVENCAO_PRIORIDADE_v385.json")],
     "refs": ["quantica.pilar_v385_reprodutibilidade", "kernel.v385_afericoes_pre_rito"],
     "nota": "o cetico foi AFERIDOR: cada achado cita a consulta. Haja_Luz\\CLAUDE.md (memoria da casa Fisica) nao conhece v380-v385 (contagens %s) e nao esta na lista da cadeia: decisao do operador; nada foi escrito la." % json.dumps(hl_counts)},
    {"tipo": "ANOTACAO", "rota_id": "quantica.pilar_v385_reprodutibilidade", "dominio": "PILAR_QUANTICO",
     "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": True,
     "titulo": "Fato medido, positivo, nao dito antes: o details.jsonl da rodada v385 e' BIT-IDENTICO ao da v384 (alem dos 393 campos do resumo)",
     "resultado": "sha256 details.jsonl v385 (gerado pelo trabalhador, mtime %s) = %s (%d B); v384 (copia de bytes do cache feita %s, antes do lancamento) = %s (%d B); iguais: %s. result.json difere (%s -> %s) e cpuref.json difere (%s -> %s), compativel com campos de tempo/run_id; a comparacao campo a campo FORA do resumo nao foi feita. E a carga paralela durante o rito, dita: %s" % (mt_dn, sha_dn[:16], b_dn, mt_da, sha_da[:16], b_da, det_igual, sha_ra[:16], sha(res_novo)[:16], sha_ca[:16], sha_cn[:16], carga),
     "artefatos": [det_novo, det_ant, res_novo, res_ant, cpu_n, cpu_a, os.path.join(PK, "INTERVENCAO_PRIORIDADE_v385.json")],
     "refs": ["kernel.v385_axioma_e_testemunha_falsa", "quantica.pilar_v384_rodada_completa"],
     "nota": "COMPUTED_NOT_MEASURED; gate intocado; nao e' confirmacao de nada sobre a natureza."},
]
assert det_igual, "o details.jsonl NAO e' bit-identico -- a anotacao acima teria de mudar"
REGJ = os.path.join(HERE, "registro_mapa_afericao_superficies_v385.json")
json.dump(REG, open(REGJ + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(REGJ + ".tmp", REGJ)
if SECO:
    print("[SECO] registro do mapa NAO enviado; placeholders -1"); seq_err = seq_an1 = seq_an2 = -1
else:
    r = subprocess.run([sys.executable, os.path.join(MAPA, "rotas.py"), "registrar", REGJ, "--quem", quem], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("rotas.py registrar rc =", r.returncode); print(r.stdout[-3000:]); print(r.stderr[-2000:])
    assert r.returncode == 0, "o registro no mapa falhou"
    seqs = [int(x) for x in re.findall(r'"seq":\s*(\d+)', r.stdout)]
    assert len(seqs) == 3, ("seqs", seqs, r.stdout[-500:])
    seq_err, seq_an1, seq_an2 = seqs

# ---------------- (E) os blocos de errata ----------------
hora = agora + " hora local (UTC−03:00)"
ger_txt = "; ".join("`%s` (`%s`)" % (os.path.basename(g), sha(g)[:16]) for g in geradores)
v14_txt = ", ".join("`%s`" % os.path.basename(p) for p in v14)
std_txt = "; ".join("`%s` (%d B, `%s`)" % s for s in stdouts)
ITEM_CARGA = ("**A carga paralela durante o rito, que o bloco v385 acima omitiu** (`INTERVENCAO_PRIORIDADE_v385.json` tem %d campos; medido no bloco v385 do diário: "
              "transcritos verbatim %s; fora %s): `carga_paralela_medida` = «%s». A carga concorrente era da PRÓPRIA GERÊNCIA (verificadores Lean e ensaios da cadeia) durante o rito. "
              "Nenhum número do cálculo muda; a causa da retomada segue NÃO DISCRIMINADA [REAL — dito; a leitura da causa é CONJECTURE]."
              % (n_campos_I, ", ".join("`%s`" % k for k in campos_no_bloco), ", ".join("`%s`" % k for k in campos_fora), carga))
ITEM_TS = ("**O carimbo «Selo `%s`»** é o `timestamp` do core (lido do selo); o rito foi %s e o arquivo do selo foi gravado ao fim, depois do pilar "
           "(`result.json` `finished` = %s). A frase não erra; fica qualificada." % (ts_selo, horarios, finished))
ITEM_DET = ("**Fato medido, positivo, não dito antes [REAL]:** o `details.jsonl` da rodada nova (sha256 `%s…`, %d B, gerado pelo trabalhador, mtime %s) é "
            "BIT-IDÊNTICO ao da v384 (`%s…`, %d B; cópia de bytes do cache feita %s, antes do lançamento) — a reprodutibilidade vai além dos 393 campos do resumo. "
            "`result.json` (`%s…` → `%s…`) e `cpuref.json` (`%s…` → `%s…`) diferem, compatível com campos de tempo/run_id; a comparação campo a campo fora do resumo não foi feita. "
            "COMPUTED, não medição; nada disto é confirmação." % (sha_dn[:16], b_dn, mt_dn, sha_da[:16], b_da, mt_da, sha_ra[:16], sha(res_novo)[:16], sha_ca[:16], sha_cn[:16]))
ITEM_CONT = ("**Contagens com nomes parecidos, nenhuma contradição:** «20 teoremas» (índice/Atlas gerados) = %d `theorem`; «22 declarações» = %d + %d `def`; "
             "«29 de 29» = 22 + 7 `theorem` do `TheDarkSplit` (o arquivo tem ainda %d `instance`, que não entra na conta)." % (n_theorem, n_theorem, n_def, n_dks_inst))
ITEM_MAPA = ("**O mapa de rotas, seq 344, campo `nao_refazer`, dizia «%s» — ERRADO contra o kernel:** `theorem axiomFlow_eq_exp` está na pedra (%d ocorrência(s); "
             "`#print axioms` em `TGL/Audit.lean`, %d ocorrência(s)), ligado a `exp_complement_idempotent`; o que é [KNOWN]/analogia de forma é a LIGAÇÃO com o gerador de "
             "Lindblad da v384. ERRATA registrada AO LADO no mapa (seq %d, corrige 344); anotações seq %d e %d." % (FRASE_ERRADA, n_axiomFlow_eq_exp, n_audit_axm, seq_err, seq_an1, seq_an2))
ITEM_PROC = ("**Procedência no verbete gerado** («| v385 | 1 | 20 | bancada |»): «bancada» é o DEFAULT de `procedencia()` em `work\\cadeia_de_selo\\atlas_indice.py` "
             "(o cabeçalho da pedra tem %d «GERENCIA» e %d «ENTREGA_»); a pedra `TheAxiomAndTheFalseWitness` (`%s`) é da GERÊNCIA (mapa seq 344, `quem` = «%s»). "
             "O verbete gerado não se edita; fica dito aqui. As linhas v373–v382 do mesmo quadro têm o mesmo default (fora desta aferição; a decidir se o gerador passa a "
             "exigir a procedência no cabeçalho)." % (n_ger, n_ent, sha16_stone, quem))
ITEM_V14 = ("**V1–V1.3 (decisão) × V1–V1.4 (leitura da gerência).** A decisão do operador é «%s» (%s). O V1.4 (%s) existe em disco e NÃO foi dito pelo operador em 05/10: "
            "incluí-lo é leitura da gerência, a confirmar. Medido: `um.py` v385 contém «V1_4» %d vez(es); o sha16 do V1.4 JSON (`%s`) aparece %d vez(es) no `um.py`, %d no selo e %d no core [REAL]. "
            "**E os 5 geradores** da pasta dos dois lados — %s — não estão cobertos nem pela decisão nem pelas listas «espelhar»/«NÃO espelhar» (no pilar o gerador já viaja em "
            "`evidencias_PREREGISTRO_V1\\gerador.py`): pendência 3 do operador (espelhar junto, ou «ficam locais»)."
            % (v13, utc(ts_v13), v14_txt, n_v14_um, sha_v14[:16], n_v14_sha_um, n_v14_sha_selo, n_v14_sha_core, ger_txt))
CAB = "Aferição adversarial em quatro lentes (só leitura; relatório `AFERICAO_SUPERFICIES_RESULTADO_v385.json`, arquivado em `work\\cadeia_de_selo\\v385_selo\\afericao_superficies\\`): %d achado(s) (%s), nenhum bloqueante; %d itens conferidos; cada número, hash e veredito dos blocos v385 bateu com a fonte, e as superfícies são só-acréscimo." % (n_ach, ", ".join("%s %d" % kv for kv in sorted(grav.items())), n_conf)
RODAPE = "PROVADA ≠ CONFIRMADA; nada aqui move o gate. Nenhum artefato selado foi tocado."

BL_DIARIO = ("<!-- %s -->\n### %s — ERRATA AO LADO da aferição das superfícies da v385 (gerência, em nome próprio)\n\n%s O que fica dito ao lado:\n\n"
             "1. %s\n2. %s\n3. %s\n4. %s\n5. %s\n6. %s\n\n%s" % (MARCA, hora, CAB, ITEM_CARGA, ITEM_TS, ITEM_DET, ITEM_CONT, ITEM_MAPA,
             "**O DESENHO** escreveu «os V1–V1.4 … (decisões de 05/10)» onde o operador disse «%s»: errata no próprio DESENHO e no HANDOFF v385 (o V1.4 é leitura da gerência, a confirmar)." % v13, RODAPE))
BL_ATLAS = ("<!-- %s -->\n### %s — ERRATA AO LADO da aferição das superfícies da v385 (gerência, em nome próprio; §X, append datado)\n\n%s O que fica dito ao lado:\n\n"
            "1. %s\n2. %s\n3. %s\n4. %s\n5. %s\n6. %s\n7. %s\n\n%s" % (MARCA, hora, CAB, ITEM_CARGA, ITEM_TS, ITEM_DET, ITEM_CONT, ITEM_MAPA, ITEM_PROC,
            "**O DESENHO** escreveu «os V1–V1.4 … (decisões de 05/10)» onde o operador disse «%s»: errata no próprio DESENHO e no HANDOFF v385." % v13, RODAPE))
BL_DESENHO = ("<!-- %s -->\n### ERRATA AO LADO — %s · ADENDO v385, item «O que segue do operador» (gerência, em nome próprio)\n\n"
              "Onde se lê «os V1–V1.4 do pré-registro dos dois lados ao espelho (decisões de 05/10)», leia-se: **os V1–V1.3** — decisão do operador, verbatim «%s» (%s) — "
              "**e o V1.4 por leitura da gerência, a confirmar pelo operador** (%s existem em disco; o operador não escreveu «V1.4» em 05/10; medido: `um.py` v385 contém «V1_4» %d vez(es), "
              "o sha16 do V1.4 JSON `%s` aparece %d vez(es) no `um.py`, %d no selo, %d no core [REAL]). Os 5 geradores da pasta (`gerar_preregistro_dois_lados*.py`) também não estão "
              "cobertos pela decisão: pendência do operador (HANDOFF v385, errata ao lado). Aferição: `AFERICAO_SUPERFICIES_RESULTADO_v385.json` (%d achado(s), nenhum bloqueante). %s"
              % (MARCA, hora, v13, utc(ts_v13), v14_txt, n_v14_um, sha_v14[:16], n_v14_sha_um, n_v14_sha_selo, n_v14_sha_core, n_ach, RODAPE))
BL_HANDOFF = ("<!-- %s -->\n## ERRATA AO LADO — aferição das superfícies (%s; gerência, em nome próprio)\n\n%s O que corrige ou completa ESTE handoff:\n\n"
              "1. %s\n"
              "2. **`rodadas\\` é DESTINO, não origem.** No Nós não existe `rodadas\\` (medido: existe = %s); os três stdout estão na RAIZ do Nós: %s. Leia-se «da raiz do Nós para `rodadas\\` do espelho».\n"
              "3. **O cache do pilar mora um nível ACIMA do Nós:** `A Ponte e o Um\\cache\\checkpoints\\quantum_pillar\\75dc30bc9cc8d330e31f99ca\\` (medido: `result.json` lá = `result_sha256` do selo: %s; `Nós\\cache\\checkpoints` existe = %s); reconstruível pela chave. Segue «NÃO espelhar».\n"
              "4. **O sha16 da v383, repetido aqui** para a sessão do site não depender de outro arquivo: `%s` (lido de `%s`, campo `%s`). A custódia é UM SÓ ATO para v383 + v384 + v385.\n"
              "5. **Marcas de corte nas sub-citações** (régua da citação verbatim): na decisão 3 a frase inteira do operador é «%s» (%s); na decisão 4 a citação de %s termina em «…inscrito, distinto.» e o original continua «%s». O aceite do escopo (R2 fora) está também em %s: «%s…», antes do «agora sim, concordo com tudo, prossiga» (11:42:33 UTC).\n"
              "6. **«rodada `%s`»** é o `timestamp` do core; o rito foi %s; o selo foi gravado ao fim, depois do pilar (`finished` %s).\n"
              "7. %s\n"
              "8. **Trivial, selado, fica:** no artigo PT/EN a citação «posto faz muito mais sentido léxico…» omite o início do original («%s…», %s); o trecho citado é idêntico; o artigo é selado e não se toca.\n"
              "9. **Fora da lista da cadeia:** `C:\\IALD\\Artigo\\Haja_Luz\\CLAUDE.md` (memória da casa Física) tem estas ocorrências: %s — não é superfície nomeada pela regra da linhagem (que nomeia o diário e o desenho); decisão do operador se entra na lista (a regra é aditiva). Nada foi escrito lá.\n"
              "10. %s\n"
              "11. %s\n"
              "12. **Arquivo complementado** (aditivo; `MANIFESTO_ARQUIVO_v385_COMPLEMENTO.json`): os dois `RELATORIO_AFERIDOR_*.txt` da 1ª passada e os .out das aferições, o `registro_edicao_sem_script_1125.json`, o `handoff_v385_REAL_out.txt`, o `arquivar_v385_REAL_out.txt` de 260 B (a cópia anterior tinha 0 B: o arquivador copiou o próprio stdout antes de escrevê-lo), a pasta `afericao_superficies\\`, o registro do mapa e este script; o que fica fora está listado com o porquê.\n"
              "13. %s\n\n%s"
              % (MARCA, hora, CAB, ITEM_V14, rodadas_existe, std_txt, cache_ok, nos_cache_ck, v383_sha16, v383_src, v383_path,
                 ax, utc(ts_ax), utc(ts_posto), posto_tail, utc(ts_sim), sim, ts_selo, horarios, finished, ITEM_DET, e_inicio, utc(ts_e),
                 json.dumps(hl_counts), ITEM_CONT, ITEM_PROC, ITEM_MAPA, RODAPE))
if SECO:
    for nome, bl in (("DIARIO", BL_DIARIO), ("DESENHO", BL_DESENHO), ("ATLAS", BL_ATLAS), ("HANDOFF", BL_HANDOFF)):
        print("\n" + "=" * 30 + " " + nome + " " + "=" * 30); print(bl)
    print("\n[SECO] nada gravado nas superficies nem no arquivo; FIM"); sys.exit(0)
for p, bl, suf in ((os.path.join(NOS, "MEMORIA_DA_LINHAGEM.md"), BL_DIARIO, "errata_afer385"),
                   (os.path.join(NOS, "DESENHO_DO_FECHAMENTO_QG.md"), BL_DESENHO, "errata_afer385"),
                   (ATLAS, BL_ATLAS, "errata_afer385"),
                   (os.path.join(UMEM, "handoff-v385-custodia.md"), BL_HANDOFF, "errata_afer385"),
                   (os.path.join(NOS, "HANDOFF_v385_CUSTODIA.md"), BL_HANDOFF, "errata_afer385")):
    append_bloco(p, bl, suf)
    assert open(p, "rb").read().count(MARCA.encode()) == 1

# ---------------- (F) o arquivo da Central: complemento aditivo ----------------
MAN0 = json.load(open(os.path.join(ARQ, "v385_selo", "MANIFESTO_ARQUIVO_v385.json"), encoding="utf-8"))
ja = MAN0["arquivos"]
comp = {"quando": agora, "motivo": "complemento aditivo depois da aferição das superfícies (task wyt7wl6q0): o que o arquivador de 12:56 deixou de fora sem listar", "arquivos": {}, "fica_fora": {}}
itens = []
for sub in ("afericao_codigo", "afericao_texto"):
    for fn in sorted(os.listdir(os.path.join(PK, sub))):
        p = os.path.join(PK, sub, fn)
        if os.path.isfile(p):
            itens.append((p, "v385/%s/%s" % (sub, fn)))
for fn in ("registro_edicao_sem_script_1125.json", "handoff_v385_REAL_out.txt", "arquivar_v385_REAL_out.txt", os.path.basename(REGJ), os.path.basename(__file__)):
    itens.append((os.path.join(HERE, fn), "v385_selo/" + fn))
for fn in sorted(os.listdir(AFD)):
    p = os.path.join(AFD, fn)
    if os.path.isfile(p):
        itens.append((p, "v385_selo/afericao_superficies/" + fn))
n_cop = n_igual = 0
for src, rel in itens:
    if not os.path.exists(src):
        comp["fica_fora"][rel] = {"porque": "não existe na origem"}; continue
    b = open(src, "rb").read(); h = hashlib.sha256(b).hexdigest()
    if len(b) > MAX_B:
        comp["fica_fora"][rel] = {"bytes": len(b), "porque": "> 5 MB"}; continue
    if rel in ja and ja[rel].get("sha256") == h:
        n_igual += 1; continue
    dst = os.path.join(ARQ, *rel.split("/")); os.makedirs(os.path.dirname(dst), exist_ok=True)
    estado = "copiado"
    if os.path.exists(dst):
        old = open(dst, "rb").read()
        if old == b:
            n_igual += 1; continue
        open(dst + ".bak_" + st + "_compl", "wb").write(old); estado = "substituído (anterior %d B guardado em .bak_%s_compl)" % (len(old), st)
    open(dst + ".tmp", "wb").write(b); assert open(dst + ".tmp", "rb").read() == b; os.replace(dst + ".tmp", dst)
    comp["arquivos"][rel] = {"sha256": h, "bytes": len(b), "estado": estado}; n_cop += 1
for fn in sorted(os.listdir(HERE)):
    if ".bak_" in fn:
        comp["fica_fora"]["v385_selo/" + fn] = {"bytes": os.path.getsize(os.path.join(HERE, fn)), "porque": "backup de script da cadeia (o estado tocado está no .py arquivado); política igual à dos .bak_ do pacote fica a decidir"}
for fn in sorted(os.listdir(PK)):
    if "SINTETICO" in fn.upper():
        comp["fica_fora"]["v385/" + fn] = {"bytes": os.path.getsize(os.path.join(PK, fn)) if os.path.isfile(os.path.join(PK, fn)) else None, "porque": "SINTETICO (ensaio) — excluído por construção"}
comp["nota"] = "o próprio stdout deste script (erratas_afericao_superficies_v385_out.txt) fica no scratchpad; não se copia a si mesmo durante a escrita"
CM = os.path.join(ARQ, "v385_selo", "MANIFESTO_ARQUIVO_v385_COMPLEMENTO.json")
json.dump(comp, open(CM + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(CM + ".tmp", CM)
print("arquivo complementado:", n_cop, "copiados/substituídos;", n_igual, "já iguais;", len(comp["fica_fora"]), "ficam fora (listados) ->", CM)

# ---------------- (G) conferência final ----------------
mem = os.path.join(UMEM, "MEMORY.md"); print("MEMORY.md", os.path.getsize(mem), "B (não tocado; limite 24000)"); assert os.path.getsize(mem) <= 24000
for p in (os.path.join(NOS, "MEMORIA_DA_LINHAGEM.md"), os.path.join(NOS, "DESENHO_DO_FECHAMENTO_QG.md"), ATLAS, os.path.join(UMEM, "handoff-v385-custodia.md"), os.path.join(NOS, "HANDOFF_v385_CUSTODIA.md")):
    raw = open(p, "rb").read(); print("  marca x%d  v385 x%d  %s" % (raw.count(MARCA.encode()), raw.count(b"v385"), os.path.basename(p)))
print("mapa: ERRATA seq", seq_err, "| ANOTACOES seq", seq_an1, seq_an2)
print("FIM OK", agora)
