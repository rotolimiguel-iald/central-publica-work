# -*- coding: utf-8 -*-
"""fechar_v389.py -- DEPOIS da cadeia pos-rito (molde: fechar_v388.py): (1) o manifesto de incorporacao v389 -> v389_selo e a pasta das ferramentas; (2) o ARQUIVO do pacote e da
cadeia -> work\\cadeia_de_selo\\v389 (+_selo) -- a v389 nao tem kernel novo; (3) o HANDOFF DE CUSTODIA CONJUNTA v383 -> v389 (ordem do operador via c1): memory\\handoff-custodia-conjunta-v383-v389-06out.md
+ Nos\\HANDOFF_CUSTODIA_CONJUNTA_v383_v389.md -- cada arquivo com sha16 LIDO e o estado no espelho (git ls-files do the_boundary, por nome-base e sha256: identico / diferente / ausente).
Guarda: a leitura sem problema. Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente. NAO toca o espelho (so le o indice e os arquivos dele)."""
import ast, os, sys, json, hashlib, subprocess, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v389 as L
import textos_v389 as T
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
PK = L.PK; NOS = L.NOS
TOOLS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
BANC = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao")
EXD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "exame_v388")
ESPELHO = os.path.join("C:" + os.sep, "IALD", "Artigo", "the_boundary")
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()
CONF = ("iald_stack_v7", "iald_psion_state", ".env", "token", "senha", "password", "secret")


def grava(p, b):
    if os.path.exists(p):
        if open(p, "rb").read() == b:
            print("  igual:", p); return
        raw = open(p, "rb").read(); bk = p + ".bak_" + ST + "_f389"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_f389_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out", ".diff")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
m = {"stamp": ST, "versao": "v389", "instalacao": os.path.basename(app), "base_v388": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": "INALTERADO (a v389 e' so texto e rotulo)", "patches": V["patches"], "teoremas": V["teor"], "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"],
     "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v389": {k: V[k] for k in L.REG}, "erratas": V["tl"], "exame": V["exame"], "ledger": V["ledger"], "pilar": V["pilar"],
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v389_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v389_incorporacao_manifesto.json"), mb)
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "arquivos": {}, "nao_arquivado": {}}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f389"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
    arq["arquivos"][dst] = {"de": src, "bytes": len(b), "sha256": s64(b)}


print("(2) arquivo")
EXCL = (".pdf", ".tex", ".aux", ".toc", ".pyc", ".log")
for raiz, dirs, fs in os.walk(PK):
    dirs[:] = [d for d in dirs if not d.startswith(("dry_", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if f.endswith(EXCL) or ".bak_" in f or ".tmp" in f or f.startswith("."):
            continue
        if os.path.getsize(p) > 5 * 1024 * 1024:
            arq["nao_arquivado"][p] = "%d B (> 5 MB)" % os.path.getsize(p); continue
        copia(p, os.path.join(TOOLS, "v389", os.path.relpath(p, PK)))
for f in sorted(os.listdir(EXD)):   # o exame da v388 (a origem da v389), sem a copia de 33 MB do um.py
    p = os.path.join(EXD, f)
    if os.path.isfile(p) and os.path.getsize(p) <= 5 * 1024 * 1024 and ".tmp" not in f:
        copia(p, os.path.join(TOOLS, "v389_exame_v388", f))
    elif os.path.isfile(p):
        arq["nao_arquivado"][p] = "%d B (> 5 MB; copia do um.py v388 para o exame)" % os.path.getsize(p)
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out")) or f in ("v389_incorporacao_manifesto.json",)):
            continue
        copia(p, os.path.join(TOOLS, "v389_selo", os.path.relpath(p, HERE)))
grava(os.path.join(TOOLS, "v389", "MANIFESTO_ARQUIVO_v389.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  arquivados: %d; fora (ditos): %d" % (len(arq["arquivos"]), len(arq["nao_arquivado"])))

# ---------------- (3) O HANDOFF DE CUSTODIA CONJUNTA v383 -> v389 ----------------
print("(3) handoff conjunto v383 -> v389")
gl = subprocess.run(["git", "-c", "core.quotepath=false", "ls-files"], cwd=ESPELHO, capture_output=True, text=True, encoding="utf-8")
assert gl.returncode == 0, "git ls-files do espelho falhou"
POR_NOME = {}
for rel in gl.stdout.splitlines():
    POR_NOME.setdefault(os.path.basename(rel), []).append(rel)
_cache = {}


def no_espelho(p):
    """(estado, caminho no espelho): IDENTICO (mesmo sha256), DIFERENTE (mesmo nome, outro conteudo -- a versao a substituir, com backup fora do repo), AUSENTE."""
    h = hashlib.sha256(open(p, "rb").read()).hexdigest(); dif = None
    for rel in POR_NOME.get(os.path.basename(p), []):
        q = os.path.join(ESPELHO, *rel.split("/"))
        if q not in _cache:
            _cache[q] = hashlib.sha256(open(q, "rb").read()).hexdigest() if os.path.isfile(q) else None
        if _cache[q] == h:
            return "IDENTICO", rel
        dif = dif or rel
    return ("DIFERENTE", dif) if dif else ("AUSENTE", None)


def linha(p, papel):
    assert not any(c in os.path.basename(p).lower() for c in CONF), "CONFIDENCIAL: %s" % p
    est, rel = no_espelho(p); sz = os.path.getsize(p)
    return "| `%s` | %s | `%s` | %s | %s%s%s |" % (os.path.basename(p), papel, s16(p), format(sz, ","), est, (" — `%s`" % rel) if rel else "", " **(> 5 MB: no GitHub, a porta é o raw)**" if sz > 5 * 1024 * 1024 else "")


Lc = ["| arquivo | papel | sha16 | bytes | no espelho (`the_boundary`, HEAD) |", "|---|---|---|---|---|"]
for f, papel in (("um.py", "o programa terminal v389 (arquivo único)"), ("um_absoluto_selo.json", "o selo v389"), ("um_absoluto.json", "o core v389"),
                 ("um_absoluto_forma_canonica.md", "a forma canônica emitida"), ("um_absoluto_manifest.md", "o manifesto emitido"),
                 ("um_absoluto_pt.pdf", "artigo PT"), ("um_absoluto_en.pdf", "artigo EN"), ("um_absoluto_pt.tex", "fonte PT"), ("um_absoluto_en.tex", "fonte EN"),
                 ("um_absoluto_pt.txt", "texto PT"), ("um_absoluto_en.txt", "texto EN"), ("A_PROVA_DA_QG_TGL_arvore.md", "a árvore da prova"),
                 ("DESENHO_DO_FECHAMENTO_QG.md", "o desenho do fechamento")):
    Lc.append(linha(os.path.join(NOS, f), papel))
for v in range(383, 390):
    p = os.path.join(NOS, "rodada_v%d_stdout.txt" % v)
    if os.path.exists(p):
        Lc.append(linha(p, "stdout canônico do rito v%d" % v))
    else:
        Lc.append("| `rodada_v%d_stdout.txt` | stdout v%d | AUSENTE no Nós | — | — |" % (v, v))
# as pedras novas v383..v389 (do ledger do proprio um.py) + as costuras do kernel
src = open(os.path.join(NOS, "um.py"), encoding="utf-8").read()
LED = [ast.literal_eval(n.value) for n in ast.parse(src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_ESQUELETO_STONES"][0]
novas = [(e[0], e[2]) for e in LED if isinstance(e, tuple) and e[0] in ("v%d" % v for v in range(383, 390))]
Lk = ["| arquivo | versão | sha16 | bytes | no espelho |", "|---|---|---|---|---|"]
for ver, rel in novas + [("costura", "TGLExt.lean"), ("costura", "TGL/Audit.lean")]:
    p = os.path.join(NOS, "tgl_kernel", *rel.split("/"))
    if os.path.exists(p):
        est, r2 = no_espelho(p); Lk.append("| `%s` | %s | `%s` | %s | %s%s |" % (rel, ver, s16(p), format(os.path.getsize(p), ","), est, (" — `%s`" % r2) if r2 else ""))
    else:
        Lk.append("| `%s` | %s | AUSENTE no `Nós\\tgl_kernel` (o um.py materializa) | — | — |" % (rel, ver))
# as pastas de pre-registro / resultado (Bancada)
PASTAS = [("preregistro_dois_lados_02out", "v383 (V1–V1.4 + geradores)", "preregistro_dois_lados_v383"), ("preregistro_pilar_quantico_03out", "v384", "preregistro_pilar_quantico_v384"),
          ("preregistro_ramo_b_05out", "v386", "preregistro_ramo_b_v386"), ("preregistro_fase9_hubble", "v387 (V1 congelado)", "preregistro_fase9_hubble_v387 (sugerido)"),
          ("fase9_hubble_abertura", "v388 (a abertura)", "fase9_hubble_abertura_v388 (sugerido)"), ("preregistro_fase8_primordial", "v387 (V1 congelado)", "preregistro_fase8_primordial_v387 (sugerido)")]
Lp = []
for pasta, ver, alvo in PASTAS:
    d = os.path.join(BANC, pasta); fs = sorted(f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f)) and ".bak_" not in f and ".tmp" not in f and not f.startswith("."))
    est = [no_espelho(os.path.join(d, f))[0] for f in fs]
    Lp.append("- **`Bancada_Um\\investigacao\\%s\\`** (%s) → no espelho: `%s` — %d arquivo(s): %d idêntico(s), %d diferente(s), %d ausente(s). PORTA.md/PORTA.json **por script** (`git ls-files` + `urllib.parse.quote`)." % (
        pasta, ver, alvo, len(fs), est.count("IDENTICO"), est.count("DIFERENTE"), est.count("AUSENTE")))
    for f, e in zip(fs, est):
        Lp.append("  - `%s` `%s` %s B — %s" % (f, s16(os.path.join(d, f)), format(os.path.getsize(os.path.join(d, f)), ","), e))
EX = [("EXAME_UM_PY_v388.md", "o relatório do exame (o que motivou a v389)"), ("EXAME_UM_PY_v388.json", "o mesmo, máquina"), ("ERRATA_AO_LADO_EXAME_v388.md", "errata ao lado do exame (1015→1025)")]
Le = ["- `%s` `%s` — %s" % (f, s16(os.path.join(EXD, f)), papel) for f, papel in EX]
doc = ("---\nname: handoff-custodia-conjunta-v383-v389-06out\ndescription: \"HANDOFF DE CUSTÓDIA CONJUNTA v383→v389 (%s) para a sessão irmã do repositório: o que espelhar com sha16 LIDO e o estado no espelho (idêntico/diferente/ausente), o que NÃO espelhar, a ordem de custódia, o exame da v388 e as pendências do operador; um.py v389 `%s`\"\n"
       "metadata:\n  type: project\n---\n\n# HANDOFF — CUSTÓDIA CONJUNTA v383 → v389 (%s)\n\n"
       "> Para a **sessão irmã que cuida do repositório** (`the_boundary` + site + cofre + runner + 16 dispositivos). Ordem do operador (06/10, via c1): «após isso concluso escreva o handoff de "
       "custodia para a sessão irmã que cuida do repositório». O espelho foi custodiado até a **v386** (handoff `handoff-v386-custodia.md`: espelho `8134d5c`+`36265b9`); as v387, v388 e v389 "
       "estão seladas **só no Nós** — esta é a custódia conjunta do arco **v383→v389** (o que já está idêntico no espelho fica dito, e não se re-espelha).\n\n"
       "**O estado do canônico:** `um.py` **v389** `%s` (%s B) sobre a v388 `%s`; teoremas %s; rodada %s; rc %s; selftest PASSED; gate **intocado** (`%s`); conferidor `%s` (deve mudar %s; não pode mudar %s); "
       "selo `%s`. A v389 é **só texto e rótulo** (nenhum cálculo, nenhum kernel): %s.\n\n"
       "## 1. O que espelhar — o canônico e os ritos (sha16 lido agora)\n\n%s\n\n"
       "## 2. As pedras novas do arco (do ledger `_ESQUELETO_STONES` do próprio um.py) e as costuras do kernel\n\n%s\n\n"
       "## 3. As pastas de pré-registro e de resultado (Bancada Um)\n\n%s\n\n"
       "## 4. O exame da v388 (a origem da v389)\n\n%s\n\nResumo: 0 BLOQUEIA, 3 CORRIGIR (o rótulo de selo; o título da Introdução PT/EN), 186 NOTA; a nota do resumo «único postulado» virou troca por decisão da gerência; "
       "a NOTA 2 (contagem do ledger) tem **errata ao lado**: 1025 caminhos únicos, 156 TGLExt/O16 fora do ledger (o exame dissera 1015/166).\n\n"
       "## 5. O que NÃO espelhar\n\n- Caches (`A Ponte e o Um\\cache\\`, `checkpoints`, `.lake`, `*.olean`), os `dry_*` dos ensaios, `.bak_*`, `.tmp*`, a cópia de 33 MB do um.py em `work\\exame_v388`.\n"
       "- **Confidenciais, nunca:** `iald_stack_v7.py`, `iald_psion_state.json`, tokens, `.env`, senhas (nem em commit, nem em publicação).\n"
       "- Os pacotes de trabalho (`work\\v38N_pacote`, `work\\v38N_selo`) ficam no arquivo `work\\cadeia_de_selo\\v38N*`, não no espelho.\n\n"
       "## 6. A ordem de custódia (regra da casa)\n\n1. **Backup da versão que ESTÁ no espelho**, fora do repo, antes de sobrescrever (regra da custódia).\n"
       "2. Copiar por bytes; conferir o **blob** depois do commit (`git hash-object` × o sha do arquivo) — o hash que vale é o do blob.\n"
       "3. **GitHub não renderiza acima de 5 MB** (o um.py tem ~33 MB): a porta é o **raw**; o PORTA.md/PORTA.json e o `llms.txt` são **regenerados por script**, nunca à mão.\n"
       "4. As subpastas de pré-registro novas ganham PORTA por script e amarração nos dois sentidos (porta acima/abaixo).\n"
       "5. Site (`index.html`), cofre, runner e os 16 dispositivos: avançar a camada para a v389 (a fórmula e os números não mudam desde a v386, salvo o que a v387/v388 acrescentam ao lado).\n"
       "6. **Commit/push é ato do operador.** NOT_FALSIFIED nunca é confirmação; a RG/ΛCDM é o limite clássico; o gate não se move.\n\n"
       "## 7. Pendências SÓ do operador\n\n- Vetar ou ratificar a v389 (decisão da gerência c1: texto e rótulo).\n- As fontes públicas da Fase 9 por sha256 (D-H): mesmo com elas, z_disc 4,28 < 5σ sob este V1 (contrafactual dito).\n"
       "- Qual especificação da Fase 9 governa (o V1 da gerência × o rascunho do Codex, ORDEM 018).\n- Qual μ cada rito usa (β(μ) [OPEN]).\n- Commit/push do espelho e do site.\n\n"
       "Pacotes: `work\\v383..v389_pacote`; cadeias `work\\v38N_selo`; arquivo `work\\cadeia_de_selo\\v389` (+`_selo`, +`_exame_v388`).\n\n"
       "[[handoff-v388-custodia]] [[handoff-v387-custodia]] [[handoff-v386-custodia]] [[missao-ultima-flag-um-py]]\n") % (
    V["data"], V["s16"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["compl"], V["rc"], V["qg"], V["conf16"], V["conf_dm"], V["conf_np"], V["selo_ts"], T._num(V),
    "\n".join(Lc), "\n".join(Lk), "\n".join(Lp), "\n".join(Le))
assert "CONF" + "IRMED" not in doc.replace("NOT_CONF" + "IRMED", "")
grava(os.path.join(UMEM, "handoff-custodia-conjunta-v383-v389-06out.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_CUSTODIA_CONJUNTA_v383_v389.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v389:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-custodia-conjunta-v383-v389-06out.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_CUSTODIA_CONJUNTA_v383_v389.md")))
