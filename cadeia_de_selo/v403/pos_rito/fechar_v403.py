# -*- coding: utf-8 -*-
"""fechar_v403.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v402.py FINAL, o que rodou em 26-27/10): (1) o manifesto de incorporacao v403 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\cadeia_de_selo\\v403 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\cadeia_de_selo\\v403_selo, A COPIA DO SIDECAR um_absoluto_selo_acom.json (reescrito pelo rito) E DO SELO PRIMARIO para a mesma pasta, e do kernel (work\\cadeia_de_selo\\v403\\kernel e, se existir, work\\v403_kernel; mais as TRES pedras do Nos) -> work\\cadeia_de_selo\\v403_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v402_v403.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v403.txt (o kernel embutido: as TRES pedras novas (TGLExt/Caminho, TGLExt/Vida, TGLExt/VerdadeAdendo; os nomes sao do operador, 27/10/2026), a raiz e o Audit);
(4) o HANDOFF (memory\\handoff-v403-custodia.md + Nos\\HANDOFF_v403_CUSTODIA.md) para a sessao do site, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado),
gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme) sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o NOVO, «Caminho, Verdade e Vida (v403)», gerado dos registros selados caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403 e cunhagens_v403
(numeros LIDOS do core, estatutos, limites, as inscricoes do operador de 27/10, as erratas E5 e E6 em nome da gerencia c1, a F8.1, sem o 4,44); o handoff traz tambem a NOTA ao lado do paragrafo da v402 (os nomes que ele trazia como provisorios sao agora os do operador) e DIZ que os paragrafos do testemunho de dois (v399), da falsidade (v401) e da v402 SEGUEM COMO ESTAO, e LISTA o sidecar com o sha256 e o veredito.
GUARDAS: a leitura sem problema (inclui o sidecar); o PARAGRAFO DO QUADRO passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do operador verbatim; numeros
iguais aos do resultado); o PARAGRAFO NOVO passa na verificacao propria (T.verificar_paragrafo_v403: numeros == ESPERADOS e == o gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim das falas do operador, do kernel embutido ou do adendo que a errata supera; sem alegacao de seguranca criptografica) --
se QUALQUER um nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v403_*.json do 10-bis, o recibo da PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA e o handoff nao nasce;
a guarda de texto P18 no handoff.
v403 (FILA DA MEMORIA): o diretorio de memoria e' parametrizado por V403_MEMORIA_DIR (padrao: o REAL; no ensaio, uma COPIA); o manifesto REGISTRA (so' informa, nao recusa) o estado da fila ao fechar: sha256 do memoria.py, do MEMORY.md e do PINO_MEMORY.json, se o pino confere com o indice e se a pausa do vigia esta ausente.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
import glob, hashlib, json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v403 as L
import textos_v403 as T
from guarda_p18_v403 import violacoes
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V403"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v403 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO), as MESMAS funcoes do quadro do artigo sobre o core SELADO do Nos; (2) o paragrafo NOVO da v403 (Caminho,
# Verdade e Vida), gerado dos registros selados e verificado contra o core e contra ESPERADOS (sem o 4,44; citacoes verbatim das falas do operador ou do kernel embutido; sem alegacao de seguranca criptografica); os do testemunho de dois (v399), da falsidade (v401) e da v402 SEGUEM COMO ESTAO e nao sao regenerados;
# sem passar nas verificacoes, RECUSA (rc 2) ANTES de escrever qualquer coisa
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    PAR_F, PAR_F_INFO = T.paragrafo_v403()   # (o handoff de textos_v403 o recebe como readme_paragrafo_v403)
except BaseException as e_:   # noqa: BLE001
    print("FECHAR RECUSADO: um dos paragrafos prontos do README e do site (o quadro O Teste da Unica Palavra, v397, ou o da v403: Caminho, Verdade e Vida) nao passou nas verificacoes (regra da ordem do 4,44; frase verbatim; numeros iguais aos do resultado pinado e aos de ESPERADOS; citacoes verbatim; sem alegacao de seguranca criptografica):", repr(e_)[:700]); sys.exit(2)
# o SIDECAR (arquivo NOVO da custodia, D5): a leitura ja' o conferiu (existe, JSON valido, selado, tres objetos com o SHA-256 dos arquivos do Nos); aqui so' o resumo que o manifesto e o handoff levam
if not (V["sidecar"]["ok"] is True and os.path.isfile(os.path.join(L.NOS, "um_absoluto_selo_acom.json"))):
    print("FECHAR RECUSADO: o sidecar um_absoluto_selo_acom.json nao esta selado ou nao existe no Nos:", V["sidecar"].get("erro")); sys.exit(2)
SC_INFO = {"arquivo": "um_absoluto_selo_acom.json", "sha256": V["sidecar"]["sha256"], "bytes": V["sidecar"]["bytes"], "veredito": V["sidecar"]["veredito"], "esquema": V["sidecar"]["esquema"], "recusas": V["sidecar"]["recusas"],
           "objetos": {n_: {"bytes": o_["bytes"], "sha256": o_["sha256"]} for n_, o_ in V["sidecar"]["objetos"].items()}}
NOS = L.NOS; WK = os.path.dirname(os.path.dirname(PK)); TOOLS = os.path.join(WK, "cadeia_de_selo")
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
UMEM = os.path.abspath(os.environ.get("V403_MEMORIA_DIR", "").strip() or MEM_REAL)   # v403 (fila da memoria): a pasta de memoria e' parametrizada por V403_MEMORIA_DIR (padrao: a REAL; no ensaio, uma COPIA)
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()
DIRS_B3 = os.path.join(PK, "bancada_B3"); DIRS_SERV = os.path.join(PK, "bancada_B3_servico")


def _j(p):
    return json.load(open(p, encoding="utf-8"))


# ---------------------------------------------------------------- 0. os tres recibos do B(3): sem eles, nao fecha
def recibos_b3():
    prob = []; out = {}
    # a pasta do aplicar e' nova a cada tentativa (bancada_B3, bancada_B3_2, ...); o ensaio (bancada_B3_ensaio_*) NAO conta
    ap = sorted(glob.glob(os.path.join(DIRS_B3, "RECIBO_SINCRONIZACAO_v403_*.json")) + glob.glob(os.path.join(PK, "bancada_B3_[0-9]*", "RECIBO_SINCRONIZACAO_v403_*.json")), key=os.path.getmtime)
    if not ap:
        prob.append("sem o RECIBO_SINCRONIZACAO_v403_*.json do 10-bis em %s (nem em bancada_B3_<n>)" % DIRS_B3)
    else:
        r = _j(ap[-1])
        if not (str(r.get("veredito") or "").startswith("REPINADA_B") and "__SALTO_" not in str(r.get("veredito") or "") and r.get("salto") in (None, {}) and r.get("modo") == "aplicar" and r.get("fase") == "pos_selo" and r.get("versao_alvo") == "v403"
                and (r.get("bateria_resultado") or {}).get("veredito") == "BATERIA_PASSA" and r.get("aplicacao")):
            prob.append("o recibo do 10-bis nao e' de uma aplicacao pos_selo v403 com a bateria passando: %s" % os.path.basename(ap[-1]))
        out["aplicar"] = {"path": ap[-1], "sha256": s64(open(ap[-1], "rb").read()), "veredito": r.get("veredito"), "manifesto_novo_sha256": (r.get("manifesto_novo") or {}).get("sha256"),
                          "evento": ((r.get("evento_c1") or {}).get("evento")), "bateria": (r.get("bateria_resultado") or {}).get("veredito")}
    pp = os.path.join(DIRS_SERV, "RECIBO_PARADA_v403.json"); rp = os.path.join(DIRS_SERV, "RECIBO_RELIGAMENTO_v403.json")
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
        if not (vs == "v403" and msha and esperado and msha == esperado and (d.get("pid") or d.get("PID")) and (d.get("hora") or d.get("quando"))):
            prob.append("o recibo do religamento nao traz versao servida v403, o sha do manifesto novo do recibo do 10-bis, pid e hora")
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
        raw = open(p, "rb").read(); bk = p + ".bak_" + ST + "_f403"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp_f403_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


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
assert os.path.exists(base) and s16(base) == V["base16"], "o backup da base (APLICADO_AO_CANONICO) nao e' a v402 selada: " + base
print("(3) diffs")
exe = shutil.which("diff")
if exe:
    r = subprocess.run([exe, "-U", "2", "--label", "um.py v402 %s" % V["base16"], "--label", "um.py v403 %s" % V["s16"], base, um], capture_output=True)
    assert r.returncode == 1, "diff rc=%s: %s" % (r.returncode, r.stderr[:200])
    dd = r.stdout
else:
    import difflib
    a = open(base, "r", encoding="utf-8", newline="").read().splitlines(); b = open(um, "r", encoding="utf-8", newline="").read().splitlines()
    dd = ("\n".join(difflib.unified_diff(a, b, "um.py v402 %s" % V["base16"], "um.py v403 %s" % V["s16"], lineterm="", n=2)) + "\n").encode("utf-8")
grava(os.path.join(PK, "DIFF_v402_v403.diff"), dd)
import difflib
E0 = carregar_embutido(base); E1 = carregar_embutido(um)
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v402 (%s) -> v403 (%s)" % (V["base16"], V["s16"]), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, s64(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a_, b_ = E0[k].splitlines(), E1[k].splitlines(); d_ = list(difflib.unified_diff(a_, b_, "v402/" + k, "v403/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, s64(E0[k].encode())[:16], s64(E1[k].encode())[:16], sum(1 for l in d_ if l.startswith("+") and not l.startswith("+++")),
                                                         sum(1 for l in d_ if l.startswith("-") and not l.startswith("---"))))
    if k == "TGLExt.lean":
        out += ["      " + l for l in d_]
    else:
        out += ["      " + l[:200] for l in d_[:6]] + ["      ... (%d linhas de diff no total)" % len(d_)]
grava(os.path.join(PK, "DIFF_KERNEL_v403.txt"), ("\n".join(out) + "\n").encode("utf-8"))
assert len(novos) == V["n_pedras"] and not removidos, ("o kernel embutido: novos != pedras do registro ou arquivo removido", len(novos), V["n_pedras"], removidos)

# ---------------------------------------------------------------- (1) o manifesto de incorporacao
def fila_info():
    """O estado da FILA DA MEMORIA ao fechar (v403; SO' INFORMA, nao recusa): o memoria.py (sha16 e se e' o do PINO_MEMORIA_PY_v403.json), o MEMORY.md (sha256, bytes, linhas), o PINO_MEMORY.json (sha256 do indice, quem e quando pinou), se o pino CONFERE com o indice agora
    e se a fila\\PAUSA_VIGIA.json esta ausente. Tudo LIDO dos arquivos por script."""
    try:
        f_ = os.path.join(UMEM, "fila"); mp_ = os.path.join(f_, "memoria.py"); ix_ = os.path.join(UMEM, "MEMORY.md"); pn_ = os.path.join(f_, "PINO_MEMORY.json"); pp_ = os.path.join(PK, "PINO_MEMORIA_PY_v403.json")
        pino_ = _j(pn_) if os.path.isfile(pn_) else {}
        ixb_ = open(ix_, "rb").read() if os.path.isfile(ix_) else b""
        d_ = {"dir": UMEM, "memoria_py_sha16": s16(mp_) if os.path.isfile(mp_) else None, "memoria_py_igual_ao_pino_v403": (s16(mp_) == _j(pp_)["sha16"]) if (os.path.isfile(mp_) and os.path.isfile(pp_)) else None,
              "memory_md_sha256": s64(ixb_) if ixb_ else None, "memory_md_bytes": len(ixb_), "memory_md_linhas": ixb_.count(b"\n"), "pino_sha256": pino_.get("sha256"), "pino_por": pino_.get("por"), "pino_em": pino_.get("pinado_em"), "pino_via": pino_.get("via"),
              "pino_confere_com_o_indice": bool(ixb_) and pino_.get("sha256") == s64(ixb_), "pausa_do_vigia_ausente": not os.path.exists(os.path.join(f_, "PAUSA_VIGIA.json"))}
    except Exception as e_:   # noqa: BLE001
        d_ = {"erro": repr(e_)[:200]}
    return d_


FILA_INFO = fila_info()
print("(0) fila da memoria ao fechar:", json.dumps({k_: FILA_INFO.get(k_) for k_ in ("memory_md_linhas", "pino_confere_com_o_indice", "pausa_do_vigia_ausente", "memoria_py_igual_ao_pino_v403")}, ensure_ascii=False))
ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out", ".diff", ".md")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
ESP = _j(os.path.join(PK, "ESPERADOS_v403.json"))
pedras_nos = {rel: s16(os.path.join(NOS, "tgl_kernel", *rel.split("/"))) for rel in ESP["pedras_sha256"]}
# v403: o manifesto lista as fontes pinadas dos registros (insumos/: as tres pedras e a medida KH-N1); as falas ficam em insumos/cunhagens (indexadas no arquivo)
m = {"stamp": ST, "versao": "v403", "instalacao": os.path.basename(app), "base_v402": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": {"pedras_no_nos_sha16": pedras_nos, "escada": [V["escada_antes"], V["teor"]], "axiom_report_n": V["axiom_report_n"], "build_full_log_sha16": s16(os.path.join(PK, "kernel", "build_full.log")) if os.path.exists(os.path.join(PK, "kernel", "build_full.log")) else None,
                "kernel_recibo_sha16": s16(os.path.join(PK, "kernel", "KERNEL_RECIBO_v403.json")) if os.path.exists(os.path.join(PK, "kernel", "KERNEL_RECIBO_v403.json")) else None},
     "patches": V["patches"], "teoremas": V["teor"], "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"],
     "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v403": V["reg403"], "registros_v402": V["reg402_estado"], "registros_v401": V["reg401_estado"], "registros_v399": V["reg399"], "caminho": V["caminho"], "vida": V["vida"], "verdade_adendo": V["verdade_adendo"], "bandeiras_do_gate": V["gate"], "funcoes_v402_recriadas": V["fun402"], "pedras_v402_como_registro": V["pedras_v402"], "falsidade_v401": V["fal401"],
     "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, "readme_paragrafo_v403": {"sha16": hashlib.sha256(PAR_F.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_F_INFO}, "paragrafos_anteriores_seguem_como_estao": ["testemunho_de_dois_v399", "falsidade_v401", "ponte_queda_esperanca_v402"], "nota_ao_lado_do_paragrafo_v402_no_handoff": True, "fila_da_memoria": FILA_INFO, "sidecar_acom": SC_INFO, "troca_dita": V["troca_dita"], "pedras": V["pedras"], "varredura": V["varr"], "verbatins": V["verbatins"], "fundacao_v390": V["fd390"], "pilar": V["pilar"],
     "insumos_sha16": {f_: s16(os.path.join(PK, "insumos", f_)) for f_ in sorted(os.listdir(os.path.join(PK, "insumos"))) if os.path.isfile(os.path.join(PK, "insumos", f_))}, "b3": B3,
     "diffs": {"DIFF_v402_v403.diff": s16(os.path.join(PK, "DIFF_v402_v403.diff")), "DIFF_KERNEL_v403.txt": s16(os.path.join(PK, "DIFF_KERNEL_v403.txt"))},
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v403_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v403_incorporacao_manifesto.json"), mb)
# ---------------------------------------------------------------- (2) o arquivo
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "pacote": PK, "arquivos": {}, "copias": {}, "nao_copiado": {}}


def indexa(p):
    b = open(p, "rb").read(); arq["arquivos"][p] = {"bytes": len(b), "sha256": s64(b)}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f403"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
    arq["copias"][dst] = {"de": src, "bytes": len(b), "sha256": s64(b)}


print("(2) arquivo")
EXCL = (".pyc",)
for raiz, dirs, fs in os.walk(PK):
    dirs[:] = [d for d in dirs if not d.startswith(("dry_", "__pycache__", "pilar_anterior", "memoria_copia"))]   # (memoria_copia: a COPIA da memoria do ensaio da fila, descartavel; so' o JSON de evidencia entra)
    for f in fs:
        p = os.path.join(raiz, f)
        if f.endswith(EXCL) or ".bak_" in f or ".tmp" in f:
            continue
        indexa(p)
# pos_rito (e o conferidor) -> v403_selo
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out", ".txt")) or f in ("v403_incorporacao_manifesto.json", "DERIVACAO_v403.json", "HARNESS_TEXTOS_ENSAIO_v403.json", "HARNESS_FECHAR_SANDBOX_v403.json", "FILA_MEMORIA_ENSAIO_v403.json", "registro_mapa_v403.json", "NOTAS_DERIVACAO_v403.md")):
            continue
        copia(p, os.path.join(TOOLS, "v403_selo", os.path.relpath(p, HERE)))
# v403: o SIDECAR (arquivo NOVO da custodia, D5) e o SELO PRIMARIO, ao lado: copias de bytes em v403_selo (a segunda testemunha so' se confere com o selo; o selo nao pode conter o selo ACOM de si mesmo)
for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json"):
    copia(os.path.join(NOS, nm_), os.path.join(TOOLS, "v403_selo", nm_))
# kernel: a pasta kernel da cadeia (+ work\v403_kernel, se existir) e as pedras do Nos -> v403_kernel
for src in (os.path.join(PK, "kernel"), os.path.join(WK, "v403_kernel")):
    if os.path.isdir(src):
        for f in sorted(os.listdir(src)):
            p = os.path.join(src, f)
            if os.path.isfile(p):
                if os.path.getsize(p) > 5 * 1024 * 1024:
                    arq["nao_copiado"][p] = "%d B (> 5 MB; indexado por sha256)" % os.path.getsize(p); continue
                copia(p, os.path.join(TOOLS, "v403_kernel", ("" if src.startswith(PK) else "work_v403_kernel"), f))
for rel in ESP["pedras_sha256"]:
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v403_kernel", "pedras", rel.replace("/", "_")))
for rel in ("TGLExt.lean", "TGL/Audit.lean"):
    copia(os.path.join(NOS, "tgl_kernel", *rel.split("/")), os.path.join(TOOLS, "v403_kernel", "depois", rel.replace("/", "_")))
for f in ("DIFF_v402_v403.diff", "DIFF_KERNEL_v403.txt"):
    copia(os.path.join(PK, f), os.path.join(TOOLS, "v403_kernel", f))
grava(os.path.join(PK, "MANIFESTO_ARQUIVO_v403.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  indexados: %d; copiados: %d; nao copiados (ditos): %d" % (len(arq["arquivos"]), len(arq["copias"]), len(arq["nao_copiado"])))
# ---------------------------------------------------------------- (4) o handoff
ap_ = B3.get("aplicar") or {}
# o handoff da v403: o texto vive em textos_v403.handoff(V, k) (testavel pelo harness); aqui so' entram os campos dos recibos do B(n), lidos dos arquivos (nenhum numero digitado)
_k = {"readme_paragrafo": PAR, "readme_paragrafo_v403": PAR_F, "ap_nome": os.path.basename(ap_.get("path", "?")), "ap_sha": str(ap_.get("sha256"))[:16], "ap_ver": ap_.get("veredito"), "ap_evento": ap_.get("evento"), "ap_bat": ap_.get("bateria"),
      "par_sha": str((B3.get("parada") or {}).get("sha256"))[:16], "rel_sha": str((B3.get("religamento") or {}).get("sha256"))[:16], "rel_man": str((B3.get("religamento") or {}).get("manifesto_sha256"))[:16]}
doc = T.handoff(V, _k)
vv = violacoes(doc)
assert not vv, "a guarda de texto (P18) achou violacao(oes) no handoff: %r" % (vv[:3],)
print("(4) handoff")
grava(os.path.join(UMEM, "handoff-v403-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v403_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v403:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v403-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v403_CUSTODIA.md")))
