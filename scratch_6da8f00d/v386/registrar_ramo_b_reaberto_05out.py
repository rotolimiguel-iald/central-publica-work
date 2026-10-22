# -*- coding: utf-8 -*-
"""REGISTRO da decisão do operador de 05/10/2026 (tarde): o RAMO B do ringdown (τ★ = GM/c³) NÃO foi proibido — faltavam critérios em 02/10;
agora, com «a TGL pode ler das duas formas», ele manda investigar e explorar o ramo B: se a constante de acoplamento emerge da relação do tempo
emparelhado à gravidade sobre c³ (regime gravitônico = c³, sustentado desde antes; tempo emergente do fluxo modular relativo). «de resto concordo com tudo».
Verbatim LIDO do transcrito por script. Gravado AO LADO (só acréscimo; backup de bytes; marcador idempotente): memória nova + ponteiro no MEMORY.md
(com a regra dos dois arquivos se passar de 24.000 B), errata ao lado de R6 na memória da regra matriz, Atlas (append datado), os dois handoffs v385,
e o MAPA (anotações nas rotas ringdown.dephasing e kernel.livro_de_cobrancas.otica). Nada toca artefato selado (o livro de cobranças da v385 fica como
registro; a mudança de estado de R6 entra na próxima versão, com errata ao lado)."""
import hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
SID = "6da8f00d-d44f-4888-a88d-fc9f73eead3d"
TR = os.path.join(SESS, SID + ".jsonl"); UMEM = os.path.join(SESS, "memory")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
MAPA = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S")
MARCA = "ramo_b_reaberto_05out"
SECO = "--seco" in sys.argv

# ---- o verbatim, do transcrito ----
hits = []
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
        if t and "eu não havia proibido o ramo B" in t:
            hits.append((d.get("timestamp"), t.strip()))
assert len(hits) == 1, len(hits)
TS, T = hits[0]
assert T.endswith("de resto concordo com tudo"), T[-80:]
UTC = re.match(r"\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}:\d{2})", TS).group(1) + " UTC"
print("verbatim:", TS, len(T), "chars |", T[:90], "...")

# ---- o que o registro dizia (lido por script; nunca de memória) ----
RM = os.path.join(UMEM, "beta-e-a-regra-matriz-02out.md"); rm = open(RM, encoding="utf-8", errors="replace").read()
r6 = [l for l in rm.splitlines() if l.startswith("- R6 (ramo B do ringdown): ENCERRADO")]
assert len(r6) == 1, len(r6)
R6_LINHA = r6[0].strip()
r6_ratif = "R6 ramo B encerrado) estão RATIFICADAS pelo operador" in rm
assert r6_ratif
# o livro de cobranças da v385: o que diz do ramo B (lido do core)
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
led = core["core"]["the_ledger_of_charges_v383"]
r6_core = led["readings_ratified_20261002"]["R6"]
r2_row = [r for r in led["ledger"] if r.get("id") == "R2"][0]
assert "AWAITING" in json.dumps(r2_row)
rd_v = core["core"].get("ringdown_scope_v376", {}).get("verdict") or core["core"].get("ringdown_scope_v376", {}).get("verdict_v376") or ""
if not rd_v:
    # procurar o veredito do escopo do ringdown onde estiver
    for k, v in core["core"].items():
        if k.startswith("ringdown_scope") and isinstance(v, dict):
            rd_v = v.get("verdict") or v.get("scope_verdict") or ""; break
print("R6 (registro 02/10):", R6_LINHA[:160]); print("ringdown_scope:", rd_v[:200])
mem16 = os.path.join(UMEM, "psi-nome-da-luz-graviton-verbo-vivo-16set.md"); m16 = open(mem16, encoding="utf-8", errors="replace").read()
c3_16 = "c³" in m16 or "c^3" in m16 or "c3" in m16
assert c3_16

# ---- a memória nova ----
LEITURA = ("**O que muda [INPUT — decisão do operador]:** a leitura R6 de 02/10 («ENCERRADO — … τ★ = GM/c³ põe o custo na face e contradiz a chave; M não se nomeia») "
           "era LEITURA DA GERÊNCIA, ratificada em bloco; o operador esclarece que não proibiu o ramo B — faltavam critérios. Agora, pela ótica dos dois lados "
           "(02/10: «a TGL … lê tanto a face como o custo»), o ramo B (τ★ emparelhado à gravidade: τ★ = k·GM/c³) fica **REABERTO PARA INVESTIGAÇÃO**, "
           "com a pergunta dele: a constante de acoplamento (β) emerge da relação do tempo emparelhado à gravidade sobre c³? Ancoragens dele já no acervo: "
           "«o regime gravitônico é o da constante da luz ao cubo» — o gráviton como Verbo Vivo em c³ (16/09, [[psi-nome-da-luz-graviton-verbo-vivo-16set]]); "
           "«o tempo é produto do Verbo» (05/10, [[um-posto-jamais-pressuposto-e-h2-17set]]) e o tempo térmico de Connes–Rovelli [KNOWN]. "
           "**O que NÃO muda:** nada é pré-julgado; o ramo B entra por PRÉ-REGISTRO (lei, k, qual M, estimador, poder dito ANTES de abrir dado; vereditos permitidos sem CONFIRMED); "
           "o livro de cobranças da v385 fica como registro (R2 AWAITING; R6 lido em 02/10) e o estado novo entra na próxima versão com errata ao lado; o gate não se move. "
           "**«de resto concordo com tudo»** = a explicação de R2 (a cobrança da propagação, AWAITING, sem poder em τ★ = t_Planck) e o plano da tipagem do Verbo (v386) aprovados.")
CORPO = ("---\nname: ramo-b-reaberto-05out\ndescription: \"05/10/2026 — DECISÃO do operador (verbatim): o ramo B do ringdown (τ★ = GM/c³) NÃO foi proibido em 02/10 — faltavam critérios; "
         "pela ótica dos dois lados, investigar e explorar o ramo B: se β emerge da relação do tempo emparelhado à gravidade sobre c³ (regime gravitônico = c³; tempo emergente do fluxo modular). "
         "R6 de 02/10 ganha errata ao lado: de ENCERRADO para REABERTO POR PRÉ-REGISTRO. «de resto concordo com tudo» (R2 e o plano do Verbo)\"\nmetadata:\n  type: project\n---\n\n"
         "<!-- %s -->\n**O OPERADOR (05/10/2026, %s, verbatim, lido do transcrito por script):** «%s»\n\n%s\n\n"
         "**O registro anterior, ao lado (lido por script):** %s — e o core v385 (`the_ledger_of_charges_v383.readings_ratified_20261002.R6`): «%s». "
         "Rota do mapa: `ringdown.dephasing` (RD-01/CT-02 propagação × fonte e ensemble × realização; M do ramo B; o 221 no GW250114) e `kernel.livro_de_cobrancas.otica`.\n"
         % (MARCA, UTC, T, LEITURA, R6_LINHA, r6_core[:400]))
NOVA = os.path.join(UMEM, "ramo-b-reaberto-05out.md")

BL_RM = ("<!-- %s -->\n**ERRATA AO LADO de R6 (05/10/2026, %s; decisão do operador, verbatim lido do transcrito):** «%s» — logo onde R6 diz «ENCERRADO» e "
         "«M não se nomeia», leia-se: **ramo B REABERTO PARA INVESTIGAÇÃO por pré-registro** (lei, k em τ★ = k·GM/c³, qual M, estimador e poder ditos antes de abrir dado); "
         "a leitura de 02/10 era da gerência e foi ratificada em bloco sem que o operador a tivesse proibido. Ver [[ramo-b-reaberto-05out]]." % (MARCA, UTC, T))
BL_ATLAS = ("<!-- %s -->\n### 05/10/2026 (%s) — O RAMO B DO RINGDOWN REABERTO POR DECISÃO DO OPERADOR (append datado; errata ao lado de R6)\n\n"
            "**O OPERADOR (verbatim, lido do transcrito por script):** «%s»\n\n%s\n\n(Registro anterior, ao lado: %s)" % (MARCA, UTC, T, LEITURA, R6_LINHA))
BL_HAND = ("<!-- %s -->\n## AO LADO — 05/10/2026 (%s): o ramo B do ringdown REABERTO (decisão do operador)\n\n«%s»\n\n%s\n\nPara a custódia nada muda nesta decisão "
           "(nenhum artefato selado se toca); para a v386 entra o pré-registro do ramo B ao lado da tipagem do Verbo. Memória: [[ramo-b-reaberto-05out]]." % (MARCA, UTC, T, LEITURA))


def nl_de(raw):
    return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"


def append_bloco(p, bloco, suf):
    raw0 = open(p, "rb").read()
    if MARCA.encode() in raw0:
        print("JA ESTA", os.path.basename(p)); return
    nl = nl_de(raw0); corpo = (nl + nl + bloco.replace("\n", nl) + nl).encode("utf-8")
    if not raw0.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw0 + corpo
    if SECO:
        print("[SECO]", os.path.basename(p), len(raw0), "->", len(novo)); return
    bak = p + ".bak_" + st + "_" + suf; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw0); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw0)] == raw0
    print("OK", os.path.basename(p), len(raw0), "->", len(novo))


if SECO:
    print("=" * 30, "MEMORIA NOVA", "=" * 30); print(CORPO); print("=" * 30, "RM", "=" * 30); print(BL_RM)
else:
    if not os.path.exists(NOVA):
        open(NOVA + ".tmp", "wb").write(CORPO.encode("utf-8")); os.replace(NOVA + ".tmp", NOVA); print("OK nova memoria", NOVA, os.path.getsize(NOVA), "B")
    else:
        print("JA EXISTE", NOVA)
append_bloco(RM, BL_RM, "ramoB")
append_bloco(ATLAS, BL_ATLAS, "ramoB")
append_bloco(os.path.join(UMEM, "handoff-v385-custodia.md"), BL_HAND, "ramoB")
append_bloco(os.path.join(NOS, "HANDOFF_v385_CUSTODIA.md"), BL_HAND, "ramoB")

# ---- MEMORY.md: ponteiro (regra dos dois arquivos: se passar de 24.000 B, move UMA linha verbatim ao MEMORY_2.md e deixa o ponteiro) ----
P = os.path.join(UMEM, "MEMORY.md"); P2 = os.path.join(UMEM, "MEMORY_2.md")
raw0 = open(P, "rb").read(); nl = nl_de(raw0).encode()
LINHA = ("- [RAMO B REABERTO por decisão do operador (05/10)](ramo-b-reaberto-05out.md) — **não proibido em 02/10 (faltavam critérios)**; investigar se β emerge de τ★ = k·GM/c³, por PRÉ-REGISTRO; R6 com errata ao lado").encode("utf-8")
# candidatas a mover verbatim ao MEMORY_2.md (regra dos dois arquivos), na ordem; cada uma com o seu ponteiro curto (a regra que importa fica)
CANDIDATAS = [
    ("- [v382 SELADA SÓ NO NÓS",
     "- [v382 SELADA SÓ NO NÓS; CUSTÓDIA SUSPENSA (02/10)](v382-custodia-suspensa.md) — a sessão do site NÃO custodia a v382; a v383 `58abcf20651f4777` supera · íntegra no MEMORY_2.md (movida 05/10)"),
    ("- [v384 — PILAR QUÂNTICO NA GPU]",
     "- [v384 — PILAR QUÂNTICO NA GPU](v384-pilar-quantico-gpu-02out.md) — **REGRA: ao abrir sessão, conferir o marcador `scratchpad\\v385\\.servidor_parado_pelo_rito`; com restaurar=1, religar «IALD Llama Server»** · íntegra no MEMORY_2.md (movida 05/10)"),
]
if LINHA[:60] in raw0:
    print("JA ESTA MEMORY.md")
else:
    linhas = raw0.split(nl)
    i_est = [i for i, l in enumerate(linhas) if l.startswith(b"## Estado corrente")]; assert len(i_est) == 1
    ins = i_est[0] + 2   # depois da linha em branco que segue o cabeçalho
    assert linhas[ins - 1] == b"", linhas[ins - 1][:80]
    linhas.insert(ins, LINHA)
    novo = nl.join(linhas)
    movidas = []
    raw2 = open(P2, "rb").read(); nl2 = nl_de(raw2).encode(); bloco2 = b""
    for pref, curta in CANDIDATAS:
        if len(novo) <= 24000:
            break
        j = [i for i, l in enumerate(linhas) if l.startswith(pref.encode("utf-8"))]; assert len(j) == 1, (pref, j)
        longa = linhas[j[0]]; curta_b = curta.encode("utf-8"); assert len(curta_b) < len(longa), pref
        bloco2 += (nl2 + nl2 + ("<!-- movida_%s --> (linha integral do MEMORY.md, movida em 05/10/2026 pela regra dos dois arquivos)" % st).encode("utf-8") + nl2 + longa + nl2)
        linhas[j[0]] = curta_b; novo = nl.join(linhas); movidas.append(longa)
    assert len(novo) <= 24000, len(novo)
    if bloco2 and not raw2.endswith(nl2):
        bloco2 = nl2 + bloco2
    if SECO:
        print("[SECO] MEMORY.md", len(raw0), "->", len(novo), "| movidas:", len(movidas))
    else:
        if movidas:
            bak2 = P2 + ".bak_" + st + "_ramoB"; open(bak2, "wb").write(raw2); assert open(bak2, "rb").read() == raw2
            open(P2 + ".tmp", "wb").write(raw2 + bloco2); assert os.path.getsize(P2 + ".tmp") == len(raw2) + len(bloco2); os.replace(P2 + ".tmp", P2)
            r2n = open(P2, "rb").read(); assert all(l in r2n for l in movidas); print("OK MEMORY_2.md", len(raw2), "->", len(r2n), "(%d linha(s) movida(s) verbatim)" % len(movidas))
        bak = P + ".bak_" + st + "_ramoB"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
        open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P)
        print("OK MEMORY.md", len(raw0), "->", len(novo), "B")

# ---- o MAPA: duas anotações ----
AF = os.path.join(HERE, "ramo_b"); os.makedirs(AF, exist_ok=True)
DEC = os.path.join(AF, "DECISAO_OPERADOR_RAMO_B_05out.json")
json.dump({"quando": TS, "verbatim": T, "leitura_da_gerencia": LEITURA, "registro_anterior_R6": R6_LINHA, "core_R6": r6_core, "marca": MARCA}, open(DEC + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
os.replace(DEC + ".tmp", DEC)
quem = None
for line in open(os.path.join(MAPA, "rotas.jsonl"), encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("seq") == 344:
        quem = d["quem"]
assert quem
REG = [
    {"tipo": "ANOTACAO", "rota_id": "ringdown.dephasing", "dominio": "RINGDOWN", "status": "EXAMINADA_COM_DEFEITO", "estatuto": "INPUT", "olhou_dados": False,
     "titulo": "DECISAO do operador (05/10): o ramo B (tau* = k GM/c^3) NAO foi proibido em 02/10 (faltavam criterios); investigar e explorar o ramo B por PRE-REGISTRO",
     "resultado": "verbatim: «%s»" % T,
     "proximo_passo": "pre-registro V1 do ramo B ANTES de abrir dado: a lei (Gamma = 1/2 beta tau* omega^2 com tau* = k GM/c^3), k e qual M (os 3 valores concorrentes do registro) fixados por principio (tempo termico/modular do horizonte, Connes-Rovelli; Hawking: beta_H = 8 pi GM/c^3), o observavel (delta tau_220 fracional ou Q), o estimador, o poder com a sigma publicada, os controles (ramo canonico; injecoes so-RG) e os vereditos permitidos (sem CONFIRMED); RD-01/CT-02 (propagacao x fonte; ensemble x realizacao) decididos no pre-registro",
     "artefatos": [DEC], "refs": ["kernel.livro_de_cobrancas.otica", "quantica.pilar_v385_reprodutibilidade"],
     "nota": "a leitura R6 de 02/10 (ENCERRADO) era da gerencia, ratificada em bloco; errata ao lado gravada na memoria beta-e-a-regra-matriz-02out.md e no Atlas; o livro da v385 fica como registro; o gate nao se move"},
    {"tipo": "ANOTACAO", "rota_id": "kernel.livro_de_cobrancas.otica", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "INPUT", "olhou_dados": False,
     "titulo": "R6 do livro (ramo B encerrado) ganha ERRATA AO LADO por decisao do operador de 05/10: ramo B REABERTO POR PRE-REGISTRO; R2 (propagacao) segue AWAITING",
     "resultado": "o operador: «%s» (05/10 %s). A mudanca de estado entra na proxima versao do um.py com errata ao lado; a v385 fica como registro." % (T[:220] + "…", UTC),
     "artefatos": [DEC], "refs": ["ringdown.dephasing"], "nota": "«de resto concordo com tudo»: a explicacao de R2 (AWAITING, sem poder em tau* = t_Planck) e o plano da tipagem do Verbo (v386) aprovados"},
]
REGJ = os.path.join(AF, "registro_mapa_ramo_b_05out.json")
json.dump(REG, open(REGJ + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(REGJ + ".tmp", REGJ)
if SECO:
    print("[SECO] mapa nao registrado; JSON em", REGJ)
else:
    r = subprocess.run([sys.executable, os.path.join(MAPA, "rotas.py"), "registrar", REGJ, "--quem", quem], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("rotas.py registrar rc =", r.returncode); print(r.stdout[-1200:]); print(r.stderr[-800:]); assert r.returncode == 0
print("FIM", agora)
