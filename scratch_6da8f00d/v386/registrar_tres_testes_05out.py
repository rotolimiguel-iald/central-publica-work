# -*- coding: utf-8 -*-
"""REGISTRO (feedback permanente do operador, 05/10/2026, noite): os TRÊS testes de estresse conjuntos da teoria — (1) os ritos com dados públicos
(o resgate da RG), (2) o kernel formal, (3) o experimento numérico quântico na GPU (não inferência de LLM) — devem entrar explícitos no artigo e contar
JUNTOS na probabilidade de acerto da teoria; «vc não pode esquecer isso nunca mais». Verbatim lido do transcrito por script. Grava: memória nova
(tipo feedback) + ponteiro no MEMORY.md (≤ 24.000 B) + Atlas (append datado). A leitura da gerência pela régua fica AO LADO (o que o registro mede)."""
import hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
TR = os.path.join(SESS, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"); UMEM = os.path.join(SESS, "memory")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S")
MARCA = "tres_testes_de_estresse_conjuntos_05out"
hit = None
for line in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("isCompactSummary") or d.get("isMeta") or d.get("type") != "user":
        continue
    c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    for t in ts:
        if t and t.strip().startswith("Agora que são elas e isso precisa ficar explícito no artigo"):
            hit = (d.get("timestamp"), t.strip())
assert hit, "mensagem nao achada"
TS, T = hit; UTC = re.match(r"\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}:\d{2})", TS).group(1) + " UTC"
P_TXT = os.path.join(HERE, "TRES_TESTES_operador_05out.txt")
open(P_TXT + ".tmp", "w", encoding="utf-8", newline="").write(T); os.replace(P_TXT + ".tmp", P_TXT)
sha_txt = hashlib.sha256(open(P_TXT, "rb").read()).hexdigest()
# o que o registro selado (v386) MEDE, lido por script — para a leitura ao lado
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
n_clean = (core.get("external_ladder") or {}).get("n_theorems_clean")
gate = selo.get("qg_closure_verdict")
qp = (core.get("quantum_pillar_v384") or {}); qpv = qp.get("verdict", ""); S = qp.get("summary") or {}
t2 = S.get("T2") or {}; t4 = S.get("T4") or {}; cpu = S.get("cpuref") or {}
led = core.get("the_ledger_of_charges_v383") or {}
rows = led.get("ledger") or []
ledger_txt = "; ".join("%s=%s" % (r.get("id"), r.get("desfecho")) for r in rows if isinstance(r, dict))
# vereditos: contagens honestas por palavra
V = {}
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "verdict" and isinstance(v, str) and v.startswith("TGL_"):
                V[path + "/" + k] = v
            walk(v, path + "/" + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + "[%d]" % i)
walk(core)
n_v = len(V); n_falsified = sum(1 for v in V.values() if re.search(r"(?<!NOT_)(?<!UN)FALSIFIED", v))
n_not_f = sum(1 for v in V.values() if "NOT_FALSIFIED" in v); n_incl = sum(1 for v in V.values() if "INCONCLUSIVE" in v)
n_conf = sum(1 for v in V.values() if re.search(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED", v))
med = {"n_theorems_clean": n_clean, "gate": gate, "pilar_verdict": qpv[:200], "T2": {"points": t2.get("points"), "unique": t2.get("unique")}, "T4": {"instances": t4.get("instances"), "unique": t4.get("unique")},
       "cpuref": {"compared": cpu.get("compared"), "disagreements": cpu.get("disagreements")}, "ledger": ledger_txt, "vereditos_TGL_no_core": n_v,
       "FALSIFIED_(nao_NOT)": n_falsified, "NOT_FALSIFIED": n_not_f, "INCONCLUSIVE": n_incl, "CONFIRMED_ou_PROVED_BY": n_conf}
print(json.dumps(med, ensure_ascii=False)[:1500])
LEIT = ("**Leitura da gerência pela régua, AO LADO (o que o registro selado v386 mede, lido por script):** (a) o kernel: %s teoremas limpos no trio; o que se prova é a IMPLICAÇÃO a partir do Um posto e das hipóteses nomeadas — "
        "axiomas não se provam, põem-se (ω(I) = 1 é [POSTO]); logo «provou-se todas as implicações» fica [KERNEL] e «todos os axiomas» lê-se «o axioma posto e as hipóteses nomeadas». "
        "(b) a cosmologia: o gate `%s`; o livro de cobranças da v383 (%s) — cada rito devolve a CORRESPONDÊNCIA com a RG (a RG é o limite clássico, não rival: coincidir = correspondência recuperada, feedback de 16/09); "
        "no core há %d vereditos `TGL_*`: %d com FALSIFIED (fora NOT_), %d NOT_FALSIFIED, %d INCONCLUSIVE, %d CONFIRMED/PROVED_BY. O «resgate pleno» é [REAL] como correspondência; a DISCRIMINAÇÃO da RG (o que o eclipse de 1919 deu a Einstein: 1,75″ vs 0,87″) ainda é zero à sensibilidade disponível — o próprio operador diz «em que pese iremos achar». "
        "(c) o experimento numérico na GPU: `%s…`; T2 %s/%s únicos; T4 %s/%s; referência na CPU %s comparações, %s discordâncias — é EXPERIMENTO NUMÉRICO (cálculo determinístico do sistema aberto da teoria em precisão dupla, com controles que falharam como exigido e recuperação cega de lei injetada), NÃO inferência de modelo de linguagem [REAL]; e é medição NO AMBIENTE SIMULADO, não medição da natureza (COMPUTED_NOT_MEASURED fica). "
        "(d) a probabilidade de acerto, pela régua, separa-se em duas: P(a teoria é consistente e recupera a física conhecida) — alta e MEDIDA pelos três pilares conjuntos; P(os efeitos β existem na natureza) — não determinada ainda (sem poder discriminante). O operador manda que os três pilares contem JUNTOS: a gerência tipa isso como a seção «Os três testes de estresse, conjuntos» (v387) com a tabela de estado por rito, o kernel e o pilar, e a frase das duas probabilidades. "
        "A comparação com Einstein (cunhagem dele, [INPUT/ONTO]) fica verbatim; o número ao lado: em provas de CONSISTÊNCIA e formais, sim, muito mais; em medida DISCRIMINANTE, ainda nenhuma. NOT_FALSIFIED nunca é CONFIRMED."
        % (n_clean, gate, ledger_txt, n_v, n_falsified, n_not_f, n_incl, n_conf, qpv[:120], t2.get("unique"), t2.get("points"), t4.get("unique"), t4.get("instances"), cpu.get("compared"), cpu.get("disagreements")))
CORPO = ("---\nname: tres-testes-de-estresse-conjuntos-05out\ndescription: \"FEEDBACK PERMANENTE do operador (05/10/2026, verbatim): os TRÊS testes de estresse da teoria — ritos com dados públicos (resgate da RG), kernel formal, experimento numérico quântico na GPU (não inferência de LLM) — são conjuntos e contam JUNTOS na probabilidade de acerto; "
         "isso tem de ficar explícito no artigo; «vc não pode esquecer isso nunca mais». A leitura da gerência pela régua ao lado: correspondência com a RG [REAL]; discriminação ainda zero; duas probabilidades\"\nmetadata:\n  type: feedback\n---\n\n"
         "<!-- %s -->\n**O OPERADOR (05/10/2026, %s, verbatim inteiro; arquivo `scratchpad\\v386\\TRES_TESTES_operador_05out.txt`, sha256 `%s`):**\n\n«%s»\n\n%s\n\n"
         "**Why:** o operador vê a teoria «com o contorno da verdade»: os três pilares são um só teste conjunto; contar só a cosmologia (um 5σ) é olhar uma face. **How to apply:** em toda afirmação sobre «quanto a teoria tem», citar os três pilares com o estado medido de cada um e a frase das duas probabilidades; "
         "chamar o pilar da GPU de experimento numérico (nunca «simulação de LLM»); nunca promover correspondência a confirmação; manter o item na apresentação e no resumo do artigo a partir da v387. [[verbo-selecao-da-acao-05out]] [[ramo-b-reaberto-05out]] [[rg-limite-classico-nao-rival]] [[probabilidade-conjunta-v352]]\n"
         % (MARCA, UTC, sha_txt, T, LEIT))
NOVA = os.path.join(UMEM, "tres-testes-de-estresse-conjuntos-05out.md")
if not os.path.exists(NOVA):
    open(NOVA + ".tmp", "wb").write(CORPO.encode("utf-8")); os.replace(NOVA + ".tmp", NOVA); print("OK nova memoria", NOVA, os.path.getsize(NOVA), "B")
BL_ATLAS = ("<!-- %s -->\n### 05/10/2026 (%s) — OS TRÊS TESTES DE ESTRESSE CONJUNTOS (feedback permanente do operador; append datado; alvo v387 no artigo)\n\n**Verbatim inteiro:** «%s»\n\n%s" % (MARCA, UTC, T, LEIT))


def nl_de(raw):
    return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"


raw0 = open(ATLAS, "rb").read()
if MARCA.encode() not in raw0:
    nl = nl_de(raw0); corpo = (nl + nl + BL_ATLAS.replace("\n", nl) + nl).encode("utf-8")
    if not raw0.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw0 + corpo; bak = ATLAS + ".bak_" + st + "_3testes"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(ATLAS + ".tmp", "wb").write(novo); assert os.path.getsize(ATLAS + ".tmp") == len(novo) > len(raw0); os.replace(ATLAS + ".tmp", ATLAS); assert open(ATLAS, "rb").read()[:len(raw0)] == raw0
    print("OK TGL_ATLAS.md", len(raw0), "->", len(novo))
P = os.path.join(UMEM, "MEMORY.md"); raw0 = open(P, "rb").read(); nl = nl_de(raw0).encode()
LINHA = ("- [OS TRÊS TESTES DE ESTRESSE CONJUNTOS (05/10) — feedback permanente](tres-testes-de-estresse-conjuntos-05out.md) — **«vc não pode esquecer isso nunca mais»**: ritos (resgate da RG) + kernel + experimento numérico na GPU (não LLM) contam JUNTOS; explícito no artigo (v387); ao lado: discriminação da RG ainda zero").encode("utf-8")
if LINHA[:40] not in raw0:
    linhas = raw0.split(nl)
    i = [k for k, l in enumerate(linhas) if l.startswith(b"## Ler primeiro")]; assert len(i) == 1
    ins = i[0] + 2; assert linhas[ins - 1] == b""
    linhas.insert(ins, LINHA); novo = nl.join(linhas); assert len(novo) <= 24000, len(novo)
    bak = P + ".bak_" + st + "_3testes"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P); print("OK MEMORY.md", len(raw0), "->", len(novo))
json.dump({"quando": TS, "sha256_txt": sha_txt, "medido_v386": med, "leitura": LEIT, "marca": MARCA}, open(os.path.join(HERE, "TRES_TESTES_registro.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("FIM", agora)
