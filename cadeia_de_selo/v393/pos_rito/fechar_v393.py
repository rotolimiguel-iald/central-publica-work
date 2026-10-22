# -*- coding: utf-8 -*-
"""fechar_v393.py -- DEPOIS da cadeia pos-rito e do elo B(3) (molde: fechar_v392.py + fechar_v390.py): (1) o manifesto de incorporacao v393 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\cadeia_de_selo\\v393 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\cadeia_de_selo\\v393_selo e do kernel (work\\cadeia_de_selo\\v393\\kernel e, se existir, work\\v393_kernel; mais as pedras do Nos) -> work\\cadeia_de_selo\\v393_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v392_v393.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v393.txt (o kernel embutido, molde do v390);
(4) o HANDOFF (memory\\handoff-v393-custodia.md + Nos\\HANDOFF_v393_CUSTODIA.md) para a sessao do site.
GUARDAS: a leitura sem problema; os tres RECIBOS do B(3) (R3, Remissao 4): o RECIBO_SINCRONIZACAO_v393_*.json do 10-bis (aplicar, bateria passa), o recibo da PARADA do servico (10-bis-a) e o do
RELIGAMENTO (10-ter, com a versao servida e o sha do manifesto novo) -- sem eles o fechar RECUSA e o handoff nao nasce; a guarda de texto P18 no handoff.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
import glob, hashlib, json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v393 as L
import textos_v393 as T
from guarda_p18_v393 import violacoes
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
NOS = L.NOS; WK = os.path.dirname(os.path.dirname(PK)); TOOLS = os.path.join(WK, "cadeia_de_selo")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()
DIRS_B3 = os.path.join(PK, "bancada_B3"); DIRS_SERV = os.path.join(PK, "bancada_B3_servico")


def _j(p):
    return json.load(open(p, encoding="utf-8"))


# ---------------------------------------------------------------- 0. os tres recibos do B(3): sem eles, nao fecha
def recibos_b3():
    prob = []; out = {}
    # a pasta do aplicar e' nova a cada tentativa (bancada_B3, bancada_B3_2, ...); o ensaio (bancada_B3_ensaio_*) NAO conta
    ap = sorted(glob.glob(os.path.join(DIRS_B3, "RECIBO_SINCRONIZACAO_v393_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v393_*.json")), key=os.path.getmtime)
    if not ap:
        prob.append("sem o RECIBO_SINCRONIZACAO_v393_*.json do 10-bis em %s (nem em bancada_B3_<n>)" % DIRS_B3)
    else:
        r = _j(ap[-1])
        if not (str(r.get("veredito") or "").startswith("REPINADA_B") and r.get("modo") == "aplicar" and r.get("fase") == "pos_selo" and r.get("versao_alvo") == "v393"
                and (r.get("bateria_resultado") or {}).get("veredito") == "BATERIA_PASSA" and r.get("aplicacao")):
            prob.append("o recibo do 10-bis nao e' de uma aplicacao pos_selo v393 com a bateria passando: %s" % os.path.basename(ap[-1]))
        out["aplicar"] = {"path": ap[-1], "sha256": s64(open(ap[-1], "rb").read()), "veredito": r.get("veredito"), "manifesto_novo_sha256": (r.get("manifesto_novo") or {}).get("sha256"),
                          "evento": ((r.get("evento_c1") or {}).get("evento")), "bateria": (r.get("bateria_resultado") or {}).get("veredito")}
    pp = os.path.join(DIRS_SERV, "RECIBO_PARADA_v393.json"); rp = os.path.join(DIRS_SERV, "RECIBO_RELIGAMENTO_v393.json")
    if not os.path.exists(pp):
        prob.append("sem o recibo da PARADA do servico (10-bis-a): %s" % pp)
    else:
        d = _j(pp); pid = d.get("pid") or d.get("pids") or d.get("PID"); fech = d.get("porta_fechada") or d.get("fechada"); hora = d.get("hora") or d.get("quando")
        if not (pid and fech is True and d.get("porta") == 18777 and hora):
            prob.append("o recibo da parada nao traz pid, porta 18777, porta_fechada true e hora")
        out["parada"] = {"path": pp, "sha256": s64(open(pp, "rb").read()), "hora": hora, "pid": pid}
    if not os.path.exists(rp):
        prob.append("sem o recibo do RELIGAMENTO do servico (10-ter): %s" % rp)
    else:
        d = _j(rp); vs = d.get("versao_servida") or d.get("versao"); msha = d.get("manifesto_sha256")
        esperado = (out.get("aplicar") or {}).get("manifesto_novo_sha256")
        if not (vs == "v393" and msha and esperado and msha == esperado and (d.get("pid") or d.get("PID")) and (d.get("hora") or d.get("quando"))):
            prob.append("o recibo do religamento nao traz versao servida v393, o sha do manifesto novo do recibo do 10-bis, pid e hora")
        out["religamento"] = {"path": rp, "sha256": s64(open(rp, "rb").read()), "versao_servida": vs, "manifesto_sha256": msha}
    return out, prob


B3, PB3 = recibos_b3()
if PB3:
    print("FECHAR RECUSADO -- o elo B(3) da Bancada nao esta completo (R3, Remissao 4):")
    for x in PB3:
        print("  -", x)
    print("  (a cadeia para em AGUARDA_OPERADOR ate a palavra do operador para a B3; depois rodar a cadeia a partir do passo 11)"); sys.exit(2)


def grava(p, b):
    if os.path.exists(p):
        if open(p, "rb").read() == b:
            print("  igual:", p); return
        raw = open(p, "rb").read(); bk = p + ".bak_" + ST + "_f392"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp_f392_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


# ---------------------------------------------------------------- (3) os dois diffs (antes do manifesto, para entrarem nele)
def carregar_embutido(path):
    import ast
    text = open(path, "rb").read().decode("utf-8"); lines = text.splitlines(keepends=True)
    i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]; assert len(i0) == 1, i0
    j = i0[0] + 1
    while lines[j].rstrip("\r\n") != "}":
        j += 1
    return ast.literal_eval("".join(lines[i0[0]:j + 1]).split("=", 1)[1].strip())


um = os.path.join(NOS, "um.py"); base = V["base_backup"]
assert os.path.exists(base) and s16(base) == V["base16"], "o backup da base (APLICADO_AO_CANONICO) nao e' a v392 selada: " + base
print("(3) diffs")
exe = shutil.which("diff")
if exe:
    r = subprocess.run([exe, "-U", "2", "--label", "um.py v392 %s" % V["base16"], "--label", "um.py v393 %s" % V["s16"], base, um], capture_output=True)
    assert r.returncode == 1, "diff rc=%s: %s" % (r.returncode, r.stderr[:200])
    dd = r.stdout
else:
    import difflib
    a = open(base, "r", encoding="utf-8", newline="").read().splitlines(); b = open(um, "r", encoding="utf-8", newline="").read().splitlines()
    dd = ("\n".join(difflib.unified_diff(a, b, "um.py v392 %s" % V["base16"], "um.py v393 %s" % V["s16"], lineterm="", n=2)) + "\n").encode("utf-8")
grava(os.path.join(PK, "DIFF_v392_v393.diff"), dd)
import difflib
E0 = carregar_embutido(base); E1 = carregar_embutido(um)
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v392 (%s) -> v393 (%s)" % (V["base16"], V["s16"]), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, s64(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a_, b_ = E0[k].splitlines(), E1[k].splitlines(); d_ = list(difflib.unified_diff(a_, b_, "v392/" + k, "v393/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, s64(E0[k].encode())[:16], s64(E1[k].encode())[:16], sum(1 for l in d_ if l.startswith("+") and not l.startswith("+++")),
                                                         sum(1 for l in d_ if l.startswith("-") and not l.startswith("---"))))
    if k == "TGLExt.lean":
        out += ["      " + l for l in d_]
    else:
        out += ["      " + l[:200] for l in d_[:6]] + ["      ... (%d linhas de diff no total)" % len(d_)]
grava(os.path.join(PK, "DIFF_KERNEL_v393.txt"), ("\n".join(out) + "\n").encode("utf-8"))
assert len(novos) == V["n_pedras"] and not removidos, ("o kernel embutido: novos != pedras do registro ou arquivo removido", len(novos), V["n_pedras"], removidos)

# ---------------------------------------------------------------- (1) o manifesto de incorporacao
ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out", ".diff", ".md")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
ESP = _j(os.path.join(PK, "ESPERADOS_v393.json"))
pedras_nos = {rel: s16(os.path.join(NOS, "tgl_kernel", *rel.split("/"))) for rel in ESP["pedras_sha256"]}
m = {"stamp": ST, "versao": "v393", "instalacao": os.path.basename(app), "base_v392": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": {"pedras_no_nos_sha16": pedras_nos, "escada": [V["escada_antes"], V["teor"]], "axiom_report_n": V["axiom_report_n"], "build_full_log_sha16": s16(os.path.join(PK, "kernel", "build_full.log")) if os.path.exists(os.path.join(PK, "kernel", "build_full.log")) else None,
                "kernel_recibo_sha16": s16(os.path.join(PK, "kernel", "KERNEL_RECIBO_v393.json")) if os.path.exists(os.path.join(PK, "kernel", "KERNEL_RECIBO_v393.json")) else None},
     "patches": V["patches"], "teoremas": V["teor"], "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"],
     "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v393": V["registros"], "troca_dita": V["troca_dita"], "pedras": V["pedras"], "varredura": V["varr"], "verbatins": V["verbatins"], "fundacao_v390": V["fd390"], "pilar": V["pilar"],
     "insumo_codex_regra_sha16": s16(os.path.join(PK, "insumos", "AO_CLAUDE_INTEGRAR_REGRA_V393.md")), "b3": B3,
     "diffs": {"DIFF_v392_v393.diff": s16(os.path.join(PK, "DIFF_v392_v393.diff")), "DIFF_KERNEL_v393.txt": s16(os.path.join(PK, "DIFF_KERNEL_v393.txt"))},
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v393_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v393_incorporacao_manifesto.json"), mb)
# ---------------------------------------------------------------- (2) o arquivo
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "pacote": PK, "arquivos": {}, "copias": {}, "nao_copiado": {}}


def indexa(p):
    b = open(p, "rb").read(); arq["arquivos"][p] = {"bytes": len(b), "sha256": s64(b)}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f392"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
    arq["copias"][dst] = {"de": src, "bytes": len(b), "sha256": s64(b)}


print("(2) arquivo")
EXCL = (".pyc",)
for raiz, dirs, fs in os.walk(PK):
    dirs[:] = [d for d in dirs if not d.startswith(("dry_", "__pycache__", "pilar_anterior"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if f.endswith(EXCL) or ".bak_" in f or ".tmp" in f:
            continue
        indexa(p)
# pos_rito (e o conferidor) -> v393_selo
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out", ".txt")) or f == "v393_incorporacao_manifesto.json"):
            continue
        copia(p, os.path.join(TOOLS, "v393_selo", os.path.relpath(p, HERE)))
# kernel: a pasta kernel da cadeia (+ work\v393_kernel, se existir) e as pedras do Nos -> v393_kernel
for src in (os.path.join(PK, "kernel"), os.path.join(WK, "v393_kernel")):
    if os.path.isdir(src):
        for f in sorted(os.listdir(src)):
            p = os.path.join(src, f)
            if os.path.isfile(p):
                if os.path.getsize(p) > 5 * 1024 * 1024:
                    arq["nao_copiado"][p] = "%d B (> 5 MB; indexado por sha256)" % os.path.getsize(p); continue
                copia(p, os.path.join(TOOLS, "v393_kernel", ("" if src.startswith(PK) else "work_v393_kernel"), f))
for rel in ESP["pedras_sha256"]:
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v393_kernel", "pedras", rel.replace("/", "_")))
for rel in ("TGLExt.lean", "TGL/Audit.lean"):
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v393_kernel", "depois", rel.replace("/", "_")))
for f in ("DIFF_v392_v393.diff", "DIFF_KERNEL_v393.txt"):
    copia(os.path.join(PK, f), os.path.join(TOOLS, "v393_kernel", f))
grava(os.path.join(PK, "MANIFESTO_ARQUIVO_v393.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  indexados: %d; copiados: %d; nao copiados (ditos): %d" % (len(arq["arquivos"]), len(arq["copias"]), len(arq["nao_copiado"])))
# ---------------------------------------------------------------- (4) o handoff
ap_ = B3.get("aplicar") or {}
doc = ("---\nname: handoff-v393-custodia\ndescription: \"HANDOFF v393 (%s) para a sessão do site: a regra e o coração; `%s`; B3 da Bancada feita; custódia + pendências do operador\"\n"
       "metadata:\n  type: project\n---\n\n# HANDOFF v393 — CUSTÓDIA (%s)\n\n"
       "**O que é:** `um.py` **v393** `%s` (%s B) sobre a v392 `%s`; %s; COMPLETA; rc %s; selftest PASSED; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); pilar %s pela chave. "
       "Selo `%s`.\n\n**O que entrou e o que mediu:** %s.\n\n"
       "**O elo B(3) da Bancada Um (feito antes deste handoff):** recibo da aplicação `%s` (sha256 `%s`; veredito `%s`; evento %s; bateria `%s`); recibo da parada do serviço sha256 `%s`; "
       "recibo do religamento sha256 `%s` (versão servida v393, manifesto `%s`).\n\n"
       "**Para a sessão do site (custódia):** o `um.py` v393, `rodada_v393_stdout.txt`, o selo, o core, o .md canônico e o manifesto, os artigos PT/EN (%s), as quatro cunhagens do operador de 14/10 por sha256 (%s), "
       "as três pedras da regra (`work\\cadeia_de_selo\\v393_kernel\\pedras`) e os dois diffs (`DIFF_v392_v393.diff`, `DIFF_KERNEL_v393.txt`) — com PORTA gerada por script, URL raw (o um.py tem mais de 5 MB), backup da "
       "versão v392 no espelho fora do repositório, blob conferido depois do push. Publicar as pedras novas no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; os recibos da bateria do B(3) vão ao espelho com PORTA; a errata ao lado do registro `kh_n1_cobertura_v392` (re-pinagem a uma cópia; pisos no lugar das igualdades); "
       "o runner da Fronteira e a camada v393 dos 16 dispositivos (o número do runner é da sessão do site); quatro céticos independentes antes do portão do operador.\n\n"
       "**Pendências SÓ do operador:** a custódia, subir o site, commit/push. A evidência espectral independente do coração (cadeia pinada independente do CODATA) segue ausente; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v393.\n\n"
       "Pacote e cadeia: `work\\cadeia_de_selo\\v393` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v393_selo` e `v393_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
       "[[v393-selada-a-regra-e-o-coracao-14out]] [[missao-ultima-flag-um-py]] [[handoff-v392-custodia]]\n") % (
    V["data"], V["s16"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
    "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["selo_ts"], T._num(V),
    os.path.basename(ap_.get("path", "?")), str(ap_.get("sha256"))[:16], ap_.get("veredito"), ap_.get("evento"), ap_.get("bateria"), str((B3.get("parada") or {}).get("sha256"))[:16],
    str((B3.get("religamento") or {}).get("sha256"))[:16], str((B3.get("religamento") or {}).get("manifesto_sha256"))[:16],
    ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), T._verb(V))
vv = violacoes(doc)
assert not vv, "a guarda de texto (P18) achou violacao(oes) no handoff: %r" % (vv[:3],)
print("(4) handoff")
grava(os.path.join(UMEM, "handoff-v393-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v393_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v393:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v393-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v393_CUSTODIA.md")))
