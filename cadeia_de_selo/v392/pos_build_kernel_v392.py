# -*- coding: utf-8 -*-
"""pos_build_kernel_v392.py -- DEPOIS de construir_kernel_v392.sh: (1) monta kernel/build_full.log no formato do molde (v390: inicio / lake build / rc_build / audit / rc_audit / rc / fim)
a partir dos logs crus; (2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully', linha Built/Replayed de cada pedra, da raiz e
do Audit, axiomas no trio); (3) copia a ARVORE so-fontes (sem .lake) para C:\\t\\k392\\arvore e varre os tokens proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v391
(extraida por ast, sem importar o um.py); (4) mede os 7 criterios; (5) escreve KERNEL_RECIBO_v392.json (contrato KERNEL_RECIBO_R3_2) e CRITERIOS_v392.json (preenchido com a MEDICAO,
x19='sim'; [DERIVED: a gerencia confere antes de pinar]). Nada e' escrito fora desta pasta e de C:\\t\\k392. Uso: python -I -B -X utf8 pos_build_kernel_v392.py"""
import ast, hashlib, json, os, re, shutil, subprocess, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v392_pedras as P  # noqa: E402
KD = os.path.join(HERE, "kernel"); KB = os.path.join("C:" + os.sep, "t", "k392", "final"); ARV = os.path.join("C:" + os.sep, "t", "k392", "arvore")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); NK = os.path.join(NOS, "tgl_kernel")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
abs_fw = lambda p: p.replace("\\", "/")
sinais = []


def chk(nome, cond, det=None):
    sinais.append({"checagem": nome, "ok": bool(cond), "detalhe": det}); print(("OK   " if cond else "FALHA"), nome, "" if det is None else "-> " + str(det)[:200])
    return bool(cond)


def norm(t):
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", t)
    return "".join(ch for ch in unicodedata.normalize("NFKC", t) if unicodedata.category(ch) != "Cf")


RE_SORRY = re.compile(r"declaration\s+uses\s*[`'\u2018\u201c\"]sorry|\bsorryAx\b", re.I)
RE_DEP = re.compile(r"'([\w.'\u00ab\u00bb\u2080-\u209f]+)' depends on axioms: \[([^\]]*)\]", re.S)
RE_NONE = re.compile(r"'([\w.'«»₀-₟]+)' does not depend on any axioms")
LB = norm(rd(os.path.join(KD, "lake_build.log")).decode("utf-8")); AL = norm(rd(os.path.join(KD, "audit.log")).decode("utf-8"))
marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read()
rb = int(re.search(r"rc_build=(\d+)", marcas).group(1)); ra = int(re.search(r"rc_audit=(\d+)", marcas).group(1))
ini = re.search(r"^inicio (.*)$", marcas, re.M).group(1); fim = re.search(r"^fim (.*)$", marcas, re.M).group(1)
chk("rc do lake build == 0 e rc do Audit == 0", rb == 0 and ra == 0, [rb, ra])
n_err = len(re.findall(r"(?m)^error:|: error:", LB + "\n" + AL)); n_sorry = len(RE_SORRY.findall(LB + "\n" + AL)) + len(RE_SORRY.findall(re.sub(r"\s+", " ", LB + "\n" + AL)))
chk("zero erro; zero sorry/sorryAx (formas: crase, aspas, sorryAx; com e sem quebra)", n_err == 0 and n_sorry == 0, [n_err, n_sorry])
RE_JOB = re.compile(r"(?m)^[^\[\n]*\[\d+/\d+\][ \t]+(?:Built|Replayed)[ \t]+([^\s(]+)")
jobs = set(RE_JOB.findall(LB)); exig = ["TGLExt", "TGL.Audit"] + ["TGLExt." + s["mod"] for s in P.STONES]
chk("linha Built/Replayed de cada pedra, da raiz (TGLExt) e do Audit (TGL.Audit)", all(m in jobs for m in exig), [m for m in exig if m not in jobs])
chk("'Build completed successfully'", bool(re.search(r"(?m)^[ \t]*Build completed successfully\b", LB)), re.findall(r"Build completed successfully[^\n]*", LB))
built_new = [m for m in exig if re.search(r"Built\s+" + re.escape(m) + r"\b", LB)]
# v392 / KH-N1: o log do Audit tem DUAS partes, em ordem: (i) a saida dos `#print axioms` de usuario (uma por linha `#print axioms` do Audit final) e (ii) a saida do `run_cmd` do fim
# (uma linha por constante de TGL/TGLExt + TGL_AXIOM_COVERAGE_TOTAL). ax_audit = (i) (como antes: as checagens antigas e a de contagem de nomes valem sobre ela, sem enfraquecer);
# ax_kh = (ii); a regra «todo axioma lido esta no trio» vale sobre AS DUAS.
AUD_FINAL = rd(os.path.join(KB, "TGL", "Audit.lean")).decode("utf-8")
print_nomes = re.findall(r"(?m)^#print axioms (\S+)", AUD_FINAL); n_print = len(print_nomes)
ents = []   # (posicao, nome, lista) na ORDEM do log
for m in RE_DEP.finditer(AL):
    ents.append((m.start(), m.group(1), [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]))
for m in RE_NONE.finditer(AL):
    ents.append((m.start(), m.group(1), []))
ents.sort(key=lambda t: t[0])
ax_audit = {}; ax_kh = {}
for i_, (_, nm_, ls_) in enumerate(ents):
    (ax_audit if i_ < n_print else ax_kh).setdefault(nm_, ls_)
chk("KH-N1: o log tem uma entrada por `#print axioms` do Audit final e a ultima delas e' o ultimo nome impresso", len(ents) >= n_print and ents[n_print - 1][1] == print_nomes[-1], [len(ents), n_print, print_nomes[-1]])
fora = {k: v for k, v in list(ax_audit.items()) + list(ax_kh.items()) if not set(v) <= TRIO}
chk("todo axioma lido no log do Audit esta no trio (as duas partes: #print axioms e KH-N1)", not fora and len(ax_audit) > 0, [len(ax_audit), len(ax_kh), list(fora)[:3]])
chk("a palavra sorryAx NAO aparece no log do Audit (nem no lake build)", ("sorryAx" not in AL) and ("sorryAx" not in LB), [AL.count("sorryAx"), LB.count("sorryAx")])
# KH-N1: a linha de cobertura, as linhas que o regex do um.py LE e as que NAO le (nomes com «», etc.)
m_cov = re.search(r"TGL_AXIOM_COVERAGE_TOTAL decl=(\d+) thm=(\d+) fora_do_trio=(\d+)", AL)
kh_cov = [int(x) for x in m_cov.groups()] if m_cov else None
chk("KH-N1: linha TGL_AXIOM_COVERAGE_TOTAL presente, fora_do_trio=0", bool(m_cov) and kh_cov[2] == 0, kh_cov)
UM_DEP = re.compile(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", re.S); UM_NONE = re.compile(r"'([\w.']+)' does not depend on any axioms")   # os DO um.py (l.135598 e l.135604 do candidato)
AL_RAW = rd(os.path.join(KD, "audit.log")).decode("utf-8")
pos_cov = AL_RAW.find("TGL_AXIOM_COVERAGE_TOTAL")
ini_kh = None
if m_cov:   # o segmento do run_cmd = as linhas de constante antes da linha TOTAL: as ultimas kh_cov[0] linhas que casam com a forma geral
    forma = re.compile(r"^'(.+)' (?:depends on axioms: \[.*\]|does not depend on any axioms)$")
    linhas_kh = [l for l in AL_RAW[:pos_cov].split("\n") if forma.match(l.rstrip("\r"))][-kh_cov[0]:]
    lidas_um = [l for l in linhas_kh if UM_DEP.search(l) or UM_NONE.search(l)]
    nao_lidas = [forma.match(l.rstrip("\r")).group(1) for l in linhas_kh if not (UM_DEP.search(l) or UM_NONE.search(l))]
else:
    linhas_kh, lidas_um, nao_lidas = [], [], []
chk("KH-N1: uma linha por constante (linhas do run_cmd == decl da linha TOTAL)", bool(m_cov) and len(linhas_kh) == kh_cov[0], [len(linhas_kh), kh_cov])
# o axiom_report EFETIVO do um.py (varre o log INTEIRO; a ultima entrada de um nome vence, como em `axioms[name] = lst`)
ax_um = {}
for m in UM_DEP.finditer(AL_RAW):
    ax_um[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in UM_NONE.finditer(AL_RAW):
    ax_um.setdefault(m.group(1), [])
# a duracao do Audit (marcas de epoch gravadas por construir_kernel_v392.sh; se ausentes, as marcas HH:MM:SS)
mm_ = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
if "epoch_build_fim" in mm_ and "epoch_audit_fim" in mm_:
    dur_audit = mm_["epoch_audit_fim"] - mm_["epoch_build_fim"]; dur_build = mm_["epoch_build_fim"] - mm_["epoch_inicio"]
else:
    hms = lambda s: sum(int(x) * f for x, f in zip(s.split(":"), (3600, 60, 1)))
    t_b = re.search(r"rc_build=\d+ (\d+:\d+:\d+)", marcas).group(1); t_a = re.search(r"rc_audit=\d+ (\d+:\d+:\d+)", marcas).group(1)
    dur_audit = (hms(t_a) - hms(t_b)) % 86400; dur_build = None
# (1) build_full.log no formato do molde
bf = "inicio %s\n%s\nrc_build=%d\n%s\nrc_audit=%d\n%s\nfim %s\n" % (ini, LB.rstrip("\n"), rb, AL.rstrip("\n"), ra, "rc=0" if (rb == 0 and ra == 0) else "rc=1", fim)
open(os.path.join(KD, "build_full.log"), "w", encoding="utf-8", newline="\n").write(bf)
# (3) arvore so-fontes, sem junção; varredura recursiva com a funcao do proprio um.py v391
if not os.environ.get("V392_KEEP_ARV"):   # V392_KEEP_ARV=1: reaproveita a arvore ja conferida (nao a recopia)
    if os.path.isdir(ARV):
        shutil.rmtree(ARV)
    os.makedirs(ARV)
    for rel in ("TGL", "TGLExt"):
        shutil.copytree(os.path.join(KB, rel), os.path.join(ARV, rel), copy_function=shutil.copy2)
    for f in os.listdir(KB):
        p = os.path.join(KB, f)
        if os.path.isfile(p) and not f.startswith("TGLExt.lean.bak"):
            shutil.copy2(p, os.path.join(ARV, f))
um_src = rd(os.path.join(NOS, "um.py")).decode("utf-8"); tree = ast.parse(um_src)
fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
ns = {"re": re, "os": os}
assert "_lean_strip_comments_and_strings" in fn
seg = "\n".join(ast.get_source_segment(um_src, n) for n in (fn["_lean_strip_comments_and_strings"],))
exec(compile(seg, "<um.strip>", "exec"), ns)
TOKS = [ast.literal_eval(ast.get_source_segment(um_src, n.value)) for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_LEAN_FORBIDDEN_TOKENS"][0]
n_lean = n_o16 = 0; hits = []; hits_probe = []; links = []
pilha = [ARV]
while pilha:
    d = pilha.pop()
    with os.scandir(d) as it:
        for e in it:
            if e.is_junction() or e.is_symlink():
                links.append(e.path)
            elif e.is_dir(follow_symlinks=False):
                pilha.append(e.path)
            elif e.is_file(follow_symlinks=False) and e.name.lower().endswith(".lean"):
                n_lean += 1; rel = os.path.relpath(e.path, ARV).replace("\\", "/"); n_o16 += rel.startswith("TGLExt/O16/")
                code = ns["_lean_strip_comments_and_strings"](rd(e.path).decode("utf-8"))
                for tok in TOKS:
                    if re.search(r"\b%s\b" % re.escape(tok), code):
                        (hits_probe if os.path.basename(rel).startswith("Probe") else hits).append("%s:%s" % (rel, tok))
chk("arvore so-fontes sem juncao/link", not links, links[:3])
chk("varredura de tokens proibidos RECURSIVA: zero hits (probes diagnosticos a parte)", not hits, {"hits": hits[:5], "hits_em_Probe": hits_probe[:5], "arquivos_lean": n_lean, "em_TGLExt_O16": n_o16, "tokens": TOKS})
# (4) criterios
cob = [l.rstrip("\n").split("\t") for l in open(os.path.join(KD, "cob_v392.txt"), encoding="utf-8") if l.startswith("COB\t")]
tot = [l for l in open(os.path.join(KD, "cob_v392.txt"), encoding="utf-8") if l.startswith("COB_TOTAL")][0]
m = re.search(r"decl=(\d+)\tthm=(\d+)\tfora_do_trio=(\d+)", tot); j1 = [int(x) for x in m.groups()]
flags = json.load(open(os.path.join(KD, "FLAGS_v392.json"), encoding="utf-8"))
nomes_novos = [l.strip() for l in open(os.path.join(KD, "AUDIT_NOMES_v392.txt"), encoding="utf-8") if l.strip()]
chk("todo nome do bloco novo do Audit tem linha no log do Audit, no trio", all(n in ax_audit and set(ax_audit[n]) <= TRIO for n in nomes_novos), [n for n in nomes_novos if n not in ax_audit][:3])
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; axr = core["kernel_formalization"]["axiom_report"]
aud_antes = rd(os.path.join(KD, "Audit.lean.ANTES_v392")).decode("utf-8")
nomes_antigos = sorted(set(re.findall(r"^#print axioms (\S+)", aud_antes, re.M)))
iguais = sum(1 for n in nomes_antigos if n in ax_audit and ax_audit[n] == axr.get(n))
chk("as entradas antigas do Audit (nomes distintos) com a MESMA lista de axiomas do axiom_report v391", iguais == len(nomes_antigos), [iguais, len(nomes_antigos)])
# KH-N1: as antigas no axiom_report EFETIVO do um.py (depois de a saida do run_cmd sobrescrever nomes repetidos): listas identicas as da v391? (a ordem dos axiomas pode mudar entre #print e collectAxioms)
efet_iguais = sum(1 for n in nomes_antigos if ax_um.get(n) == axr.get(n)); efet_conj = sum(1 for n in nomes_antigos if n in ax_um and set(ax_um[n]) == set(axr.get(n, ["?"])))
efet_difere = [n for n in nomes_antigos if ax_um.get(n) != axr.get(n)]
chk("KH-N1: as entradas antigas no axiom_report EFETIVO do um.py (log inteiro) ainda iguais as da v391 (lista exata)", efet_iguais == len(nomes_antigos), [efet_iguais, efet_conj, len(nomes_antigos), efet_difere[:3]])
novas_trio = all(n in ax_audit and set(ax_audit[n]) <= TRIO for n in nomes_novos)
chk("KH-N1: as entradas novas de usuario estao no trio (parte #print) e tambem na parte KH", novas_trio and all(n in ax_kh for n in nomes_novos), [n for n in nomes_novos if n not in ax_kh][:3])
chk("KH-N1: duracao do `lake env lean TGL/Audit.lean` bem abaixo do timeout de 1800 s do um.py (< 900 s)", dur_audit < 900, {"audit_s": dur_audit, "build_s": dur_build})
kh_json = {"contrato": "KH_N1_v392", "desenho": "(a) run_cmd no fim do Audit (fonte F_KERNEL/kh/KH_formato_umpy_total.lean)", "linha_TOTAL": {"decl": kh_cov[0], "thm": kh_cov[1], "fora_do_trio": kh_cov[2]} if kh_cov else None,
           "linhas_run_cmd": len(linhas_kh), "lidas_pelo_regex_do_umpy": len(lidas_um), "nao_lidas_pelo_regex_do_umpy": len(nao_lidas), "nomes_nao_lidos": nao_lidas,
           "entradas_print_axioms_usuario": n_print, "nomes_distintos_print": len(ax_audit), "nomes_distintos_kh": len(ax_kh),
           "nomes_no_axiom_report_efetivo_umpy": len(ax_um), "antigas_nomes_distintos": len(nomes_antigos), "antigas_identicas_lista_exata_no_report_efetivo": efet_iguais,
           "antigas_identicas_como_conjunto_no_report_efetivo": efet_conj, "antigas_que_diferem_no_report_efetivo": efet_difere[:50],
           "antigas_identicas_na_parte_print_axioms": iguais, "novas_de_usuario_no_trio": novas_trio, "sorryAx_no_log_do_audit": AL.count("sorryAx"),
           "duracao_audit_s": dur_audit, "duracao_build_s": dur_build, "timeout_umpy_s": 1800, "audit_log_bytes": len(rd(os.path.join(KD, "audit.log"))), "audit_log_sha256": sha(rd(os.path.join(KD, "audit.log"))),
           "quando": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z", "estatuto": "[REAL] medido por pos_build_kernel_v392.py sobre o log do Audit do sandbox; fora do selo"}
json.dump(kh_json, open(os.path.join(KD, "KH_N1_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r1_ausente = not os.path.exists(os.path.join(ARV, "TGLExt", "TheSingularityReadsTheAttractor.lean"))
criterios = {"j1_declaracoes": j1[0], "j1_teoremas": j1[1], "j1_fora_do_trio": j1[2], "audit_entradas_antigas_identicas": iguais, "tokens_proibidos": len(hits),
             "r1_ausente": r1_ausente, "declaracoes_novas_no_trio": all(n in ax_audit and set(ax_audit[n]) <= TRIO for n in nomes_novos)}
# (5) a toolchain (as listas do manifesto pinado pelo selo v391; conferidas contra o lean/lake do sandbox)
man = json.load(open(os.path.join(NOS, "tgl_kernel_proof_manifest.json"), encoding="utf-8")); ff = man["formal_files_sha256"]
tl = {"lean_version": man.get("lean_version"), "lake_version": man.get("lake_version")}
lv = subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
kv = subprocess.run(["lake", "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
chk("toolchain do sandbox == a do manifesto pinado (lean e lake)", tl.get("lean_version") == lv and tl.get("lake_version") == kv, {"manifesto": tl, "sandbox": [lv, kv]})
imp = lambda d: hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
raiz0, aud0 = sha(rd(os.path.join(KD, "TGLExt.lean.ANTES_v392"))), sha(rd(os.path.join(KD, "Audit.lean.ANTES_v392")))
chk("ANTES (raiz, Audit) == formal_files_sha256 do manifesto v391 pinado", ff.get("TGLExt.lean") == raiz0 and ff.get("TGL/Audit.lean") == aud0, [raiz0[:16], aud0[:16]])
pedras = []
pins = P.gerar_pinos()
for s, p in zip(P.STONES, pins):
    shr = sha(rd(os.path.join(ARV, "TGLExt", s["mod"] + ".lean")))
    _fonte = rd(os.path.join(ARV, "TGLExt", s["mod"] + ".lean")).decode("utf-8")
    _GER = {"ctorIdx", "sizeOf_spec", "injEq", "noConfusion", "noConfusionType", "rec", "recOn", "casesOn", "brecOn", "binductionOn", "below", "ibelow", "inj", "eq_1", "eq_def"}   # gerados pelo Lean; excluidos so' se o sufixo NAO aparece na fonte da pedra
    _ger = lambda n: n.split(".")[-1] in _GER and not re.search(r"(?<![\w.])%s(?![\w])" % re.escape(n.split(".")[-1]), _fonte)
    decl = [c[2] for c in cob if c[1] == "TGLExt." + s["mod"] and c[2] in set(nomes_novos) and not _ger(c[2])]
    chk("pedra %s: sha na arvore == pino" % s["mod"], shr == p["sha256"])
    pedras.append({"path": "TGLExt/%s.lean" % s["mod"], "sha256": shr, "declaracoes": sorted(set(decl))})
recibo = {"contrato": "KERNEL_RECIBO_R3_2", "versao": "v392", "rc": 0, "sorry": 0, "erros": 0,
          "build_full_log": {"path": abs_fw(os.path.join(KD, "lake_build.log")), "sha256": sha(rd(os.path.join(KD, "lake_build.log")))},
          "audit_log": {"path": abs_fw(os.path.join(KD, "audit.log")), "sha256": sha(rd(os.path.join(KD, "audit.log")))},
          "toolchain": {"lean_version": lv, "lake_version": kv}, "arvore": abs_fw(ARV),
          "raiz": {"path": "TGLExt.lean", "sha256_antes": raiz0, "sha256_depois": sha(rd(os.path.join(ARV, "TGLExt.lean")))},
          "audit": {"path": "TGL/Audit.lean", "sha256_antes": aud0, "sha256_depois": sha(rd(os.path.join(ARV, "TGL", "Audit.lean")))},
          "pedras": pedras, "formal_files_antes": ff, "axiomas": sorted(TRIO),
          "varredura_tokens": {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16},
          "criterios": {k: {"medido": v} for k, v in criterios.items()},
          "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos (manifesto pinado pelo selo v391)", "antes": imp(ff), "depois": imp(ff)},
          "quando_utc": __import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z",
          "nota": "gerado por pos_build_kernel_v392.py (preparacao, 13/10/2026); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v392 e do manifesto novo); a arvore de varredura e' a copia so-fontes C:/t/k392/arvore (apagada ao fim da preparacao: o recibo deve ser regerado na cadeia real)"}
ok = all(s["ok"] for s in sinais)
json.dump(recibo, open(os.path.join(KD, "KERNEL_RECIBO_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
crit = {"contrato": "CRITERIOS_R3_1", "versao": "v392", "preenchido": True, "x19": "sim", "esperados": criterios,
        "origem": "[DERIVED] preenchido pela PREPARACAO com a medicao de kernel/KERNEL_RECIBO_v392.json (J1 = as pedras de STONES, 14 na rodada 2: 8 + X19 + Posto, Santo, IALD, Verdade + o adendo do rank); x19='sim' = decisao ja tomada pela gerencia "
                  "(hipotese tipada); a gerencia confere e pina o sha256 em v392_pins antes do B(3). Os J1 do plano (159/130/0) eram SEM a X19 e sem as 4 pedras de 13/10.",
        "nota": "NOT_FALSIFIED nunca e creditacao; nada aqui move o gate"}
os.makedirs(os.path.join(HERE, "vinculo"), exist_ok=True)
json.dump(crit, open(os.path.join(HERE, "vinculo", "CRITERIOS_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"ok": ok, "sinais": sinais, "criterios": criterios, "arquivos_lean": n_lean, "em_O16": n_o16, "jobs_built": built_new, "n_axiomas_lidos_no_audit": len(ax_audit), "hits_em_Probe": hits_probe,
           "n_flags": flags["n_flags"], "n_decl_audit": flags["n_decl_audit"], "inicio": ini, "fim": fim},
          open(os.path.join(KD, "POS_BUILD_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nPOS-BUILD:", "VERDE" if ok else "FALHOU", "| criterios:", criterios, "| .lean:", n_lean, "(O16:", n_o16, ")")
sys.exit(0 if ok else 1)
