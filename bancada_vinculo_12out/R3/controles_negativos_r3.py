# -*- coding: utf-8 -*-
"""controles_negativos_r3.py (R3, 13/10/2026) -- roda o sandbox COMPLETO do vinculo em raiz curta (C:/t/vb*) e TODOS os controles negativos:
os 94 da R2 (C1-C7, A1-A13, T16, idempotencia; nomes mantidos, argumentos ajustados as flags novas da R3) e os NOVOS, um ou mais por achado
da re-auditoria da R2 (N1-N16), cada um com a recusa esperada e a prova de que nada foi gravado onde nao devia.
Sequencia (tudo dentro de <raiz>; a producao, o Nos e o livro de eventos real sao SO lidos):
  run 1a  pre_selo ensaio, Bancada b1 (manifesto pina o Nos REAL), Nos real v391 -- a bateria inteira (isolada: -E -P, cwd vazio)
  run 1b  pre_selo ensaio, Bancada b2 (manifesto pina nos/, copia do Nos v391) -- o recibo pre-selo que o B3 do sandbox encadeia
  decoy   pd/ = copia de b2 + o seu recibo pre-selo; pd_pristino/ e a copia de restauracao. "Producao" simulada EM PROCESSO: o modulo
          e importado e PRODUCAO, EVENTOS_QUADRO e servico_responde sao trocados (nunca a producao real; argumentos conferidos)
  controles ANTES do selo
  o "selo" do sandbox: nos/ recebe os bytes de nos_v392/ (um.py, selo, core e o manifesto do kernel sintetico)
  controles DEPOIS do selo (N1 do kernel, N2/N3/N4 no decoy de producao, N5, N10, N14, N16, e os da R2)
  run 2   pos_selo aplicar --sandbox em b2, com --evento-hash, --recibo-pre-selo-sha256 e --kernel-recibo-sha256 (contrato KERNEL_RECIBO_R3)
  depois: re-execucao (idempotencia), estado final de b2; as juncoes criadas aqui sao DESFEITAS (nunca seguidas)
Saida: R3/CONTROLES_NEGATIVOS_R3.json e <raiz>/s/*. uso: controles_negativos_r3.py <raiz curta C:/t/vb*>"""
import sys
sys.dont_write_bytecode = True
import contextlib, copy, datetime, hashlib, importlib.util, io, json, os, shutil, subprocess, time, zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
R2 = AQUI.parent / "R2"
RAIZ = Path(sys.argv[1]).resolve()
assert RAIZ.parent == Path("C:/t").resolve() and RAIZ.name.startswith("vb"), "raiz curta obrigatoria (C:/t/vb*)"
PY = sys.executable
SYNC = AQUI / "sincronizar_bancada.py"
BAT = R2 / "BATERIA_VINCULO.json"                 # a bateria R2, inalterada na R3 (pinada por sha)
GER = R2 / "gerar_canais_mcp.py"                  # inalterado na R3
DECL = AQUI.parent / "sandbox" / "CANAIS_v391_exemplo.json"
PROD = Path("C:/IALD/Bancada_Um")
NOS_REAL = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
EVENTOS_REAL = Path("C:/IALD/PROGRAMA_IALD/eventos.jsonl")
WORK = Path("C:/IALD/Central de Patentes/work")
B1, B2, NOS, NOS392, FX, S = RAIZ / "b1", RAIZ / "b2", RAIZ / "nos", RAIZ / "nos_v392", RAIZ / "fx", RAIZ / "s"
SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R3.json").read_text(encoding="utf-8"))
ELOS = SBM["fx"]["elos_de_ensaio"]
EV_SB = FX / "eventos_sandbox.jsonl"
K_OK = FX / "KERNEL_RECIBO_v392_SINTETICO_VALIDO.json"
TK_A = "TGL_PRO" + "VED"          # a palavra guardada, so montada em RAM (nunca escrita em disco por este arquivo)
TK_C = "CONF" + "IRMED"
S.mkdir(exist_ok=True)
T0 = time.time()
RES = []
JUNCOES = []


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha(p):
    return sha_b(Path(p).read_bytes())


def sha_teste(t):
    return sha_b(json.dumps(t, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def foto(raiz):
    """fotografia por sha256 de todos os arquivos de uma copia, SEM seguir juncao nem link (a juncao entra como marca)."""
    raiz, out = Path(raiz), {}

    def walk(d):
        with os.scandir(d) as it:
            for e in it:
                rel = os.path.relpath(e.path, raiz)
                if e.is_junction() or e.is_symlink():
                    out[rel] = "JUNCAO_OU_LINK"
                elif e.is_dir(follow_symlinks=False):
                    walk(e.path)
                elif e.is_file(follow_symlinks=False):
                    out[rel] = sha(e.path)
    if raiz.exists():
        walk(raiz)
    return out


def _pastas(raiz):
    """todas as pastas sob raiz, SEM descer em juncao nem link."""
    pilha = [Path(raiz)]
    while pilha:
        d = pilha.pop()
        yield d
        with os.scandir(d) as it:
            for e in it:
                if not (e.is_junction() or e.is_symlink()) and e.is_dir(follow_symlinks=False):
                    pilha.append(Path(e.path))


def tem_pycache(raiz):
    return any(d.name == "__pycache__" for d in _pastas(raiz))


def juncao(link, alvo):
    r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(alvo)], capture_output=True)   # bytes: a saida do cmd vem na pagina de codigo do console
    assert Path(link).is_junction(), (r.stdout + r.stderr).decode("utf-8", errors="replace")
    JUNCOES.append(Path(link))
    return Path(link)


def copiar_sem_juncao(src, dst):
    def ign(d, nomes):
        return [n for n in nomes if Path(d, n).is_junction() or Path(d, n).is_symlink()]
    shutil.copytree(src, dst, ignore=ign)
    return Path(dst)


def apagar_arvore(p):
    """apaga uma arvore do sandbox SEM seguir juncao: juncoes sao desfeitas (os.rmdir no link) antes do rmtree."""
    p = Path(p)
    if not p.exists() and not p.is_junction():
        return
    if p.is_junction() or p.is_symlink():
        os.rmdir(p)
        return
    for d in list(_pastas(p)):
        with os.scandir(d) as it:
            links = [Path(e.path) for e in it if e.is_junction() or (e.is_symlink() and e.is_dir())]
        for q in links:
            os.rmdir(q)
    shutil.rmtree(p)


def mini_bateria(nome, ids=("T01_IDENTIDADE", "T15_SONDAS", "T17_LEAN_KERNEL"), extra=(), mutar=None, manter_copias=True, escapar_token=False):
    """uma bateria derivada da R2 com o subconjunto de testes dado (+ extras), pinada por teste; devolve (path, sha256)."""
    b = json.loads(BAT.read_bytes())
    b["testes"] = [t for t in b["testes"] if t["id"] in ids] + list(extra)
    if not manter_copias:
        b["copias"] = []
    if mutar:
        mutar(b)
    b["testes_sha256"] = {t["id"]: sha_teste(t) for t in b["testes"]}
    b["versao_bateria"] = "VINCULO-13out-R3-controle-" + nome
    texto = json.dumps(b, ensure_ascii=False, indent=1)
    if escapar_token:   # N14: o token so por escape JSON (o arquivo nunca o contem literal; o JSON decodificado contem)
        texto = texto.replace(TK_C, "\\u0043" + TK_C[1:])
        assert TK_C not in texto
    p = FX / ("BT_%s.json" % nome)
    p.write_bytes(texto.encode("utf-8"))
    return p, sha(p)


def _pinar(p):
    p = Path(p)
    return dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size)


def _ult(stdout):
    ult = (stdout.strip().splitlines() or [""])[-1]
    try:
        return json.loads(ult)
    except ValueError:
        return dict(veredito=None, recusa=None, bruto=ult[:400])


def _registrar(d, ok):
    d["passa"] = ok
    RES.append(d)
    print(("PASSA" if ok else "FALHA"), d["controle"], "rc=%s" % d.get("rc"), str(d.get("recusa") or d.get("veredito") or d.get("bruto") or "")[:150], flush=True)
    return d


def run(nome, args, rc_esp, recusa_esp=None, bancada=None, saida=None, flags=("-B", "-X", "utf8"), sync=None, veredito_esp=None, extra_ok=None, nota="",
        env_extra=None):
    """roda o esboco num subprocesso; confere rc, codigo da recusa (prefixo), veredito e que a copia nao mudou (fotografia por sha256)."""
    saida = saida or (S / nome)
    cmd = [PY, *flags, str(sync or SYNC), "--saida", str(saida)] + [str(x) for x in args]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    env.update(env_extra or {})
    antes = foto(bancada) if bancada else None
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, env=env, stdin=subprocess.DEVNULL)
    depois = foto(bancada) if bancada else None
    j = _ult(r.stdout)
    if j.get("bruto") is not None:
        j["stderr"] = r.stderr[-800:]
    intocada = (antes == depois) if bancada else None
    ok = (r.returncode == rc_esp) and (recusa_esp is None or str(j.get("recusa") or "").startswith(recusa_esp)) \
        and (veredito_esp is None or str(j.get("veredito") or "").startswith(veredito_esp)) and (intocada in (True, None))
    extra = None
    if extra_ok is not None:
        try:
            extra = extra_ok(j, r)
        except Exception as exc:
            extra = "EXCECAO: %r" % (exc,)
        ok = ok and extra is True
    d = dict(controle=nome, nota=nota, nivel="subprocesso", comando=[str(x) for x in args], flags=list(flags), rc=r.returncode, rc_esperado=rc_esp,
             recusa=j.get("recusa"), recusa_esperada=recusa_esp, veredito=j.get("veredito"), veredito_esperado=veredito_esp, recibo=j.get("recibo"),
             recibo_sha256=j.get("recibo_sha256"), bancada_copia=str(bancada) if bancada else None, bancada_copia_intocada=intocada, prova_extra=extra)
    if not ok and j.get("bruto") is not None:
        d["bruto"] = j
    _registrar(d, ok)
    return d, j


def unit(nome, fn, recusa_esp=None, nota=""):
    """controle unitario: chama a funcao do modulo; recusa esperada por prefixo (ou None = tem de aceitar)."""
    try:
        r = fn()
        ok = recusa_esp is None
        d = dict(controle=nome, nota=nota, nivel="unitario", aceito=True, retorno=(r if isinstance(r, (dict, str, int, float, bool, type(None))) else str(r)),
                 recusa_esperada=recusa_esp)
    except MOD.Recusa as exc:
        ok = recusa_esp is not None and str(exc).startswith(recusa_esp)
        d = dict(controle=nome, nota=nota, nivel="unitario", aceito=False, recusa=str(exc)[:300], recusa_esperada=recusa_esp)
    return _registrar(d, ok)


def checar(nome, cond, nota="", **info):
    """controle unitario booleano (a condicao e a prova)."""
    try:
        ok = bool(cond())
    except Exception as exc:
        ok, info["excecao"] = False, repr(exc)
    return _registrar(dict(controle=nome, nota=nota, nivel="unitario", **info), ok)


def inproc(nome, argv, rc_esp, recusa_esp=None, veredito_esp=None, patches=None, bancada=None, extra_ok=None, nota=""):
    """roda main() EM PROCESSO com atributos do modulo trocados (decoy de producao, sonda do servico simulada, bateria instrumentada).
    Nenhum argumento pode apontar para a producao real nem para o Nos real; os atributos voltam no fim."""
    for x in argv:
        sx = str(x).lower()
        assert str(PROD).lower() not in sx and str(NOS_REAL).lower() not in sx, "decoy: argumento aponta a producao/Nos real: %s" % x
    patches = patches or {}
    antigos = {k: getattr(MOD, k) for k in patches}
    antes = foto(bancada) if bancada else None
    buf = io.StringIO()
    try:
        for k, v in patches.items():
            setattr(MOD, k, v)
        with contextlib.redirect_stdout(buf):
            rc = MOD.main([str(x) for x in argv])
    finally:
        for k, v in antigos.items():
            setattr(MOD, k, v)
    j = _ult(buf.getvalue())
    depois = foto(bancada) if bancada else None
    ok = (rc == rc_esp) and (recusa_esp is None or str(j.get("recusa") or "").startswith(recusa_esp)) \
        and (veredito_esp is None or str(j.get("veredito") or "").startswith(veredito_esp))
    if bancada and extra_ok is None:
        ok = ok and antes == depois
    extra = None
    if extra_ok is not None:
        try:
            extra = extra_ok(j, antes, depois)
        except Exception as exc:
            extra = "EXCECAO: %r" % (exc,)
        ok = ok and extra is True
    d = dict(controle=nome, nota=nota, nivel="em processo (decoy)", comando=[str(x) for x in argv], trocados=sorted(patches), rc=rc, rc_esperado=rc_esp,
             recusa=j.get("recusa"), recusa_esperada=recusa_esp, veredito=j.get("veredito"), veredito_esperado=veredito_esp, recibo=j.get("recibo"),
             recibo_sha256=j.get("recibo_sha256"), prova_extra=extra)
    _registrar(d, ok)
    return d, j


def testes(j):
    return {t["id"]: t for t in json.loads(Path(j["recibo"]).read_bytes())["bateria_resultado"]["testes"]}


def recibo_de(j):
    return json.loads(Path(j["recibo"]).read_bytes())


spec = importlib.util.spec_from_file_location("sync_r3", SYNC)
MOD = importlib.util.module_from_spec(spec)
sys.modules["sync_r3"] = MOD
spec.loader.exec_module(MOD)

PROD_LISTA_ANTES = sorted(os.listdir(PROD))
NOS_LISTA_ANTES = sorted(os.listdir(NOS_REAL))
EV_REAL_BYTES_ANTES = EVENTOS_REAL.read_bytes()   # o livro e VIVO (outras sessoes anotam): confere-se que so cresceu, nunca que ficou igual
EV_REAL_SHA_ANTES = sha_b(EV_REAL_BYTES_ANTES)
PROD_MAN_ANTES = sha(PROD / "canonical_contracts.json")


def isolado(rec, saida):
    """N5: todo teste executado rodou com -E -P logo apos o interpretador, ambiente sem PYTHON*, cwd numa pasta vazia nova sob --saida."""
    ex = [t for t in rec["bateria_resultado"]["testes"] if t.get("comando_executado")]
    return bool(ex) and all(t["comando_executado"][1:3] == ["-E", "-P"] and Path(t["cwd"]).parent == Path(saida) / "cwd_testes" for t in ex)


# ================================================================ run 1a e 1b (a bateria inteira, pre_selo, ensaio)
run("RUN_1a_pre_selo_b1_nos_real", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--modo", "ensaio", "--fase", "pre_selo"], 0,
    veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1, saida=S / "1a",
    extra_ok=lambda j, r: (lambda rec: rec["bateria_resultado"]["falha"] == 0 and rec["bateria_resultado"]["passa"] == 13 and
                           testes(j)["T16_DEPLOY_FIXTURE"]["resultado"] == "PASSA" and testes(j)["T12_T13_T14_ATRATOR"]["resultado"] == "PASSA" and
                           rec["nos"]["um_py"]["sha256"] == SBM["nos"]["um_py"]["sha256"] and rec["manifesto_anterior"]["pina_o_nos_real"] is True and
                           rec["nos"]["kernel"]["raiz_sha256"] == SBM["fx"]["kernel_v391"]["raiz_sha256"] and isolado(rec, S / "1a"))(recibo_de(j)),
    nota="etapa 1 da cadeia: os testes finais contra a v391 ainda canonica, Nos REAL, bateria inteira (T16 em raiz curta; T12-T14 pre-selo); R3: cada teste com -E -P, "
         "ambiente sem PYTHON* e cwd vazio novo; o recibo traz o kernel v391 lido do manifesto pinado pelo selo")
run("RUN_1b_pre_selo_b2_nos_copia", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--modo", "ensaio", "--fase", "pre_selo"], 0,
    veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B2, saida=S / "1b",
    extra_ok=lambda j, r: (lambda rec: rec["bateria_resultado"]["falha"] == 0 and rec["bateria_resultado"]["passa"] == 13 and rec["manifesto_anterior"]["pina_o_nos_real"] is False
                           and rec["manifesto_anterior"]["nos_alvo_e_o_pinado"] is True and rec["nos"]["kernel"]["impressao_formal"] == SBM["fx"]["kernel_v391"]["impressao_formal"]
                           and isolado(rec, S / "1b"))(recibo_de(j)),
    nota="o mesmo ensaio contra b2 (manifesto pina a copia do Nos): e este recibo que o B3 do sandbox encadeia por hash (e o kernel ANTES que o T17 cruza)")
R1A = sorted((S / "1a").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
R1B = sorted((S / "1b").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
BAT_SHA = sha(BAT)
K_OK_SHA = sha(K_OK)
bt_min, bt_min_sha = mini_bateria("minima_pos_selo")
bt_min_pre, bt_min_pre_sha = mini_bateria("minima_pre_selo", ids=("T01_IDENTIDADE", "T15_SONDAS"))

# ================================================================ o decoy de producao (pd/), montado ANTES do selo
PD, PD_PRIST = RAIZ / "pd", RAIZ / "pd_pristino"
shutil.copytree(B2, PD)
run("N0_decoy_pre_selo_ensaio", ["--bancada", PD, "--nos", NOS, "--versao", "v391", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--modo", "ensaio",
                                 "--fase", "pre_selo"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=PD, saida=S / "pd_pre",
    nota="montagem do decoy: pd/ e uma copia de b2 (pina nos/); o seu recibo pre-selo (T01, T15) e o que o B3 do decoy exige")
R_PD = sorted((S / "pd_pre").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
shutil.copytree(PD, PD_PRIST)


def decoy_reset():
    apagar_arvore(PD)
    shutil.copytree(PD_PRIST, PD)


def sonda_seq(seq):
    estado = {"i": 0}

    def f(porta=None):
        i = estado["i"]
        estado["i"] += 1
        return seq[i] if i < len(seq) else seq[-1]
    return f


def decoy_args(saida, kernel=K_OK, kernel_sha="auto", pre=R_PD, pre_sha="auto", evento="decoy", evento_hash="auto", modo="aplicar", extra=()):
    a = ["--bancada", PD, "--producao", "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--modo", modo,
         "--fase", "pos_selo", "--saida", saida]
    if evento:
        a += ["--evento", ELOS[evento]["seq"]]
    if evento_hash == "auto" and evento:
        a += ["--evento-hash", ELOS[evento]["hash16"]]
    elif evento_hash not in ("auto", None):
        a += ["--evento-hash", evento_hash]
    if pre:
        a += ["--recibo-pre-selo", pre]
    if pre and pre_sha == "auto":
        a += ["--recibo-pre-selo-sha256", sha(pre)]
    elif pre_sha not in ("auto", None):
        a += ["--recibo-pre-selo-sha256", pre_sha]
    if kernel:
        a += ["--kernel-recibo", kernel]
    if kernel and kernel_sha == "auto":
        a += ["--kernel-recibo-sha256", sha(kernel)]
    elif kernel_sha not in ("auto", None):
        a += ["--kernel-recibo-sha256", kernel_sha]
    return a + list(extra)


def decoy(nome, rc_esp, recusa_esp=None, veredito_esp=None, sondas=(False,), patches_extra=None, extra_ok=None, nota="", **kw):
    decoy_reset()
    patches = dict(PRODUCAO=PD, EVENTOS_QUADRO=EV_SB, servico_responde=sonda_seq(list(sondas)))
    patches.update(patches_extra or {})
    return inproc(nome, decoy_args(S / nome, **kw), rc_esp, recusa_esp, veredito_esp, patches=patches, bancada=PD, extra_ok=extra_ok, nota=nota)


# ================================================================ controles ANTES do selo
# --- os 7 da R1
run("C1_versao_errada", ["--bancada", B1, "--versao", "v393", "--bateria", BAT, "--sem-bateria"], 2, "SELO_VERSAO_DIFERENTE", bancada=B1)
drift = RAIZ / "b2d"
shutil.copytree(B2, drift)
p = drift / "bancada" / "motor.py"
b = p.read_bytes()
p.write_bytes(b[:-1] + bytes([b[-1] ^ 1]))
run("C2_code_drift", ["--bancada", drift, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--forcar-regeracao"], 2, "CODE_DRIFT_NAO_E_SINCRONIZACAO", bancada=drift,
    nota="deriva de CODIGO numa copia (um byte de motor.py): nao e sincronizacao; --forcar-regeracao leva ao regenerar, onde a deriva e nomeada")
apagar_arvore(drift)
run("C3_aplicar_sem_evento", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar"], 2, "EVENTO_C1_AUSENTE", bancada=B2)
run("C4_evento_real_nao_nomeia", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--modo", "aplicar", "--evento", "1",
                                  "--recibo-pre-selo", R1B, "--recibo-pre-selo-sha256", sha(R1B), "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 2,
    "EVENTO_TIPO_INVALIDO", bancada=B2,
    nota="o evento seq 1 do quadro REAL (tipo criacao) nao nomeia a gravacao: recusado por tipo, nao por substring; o livro real e so lido (R3: com os pinos N1/N2)")
run("C5_nos_diferente_sem_sandbox", ["--bancada", B1, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "NOS_DIFERENTE_DO_PINADO", bancada=B1)
run("C6_producao_sem_flag", ["--bancada", PROD, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "PRODUCAO_SEM_FLAG")

# --- A2: identidade da Bancada por samefile, em todas as formas de caminho (nenhuma le ou grava a producao: a guarda recusa antes)
jprod = juncao(RAIZ / "jprod", PROD)
jb1 = juncao(RAIZ / "jb1", B1)
formas_prod = {
    "prefixo_longo": "\\\\?\\" + str(PROD), "unc_localhost": "\\\\localhost\\C$" + str(PROD)[2:], "unc_127": "\\\\127.0.0.1\\C$" + str(PROD)[2:],
    "unc_host": "\\\\%s\\C$%s" % (os.environ.get("COMPUTERNAME", "localhost"), str(PROD)[2:]), "prefixo_unc": "\\\\?\\UNC\\localhost\\C$" + str(PROD)[2:],
    "prefixo_ponto": "\\\\.\\" + str(PROD), "nome_83": str(Path("C:/IALD/BANCAD~1")), "minusculas": str(PROD).lower(), "barras_normais": str(PROD).replace("\\", "/"),
    "barra_dupla_e_ponto": str(PROD).replace("\\Bancada", "\\\\Bancada") + "\\.", "unc_barras_normais": "//localhost/C$" + str(PROD)[2:].replace("\\", "/"),
    "juncao": str(jprod), "relativo_pelo_cwd": os.path.relpath(PROD, os.getcwd()),
}
for k, f in formas_prod.items():
    run("A2_producao_%s" % k, ["--bancada", f, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "PRODUCAO_SEM_FLAG",
        extra_ok=lambda j, r: j.get("recibo") is None, nota="forma %r: reconhecida como a producao por identidade; nada gravado (nem recibo)" % f)
run("A2_producao_prefixo_longo_com_producao_e_sandbox", ["--bancada", "\\\\?\\" + str(PROD), "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--producao", "--sandbox"], 2, "SANDBOX_NA_PRODUCAO")
run("A2_unc_nao_local", ["--bancada", "\\\\10.255.255.1\\C$\\IALD\\Bancada_Um", "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "CAMINHO_UNC_NAO_LOCAL")
run("A2_B1_replay_prefixo_sandbox_aplicar_b1", ["--bancada", "\\\\?\\" + str(B1), "--versao", "v391", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar",
                                               "--fase", "pos_selo", "--evento", "SANDBOX:B1 prefixo"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1,
    nota="o ataque B1 (ALTA) da auditoria R1: na R1 gravou o manifesto B3 na copia; desde a R2 a forma do caminho e normalizada e --sandbox e recusado porque o manifesto pina o Nos real")
run("A2_B1_replay_juncao_sandbox_aplicar_b1", ["--bancada", jb1, "--versao", "v391", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar",
                                              "--fase", "pos_selo", "--evento", "SANDBOX:B1 juncao"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1)
run("A2_sandbox_em_copia_que_pina_o_nos_real_ensaio", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--sandbox"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1)
run("A2_producao_flag_em_copia_e_aceito_sem_efeito", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--producao"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1,
    nota="--producao numa copia nao e erro (A12 da auditoria R1): o recibo diz producao=false", extra_ok=lambda j, r: recibo_de(j)["producao"] is False)
# --- N13: Volume{GUID}, GLOBALROOT e \??\ -- recusa por REGRA explicita (na R2, por acidente)
GUID = "{12345678-1234-1234-1234-123456789abc}"
for k, f, esp in (("volume_guid_prefixo_longo", "\\\\?\\Volume" + GUID + "\\IALD\\Bancada_Um", "CAMINHO_VOLUME_GUID_NAO_ADMITIDO"),
                  ("volume_guid_prefixo_ponto", "\\\\.\\Volume" + GUID + "\\IALD\\Bancada_Um", "CAMINHO_VOLUME_GUID_NAO_ADMITIDO"),
                  ("globalroot", "\\\\?\\GLOBALROOT\\Device\\HarddiskVolume3\\IALD\\Bancada_Um", "CAMINHO_DISPOSITIVO_NAO_ADMITIDO"),
                  ("pipe", "\\\\.\\pipe\\bancada", "CAMINHO_DISPOSITIVO_NAO_ADMITIDO")):
    run("N13_bancada_%s" % k, ["--bancada", f, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, esp,
        extra_ok=lambda j, r: j.get("recibo") is None, nota="N13: a forma %r e recusada por regra explicita, antes de qualquer leitura; nada gravado" % f)
run("N13_saida_volume_guid", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "CAMINHO_VOLUME_GUID_NAO_ADMITIDO", bancada=B1,
    saida="\\\\?\\Volume" + GUID + "\\t\\x", extra_ok=lambda j, r: j.get("recibo") is None)
run("N13_producao_prefixo_nt", ["--bancada", "\\??\\" + str(PROD), "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "PRODUCAO_SEM_FLAG",
    extra_ok=lambda j, r: j.get("recibo") is None, nota="N13: o prefixo NT \\??\\ com letra de disco e normalizado e reconhecido como a producao")

# --- A5 e N8: --saida so dentro das raizes ESTREITAS; nunca sob a producao, o Nos, a --bancada, a pasta do esboco ou das fontes da bateria
def _nada_criado(caminho):
    return lambda j, r: (not Path(caminho).exists()) and j.get("recibo") is None


for k, sd, esp in (("na_producao", PROD / "estado" / "saida_A5", "SAIDA_NA_PRODUCAO"), ("no_nos", NOS_REAL / "saida_A5", "SAIDA_NO_NOS"),
                   ("dentro_da_bancada", B1 / "estado" / "saida_A5", "SAIDA_DENTRO_DA_BANCADA"),
                   ("fora_das_raizes", Path(os.environ.get("TEMP", "C:/Users")) / "saida_A5_R3", "SAIDA_FORA_DAS_RAIZES_PERMITIDAS"),
                   ("na_producao_por_prefixo", "\\\\?\\" + str(PROD / "estado" / "saida_A5b"), "SAIDA_NA_PRODUCAO"), ("na_producao_por_juncao", jprod / "estado" / "saida_A5c", "SAIDA_NA_PRODUCAO")):
    run("A5_saida_%s" % k, ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, esp, bancada=B1, saida=sd,
        extra_ok=_nada_criado(str(sd).replace("\\\\?\\", "")), nota="a pasta %s nao pode nascer" % sd)
for k, sd, esp, ver in (("C_t_fora_do_vb", Path("C:/t/n8_fora_do_vb"), "SAIDA_FORA_DAS_RAIZES_PERMITIDAS", "v391"),
                        ("C_t_raiz", Path("C:/t"), "SAIDA_FORA_DAS_RAIZES_PERMITIDAS", "v391"),
                        ("work_outra_pasta", WORK / "n8_outra_pasta_R3", "SAIDA_FORA_DAS_RAIZES_PERMITIDAS", "v391"),
                        ("cadeia_de_outra_versao", WORK / "cadeia_de_selo" / "v393" / "n8_R3", "SAIDA_FORA_DAS_RAIZES_PERMITIDAS", "v391"),
                        ("pasta_das_fontes_da_bateria", WORK / "bancada_vinculo_12out" / "bateria" / "n8_R3", "SAIDA_NA_PASTA_DE_FONTES", "v391"),
                        ("pasta_da_bateria_R2", R2 / "n8_R3", "SAIDA_NA_PASTA_DE_FONTES", "v391"),
                        ("pasta_do_esboco_R3", AQUI / "n8_R3", "SAIDA_NA_PASTA_DE_FONTES", "v391"),
                        ("pasta_de_fonte_no_tunel", Path(json.loads(BAT.read_bytes())["testes"][1]["fontes"][0]["path"]).parent / "n8_R3", "SAIDA_NA_PASTA_DE_FONTES", "v391")):
    run("N8_saida_%s" % k, ["--bancada", B1, "--versao", ver, "--bateria", BAT, "--sem-bateria"], 2, esp, bancada=B1, saida=sd,
        extra_ok=_nada_criado(sd) if sd != Path("C:/t") else (lambda j, r: j.get("recibo") is None),
        nota="N8 [INPUT da gerencia]: --saida %s recusada antes de qualquer gravacao (nada nasce)" % sd)
run("N8_versao_invalida_nao_compoe_caminho", ["--bancada", B1, "--versao", "..\\v391", "--bateria", BAT, "--sem-bateria"], 2, "VERSAO_INVALIDA", bancada=B1,
    extra_ok=lambda j, r: j.get("recibo") is None, nota="a versao entra no caminho das raizes (cadeia_de_selo/vNNN): so vNNN e admitida")
for k, sd, ver, aceita in (("cadeia_de_selo_da_versao", WORK / "cadeia_de_selo" / "v391" / "x", "v391", True), ("vNNN_bateria", WORK / "v391_bateria" / "x", "v391", True),
                           ("bancada_vinculo", WORK / "bancada_vinculo_12out" / "R3_saida_hipotetica", "v391", True), ("sandbox_vb", Path("C:/t/vb9/x"), "v391", True),
                           ("sandbox_outro", Path("C:/t/mo2/x"), "v391", False), ("cadeia_de_selo_outra_versao", WORK / "cadeia_de_selo" / "v391" / "x", "v392", False)):
    unit("N8_predicado_%s" % k, (lambda sd=sd, ver=ver: MOD.guardar_saida(MOD.caminho_canonico(sd), B1, NOS, ver, BAT)), None if aceita else "SAIDA_",
         nota="N8: o predicado da guarda, avaliado sem gravar (%s, versao %s): %s" % (sd, ver, "admitida" if aceita else "recusada"))
for k, sd, ver, fase, aceita in (("pre_selo_v391_em_v392_bateria", WORK / "v392_bateria" / "pre_selo", "v391", "pre_selo", True),
                                 ("pos_selo_v391_em_v392_bateria", WORK / "v392_bateria" / "pre_selo", "v391", "pos_selo", False),
                                 ("pre_selo_v391_em_cadeia_v392", WORK / "cadeia_de_selo" / "v392" / "x", "v391", "pre_selo", True),
                                 ("pre_selo_v391_em_v391_bateria", WORK / "v391_bateria" / "x", "v391", "pre_selo", False)):
    unit("N8_predicado_%s" % k, (lambda sd=sd, ver=ver, fase=fase: MOD.guardar_saida(MOD.caminho_canonico(sd), B1, NOS, ver, BAT, fase)), None if aceita else "SAIDA_",
         nota="N8: a raiz da cadeia e a da versao que esta sendo selada (a seguinte na fase pre_selo): %s, versao %s, fase %s: %s" % (sd, ver, fase, "admitida" if aceita else "recusada"))

# --- A7: bateria pinada por sha256 (arquivo e teste) e conjunto minimo em aplicar
bt_triv, bt_triv_sha = mini_bateria("trivial", ids=(), extra=[dict(id="T00_TRIVIAL", teste="um teste trivial", fontes=[_pinar(SYNC)],
                                                                   comando=["{py}", "-c", "print('ok')"], cwd="{raiz}", verificacao=dict(tipo="exit0"), fases=["pre_selo", "pos_selo"],
                                                                   obrigatorio_em=["ensaio", "aplicar"], timeout_s=60)], manter_copias=False)
run("A7_bateria_trivial_em_aplicar", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_triv, "--bateria-sha256", bt_triv_sha, "--sandbox", "--modo", "aplicar",
                                      "--evento", "SANDBOX:A7"], 2, "BATERIA_MINIMA_AUSENTE", bancada=B2, nota="o ataque A7 da auditoria R1: na R1 um teste trivial bastava para gravar")
run("A7_bateria_sem_sha_em_aplicar", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--sandbox", "--modo", "aplicar", "--evento", "SANDBOX:A7"], 2, "BATERIA_SHA_AUSENTE", bancada=B2)
run("A7_bateria_sha_divergente", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--bateria-sha256", "0" * 64, "--sandbox", "--modo", "aplicar", "--evento", "SANDBOX:A7"], 2,
    "BATERIA_SHA_DIVERGE", bancada=B2)


def _mutar_timeout(b):
    b["testes"][0]["timeout_s"] = 1


bt_mut, bt_mut_sha = mini_bateria("teste_adulterado", mutar=_mutar_timeout)
bj = json.loads(bt_mut.read_bytes())
bj["testes"][0]["timeout_s"] = 2
bt_mut.write_bytes(json.dumps(bj, ensure_ascii=False, indent=1).encode("utf-8"))   # o teste muda DEPOIS do pino por teste
run("A7_teste_adulterado_apos_pino", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_mut, "--bateria-sha256", sha(bt_mut), "--sem-bateria"], 2, "BATERIA_TESTE_SHA_DIVERGE", bancada=B2)
bt_vinc, bt_vinc_sha = mini_bateria("marcador_vinculo", mutar=lambda b: b["testes"][0]["comando"].__setitem__(4, "{vinculo}/bateria/t01_identidade.py"))
run("A3_marcador_vinculo_proibido", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_vinc, "--bateria-sha256", bt_vinc_sha, "--sem-bateria"], 2, "MARCADOR_VINCULO_PROIBIDO", bancada=B2,
    nota="o ataque A8/A3 da auditoria R1: o comando que roda da pasta do esboco e recusado na carga da bateria")

# --- A8: mesma versao, hash diferente do um.py -> SELO_PROGRAMA_DIVERGE; reparo so em aplicar com evento nomeado
b1x = RAIZ / "b1x"
shutil.copytree(B1, b1x)
mx = json.loads((b1x / "canonical_contracts.json").read_bytes())
mx["canonical"]["script"]["sha256"] = "1" * 64
(b1x / "canonical_contracts.json").write_bytes(json.dumps(mx, ensure_ascii=False, indent=1).encode("utf-8"))
run("A8_mesma_versao_hash_diferente", ["--bancada", b1x, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "SELO_PROGRAMA_DIVERGE", bancada=b1x,
    nota="o ataque A5 da auditoria R1: manifesto v391 com outro sha do um.py; o disco tem a v391 real")
run("A8_reparo_em_ensaio_recusado", ["--bancada", b1x, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--reparo-de-pino"], 2, "REPARO_SO_EM_APLICAR", bancada=b1x)
apagar_arvore(b1x)
b2x = RAIZ / "b2x"
shutil.copytree(B2, b2x)
mx = json.loads((b2x / "canonical_contracts.json").read_bytes())
mx["canonical"]["script"]["sha256"] = "1" * 64
(b2x / "canonical_contracts.json").write_bytes(json.dumps(mx, ensure_ascii=False, indent=1).encode("utf-8"))
linhas = [l for l in EV_SB.read_text(encoding="utf-8").splitlines() if l.strip()]
ult = json.loads(linhas[-1])


def elo(prev, tipo, quem, dados):
    e = {"seq": prev["seq"] + 1, "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "tipo": tipo, "quem": quem, "dados": dados, "anterior": prev["hash"]}
    e["hash"] = sha_b(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8"))
    return e


nos_um_sha = sha(NOS / "um.py")
nos_selo_sha = sha(NOS / "um_absoluto_selo.json")
e_rep = elo(ult, "SINCRONIZACAO_BANCADA", "claude-c1", dict(versao="v391", bancada=str(b2x), acao="sincronizacao", um_py=nos_um_sha[:16], selo=nos_selo_sha[:16], reparo=True, nota="ENSAIO A8: reparo de pino nomeado"))
e_sem = elo(e_rep, "SINCRONIZACAO_BANCADA", "claude-c1", dict(versao="v391", bancada=str(b2x), acao="sincronizacao", um_py=nos_um_sha[:16], selo=nos_selo_sha[:16], nota="ENSAIO A8: evento SEM reparo"))
ev_rep = FX / "eventos_sandbox_reparo.jsonl"
ev_rep.write_text("\n".join(linhas + [json.dumps(e_rep, ensure_ascii=False), json.dumps(e_sem, ensure_ascii=False)]) + "\n", encoding="utf-8")
run("A8_reparo_com_evento_sem_dados_reparo", ["--bancada", b2x, "--nos", NOS, "--versao", "v391", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--sandbox", "--modo", "aplicar", "--fase", "pre_selo",
                                              "--reparo-de-pino", "--evento", str(e_sem["seq"]), "--evento-hash", e_sem["hash"][:16], "--eventos", ev_rep], 2, "EVENTO_NAO_AUTORIZA_REPARO", bancada=b2x)
d, j = run("A8_reparo_nomeado_em_evento_aplica", ["--bancada", b2x, "--nos", NOS, "--versao", "v391", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--sandbox", "--modo", "aplicar", "--fase", "pre_selo",
                                                 "--reparo-de-pino", "--evento", str(e_rep["seq"]), "--evento-hash", e_rep["hash"][:16], "--eventos", ev_rep], 0, veredito_esp="REPINADA_B3__APLICADA",
           extra_ok=lambda j, r: json.loads((b2x / "canonical_contracts.json").read_bytes())["canonical"]["script"]["sha256"] == nos_um_sha and
                                 recibo_de(j)["reparo_de_pino_autorizado_por"] == e_rep["seq"],
           nota="o unico caminho admitido para a mesma versao com outro hash: --reparo-de-pino em aplicar, evento c1 encadeado com dados.reparo=true (R3: com --evento-hash)")
apagar_arvore(b2x)

# --- N15 [INPUT da gerencia]: mesma versao, MESMO um.py, selo DIFERENTE -> SEAL_CHANGED_SAME_VERSION, salvo --reparo-de-pino com evento
NSM = FX / "nos_selo_mudado"
NSM.mkdir()
for f in ("um.py", "um_absoluto.json", "tgl_kernel_proof_manifest.json"):
    shutil.copyfile(NOS / f, NSM / f)
sj = json.loads((NOS / "um_absoluto_selo.json").read_bytes())
sj["RITO_REFEITO_SINTETICO_N15"] = "fixture R3: o mesmo um.py v391 com um selo de bytes diferentes (o rito refeito); nao e selo do rito"
(NSM / "um_absoluto_selo.json").write_bytes(json.dumps(sj, ensure_ascii=False, indent=1).encode("utf-8"))
nsm_selo_sha = sha(NSM / "um_absoluto_selo.json")
run("N15_selo_diferente_mesma_versao_ensaio", ["--bancada", B2, "--nos", NSM, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--sandbox"], 2, "SEAL_CHANGED_SAME_VERSION", bancada=B2,
    nota="N15: a R2 re-pinava a mesma versao so pelo hash do selo (REPINADA_B3, rc 0); a R3 recusa")
b2r = RAIZ / "b2r"
shutil.copytree(B2, b2r)
e15 = elo(ult, "SINCRONIZACAO_BANCADA", "claude-c1", dict(versao="v391", bancada=str(b2r), acao="sincronizacao", um_py=nos_um_sha[:16], selo=nsm_selo_sha[:16], reparo=True,
                                                         nota="ENSAIO N15: re-pino do selo da mesma versao, nomeado"))
e15s = elo(e15, "SINCRONIZACAO_BANCADA", "claude-c1", dict(versao="v391", bancada=str(b2r), acao="sincronizacao", um_py=nos_um_sha[:16], selo=nsm_selo_sha[:16],
                                                          nota="ENSAIO N15: evento sem reparo"))
ev15 = FX / "eventos_sandbox_n15.jsonl"
ev15.write_text("\n".join(linhas + [json.dumps(e15, ensure_ascii=False), json.dumps(e15s, ensure_ascii=False)]) + "\n", encoding="utf-8")
run("N15_selo_diferente_aplicar_sem_reparo", ["--bancada", b2r, "--nos", NSM, "--versao", "v391", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
                                              "--fase", "pos_selo", "--evento", str(e15s["seq"]), "--evento-hash", e15s["hash"][:16], "--eventos", ev15], 2, "SEAL_CHANGED_SAME_VERSION", bancada=b2r)
run("N15_selo_diferente_reparo_nomeado_aplica", ["--bancada", b2r, "--nos", NSM, "--versao", "v391", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--sandbox", "--modo", "aplicar",
                                                 "--fase", "pre_selo", "--reparo-de-pino", "--evento", str(e15["seq"]), "--evento-hash", e15["hash"][:16], "--eventos", ev15], 0,
    veredito_esp="REPINADA_B3__APLICADA",
    extra_ok=lambda j, r: json.loads((b2r / "canonical_contracts.json").read_bytes())["canonical"]["seal"]["sha256"] == nsm_selo_sha and recibo_de(j)["reparo_de_pino_autorizado_por"] == e15["seq"],
    nota="o caminho admitido: --reparo-de-pino em aplicar com evento c1 encadeado (dados.reparo=true) que nomeia o selo novo")
apagar_arvore(b2r)

# --- A9: sem -B, nenhum __pycache__ nasce na Bancada-copia
run("A9_sem_B_nenhum_pycache", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1, flags=("-X", "utf8"),
    extra_ok=lambda j, r: not tem_pycache(B1) and recibo_de(j)["python_dont_write_bytecode"] is True,
    nota="o ataque B3 da auditoria R1: na R1 nascia bancada/__pycache__/canonical.*.pyc; desde a R2 sys.dont_write_bytecode=True no topo")

# --- A10 e N9: traversal e nomes reservados em code[].path e em copias[].para
b1t = RAIZ / "b1t"
shutil.copytree(B1, b1t)
fora = RAIZ / "fora"
fora.mkdir(exist_ok=True)
evil = b"# evil\n"
(fora / "evil.py").write_bytes(evil)
mt = json.loads((b1t / "canonical_contracts.json").read_bytes())
mt["code"].append(dict(path="..\\fora\\evil.py", bytes=len(evil), sha256=sha_b(evil)))
(b1t / "canonical_contracts.json").write_bytes(json.dumps(mt, ensure_ascii=False, indent=1).encode("utf-8"))
run("A10_traversal_em_code_path", ["--bancada", b1t, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--forcar-regeracao"], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=b1t,
    extra_ok=lambda j, r: not (S / "A10_traversal_em_code_path" / "raiz" / "candidate").exists() and not (S / "fora" / "evil.py").exists() and not (S / "A10_traversal_em_code_path" / "fora").exists(),
    nota="o ataque A1 da auditoria R1: code[].path com '..' escapava de --saida no staging")
run("A10_traversal_em_code_path_ja_sincronizada", ["--bancada", b1t, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=b1t)
apagar_arvore(b1t)
bt_cop, bt_cop_sha = mini_bateria("copia_traversal", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["copias"].__setitem__(0, dict(b["copias"][0], para="..\\x_A10.py")))
run("A10_traversal_em_copias_para", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_cop, "--bateria-sha256", bt_cop_sha], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=B2,
    extra_ok=lambda j, r: not (S / "x_A10.py").exists(), nota="o ataque A9 da auditoria R1: copias[].para com '..' saia de --saida")
bt_abs, bt_abs_sha = mini_bateria("copia_absoluta", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["copias"].__setitem__(0, dict(b["copias"][0], para=str(RAIZ / "fora" / "x_abs_A10.py"))))
run("A10_copia_absoluta", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_abs, "--bateria-sha256", bt_abs_sha], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=B2,
    extra_ok=lambda j, r: not (RAIZ / "fora" / "x_abs_A10.py").exists())
bt_res, bt_res_sha = mini_bateria("copia_nome_reservado", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["copias"].__setitem__(0, dict(b["copias"][0], para="tests_core/aux.py")))
run("N9_nome_reservado_em_copias_para", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_res, "--bateria-sha256", bt_res_sha], 2, "CAMINHO_NOME_RESERVADO", bancada=B2,
    extra_ok=lambda j, r: not any(n.lower().startswith("aux") for n in (os.listdir(S / "N9_nome_reservado_em_copias_para" / "raiz" / "tests_core")
                                                                       if (S / "N9_nome_reservado_em_copias_para" / "raiz" / "tests_core").exists() else [])),
    nota="N9: copias[].para = tests_core/aux.py (nome reservado) recusado; na R2 nascia como arquivo")
for k, rel, esp in (("CON", "CON", "CAMINHO_NOME_RESERVADO"), ("aux_txt", "x/aux.txt", "CAMINHO_NOME_RESERVADO"), ("prn_minusculo", "prn", "CAMINHO_NOME_RESERVADO"),
                    ("COM1_txt", "COM1.txt", "CAMINHO_NOME_RESERVADO"), ("NUL_json", "a/NUL.json", "CAMINHO_NOME_RESERVADO"), ("LPT9", "LPT9", "CAMINHO_NOME_RESERVADO"),
                    ("COM_sobrescrito", "COM\u00b9", "CAMINHO_NOME_RESERVADO"), ("CON_espaco", "CON .txt", "CAMINHO_NOME_RESERVADO"),
                    ("cauda_ponto", "x.py.", "CAMINHO_CAUDA_INVALIDA"), ("cauda_espaco", "x.py ", "CAMINHO_CAUDA_INVALIDA"), ("caractere_coringa", "x*.py", "CAMINHO_CARACTERE_INVALIDO"),
                    ("nome_comum_aceito", "bancada/console_py.py", None)):
    unit("N9_relativo_seguro_%s" % k, (lambda rel=rel: str(MOD.relativo_seguro(rel, FX / "n9_raiz_inexistente"))), esp,
         nota="N9: relativo_seguro(%r) -- avaliado sem gravar" % rel)

# --- A11 (unitario): UM_VERSION unica na coluna 0; alpha e UM_VERSION sem reatribuicao indentada
import math


def nos_minusculo(nome, texto, manifesto=None, pino_manifesto=None):
    d = FX / ("nos_" + nome)
    d.mkdir(exist_ok=True)
    um = texto.encode("utf-8")
    alpha = 7.2973525693e-3
    core = json.dumps(dict(core=dict(beta=alpha * math.sqrt(math.e), qg_closure_verdict="ENSAIO"))).encode("utf-8")
    pinos = {"um.py": sha_b(um), "um_absoluto.json": sha_b(core)}
    if manifesto is not None:
        (d / "tgl_kernel_proof_manifest.json").write_bytes(manifesto)
        pinos["tgl_kernel_proof_manifest.json"] = pino_manifesto or sha_b(manifesto)
    selo = json.dumps(dict(um_version="v999", sha256=pinos)).encode("utf-8")
    (d / "um.py").write_bytes(um)
    (d / "um_absoluto_selo.json").write_bytes(selo)
    (d / "um_absoluto.json").write_bytes(core)
    return d


BASE = 'UM_VERSION = "v999"\nALPHA_FINE_CODATA_2018 = 7.2973525693e-3\nx = 1\n'
unit("A11_nos_minusculo_limpo_aceito", lambda: MOD.ler_nos(nos_minusculo("limpo", BASE), "v999")["UM_VERSION"], None, nota="fixture minima: uma linha de cada na coluna 0 -> aceito")
unit("A11_segunda_UM_VERSION_coluna_0", lambda: MOD.ler_nos(nos_minusculo("v_dup", BASE + 'UM_VERSION = "v998"\n'), "v999"), "UM_VERSION_LINHA_NAO_UNICA")
unit("A11_alpha_reatribuido_indentado", lambda: MOD.ler_nos(nos_minusculo("a_ind", BASE + 'def f():\n    ALPHA_FINE_CODATA_2018 = 0.5\n'), "v999"), "ALPHA_REATRIBUIDA_INDENTADA")
unit("A11_UM_VERSION_reatribuida_indentada", lambda: MOD.ler_nos(nos_minusculo("v_ind", BASE + 'if x:\n    UM_VERSION = "v998"\n'), "v999"), "UM_VERSION_REATRIBUIDA_INDENTADA")
unit("A11_alpha_duplicado_coluna_0", lambda: MOD.ler_nos(nos_minusculo("a_dup", BASE + 'ALPHA_FINE_CODATA_2018=0.5\n'), "v999"), "ALPHA_LINHA_NAO_UNICA")
unit("A11_comparacao_nao_e_atribuicao", lambda: MOD.ler_nos(nos_minusculo("cmp", BASE + 'if x:\n    assert ALPHA_FINE_CODATA_2018 == 7.2973525693e-3\n'), "v999")["UM_VERSION"], None,
     nota="'==' nao e reatribuicao: aceito")
unit("N1_ler_nos_manifesto_do_kernel_nao_pinado_pelo_selo", lambda: MOD.ler_nos(nos_minusculo("km_pino", BASE, b'{"formal_files_sha256": {}}', "a" * 64), "v999"),
     "SELO_NAO_PINA_O_MANIFESTO_DO_KERNEL_DO_DISCO", nota="N1: o manifesto do kernel em disco nao e o que o selo pina -> ler_nos recusa")
unit("N1_ler_nos_manifesto_do_kernel_pinado_aceito", lambda: MOD.ler_nos(nos_minusculo("km_ok", BASE, b'{"formal_files_sha256": {"TGLExt.lean": "' + b"b" * 64 + b'"}}'), "v999")["kernel"]["raiz_sha256"],
     None, nota="N1: o manifesto pinado e lido; o recibo guarda a raiz, o Audit e a impressao formal")

# --- A4, N6, N11 (unitario): o evento pela cadeia de hash, o hash do elo por flag, chaves fechadas, negacao normalizada
NI = dict(um_py=dict(sha256=sha(NOS392 / "um.py")), selo=dict(sha256=sha(NOS392 / "um_absoluto_selo.json")))
H = lambda k: ELOS[k]["hash16"]
unit("A4_evento_valido_encadeado_aceito", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("valido"))["hash"][:16], None,
     nota="elo valido do livro de ensaio: encadeado, c1, tipo certo, campos por JSON, hash do elo conferido (N6) -> aceito")
unit("A4_F1_forjado_sem_cadeia", lambda: MOD.verificar_evento("90001", "v392", B2, True, NI, False, FX / "eventos_forjado_sem_cadeia.jsonl", "00" * 8), "EVENTOS_CADEIA_QUEBRADA")
unit("A4_F6_seq_duplicado_encadeado", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, FX / "eventos_forjado_seq_duplicado.jsonl", H("valido")), "EVENTO_SEQ_DUPLICADO")
unit("A4_F2_outra_sessao", lambda: MOD.verificar_evento(str(ELOS["outra_sessao"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("outra_sessao")), "EVENTO_NAO_E_DA_C1")
unit("A4_F3_texto_que_nega", lambda: MOD.verificar_evento(str(ELOS["negacao"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("negacao")), "EVENTO_COM_NEGACAO")
unit("A4_F4_hashes_de_outro_programa", lambda: MOD.verificar_evento(str(ELOS["outro_programa"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("outro_programa")), "EVENTO_NAO_NOMEIA_O_PROGRAMA")
unit("A4_F5_outra_versao", lambda: MOD.verificar_evento(str(ELOS["outra_versao"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("outra_versao")), "EVENTO_NAO_NOMEIA_A_VERSAO")
unit("A4_outra_bancada_por_identidade", lambda: MOD.verificar_evento(str(ELOS["outra_bancada"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("outra_bancada")), "EVENTO_NAO_NOMEIA_ESTA_BANCADA")
unit("A4_tipo_errado", lambda: MOD.verificar_evento(str(ELOS["tipo_errado"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("tipo_errado")), "EVENTO_TIPO_INVALIDO")
unit("A4_sem_acao", lambda: MOD.verificar_evento(str(ELOS["sem_acao"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("sem_acao")), "EVENTO_NAO_NOMEIA_A_SINCRONIZACAO")
unit("A4_F7_evento_real_706_nova_F06", lambda: MOD.verificar_evento("706", "v392", B2, True, NI, False, EV_SB), "EVENTO_TIPO_INVALIDO")
unit("A4_F8_sandbox_literal_fora_do_sandbox", lambda: MOD.verificar_evento("SANDBOX:x", "v392", B2, False, NI, False, EV_SB), "EVENTO_SANDBOX_FORA_DO_SANDBOX")
unit("A4_F10_seq_inexistente", lambda: MOD.verificar_evento("123456789", "v392", B2, True, NI, False, EV_SB), "EVENTO_NAO_ENCONTRADO")
unit("A4_F11_nao_numerico", lambda: MOD.verificar_evento("abc", "v392", B2, True, NI, False, EV_SB), "EVENTO_C1_INVALIDO")
ULT_REAL = json.loads([l for l in EVENTOS_REAL.read_text(encoding="utf-8").splitlines() if l.strip()][-1])["seq"]
unit("A4_livro_real_integro_seq_seguinte_nao_existe_nele", lambda: MOD.verificar_evento(str(ULT_REAL + 1), "v392", B2, True, NI, False, EVENTOS_REAL), "EVENTO_NAO_ENCONTRADO",
     nota="o livro REAL (so lido, %d elos no momento): a cadeia inteira e conferida e o seq seguinte nao existe nele" % ULT_REAL)
unit("A4_livro_real_ultimo_elo_nao_e_sincronizacao", lambda: MOD.verificar_evento(str(ULT_REAL), "v392", B2, True, NI, False, EVENTOS_REAL), "EVENTO_",
     nota="o ultimo elo real (seq %d) e de outro tipo/outra unidade: recusado por campo" % ULT_REAL)
run("A4_eventos_alternativo_fora_do_sandbox", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--eventos", EV_SB], 2, "EVENTOS_ALTERNATIVO_FORA_DO_SANDBOX", bancada=B2)
# N6
unit("N6_evento_hash_ausente", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, EV_SB, None), "EVENTO_HASH_AUSENTE",
     nota="N6 [INPUT da gerencia]: o elo valido sem --evento-hash e recusado (a cadeia passa o hash do elo que anotou)")
unit("N6_evento_hash_divergente", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, EV_SB, "0" * 16), "EVENTO_HASH_DIVERGE")
unit("N6_evento_hash_de_outro_elo", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("outra_sessao")), "EVENTO_HASH_DIVERGE")
unit("N6_evento_hash_invalido", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, EV_SB, "xyz"), "EVENTO_HASH_INVALIDO")
unit("N6_evento_hash_curto", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("valido")[:12]), "EVENTO_HASH_INVALIDO",
     nota="menos de 16 hex nao vale")
checar("N6_autoria_declarada_como_convencao", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, EV_SB, H("valido"))["autoria"].startswith("convencao"),
       nota="N6: o retorno diz, por escrito, que quem=claude-c1 e convencao do quadro, nao autenticacao")
# N11
for k, esp in (("n11_nfd", "EVENTO_COM_NEGACAO"), ("n11_largura_cheia", "EVENTO_COM_NEGACAO"), ("n11_largura_zero", "EVENTO_COM_NEGACAO"),
               ("n11_chave_negacao", "EVENTO_COM_NEGACAO"), ("n11_chave_proibido", "EVENTO_COM_NEGACAO"), ("n11_chave_desconhecida", "EVENTO_CHAVE_NAO_ADMITIDA")):
    unit("N11_%s" % k[4:], (lambda k=k: MOD.verificar_evento(str(ELOS[k]["seq"]), "v392", B2, True, NI, False, EV_SB, H(k))), esp,
         nota="N11: a negacao escondida por forma Unicode ou posta na CHAVE, e a chave fora do conjunto fechado; na R2 passavam")
checar("N11_guarda_palavra_largura_cheia", lambda: MOD.contem_palavra("".join(chr(ord(c) + 0xFEE0) if "!" <= c <= "~" else c for c in TK_A)),
       nota="N14/N11: a palavra guardada em largura cheia e vista pela guarda (NFKC)")
checar("N11_guarda_palavra_largura_zero", lambda: MOD.contem_palavra(TK_A[:3] + "\u200b" + TK_A[3:]), nota="a palavra guardada com espaco de largura zero no meio e vista (Cf removido)")
unit("N11_json_bytes_palavra_na_chave", lambda: MOD.json_bytes({TK_A: 1}), "PALAVRA_PROIBIDA_NA_SAIDA", nota="a guarda varre CHAVES e valores do JSON decodificado")
unit("N11_json_bytes_palavra_por_escape", lambda: MOD.json_bytes(json.loads('{"x": "\\u0043' + TK_C[1:] + '"}')), "PALAVRA_PROIBIDA_NA_SAIDA")
checar("N11_texto_comum_nao_e_negacao", lambda: MOD.negacao_em(dict(nota="ENSAIO R3 em sandbox (copia b2); o quadro real segue intocado", bancada="C:/t/vb3/b2")) is None,
       nota="o filtro normalizado nao recusa o texto do elo valido (controle de falso positivo)")

# --- N12 (em processo): hardlink dos arquivos do Nos noutra pasta -> --sandbox recusado (o "Nos real" e um decoy em copia; nada do Nos real e tocado)
NRD, HL, NCP = RAIZ / "nos_real_decoy", RAIZ / "hl", RAIZ / "nc"
for d_ in (NRD, HL, NCP):
    d_.mkdir()
for f in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json"):
    shutil.copyfile(NOS / f, NRD / f)
    os.link(NRD / f, HL / f)
    shutil.copyfile(NOS / f, NCP / f)
b2h, b2c = RAIZ / "b2h", RAIZ / "b2c"
for bb, alvo in ((b2h, HL), (b2c, NCP)):
    shutil.copytree(B2, bb)
    mh = json.loads((bb / "canonical_contracts.json").read_bytes())
    mh["canonical"]["script"]["path"] = str(alvo / "um.py")
    mh["canonical"]["seal"]["path"] = str(alvo / "um_absoluto_selo.json")
    (bb / "canonical_contracts.json").write_bytes(json.dumps(mh, ensure_ascii=False, indent=1).encode("utf-8"))
inproc("N12_hardlink_do_nos_recusa_sandbox", ["--bancada", b2h, "--nos", HL, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--sandbox", "--saida", S / "N12_hl"], 2,
       "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", patches=dict(NOS_PADRAO=NRD), bancada=b2h,
       nota="N12: o manifesto pina hardlinks dos arquivos do 'Nos real' (decoy) noutra pasta; a R2 olhava so a pasta e admitia --sandbox")
inproc("N12_copia_simples_admitida", ["--bancada", b2c, "--nos", NCP, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--sandbox", "--saida", S / "N12_nc"], 0,
       veredito_esp="JA_SINCRONIZADA__ENSAIO", patches=dict(NOS_PADRAO=NRD), bancada=b2c, nota="contraprova: copia byte a byte (nao hardlink) noutra pasta e admitida em --sandbox")
for bb in (b2h, b2c):
    apagar_arvore(bb)

# --- A13: a guarda de palavra no gerador de canais (R2, inalterado), aplicada a declaracao inteira
d13 = json.loads(DECL.read_bytes())
d13["canais"][0]["veredito_selado"] = "TGL_X_" + TK_C
spec13 = importlib.util.spec_from_file_location("gerar_canais_r2", GER)
G13 = importlib.util.module_from_spec(spec13)
sys.modules["gerar_canais_r2"] = G13
spec13.loader.exec_module(G13)
try:
    G13.gerar(d13, RAIZ / "canais_suja")
    msg13 = "ACEITO (inesperado)"
except SystemExit as exc:
    msg13 = str(exc)
ok13 = msg13.startswith("PALAVRA_PROIBIDA_NA_DECLARACAO") and not (RAIZ / "canais_suja").exists()
_registrar(dict(controle="A13_declaracao_com_token_recusada", nivel="unitario (em RAM)", recusa=msg13, pasta_nasceu=(RAIZ / "canais_suja").exists(),
                nota="o achado A13 (R1): a declaracao com o token nao gera nada (nem a pasta)"), ok13)
r13b = subprocess.run([PY, "-B", "-X", "utf8", str(GER), str(DECL), str(RAIZ / "canais")], capture_output=True, text=True, encoding="utf-8", errors="replace")
ger = RAIZ / "canais" / "GERACAO_RECIBO.json"
ok13b = r13b.returncode == 0 and ger.exists() and (RAIZ / "canais" / "registros_gerados.py").exists()
_registrar(dict(controle="A13_declaracao_limpa_gera", nivel="subprocesso", rc=r13b.returncode, gerados=(json.loads(ger.read_bytes()) if ger.exists() else None),
                nota="a declaracao limpa (CANAIS_v391_exemplo.json da R1) gera os quatro arquivos"), ok13b)

# ================================================================ o "selo" do sandbox: nos/ recebe os bytes de nos_v392/
for f in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json"):
    shutil.copyfile(NOS392 / f, NOS / f)
assert sha(NOS / "um.py") == SBM["nos_v392"]["um_py"]["sha256"] and sha(NOS / "tgl_kernel_proof_manifest.json") == SBM["nos_v392"]["kernel_manifest"]["sha256"]
_registrar(dict(controle="SELO_DO_SANDBOX", nivel="montagem", nos_um_py_sha256=sha(NOS / "um.py"), nos_selo_sha256=sha(NOS / "um_absoluto_selo.json"),
                nos_kernel_manifest_sha256=sha(NOS / "tgl_kernel_proof_manifest.json"),
                nota="nos/ passou de v391 para o v392 sintetico no MESMO caminho pinado por b2 (com o manifesto do kernel sintetico): o canonical.py de b2 deve recusar (PIN_CHANGED)"), True)
NI392 = MOD.ler_nos(NOS392, "v392")
PRE = MOD.conferir_recibo_pre_selo(R1B, MOD.estado_anterior(B2, MOD.carregar_canonical(B2)[0]), B2, False, sha(R1B))

# ================================================================ controles DEPOIS do selo (b2 em PIN_CHANGED)
# --- C7: bateria com um teste que FALHA, em aplicar com evento sandbox: nada se grava
falha_py = FX / "falha_injetada.py"
falha_py.write_bytes(b"import sys\nprint('falha injetada')\nsys.exit(1)\n")
t_falha = dict(id="T00_FALHA_INJETADA", teste="controle: um teste que falha de proposito", fontes=[_pinar(falha_py)],
               comando=["{py}", "-B", "{fonte:0}"], cwd="{raiz}", verificacao=dict(tipo="exit0"), fases=["pre_selo", "pos_selo"], obrigatorio_em=["ensaio", "aplicar"], timeout_s=60)
bt_c7, bt_c7_sha = mini_bateria("C7_falha", extra=[t_falha])
run("C7_bateria_falha_em_aplicar", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_c7, "--bateria-sha256", bt_c7_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                    "--evento", "SANDBOX:controle C7", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 3,
    veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", bancada=B2,
    extra_ok=lambda j, r: not (B2 / "CONTRATO_CANONICO_B3.md").exists() and {k: t["resultado"] for k, t in testes(j).items()} ==
    {"T01_IDENTIDADE": "PASSA", "T15_SONDAS": "PASSA", "T17_LEAN_KERNEL": "PASSA", "T00_FALHA_INJETADA": "FALHA"})

# --- A1 e N1: o T17 pelo recibo do kernel VINCULADO ao manifesto do kernel pinado pelo selo
K = json.loads(K_OK.read_bytes())
KL = FX / "kernel_logs"


def kfix(nome, mut=None, novo=None):
    k = copy.deepcopy(K) if novo is None else novo
    if mut:
        mut(k)
    p = FX / ("KERNEL_RECIBO_INVALIDO_%s.json" % nome)
    p.write_bytes(json.dumps(k, ensure_ascii=False, indent=1).encode("utf-8"))
    return p


def log_fix(nome, texto):
    p = KL / ("%s.log" % nome)
    p.write_bytes(texto.encode("utf-8"))
    return dict(path=str(p), sha256=sha(p))


log_b_ok = (KL / "build_full_SINTETICO.log").read_text(encoding="utf-8")
log_a_ok = (KL / "audit_SINTETICO.log").read_text(encoding="utf-8")
KS2 = FX / "kernel_src_mudada"
shutil.copytree(FX / "kernel_src", KS2)
(KS2 / "TGLExt" / "PedraSinteticaA.lean").write_bytes((KS2 / "TGLExt" / "PedraSinteticaA.lean").read_bytes() + b"-- mudado depois do recibo\n")
FIX = dict(
    sorry=(kfix("sorry", lambda k: k.update(sorry=1)), "sorry=1"),
    versao=(kfix("versao", lambda k: k.update(versao="v391")), "e da versao"),
    log=(kfix("log", lambda k: k["build_full_log"].update(sha256="0" * 64)), "nao bate com o sha declarado"),
    um_py=(kfix("um_py", lambda k: k.update(um_py_sha256=SBM["nos_v392"]["um_py"]["sha256"])), "campos PROIBIDOS"),
    r2_minimo_4_campos=(kfix("r2_minimo_4_campos", novo=dict(versao="v392", rc=0, sorry=0, build_full_log_sha256="0" * 64)), "contrato="),
    manifesto_proibido=(kfix("manifesto_proibido", lambda k: k.update(tgl_kernel_proof_manifest_sha256=SBM["nos_v392"]["kernel_manifest"]["sha256"])), "campos PROIBIDOS"),
    contrato_errado=(kfix("contrato_errado", lambda k: k.update(contrato="KERNEL_RECIBO_R2")), "contrato="),
    campo_ausente=(kfix("campo_ausente", lambda k: k.pop("audit_log")), "sem os campos"),
    rc_float=(kfix("rc_float", lambda k: k.update(rc=0.0)), "rc=0.0"),
    rc_bool=(kfix("rc_bool", lambda k: k.update(rc=False)), "rc=False"),
    erros_texto=(kfix("erros_texto", lambda k: k.update(erros="0")), "erros="),
    log_ausente=(kfix("log_ausente", lambda k: k["build_full_log"].update(path=str(KL / "nao_existe.log"))), "ausente em disco"),
    log_relativo=(kfix("log_relativo", lambda k: k["build_full_log"].update(path="build_full_SINTETICO.log")), "nao e absoluto"),
    log_com_sorry=(kfix("log_com_sorry", lambda k: k.update(build_full_log=log_fix("build_com_sorry", log_b_ok + "TGLExt/PedraSinteticaA.lean:3:8: warning: declaration uses 'sorry'\n"))),
                   "ocorrencia(s) de sorry"),
    log_com_erro=(kfix("log_com_erro", lambda k: k.update(build_full_log=log_fix("build_com_erro", log_b_ok + "TGLExt/PedraSinteticaB.lean:3:1: error: unknown identifier 'x'\n"))),
                  "linha(s) de erro"),
    logs_iguais=(kfix("logs_iguais", lambda k: k.update(audit_log=dict(k["build_full_log"]))), "mesmo arquivo"),
    audit_axioma_proprio=(kfix("audit_axioma_proprio", lambda k: k.update(audit_log=log_fix("audit_axioma_proprio", log_a_ok + "'TGLExt.X.y' depends on axioms: [propext, TGL.axiomaProprio]\n"))),
                          "axiomas fora do trio"),
    audit_sorryAx=(kfix("audit_sorryAx", lambda k: k.update(audit_log=log_fix("audit_sorryAx", log_a_ok + "'TGLExt.X.y' depends on axioms: [sorryAx]\n"))), "sorry"),
    audit_sem_print=(kfix("audit_sem_print", lambda k: k.update(audit_log=log_fix("audit_sem_print", "audit.log sem nenhuma linha de axiomas\n"))), "nenhuma linha"),
    axiomas_declarados_fora=(kfix("axiomas_declarados_fora", lambda k: k["axiomas"].append("TGL.axiomaProprio")), "axiomas declarados fora do trio"),
    axiomas_nao_declarados=(kfix("axiomas_nao_declarados", lambda k: k.update(axiomas=["propext"])), "que o recibo nao declara"),
    toolchain_diverge=(kfix("toolchain_diverge", lambda k: k["toolchain"].update(lean_version="Lean (version 4.30.0)")), "toolchain"),
    raiz_depois_diverge=(kfix("raiz_depois_diverge", lambda k: k["raiz"].update(sha256_depois=sha_b(b"outra raiz"))), "formal_files_sha256"),
    audit_depois_diverge=(kfix("audit_depois_diverge", lambda k: k["audit"].update(sha256_depois=sha_b(b"outro audit"))), "formal_files_sha256"),
    raiz_caminho_errado=(kfix("raiz_caminho_errado", lambda k: k["raiz"].update(path="TGLExt/Outra.lean")), "raiz exige"),
    pedra_fora_do_manifesto=(kfix("pedra_fora_do_manifesto", lambda k: k["pedras"].append(dict(path="TGLExt/PedraNaoSelada.lean", sha256=sha_b(b"nao selada")))), "formal_files_sha256"),
    pedra_sha_diverge=(kfix("pedra_sha_diverge", lambda k: k["pedras"][0].update(sha256=sha_b(b"outra pedra"))), "formal_files_sha256"),
    pedra_repetida=(kfix("pedra_repetida", lambda k: k["pedras"].append(dict(k["pedras"][0]))), "repetido"),
    pedra_fora_de_TGLExt=(kfix("pedra_fora_de_TGLExt", lambda k: k["pedras"].append(dict(path="TGL/Audit.lean", sha256=k["audit"]["sha256_depois"]))), "caminho invalido"),
    pedras_vazias=(kfix("pedras_vazias", lambda k: k.update(pedras=[])), "pedras vazias"),
    arvore_mudou=(kfix("arvore_mudou", lambda k: k.update(arvore=str(KS2))), "mudou depois do recibo"),
    arvore_ausente=(kfix("arvore_ausente", lambda k: k.update(arvore=str(FX / "arvore_que_nao_existe"))), "arvore do build ausente"),
    criterio_j1_diverge=(kfix("criterio_j1_diverge", lambda k: k["criterios"]["j1_declaracoes"].update(medido=1)), "criterio j1_declaracoes"),
    criterio_ausente=(kfix("criterio_ausente", lambda k: k["criterios"].pop("r1_ausente")), "criterio r1_ausente"),
    criterio_tipo=(kfix("criterio_tipo", lambda k: k["criterios"]["tokens_proibidos"].update(medido=0.0)), "criterio tokens_proibidos"),
    impressao_mudou=(kfix("impressao_mudou", lambda k: k["nos_kernel_impressao"].update(depois=sha_b(b"outra impressao"))), "impressao do kernel do Nos mudou"),
)
for nome in ("sorry", "versao", "log", "um_py"):      # os 4 da R2, mantidos pelo nome, agora no contrato R3
    kp, contem = FIX[nome]
    run("A1_kernel_recibo_invalido_%s" % nome, ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
                                               "--fase", "pos_selo", "--evento", "SANDBOX:A1", "--kernel-recibo", kp, "--kernel-recibo-sha256", sha(kp)], 3,
        veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", bancada=B2,
        extra_ok=lambda j, r, contem=contem: (lambda t: t["resultado"] == "FALHA" and t.get("comando") is None and contem in t["detalhe"])(testes(j)["T17_LEAN_KERNEL"]),
        nota="A1 (R2) no contrato R3: o recibo invalido e lido por hash, sem subprocesso, e o T17 FALHA com o motivo")
for nome in ("r2_minimo_4_campos", "log_com_sorry", "raiz_depois_diverge", "arvore_mudou"):   # os N1 principais tambem pelo caminho inteiro do aplicar
    kp, contem = FIX[nome]
    run("N1_sub_kernel_recibo_%s" % nome, ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
                                          "--fase", "pos_selo", "--evento", "SANDBOX:N1", "--kernel-recibo", kp, "--kernel-recibo-sha256", sha(kp)], 3,
        veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", bancada=B2,
        extra_ok=lambda j, r, contem=contem: (lambda t: t["resultado"] == "FALHA" and contem in t["detalhe"])(testes(j)["T17_LEAN_KERNEL"]),
        nota="N1 (ALTA): o recibo %s passava na R2 (o T17 era autodeclarado); na R3 o T17 FALHA e nada se grava" % nome)
for nome, (kp, contem) in FIX.items():
    passa_ret, det, _ = MOD.verificar_kernel_recibo(kp, "v392", NI392, sha(kp), None, True)
    _registrar(dict(controle="N1_unit_kernel_recibo_%s" % nome, nivel="unitario", detalhe=det[:300], esperado_no_detalhe=contem,
                    nota="N1: verificar_kernel_recibo(%s) recusa" % kp.name), passa_ret is False and contem in det)


def _unit_k(nome, esperado_ok, contem, ni=None, sha_=None, pre=None, sandbox=True, kp=K_OK, nota=""):
    passa_ret, det, _ = MOD.verificar_kernel_recibo(kp, "v392", ni or NI392, sha_, pre, sandbox)
    ok = (passa_ret is True) if esperado_ok else (passa_ret is False and contem in det)
    _registrar(dict(controle=nome, nivel="unitario", detalhe=det[:300], esperado_no_detalhe=contem, nota=nota), ok)


_unit_k("N1_unit_kernel_recibo_valido_aceito_em_sandbox", True, None, sha_=K_OK_SHA, nota="contraprova: o recibo sintetico valido passa (sandbox, sem pre-selo: ANTES nao cruzado e dito)")
_unit_k("N1_unit_kernel_recibo_valido_aceito_com_pre_selo", True, None, sha_=K_OK_SHA, pre=PRE, sandbox=False, nota="contraprova: com o recibo pre-selo do run 1b, o ANTES e cruzado")
_unit_k("N1_unit_sem_sha_fora_do_sandbox", False, "sem --kernel-recibo-sha256", sha_=None, pre=PRE, sandbox=False)
_unit_k("N1_unit_sha_divergente", False, "KERNEL_RECIBO_SHA_DIVERGE", sha_="0" * 64)
_unit_k("N1_unit_sem_pre_selo_fora_do_sandbox", False, "ANTES nao e conferivel", sha_=K_OK_SHA, pre=None, sandbox=False)
pre_mut = copy.deepcopy(PRE)
pre_mut["kernel_anterior"]["raiz_sha256"] = sha_b(b"outra raiz anterior")
_unit_k("N1_unit_antes_diverge_do_pre_selo", False, "recibo pre-selo", sha_=K_OK_SHA, pre=pre_mut, sandbox=False)
pre_mut2 = copy.deepcopy(PRE)
pre_mut2["kernel_anterior"]["impressao_formal"] = sha_b(b"outra impressao")
_unit_k("N1_unit_impressao_antes_diverge_do_pre_selo", False, "nos_kernel_impressao.antes", sha_=K_OK_SHA, pre=pre_mut2, sandbox=False)
ni_ss = dict(NI392, _kernel_man=None, kernel=None)
_unit_k("N1_unit_selo_sem_pino_do_manifesto", False, "nao pina tgl_kernel_proof_manifest.json", ni=ni_ss, sha_=K_OK_SHA)
km = NI392["_kernel_man"]
km_st = dict(km, statuses=dict(km["statuses"], sorryAx_absent=False))
_unit_k("N1_unit_manifesto_status_falso", False, "statuses do manifesto", ni=dict(NI392, _kernel_man=km_st), sha_=K_OK_SHA)
km_ax = dict(km, axiom_report=dict(km["axiom_report"], **{"TGLExt.X.ruim": ["propext", "sorryAx"]}))
_unit_k("N1_unit_manifesto_axiom_report_fora_do_trio", False, "axiom_report fora do trio", ni=dict(NI392, _kernel_man=km_ax), sha_=K_OK_SHA)
ni_tc = dict(NI392, kernel=dict(NI392["kernel"], lean_version="Lean (version 9.9.9)"))
_unit_k("N1_unit_manifesto_toolchain_diverge", False, "toolchain", ni=ni_tc, sha_=K_OK_SHA)
run("N1_kernel_recibo_sem_sha_em_aplicar", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
                                            "--fase", "pos_selo", "--evento", "SANDBOX:N1", "--kernel-recibo", K_OK], 2, "KERNEL_RECIBO_SHA_AUSENTE", bancada=B2,
    nota="N1/N2: em aplicar o recibo do kernel exige o sha pinado (--kernel-recibo-sha256), mesmo em --sandbox")
run("N1_kernel_recibo_sha_divergente", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
                                        "--fase", "pos_selo", "--evento", "SANDBOX:N1", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", "1" * 64], 2, "KERNEL_RECIBO_SHA_DIVERGE", bancada=B2)
run("N1_kernel_recibo_ausente_fora_do_sandbox", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--modo", "aplicar", "--fase", "pos_selo",
                                                 "--evento", str(ELOS["valido"]["seq"]), "--evento-hash", H("valido"), "--recibo-pre-selo", R1B, "--recibo-pre-selo-sha256", sha(R1B)], 2,
    "KERNEL_RECIBO_AUSENTE", bancada=B2, nota="fora do sandbox, o B(n) sem --kernel-recibo e recusado antes da bateria")
run("A1_kernel_recibo_ausente_em_ensaio_NAO_EXECUTADO", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "ensaio",
                                                             "--fase", "pos_selo"], 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2,
    extra_ok=lambda j, r: testes(j)["T17_LEAN_KERNEL"]["resultado"] == "NAO_EXECUTADO",
    nota="em ensaio sem recibo o T17 fica NAO_EXECUTADO com o motivo (nunca PASSA por omissao)")
bt_t17, _ = mini_bateria("so_T17", ids=("T17_LEAN_KERNEL",), manter_copias=False)
r_a1 = MOD.rodar_bateria(json.loads(bt_t17.read_bytes()), dict(py=PY, raiz=str(FX / "u"), candidate=str(FX / "u"), nos=str(NOS), versao="v392", recibos=str(FX / "u" / "rec"),
                                                               tunel="", saida=str(FX / "u"), rotulo="u", kernel_recibo=""), FX / "u" / "rec", "aplicar", "pos_selo", False, None, NI392, ())
_registrar(dict(controle="A1_kernel_recibo_ausente_em_aplicar_fora_do_sandbox_FALHA", nivel="unitario", retorno=r_a1["testes"][-1]["resultado"],
                nota="unitario: fora do sandbox, aplicar sem --kernel-recibo -> T17 FALHA"), r_a1["testes"][-1]["resultado"] == "FALHA")

# --- A3: a bateria roda a partir dos caminhos PINADOS, nunca da pasta onde o esboco esta
esb = RAIZ / "esb"
(esb / "bateria").mkdir(parents=True)
shutil.copyfile(SYNC, esb / "sincronizar_bancada.py")
t01_real = Path(json.loads(BAT.read_bytes())["testes"][0]["fontes"][0]["path"])
adult = t01_real.read_bytes().replace(b'veredito=("PASSA" if not falhas else "FALHA")', b'veredito="PASSA"  # ADULTERADO').replace(b'checks["sem_literal_de_beta_em_bancada_py"] = lit_beta == []', b'checks["sem_literal_de_beta_em_bancada_py"] = True; print("ADULTERADO")')
assert adult != t01_real.read_bytes()
(esb / "bateria" / "t01_identidade.py").write_bytes(adult)
run("A3_esboco_copiado_com_t01_adulterado_ao_lado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--sandbox", "--modo", "ensaio",
                                                     "--fase", "pos_selo"], 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, sync=esb / "sincronizar_bancada.py",
    extra_ok=lambda j, r: (lambda t01: t01["resultado"] == "PASSA" and os.path.samefile(t01["comando"][4], t01_real) and t01["fontes"][0]["estado"] == "OK" and
                           "ADULTERADO" not in Path(t01["log"]["path"]).read_text(encoding="utf-8"))(testes(j)["T01_IDENTIDADE"]),
    nota="o ataque A8/A3 (ALTA) da auditoria R1: o esboco copiado para outra pasta com um t01 ADULTERADO ao lado; o comando executa o caminho pinado")
bt_np, bt_np_sha = mini_bateria("py_nao_pinado", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["testes"][0]["comando"].__setitem__(4, str(esb / "bateria" / "t01_identidade.py")))
run("A3_comando_executa_py_nao_pinado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_np, "--bateria-sha256", bt_np_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 3,
    veredito_esp="REPINADA_B3__BATERIA_FALHOU", bancada=B2,
    extra_ok=lambda j, r: "COMANDO_EXECUTA_ARQUIVO_NAO_PINADO" in testes(j)["T01_IDENTIDADE"]["detalhe"],
    nota="um comando cujo .py nao e fonte pinada nem copia conferida e recusado ANTES de executar")
t01_fx = FX / "t01_copia_pinada.py"
shutil.copyfile(t01_real, t01_fx)
bt_fx, bt_fx_sha = mini_bateria("fonte_adulterada", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["testes"][0]["fontes"].__setitem__(0, _pinar(t01_fx)))
t01_fx.write_bytes(adult)   # a fonte pinada e adulterada DEPOIS do pino
run("A3_fonte_pinada_adulterada_antes_de_rodar", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_fx, "--bateria-sha256", bt_fx_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 3,
    veredito_esp="REPINADA_B3__BATERIA_FALHOU", bancada=B2,
    extra_ok=lambda j, r: (lambda t01: t01["resultado"] == "FALHA" and t01["fontes"][0]["estado"] == "ALTERADA" and "comando" not in t01)(testes(j)["T01_IDENTIDADE"]),
    nota="o sha256 e conferido ANTES de executar: fonte alterada = FALHA sem subprocesso")

# --- N5 e N16: interpretador isolado, ambiente limpo, cwd vazio, modulo-sombra recusado, gramatica fechada do comando
def fixture_py(sub, nome, texto):
    d_ = FX / sub
    d_.mkdir(exist_ok=True)
    p_ = d_ / nome
    p_.write_bytes(texto.encode("utf-8"))
    return p_


def t_extra(tid, fonte, comando, ver=None, extra_fontes=()):
    return dict(id=tid, teste="controle R3 " + tid, fontes=[_pinar(fonte)] + [_pinar(x) for x in extra_fontes], comando=comando, cwd="{raiz}",
                verificacao=ver or dict(tipo="exit0"), fases=["pre_selo", "pos_selo"], obrigatorio_em=["ensaio", "aplicar"], timeout_s=120)


MARC = FX / "n5_MARCADORES"
MARC.mkdir()
sombra_hl = fixture_py("n5s", "teste_sombra.py", "import hashlib\nprint('ok', hashlib.sha256(b'x').hexdigest()[:8])\n")
fixture_py("n5s", "hashlib.py", "from pathlib import Path\n(Path(__file__).resolve().parent.parent / 'n5_MARCADORES' / 'sombra_hashlib_executou.txt').write_text('x')\n")
sombra_pk = fixture_py("n5p", "teste_pacote.py", "import json\nprint(json.dumps({'ok': 1}))\n")
fixture_py("n5p/json", "__init__.py", "from pathlib import Path\n(Path(__file__).resolve().parents[2] / 'n5_MARCADORES' / 'sombra_json_executou.txt').write_text('x')\n")
sombra_np = fixture_py("n5n", "teste_numpy.py", "print('ok')\n")
fixture_py("n5n", "numpy.py", "raise SystemExit('sombra de numpy')\n")
amb = fixture_py("n5e", "teste_ambiente.py",
                 "import os, sys, json\nfrom pathlib import Path\n"
                 "cwd = os.getcwd()\naqui = os.path.normcase(str(Path(__file__).resolve().parent))\n"
                 "r = dict(cwd=cwd, cwd_vazio_no_inicio=(os.listdir(cwd) == []), ignore_environment=bool(sys.flags.ignore_environment),\n"
                 "         pythonpath_no_ambiente=('PYTHONPATH' in os.environ), safe_path=bool(sys.flags.safe_path),\n"
                 "         pasta_do_script_no_sys_path=any(os.path.normcase(os.path.abspath(p or cwd)) == aqui for p in sys.path),\n"
                 "         sitecustomize_do_ataque=bool(getattr(sys.modules.get('sitecustomize'), 'MARCA_N5', False)))\n"
                 "ok = r['cwd_vazio_no_inicio'] and r['ignore_environment'] and r['safe_path'] and not r['pythonpath_no_ambiente'] and not r['pasta_do_script_no_sys_path'] and not r['sitecustomize_do_ataque']\n"
                 "r['veredito'] = 'PASSA' if ok else 'FALHA'\nPath(sys.argv[1]).write_text(json.dumps(r), encoding='utf-8')\nprint(json.dumps(r))\n")
fixture_py("n5pp", "sitecustomize.py", "MARCA_N5 = True\nfrom pathlib import Path\n(Path(__file__).resolve().parent.parent / 'n5_MARCADORES' / 'sitecustomize_executou.txt').write_text('x')\n")
(FX / "n5vazio").mkdir()
T_AMB = t_extra("T00_AMBIENTE", amb, ["{py}", "-B", "-X", "utf8", "{fonte:0}", "{recibos}/T00_AMBIENTE.json"],
                dict(tipo="json_igual", arquivo="{recibos}/T00_AMBIENTE.json", campos=dict(veredito="PASSA")))
bt_n5, bt_n5_sha = mini_bateria("N5_sombra_e_ambiente", ids=("T01_IDENTIDADE", "T15_SONDAS"), extra=[
    t_extra("T00_SOMBRA_HASHLIB", sombra_hl, ["{py}", "-B", "{fonte:0}"]),
    t_extra("T00_SOMBRA_PACOTE_JSON", sombra_pk, ["{py}", "-B", "{fonte:0}"]),
    t_extra("T00_SOMBRA_NUMPY", sombra_np, ["{py}", "-B", "{fonte:0}"])])
run("N5_modulo_sombra_ao_lado_da_fonte", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_n5, "--bateria-sha256", bt_n5_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 3,
    veredito_esp="REPINADA_B3__BATERIA_FALHOU", bancada=B2,
    extra_ok=lambda j, r: (lambda ts: all(ts[x]["resultado"] == "FALHA" and "SOMBRA_DE_MODULO_AO_LADO_DA_FONTE" in ts[x]["detalhe"] and "comando_executado" not in ts[x]
                                          for x in ("T00_SOMBRA_HASHLIB", "T00_SOMBRA_PACOTE_JSON", "T00_SOMBRA_NUMPY"))
                           and ts["T01_IDENTIDADE"]["resultado"] == "PASSA" and not any(MARC.iterdir()))(testes(j)),
    nota="N5: hashlib.py, o pacote json/ e numpy.py postos ao lado de fonte pinada sombreiam stdlib/site; na R2 o hashlib.py executava dentro do teste; na R3 o teste FALHA sem executar nada")
bt_amb, bt_amb_sha = mini_bateria("N5_ambiente", ids=("T01_IDENTIDADE", "T15_SONDAS"), extra=[T_AMB])
run("N5_PYTHONPATH_injetado_nao_chega_ao_teste", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_amb, "--bateria-sha256", bt_amb_sha, "--sandbox", "--modo", "ensaio",
                                                  "--fase", "pos_selo"], 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, flags=("-E", "-B", "-X", "utf8"),
    env_extra=dict(PYTHONPATH=str(FX / "n5pp")),
    extra_ok=lambda j, r: (lambda ts: ts["T00_AMBIENTE"]["resultado"] == "PASSA" and not any(MARC.iterdir()) and
                           json.loads(Path(S / "N5_PYTHONPATH_injetado_nao_chega_ao_teste" / "recibos" / "T00_AMBIENTE.json").read_text(encoding="utf-8"))["cwd"].startswith(
                               str(S / "N5_PYTHONPATH_injetado_nao_chega_ao_teste" / "cwd_testes")))(testes(j)),
    nota="N5: com PYTHONPATH apontando um sitecustomize de ataque (o esboco chamado com -E), o teste ve: -E, -P, sem PYTHONPATH, cwd vazio novo, pasta do script fora do sys.path; o sitecustomize nao roda")
run("N5_PYTHONPATH_sem_E_recusado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_amb, "--bateria-sha256", bt_amb_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 2,
    "AMBIENTE_PYTHON_INJETAVEL", bancada=B2, env_extra=dict(PYTHONPATH=str(FX / "n5vazio")), extra_ok=lambda j, r: j.get("recibo") is None,
    nota="N5: o proprio esboco recusa rodar com PYTHONPATH/PYTHONHOME/PYTHONSTARTUP no ambiente sem -E (a pasta apontada e vazia)")
zp = FX / "n16" / "app.zip"
zp.parent.mkdir()
with zipfile.ZipFile(zp, "w") as z:
    z.writestr("__main__.py", "print('zip executou')\n")
pasta_main = fixture_py("n16/pasta", "__main__.py", "print('pasta executou')\n")
ok_py = fixture_py("n16", "ok.py", "print('ok')\n")
bt_n16, bt_n16_sha = mini_bateria("N16_formas_de_comando", ids=("T01_IDENTIDADE", "T15_SONDAS"), extra=[
    t_extra("T00_FORMA_C", ok_py, ["{py}", "-c", "print('c executou')"]),
    t_extra("T00_FORMA_M", ok_py, ["{py}", "-m", "json.tool", "{fonte:0}"]),
    t_extra("T00_FORMA_ZIP", zp, ["{py}", "-B", "{fonte:0}"]),
    t_extra("T00_FORMA_PASTA", pasta_main, ["{py}", "-B", str(pasta_main.parent)]),
    t_extra("T00_FORMA_OPCAO_I", ok_py, ["{py}", "-I", "{fonte:0}"]),
    t_extra("T00_FORMA_SEM_PY", ok_py, ["python", "{fonte:0}"]),
    t_extra("T00_FORMA_RELATIVA", ok_py, ["{py}", "-B", "ok.py"])])
run("N16_formas_de_comando_fora_da_gramatica", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_n16, "--bateria-sha256", bt_n16_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 3,
    veredito_esp="REPINADA_B3__BATERIA_FALHOU", bancada=B2,
    extra_ok=lambda j, r: (lambda ts: all(ts[x]["resultado"] == "FALHA" and ("COMANDO_FORMA_NAO_ADMITIDA" in ts[x]["detalhe"] or "COMANDO_EXECUTA_ARQUIVO_NAO_PINADO" in ts[x]["detalhe"])
                                          and "comando_executado" not in ts[x] for x in ts if x.startswith("T00_FORMA_")) and len([x for x in ts if x.startswith("T00_FORMA_")]) == 7)(testes(j)),
    nota="N16: -c, -m, zip, pasta com __main__, -I, comando sem {py} e .py relativo: todos recusados antes de executar (na R2 a guarda so olhava argumentos .py)")

# --- N14: a palavra guardada na saida de um teste e na propria bateria
tok = fixture_py("n14", "teste_token.py", "print('linha comum')\nprint('TGL_PRO' + 'VED')\n")
bt_n14, bt_n14_sha = mini_bateria("N14_token_na_saida", ids=("T01_IDENTIDADE", "T15_SONDAS"), extra=[t_extra("T00_TOKEN_NA_SAIDA", tok, ["{py}", "-B", "{fonte:0}"])])
run("N14_token_na_saida_do_teste_log_suprimido", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_n14, "--bateria-sha256", bt_n14_sha, "--sandbox", "--modo", "ensaio",
                                                  "--fase", "pos_selo"], 3, veredito_esp="REPINADA_B3__BATERIA_FALHOU", bancada=B2,
    extra_ok=lambda j, r: (lambda t: t["resultado"] == "FALHA" and t["log"]["suprimido"] is True and not MOD.contem_palavra(Path(t["log"]["path"]).read_text(encoding="utf-8"))
                           and "SAIDA_SUPRIMIDA" in Path(t["log"]["path"]).read_text(encoding="utf-8"))(testes(j)["T00_TOKEN_NA_SAIDA"]),
    nota="N14: na R2 o .log era gravado ANTES da guarda (o token ficava em disco); na R3 a guarda vem antes e o log sai suprimido (so o sha do texto)")
bt_n14b, bt_n14b_sha = mini_bateria("N14_token_na_bateria", ids=("T01_IDENTIDADE", "T15_SONDAS"), escapar_token=True,
                                    mutar=lambda b: b["testes"][0].update(teste="X_" + TK_C))
run("N14_token_na_bateria_recibo_minimo", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_n14b, "--bateria-sha256", bt_n14b_sha, "--sandbox", "--modo", "ensaio",
                                           "--fase", "pos_selo"], 2, "PALAVRA_PROIBIDA_NA_SAIDA", bancada=B2,
    extra_ok=lambda j, r: j.get("recibo") is not None and not MOD.contem_palavra(Path(j["recibo"]).read_text(encoding="utf-8")) and r.returncode == 2 and "Traceback" not in r.stderr,
    nota="N14: na R2 o token (por escape) na bateria virava traceback rc 1 sem JSON; na R3 sai um recibo MINIMO sem a palavra, rc 2")

# --- A4 (subprocesso): o evento com negacao e o evento de outro programa, no caminho real do aplicar; N6 pelo caminho inteiro
run("A4_sub_evento_com_negacao", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                  "--evento", str(ELOS["negacao"]["seq"]), "--evento-hash", H("negacao"), "--eventos", EV_SB, "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 2,
    "EVENTO_COM_NEGACAO", bancada=B2)
run("A4_sub_evento_forjado_sem_cadeia", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                         "--evento", "90001", "--eventos", FX / "eventos_forjado_sem_cadeia.jsonl", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 2,
    "EVENTOS_CADEIA_QUEBRADA", bancada=B2)
run("N6_sub_aplicar_sem_evento_hash", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                       "--evento", str(ELOS["valido"]["seq"]), "--eventos", EV_SB, "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 2, "EVENTO_HASH_AUSENTE", bancada=B2,
    nota="N6: o elo valido sem --evento-hash: recusado antes de qualquer gravacao")
run("N6_sub_aplicar_evento_hash_errado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                          "--evento", str(ELOS["valido"]["seq"]), "--evento-hash", H("decoy"), "--eventos", EV_SB, "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 2,
    "EVENTO_HASH_DIVERGE", bancada=B2)

# --- A6 e N2: o recibo pre-selo conferido por identidade e por PINO
pre_forj = FX / "PRE_forjado.json"
pre_forj.write_bytes(json.dumps(dict(fase="pre_selo", bateria_resultado=dict(veredito="BATERIA_PASSA", testes=[]), versao_alvo="v000", bancada=dict(dir="X:/outra"),
                                     nos=dict(um_py=dict(sha256="0" * 64)), veredito="JA_SINCRONIZADA__ENSAIO__FORJADO")).encode("utf-8"))
run("A6_recibo_pre_selo_forjado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                   "--evento", "SANDBOX:A6", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA, "--recibo-pre-selo", pre_forj], 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=B2,
    nota="o ataque B4 da auditoria R1: recibo pre-selo forjado (v000, outra bancada, outro um.py) recusado por identidade")
run("A6_recibo_pre_selo_de_outra_bancada", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                            "--evento", "SANDBOX:A6", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA, "--recibo-pre-selo", R1A], 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=B2,
    nota="o recibo REAL do run 1a (Bancada b1) usado para b2: outra Bancada por identidade -> recusado")
rj = json.loads(R1B.read_bytes())
rj["nos"]["um_py"]["sha256"] = "2" * 64
pre_mut_p = FX / "PRE_1b_um_py_trocado.json"
pre_mut_p.write_bytes(json.dumps(rj, ensure_ascii=False).encode("utf-8"))
run("A6_recibo_pre_selo_1b_com_um_py_trocado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                                "--evento", "SANDBOX:A6", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA, "--recibo-pre-selo", pre_mut_p], 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=B2)
run("A6_recibo_pre_selo_na_fase_pre_selo", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--fase", "pre_selo", "--recibo-pre-selo", R1A], 2, "RECIBO_PRE_SELO_NA_FASE_PRE_SELO", bancada=B1)
run("A6_aplicar_fora_do_sandbox_sem_recibo_pre_selo", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--modo", "aplicar", "--fase", "pos_selo",
                                                       "--evento", str(ELOS["valido"]["seq"]), "--kernel-recibo", K_OK], 2, "RECIBO_PRE_SELO_AUSENTE", bancada=B2)
run("APLICAR_na_fase_pre_selo_recusado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--sandbox", "--modo", "aplicar", "--fase", "pre_selo",
                                          "--evento", "SANDBOX:x"], 2, "APLICAR_SO_NA_FASE_POS_SELO", bancada=B2)
rj2 = json.loads(R1B.read_bytes())
rj2["nos"].pop("kernel")
pre_sk = FX / "PRE_1b_sem_kernel.json"
pre_sk.write_bytes(json.dumps(rj2, ensure_ascii=False).encode("utf-8"))
run("N1_recibo_pre_selo_sem_kernel", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                      "--evento", "SANDBOX:N1", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA, "--recibo-pre-selo", pre_sk], 2, "RECIBO_PRE_SELO_SEM_KERNEL", bancada=B2,
    nota="N1: o recibo pre-selo R3 tem de trazer o kernel anterior (o ANTES que o T17 cruza)")
run("N2_aplicar_fora_do_sandbox_sem_sha_do_pre_selo", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--modo", "aplicar", "--fase", "pos_selo",
                                                       "--evento", str(ELOS["valido"]["seq"]), "--evento-hash", H("valido"), "--recibo-pre-selo", R1B, "--kernel-recibo", K_OK,
                                                       "--kernel-recibo-sha256", K_OK_SHA], 2, "RECIBO_PRE_SELO_SHA_AUSENTE", bancada=B2,
    nota="N2: fora do sandbox, o recibo pre-selo exige o sha pinado (--recibo-pre-selo-sha256)")
run("N2_sha_do_pre_selo_divergente", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                      "--evento", "SANDBOX:N2", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA, "--recibo-pre-selo", R1B, "--recibo-pre-selo-sha256", "3" * 64], 2,
    "RECIBO_PRE_SELO_SHA_DIVERGE", bancada=B2)

# --- N10: o recibo do aplicar nao segue juncao em estado/ (para fora nem para dentro); verificado ANTES da primeira gravacao
b2j, b2k = RAIZ / "b2j", RAIZ / "b2k"
fora_estado = RAIZ / "fora_estado"
fora_estado.mkdir()
for bb in (b2j, b2k):
    shutil.copytree(B2, bb)
    os.rmdir(bb / "estado")
juncao(b2j / "estado", fora_estado)
(b2k / "outro_estado").mkdir()
juncao(b2k / "estado", b2k / "outro_estado")
run("N10_estado_juncao_para_fora", ["--bancada", b2j, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                    "--evento", "SANDBOX:N10", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 2, "CAMINHO_", bancada=b2j,
    extra_ok=lambda j, r: not any(fora_estado.iterdir()) and not (b2j / "CONTRATO_CANONICO_B3.md").exists(),
    nota="N10: estado/ e uma juncao para fora da Bancada; na R2 o recibo nascia fora; na R3 o pre-voo recusa antes de qualquer gravacao (manifesto intocado)")
run("N10_estado_juncao_para_dentro", ["--bancada", b2k, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                      "--evento", "SANDBOX:N10", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 2, "CAMINHO_COM_JUNCAO", bancada=b2k,
    extra_ok=lambda j, r: not any((b2k / "outro_estado").iterdir()),
    nota="N10: mesmo uma juncao que fica dentro da Bancada e recusada (o recibo nao segue juncao)")

# --- N1, N2, N3, N4 no DECOY de producao (em processo; PRODUCAO, EVENTOS_QUADRO e a sonda do servico trocados)
MAN_PD = sha(PD_PRIST / "canonical_contracts.json")


def pd_intocado(j, a, d):
    return a == d and sha(PD / "canonical_contracts.json") == MAN_PD


decoy("N1_decoy_Xn3_replay_recibo_de_4_campos", 3, veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", kernel=FIX["r2_minimo_4_campos"][0],
      extra_ok=lambda j, a, d: pd_intocado(j, a, d) and testes(j)["T17_LEAN_KERNEL"]["resultado"] == "FALHA",
      nota="N1 (ALTA), o Xn3 da re-auditoria refeito: na R2 a producao-decoy foi APLICADA com um recibo do kernel de 4 campos; na R3 o T17 FALHA e nada se grava")
decoy("N2_decoy_producao_sem_sha_do_pre_selo", 2, "RECIBO_PRE_SELO_SHA_AUSENTE", pre_sha=None, extra_ok=pd_intocado,
      nota="N2: na producao (decoy) o recibo pre-selo sem --recibo-pre-selo-sha256 e recusado")
pre_mao = FX / "PRE_escrito_a_mao.json"
rjm = json.loads(R_PD.read_bytes())
rjm["nota_do_ataque"] = "recibo pre-selo escrito a mao: o conteudo confere, o pino nao"
pre_mao.write_bytes(json.dumps(rjm, ensure_ascii=False).encode("utf-8"))
decoy("N2_decoy_recibo_pre_selo_escrito_a_mao", 2, "RECIBO_PRE_SELO_SHA_DIVERGE", pre=pre_mao, pre_sha=sha(R_PD), extra_ok=pd_intocado,
      nota="N2: o A6n da re-auditoria: um recibo pre-selo de conteudo valido escrito a mao e ACEITO na R2; na R3 o sha pinado (vNNN_pins) nao bate")
decoy("N2_decoy_ensaio_producao_sem_sha_do_pre_selo", 2, "RECIBO_PRE_SELO_SHA_AUSENTE", pre_sha=None, modo="ensaio", evento=None, evento_hash=None, extra_ok=pd_intocado,
      nota="N2: em --producao a flag e exigida tambem no ensaio")
decoy("N3_decoy_servico_no_ar_no_inicio", 2, "SERVICO_NO_AR", sondas=(True,), extra_ok=pd_intocado, nota="o comportamento da R2, mantido")
decoy("N3_decoy_servico_volta_durante_a_bateria", 2, "SERVICO_VOLTOU_ANTES_DE_GRAVAR", sondas=(False, True), extra_ok=pd_intocado,
      nota="N3: o SVCb da re-auditoria: o servico sobe durante a bateria; na R2 a gravacao acontecia; na R3 a sonda imediatamente antes do backup recusa (nada gravado)")


def _so_backup_novo(j, a, d):
    novos = sorted(set(d) - set(a))
    return sha(PD / "canonical_contracts.json") == MAN_PD and all(".bak_B3_" in n for n in novos) and len(novos) == 1 and \
        not (PD / "CONTRATO_CANONICO_B3.md").exists() and all(a[k] == d[k] for k in a)


decoy("N3_decoy_servico_volta_antes_do_contrato", 2, "SERVICO_VOLTOU_ANTES_DE_GRAVAR", sondas=(False, False, True), extra_ok=_so_backup_novo,
      nota="N3: volta entre o backup e o contrato: recusa; o manifesto intocado, nenhum contrato; so o backup de bytes fica (backups nunca se apagam)")
decoy("N3_decoy_servico_volta_imediatamente_antes_da_troca", 2, "SERVICO_VOLTOU_ANTES_DE_GRAVAR", sondas=(False, False, False, False, True), extra_ok=_so_backup_novo,
      nota="N3: volta no ultimo instante antes do os.replace: recusa; o contrato novo e o temporario sao desfeitos")
decoy("N3_decoy_servico_volta_antes_do_recibo_em_estado", 2, "APLICACAO_REVERTIDA", sondas=(False, False, False, False, False, True), extra_ok=_so_backup_novo,
      nota="N3: volta depois da troca, antes do recibo em estado/: o manifesto anterior volta byte a byte (rollback) e o contrato sai")
MUTADO = {}
ORIG_RB = MOD.rodar_bateria


def rb_mutante(*a, **k):
    r = ORIG_RB(*a, **k)
    p_ = PD / "canonical_contracts.json"
    p_.write_bytes(p_.read_bytes() + b"\n")          # a mudanca concorrente durante a bateria (o JSON segue valido)
    MUTADO["sha"] = sha(p_)
    return r


decoy("N4_decoy_manifesto_muda_durante_a_bateria", 2, "MANIFESTO_MUDOU_DESDE_A_LEITURA", patches_extra=dict(rodar_bateria=rb_mutante),
      extra_ok=lambda j, a, d: sha(PD / "canonical_contracts.json") == MUTADO.get("sha") != MAN_PD and not (PD / "CONTRATO_CANONICO_B3.md").exists()
      and not any(".bak_B3_" in n for n in d),
      nota="N4: o Xn2 da re-auditoria: na R2 a mudanca concorrente era apagada (atualizacao perdida, so no .bak); na R3 o aplicar compara com os bytes do passo 3 e recusa: a mudanca fica")
decoy("N1_decoy_contraprova_recibo_valido_aplica", 0, veredito_esp="REPINADA_B3__APLICADA",
      extra_ok=lambda j, a, d: (lambda rec: rec["producao"] is True and rec["evento_c1"]["verificado"] is True and testes(j)["T17_LEAN_KERNEL"]["resultado"] == "PASSA" and
                                "cruzado com o recibo pre-selo" in testes(j)["T17_LEAN_KERNEL"]["detalhe"] and sha(PD / "canonical_contracts.json") == rec["manifesto_novo"]["sha256"] and
                                rec["manifesto_novo"]["kernel_recibo_sha256_encadeado"] == K_OK_SHA and [s["no_ar"] for s in rec["sondagens_do_servico"]] == [False] * 6 and
                                Path(rec["aplicacao"]["copia_do_recibo"]).exists())(recibo_de(j)),
      nota="contraprova do decoy: com o recibo do kernel valido, os pinos (N1, N2), o hash do elo (N6) e o servico parado nas 6 sondagens (N3), a producao-decoy e aplicada")
decoy_reset()

# ================================================================ run 2: o elo B3 na copia b2, com TUDO pinado e encadeado
MAN_B2_ANTES = sha(B2 / "canonical_contracts.json")
d2, j2 = run("RUN_2_pos_selo_aplicar_b2", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                           "--evento", str(ELOS["valido"]["seq"]), "--evento-hash", H("valido"), "--eventos", EV_SB, "--recibo-pre-selo", R1B, "--recibo-pre-selo-sha256", sha(R1B),
                                           "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 0,
             veredito_esp="REPINADA_B3__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", saida=S / "2",
             extra_ok=lambda j, r: (lambda rec: rec["bateria_resultado"]["falha"] == 0 and rec["bateria_resultado"]["passa"] == 13 and rec["bateria_resultado"]["nao_executado"] == 1 and
                                    testes(j)["T17_LEAN_KERNEL"]["resultado"] == "PASSA" and "cruzado com o recibo pre-selo" in testes(j)["T17_LEAN_KERNEL"]["detalhe"] and
                                    testes(j)["T16_DEPLOY_FIXTURE"]["resultado"] == "PASSA" and isolado(rec, S / "2") and
                                    rec["pino_velho_recusado_pelo_instalado"] == "PIN_CHANGED" and rec["evento_c1"]["verificado"] is True and rec["evento_c1"]["evento"] == ELOS["valido"]["seq"] and
                                    rec["evento_c1"]["hash_conferido"] == H("valido") and
                                    rec["recibo_pre_selo"]["sha256"] == sha(R1B) and rec["manifesto_novo"]["recibo_pre_selo_sha256_encadeado"] == sha(R1B) and
                                    rec["manifesto_novo"]["kernel_recibo_sha256_encadeado"] == K_OK_SHA and
                                    sha(B2 / "canonical_contracts.json") == rec["manifesto_novo"]["sha256"] and sha(rec["aplicacao"]["backup"]) == MAN_B2_ANTES and
                                    rec["aplicacao"]["manifesto_lido_no_passo_3_sha256"] == MAN_B2_ANTES and
                                    (B2 / "CONTRATO_CANONICO_B3.md").exists() and Path(rec["aplicacao"]["copia_do_recibo"]).exists() and rec["aplicacao"]["pos_conferencia"]["ok"] is True and
                                    rec["aplicacao"]["pos_conferencia"]["canonical_version"] == "v392" and rec["nos"]["beta_runtime"] == rec["aplicacao"]["pos_conferencia"]["beta_tgl"].__repr__() and
                                    not tem_pycache(B2))(recibo_de(j)),
             nota="o elo B3 do sandbox (R3): PIN_CHANGED real; evento encadeado com hash conferido (N6); recibo pre-selo por sha (N2) e encadeado; T17 pelo recibo do kernel VINCULADO ao manifesto "
                  "do kernel pinado pelo selo e com o ANTES cruzado (N1); bateria 13 PASSA isolada (N5); manifesto B3 gravado em b2 com backup, contrato e recibo em estado/sincronizacao")
run("RUN_2bis_idempotente", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                             "--evento", str(ELOS["valido"]["seq"]), "--evento-hash", H("valido"), "--eventos", EV_SB, "--recibo-pre-selo", R1B, "--recibo-pre-selo-sha256", sha(R1B),
                             "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 0, veredito_esp="JA_SINCRONIZADA__NADA_A_GRAVAR", bancada=B2,
    nota="repetir o B3 ja aplicado: a bateria roda de novo na copia, nada se grava (idempotencia)")
run("POS_estado_final_b2_v392_ensaio", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT, "--sem-bateria"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B2,
    nota="estado final: b2 sincronizada em v392 (ensaio sem bateria, so leitura)")

# ================================================================ fecho: juncoes desfeitas PRIMEIRO; a producao, o Nos e o livro real intocados
for jj in JUNCOES:
    if jj.is_junction():
        os.rmdir(jj)          # remove a JUNCAO (nunca o alvo)
juncoes_restantes = [str(jj) for jj in JUNCOES if os.path.lexists(jj)]
assert sorted(os.listdir(PROD)) == PROD_LISTA_ANTES, "a lista da producao mudou"
assert sorted(os.listdir(NOS_REAL)) == NOS_LISTA_ANTES, "a lista do Nos mudou"
EV_REAL_BYTES_DEPOIS = EVENTOS_REAL.read_bytes()
assert EV_REAL_BYTES_DEPOIS.startswith(EV_REAL_BYTES_ANTES), "o livro real de eventos foi REESCRITO (nao so acrescido)"
EV_N_ANTES, EV_N_DEPOIS = len(EV_REAL_BYTES_ANTES.splitlines()), len(EV_REAL_BYTES_DEPOIS.splitlines())
EV_NOVOS = [json.loads(l) for l in EV_REAL_BYTES_DEPOIS[len(EV_REAL_BYTES_ANTES):].decode("utf-8").splitlines() if l.strip()]
assert not any(e.get("tipo") == "SINCRONIZACAO_BANCADA" for e in EV_NOVOS), "nasceu no livro real um elo SINCRONIZACAO_BANCADA durante os controles"
assert sha(PROD / "canonical_contracts.json") == PROD_MAN_ANTES == SBM["manifesto_producao_sha256"], "o manifesto de producao mudou"
n_pass = sum(1 for x in RES if x["passa"])
nomes = [x["controle"] for x in RES]
assert len(nomes) == len(set(nomes)), "nome de controle repetido"
R2_NOMES = [c["controle"] for c in json.loads((R2 / "CONTROLES_NEGATIVOS_R2.json").read_bytes())["controles"]]
faltam_r2 = sorted(set(R2_NOMES) - set(nomes))
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3 (13/10/2026)", raiz=str(RAIZ), script_sha256=sha(SYNC), bateria_sha256=BAT_SHA,
           gerar_canais_sha256=sha(GER), montar_sandbox_sha256=sha(AQUI / "montar_sandbox.py"), controles_sha256=sha(Path(__file__)), segundos=round(time.time() - T0, 1),
           n=len(RES), passam=n_pass, n_da_R2=len(R2_NOMES), da_R2_presentes=len(R2_NOMES) - len(faltam_r2), da_R2_ausentes=faltam_r2, n_novos_R3=len(RES) - (len(R2_NOMES) - len(faltam_r2)),
           producao_intocada=dict(lista_igual=True, manifesto_sha256=sha(PROD / "canonical_contracts.json")), nos_real_intocado=True, eventos_jsonl_real_sha256=EV_REAL_SHA_ANTES,
           eventos_jsonl_real=dict(sha256_antes=EV_REAL_SHA_ANTES, sha256_depois=sha_b(EV_REAL_BYTES_DEPOIS), so_cresceu=True, linhas_antes=EV_N_ANTES, linhas_depois=EV_N_DEPOIS,
                                   elos_novos_de_outras_sessoes=[dict(seq=e.get("seq"), tipo=e.get("tipo"), quem=e.get("quem")) for e in EV_NOVOS],
                                   nota="o livro e vivo; este script nunca o abre para escrita; confere-se que so cresceu (prefixo de bytes) e que nenhum elo de sincronizacao nasceu"),
           juncoes_criadas=[str(jj) for jj in JUNCOES], juncoes_restantes=juncoes_restantes,
           controles=RES, veredito=("TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" if n_pass == len(RES) and not faltam_r2 and not juncoes_restantes else "ALGUM_CONTROLE_NAO_RECUSOU"),
           nota="NOT_FALSIFIED nunca e creditacao; nada aqui move o gate; nenhum dado observado; a producao, o Nos e o livro de eventos real foram so lidos; "
                "a producao foi simulada por decoy EM PROCESSO numa copia (pd/)")
texto = json.dumps(out, ensure_ascii=False, indent=1, default=str)
assert not MOD.contem_palavra(texto), "a palavra guardada apareceu no resultado dos controles"
(AQUI / "CONTROLES_NEGATIVOS_R3.json").write_bytes(texto.encode("utf-8"))
print(out["veredito"], "%d/%d" % (n_pass, len(RES)), "R2 presentes %d/%d" % (out["da_R2_presentes"], len(R2_NOMES)), "%.0f s" % out["segundos"])
