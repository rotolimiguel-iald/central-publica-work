# -*- coding: utf-8 -*-
"""controles_negativos_r3_5.py (R3.5, 19/10/2026) -- os 547 da R3.4 (nomes mantidos; a familia b1 e os controles que liam o Nos REAL migrados para o stand-in da custodia v393 -- o Nos real esta no meio do rito da v394 --, e os 3 controles da varredura de auditoria que a lista de PERMISSAO estrita muda de forma) e os NOVOS (prefixos R35_M_ evasoes do modulo de auditoria, R35_V_ validade do recibo pre_selo real da R3.4, R35_P_ a bateria da v394 contra o candidato real). Da R3.4: controles_negativos_r3_4.py (R3.4, 19/10/2026) -- os 401 da R3.3 (nomes mantidos; os da familia b1 e os runs 1a/1b migrados para o estado de hoje: producao B3/v392, Nos real v393, bateria por versao) e os NOVOS (prefixos R34_S_ salto, R34_P_ bateria por versao, R34_M_ modulos de auditoria). Da R3.3: os 399 da R3.2 (nomes mantidos) e 2 NOVOS (prefixo R33_), os casos EXATOS da reauditoria a70d70d5:
R32-A (-I -B -X utf8 -i com PYTHONSTARTUP) e R32-B (mudanca logo depois do os.replace do rollback -> ROLLBACK_DIVERGE). Todo subprocesso do esboco roda
com -I -B -X utf8 e este script tambem. uso: python -I -B -X utf8 controles_negativos_r3_3.py <raiz curta C:/t/vb*>
Da R3.2: os 337 controles da R3.1 (nomes mantidos; os que mudaram de formato listados com motivo em
CONTROLES_NEGATIVOS_R3_2.json) e os NOVOS da R3.2 (prefixo R32_), o caso EXATO do auditor e uma variante para cada achado da reauditoria
a721b706 (R31-1 a R31-6) e para o item 3 da 12-ter do plano. Todo subprocesso do esboco roda com -I -B -X utf8 (R31-1), e ESTE script tambem
tem de rodar assim (as chamadas em processo de main() conferem o interpretador corrente). Com --recibo-pre-selo, todo comando recebe
--selo-anterior/--kernel-manifesto-anterior (a custodia v391 do sandbox, fx/custodia_v391), porque o B(n) R3.2 exige o pino externo (R31-3).
uso: python -I -B -X utf8 controles_negativos_r3_2.py <raiz curta C:/t/vb*>
Da R3.1: controles_negativos_r3_1.py (R3.1, 13/10/2026) -- os 235 controles da R3 (nomes mantidos; os que mudaram de formato listados com
motivo em CONTROLES_NEGATIVOS_R3_1.json) e os NOVOS da R3.1 (prefixo R31_), um ou mais por achado da reauditoria curta a61fad96 (A1, A1b,
A2, A3, A4, N1k, N1l, N1m, N2c, N3a, N4b), no formato REAL: a linha verbatim do aviso de sorry do Lean 4.31 lida de um log do Nos
(bancada_corpus, so leitura) e os ataques do auditor refeitos. Com --kernel-recibo, todo comando recebe --criterios/--criterios-sha256
(o CRITERIOS sintetico pinado), porque o B(n) R3.1 exige os esperados pinados (A3).
Da R3: roda o sandbox COMPLETO do vinculo em raiz curta (C:/t/vb*) e TODOS os controles negativos:
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
Saida: R3_1/CONTROLES_NEGATIVOS_R3_1.json e <raiz>/s/*. uso: controles_negativos_r3_1.py <raiz curta C:/t/vb*>"""
import sys
sys.dont_write_bytecode = True
import contextlib, copy, datetime, hashlib, importlib.util, io, json, os, shutil, subprocess, time, zipfile
from pathlib import Path
assert sys.flags.isolated and sys.flags.dont_write_bytecode and sys.flags.utf8_mode, "R3.4 (R31-1): rode com python -I -B -X utf8"

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
NOS_STAND, B1R, B1S394, NOS394S = RAIZ / "nos_real", RAIZ / "b1real", RAIZ / "b1v394s", RAIZ / "nos_v394s"   # R3.5: o stand-in do Nos v393 (custodia), b1real (pina o caminho real), o stand-in do v394
R34 = AQUI.parent / "R3_4"
def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha(p):
    return sha_b(Path(p).read_bytes())


SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R3_5.json").read_text(encoding="utf-8"))
VR = SBM["nos_real"]["versao"]                       # R3.4: a versao do Nos REAL de hoje (v393): a familia b1 usa esta versao onde a R3.3 usava v391
VR_ERRADA = "v%d" % (int(VR[1:]) + 1)                # uma versao que o Nos real nao tem
PASTA_R33 = AQUI.parent / "R3_3"             # (R33 e um dicionario mais abaixo, do controle R32-B)
GERAR_CADEIA = AQUI / "gerar_cadeia_de_selos.py"
R31 = AQUI.parent / "R3_1"
R32 = AQUI.parent / "R3_2"
# R31-3 (R3.2): a custodia v391 do sandbox (o selo e o manifesto do kernel da versao anterior), gravada pelo montar_sandbox antes do "selo"
SELO_ANT = FX / "custodia_v391" / "um_absoluto_selo.json"
KMAN_ANT = FX / "custodia_v391" / "tgl_kernel_proof_manifest.json"
assert sha(SELO_ANT) == SBM["nos"]["selo"]["sha256"] and sha(KMAN_ANT) == SBM["nos"]["kernel_manifest"]["sha256"], "custodia v391 do sandbox"
SEM_SELO_ANT = set()      # controles que testam a AUSENCIA do selo anterior (sem injecao)
INJETADOS_SELO = []
INJETADOS_NOS = []        # R3.5: controles cujo comando ganhou --nos <stand-in v393 da custodia> (antes liam o Nos real por omissao)       # controles cujo comando ganhou --selo-anterior/--kernel-manifesto-anterior (mudanca de formato registrada)
R3 = AQUI.parent / "R3"
ELOS = SBM["fx"]["elos_de_ensaio"]
EV_SB = FX / "eventos_sandbox.jsonl"
K_OK = FX / "KERNEL_RECIBO_v392_SINTETICO_VALIDO.json"
TK_A = "TGL_PRO" + "VED"          # a palavra guardada, so montada em RAM (nunca escrita em disco por este arquivo)
TK_C = "CONF" + "IRMED"
S.mkdir(exist_ok=True)
T0 = time.time()
RES = []
JUNCOES = []


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


def run(nome, args, rc_esp, recusa_esp=None, bancada=None, saida=None, flags=("-I", "-B", "-X", "utf8"), sync=None, veredito_esp=None, extra_ok=None, nota="",
        env_extra=None, sem_criterios=False):
    """roda o esboco num subprocesso; confere rc, codigo da recusa (prefixo), veredito e que a copia nao mudou (fotografia por sha256).
    R3.1: com --kernel-recibo e sem --criterios, injeta --criterios/--criterios-sha256 (o CRITERIOS sintetico) e registra o nome."""
    args = com_nos_stand(nome, com_criterios(nome, args, sem_criterios))
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


def inproc(nome, argv, rc_esp, recusa_esp=None, veredito_esp=None, patches=None, bancada=None, extra_ok=None, nota="", sem_criterios=False):
    """roda main() EM PROCESSO com atributos do modulo trocados (decoy de producao, sonda do servico simulada, bateria instrumentada).
    Nenhum argumento pode apontar para a producao real nem para o Nos real; os atributos voltam no fim. R3.1: injecao dos criterios."""
    argv = com_criterios(nome, argv, sem_criterios)
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


def _conferir_pre(*a_):
    """R31-3 (R3.2): conferir_recibo_pre_selo com o pino externo (a custodia v391 do sandbox)."""
    return MOD.conferir_recibo_pre_selo(*a_, selo_anterior=SELO_ANT, kernel_manifesto_anterior=KMAN_ANT)

# ================================================================ R3.1: o CRITERIOS sintetico pinado (A3) e a amostra REAL do sorry (A1)
CRIT = FX / "CRITERIOS_v392_SINTETICO.json"
CRIT_SHA = sha(CRIT)
CRIT_OBJ = MOD.carregar_criterios(CRIT, CRIT_SHA, "v392")
CRIT_MODELO = AQUI / "CRITERIOS_V392.json"
AMOSTRA = SBM["fx"]["amostra_sorry_lean431"]
LINHA_REAL = bytes.fromhex(AMOSTRA["linha_hex"])          # a linha verbatim do log real do Nos (com o CR do CRLF)
assert b"declaration uses `sorry`" in LINHA_REAL and sha(AMOSTRA["path"]) == AMOSTRA["sha256"], "a amostra real nao confere"
SITE_REAL = MOD.site_do_usuario_real()
INJETADOS = []   # controles cujo comando ganhou --criterios/--criterios-sha256 (A3): mudanca de formato registrada


CRIT_POR_VERSAO = {"v392": (CRIT, CRIT_SHA)}


def crit_para(versao):
    """o CRITERIOS sintetico da versao do comando (o B(n) recusa criterios de outra versao): para v392, o do sandbox; para outra (os
    controles antigos que rodam com --versao v391 e --kernel-recibo), uma copia com SO a versao trocada, pinada por sha."""
    if versao not in CRIT_POR_VERSAO:
        c_ = json.loads(CRIT.read_bytes())
        c_["versao"] = versao
        p_ = FX / ("CRITERIOS_%s_SINTETICO.json" % versao)
        p_.write_bytes(json.dumps(c_, ensure_ascii=False, indent=1).encode("utf-8"))
        CRIT_POR_VERSAO[versao] = (p_, sha(p_))
    return CRIT_POR_VERSAO[versao]


def com_nos_stand(nome, args):
    """R3.5: o Nos REAL esta no meio do rito da v394 (um.py v394 instalado, selo v393): nao se le. Todo comando do sandbox sem --nos (que lia o Nos real por omissao) le o stand-in v393 (nos_real/, copia de bytes da custodia)."""
    a = [str(x) for x in args]
    if "--nos" not in a:
        INJETADOS_NOS.append(nome)
        a = a + ["--nos", str(NOS_STAND)]
    return a


def com_criterios(nome, args, sem_criterios=False):
    a = [str(x) for x in args]
    if not sem_criterios and "--kernel-recibo" in a and "--criterios" not in a and "--criterios-sha256" not in a:
        v_ = a[a.index("--versao") + 1] if "--versao" in a and a.index("--versao") + 1 < len(a) else "v392"
        v_ = v_ if (v_.startswith("v") and v_[1:].isdigit()) else "v392"
        p_, s_ = crit_para(v_)
        INJETADOS.append(nome)
        a = a + ["--criterios", str(p_), "--criterios-sha256", s_]
    # R31-3 (R3.2): com --recibo-pre-selo, o pino externo do kernel anterior (a custodia v391 do sandbox), salvo nos controles da ausencia
    if "--recibo-pre-selo" in a and "--selo-anterior" not in a and "--kernel-manifesto-anterior" not in a and nome not in SEM_SELO_ANT:
        INJETADOS_SELO.append(nome)
        a = a + ["--selo-anterior", str(SELO_ANT), "--kernel-manifesto-anterior", str(KMAN_ANT)]
    return a


PROD_LISTA_ANTES = sorted(os.listdir(PROD))
NOS_LISTA_ANTES = sorted(os.listdir(NOS_REAL))
NOS_UM_SHA_ANTES = sha(NOS_REAL / "um.py")        # R3.5: so para registrar que este script nao mexeu (o rito escreve no Nos, nao este script)
EV_REAL_BYTES_ANTES = EVENTOS_REAL.read_bytes()   # o livro e VIVO (outras sessoes anotam): confere-se que so cresceu, nunca que ficou igual
EV_REAL_SHA_ANTES = sha_b(EV_REAL_BYTES_ANTES)
PROD_MAN_ANTES = sha(PROD / "canonical_contracts.json")


def isolado(rec, saida):
    """N5 + A4 (R3.1): todo teste executado rodou com -E -P -s logo apos o interpretador e pelo lancador pinado (sha conferido), ambiente
    sem PYTHON* herdado, APPDATA numa pasta vazia nova sob --saida, cwd numa pasta vazia nova sob --saida; o recibo traz o residuo."""
    ex = [t for t in rec["bateria_resultado"]["testes"] if t.get("comando_executado")]
    prep = rec["bateria_resultado"]["isolamento"].get("preparado") or {}
    return bool(ex) and prep.get("lancador", {}).get("sha256") == MOD.LANCADOR_SHA256 and "residuo_declarado" in prep and all(
        t["comando_executado"][1:4] == ["-E", "-P", "-s"] and any(Path(x).name == MOD.LANCADOR_NOME for x in t["comando_executado"])
        and Path(t["cwd"]).parent == Path(saida) / "cwd_testes" and Path(t["isolamento"]["appdata"]).parent == Path(saida) / "appdata_vazio"
        and t["isolamento"]["lancador_sha256"] == MOD.LANCADOR_SHA256 for t in ex)


# ================================================================ R3.4 (P): as baterias POR VERSAO, geradas por script (o T12 da R2 pina o um.py v391)
GEN_BAT = AQUI / "gerar_bateria_r3_4.py"
DRV_BAT = AQUI / "bateria_r3_4" / "t12_t14_atrator_r3_4.py"
PINOS_BN_REAL = WORK / "cadeia_de_selo" / VR / ("PINOS_BN_%s.json" % VR)


def gerar_bateria_r34(nome, versao, nos_dir, real=False, base=None):
    """roda gerar_bateria_r3_4.py (subprocesso, -I -B -X utf8): devolve (bateria, sha256, pino). real=True: pinos da cadeia (PINOS_BN) da versao instalada; senao, sandbox."""
    pino, saida = FX / ("PINO_UM_PY_%s.json" % nome), FX / ("BATERIA_R34_%s.json" % nome)
    base = base or BAT
    cmd = [PY, "-I", "-B", "-X", "utf8", str(GEN_BAT), "--base", str(base), "--base-sha256", sha(base), "--versao", versao, "--nos", str(nos_dir), "--driver", str(DRV_BAT),
           "--pino-saida", str(pino), "--saida", str(saida)] + (["--pinos-bn", str(PINOS_BN_REAL)] if real else ["--sandbox"])
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stdout + r.stderr
    return saida, sha(saida), pino


BAT_REAL, BAT_REAL_SHA, PINO_REAL = gerar_bateria_r34("real_" + VR, VR, NOS_STAND, real=True)
BAT_V391, BAT_V391_SHA, PINO_V391 = gerar_bateria_r34("v391_copia", "v391", NOS)

# ================================================================ run 1a e 1b (a bateria inteira, pre_selo, ensaio)
run("RUN_1a_pre_selo_b1_nos_real", ["--bancada", B1, "--versao", VR, "--bateria", BAT_REAL, "--bateria-sha256", BAT_REAL_SHA, "--modo", "ensaio", "--fase", "pre_selo"], 0,
    veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1, saida=S / "1a",
    extra_ok=lambda j, r: (lambda rec: rec["bateria_resultado"]["falha"] == 0 and rec["bateria_resultado"]["passa"] == 13 and
                           testes(j)["T16_DEPLOY_FIXTURE"]["resultado"] == "PASSA" and testes(j)["T12_T13_T14_ATRATOR"]["resultado"] == "PASSA" and
                           rec["nos"]["um_py"]["sha256"] == SBM["nos_real"]["um_py"]["sha256"] and rec["manifesto_anterior"]["pina_o_nos_real"] is False and
                           rec["nos"]["kernel"]["raiz_sha256"] == SBM["nos_real"]["kernel"]["raiz_sha256"] and isolado(rec, S / "1a")
                           and rec["bateria"]["pinos_da_versao"]["conferidos_contra_o_nos_lido"] is True and rec["bateria"]["pinos_da_versao"]["versao"] == VR)(recibo_de(j)),
    nota="etapa 1 da cadeia: os testes finais contra a v391 ainda canonica, Nos REAL, bateria inteira (T16 em raiz curta; T12-T14 pre-selo); R3: cada teste com -E -P, "
         "ambiente sem PYTHON* e cwd vazio novo; o recibo traz o kernel v391 lido do manifesto pinado pelo selo")
run("RUN_1b_pre_selo_b2_nos_copia", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT_V391, "--bateria-sha256", BAT_V391_SHA, "--modo", "ensaio", "--fase", "pre_selo"], 0,
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


def decoy(nome, rc_esp, recusa_esp=None, veredito_esp=None, sondas=(False,), patches_extra=None, extra_ok=None, nota="", sem_criterios=False, **kw):
    decoy_reset()
    patches = dict(PRODUCAO=PD, EVENTOS_QUADRO=EV_SB, servico_responde=sonda_seq(list(sondas)))
    patches.update(patches_extra or {})
    return inproc(nome, decoy_args(S / nome, **kw), rc_esp, recusa_esp, veredito_esp, patches=patches, bancada=PD, extra_ok=extra_ok, nota=nota,
                  sem_criterios=sem_criterios)


# ================================================================ controles ANTES do selo
# --- os 7 da R1
run("C1_versao_errada", ["--bancada", B1, "--versao", VR_ERRADA, "--bateria", BAT, "--sem-bateria"], 2, "SELO_VERSAO_DIFERENTE", bancada=B1)
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
jb1 = juncao(RAIZ / "jb1", B1R)
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
run("A2_B1_replay_prefixo_sandbox_aplicar_b1", ["--bancada", "\\\\?\\" + str(B1R), "--versao", VR, "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar",
                                               "--fase", "pos_selo", "--evento", "SANDBOX:B1 prefixo"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1R,
    nota="o ataque B1 (ALTA) da auditoria R1: na R1 gravou o manifesto B3 na copia; desde a R2 a forma do caminho e normalizada e --sandbox e recusado porque o manifesto pina o Nos real")
run("A2_B1_replay_juncao_sandbox_aplicar_b1", ["--bancada", jb1, "--versao", VR, "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar",
                                              "--fase", "pos_selo", "--evento", "SANDBOX:B1 juncao"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1R)
run("A2_sandbox_em_copia_que_pina_o_nos_real_ensaio", ["--bancada", B1R, "--versao", VR, "--bateria", BAT, "--sem-bateria", "--sandbox"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1R)
run("A2_producao_flag_em_copia_e_aceito_sem_efeito", ["--bancada", B1, "--versao", VR, "--bateria", BAT, "--sem-bateria", "--producao"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1,
    nota="--producao numa copia nao e erro (A12 da auditoria R1): o recibo diz producao=false", extra_ok=lambda j, r: recibo_de(j)["producao"] is False)
# --- N13: Volume{GUID}, GLOBALROOT e \??\ -- recusa por REGRA explicita (na R2, por acidente)
GUID = "{12345678-1234-1234-1234-123456789abc}"
for k, f, esp in (("volume_guid_prefixo_longo", "\\\\?\\Volume" + GUID + "\\IALD\\Bancada_Um", "CAMINHO_VOLUME_GUID_NAO_ADMITIDO"),
                  ("volume_guid_prefixo_ponto", "\\\\.\\Volume" + GUID + "\\IALD\\Bancada_Um", "CAMINHO_VOLUME_GUID_NAO_ADMITIDO"),
                  ("globalroot", "\\\\?\\GLOBALROOT\\Device\\HarddiskVolume3\\IALD\\Bancada_Um", "CAMINHO_DISPOSITIVO_NAO_ADMITIDO"),
                  ("pipe", "\\\\.\\pipe\\bancada", "CAMINHO_DISPOSITIVO_NAO_ADMITIDO")):
    run("N13_bancada_%s" % k, ["--bancada", f, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, esp,
        extra_ok=lambda j, r: j.get("recibo") is None, nota="N13: a forma %r e recusada por regra explicita, antes de qualquer leitura; nada gravado" % f)
run("N13_saida_volume_guid", ["--bancada", B1, "--versao", VR, "--bateria", BAT, "--sem-bateria"], 2, "CAMINHO_VOLUME_GUID_NAO_ADMITIDO", bancada=B1,
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
    run("A5_saida_%s" % k, ["--bancada", B1, "--versao", VR, "--bateria", BAT, "--sem-bateria"], 2, esp, bancada=B1, saida=sd,
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
run("A8_mesma_versao_hash_diferente", ["--bancada", b1x, "--versao", VR, "--bateria", BAT, "--sem-bateria"], 2, "SELO_PROGRAMA_DIVERGE", bancada=b1x,
    nota="o ataque A5 da auditoria R1: manifesto v391 com outro sha do um.py; o disco tem a v391 real")
run("A8_reparo_em_ensaio_recusado", ["--bancada", b1x, "--versao", VR, "--bateria", BAT, "--sem-bateria", "--reparo-de-pino"], 2, "REPARO_SO_EM_APLICAR", bancada=b1x)
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
run("A9_sem_B_nenhum_pycache", ["--bancada", B1, "--versao", VR, "--bateria", BAT, "--sem-bateria"], 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B1, flags=("-I", "-X", "utf8"),
    extra_ok=lambda j, r: not tem_pycache(B1) and j.get("recibo") is None and "-B" in str(j.get("recusa")),
    nota="o ataque B3 da auditoria R1: na R1 nascia bancada/__pycache__/canonical.*.pyc; desde a R2 sys.dont_write_bytecode=True no topo. R3.2 (R31-1): sem -B o "
         "esboco recusa antes de qualquer import (INTERPRETADOR_NAO_ISOLADO) e nenhum __pycache__ nasce")
run("R32_A9_com_I_e_B_nenhum_pycache", ["--bancada", B1, "--versao", VR, "--bateria", BAT, "--sem-bateria"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1,
    extra_ok=lambda j, r: not tem_pycache(B1) and recibo_de(j)["python_dont_write_bytecode"] is True and recibo_de(j)["python_isolado"]["dont_write_bytecode_flag"] is True,
    nota="R3.2: com -I -B -X utf8 (a chamada exigida) o canonical.py instalado e importado e nenhum __pycache__ nasce")

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
run("A10_traversal_em_code_path", ["--bancada", b1t, "--versao", VR, "--bateria", BAT, "--sem-bateria", "--forcar-regeracao"], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=b1t,
    extra_ok=lambda j, r: not (S / "A10_traversal_em_code_path" / "raiz" / "candidate").exists() and not (S / "fora" / "evil.py").exists() and not (S / "A10_traversal_em_code_path" / "fora").exists(),
    nota="o ataque A1 da auditoria R1: code[].path com '..' escapava de --saida no staging")
run("A10_traversal_em_code_path_ja_sincronizada", ["--bancada", b1t, "--versao", VR, "--bateria", BAT, "--sem-bateria"], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=b1t)
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
PRE = _conferir_pre(R1B, MOD.estado_anterior(B2, MOD.carregar_canonical(B2)[0]), B2, False, sha(R1B))

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
    # R3.1 (A1): o controle antigo usava o formato de aspas simples (o mesmo da regex da R3: confirmava-se a si mesmo); agora a linha e
    # a VERBATIM do aviso real do Lean 4.31 (crases), lida de um log do Nos; o de aspas fica num controle proprio
    log_com_sorry=(kfix("log_com_sorry", lambda k: k.update(build_full_log=log_fix("build_com_sorry", log_b_ok + LINHA_REAL.decode("utf-8") + "\n"))),
                   "ocorrencia(s) de sorry"),
    log_com_sorry_aspas=(kfix("log_com_sorry_aspas", lambda k: k.update(build_full_log=log_fix("build_com_sorry_aspas", log_b_ok + "TGLExt/PedraSinteticaA.lean:3:8: warning: declaration uses 'sorry'\n"))),
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
    toolchain_diverge=(kfix("toolchain_diverge", lambda k: k["toolchain"].update(lean_version=["Lean (version 4.30.0)"])), "toolchain"),   # R3.1: lista (N1m)
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
    passa_ret, det, _ = MOD.verificar_kernel_recibo(kp, "v392", NI392, sha(kp), None, True, CRIT_OBJ)
    _registrar(dict(controle="N1_unit_kernel_recibo_%s" % nome, nivel="unitario", detalhe=det[:300], esperado_no_detalhe=contem,
                    nota="N1: verificar_kernel_recibo(%s) recusa" % kp.name), passa_ret is False and contem in det)


def _unit_k(nome, esperado_ok, contem, ni=None, sha_=None, pre=None, sandbox=True, kp=K_OK, nota=""):
    passa_ret, det, _ = MOD.verificar_kernel_recibo(kp, "v392", ni or NI392, sha_, pre, sandbox, CRIT_OBJ)
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
ni_tc = dict(NI392, kernel=dict(NI392["kernel"], lean_version=["Lean (version 9.9.9)"]))   # R3.1: lista (N1m)
_unit_k("N1_unit_manifesto_toolchain_diverge", False, "toolchain", ni=ni_tc, sha_=K_OK_SHA)

# ================================================================ R3.1: A1, A1b, A2, A3, N1k, N1l, N1m, N2c -- no formato REAL
def _kr(nome, mut):
    """um recibo do kernel derivado do valido (contrato KERNEL_RECIBO_R3_1); devolve o caminho."""
    return kfix("R31_" + nome, mut)


def _ku(nome, kp, contem, ni=None, pre=None, sandbox=True, criterios="auto", nota="", aceita=False):
    """controle unitario de verificar_kernel_recibo: recusa com `contem` no detalhe (ou aceita, na contraprova)."""
    passa_ret, det, pino_ = MOD.verificar_kernel_recibo(kp, "v392", ni or NI392, sha(kp), pre, sandbox, CRIT_OBJ if criterios == "auto" else criterios)
    ok = (passa_ret is True) if aceita else (passa_ret is False and contem in det)
    _registrar(dict(controle=nome, nivel="unitario", detalhe=det[:400], esperado_no_detalhe=contem, aceita_esperado=aceita, recibo=str(kp), recibo_sha256=sha(kp),
                    nota=nota), ok)
    return pino_ or {}


def _ksub(nome, kp, contem, nota=""):
    """o caminho inteiro do aplicar (subprocesso, sandbox, b2): o T17 FALHA com o motivo e nada se grava."""
    run(nome, ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
               "--fase", "pos_selo", "--evento", "SANDBOX:R3.1", "--kernel-recibo", kp, "--kernel-recibo-sha256", sha(kp)], 3,
        veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", bancada=B2,
        extra_ok=lambda j, r, contem=contem: (lambda t: t["resultado"] == "FALHA" and contem in t["detalhe"])(testes(j)["T17_LEAN_KERNEL"]), nota=nota)


def _blog(nome, b):
    p_ = KL / ("R31_%s.log" % nome)
    p_.write_bytes(b)
    return dict(path=str(p_), sha256=sha(p_))


LB, LA = (KL / "build_full_SINTETICO.log").read_bytes(), (KL / "audit_SINTETICO.log").read_bytes()

# --- A1: o aviso REAL do Lean 4.31 (crases), verbatim de um log do Nos (so lido)
checar("R31_A1_regex_pega_crase_e_aspas", lambda: len(MOD.RE_LOG_SORRY.findall(LINHA_REAL.decode("utf-8"))) == 1
       and len(MOD.RE_LOG_SORRY.findall("x.lean:1:1: warning: declaration uses 'sorry'")) == 1 and len(MOD.RE_LOG_SORRY.findall("declaration uses sorry")) == 0,
       nota="A1: a linha verbatim do log real (crases) e a forma de aspas simples casam; sem delimitador nao casa", linha_real=LINHA_REAL.decode("utf-8"), fonte=AMOSTRA)
_am_txt, _am_cod = MOD.normalizar_log(Path(AMOSTRA["path"]).read_bytes())
# rodada 1 da R3.1: este controle esqueceu os sorryAx das linhas de #print axioms do mesmo log (o esboco os conta, como a R3 ja contava);
# o esperado agora soma os tres, medidos por bytes no arquivo real
import re as _re
_am_bytes = Path(AMOSTRA["path"]).read_bytes()
_N_SORRYAX = len(_re.findall(rb"\bsorryAx\b", _am_bytes))
checar("R31_A1_contagem_no_log_real_do_Nos",
       lambda: len(MOD.RE_LOG_SORRY.findall(_am_txt)) == AMOSTRA["n_avisos_crase_no_arquivo"] + AMOSTRA["n_avisos_aspas_no_arquivo"] + _N_SORRYAX
       and AMOSTRA["n_avisos_crase_no_arquivo"] > 0
       and len(MOD.RE_LOG_SORRY.findall(_am_txt.replace("`sorry`", "x"))) == AMOSTRA["n_avisos_aspas_no_arquivo"] + _N_SORRYAX,
       nota="A1: no log REAL inteiro (so lido; CRLF), a contagem do esboco R3.1 == o medido por bytes: %d avisos com crase + %d com aspas + %d sorryAx "
            "nas linhas de axiomas; tirando as crases, sobram so aspas + sorryAx (a regex da R3 nao via os avisos com crase)"
            % (AMOSTRA["n_avisos_crase_no_arquivo"], AMOSTRA["n_avisos_aspas_no_arquivo"], _N_SORRYAX), fonte=AMOSTRA, codificacao=_am_cod, sorryAx_por_bytes=_N_SORRYAX)
KP_SORRY_REAL = _kr("sorry_real_crase", lambda k: k.update(build_full_log=_blog("sorry_real_crase", LB + LINHA_REAL + b"\n")))
_ku("R31_A1_unit_sorry_real_lean431_crase", KP_SORRY_REAL, "ocorrencia(s) de sorry",
    nota="A1 (o N1a da reauditoria): a linha REAL do Lean 4.31 (crases) no build log; na R3 o recibo era aceito com sorry=0")
_ksub("R31_A1_sub_sorry_real_lean431_crase", KP_SORRY_REAL, "ocorrencia(s) de sorry", nota="A1 pelo caminho inteiro do aplicar: T17 FALHA e nada se grava")
_ku("R31_A1_unit_sorry_aspas_simples", _kr("sorry_aspas", lambda k: k.update(build_full_log=_blog("sorry_aspas", LB + b"warning: TGLExt/PedraSinteticaA.lean:3:8: declaration uses 'sorry'\n"))),
    "ocorrencia(s) de sorry", nota="A1: o formato de aspas simples continua contado")
_ku("R31_A1_unit_sorry_real_no_audit_log", _kr("sorry_real_audit", lambda k: k.update(audit_log=_blog("sorry_real_audit", LA + LINHA_REAL + b"\n"))),
    "ocorrencia(s) de sorry", nota="A1: o aviso real no log do Audit tambem conta")
_ku("R31_A1_unit_sorry_real_declarado_1", _kr("sorry_real_declarado", lambda k: k.update(sorry=1, build_full_log=_blog("sorry_real_declarado", LB + LINHA_REAL + b"\n"))),
    "sorry=1", nota="A1: declarar sorry=1 (a contagem certa) nao salva: sorry tem de ser 0")

# --- A1b: a normalizacao do log antes de contar
KP_UTF16_SEM_BOM = _kr("utf16_sem_bom", lambda k: k.update(build_full_log=_blog("utf16_sem_bom", LB + "warning: TGLExt/PedraSinteticaA.lean:3:8: declaration uses `sorry`\n".encode("utf-16-le"))))
_ku("R31_A1b_UTF16LE_sem_BOM_anexado", KP_UTF16_SEM_BOM, "LOG_COM_CARACTERE_DE_CONTROLE",
    nota="A1b (o N1b da reauditoria): UTF-16LE sem BOM no meio de um log UTF-8; na R3 o sorry escondido passava")
_ksub("R31_A1b_sub_UTF16LE_sem_BOM_anexado", KP_UTF16_SEM_BOM, "LOG_COM_CARACTERE_DE_CONTROLE")
_ku("R31_A1b_sorry_real_em_log_UTF16_com_BOM", _kr("utf16_bom_sorry", lambda k: k.update(build_full_log=_blog("utf16_bom_sorry", (LB + LINHA_REAL + b"\n").decode("utf-8").encode("utf-16")))),
    "ocorrencia(s) de sorry", nota="A1b: o log inteiro em UTF-16 com BOM (o que o PowerShell 5.1 grava com >) e decodificado e o sorry real e contado")
_ku("R31_A1b_contraprova_log_UTF16_com_BOM_limpo_aceito", _kr("utf16_bom_limpo", lambda k: k.update(build_full_log=_blog("utf16_bom_limpo", LB.decode("utf-8").encode("utf-16")))),
    None, aceita=True, nota="contraprova: um build log UTF-16 com BOM, sem sorry nem erro, passa")
_ku("R31_A1b_contraprova_log_UTF8_com_BOM_limpo_aceito", _kr("utf8_bom_limpo", lambda k: k.update(build_full_log=_blog("utf8_bom_limpo", b"\xef\xbb\xbf" + LB))),
    None, aceita=True, nota="contraprova: UTF-8 com BOM passa")
_ku("R31_A1b_sorry_real_com_quebra_so_CR", _kr("cr_sorry", lambda k: k.update(build_full_log=_blog("cr_sorry", LB + b"\r" + LINHA_REAL.rstrip(b"\r") + b"\r"))),
    "ocorrencia(s) de sorry", nota="A1b: CR sozinho como quebra")
_ku("R31_A1b_erro_com_quebra_so_CR", _kr("cr_erro", lambda k: k.update(build_full_log=_blog("cr_erro", LB + b"\rerror: TGLExt/PedraSinteticaA.lean:3:8: unknown identifier 'x'\rerror: build failed\r"))),
    "linha(s) de erro", nota="A1b (o N1d da reauditoria): na R3 os erros com CR sozinho nao eram contados")
_ku("R31_A1b_erro_com_cor_ANSI", _kr("ansi_erro", lambda k: k.update(build_full_log=_blog("ansi_erro", LB + b"\x1b[31merror:\x1b[0m TGLExt/PedraSinteticaA.lean:3:8: unknown identifier 'x'\n"))),
    "linha(s) de erro", nota="A1b (o N1e da reauditoria): a cor ANSI escondia o erro")
_ku("R31_A1b_sorry_com_cor_ANSI", _kr("ansi_sorry", lambda k: k.update(build_full_log=_blog("ansi_sorry", LB + b"warning: x.lean:1:1: declaration uses \x1b[1m`sorry`\x1b[0m\n"))),
    "ocorrencia(s) de sorry")
_ku("R31_A1b_sorry_com_espaco_de_largura_zero", _kr("zw_sorry", lambda k: k.update(build_full_log=_blog("zw_sorry", LB + "warning: x.lean:1:1: declaration uses `so​rry`\n".encode("utf-8")))),
    "ocorrencia(s) de sorry")
_ku("R31_A1b_log_que_nao_decodifica", _kr("utf8_invalido", lambda k: k.update(build_full_log=_blog("utf8_invalido", LB + b"\xc3(\n"))), "LOG_NAO_DECODIFICA")
_ku("R31_A1b_ESC_solto_no_log_do_Audit", _kr("esc_solto", lambda k: k.update(audit_log=_blog("esc_solto", LA + b"\x1b\n"))), "LOG_COM_CARACTERE_DE_CONTROLE")

# --- A2: logs vazios ou curtos demais
KP_BUILD_VAZIO = _kr("build_vazio", lambda k: k.update(build_full_log=_blog("build_vazio", b"")))
_ku("R31_A2_build_log_vazio", KP_BUILD_VAZIO, "build_full_log vazio", nota="A2 (o N1f da reauditoria): na R3 um build log vazio era aceito")
_ksub("R31_A2_sub_build_log_vazio", KP_BUILD_VAZIO, "build_full_log vazio")
_ku("R31_A2_build_log_so_brancos", _kr("build_brancos", lambda k: k.update(build_full_log=_blog("build_brancos", b" \r\n\t\n"))), "build_full_log vazio")
_ku("R31_A2_audit_log_com_uma_linha", _kr("audit_uma_linha", lambda k: k.update(audit_log=_blog("audit_uma_linha", b"'TGLExt.PedraSinteticaA.um' depends on axioms: [propext, Classical.choice, Quot.sound]\n"))),
    "LOG_DO_AUDIT_CURTO", nota="A2: o Audit.lean pinado tem 2 #print axioms; um log com 1 linha e recusado")
_ku("R31_A2_audit_log_do_ataque_N1g", _kr("audit_ataque_n1g", lambda k: k.update(audit_log=_blog("audit_ataque_n1g", b"'X' does not depend on any axioms\n"))),
    "LOG_DO_AUDIT_CURTO", nota="A2 (o N1g da reauditoria, a mesma linha): na R3 era aceito")
PINO_OK = _ku("R31_A2_contraprova_audit_log_com_as_2_linhas_aceito", K_OK, None, aceita=True, nota="contraprova: o log do Audit com as 2 linhas do Audit.lean pinado passa")
checar("R31_A2_o_minimo_vem_do_Audit_lean_pinado", lambda: PINO_OK["logs"]["print_axioms_no_audit_pinado"] == 2 and PINO_OK["logs"]["linhas_de_axiomas"] == 2,
       nota="A2: o pino do recibo do kernel registra o minimo (os #print axioms do Audit.lean pinado) e o que o log trouxe", logs=PINO_OK.get("logs"))

# --- A3: os esperados nao vem do recibo
KP_AUTODECL = _kr("criterio_autodeclarado", lambda k: k["criterios"].update(j1_declaracoes=dict(esperado=7, medido=7), audit_entradas_antigas_identicas=dict(esperado=1, medido=1)))
_ku("R31_A3_esperado_autodeclarado_no_recibo", KP_AUTODECL, "CRITERIO_AUTODECLARADO",
    nota="A3 (o N1h da reauditoria): esperado = medido = 7 no proprio recibo era aceito na R3; agora o esperado so vem do CRITERIOS pinado")
_ksub("R31_A3_sub_esperado_autodeclarado_no_recibo", KP_AUTODECL, "CRITERIO_AUTODECLARADO")
_ku("R31_A3_medido_contra_o_esperado_pinado", _kr("criterio_medido_7", lambda k: k["criterios"].update(j1_declaracoes=dict(medido=7))),
    "criterio j1_declaracoes: medido 7 != esperado 2", nota="A3: o medido 7 (sem esperado no recibo) contra o esperado 2 do CRITERIOS pinado")
_ku("R31_A3_criterio_com_chave_extra", _kr("criterio_chave_extra", lambda k: k["criterios"]["j1_declaracoes"].update(nota="x")), "so 'medido'")
_ku("R31_A3_criterio_fora_do_contrato", _kr("criterio_fora", lambda k: k["criterios"].update(outro=dict(medido=1))), "criterios fora do contrato")
_ku("R31_A3_sem_criterios_pinados", K_OK, "CRITERIOS_AUSENTES", criterios=None, nota="A3: sem o CRITERIOS pinado nem o recibo valido passa")


def _crit(nome, mut):
    c_ = json.loads(CRIT.read_bytes())
    mut(c_)
    p_ = FX / ("R31_CRIT_%s.json" % nome)
    p_.write_bytes(json.dumps(c_, ensure_ascii=False, indent=1).encode("utf-8"))
    return p_


for nome_, mut_, esp_ in (("x19_nulo", lambda c: c.update(x19=None), "CRITERIOS_SEM_DECISAO_X19"),
                          ("x19_texto_livre", lambda c: c.update(x19="talvez"), "CRITERIOS_SEM_DECISAO_X19"),
                          ("nao_preenchido", lambda c: c.update(preenchido=False), "CRITERIOS_NAO_PREENCHIDOS"),
                          ("preenchido_texto", lambda c: c.update(preenchido="true"), "CRITERIOS_NAO_PREENCHIDOS"),
                          ("outra_versao", lambda c: c.update(versao="v391"), "CRITERIOS_DE_OUTRA_VERSAO"),
                          ("contrato_errado", lambda c: c.update(contrato="CRITERIOS_R3"), "CRITERIOS_CONTRATO_INVALIDO"),
                          ("esperado_nulo", lambda c: c["esperados"].update(j1_declaracoes=None), "CRITERIOS_ESPERADO_INVALIDO"),
                          ("esperado_float", lambda c: c["esperados"].update(j1_teoremas=2.0), "CRITERIOS_ESPERADO_INVALIDO"),
                          ("esperado_texto", lambda c: c["esperados"].update(tokens_proibidos="0"), "CRITERIOS_ESPERADO_INVALIDO"),
                          ("esperado_bool_onde_int", lambda c: c["esperados"].update(j1_fora_do_trio=False), "CRITERIOS_ESPERADO_INVALIDO"),
                          ("esperado_int_onde_bool", lambda c: c["esperados"].update(r1_ausente=1), "CRITERIOS_ESPERADO_INVALIDO"),
                          ("esperado_negativo", lambda c: c["esperados"].update(j1_declaracoes=-1), "CRITERIOS_ESPERADO_INVALIDO"),
                          ("chave_a_menos", lambda c: c["esperados"].pop("r1_ausente"), "CRITERIOS_CHAVES_DIVERGEM"),
                          ("chave_a_mais", lambda c: c["esperados"].update(extra=1), "CRITERIOS_CHAVES_DIVERGEM"),
                          ("sem_esperados", lambda c: c.pop("esperados"), "CRITERIOS_SEM_ESPERADOS")):
    _p = _crit(nome_, mut_)
    unit("R31_A3_criterios_%s" % nome_, (lambda _p=_p: MOD.carregar_criterios(_p, sha(_p), "v392")), esp_, nota="A3: o arquivo de criterios mal formado e recusado na carga")
_pl = FX / "R31_CRIT_lista.json"
_pl.write_bytes(b"[1, 2]")
unit("R31_A3_criterios_nao_objeto", lambda: MOD.carregar_criterios(_pl, sha(_pl), "v392"), "CRITERIOS_ILEGIVEIS")
unit("R31_A3_criterios_sha_divergente", lambda: MOD.carregar_criterios(CRIT, "0" * 64, "v392"), "CRITERIOS_SHA_DIVERGE")
unit("R31_A3_criterios_sem_sha", lambda: MOD.carregar_criterios(CRIT, None, "v392"), "CRITERIOS_SHA_AUSENTE")
unit("R31_A3_modelo_da_gerencia_recusado", lambda: MOD.carregar_criterios(CRIT_MODELO, sha(CRIT_MODELO), "v392"), "CRITERIOS_NAO_PREENCHIDOS",
     nota="o modelo R3_1/CRITERIOS_V392.json (preenchido=false; x19 e esperados nulos) nao vale ate a gerencia preencher na derivacao")
unit("R31_A3_contraprova_criterios_sintetico_aceito", lambda: MOD.carregar_criterios(CRIT, CRIT_SHA, "v392")["x19"], None, nota="contraprova")
_BASE_A3 = ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
            "--evento", "SANDBOX:R3.1-A3", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA]
run("R31_A3_sub_kernel_recibo_sem_criterios", _BASE_A3, 2, "CRITERIOS_AUSENTES", bancada=B2, sem_criterios=True,
    nota="A3: com --kernel-recibo e sem --criterios o B(n) recusa antes da bateria (rc 2)")
run("R31_A3_sub_criterios_sem_sha", _BASE_A3 + ["--criterios", CRIT], 2, "CRITERIOS_SHA_AUSENTE", bancada=B2)
run("R31_A3_sub_criterios_sha_divergente", _BASE_A3 + ["--criterios", CRIT, "--criterios-sha256", "2" * 64], 2, "CRITERIOS_SHA_DIVERGE", bancada=B2)
run("R31_A3_sub_sha_sem_arquivo_de_criterios", _BASE_A3 + ["--criterios-sha256", CRIT_SHA], 2, "CRITERIOS_AUSENTES", bancada=B2)
run("R31_A3_sub_modelo_da_gerencia_recusado", _BASE_A3 + ["--criterios", CRIT_MODELO, "--criterios-sha256", sha(CRIT_MODELO)], 2, "CRITERIOS_NAO_PREENCHIDOS", bancada=B2)

# --- N1k, N1l, N1m: o manifesto do kernel pinado pelo selo, alterado e RE-PINADO num Nos de ataque (o caminho inteiro por ler_nos)
AT31 = RAIZ / "aud31"
AT31.mkdir(exist_ok=True)


def nos_ataque(nome, mut_man):
    d_ = AT31 / ("nos_" + nome)
    d_.mkdir(parents=True)
    for f_ in ("um.py", "um_absoluto.json"):
        shutil.copyfile(NOS392 / f_, d_ / f_)
    man_ = json.loads((NOS392 / "tgl_kernel_proof_manifest.json").read_bytes())
    mut_man(man_)
    mb_ = json.dumps(man_, ensure_ascii=False, indent=1).encode("utf-8")
    (d_ / "tgl_kernel_proof_manifest.json").write_bytes(mb_)
    selo_ = json.loads((NOS392 / "um_absoluto_selo.json").read_bytes())
    selo_["sha256"]["tgl_kernel_proof_manifest.json"] = sha_b(mb_)
    (d_ / "um_absoluto_selo.json").write_bytes(json.dumps(selo_, ensure_ascii=False, indent=1).encode("utf-8"))
    return MOD.ler_nos(d_, "v392")


_ni = nos_ataque("ax_ausente", lambda m: [m["axiom_report"].pop(x) for x in [n for n in list(m["axiom_report"]) if "PedraSintetica" in n]])
_ku("R31_N1k_axiom_report_sem_as_declaracoes_das_pedras", K_OK, "nao tem entrada no axiom_report", ni=_ni,
    nota="N1k (o ataque da reauditoria): as declaracoes das pedras saem do axiom_report do manifesto pinado; na R3 o mesmo recibo passava")
_ku("R31_N1k_pedra_sem_declaracoes", _kr("pedra_sem_declaracoes", lambda k: k["pedras"][0].pop("declaracoes")), "exige declaracoes")
_ku("R31_N1k_declaracoes_repetidas", _kr("declaracoes_repetidas", lambda k: k["pedras"][0].update(declaracoes=["TGLExt.PedraSinteticaA.um"] * 2)), "exige declaracoes")
_ku("R31_N1k_declaracoes_vazias", _kr("declaracoes_vazias", lambda k: k["pedras"][1].update(declaracoes=[])), "exige declaracoes")
_ku("R31_N1k_declaracao_sem_entrada_no_axiom_report", _kr("declaracao_inventada", lambda k: k["pedras"][0]["declaracoes"].append("TGLExt.PedraSinteticaA.inventada")),
    "nao tem entrada no axiom_report")
AR_VELHA = next(n for n in km["axiom_report"] if not n.startswith("TGLExt.PedraSintetica"))
_ku("R31_N1k_declaracao_nao_impressa_no_log_do_Audit", _kr("declaracao_fora_do_log", lambda k: k["pedras"][0]["declaracoes"].append(AR_VELHA)),
    "nao foi impressa no log do Audit", nota="N1k: uma declaracao que existe no axiom_report (%s) mas nao no log do Audit" % AR_VELHA)
_ku("R31_N1k_declaracao_nao_nomeada_na_fonte_da_pedra",
    _kr("declaracao_fora_da_fonte", lambda k: (k["pedras"][0]["declaracoes"].append(AR_VELHA),
                                               k.update(audit_log=_blog("audit_com_velha", LA + ("'%s' depends on axioms: [propext]\n" % AR_VELHA).encode("utf-8"))))),
    "nao e nomeada na fonte da pedra", nota="N1k: a declaracao esta no axiom_report e no log, mas a pedra que a reclama nao a define")
_ni = nos_ataque("pedra_oculta", lambda m: m["formal_files_sha256"].update({"TGLExt/PedraOculta.lean": sha_b(b"theorem oculto : True := sorry\n")}))
_ku("R31_N1l_pedra_selada_nao_listada_no_recibo", K_OK, "NAO listada", ni=_ni,
    nota="N1l (o ataque da reauditoria): uma pedra a mais no manifesto pinado pelo selo, fora do recibo; na R3 passava")
_fa2 = dict(K["formal_files_antes"])
_fa2["TGLExt/PedraSinteticaB.lean"] = K["pedras"][1]["sha256"]
_imp2 = MOD.impressao_formal(_fa2)
_ku("R31_N1l_pedra_do_recibo_que_nao_e_nova", _kr("pedra_nao_nova", lambda k: (k.update(formal_files_antes=_fa2), k["nos_kernel_impressao"].update(antes=_imp2, depois=_imp2))),
    "nao sao novas nem mudadas", nota="N1l: sandbox sem recibo pre-selo, para chegar a regra (com o pre-selo o ANTES ja recusaria)")
_ku("R31_N1l_formal_files_antes_nao_bate_com_a_impressao", _kr("antes_impressao_diverge", lambda k: k["formal_files_antes"].update({"TGLExt/Inventado.lean": "a" * 64})),
    "impressao de formal_files_antes")
_ku("R31_N1l_formal_files_antes_sem_a_raiz_do_antes", _kr("antes_sem_raiz", lambda k: (k["formal_files_antes"].update({"TGLExt.lean": "c" * 64}),
                                                                                         k["nos_kernel_impressao"].update(antes=MOD.impressao_formal(k["formal_files_antes"]),
                                                                                                                          depois=MOD.impressao_formal(k["formal_files_antes"])))),
    "nao traz a raiz e o Audit do ANTES")
_ni = nos_ataque("arquivo_removido", lambda m: m["formal_files_sha256"].pop(next(c for c in m["formal_files_sha256"] if c.startswith("TGLExt/") and "PedraSintetica" not in c)))
_ku("R31_N1l_arquivo_formal_removido", K_OK, "ausente(s) no manifesto", ni=_ni)
_ni = nos_ataque("mudado_fora", lambda m: m["formal_files_sha256"].update(
    {next(c for c in m["formal_files_sha256"] if not c.startswith("TGLExt/") and c not in ("TGLExt.lean", "TGL/Audit.lean")): "b" * 64}))
_ku("R31_N1l_arquivo_mudado_fora_de_TGLExt", K_OK, "fora de TGLExt/", ni=_ni)
_ku("R31_N1l_recibo_sem_formal_files_antes", _kr("sem_formal_files_antes", lambda k: k.pop("formal_files_antes")), "formal_files_antes")
_ku("R31_N1l_contraprova_com_pre_selo_aceito", K_OK, None, pre=PRE, sandbox=False, aceita=True, nota="contraprova: com o recibo pre-selo do run 1b, a cobertura e o ANTES passam")
_ni = nos_ataque("sem_toolchain", lambda m: [m.pop("lean_version"), m.pop("lake_version")])
_ku("R31_N1m_manifesto_e_recibo_sem_toolchain", _kr("toolchain_vazia", lambda k: k.update(toolchain={})), "toolchain", ni=_ni,
    nota="N1m (o ataque da reauditoria): na R3 a ausencia nos dois lados passava")
_ni = nos_ataque("toolchain_texto", lambda m: m.update(lean_version="Lean (version 9.9.9)", lake_version="Lake 9"))
_ku("R31_N1m_manifesto_toolchain_texto_nao_lista", _kr("toolchain_L", lambda k: k.update(toolchain=dict(lean_version="L", lake_version="L"))), "nao e LISTA", ni=_ni,
    nota="N1m (o ataque da reauditoria): texto no manifesto e 'L' no recibo (o [0] da R3 pegava a primeira letra)")
_ku("R31_N1m_recibo_toolchain_em_texto_formato_R3", _kr("toolchain_texto_R3", lambda k: k.update(toolchain=dict(lean_version=k["toolchain"]["lean_version"][0],
                                                                                                              lake_version=k["toolchain"]["lake_version"][0]))),
    "como LISTA", nota="N1m: o formato da R3 (texto) nao vale mais")
_ku("R31_N1m_recibo_toolchain_listas_vazias", _kr("toolchain_listas_vazias", lambda k: k.update(toolchain=dict(lean_version=[], lake_version=[]))), "como LISTA")
_ku("R31_N1m_recibo_toolchain_com_elemento_a_mais", _kr("toolchain_a_mais", lambda k: k["toolchain"]["lean_version"].append("Lean (version 4.31.0) outra")), "toolchain do build")
_ku("R31_N1m_recibo_toolchain_sem_lake", _kr("toolchain_sem_lake", lambda k: k["toolchain"].pop("lake_version")), "como LISTA")

# --- N2c: o recibo pre-selo cruzado com o selo pinado no manifesto anterior da Bancada (b2 ainda pina a v391 aqui)
ANT_B2 = MOD.estado_anterior(B2, MOD.carregar_canonical(B2)[0])


def _pre(nome, mut, base=None):
    rj_ = json.loads(Path(base or R1B).read_bytes())
    mut(rj_)
    p_ = FX / ("R31_PRE_%s.json" % nome)
    p_.write_bytes(json.dumps(rj_, ensure_ascii=False, indent=1).encode("utf-8"))
    return p_


_p = _pre("selo_e_kernel_trocados", lambda r: (r["nos"]["selo"].update(sha256=sha_b(b"selo de outro rito"), tgl_kernel_proof_manifest_sha256=sha_b(b"km de outro rito")),
                                               r["nos"]["kernel"].update(sha256=sha_b(b"km de outro rito"), raiz_sha256=sha_b(b"raiz de outro rito"))))
unit("R31_N2c_selo_e_kernel_de_outro_rito", lambda: _conferir_pre(_p, ANT_B2, B2, False, sha(_p)), "RECIBO_PRE_SELO_NAO_CORRESPONDE",
     nota="N2c (o ataque da reauditoria): mesma versao e mesmo um.py, selo e kernel de outro rito; na R3 era aceito com o pino forjado")
_p2 = _pre("so_selo_trocado", lambda r: r["nos"]["selo"].update(sha256=sha_b(b"outro selo")))
unit("R31_N2c_so_o_selo_trocado", lambda: _conferir_pre(_p2, ANT_B2, B2, False, sha(_p2)), "RECIBO_PRE_SELO_NAO_CORRESPONDE")
_p3 = _pre("kernel_que_o_selo_nao_pina", lambda r: r["nos"]["kernel"].update(sha256=sha_b(b"outro manifesto do kernel")))
unit("R31_N2c_kernel_que_o_selo_dele_nao_pina", lambda: _conferir_pre(_p3, ANT_B2, B2, False, sha(_p3)), "RECIBO_PRE_SELO_NAO_CORRESPONDE")
_p4 = _pre("selo_ausente", lambda r: r["nos"].pop("selo"))
unit("R31_N2c_recibo_sem_selo", lambda: _conferir_pre(_p4, ANT_B2, B2, False, sha(_p4)), "RECIBO_PRE_SELO_NAO_CORRESPONDE")
unit("R31_N2c_contraprova_recibo_1b_aceito", lambda: _conferir_pre(R1B, ANT_B2, B2, False, sha(R1B))["selo_cruzado_com_o_manifesto_anterior"], None,
     nota="contraprova: o recibo do run 1b, lido contra a v391 copiada, cruza o selo")
run("R31_N2c_sub_selo_e_kernel_de_outro_rito", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
                                                "--fase", "pos_selo", "--evento", "SANDBOX:N2c", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA,
                                                "--recibo-pre-selo", _p, "--recibo-pre-selo-sha256", sha(_p)], 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=B2)
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
# R3.1 (A4): o teste de ambiente mudou de formato. Na R3 exigia PYTHONPATH ausente; na R3.1 o esboco poe PYTHONPATH = o site do usuario
# (achado pela pasta conhecida do Windows) para os NETOS, e o teste exige: -E, -P, -s no filho; APPDATA numa pasta vazia; nenhum
# usercustomize; o neto com o site do usuario desligado (PYTHONNOUSERSITE) e sem usercustomize. O controle confere o PYTHONPATH.
AMB_FONTE = '''import os, sys, json, subprocess
import importlib.util
from pathlib import Path
cwd = os.getcwd()
vazio = os.listdir(cwd) == []
aqui = os.path.normcase(str(Path(__file__).resolve().parent))
appdata = os.environ.get('APPDATA') or ''
appdata_vazia = bool(appdata) and os.path.isdir(appdata) and os.listdir(appdata) == []
codigo_neto = ('import json, os, site, sys, importlib.util; print(json.dumps(dict(user_site=bool(site.ENABLE_USER_SITE), '
               'usercustomize=("usercustomize" in sys.modules), numpy=importlib.util.find_spec("numpy") is not None, '
               'pythonpath=os.environ.get("PYTHONPATH"), appdata=os.environ.get("APPDATA"))))')
neto = subprocess.run([sys.executable, '-c', codigo_neto], capture_output=True, text=True)
try:
    n = json.loads(neto.stdout.strip().splitlines()[-1])
except Exception:
    n = dict(erro=(neto.stderr or '')[-300:])
r = dict(cwd=cwd, cwd_vazio_no_inicio=vazio, ignore_environment=bool(sys.flags.ignore_environment), safe_path=bool(sys.flags.safe_path),
         no_user_site=bool(sys.flags.no_user_site), appdata=appdata, appdata_vazia=appdata_vazia, pythonpath=os.environ.get('PYTHONPATH'),
         usercustomize_carregado=('usercustomize' in sys.modules),
         pasta_do_script_no_sys_path=any(os.path.normcase(os.path.abspath(p or cwd)) == aqui for p in sys.path),
         sitecustomize_do_ataque=bool(getattr(sys.modules.get('sitecustomize'), 'MARCA_N5', False)),
         numpy_no_filho=importlib.util.find_spec('numpy') is not None, neto=n)
ok = (r['cwd_vazio_no_inicio'] and r['ignore_environment'] and r['safe_path'] and r['no_user_site'] and r['appdata_vazia'] and not r['usercustomize_carregado']
      and not r['pasta_do_script_no_sys_path'] and not r['sitecustomize_do_ataque'] and n.get('user_site') is False and n.get('usercustomize') is False)
r['veredito'] = 'PASSA' if ok else 'FALHA'
Path(sys.argv[1]).write_text(json.dumps(r), encoding='utf-8')
print(json.dumps(r))
'''
amb = fixture_py("n5e", "teste_ambiente.py", AMB_FONTE)
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
                                                  "--fase", "pos_selo"], 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, flags=("-I", "-B", "-X", "utf8"),
    env_extra=dict(PYTHONPATH=str(FX / "n5pp")),
    extra_ok=lambda j, r: (lambda ts, amb_: ts["T00_AMBIENTE"]["resultado"] == "PASSA" and not any(MARC.iterdir()) and
                           amb_["cwd"].startswith(str(S / "N5_PYTHONPATH_injetado_nao_chega_ao_teste" / "cwd_testes")) and
                           amb_["pythonpath"] == SITE_REAL and amb_["neto"].get("pythonpath") == SITE_REAL)(
        testes(j), json.loads(Path(S / "N5_PYTHONPATH_injetado_nao_chega_ao_teste" / "recibos" / "T00_AMBIENTE.json").read_text(encoding="utf-8"))),
    nota="N5: com PYTHONPATH apontando um sitecustomize de ataque (o esboco chamado com -E), o teste ve: -E, -P, sem PYTHONPATH, cwd vazio novo, pasta do script fora do sys.path; o sitecustomize nao roda")
run("N5_PYTHONPATH_sem_E_recusado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_amb, "--bateria-sha256", bt_amb_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 2,
    "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-B", "-X", "utf8"), env_extra=dict(PYTHONPATH=str(FX / "n5vazio")), extra_ok=lambda j, r: j.get("recibo") is None,
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

# --- A4 (R3.1, residuo): um APPDATA de ATAQUE (site do usuario com .pth e usercustomize que deixam marcas) no ambiente do esboco
A4M = FX / "a4_MARCADORES"
A4M.mkdir()
APPDATA_ATAQUE = FX / "a4_appdata_ataque"
_sp_ataque = APPDATA_ATAQUE / "Python" / ("Python" + sys.winver.replace(".", "")) / "site-packages"
_sp_ataque.mkdir(parents=True)
_marca = json.dumps(A4M.as_posix())
(_sp_ataque / "a4_ataque.pth").write_text("import os, sys; open(%s + '/pth_%%d.txt' %% os.getpid(), 'w').write(repr(sys.argv))\n" % _marca, encoding="utf-8")
(_sp_ataque / "usercustomize.py").write_text("import os, sys\nopen(%s + '/usercustomize_%%d.txt' %% os.getpid(), 'w').write(repr(sys.argv))\n" % _marca, encoding="utf-8")


def _marcas_e_limpa():
    """as marcas deixadas (nome -> argv do processo que executou o .pth/usercustomize); apaga-as (so dentro do sandbox)."""
    out_ = {}
    for m_ in sorted(A4M.iterdir()):
        out_[m_.name] = m_.read_text(encoding="utf-8")
        m_.unlink()
    return out_


T_AMB_A4 = t_extra("T00_AMBIENTE", amb, ["{py}", "-B", "-X", "utf8", "{fonte:0}", "{recibos}/T00_AMBIENTE.json"],
                   dict(tipo="json_igual", arquivo="{recibos}/T00_AMBIENTE.json", campos=dict(veredito="PASSA")))
bt_a4, bt_a4_sha = mini_bateria("A4_appdata_de_ataque", ids=("T01_IDENTIDADE", "T15_SONDAS"), extra=[T_AMB_A4])
_ARGS_A4 = ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_a4, "--bateria-sha256", bt_a4_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"]
MARCAS_A4 = {}


def _amb_json(nome):
    return json.loads(Path(S / nome / "recibos" / "T00_AMBIENTE.json").read_text(encoding="utf-8"))


def _a4_ok(nome, j, esboco_com_s):
    rec_, ts_, amb_ = recibo_de(j), testes(j), _amb_json(nome)
    marcas_ = MARCAS_A4[nome] = _marcas_e_limpa()
    prep_ = rec_["bateria_resultado"]["isolamento"]["preparado"]
    de_teste = {k_: v_ for k_, v_ in marcas_.items() if "sincronizar_bancada.py" not in v_}
    return (ts_["T00_AMBIENTE"]["resultado"] == "PASSA" and ts_["T01_IDENTIDADE"]["resultado"] == "PASSA" and not de_teste
            and (not marcas_ if esboco_com_s else len(marcas_) >= 1)
            and amb_["pythonpath"] == SITE_REAL and amb_["neto"].get("pythonpath") == SITE_REAL and amb_["numpy_no_filho"] is True and amb_["neto"].get("numpy") is True
            and Path(amb_["appdata"]).parent == S / nome / "appdata_vazio" and amb_["neto"].get("appdata") == amb_["appdata"]
            and prep_["site_do_usuario"]["path"] == SITE_REAL and prep_["site_do_usuario"]["iguais"] is False
            and rec_["python_no_user_site"] is esboco_com_s and isolado(rec_, S / nome))


run("R31_A4_appdata_de_ataque_esboco_com_s", _ARGS_A4, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-s", "-B", "-X", "utf8"),
    env_extra=dict(APPDATA=str(APPDATA_ATAQUE)), extra_ok=lambda j, r: (lambda m_: j.get("recibo") is None and not m_)(MARCAS_A4.setdefault("R31_A4_appdata_de_ataque_esboco_com_s", _marcas_e_limpa())),
    nota="A4 (o N5b da reauditoria): APPDATA de ataque no ambiente do esboco chamado com -s; os testes rodam com -E -P -s pelo lancador, APPDATA vazio e o site do "
         "usuario REAL (pasta conhecida) so como caminho: nenhuma marca de .pth nem de usercustomize em processo nenhum; numpy segue importavel no filho e no neto")
run("R31_A4_appdata_de_ataque_esboco_sem_s_residuo_so_no_esboco", _ARGS_A4, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-B", "-X", "utf8"),
    env_extra=dict(APPDATA=str(APPDATA_ATAQUE)), extra_ok=lambda j, r: (lambda m_: j.get("recibo") is None and len(m_) >= 1 and all("sincronizar_bancada.py" in v_ for v_ in m_.values()))(
        MARCAS_A4.setdefault("R31_A4_appdata_de_ataque_esboco_sem_s_residuo_so_no_esboco", _marcas_e_limpa())),
    nota="A4 (o N5a da reauditoria): o esboco SEM -s executa o .pth e o usercustomize do APPDATA dele (residuo declarado: a cadeia chama com -s); nenhum processo de "
         "TESTE executa (na R3: 4 marcas em processos -E -P)")
run("R32_A4_appdata_de_ataque_esboco_com_I", _ARGS_A4, 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, flags=("-I", "-B", "-X", "utf8"),
    env_extra=dict(APPDATA=str(APPDATA_ATAQUE)), extra_ok=lambda j, r: _a4_ok("R32_A4_appdata_de_ataque_esboco_com_I", j, True),
    nota="A4/R31-1 (R3.2): o mesmo APPDATA de ataque, com o esboco chamado como exigido (-I -B -X utf8): nenhuma marca de .pth nem de usercustomize em processo "
         "nenhum; os testes com -E -P -s pelo lancador; numpy segue importavel no filho e no neto")
_lanc_dir = FX / "a4_lancador_adulterado"
(_lanc_dir / "lancador").mkdir(parents=True)
(_lanc_dir / "lancador" / MOD.LANCADOR_NOME).write_bytes(MOD.LANCADOR_FONTE.encode("utf-8") + b"import os\n")
unit("R31_A4_lancador_adulterado_recusado", lambda: MOD.preparar_isolamento(_lanc_dir), "LANCADOR_ALTERADO")
_site_cust = FX / "a4_site_com_customize"
_site_cust.mkdir()
(_site_cust / "sitecustomize.py").write_text("X = 1\n", encoding="utf-8")
_site_sombra = FX / "a4_site_sombra"
_site_sombra.mkdir()
(_site_sombra / "json.py").write_text("X = 1\n", encoding="utf-8")


def _com_site(dirp, fn):
    antigo_ = MOD.site_do_usuario_real
    MOD.site_do_usuario_real = lambda: str(dirp)
    try:
        return fn()
    finally:
        MOD.site_do_usuario_real = antigo_


unit("R31_A4_site_do_usuario_com_sitecustomize_recusado", lambda: _com_site(_site_cust, lambda: MOD.preparar_isolamento(FX / "a4_p1")), "SITE_DO_USUARIO_COM_CUSTOMIZE",
     nota="A4: um sitecustomize no site do usuario rodaria nos netos pelo PYTHONPATH")
unit("R31_A4_site_do_usuario_que_sombreia_a_stdlib_recusado", lambda: _com_site(_site_sombra, lambda: MOD.preparar_isolamento(FX / "a4_p2")), "SITE_DO_USUARIO_SOMBREIA_A_STDLIB")
ISO_A4 = MOD.preparar_isolamento(FX / "a4_p0")[0]


def _residuo_independente():
    import site as site_, sysconfig as sc_
    dirs_ = []
    for d_ in list(site_.getsitepackages()) + [sc_.get_paths().get(x_) for x_ in ("stdlib", "platstdlib", "purelib", "platlib")]:
        if d_ and os.path.isdir(d_) and not any(os.path.normcase(d_) == os.path.normcase(y_) for y_ in dirs_):
            dirs_.append(d_)
    return [sha(os.path.join(d_, n_)) for d_ in dirs_ for n_ in sorted(os.listdir(d_)) if os.path.isfile(os.path.join(d_, n_))
            and (n_.lower().endswith(".pth") or n_.split(".")[0].lower() in ("sitecustomize", "usercustomize"))]


_pth_usuario = sorted(n_ for n_ in os.listdir(SITE_REAL) if n_.lower().endswith(".pth")) if SITE_REAL and os.path.isdir(SITE_REAL) else []
checar("R31_A4_residuo_declarado_confere_com_medida_independente",
       lambda: [e_["sha256"] for e_ in ISO_A4["residuo_declarado"]["pth_e_customize_do_site_do_sistema_que_executam"]] == _residuo_independente()
       and [Path(e_["path"]).name for e_ in ISO_A4["site_do_usuario"]["pth_que_NAO_executam_mais"]] == _pth_usuario
       and all(sha(e_["path"]) == e_["sha256"] for e_ in ISO_A4["site_do_usuario"]["pth_que_NAO_executam_mais"])
       and ISO_A4["lancador"]["sha256"] == sha(Path(ISO_A4["lancador"]["path"])) == MOD.LANCADOR_SHA256,
       nota="A4: o recibo lista, com sha256, os .pth/customize do site do SISTEMA que ainda executam (medida independente aqui) e os .pth do site do usuario que "
            "deixaram de executar (so lidos; o site do usuario real nao e tocado)", residuo=ISO_A4["residuo_declarado"], site_do_usuario=ISO_A4["site_do_usuario"])
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
run("A6_recibo_pre_selo_na_fase_pre_selo", ["--bancada", B1, "--versao", VR, "--bateria", BAT, "--sem-bateria", "--fase", "pre_selo", "--recibo-pre-selo", R1A], 2, "RECIBO_PRE_SELO_NA_FASE_PRE_SELO", bancada=B1)
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
decoy("N3_decoy_servico_volta_antes_do_recibo_em_estado", 2, "SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO", sondas=(False, False, False, False, False, True),
      extra_ok=_so_backup_novo,
      nota="N3: volta depois da troca, antes do recibo em estado/: o manifesto anterior volta byte a byte (rollback) e o contrato sai. R3.1 (N3a): o servico "
           "segue no ar depois do rollback (a sonda simulada repete o ultimo valor): o codigo passa a ser o proprio, SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO")
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
# --- R3.1 no DECOY de producao: A1, A3, N2c, N3a, N4b (em processo; PRODUCAO, EVENTOS_QUADRO e a sonda do servico trocados)
decoy("R31_A1_decoy_sorry_real_nao_aplica", 3, veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", kernel=KP_SORRY_REAL,
      extra_ok=lambda j, a, d: pd_intocado(j, a, d) and "ocorrencia(s) de sorry" in testes(j)["T17_LEAN_KERNEL"]["detalhe"],
      nota="A1 na producao-decoy: o recibo do kernel com o aviso REAL do Lean 4.31 no log nao aplica")
decoy("R31_A3_decoy_criterio_autodeclarado_nao_aplica", 3, veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", kernel=KP_AUTODECL,
      extra_ok=lambda j, a, d: pd_intocado(j, a, d) and "CRITERIO_AUTODECLARADO" in testes(j)["T17_LEAN_KERNEL"]["detalhe"],
      nota="A3 na producao-decoy: o recibo com esperado = medido = 7 nao aplica")
decoy("R31_A3_decoy_sem_criterios", 2, "CRITERIOS_AUSENTES", sem_criterios=True, extra_ok=pd_intocado,
      nota="A3 na producao-decoy: com --kernel-recibo e sem --criterios, recusa antes da bateria")
_pre_n2c = _pre("decoy_selo_e_kernel_trocados", lambda r: (r["nos"]["selo"].update(sha256=sha_b(b"selo de outro rito"), tgl_kernel_proof_manifest_sha256=sha_b(b"km de outro rito")),
                                                           r["nos"]["kernel"].update(sha256=sha_b(b"km de outro rito"), raiz_sha256=sha_b(b"raiz de outro rito"))), base=R_PD)
decoy("R31_N2c_decoy_selo_e_kernel_de_outro_rito", 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", pre=_pre_n2c, extra_ok=pd_intocado,
      nota="N2c (o ataque da reauditoria) na producao-decoy: o pino do recibo pre-selo forjado em vNNN_pins (sha do forjado) nao basta: o selo dele nao e o do manifesto anterior")
N4B = {}


def _mutar_mesmo_tamanho_e_mtime(p_):
    p_ = Path(p_)
    st_ = p_.stat()
    b_ = p_.read_bytes()
    i_ = b_.index(b'"sha256": "') + len(b'"sha256": "')
    b2_ = b_[:i_] + (b"1" if b_[i_:i_ + 1] != b"1" else b"2") + b_[i_ + 1:]
    p_.write_bytes(b2_)
    os.utime(p_, ns=(st_.st_atime_ns, st_.st_mtime_ns))
    return sha_b(b2_), len(b2_) == len(b_), p_.stat().st_mtime_ns == st_.st_mtime_ns


def _sonda_que_muta_na_quinta():
    estado_ = {"i": 0}

    def f_(porta=None):
        estado_["i"] += 1
        if estado_["i"] == 5:          # 5 = imediatamente_antes_da_troca (inicio, antes_do_backup, antes_do_contrato, antes_do_temporario, ...)
            N4B["sha"], N4B["tamanho_igual"], N4B["mtime_igual"] = _mutar_mesmo_tamanho_e_mtime(PD / "canonical_contracts.json")
        return False
    return f_


def _n4b_ok(j, a, d):
    baks = [n_ for n_ in d if ".bak_B3_" in n_]
    return (sha(PD / "canonical_contracts.json") == N4B.get("sha") != MAN_PD and N4B.get("tamanho_igual") is True and N4B.get("mtime_igual") is True
            and not (PD / "CONTRATO_CANONICO_B3.md").exists() and not any(n_.startswith("canonical_contracts.json.tmp") for n_ in d)
            and len(baks) == 1 and sha(PD / baks[0]) == MAN_PD)


decoy("R31_N4b_decoy_mudanca_durante_a_ultima_sonda", 2, "MANIFESTO_MUDOU_DESDE_A_LEITURA", patches_extra=dict(servico_responde=_sonda_que_muta_na_quinta()),
      extra_ok=_n4b_ok,
      nota="N4b (o ataque da reauditoria): a mudanca concorrente (mesmo tamanho, mesmo mtime) feita DURANTE a sonda imediatamente antes da troca; na R3 era "
           "sobrescrita e nao ficava no .bak; na R3.1 a comparacao vem depois da sonda: recusa, a mudanca fica, nenhum contrato nem temporario, o .bak guarda o lido no passo 3")
import inspect as _inspect
_src_ap = _inspect.getsource(MOD.aplicar_na_bancada)
checar("R31_N4b_ordem_sonda_compara_troca_no_codigo",
       lambda: _src_ap.index('guarda_servico("imediatamente_antes_da_troca")') < _src_ap.rindex("man_p.read_bytes() != antes_esperado") < _src_ap.index("os.replace(tmp, man_p)"),
       nota="N4b: no codigo do aplicar a ultima comparacao de bytes fica entre a ultima sonda e o os.replace")
decoy("R31_N3a_decoy_servico_subiu_no_os_replace", 2, "SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO", sondas=(False, False, False, False, False, True, True),
      extra_ok=lambda j, a, d: _so_backup_novo(j, a, d) and (lambda rec: rec["aplicacao_revertida"]["servico_no_ar_apos_rollback"] is True
                                                             and rec["aplicacao_revertida"]["manifesto_em_disco_sha256"] == MAN_PD
                                                             and rec["aplicacao_revertida"]["manifesto_novo_sha256"] not in (None, MAN_PD)
                                                             and rec["sondagens_do_servico"][-1]["momento"] == "apos_rollback"
                                                             and rec["aplicacao_revertida"]["nota"] == MOD.N3A_NOTA)(recibo_de(j)),
      nota="N3a (o ataque da reauditoria): o servico que sobe no instante do os.replace fica com o manifesto NOVO em RAM; o rollback devolve o VELHO ao disco; "
           "a sonda depois do rollback ve o servico no ar e recusa com codigo proprio; o recibo diz os dois sha e a nota")
decoy("R31_N3a_decoy_rollback_com_o_servico_ja_fora", 2, "APLICACAO_REVERTIDA", sondas=(False, False, False, False, False, True, False),
      extra_ok=lambda j, a, d: _so_backup_novo(j, a, d) and (lambda rec: rec["aplicacao_revertida"]["servico_no_ar_apos_rollback"] is False
                                                             and not str(rec["recusa"]).startswith("SERVICO_NO_AR_APOS_ROLLBACK"))(recibo_de(j)),
      nota="N3a: se o servico ja nao responde depois do rollback, o codigo segue APLICACAO_REVERTIDA (e o recibo traz a nota da RAM)")
decoy("R31_N3a_contraprova_recibo_documenta_a_ram", 0, veredito_esp="REPINADA_B3__APLICADA",
      extra_ok=lambda j, a, d: (lambda rec: rec["servico_e_manifesto_em_ram"] == MOD.N3A_NOTA and Path(rec["aplicacao"]["copia_do_recibo"]).exists()
                                and json.loads(Path(rec["aplicacao"]["copia_do_recibo"]).read_bytes())["servico_e_manifesto_em_ram"] == MOD.N3A_NOTA)(recibo_de(j)),
      nota="N3a: o recibo do aplicar (e a copia dele em estado/sincronizacao) documenta que o servico religado tem de ser conferido (10-ter)")
decoy_reset()


# ================================================================ R3.2: os achados da reauditoria a721b706 (R31-1 a R31-6 e o item 3 da 12-ter)
# Cada achado: o caso EXATO do auditor (ATAQUES_R3_1_AUDITOR.json) e pelo menos uma variante; contraprovas onde ha forma valida.
AT32 = RAIZ / "aud32"
AT32.mkdir(exist_ok=True)
M32 = AT32 / "marcas"
M32.mkdir(exist_ok=True)


def _marcas32():
    out_ = {m_.name: m_.read_text(encoding="utf-8", errors="replace")[:300] for m_ in sorted(M32.iterdir())}
    for m_ in list(M32.iterdir()):
        m_.unlink()
    return out_


# --- R31-1 (MEDIA): o esboco exige python -I -B -X utf8; um json.py (e um argparse.py) AO LADO do esboco nao chega a ser importado
ESB32 = AT32 / "esboco_com_vizinhos"
ESB32.mkdir()
shutil.copyfile(SYNC, ESB32 / "sincronizar_bancada.py")
_m32 = json.dumps(M32.as_posix())
# o json.py do auditor (art_a721b706/ataques_r3_1.py): deixa a marca e devolve o json verdadeiro (o esboco seguiria funcionando)
(ESB32 / "json.py").write_text(
    "import os, sys, importlib\n"
    "open(%s + '/json_sombra_%%d.txt' %% os.getpid(), 'w').write(repr(sys.orig_argv))\n"
    "_d = os.path.normcase(os.path.dirname(os.path.abspath(__file__)))\n"
    "sys.path[:] = [p for p in sys.path if os.path.normcase(os.path.abspath(p or '.')) != _d]\n"
    "del sys.modules['json']\n"
    "_r = importlib.import_module('json')\n"
    "sys.modules['json'] = _r\n" % _m32, encoding="utf-8")
(ESB32 / "argparse.py").write_text(
    "import os, sys, importlib\n"
    "open(%s + '/argparse_sombra_%%d.txt' %% os.getpid(), 'w').write(repr(sys.orig_argv))\n"
    "_d = os.path.normcase(os.path.dirname(os.path.abspath(__file__)))\n"
    "sys.path[:] = [p for p in sys.path if os.path.normcase(os.path.abspath(p or '.')) != _d]\n"
    "del sys.modules['argparse']\n"
    "_r = importlib.import_module('argparse')\n"
    "sys.modules['argparse'] = _r\n" % _m32, encoding="utf-8")
(ESB32 / "sitecustomize.py").write_text("import os, sys\nopen(%s + '/sitecustomize_esb_%%d.txt' %% os.getpid(), 'w').write(repr(sys.orig_argv))\n" % _m32, encoding="utf-8")
assert sha(ESB32 / "sincronizar_bancada.py") == sha(SYNC)
_ARGS_R311 = ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"]
_ = _marcas32()
MARCAS_R32 = {}


def _r311_recusa(nome):
    def f_(j, r):
        m_ = MARCAS_R32[nome] = _marcas32()
        return j.get("recibo") is None and not m_ and "nada importado alem de sys" in str(j.get("recusa"))
    return f_


run("R32_R31_1_exato_json_sombra_ao_lado_chamado_com_s", _ARGS_R311, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, sync=ESB32 / "sincronizar_bancada.py",
    flags=("-s", "-B", "-X", "utf8"), extra_ok=_r311_recusa("R32_R31_1_exato_json_sombra_ao_lado_chamado_com_s"),
    nota="R31-1 (o caso EXATO do auditor): o json.py do ataque ao lado do esboco, chamado com -s como mandava a remissao R3.1-0; na R3.1 executava no processo que "
         "grava a producao; na R3.2 a guarda do topo (antes de qualquer import alem de sys) recusa: rc 2, nenhuma marca, nada gravado")
run("R32_R31_1_variante_com_I_a_sombra_nao_executa_e_o_esboco_roda", _ARGS_R311, 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2, sync=ESB32 / "sincronizar_bancada.py",
    flags=("-I", "-B", "-X", "utf8"),
    extra_ok=lambda j, r: (lambda m_: not m_ and recibo_de(j)["python_isolado"]["isolated"] is True and recibo_de(j)["python_isolado"]["safe_path"] is True)(
        MARCAS_R32.setdefault("R32_R31_1_variante_com_I", _marcas32())),
    nota="R31-1: o mesmo esboco com json.py, argparse.py e sitecustomize.py ao lado, chamado como a remissao R3.2-0 manda (-I -B -X utf8): roda (ensaio), nenhuma marca")
run("R32_R31_1_variante_s_P_tambem_recusado", _ARGS_R311, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, sync=ESB32 / "sincronizar_bancada.py",
    flags=("-s", "-P", "-B", "-X", "utf8"), extra_ok=_r311_recusa("R32_R31_1_variante_s_P_tambem_recusado"),
    nota="R31-1 [INPUT da gerencia]: -s -P tambem cortaria o sys.path[0], mas a regra e uma so: -I (isolated); sem ele, recusa")
run("R32_R31_1_variante_I_sem_B", _ARGS_R311, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-I", "-X", "utf8"),
    extra_ok=lambda j, r: j.get("recibo") is None and "-B" in str(j.get("recusa")) and not tem_pycache(B2))
run("R32_R31_1_variante_I_sem_X_utf8", _ARGS_R311, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-I", "-B"),
    extra_ok=lambda j, r: j.get("recibo") is None and "-X utf8" in str(j.get("recusa")))
run("R32_R31_1_variante_E_s_B_X_sem_I", _ARGS_R311, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-E", "-s", "-B", "-X", "utf8"),
    extra_ok=lambda j, r: j.get("recibo") is None and "-P" in str(j.get("recusa")))


class _FlagsFalsas:
    isolated = 0
    ignore_environment = 1
    safe_path = 1
    no_user_site = 1
    dont_write_bytecode = 1
    utf8_mode = 1


decoy("R32_R31_1_variante_em_processo_main_confere_de_novo", 2, "INTERPRETADOR_NAO_ISOLADO", patches_extra=dict(_flags_do_interpretador=lambda: _FlagsFalsas),
      extra_ok=lambda j, a, d: pd_intocado(j, a, d) and j.get("recibo") is None,
      nota="R31-1: main() chamada em processo (decoy de producao) com um interpretador simulado sem isolated: recusa antes de ler argumento, nada gravado")
checar("R32_R31_1_sob_I_o_site_do_usuario_segue_sombreavel",
       lambda: bool(sys.flags.isolated) and "numpy" in MOD.sombreaveis() and MOD.site_do_usuario_real() is not None,
       nota="R31-1 (achado da 1a rodada da R3.2, controle N5_modulo_sombra_ao_lado_da_fonte): sob -I o site do usuario nao entra no sys.path do esboco, "
            "mas os testes o recebem como caminho; os modulos dele (numpy) seguem na lista dos sombreaveis (o numpy.py ao lado de fonte pinada e recusado)")
_src_topo = SYNC.read_text(encoding="utf-8")
checar("R32_R31_1_guarda_antes_de_qualquer_import",
       lambda: [l_ for l_ in _src_topo[:_src_topo.index("_falta = _flags_que_faltam()")].splitlines() if l_.startswith(("import ", "from "))] == ["import sys"]
       and _src_topo.index("_falta = _flags_que_faltam()") < _src_topo.index("import argparse") < _src_topo.index("import json"),
       nota="R31-1: no codigo, a unica importacao antes da guarda e `import sys` (embutido; nao se sombreia); json, argparse e o resto vem depois")

# --- R31-2: mudanca do manifesto entre o os.replace e o recibo (a 6a sonda) -- recusa, rollback e sonda depois do rollback
R312 = {}


def _sonda_que_muta_na(n_alvo, no_ar_depois=False):
    estado_ = {"i": 0}

    def f_(porta=None):
        estado_["i"] += 1
        if estado_["i"] == n_alvo:
            R312["sha"], R312["tamanho_igual"], R312["mtime_igual"] = _mutar_mesmo_tamanho_e_mtime(PD / "canonical_contracts.json")
        return bool(no_ar_depois and estado_["i"] > n_alvo)
    return f_


def _r312_ok(prefixo_causa):
    def f_(j, a, d):
        rec_ = recibo_de(j)
        ap_ = rec_.get("aplicacao") or {}
        ev_ = (ap_.get("manifesto_estranho") or {})
        est_ = sorted((PD / "estado" / "sincronizacao").glob("RECIBO_SINCRONIZACAO_*.json")) if (PD / "estado" / "sincronizacao").exists() else []
        return (_so_backup_novo(j, a, d) and prefixo_causa in str(j.get("recusa")) and ev_.get("sha256") == R312.get("sha") and Path(ev_.get("evidencia", "")).is_file()
                and sha(ev_["evidencia"]) == R312.get("sha") and not est_ and R312.get("tamanho_igual") is True and R312.get("mtime_igual") is True
                and rec_["sondagens_do_servico"][-1]["momento"] == "apos_rollback")
    return f_


R312.clear()
decoy("R32_R31_2_exato_mudanca_do_manifesto_durante_a_sexta_sonda", 2, "APLICACAO_REVERTIDA: MANIFESTO_MUDOU_APOS_A_TROCA",
      patches_extra=dict(servico_responde=_sonda_que_muta_na(6)), extra_ok=_r312_ok("MANIFESTO_MUDOU_APOS_A_TROCA"),
      nota="R31-2 (o caso EXATO do auditor): a mudanca do manifesto (mesmo tamanho e mtime) durante a 6a sonda, antes_do_recibo_em_estado; na R3.1 terminava rc 0 "
           "APLICADA com o disco diferente do declarado; na R3.2: recusa, os bytes estranhos ficam em --saida com sha, nenhum recibo em estado, rollback ao ANTERIOR "
           "e a sonda depois do rollback")
R312.clear()
_orig_gravar_novo = MOD.gravar_novo


def _gravar_e_mutar(p_, data_):
    r_ = _orig_gravar_novo(p_, data_)
    if Path(p_).parent.name == "sincronizacao" and Path(p_).parent.parent.name == "estado" and Path(p_).parent.parent.parent == PD:
        R312["sha"], R312["tamanho_igual"], R312["mtime_igual"] = _mutar_mesmo_tamanho_e_mtime(PD / "canonical_contracts.json")
        R312["recibo_em_estado_existia"] = Path(p_).exists()
    return r_


decoy("R32_R31_2_variante_mudanca_logo_depois_do_recibo_em_estado", 2, "APLICACAO_REVERTIDA: MANIFESTO_MUDOU_APOS_O_RECIBO_EM_ESTADO",
      patches_extra=dict(gravar_novo=_gravar_e_mutar),
      extra_ok=lambda j, a, d: _r312_ok("MANIFESTO_MUDOU_APOS_O_RECIBO_EM_ESTADO")(j, a, d) and R312.get("recibo_em_estado_existia") is True
      and (recibo_de(j)["aplicacao"].get("recibo_em_estado_retirado") or {}).get("sha256") is not None,
      nota="R31-2: a mudanca logo DEPOIS de gravar o recibo em estado/sincronizacao: a 2a conferencia ve, o recibo em estado (que dizia APLICADA) sai, rollback")
R312.clear()
decoy("R32_R31_2_variante_servico_no_ar_depois_do_rollback", 2, "SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO",
      patches_extra=dict(servico_responde=_sonda_que_muta_na(6, no_ar_depois=True)),
      extra_ok=lambda j, a, d: _so_backup_novo(j, a, d) and "MANIFESTO_MUDOU_APOS_A_TROCA" in str(j.get("recusa"))
      and recibo_de(j)["aplicacao_revertida"]["servico_no_ar_apos_rollback"] is True,
      nota="R31-2 + N3a: se o servico responde depois desse rollback, o codigo e o proprio (reinicio com recibo de identidade, 10-ter); a causa fica no texto")
decoy("R32_R31_2_contraprova_aplica_com_as_duas_conferencias", 0, veredito_esp="REPINADA_B3__APLICADA",
      extra_ok=lambda j, a, d: (lambda rec: [c_["momento"] for c_ in rec["aplicacao"]["conferencia_pos_troca"]] == ["depois_da_ultima_sonda_antes_do_recibo", "depois_do_recibo_em_estado"]
                                and all(c_["igual_ao_novo"] is True and c_["manifesto_em_disco_sha256"] == rec["manifesto_novo"]["sha256"] for c_ in rec["aplicacao"]["conferencia_pos_troca"])
                                and sha(PD / "canonical_contracts.json") == rec["manifesto_novo"]["sha256"] and Path(rec["aplicacao"]["copia_do_recibo"]).exists()
                                and "manifesto_estranho" not in rec["aplicacao"])(recibo_de(j)),
      nota="contraprova: sem mudanca alheia, as duas conferencias (antes e depois do recibo em estado) dao o manifesto novo e a producao-decoy e aplicada")
_src_main = _inspect.getsource(MOD.main)
checar("R32_R31_2_ordem_sonda_confere_recibo_confere_no_codigo",
       lambda: _src_main.index('guarda_servico("antes_do_recibo_em_estado")') < _src_main.index("if disco != novo_bytes") < _src_main.index("gravar_novo(est_rec, est_bytes)")
       < _src_main.index("if disco2 != novo_bytes"),
       nota="R31-2: no codigo do main, depois da ultima sonda vem a releitura do manifesto, o recibo em estado, e outra releitura")
decoy_reset()

# ================================================================ R3.3: os dois achados BAIXOS da reauditoria a70d70d5 (R32-A e R32-B)
# --- R32-A: -i (inspect) tambem e recusado; com PYTHONSTARTUP herdado, a marca do startup nao pode nascer e o processo nao pode ficar no REPL
_st33 = AT32 / "startup_r33.py"
_st33.write_text("open(%s + '/startup_r33_%%d.txt' %% __import__('os').getpid(), 'w').write('executou')" % _m32, encoding="utf-8")
_ = _marcas32()
run("R33_R32_A_exato_I_B_X_utf8_com_i_e_PYTHONSTARTUP", _ARGS_R311, 2, "INTERPRETADOR_NAO_ISOLADO", bancada=B2, flags=("-I", "-B", "-X", "utf8", "-i"),
    env_extra=dict(PYTHONSTARTUP=str(_st33), PYTHONINSPECT="1"),
    extra_ok=lambda j, r: (lambda m_: not m_ and j.get("recibo") is None and "sem -i" in str(j.get("recusa")) and r.returncode == 2)(_marcas32()),
    nota="R32-A (o caso EXATO do auditor): python -I -B -X utf8 -i com PYTHONSTARTUP/PYTHONINSPECT herdados e stdin no NUL; na R3.2 o esboco rodava e o "
         "startup executava depois do main() (o processo ficava no REPL); na R3.3 a guarda do topo recusa (rc 2, sem -i), sai por os._exit (SystemExit ainda "
         "entraria no REPL), nenhuma marca do startup, nada gravado")

# --- R32-B: mudanca logo depois do os.replace do rollback (a 6a sonda dispara o rollback; o os.replace do rollback e seguido de outra mudanca)
R33 = {}
_REAL_REPLACE_33 = os.replace


def _rep_f3(a_, b_, *x_, **y_):
    _REAL_REPLACE_33(a_, b_, *x_, **y_)
    if "tmp_rollback" in str(a_) and Path(b_).name == "canonical_contracts.json" and "m2" not in R33:
        R33["m2"] = _mutar_mesmo_tamanho_e_mtime(b_)


def _ok_r32b(j, a, d):
    rec_ = recibo_de(j)
    ar_ = rec_.get("aplicacao_revertida") or {}
    est_ = sorted((PD / "estado" / "sincronizacao").glob("RECIBO_SINCRONIZACAO_*.json")) if (PD / "estado" / "sincronizacao").exists() else []
    disco_ = sha(PD / "canonical_contracts.json")
    return (bool(R33.get("m2")) and R33["m2"][0] == disco_ and disco_ != MAN_PD and ar_.get("manifesto_em_disco_sha256") == disco_
            and not (PD / "CONTRATO_CANONICO_B3.md").exists() and rec_["sondagens_do_servico"][-1]["momento"] == "apos_rollback"
            and ar_.get("servico_no_ar_apos_rollback") is False and not est_ and not sorted(x_.name for x_ in PD.glob("*.tmp_*"))
            and (rec_["aplicacao"].get("manifesto_estranho") or {}).get("sha256") == R312.get("sha")
            and rec_["python_isolado"]["orig_argv"] == [str(x_) for x_ in sys.orig_argv] and rec_["python_isolado"]["inspect"] is False)


R312.clear()
R33.clear()
os.replace = _rep_f3
try:
    decoy("R33_R32_B_exato_mudanca_logo_depois_do_os_replace_do_rollback", 2, "ROLLBACK_DIVERGE",
          patches_extra=dict(servico_responde=_sonda_que_muta_na(6)), extra_ok=_ok_r32b,
          nota="R32-B (o caso EXATO do auditor, forma F3): a 6a sonda muda o manifesto (dispara o rollback) e outra mudanca vem IMEDIATAMENTE depois do os.replace do "
               "rollback; na R3.2 a recusa era visivel (rc 2, ROLLBACK_DIVERGE) mas o CONTRATO_CANONICO_B3.md ficava no decoy e o pos_rollback nao rodava; na R3.3 o "
               "contrato sai, a sonda apos_rollback roda e o recibo grava o sha do manifesto em disco (os bytes alheios); o recibo grava sys.orig_argv")
finally:
    os.replace = _REAL_REPLACE_33
R312.clear()
R33.clear()
decoy_reset()

# --- R31-3: o pino do manifesto do kernel do recibo pre-selo vem do SELO ANTERIOR (fonte externa), nunca de campo do proprio recibo
ANT_PD = MOD.estado_anterior(PD, MOD.carregar_canonical(PD)[0])


def _pre32(nome, mut, base):
    rj_ = json.loads(Path(base).read_bytes())
    mut(rj_)
    p_ = AT32 / ("PRE_%s.json" % nome)
    p_.write_bytes(json.dumps(rj_, ensure_ascii=False).encode("utf-8"))
    return p_


_falso_k = sha_b(b"manifesto do kernel de outro rito")
_p_r313 = _pre32("selo_certo_kernel_declarado_pelo_proprio_recibo", lambda r: (
    r["nos"]["selo"].update(tgl_kernel_proof_manifest_sha256=_falso_k), r["nos"]["kernel"].update(
        sha256=_falso_k, raiz_sha256=sha_b(b"outra raiz"), audit_sha256=sha_b(b"outro audit"), impressao_formal=sha_b(b"outra impressao"))), R_PD)
unit("R32_R31_3_exato_selo_certo_kernel_do_proprio_recibo", lambda: _conferir_pre(_p_r313, ANT_PD, PD, False, sha(_p_r313)), "RECIBO_PRE_SELO_NAO_CORRESPONDE",
     nota="R31-3 (o caso EXATO do auditor, sobre o recibo pre-selo do decoy): selo.sha256 verdadeiro; selo.tgl_kernel_proof_manifest_sha256, kernel.sha256, raiz, Audit e "
          "impressao forjados de forma CONSISTENTE no proprio recibo; na R3.1 era aceito; na R3.2 o pino vem do selo anterior (custodia) e recusa")
decoy("R32_R31_3_exato_no_decoy_de_producao", 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", pre=_p_r313, extra_ok=pd_intocado,
      nota="R31-3: o mesmo recibo forjado (com o sha dele, como se vNNN_pins o pinasse) pelo caminho inteiro da producao-decoy: recusa antes da bateria")
_p_r313b = _pre32("kernel_sha_verdadeiro_raiz_e_impressao_forjadas", lambda r: r["nos"]["kernel"].update(
    raiz_sha256=sha_b(b"outra raiz"), audit_sha256=sha_b(b"outro audit"), impressao_formal=sha_b(b"outra impressao")), R_PD)
unit("R32_R31_3_variante_pino_verdadeiro_raiz_audit_impressao_forjados", lambda: _conferir_pre(_p_r313b, ANT_PD, PD, False, sha(_p_r313b)), "RECIBO_PRE_SELO_NAO_CORRESPONDE",
     nota="R31-3: o pino do kernel e o verdadeiro, mas raiz, Audit e impressao do ANTES sao forjados: recalculados do manifesto do kernel que o selo anterior pina, recusa")
_selo_forj = AT32 / "selo_anterior_forjado.json"
_sj = json.loads(SELO_ANT.read_bytes())
_sj["sha256"]["tgl_kernel_proof_manifest.json"] = _falso_k
_selo_forj.write_bytes(json.dumps(_sj, ensure_ascii=False, indent=1).encode("utf-8"))
unit("R32_R31_3_variante_selo_anterior_forjado", lambda: MOD.conferir_recibo_pre_selo(_p_r313, ANT_PD, PD, False, sha(_p_r313), _selo_forj, KMAN_ANT),
     "SELO_ANTERIOR_NAO_E_O_PINADO", nota="R31-3: um --selo-anterior escrito a mao (com o pino do kernel forjado) nao e o selo pinado no manifesto da Bancada")
unit("R32_R31_3_variante_kernel_manifesto_anterior_de_outro_rito", lambda: MOD.conferir_recibo_pre_selo(R_PD, ANT_PD, PD, False, sha(R_PD), SELO_ANT, NOS392 / "tgl_kernel_proof_manifest.json"),
     "KERNEL_MANIFESTO_ANTERIOR_NAO_E_O_DO_SELO", nota="R31-3: o manifesto do kernel dado como anterior e o v392 sintetico: nao e o que o selo anterior pina")
unit("R32_R31_3_variante_sem_selo_anterior", lambda: MOD.conferir_recibo_pre_selo(R_PD, ANT_PD, PD, False, sha(R_PD)), "SELO_ANTERIOR_AUSENTE",
     nota="R31-3: sem --selo-anterior e --kernel-manifesto-anterior o recibo pre-selo nao se cruza (fail-closed)")
SEM_SELO_ANT.update({"R32_R31_3_sub_sem_selo_anterior"})
run("R32_R31_3_sub_sem_selo_anterior", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
                                        "--fase", "pos_selo", "--evento", "SANDBOX:R31-3", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA,
                                        "--recibo-pre-selo", R1B, "--recibo-pre-selo-sha256", sha(R1B)], 2, "SELO_ANTERIOR_AUSENTE", bancada=B2,
    nota="R31-3 pelo caminho inteiro (subprocesso): o recibo pre-selo VERDADEIRO sem o selo anterior e recusado antes da bateria")
run("R32_R31_3_sub_selo_anterior_sem_recibo_pre_selo", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox",
                                                        "--modo", "ensaio", "--fase", "pos_selo", "--selo-anterior", SELO_ANT, "--kernel-manifesto-anterior", KMAN_ANT], 2,
    "SELO_ANTERIOR_SEM_RECIBO_PRE_SELO", bancada=B2, nota="R31-3: flag sem efeito nao e aceita em silencio")
_ant_k = dict(ANT_B2, _man=dict(ANT_B2["_man"], sincronizacao=dict(kernel_manifesto_sha256="e" * 64)))


def _recusa_com(fn, prefixo, contem):
    try:
        fn()
        return False
    except MOD.Recusa as exc:
        return str(exc).startswith(prefixo) and contem in str(exc)


checar("R32_R31_3_variante_manifesto_da_bancada_registra_outro_kernel",
       lambda: _recusa_com(lambda: _conferir_pre(R1B, _ant_k, B2, False, sha(R1B)), "RECIBO_PRE_SELO_NAO_CORRESPONDE", "registra o manifesto do kernel"),
       nota="R31-3 (B4 em diante): o manifesto vigente gravado por um B(n) R3.2 registra o manifesto do kernel; se nao e o que o selo anterior pina, recusa")
checar("R32_R31_3_exato_a_recusa_vem_do_selo_anterior",
       lambda: _recusa_com(lambda: _conferir_pre(_p_r313, ANT_PD, PD, False, sha(_p_r313)), "RECIBO_PRE_SELO_NAO_CORRESPONDE", "SELO ANTERIOR")
       and _recusa_com(lambda: _conferir_pre(_p_r313b, ANT_PD, PD, False, sha(_p_r313b)), "RECIBO_PRE_SELO_NAO_CORRESPONDE", "SELO ANTERIOR"),
       nota="R31-3: as duas recusas acima vem da comparacao com o manifesto do kernel que o SELO ANTERIOR pina (fonte externa), nao das conferencias internas da R3.1")
unit("R32_R31_3_contraprova_recibo_1b_com_o_selo_anterior", lambda: (lambda r_: r_["kernel_cruzado_com_o_selo_anterior"]["kernel_manifesto_anterior"]["sha256"] == sha(KMAN_ANT)
                                                                       and r_["kernel_manifesto_anterior_sha256"] == sha(KMAN_ANT))(_conferir_pre(R1B, ANT_B2, B2, False, sha(R1B))) or
     (_ for _ in ()).throw(MOD.Recusa("CONTRAPROVA_FALHOU")), None, nota="contraprova: o recibo do run 1b cruza com o selo anterior da custodia do sandbox")

# --- R31-4: o build log plausivel (as linhas do lake) e o log do Audit por nome de declaracao distinto
_ku("R32_R31_4_exato_build_log_com_um_caractere", _kr("r32_build_um_caractere", lambda k: k.update(build_full_log=_blog("r32_um_caractere", b"x\n"))),
    "LOG_DE_BUILD_IMPLAUSIVEL", nota="R31-4 (o caso EXATO do auditor): um build log de 1 caractere era aceito na R3.1")
_ksub("R32_R31_4_sub_build_log_com_um_caractere", _kr("r32_build_um_caractere_sub", lambda k: k.update(build_full_log=_blog("r32_um_caractere_sub", b"x\n"))),
      "LOG_DE_BUILD_IMPLAUSIVEL", nota="R31-4 pelo caminho inteiro do aplicar: o T17 FALHA e nada se grava")
_ku("R32_R31_4_variante_so_a_linha_final", _kr("r32_build_so_final", lambda k: k.update(build_full_log=_blog("r32_so_final", b"Build completed successfully (4 jobs).\n"))),
    "LOG_DE_BUILD_IMPLAUSIVEL", nota="R31-4: a linha final sem os jobs das pedras, da raiz e do Audit")
_ku("R32_R31_4_variante_sem_a_linha_final", _kr("r32_build_sem_final", lambda k: k.update(build_full_log=_blog("r32_sem_final", LB.replace(b"Build completed successfully (4 jobs).\n", b"")))),
    "Build completed successfully", nota="R31-4: os jobs sem a linha final do lake")
_ku("R32_R31_4_variante_falta_o_job_de_uma_pedra", _kr("r32_build_sem_pedra_b", lambda k: k.update(build_full_log=_blog("r32_sem_pedra_b", b"".join(
    l_ for l_ in LB.splitlines(keepends=True) if b"PedraSinteticaB" not in l_)))), "TGLExt.PedraSinteticaB", nota="R31-4: falta o job de uma pedra listada")
# o caso exato do A2-novo: Audit.lean pinado com 5 #print axioms (2 das pedras + 3 antigas) e o log com uma linha repetida 3 vezes
_arv5 = AT32 / "arv_audit_maior"
copiar_sem_juncao(FX / "kernel_src", _arv5)
_aud5 = (_arv5 / "TGL" / "Audit.lean").read_bytes() + b"".join(b"#print axioms TGLExt.Velha.k%d\n" % i_ for i_ in range(3))
(_arv5 / "TGL" / "Audit.lean").write_bytes(_aud5)
_ni5 = nos_ataque("r32_audit_maior", lambda m: m["formal_files_sha256"].update({"TGL/Audit.lean": sha_b(_aud5)}))
_rep = b"'TGLExt.PedraSinteticaA.um' depends on axioms: [propext, Classical.choice, Quot.sound]\n"


def _k_audit5(nome, log_a):
    return _kr(nome, lambda k: (k.update(arvore=str(_arv5), audit_log=_blog(nome, log_a)), k["audit"].update(sha256_depois=sha_b(_aud5))))


_ku("R32_R31_4_exato_audit_log_com_linhas_repetidas", _k_audit5("r32_audit_repetido", LA + _rep * 3), "LOG_DO_AUDIT_CURTO", ni=_ni5,
    nota="R31-4 (o caso EXATO do auditor): o Audit.lean de 5 #print axioms e o log que repete 3 vezes a linha de uma pedra (5 linhas >= 5); na R3.1 era aceito; "
         "na R3.2 contam as declaracoes DISTINTAS (2 < 5)")
_ku("R32_R31_4_contraprova_do_auditor_audit_maior_log_curto", _k_audit5("r32_audit_curto", LA), "LOG_DO_AUDIT_CURTO", ni=_ni5,
    nota="a contraprova do auditor (o log sem repeticao) segue recusada")
_ku("R32_R31_4_variante_nomes_distintos_mas_um_nao_e_do_Audit", _kr("r32_audit_nome_estranho", lambda k: k.update(audit_log=_blog("r32_audit_nome_estranho",
    b"'TGLExt.PedraSinteticaA.um' depends on axioms: [propext, Classical.choice, Quot.sound]\n'TGLExt.Outra.x' does not depend on any axioms\n"))),
    "LOG_DO_AUDIT_CURTO", nota="R31-4: 2 nomes distintos (o minimo) mas um deles nao e impresso pelo Audit.lean pinado: o nome que falta e nomeado")
_ku("R32_R31_4_variante_a_mesma_declaracao_duas_vezes", _kr("r32_audit_dup", lambda k: k.update(audit_log=_blog("r32_audit_dup", _rep * 2))),
    "LOG_DO_AUDIT_CURTO", nota="R31-4: 2 linhas, 1 declaracao distinta, contra 2 #print axioms")
# o formato REAL (custodia v390, so leitura): as regras da R31-4 valem no build e no Audit reais
_CUST390 = Path("C:/IALD/Artigo/the_boundary_BACKUPS/um_v390_0f5154bcc2f931cb")
_real_b = MOD.normalizar_log((_CUST390 / "rodadas" / "tgl_kernel_build_capture.txt").read_bytes())[0]
_real_a = MOD.normalizar_log((_CUST390 / "rodadas" / "tgl_kernel_audit_capture.txt").read_bytes())[0]
_real_aud = (_CUST390 / "Lean" / "tgl_kernel" / "TGL" / "Audit.lean").read_text(encoding="utf-8")
_real_jobs = set(MOD.RE_LAKE_JOB.findall(_real_b))
_real_print = {x.lstrip("@") for x in MOD.RE_PRINT_AXIOMS_NOME.findall(_real_aud)}
_real_decl = {m_.group(1).lstrip("@") for m_ in MOD.RE_LOG_DECL.finditer(_real_a)}
checar("R32_R31_4_formato_real_v390_build_e_audit",
       lambda: {"TGLExt", "TGL.Audit", "TGLExt.Fundacao"} <= _real_jobs and MOD.RE_LAKE_FIM.search(_real_b) is not None and len(_real_print) == len(_real_decl) == 8523
       and not (_real_print - _real_decl) and MOD.contar_sorry(_real_b)[0] == 0 and MOD.contar_sorry(_real_a)[0] == 0,
       nota="R31-4 no formato REAL (custodia v390, so leitura): os 3 arquivos formais mudados na v390 (TGLExt, TGL.Audit, TGLExt.Fundacao) tem linha Built no build "
            "log; a linha final existe; o Audit.lean imprime 8523 nomes distintos e o log os traz todos; nenhum sorry nas tres formas de busca",
       jobs_no_build_real=len(_real_jobs), print_distintos=len(_real_print), decl_distintas_no_log=len(_real_decl),
       fontes=[str(_CUST390 / "rodadas" / "tgl_kernel_build_capture.txt"), str(_CUST390 / "rodadas" / "tgl_kernel_audit_capture.txt"),
               str(_CUST390 / "Lean" / "tgl_kernel" / "TGL" / "Audit.lean")])

# --- R31-5: o aviso de sorry partido entre linhas e o escapado em JSON
_pre_real, _ = LINHA_REAL.rstrip(b"\r").split(b"declaration uses")
_ku("R32_R31_5_exato_quebra_entre_declaration_e_uses", _kr("r32_quebra_decl_uses", lambda k: k.update(build_full_log=_blog("r32_quebra_decl_uses",
    LB + _pre_real + b"declaration\nuses `sorry`\n"))), "ocorrencia(s) de sorry",
    nota="R31-5 (o caso EXATO do auditor): o aviso real partido entre 'declaration' e 'uses' (captura com largura fixa); na R3.1 era aceito")
_ku("R32_R31_5_exato_json_com_crase_escapada", _kr("r32_json_crase", lambda k: k.update(build_full_log=_blog("r32_json_crase",
    LB + b'{"severity":"warning","data":"declaration uses \\u0060sorry\\u0060"}\n'))), "ocorrencia(s) de sorry",
    nota="R31-5 (o caso EXATO do auditor): a saida em JSON com a crase escapada \\u0060; na R3.1 era aceita")
_ksub("R32_R31_5_sub_json_com_crase_escapada", _kr("r32_json_crase_sub", lambda k: k.update(build_full_log=_blog("r32_json_crase_sub",
      LB + b'{"severity":"warning","data":"declaration uses \\u0060sorry\\u0060"}\n'))), "ocorrencia(s) de sorry")
_ku("R32_R31_5_variante_varias_quebras_e_recuo_CRLF", _kr("r32_quebras_crlf", lambda k: k.update(build_full_log=_blog("r32_quebras_crlf",
    LB + _pre_real + b"declaration\r\n      uses\r\n  `sorry`\r\n"))), "ocorrencia(s) de sorry", nota="R31-5: quebras CRLF e recuo entre as tres partes")
_ku("R32_R31_5_variante_json_com_quebra_escapada_e_aspas_escapadas", _kr("r32_json_quebra", lambda k: k.update(build_full_log=_blog("r32_json_quebra",
    LB + b'{"data":"declaration\\nuses \\u0027sorry\\u0027","pos":{"line":3}}\n'))), "ocorrencia(s) de sorry",
    nota="R31-5: no JSON, a quebra escapada (barra-n) entre as palavras e as aspas como \\u0027")
_ku("R32_R31_5_variante_sorryAx_escapado_em_JSON_no_log_do_Audit", _kr("r32_json_sorryax", lambda k: k.update(audit_log=_blog("r32_json_sorryax",
    LA + b'{"data":"\'TGLExt.X.y\' depends on axioms: [propext, sorry\\u0041x]"}\n'))), "sorry",
    nota="R31-5: sorryAx com uma letra escapada numa linha JSON do log do Audit")
_ku("R32_R31_5_contraprova_palavras_soltas_sem_sorry_aceito", _kr("r32_palavras_soltas", lambda k: k.update(build_full_log=_blog("r32_palavras_soltas",
    LB + b"info: declaration ok\nuses no axiom; the word sorry alone is not a warning\n"))), None, aceita=True,
    nota="contraprova: 'declaration', 'uses' e 'sorry' soltos, sem o aviso (sem delimitador), nao contam")
checar("R32_R31_5_contagem_no_log_real_do_Nos_igual_nas_tres_formas",
       lambda: (lambda n_, por_: por_[0] == AMOSTRA["n_avisos_crase_no_arquivo"] + AMOSTRA["n_avisos_aspas_no_arquivo"] + _N_SORRYAX and n_ == max(por_))(*MOD.contar_sorry(_am_txt)),
       nota="R31-5: no log REAL do Nos (so lido), a forma normalizada conta o mesmo que a R3.1; as outras formas nao reduzem a contagem", por_forma=MOD.contar_sorry(_am_txt)[1])

# --- R31-6: chave duplicada no CRITERIOS (e no recibo do kernel) e a X19 cruzada com as pedras
_txt_crit = CRIT.read_text(encoding="utf-8")
assert '"j1_declaracoes": 2,' in _txt_crit and '"x19": "nao",' in _txt_crit
_c_dup = AT32 / "CRITERIOS_dup.json"
_c_dup.write_text(_txt_crit.replace('"j1_declaracoes": 2,', '"j1_declaracoes": 159,\n  "j1_declaracoes": 2,', 1), encoding="utf-8")
unit("R32_R31_6_exato_chave_duplicada_em_esperados", lambda: MOD.carregar_criterios(_c_dup, sha(_c_dup), "v392"), "CRITERIOS_CHAVE_DUPLICADA",
     nota="R31-6 (o caso EXATO do auditor): 'j1_declaracoes' duas vezes (159 e 2); na R3.1 o json.loads ficava com o ultimo (2)")
_c_dup2 = AT32 / "CRITERIOS_dup_x19.json"
_c_dup2.write_text(_txt_crit.replace('"x19": "nao",', '"x19": "sim",\n "x19": "nao",', 1), encoding="utf-8")
unit("R32_R31_6_variante_x19_duplicada_no_topo", lambda: MOD.carregar_criterios(_c_dup2, sha(_c_dup2), "v392"), "CRITERIOS_CHAVE_DUPLICADA",
     nota="R31-6: a decisao X19 escrita duas vezes ('sim' e depois 'nao')")
run("R32_R31_6_sub_chave_duplicada", _BASE_A3 + ["--criterios", _c_dup, "--criterios-sha256", sha(_c_dup)], 2, "CRITERIOS_CHAVE_DUPLICADA", bancada=B2,
    nota="R31-6 pelo caminho inteiro: recusa antes da bateria, rc 2")
_k_dup = AT32 / "KR_chave_duplicada.json"
_k_dup.write_text(K_OK.read_text(encoding="utf-8").replace('"rc": 0,', '"rc": 1,\n "rc": 0,', 1), encoding="utf-8")
assert _k_dup.read_text(encoding="utf-8").count('"rc"') == 2
_ku("R32_R31_6_variante_recibo_do_kernel_com_chave_duplicada", _k_dup, "KERNEL_RECIBO_CHAVE_DUPLICADA", nota="R31-6: 'rc' 1 e depois 0 no recibo do kernel")
_c_x19 = AT32 / "CRITERIOS_x19_sim.json"
_cj = json.loads(_txt_crit)
_cj["x19"] = "sim"
_c_x19.write_text(json.dumps(_cj, ensure_ascii=False, indent=1), encoding="utf-8")
_CRIT_X19 = MOD.carregar_criterios(_c_x19, sha(_c_x19), "v392")
_ku("R32_R31_6_exato_x19_sim_sem_a_pedra_BGL", K_OK, "X19_NAO_CONFERE_COM_AS_PEDRAS", criterios=_CRIT_X19,
    nota="R31-6 (o caso EXATO do auditor): x19='sim' no CRITERIOS pinado e nenhuma pedra LightNetStandardWedgeDataBGL no recibo; na R3.1 era aceito")
_ku("R32_R31_6_variante_x19_nao_com_a_pedra_BGL", _kr("r32_x19_nao_com_bgl", lambda k: k["pedras"].append(dict(path="TGLExt/" + MOD.X19_PEDRA, sha256=sha_b(b"bgl"),
                                                                                                               declaracoes=["TGLExt.LightNetStandardWedgeDataBGL.x"]))),
    "X19_NAO_CONFERE_COM_AS_PEDRAS", nota="R31-6: x19='nao' e o recibo traz a pedra X19")
run("R32_R31_6_sub_x19_sim_sem_a_pedra", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar",
                                          "--fase", "pos_selo", "--evento", "SANDBOX:R31-6", "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA,
                                          "--criterios", _c_x19, "--criterios-sha256", sha(_c_x19)], 3, veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", bancada=B2,
    extra_ok=lambda j, r: "X19_NAO_CONFERE_COM_AS_PEDRAS" in testes(j)["T17_LEAN_KERNEL"]["detalhe"], nota="R31-6 pelo caminho inteiro: o T17 FALHA e nada se grava")
# contraprova X19 = 'sim' com a pedra presente e coerente em tudo (arvore, manifesto re-pinado pelo selo, logs, pedras == diff formal)
_arvx = AT32 / "arv_x19"
copiar_sem_juncao(FX / "kernel_src", _arvx)
_bgl_b = b"-- SINTETICO (sandbox R3.2): a pedra X19\nnamespace TGLExt.LightNetStandardWedgeDataBGL\ntheorem tres : 3 = 3 := rfl\nend TGLExt.LightNetStandardWedgeDataBGL\n"
(_arvx / "TGLExt" / MOD.X19_PEDRA).write_bytes(_bgl_b)
_audx = (_arvx / "TGL" / "Audit.lean").read_bytes() + b"#print axioms TGLExt.LightNetStandardWedgeDataBGL.tres\n"
(_arvx / "TGL" / "Audit.lean").write_bytes(_audx)
_nix = nos_ataque("r32_x19_sim", lambda m: (m["formal_files_sha256"].update({"TGL/Audit.lean": sha_b(_audx), "TGLExt/" + MOD.X19_PEDRA: sha_b(_bgl_b)}),
                                            m["axiom_report"].update({"TGLExt.LightNetStandardWedgeDataBGL.tres": []})))
_kx = _kr("r32_x19_sim_coerente", lambda k: (
    k.update(arvore=str(_arvx), build_full_log=_blog("r32_x19_build", LB.replace(b"Build completed", "\u2714 [5/5] Built TGLExt.LightNetStandardWedgeDataBGL (1s)\nBuild completed".encode("utf-8"))),
             audit_log=_blog("r32_x19_audit", LA + b"'TGLExt.LightNetStandardWedgeDataBGL.tres' does not depend on any axioms\n")),
    k["audit"].update(sha256_depois=sha_b(_audx)), k["varredura_tokens"].update(arquivos_lean=k["varredura_tokens"]["arquivos_lean"] + 1),
    k["pedras"].append(dict(path="TGLExt/" + MOD.X19_PEDRA, sha256=sha_b(_bgl_b), declaracoes=["TGLExt.LightNetStandardWedgeDataBGL.tres"]))))
_ku("R32_R31_6_contraprova_x19_sim_com_a_pedra_coerente_aceito", _kx, None, ni=_nix, criterios=_CRIT_X19, aceita=True,
    nota="contraprova: x19='sim' com a pedra X19 na arvore, no manifesto pinado pelo selo, nos dois logs e nas pedras do recibo: aceito")

# --- 12-ter item 3 do plano: a varredura de tokens recursiva (inclui TGLExt/O16), recontada pelo B(n)
_ku("R32_T3_exato_varredura_nao_recursiva", _kr("r32_tokens_nao_recursiva", lambda k: k["varredura_tokens"].update(
    arquivos_lean=sum(1 for q_ in (FX / "kernel_src").glob("*.lean")) + sum(1 for q_ in (FX / "kernel_src").glob("*/*.lean")), arquivos_lean_em_TGLExt_O16=0)),
    "TOKENS_VARREDURA_NAO_RECURSIVA",
    nota="12-ter item 3 (o defeito do um.py v391, l.134690, aqui no recibo): a contagem NAO recursiva (sem TGLExt/O16) declarada; o B(n) reconta recursivamente e recusa")
_ksub("R32_T3_sub_varredura_nao_recursiva", _kr("r32_tokens_nao_recursiva_sub", lambda k: k["varredura_tokens"].update(arquivos_lean=4, arquivos_lean_em_TGLExt_O16=0)),
      "TOKENS_VARREDURA_NAO_RECURSIVA")
_ku("R32_T3_variante_recursiva_false", _kr("r32_tokens_recursiva_false", lambda k: k["varredura_tokens"].update(recursiva=False)), "TOKENS_VARREDURA_NAO_RECURSIVA")
_ku("R32_T3_variante_campo_ausente", _kr("r32_tokens_ausente", lambda k: k.pop("varredura_tokens")), "sem os campos")
_ku("R32_T3_variante_contagem_em_texto", _kr("r32_tokens_texto", lambda k: k["varredura_tokens"].update(arquivos_lean="5")), "TOKENS_VARREDURA_NAO_RECURSIVA")
_arvj = AT32 / "arv_com_juncao"
copiar_sem_juncao(FX / "kernel_src", _arvj)
juncao(_arvj / "TGLExt" / "O16" / "j", FX / "kernel_src")
_ku("R32_T3_variante_juncao_dentro_da_arvore", _kr("r32_arvore_juncao", lambda k: k.update(arvore=str(_arvj))), "ARVORE_COM_JUNCAO_OU_LINK",
    nota="12-ter item 3: a varredura recursiva nao segue juncao; uma juncao na arvore do build e recusada (desfeita no fecho, nunca seguida)")
_n_rec, _n_o16, _lk = MOD.contar_lean_recursivo(_CUST390 / "Lean" / "tgl_kernel")
_n_nao_rec = sum(1 for q_ in (_CUST390 / "Lean" / "tgl_kernel" / "TGLExt").glob("*.lean"))
checar("R32_T3_formato_real_v390_a_recursao_importa",
       lambda: _n_o16 > 0 and not _lk and _n_rec > _n_nao_rec,
       nota="12-ter item 3 no formato REAL (custodia v390, so leitura): a arvore tem .lean em TGLExt/O16 que uma varredura de TGLExt/*.lean nao ve",
       arquivos_lean_recursivo=_n_rec, arquivos_lean_em_TGLExt_O16=_n_o16, TGLExt_nao_recursivo=_n_nao_rec)

# ================================================================ R3.4: os tres consertos da gerencia c1 (F0.6) -- S (salto), P (bateria por versao), M (modulos de auditoria)
# Prefixos: R34_S_ (salto: a Bancada pinada numa versao anterior a do Nos, com a cadeia de selos verificada por hash), R34_P_ (a bateria regenerada por script em cada versao, pinada,
# com o pino do um.py lido dos pinos da cadeia), R34_M_ (o modulo de auditoria sem declaracoes so passa em lista explicita e com a fonte conferida por script).
NOS393 = RAIZ / "nos_v393s"                          # o Nos sintetico SEGUINTE ao v392 sintetico (camada v393 do montar_sandbox R3.4)
CS = FX / "cadeia_de_selo"                           # a pasta cadeia_de_selo de ENSAIO (base_vJ + registros do instalador + backups de bytes)
AT34 = RAIZ / "aud34"
AT34.mkdir(exist_ok=True)
CADEIA_REAL = AQUI / "CADEIA_DE_SELOS_v394.json"     # a cadeia REAL v392 -> v393, gerada pelo gerador contra a pasta real cadeia_de_selo
CRIT393 = FX / "CRITERIOS_v393_SINTETICO.json"
CRIT393_SHA = sha(CRIT393)
CRIT393_OBJ = MOD.carregar_criterios(CRIT393, CRIT393_SHA, "v393")
K393 = FX / "KERNEL_RECIBO_v393s_SINTETICO_VALIDO.json"
K393_SHA = sha(K393)
NI393 = MOD.ler_nos(NOS393, "v393")
K393_OBJ = json.loads(K393.read_bytes())


def gerar_cadeia(nome, de, ate, cadeia=CS):
    """roda o gerador REAL (gerar_cadeia_de_selos.py) contra uma pasta cadeia_de_selo; devolve (arquivo, sha256)."""
    saida = FX / ("CADEIA_%s.json" % nome)
    r = subprocess.run([PY, "-I", "-B", "-X", "utf8", str(GERAR_CADEIA), "--cadeia", str(cadeia), "--de", de, "--ate", ate, "--saida", str(saida)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, r.stdout + r.stderr
    return saida, sha(saida)


CH_392, CH_392_SHA = gerar_cadeia("391_392", "v391", "v392")
CH_393, CH_393_SHA = gerar_cadeia("391_393", "v391", "v393")
CH_392_393, CH_392_393_SHA = gerar_cadeia("392_393", "v392", "v393")


def cadeia_derivada(nome, mutar, base=CH_392):
    """uma copia da cadeia gerada com `mutar(dict)` aplicado (e gravada ao lado); devolve (arquivo, sha256)."""
    c = json.loads(Path(base).read_bytes())
    mutar(c)
    p = FX / ("CADEIA_%s.json" % nome)
    p.write_bytes(json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8"))
    return p, sha(p)


def copia_adulterada(origem, nome, mut):
    """copia (byte a byte, exceto `mut(bytes)`) de um arquivo da cadeia para fx/cadeia_adulterada/<nome>/; devolve o caminho."""
    d = FX / "cadeia_adulterada" / nome
    d.mkdir(parents=True, exist_ok=True)
    p = d / Path(origem).name
    p.write_bytes(mut(Path(origem).read_bytes()))
    return str(p)


def bancada_copia(nome, mut=None):
    d = RAIZ / nome
    copiar_sem_juncao(B2, d)
    if mut:
        m_ = json.loads((d / "canonical_contracts.json").read_bytes())
        mut(m_)
        (d / "canonical_contracts.json").write_bytes(json.dumps(m_, ensure_ascii=False, indent=1).encode("utf-8"))
    return d


def args_pre(bancada, cadeia=None, cadeia_sha=None, nos=NOS, versao="v392", bateria=None, extra=()):
    b_ = bateria or (bt_min_pre, bt_min_pre_sha)
    return (["--bancada", bancada, "--nos", nos, "--versao", versao, "--fase", "pre_selo", "--modo", "ensaio", "--sandbox", "--bateria", b_[0], "--bateria-sha256", b_[1]]
            + (["--cadeia-de-selos", cadeia] if cadeia else []) + (["--cadeia-de-selos-sha256", cadeia_sha] if cadeia_sha else []) + list(extra))


SELO_392, KMAN_392 = NOS392 / "um_absoluto_selo.json", NOS392 / "tgl_kernel_proof_manifest.json"


def args_pos(bancada, recibo, cadeia=None, cadeia_sha=None, nos=NOS393, versao="v393", modo="aplicar", kernel=True, extra=()):
    a_ = ["--bancada", bancada, "--nos", nos, "--versao", versao, "--fase", "pos_selo", "--modo", modo, "--sandbox", "--bateria", bt_min, "--bateria-sha256", bt_min_sha,
          "--recibo-pre-selo", recibo, "--recibo-pre-selo-sha256", sha(recibo), "--selo-anterior", SELO_392, "--kernel-manifesto-anterior", KMAN_392]
    if modo == "aplicar":
        a_ += ["--evento", "SANDBOX:R34"]
    if kernel:
        a_ += ["--kernel-recibo", K393, "--kernel-recibo-sha256", K393_SHA, "--criterios", CRIT393, "--criterios-sha256", CRIT393_SHA]
    if cadeia:
        a_ += ["--cadeia-de-selos", cadeia, "--cadeia-de-selos-sha256", cadeia_sha]
    return a_ + list(extra)


# --- S01: o salto aceito (a Bancada pina v391, o Nos tem v392; a cadeia de selos v391 -> v392 verifica por hash)
b2sa = bancada_copia("b2sa")
d_s1, j_s1 = run("R34_S_pre_selo_salto_aceito", args_pre(b2sa, CH_392, CH_392_SHA), 0, veredito_esp="REPINADA_B3__SALTO_v391_v392__ENSAIO", bancada=b2sa, saida=S / "R34_S_pre_selo_salto",
                 extra_ok=lambda j, r: (lambda rec: rec["salto"]["versoes_puladas"] == ["v392"] and rec["salto"]["de"]["versao"] == "v391" and rec["salto"]["ate"]["versao"] == "v392"
                                        and rec["salto"]["proxima_a_selar"] == "v393" and rec["cadeia_de_selos"]["n_elos"] == 2 and rec["cadeia_de_selos"]["sha256"] == CH_392_SHA
                                        and rec["salto"]["cadeia"]["sha256"] == CH_392_SHA and rec["bateria_resultado"]["falha"] == 0 and rec["manifesto_anterior"]["version"] == "v391"
                                        and rec["manifesto_novo"]["deployment_id"].startswith("B3-v392-") and rec["manifesto_anterior"]["estado_do_contrato_instalado"] == "PIN_CHANGED"
                                        and rec["salto"]["de"]["manifesto_da_bancada_sha256"] == rec["manifesto_anterior"]["sha256"]
                                        and rec["cadeia_de_selos"]["ligacoes"][0]["registro_sha256"] == rec["salto"]["cadeia"]["ligacoes"][0]["registro_sha256"])(recibo_de(j)),
                 nota="S: a Bancada pinada em v391 contra o Nos v392 (um passo atras): a cadeia de selos (2 elos: copias de bytes, selo pina o um.py e o kernel, registro do instalador com os "
                      "backups de bytes) e verificada por hash; o recibo declara o salto, as versoes puladas e o veredito REPINADA_B3__SALTO_v391_v392__ENSAIO; a copia da Bancada fica intocada")
R_SALTO = sorted((S / "R34_S_pre_selo_salto").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
R_SALTO_SHA = sha(R_SALTO)

# --- S02-S07: a cadeia ausente, sem pino, com pino errado, sem o arquivo; flag sem efeito; Bancada a frente
run("R34_S_atrasada_sem_cadeia_recusa", args_pre(b2sa), 2, "BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS", bancada=b2sa,
    nota="S (o conserto pedido): sem cadeia verificavel o salto e recusado -- era a v394 sem saida (BATERIA_FALHOU + versao_alvo diferente da pinada)")
run("R34_S_cadeia_sem_sha_recusa", args_pre(b2sa, CH_392, None), 2, "CADEIA_DE_SELOS_SHA_AUSENTE", bancada=b2sa, nota="S: uma cadeia sem pino em vNNN_pins nao vale")
run("R34_S_cadeia_sha_divergente_recusa", args_pre(b2sa, CH_392, "5" * 64), 2, "CADEIA_DE_SELOS_SHA_DIVERGE", bancada=b2sa)
run("R34_S_sha_da_cadeia_sem_o_arquivo", args_pre(b2sa, None, CH_392_SHA), 2, "CADEIA_DE_SELOS_AUSENTE", bancada=b2sa, nota="S: --cadeia-de-selos-sha256 sem --cadeia-de-selos nao e aceito em silencio")
run("R34_S_cadeia_inexistente_recusa", args_pre(b2sa, FX / "CADEIA_que_nao_existe.json", CH_392_SHA), 2, "CADEIA_DE_SELOS_AUSENTE", bancada=b2sa)
b2_a_frente = bancada_copia("b2_a_frente", lambda m: m["canonical"].update(version="v393"))
run("R34_S_bancada_a_frente_do_nos_recusa", args_pre(b2_a_frente, CH_392, CH_392_SHA), 2, "BANCADA_A_FRENTE_DO_NOS", bancada=b2_a_frente,
    nota="S: a Bancada pina v393 e o Nos tem v392: um salto so vai para a frente")
NOS391 = CS / "v392" / "base_v391"                    # a copia completa do Nos v391 (um.py, selo, core e manifesto do kernel) que a cadeia de ensaio guarda
b2_em_dia = RAIZ / "b2_em_dia"
copiar_sem_juncao(B2, b2_em_dia)
m_ed = json.loads((b2_em_dia / "canonical_contracts.json").read_bytes())
m_ed["canonical"]["script"]["path"] = str(NOS391 / "um.py")
m_ed["canonical"]["seal"]["path"] = str(NOS391 / "um_absoluto_selo.json")
(b2_em_dia / "canonical_contracts.json").write_bytes(json.dumps(m_ed, ensure_ascii=False, indent=1).encode("utf-8"))
run("R34_S_contraprova_bancada_em_dia_sem_cadeia_ja_sincronizada", ["--bancada", b2_em_dia, "--nos", NOS391, "--versao", "v391", "--fase", "pre_selo", "--modo", "ensaio",
                                                                  "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=b2_em_dia,
    extra_ok=lambda j, r: "salto" not in recibo_de(j) or recibo_de(j)["salto"] is None, nota="contraprova: a Bancada em dia (pinada na versao do Nos) segue JA_SINCRONIZADA, sem cadeia e sem salto no recibo")
run("R34_S_cadeia_com_a_bancada_em_dia_recusa", ["--bancada", b2_em_dia, "--nos", NOS391, "--versao", "v391", "--fase", "pre_selo", "--modo", "ensaio", "--bateria", bt_min_pre,
                                                  "--bateria-sha256", bt_min_pre_sha, "--cadeia-de-selos", CH_392, "--cadeia-de-selos-sha256", CH_392_SHA], 2, "CADEIA_DE_SELOS_SEM_SALTO", bancada=b2_em_dia,
    nota="S: a flag sem efeito (a Bancada ja pina a versao do Nos) nao e aceita em silencio")

# --- S08-S20: a cadeia adulterada de todas as formas (cada uma deriva a cadeia boa e muda UMA coisa)
um_392_adulterado = copia_adulterada(json.loads(CH_392.read_bytes())["elos"][1]["um_py"]["path"], "um_392_um_byte", lambda b: b[:-1] + bytes([b[-1] ^ 1]))


def _mut_um_byte(c):
    c["elos"][1]["um_py"]["path"] = um_392_adulterado         # o sha pinado e o do arquivo bom


def _mut_selo_outra_versao(c):
    c["elos"][1]["selo"] = dict(c["elos"][0]["selo"])         # o selo da v391 no lugar do da v392 (copia boa de outra versao)


def _mut_selo_nao_pina_o_um_py(c):
    p_ = json.loads(Path(c["elos"][1]["selo"]["path"]).read_bytes())
    p_["sha256"]["um.py"] = sha_b(b"outro um.py")
    novo_ = copia_adulterada(c["elos"][1]["selo"]["path"], "selo_nao_pina", lambda b: json.dumps(p_, ensure_ascii=False, indent=1).encode("utf-8"))
    c["elos"][1]["selo"] = _pinar(novo_)


def _mut_selo_nao_pina_o_kernel(c):
    p_ = json.loads(Path(c["elos"][1]["selo"]["path"]).read_bytes())
    p_["sha256"]["tgl_kernel_proof_manifest.json"] = sha_b(b"outro kernel")
    novo_ = copia_adulterada(c["elos"][1]["selo"]["path"], "selo_nao_pina_kernel", lambda b: json.dumps(p_, ensure_ascii=False, indent=1).encode("utf-8"))
    c["elos"][1]["selo"] = _pinar(novo_)


def _mut_um_py_de_outra_versao(c):
    c["elos"][1]["um_py"] = dict(c["elos"][0]["um_py"])       # o um.py v391 no elo v392 (copia boa de outra versao)


def _mut_registro_de_outra_troca(c):
    c3_ = json.loads(CH_393.read_bytes())
    c["elos"][0]["substituido_na_instalacao_por"]["registro"] = c3_["elos"][1]["substituido_na_instalacao_por"]["registro"]   # o registro da troca v392 -> v393


def _mut_backup_de_outro_conteudo(c):
    c["elos"][0]["substituido_na_instalacao_por"]["backup_um_py"] = c["elos"][1]["um_py"]     # o backup do um.py de v391 e (na verdade) o da v392


def _mut_backup_um_byte(c):
    c["elos"][0]["substituido_na_instalacao_por"]["backup_um_py"]["path"] = copia_adulterada(c["elos"][0]["substituido_na_instalacao_por"]["backup_um_py"]["path"], "backup_um_byte",
                                                                                          lambda b: b[:-1] + bytes([b[-1] ^ 1]))


def _mut_sem_instalacao(c):
    c["elos"][0].pop("substituido_na_instalacao_por")


def _mut_ultimo_elo_com_instalacao(c):
    c["elos"][1]["substituido_na_instalacao_por"] = dict(c["elos"][0]["substituido_na_instalacao_por"])


def _mut_registro_outra_versao_declarada(c):
    c["elos"][0]["substituido_na_instalacao_por"]["versao"] = "v399"


def _mut_contrato(c):
    c["contrato"] = "CADEIA_DE_SELOS_R3"


def _mut_chave_extra(c):
    c["chave_extra"] = 1


def _mut_elo_chave_extra(c):
    c["elos"][0]["autorizado_por"] = "qualquer"


def _mut_caminho_relativo(c):
    c["elos"][1]["um_py"]["path"] = "um.py"


def _mut_copia_ausente(c):
    c["elos"][1]["kernel_manifesto"]["path"] = str(FX / "nao_existe_km.json")


def _mut_sha_maiusculo(c):
    c["elos"][1]["um_py"]["sha256"] = c["elos"][1]["um_py"]["sha256"].upper()


def _mut_um_elo_so(c):
    c["elos"] = c["elos"][1:]


def _mut_reordenada(c):
    c["elos"] = [c["elos"][1], c["elos"][0]]


def _mut_versao_repetida(c):
    c["elos"][1]["versao"] = "v391"


def _mut_versao_invalida(c):
    c["elos"][1]["versao"] = "versao392"


CASOS_S = (("copia_do_um_py_com_um_byte_mudado", _mut_um_byte, "CADEIA_DE_SELOS_COPIA_DIVERGE"),
           ("selo_de_outra_versao", _mut_selo_outra_versao, "CADEIA_DE_SELOS_SELO_DE_OUTRA_VERSAO"),
           ("selo_que_nao_pina_o_um_py", _mut_selo_nao_pina_o_um_py, "CADEIA_DE_SELOS_SELO_NAO_PINA_O_UM_PY"),
           ("selo_que_nao_pina_o_manifesto_do_kernel", _mut_selo_nao_pina_o_kernel, "CADEIA_DE_SELOS_SELO_NAO_PINA_O_KERNEL"),
           ("um_py_de_outra_versao", _mut_um_py_de_outra_versao, "CADEIA_DE_SELOS_UM_PY_DE_OUTRA_VERSAO"),
           ("registro_do_instalador_de_outra_troca", _mut_registro_de_outra_troca, "CADEIA_DE_SELOS_ELO_QUEBRADO"),
           ("backup_de_bytes_de_outro_conteudo", _mut_backup_de_outro_conteudo, "CADEIA_DE_SELOS_ELO_QUEBRADO"),
           ("backup_de_bytes_com_um_byte_mudado", _mut_backup_um_byte, "CADEIA_DE_SELOS_COPIA_DIVERGE"),
           ("elo_sem_a_instalacao_que_o_substituiu", _mut_sem_instalacao, "CADEIA_DE_SELOS_ELO_QUEBRADO"),
           ("ultimo_elo_com_instalacao", _mut_ultimo_elo_com_instalacao, "CADEIA_DE_SELOS_ELO_FINAL_COM_INSTALACAO"),
           ("instalacao_diz_outra_versao_seguinte", _mut_registro_outra_versao_declarada, "CADEIA_DE_SELOS_ELO_QUEBRADO"),
           ("contrato_errado", _mut_contrato, "CADEIA_DE_SELOS_CONTRATO_INVALIDO"),
           ("chave_a_mais_na_raiz", _mut_chave_extra, "CADEIA_DE_SELOS_ILEGIVEL"),
           ("chave_a_mais_no_elo", _mut_elo_chave_extra, "CADEIA_DE_SELOS_ELO_INVALIDO"),
           ("caminho_relativo", _mut_caminho_relativo, "CADEIA_DE_SELOS_CAMINHO_NAO_ABSOLUTO"),
           ("copia_ausente", _mut_copia_ausente, "CADEIA_DE_SELOS_COPIA_AUSENTE"),
           ("sha_em_maiuscula", _mut_sha_maiusculo, "CADEIA_DE_SELOS_ARQUIVO_INVALIDO"),
           ("um_elo_so", _mut_um_elo_so, "CADEIA_DE_SELOS_ILEGIVEL"),
           ("elos_fora_de_ordem", _mut_reordenada, "CADEIA_DE_SELOS_NAO_CONSECUTIVA"),
           ("versao_do_elo_diferente_do_um_py_da_copia", _mut_versao_repetida, "CADEIA_DE_SELOS_UM_PY_DE_OUTRA_VERSAO"),
           ("versao_mal_formada", _mut_versao_invalida, "VERSAO_INVALIDA"))
for nome_, mut_, esp_ in CASOS_S:
    p_, h_ = cadeia_derivada("deriv_" + nome_, mut_)
    run("R34_S_cadeia_%s" % nome_, args_pre(b2sa, p_, h_), 2, esp_, bancada=b2sa, nota="S: a cadeia boa com UMA coisa mudada (%s): recusa %s, antes de qualquer bateria; a copia da Bancada fica intocada" % (nome_, esp_))
# o caso 'elo_final com instalacao' tambem nao deixa passar a chave duplicada
c_dup = FX / "CADEIA_chave_duplicada.json"
c_dup.write_text(CH_392.read_text(encoding="utf-8").replace('"contrato": "CADEIA_DE_SELOS_R3_4",', '"contrato": "CADEIA_DE_SELOS_R3_4",\n "contrato": "CADEIA_DE_SELOS_R3_4",', 1), encoding="utf-8")
assert c_dup.read_text(encoding="utf-8").count('"contrato"') == 2
run("R34_S_cadeia_com_chave_duplicada", args_pre(b2sa, c_dup, sha(c_dup)), 2, "CADEIA_DE_SELOS_CHAVE_DUPLICADA", bancada=b2sa, nota="S: o json.loads ficaria com a ultima; a cadeia pinada nao pode dizer duas coisas (R31-6)")

# --- S: a cadeia que nao parte da Bancada, nao chega ao Nos, ou pula uma versao
run("R34_S_cadeia_que_nao_parte_da_bancada", args_pre(b2sa, CH_392_393, CH_392_393_SHA, nos=NOS393, versao="v393"), 2, "CADEIA_DE_SELOS_NAO_PARTE_DA_BANCADA", bancada=b2sa,
    nota="S: a cadeia v392 -> v393 contra uma Bancada que pina v391: o primeiro elo tem de ser o que a Bancada pina")
run("R34_S_cadeia_que_nao_chega_ao_nos", args_pre(b2sa, CH_392, CH_392_SHA, nos=NOS393, versao="v393"), 2, "CADEIA_DE_SELOS_NAO_CHEGA_AO_NOS", bancada=b2sa,
    nota="S: a cadeia v391 -> v392 contra um Nos que tem v393: o ultimo elo tem de ser o Nos lido agora")
c_pula = FX / "CADEIA_pula_uma_versao.json"
c_pula_o = json.loads(CH_393.read_bytes())
c_pula_o["elos"] = [c_pula_o["elos"][0], c_pula_o["elos"][2]]
c_pula.write_bytes(json.dumps(c_pula_o, ensure_ascii=False, indent=1).encode("utf-8"))
run("R34_S_cadeia_que_pula_uma_versao_sem_elo", args_pre(b2sa, c_pula, sha(c_pula), nos=NOS393, versao="v393"), 2, "CADEIA_DE_SELOS_NAO_CONSECUTIVA", bancada=b2sa,
    nota="S: v391 e v393 sem o elo da v392: nenhuma versao pode ficar sem elo (as 'versoes puladas' sao as que a cadeia lista, todas com copias e instalador)")

# --- S: tres elos (dois passos perdidos): v391 -> v392 -> v393, o Nos tem v393
d_s3, j_s3 = run("R34_S_pre_selo_salto_de_tres_elos_aceito", args_pre(b2sa, CH_393, CH_393_SHA, nos=NOS393, versao="v393"), 0, veredito_esp="REPINADA_B3__SALTO_v391_v393__ENSAIO", bancada=b2sa,
                 extra_ok=lambda j, r: (lambda rec: rec["salto"]["versoes_puladas"] == ["v392", "v393"] and rec["salto"]["proxima_a_selar"] == "v394" and rec["cadeia_de_selos"]["n_elos"] == 3
                                        and [l["de"] + ">" + l["para"] for l in rec["cadeia_de_selos"]["ligacoes"]] == ["v391>v392", "v392>v393"])(recibo_de(j)),
                 nota="S: a recuperacao de atraso vale para qualquer k: a Bancada em v391, o Nos em v393 (2 versoes sem elo B(n)), a cadeia de 3 elos")

# --- S: o pos_selo com o recibo pre-selo de um salto (negativos primeiro: a Bancada b2sa ainda esta intocada)
run("R34_S_pos_selo_recibo_de_salto_sem_cadeia_recusa", args_pos(b2sa, R_SALTO, None, None, modo="ensaio", kernel=False), 2, "RECIBO_PRE_SELO_SALTO_SEM_CADEIA", bancada=b2sa,
    nota="S: o recibo pre-selo de um salto sem a cadeia (--cadeia-de-selos) nao se confere")
run("R34_S_pos_selo_recibo_em_dia_com_cadeia_recusa", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "ensaio",
                                                       "--fase", "pos_selo", "--recibo-pre-selo", R1B, "--recibo-pre-selo-sha256", sha(R1B), "--cadeia-de-selos", CH_392,
                                                       "--cadeia-de-selos-sha256", CH_392_SHA], 2, "CADEIA_DE_SELOS_SEM_SALTO", bancada=B2,
    nota="S: o recibo pre-selo de uma Bancada em dia (JA_SINCRONIZADA) com cadeia: flag sem efeito, recusada")
run("R34_S_pos_selo_cadeia_sem_recibo_pre_selo", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "ensaio",
                                                  "--fase", "pos_selo", "--cadeia-de-selos", CH_392, "--cadeia-de-selos-sha256", CH_392_SHA], 2, "CADEIA_DE_SELOS_SEM_SALTO", bancada=B2)
_rj = json.loads(R_SALTO.read_bytes())
_rj["salto"]["versoes_puladas"] = []
_p_dout = FX / "PRE_salto_versoes_puladas_apagadas.json"
_p_dout.write_bytes(json.dumps(_rj, ensure_ascii=False).encode("utf-8"))
run("R34_S_pos_selo_recibo_com_o_salto_adulterado", args_pos(b2sa, _p_dout, CH_392, CH_392_SHA, modo="ensaio", kernel=False), 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=b2sa,
    extra_ok=lambda j, r: "o salto que o recibo declara nao e o que a cadeia" in str(j.get("recusa")),
    nota="S: o recibo (com o sha dele pinado, como se vNNN_pins o pinasse) declara versoes_puladas vazias; a cadeia diz [v392]: recusa")
_rj2 = json.loads(R_SALTO.read_bytes())
_rj2["veredito"] = "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA"
_p_ver = FX / "PRE_salto_com_veredito_em_dia.json"
_p_ver.write_bytes(json.dumps(_rj2, ensure_ascii=False).encode("utf-8"))
run("R34_S_pos_selo_recibo_de_salto_com_veredito_de_bancada_em_dia", args_pos(b2sa, _p_ver, CH_392, CH_392_SHA, modo="ensaio", kernel=False), 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=b2sa,
    extra_ok=lambda j, r: "REPINADA_B3__SALTO_v391_v392__ENSAIO" in str(j.get("recusa")), nota="S: o veredito do recibo de um salto tem de dizer o salto")
_rj3 = json.loads(R_SALTO.read_bytes())
_rj3["bateria_resultado"]["veredito"] = "BATERIA_FALHOU"
_p_bat = FX / "PRE_salto_bateria_falhou.json"
_p_bat.write_bytes(json.dumps(_rj3, ensure_ascii=False).encode("utf-8"))
run("R34_S_pos_selo_recibo_de_salto_com_bateria_que_falhou", args_pos(b2sa, _p_bat, CH_392, CH_392_SHA, modo="ensaio", kernel=False), 2, "RECIBO_PRE_SELO_INVALIDO", bancada=b2sa)
# o recibo e de uma Bancada que mudou entre o pre_selo e o B(n): outro manifesto, mesmo recibo -> o salto declarado nao confere
b2sd = bancada_copia("b2sd")
run("R34_S_pre_selo_da_bancada_que_depois_mudou", args_pre(b2sd, CH_392, CH_392_SHA), 0, veredito_esp="REPINADA_B3__SALTO_v391_v392__ENSAIO", bancada=b2sd, saida=S / "R34_S_pre_selo_b2sd")
R_SALTO_D = sorted((S / "R34_S_pre_selo_b2sd").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
(b2sd / "canonical_contracts.json").write_bytes((b2sd / "canonical_contracts.json").read_bytes() + b"\n")      # a Bancada muda depois do recibo (o JSON segue valido)
run("R34_S_pos_selo_bancada_mudou_depois_do_pre_selo_recusa", args_pos(b2sd, R_SALTO_D, CH_392, CH_392_SHA, modo="ensaio", kernel=False), 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=b2sd,
    extra_ok=lambda j, r: "o salto que o recibo declara nao e o que a cadeia" in str(j.get("recusa")),
    nota="S: o salto carrega o sha do manifesto da Bancada de quando o recibo foi feito; se a Bancada mudou, o recibo nao serve")
# versao nao consecutiva: o recibo termina em v392 e se sela v394
NOS394 = AT34 / "nos_v394s"
NOS394.mkdir(parents=True)
for f_ in ("um_absoluto.json", "tgl_kernel_proof_manifest.json"):
    shutil.copyfile(NOS393 / f_, NOS394 / f_)
_um3 = (NOS393 / "um.py").read_bytes()
_um4 = _um3.replace(b'UM_VERSION = "v393', b'UM_VERSION = "v394', 1)
assert _um4 != _um3 and len(_um4) == len(_um3)
(NOS394 / "um.py").write_bytes(_um4)
_selo4 = json.loads((NOS393 / "um_absoluto_selo.json").read_bytes())
_selo4["um_version"] = "v394"
_selo4["sha256"]["um.py"] = sha_b(_um4)
(NOS394 / "um_absoluto_selo.json").write_bytes(json.dumps(_selo4, ensure_ascii=False, indent=1).encode("utf-8"))
run("R34_S_pos_selo_versao_nao_consecutiva_recusa", args_pos(b2sa, R_SALTO, CH_392, CH_392_SHA, nos=NOS394, versao="v394", modo="ensaio", kernel=False), 2, "SALTO_VERSAO_NAO_CONSECUTIVA", bancada=b2sa,
    nota="S: o recibo termina em v392 (a seguinte e v393) e a versao a sincronizar e v394: nenhuma versao pode ficar fora da cadeia")

# --- S: o pos_selo APLICA o salto (v391 -> v393 sintetica, com T17 pelo recibo do kernel R3_4 com o modulo de auditoria) e a re-execucao e idempotente
d_s21, j_s21 = run("R34_S_pos_selo_salto_aplica", args_pos(b2sa, R_SALTO, CH_392, CH_392_SHA, modo="aplicar", kernel=True), 0,
                   veredito_esp="REPINADA_B3__SALTO_v391_v393__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", saida=S / "R34_S_pos_selo_salto",
                   extra_ok=lambda j, r: (lambda rec, man: rec["bateria_resultado"]["falha"] == 0 and testes(j)["T17_LEAN_KERNEL"]["resultado"] == "PASSA"
                                          and "cruzado com o recibo pre-selo" in testes(j)["T17_LEAN_KERNEL"]["detalhe"] and "1 modulo(s) de auditoria" in testes(j)["T17_LEAN_KERNEL"]["detalhe"]
                                          and man["sincronizacao"]["salto"]["versoes_puladas"] == ["v392"] and man["sincronizacao"]["salto"]["de"]["versao"] == "v391"
                                          and man["sincronizacao"]["salto"]["ate"]["versao"] == "v392" and man["sincronizacao"]["salto"]["proxima_a_selar"] == "v393"
                                          and man["sincronizacao"]["salto"] == rec["salto"] == recibo_de(j)["recibo_pre_selo"]["salto"] == json.loads(R_SALTO.read_bytes())["salto"]
                                          and man["canonical"]["version"] == "v393" and man["sincronizacao"]["anterior"]["version"] == "v391"
                                          and man["sincronizacao"]["anterior"]["kernel_manifesto_sha256"] == sha(KMAN_ANT) and man["sincronizacao"]["recibo_pre_selo_sha256"] == R_SALTO_SHA
                                          and man["sincronizacao"]["kernel_manifesto_sha256"] == sha(NOS393 / "tgl_kernel_proof_manifest.json")
                                          and "## Salto (R3.4)" in (b2sa / "CONTRATO_CANONICO_B3.md").read_text(encoding="utf-8")
                                          and rec["aplicacao"]["pos_conferencia"]["ok"] is True and rec["aplicacao"]["pos_conferencia"]["canonical_version"] == "v393")(
                       recibo_de(j), json.loads((b2sa / "canonical_contracts.json").read_bytes())),
                   nota="S: o elo B(n) pos_selo aceita o recibo pre-selo de um SALTO no lugar do JA_SINCRONIZADA (cadeia v391 -> v392 conferida contra a Bancada e contra o recibo; o selo anterior e o "
                        "do FIM da cadeia; T17 cruzado com o kernel do v392); grava o manifesto B3 com sincronizacao.salto (de v391, puladas [v392], ate v392, proxima v393) e o contrato com a secao do salto")
d_s22, j_s22 = run("R34_S_pos_selo_salto_idempotente", args_pos(b2sa, R_SALTO, CH_392, CH_392_SHA, modo="aplicar", kernel=True), 0, veredito_esp="JA_SINCRONIZADA__NADA_A_GRAVAR", bancada=b2sa,
                   nota="S: repetir o B(n) do salto ja aplicado: a referencia do recibo pre-selo vem do bloco sincronizacao.salto do manifesto; nada se grava")
run("R34_S_pos_selo_salto_idempotente_sem_a_cadeia", args_pos(b2sa, R_SALTO, None, None, modo="aplicar", kernel=True), 0, veredito_esp="JA_SINCRONIZADA__NADA_A_GRAVAR", bancada=b2sa,
    nota="S: na re-execucao a cadeia e opcional (o manifesto registra o salto); se vier, tem de ser a registrada")
run("R34_S_pos_selo_salto_idempotente_com_outra_cadeia_recusa", args_pos(b2sa, R_SALTO, CH_393, CH_393_SHA, modo="aplicar", kernel=True), 2, "CADEIA_DE_SELOS_NAO_E_A_DO_SALTO_REGISTRADO", bancada=b2sa,
    nota="S: a cadeia de 3 elos nao e a que o manifesto registra")
_m_applied = json.loads((b2sa / "canonical_contracts.json").read_bytes())
_m_sem_salto = RAIZ / "b2sa_sem_salto"
copiar_sem_juncao(b2sa, _m_sem_salto)
_ms = json.loads((_m_sem_salto / "canonical_contracts.json").read_bytes())
_ms["sincronizacao"].pop("salto")
(_m_sem_salto / "canonical_contracts.json").write_bytes(json.dumps(_ms, ensure_ascii=False, indent=1).encode("utf-8"))
_rj_ms = json.loads(R_SALTO.read_bytes())
_rj_ms["bancada"]["dir"] = str(_m_sem_salto)
_p_ms = FX / "PRE_salto_em_bancada_sem_salto_registrado.json"
_p_ms.write_bytes(json.dumps(_rj_ms, ensure_ascii=False).encode("utf-8"))
run("R34_S_reexecucao_recibo_de_salto_em_manifesto_sem_salto_recusa", args_pos(_m_sem_salto, _p_ms, None, None, modo="aplicar", kernel=True), 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=_m_sem_salto,
    extra_ok=lambda j, r: "nao registra sincronizacao.salto" in str(j.get("recusa")), nota="S: o recibo declara salto e o manifesto (ja sincronizado) nao o registra")
apagar_arvore(_m_sem_salto)

# --- S: o gerador da cadeia contra a pasta REAL cadeia_de_selo (v392 -> v393) e a cadeia real contra a producao e o Nos reais (so lidos)
_real_out = FX / "CADEIA_REAL_regerada.json"
_r_real = subprocess.run([PY, "-I", "-B", "-X", "utf8", str(GERAR_CADEIA), "--cadeia", str(WORK / "cadeia_de_selo"), "--de", "v392", "--ate", "v393", "--saida", str(_real_out)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, stdin=subprocess.DEVNULL)
_a_real, _b_real = json.loads(_real_out.read_bytes()), json.loads(CADEIA_REAL.read_bytes())
for _x in (_a_real, _b_real):
    _x.pop("gerada_em_utc")
checar("R34_S_gerador_regera_a_cadeia_real_v392_v393", lambda: _r_real.returncode == 0 and _a_real == _b_real,
       nota="S: o gerador, rodado de novo contra a pasta REAL work/cadeia_de_selo (base_v392, base_v393 e o registro APLICADO_AO_CANONICO da v393, com os backups .bak_ do Nos), "
            "reproduz a cadeia entregue (R3_4/CADEIA_DE_SELOS_v394.json) exceto o carimbo de hora", cadeia_real=_pinar(CADEIA_REAL))
_cad_real = MOD.carregar_cadeia_de_selos(CADEIA_REAL, sha(CADEIA_REAL))
_ant_prod = MOD.estado_anterior(PROD, MOD.carregar_canonical(PROD)[0])
_ni_real = MOD.ler_nos(NOS_STAND, VR)


def _cadeia_real_confere():
    MOD.conferir_cadeia_com_a_bancada(_cad_real, _ant_prod)
    MOD.conferir_cadeia_com_o_fim(_cad_real, VR, _ni_real["um_py"]["sha256"], _ni_real["selo"]["sha256"], _ni_real["kernel"]["sha256"], "o Nos real lido agora")
    return _cad_real["versoes"] == ["v392", "v393"] and _ant_prod["version"] == "v392" and _cad_real["ligacoes"][0]["de"] == "v392"


checar("R34_S_cadeia_real_confere_com_a_producao_e_o_nos_reais", _cadeia_real_confere,
       nota="S: a cadeia REAL: o primeiro elo e o que a Bancada de PRODUCAO pina (v392, B3) e o ultimo e o Nos REAL de hoje (v393); 2 elos, 1 ligacao (registro do instalador da v393 com os backups "
            "de bytes); producao e Nos so lidos", versoes=_cad_real["versoes"], ligacoes=_cad_real["ligacoes"])
checar("R34_S_o_selo_nao_pina_o_selo_anterior_medido", lambda: all(
    ("50bd1be10f9293e7" not in Path(NOS_STAND / f_).read_text(encoding="utf-8", errors="replace") and "b590c0aa80055e2a" not in Path(NOS_STAND / f_).read_text(encoding="utf-8", errors="replace"))
    for f_ in ("um_absoluto_selo.json", "tgl_kernel_proof_manifest.json")),
       nota="S (medida que fundamenta o desenho): o selo da v393 e o manifesto do kernel dele NAO contem o sha16 do selo nem do um.py da v392 -- 'cada selo pina o anterior' nao e literal; "
            "a ligacao entre versoes vem do registro do instalador (APLICADO_AO_CANONICO) e dos backups de bytes, que a cadeia pina")

# --- S: o gerador recusa o que nao pode gerar (arvores minimas, arquivos pequenos: o gerador so le caminhos e sha)
MIN = AT34 / "min"


def arvore_minima(nome, registros=None, sem_base=False, sem_backup=False, dup=False):
    raiz_ = MIN / nome
    for v_ in ("v391", "v392"):
        proxima_ = "v%d" % (int(v_[1:]) + 1)
        if sem_base and v_ == "v392":
            continue
        d_ = raiz_ / proxima_ / ("base_" + v_)
        d_.mkdir(parents=True)
        for n_, c_ in (("um.py", "um " + v_), ("um_absoluto_selo.json", "selo " + v_), ("tgl_kernel_proof_manifest.json", "km " + v_)):
            (d_ / n_).write_text(c_, encoding="utf-8")
    bak_ = raiz_ / "_nos"
    bak_.mkdir(parents=True)
    (bak_ / "um.py.bak_1").write_text("um v391", encoding="utf-8")
    (bak_ / "selo.bak_1").write_text("selo v391", encoding="utf-8")
    um391, um392 = b"um v391", b"um v392"
    def reg_(ts, novo_sha16):
        return dict(ts=ts, backups={"um.py": dict(backup=str(bak_ / "um.py.bak_1"), bytes=len(um391), sha16=sha_b(um391)[:16]),
                                    "um_absoluto_selo.json": dict(backup=str(bak_ / "selo.bak_1"), bytes=9, sha16=sha_b(b"selo v391")[:16])},
                    um_py_novo=dict(bytes=len(um392), sha16=novo_sha16))
    regs_ = registros if registros is not None else ([reg_("1", sha_b(um392)[:16])] + ([reg_("2", sha_b(um392)[:16])] if dup else []))
    (raiz_ / "v392").mkdir(parents=True, exist_ok=True)
    for i_, r_ in enumerate(regs_):
        (raiz_ / "v392" / ("APLICADO_AO_CANONICO_%d.json" % i_)).write_text(json.dumps(r_), encoding="utf-8")
    if sem_backup:
        (bak_ / "um.py.bak_1").unlink()
    return raiz_


def gerador_rc(raiz_):
    r_ = subprocess.run([PY, "-I", "-B", "-X", "utf8", str(GERAR_CADEIA), "--cadeia", str(raiz_), "--de", "v391", "--ate", "v392", "--saida", str(raiz_ / "saida.json")],
                        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, stdin=subprocess.DEVNULL)
    return r_.returncode, (r_.stdout + r_.stderr)


MIN.mkdir(parents=True)
rc_ok, out_ok = gerador_rc(arvore_minima("ok"))
checar("R34_S_gerador_arvore_minima_boa_gera", lambda: rc_ok == 0 and json.loads((MIN / "ok" / "saida.json").read_bytes())["contrato"] == "CADEIA_DE_SELOS_R3_4",
       nota="contraprova do gerador: uma arvore minima com tudo no lugar gera a cadeia", saida_do_gerador=out_ok[:200])
for nome_, kw_, esp_ in (("sem_registro_do_instalador", dict(registros=[]), "REGISTRO_DO_INSTALADOR: 0 registro"), ("dois_registros_que_conferem", dict(dup=True), "REGISTRO_DO_INSTALADOR: 2 registro"),
                         ("so_a_tentativa_revertida", dict(registros=[dict(ts="0", backups={"um.py": dict(backup="x", bytes=1, sha16="0" * 16)}, um_py_novo=dict(bytes=1, sha16="0" * 16))]),
                          "REGISTRO_DO_INSTALADOR: 0 registro"), ("sem_a_pasta_base", dict(sem_base=True), "BASE_AUSENTE"), ("backup_de_bytes_ausente", dict(sem_backup=True), "ARQUIVO_AUSENTE")):
    rc_, out_ = gerador_rc(arvore_minima("g_" + nome_, **kw_))
    checar("R34_S_gerador_recusa_%s" % nome_, (lambda rc_=rc_, out_=out_, esp_=esp_: rc_ != 0 and esp_ in out_), nota="o gerador recusa (rc != 0, %s) e nao escreve a cadeia" % esp_, saida_do_gerador=out_[:240])
    assert not (MIN / ("g_" + nome_) / "saida.json").exists()
checar("R34_S_versao_seguinte_e_numero", lambda: MOD.versao_seguinte("v393") == "v394" and MOD.versao_seguinte("v099") == "v100" and MOD.versao_numero("v1000") == 1000,
       nota="unitario: versao_seguinte mantem a largura (v099 -> v100)")
unit("R34_S_versao_numero_recusa_mal_formada", lambda: MOD.versao_numero("393"), "VERSAO_INVALIDA")
unit("R34_S_versao_seguinte_recusa_mal_formada", lambda: MOD.versao_seguinte("v39"), "VERSAO_INVALIDA")
checar("R34_S_o_atrasado_exige_a_cadeia_no_codigo", lambda: 'raise Recusa("BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS' in _inspect.getsource(MOD.main) and
       _inspect.getsource(MOD.main).index("conferir_cadeia_com_a_bancada(cadeia, anterior)") < _inspect.getsource(MOD.main).index("regenerar(bancada"),
       nota="unitario: no codigo do main, a cadeia e conferida (contra a Bancada e contra o Nos) ANTES do regenerar e do staging")

# --- S: o salto na PRODUCAO-DECOY (em processo; PRODUCAO, EVENTOS_QUADRO e a sonda do servico trocados): a composicao exata do B(n) da v394 -- producao + aplicar + salto + evento da cadeia + servico
PD2, PD2_PRIST, NOSD = RAIZ / "pd_salto", RAIZ / "pd_salto_pristino", RAIZ / "nosd_salto"
NOSD.mkdir()


def nosd_com(origem):
    """o 'Nos' do decoy do salto (o caminho que o manifesto pina) passa a ter os bytes de `origem` (o 'selo' do sandbox, feito a mao e so dentro do sandbox)."""
    for f_ in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json"):
        shutil.copyfile(origem / f_, NOSD / f_)


nosd_com(NOS392)
copiar_sem_juncao(B2, PD2)
_m_pd2 = json.loads((PD2 / "canonical_contracts.json").read_bytes())
_m_pd2["canonical"]["script"]["path"] = str(NOSD / "um.py")
_m_pd2["canonical"]["seal"]["path"] = str(NOSD / "um_absoluto_selo.json")
(PD2 / "canonical_contracts.json").write_bytes(json.dumps(_m_pd2, ensure_ascii=False, indent=1).encode("utf-8"))
copiar_sem_juncao(PD2, PD2_PRIST)
MAN_PD2 = sha(PD2_PRIST / "canonical_contracts.json")


def pd2_reset():
    apagar_arvore(PD2)
    copiar_sem_juncao(PD2_PRIST, PD2)


d_dps, j_dps = inproc("R34_S_decoy_pre_selo_salto_na_producao", ["--bancada", PD2, "--producao", "--nos", NOSD, "--versao", "v392", "--fase", "pre_selo", "--modo", "ensaio", "--bateria", bt_min_pre,
                                                                 "--bateria-sha256", bt_min_pre_sha, "--cadeia-de-selos", CH_392, "--cadeia-de-selos-sha256", CH_392_SHA, "--saida", S / "R34_S_decoy_pre_selo"], 0,
                      veredito_esp="REPINADA_B3__SALTO_v391_v392__ENSAIO", patches=dict(PRODUCAO=PD2, EVENTOS_QUADRO=EV_SB, servico_responde=sonda_seq([False])), bancada=PD2,
                      extra_ok=lambda j, a, d: a == d and sha(PD2 / "canonical_contracts.json") == MAN_PD2 and recibo_de(j)["producao"] is True and recibo_de(j)["salto"]["versoes_puladas"] == ["v392"]
                      and [s["no_ar"] for s in recibo_de(j)["sondagens_do_servico"]] == [],
                      nota="S: o ensaio pre_selo do salto contra a PRODUCAO-DECOY (--producao, PRODUCAO trocada para a copia): REPINADA_B3__SALTO_v391_v392, nada gravado; e o recibo que o B(n) pos_selo do decoy consome")
R_PD2 = sorted((S / "R34_S_decoy_pre_selo").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
nosd_com(NOS393)               # o 'selo' do decoy do salto: o caminho pinado passa a ter a v393 sintetica (a Bancada fica pinada na v391: PIN_CHANGED)


def pd2_args(saida, recibo, cadeia=CH_392, cadeia_sha=CH_392_SHA, evento="decoy_salto", extra=()):
    a_ = ["--bancada", PD2, "--producao", "--nos", NOSD, "--versao", "v393", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--modo", "aplicar", "--fase", "pos_selo", "--saida", saida,
          "--evento", ELOS[evento]["seq"], "--evento-hash", ELOS[evento]["hash16"], "--recibo-pre-selo", recibo, "--recibo-pre-selo-sha256", sha(recibo), "--selo-anterior", SELO_392,
          "--kernel-manifesto-anterior", KMAN_392, "--kernel-recibo", K393, "--kernel-recibo-sha256", K393_SHA, "--criterios", CRIT393, "--criterios-sha256", CRIT393_SHA]
    if cadeia:
        a_ += ["--cadeia-de-selos", cadeia, "--cadeia-de-selos-sha256", cadeia_sha]
    return a_ + list(extra)


def pd2(nome, rc_esp, recusa_esp=None, veredito_esp=None, sondas=(False,), extra_ok=None, nota="", **kw):
    pd2_reset()
    return inproc(nome, pd2_args(S / nome, **kw), rc_esp, recusa_esp, veredito_esp, patches=dict(PRODUCAO=PD2, EVENTOS_QUADRO=EV_SB, servico_responde=sonda_seq(list(sondas))), bancada=PD2,
                  extra_ok=extra_ok, nota=nota)


def pd2_intocado(j, a, d):
    return a == d and sha(PD2 / "canonical_contracts.json") == MAN_PD2


pd2("R34_S_decoy_salto_servico_no_ar_no_inicio", 2, "SERVICO_NO_AR", sondas=(True,), extra_ok=pd2_intocado, recibo=R_PD2, nota="S: o servico no ar no inicio do B(n) do salto: recusa, nada gravado")
pd2("R34_S_decoy_salto_servico_volta_durante_a_bateria", 2, "SERVICO_VOLTOU_ANTES_DE_GRAVAR", sondas=(False, True), extra_ok=pd2_intocado, recibo=R_PD2,
    nota="S: o servico sobe durante a bateria do salto: a sonda imediatamente antes de gravar recusa (nada gravado)")
pd2("R34_S_decoy_salto_sem_a_cadeia_recusa", 2, "RECIBO_PRE_SELO_SALTO_SEM_CADEIA", extra_ok=pd2_intocado, recibo=R_PD2, cadeia=None, cadeia_sha=None,
    nota="S: na producao-decoy, o recibo pre-selo de um salto sem a cadeia nao se confere")
pd2("R34_S_decoy_salto_evento_de_outra_versao_recusa", 2, "EVENTO_NAO_NOMEIA_A_VERSAO", extra_ok=pd2_intocado, recibo=R_PD2, evento="decoy",
    nota="S: o evento c1 do decoy NORMAL (versao v392) nao autoriza o salto a v393")
pd2("R34_S_decoy_salto_cadeia_adulterada_recusa", 2, "CADEIA_DE_SELOS_COPIA_DIVERGE", extra_ok=pd2_intocado, recibo=R_PD2, cadeia=FX / "CADEIA_deriv_copia_do_um_py_com_um_byte_mudado.json",
    cadeia_sha=sha(FX / "CADEIA_deriv_copia_do_um_py_com_um_byte_mudado.json"), nota="S: a cadeia com uma copia adulterada recusa tambem na producao-decoy")
d_dpa, j_dpa = pd2("R34_S_decoy_salto_aplica_na_producao_decoy", 0, veredito_esp="REPINADA_B3__SALTO_v391_v393__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", recibo=R_PD2,
                   extra_ok=lambda j, a, d: (lambda rec, man: rec["producao"] is True and rec["evento_c1"]["verificado"] is True and rec["evento_c1"]["evento"] == ELOS["decoy_salto"]["seq"]
                                             and testes(j)["T17_LEAN_KERNEL"]["resultado"] == "PASSA" and [s["no_ar"] for s in rec["sondagens_do_servico"]] == [False] * 6
                                             and man["sincronizacao"]["salto"]["versoes_puladas"] == ["v392"] and man["sincronizacao"]["salto"]["de"]["versao"] == "v391"
                                             and man["canonical"]["version"] == "v393" and sha(PD2 / "canonical_contracts.json") == rec["manifesto_novo"]["sha256"]
                                             and rec["manifesto_novo"]["recibo_pre_selo_sha256_encadeado"] == sha(R_PD2) and Path(rec["aplicacao"]["copia_do_recibo"]).exists()
                                             and sha(rec["aplicacao"]["backup"]) == MAN_PD2 and (PD2 / "CONTRATO_CANONICO_B3.md").is_file())(
                       recibo_de(j), json.loads((PD2 / "canonical_contracts.json").read_bytes())),
                   nota="S (a composicao do B(n) da v394): producao-decoy + aplicar + salto + recibo pre-selo do salto + cadeia + evento c1 encadeado (hash conferido) + servico parado nas 6 sondagens + T17 pelo "
                        "recibo do kernel R3_4 com o modulo de auditoria: aplicada; o manifesto novo registra o salto; o backup e o manifesto anterior")
pd2_reset()
nosd_com(NOS392)

# ================================================================ R3.4 (P): a bateria por versao
# --- P: o que o gerador entregou para o Nos real de hoje (v393)
_bat_real = json.loads(BAT_REAL.read_bytes())
_t12 = next(t for t in _bat_real["testes"] if t["id"] == "T12_T13_T14_ATRATOR")
checar("R34_P_bateria_gerada_para_o_nos_real_pina_a_versao_instalada", lambda: _bat_real["pinos_da_versao"]["versao"] == VR and _bat_real["pinos_da_versao"]["um_py_sha256"] == SBM["nos_real"]["um_py"]["sha256"]
       and _bat_real["pinos_da_versao"]["um_py_bytes"] == SBM["nos_real"]["um_py"]["bytes"] and _bat_real["pinos_da_versao"]["selo_sha256"] == SBM["nos_real"]["selo"]["sha256"]
       and _bat_real["pinos_da_versao"]["fonte_dos_pinos"]["pinos_bn"]["candidato_sha256"] == SBM["nos_real"]["um_py"]["sha256"]
       and _bat_real["pinos_da_versao"]["fonte_dos_pinos"]["pinos_bn"]["sha256"] == sha(PINOS_BN_REAL) and _bat_real["contrato_bateria"] == "BATERIA_R3_4",
       nota="P: pinos_da_versao da bateria gerada == o Nos real lido (um.py, bytes, selo) e == o candidato que os PINOS_BN da cadeia (v393) pinam; fonte dos pinos registrada",
       pinos=_bat_real["pinos_da_versao"])
checar("R34_P_so_o_T12_pina_o_um_py_e_aponta_o_driver_R3_4", lambda: [t["id"] for t in _bat_real["testes"] if t.get("pina_o_um_py")] == ["T12_T13_T14_ATRATOR"]
       and Path(_t12["fontes"][0]["path"]) == DRV_BAT.resolve() and Path(_t12["fontes"][-1]["path"]).name == "PINO_UM_PY_real_%s.json" % VR and "{um_py_sha256}" in _t12["comando"]
       and "{nos}" in _t12["comando"] and not any(Path(f_["path"]).name == "t12_t14_atrator.py" for f_ in _t12["fontes"]),
       nota="P: o driver R2 (que pinava o um.py v391 no pre-registro) saiu do T12; entrou o driver R3.4 e o pino da cadeia como fonte pinada; o comando recebe o um.py MEDIDO pelo esboco")
checar("R34_P_testes_sha256_confere_em_todos_os_testes", lambda: all(_bat_real["testes_sha256"][t["id"]] == MOD.sha_teste(t) for t in _bat_real["testes"]) and len(_bat_real["testes_sha256"]) == len(_bat_real["testes"]),
       nota="P: o pino por teste da bateria gerada confere (o esboco o exige na carga)")
DET = FX / "det"
DET.mkdir(exist_ok=True)
_r_det = subprocess.run([PY, "-I", "-B", "-X", "utf8", str(GEN_BAT), "--base", str(BAT), "--base-sha256", sha(BAT), "--versao", VR, "--nos", str(NOS_STAND), "--driver", str(DRV_BAT), "--pinos-bn", str(PINOS_BN_REAL),
                         "--pino-saida", str(DET / PINO_REAL.name), "--saida", str(DET / BAT_REAL.name)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, stdin=subprocess.DEVNULL)


def _sem_o_caminho_do_pino(p_):
    j_ = json.loads(Path(p_).read_bytes())
    t_ = next(t for t in j_["testes"] if t["id"] == "T12_T13_T14_ATRATOR")
    t_["fontes"][-1] = None                               # o unico campo que depende da pasta de saida: o caminho (e o sha do teste, que o contem)
    j_["testes_sha256"].pop("T12_T13_T14_ATRATOR")
    j_["gerado_por_r3_4"]["pino"] = None
    return j_


checar("R34_P_gerador_e_determinista_mesma_entrada_mesma_bateria", lambda: _r_det.returncode == 0 and PINO_REAL.read_bytes() == (DET / PINO_REAL.name).read_bytes()
       and _sem_o_caminho_do_pino(BAT_REAL) == _sem_o_caminho_do_pino(DET / BAT_REAL.name) and sha(PINO_REAL) == sha(DET / PINO_REAL.name),
       nota="P: regenerar a bateria com a mesma entrada (em outra pasta de saida) da o MESMO pino (bytes iguais) e a mesma bateria, a menos do caminho do arquivo do pino: a bateria e "
            "'regenerada por script em cada versao e pinada'")
unit("R34_P_pinos_conferem_com_o_nos_lido", lambda: MOD.conferir_pinos_da_versao(_bat_real, _ni_real, VR)["conferidos_contra_o_nos_lido"], None)


def _pv(mut):
    b_ = json.loads(json.dumps(_bat_real))
    mut(b_)
    return b_


for nome_, mut_, esp_ in (("versao_velha", lambda b: b["pinos_da_versao"].update(versao="v391"), "BATERIA_COM_PINO_VELHO"),
                          ("um_py_sha256_velho", lambda b: b["pinos_da_versao"].update(um_py_sha256=SBM["nos"]["um_py"]["sha256"]), "BATERIA_COM_PINO_VELHO"),
                          ("um_py_bytes_diferente", lambda b: b["pinos_da_versao"].update(um_py_bytes=SBM["nos"]["um_py"]["bytes"]), "BATERIA_COM_PINO_VELHO"),
                          ("selo_sha256_velho", lambda b: b["pinos_da_versao"].update(selo_sha256=SBM["nos"]["selo"]["sha256"]), "BATERIA_COM_PINO_VELHO"),
                          ("sem_o_bloco_com_teste_marcado", lambda b: b.pop("pinos_da_versao"), "BATERIA_SEM_PINOS_DA_VERSAO"),
                          ("bloco_sem_um_campo", lambda b: b["pinos_da_versao"].pop("selo_sha256"), "BATERIA_PINOS_DA_VERSAO_INVALIDOS"),
                          ("bloco_com_campo_a_mais", lambda b: b["pinos_da_versao"].update(autorizado_por="qualquer"), "BATERIA_PINOS_DA_VERSAO_INVALIDOS"),
                          ("sha_mal_formado", lambda b: b["pinos_da_versao"].update(um_py_sha256="abc"), "BATERIA_PINOS_DA_VERSAO_INVALIDOS"),
                          ("bytes_em_texto", lambda b: b["pinos_da_versao"].update(um_py_bytes="35606254"), "BATERIA_PINOS_DA_VERSAO_INVALIDOS"),
                          ("versao_mal_formada", lambda b: b["pinos_da_versao"].update(versao="393"), "BATERIA_PINOS_DA_VERSAO_INVALIDOS"),
                          ("bloco_nao_objeto", lambda b: b.update(pinos_da_versao=[1]), "BATERIA_PINOS_DA_VERSAO_INVALIDOS")):
    unit("R34_P_unit_%s" % nome_, (lambda mut_=mut_: MOD.conferir_pinos_da_versao(_pv(mut_), _ni_real, VR)), esp_,
         nota="P (unitario): a bateria gerada com UMA coisa mudada nos pinos_da_versao e recusada: %s" % esp_)
checar("R34_P_unit_bateria_sem_teste_marcado_e_sem_bloco_segue_aceita", lambda: MOD.conferir_pinos_da_versao(json.loads(BAT.read_bytes()), _ni_real, VR) == dict(declarados=False, testes_que_pinam_o_um_py=[]),
       nota="P: a bateria R2 (sem teste marcado, sem bloco) segue aceita como antes (compatibilidade); o pino velho dela aparece no teste (ver R34_P_bateria_R2_T12_contra_o_nos_atual_falha)")

# --- P: pelo caminho inteiro (subprocesso)
_bat_v391_real_ns = BAT_V391        # a bateria gerada para a copia v391 do sandbox, usada contra o Nos real v393
run("R34_P_pino_velho_bateria_v391_contra_o_nos_v393_recusa", ["--bancada", B1, "--versao", VR, "--bateria", BAT_V391, "--bateria-sha256", BAT_V391_SHA, "--modo", "ensaio", "--fase", "pre_selo"], 2,
    "BATERIA_COM_PINO_VELHO", bancada=B1, nota="P (o conserto pedido): a bateria gerada para a v391 contra o Nos que tem v393: recusa ANTES de qualquer teste (era: T12 FALHA dentro da bateria)")
run("R34_P_bateria_gerada_para_outra_versao_recusa_mesmo_com_o_sha_certo", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT_V391, "--bateria-sha256", BAT_V391_SHA, "--sandbox",
                                                                           "--modo", "ensaio", "--fase", "pos_selo"], 2, "BATERIA_COM_PINO_VELHO", bancada=B2,
    nota="P: o sha da bateria esta certo (pinado), mas ela foi gerada para v391 e o Nos tem v392")
bt_marc, bt_marc_sha = mini_bateria("P_marcado_sem_bloco", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["testes"][0].update(pina_o_um_py=True))
run("R34_P_teste_marcado_sem_pinos_da_versao_recusa", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_marc, "--bateria-sha256", bt_marc_sha, "--sandbox", "--modo", "ensaio",
                                                       "--fase", "pos_selo"], 2, "BATERIA_SEM_PINOS_DA_VERSAO", bancada=B2, nota="P: pina_o_um_py=true e nenhum pinos_da_versao na bateria")
bt_marc2, bt_marc2_sha = mini_bateria("P_marcador_texto", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["testes"][0].update(pina_o_um_py="sim"))
run("R34_P_marcador_pina_o_um_py_nao_booleano_recusa", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_marc2, "--bateria-sha256", bt_marc2_sha, "--sandbox", "--modo", "ensaio",
                                                        "--fase", "pos_selo"], 2, "BATERIA_TESTE_PINA_O_UM_PY_NAO_BOOLEANO", bancada=B2)
run("R34_P_bateria_R2_sem_bloco_segue_aceita_e_o_recibo_diz", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "ensaio",
                                                               "--fase", "pos_selo", "--sem-bateria"], 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2,
    extra_ok=lambda j, r: recibo_de(j)["bateria"]["pinos_da_versao"]["declarados"] is False, nota="P: compatibilidade: a bateria R2 (sem teste marcado) e aceita; o recibo diz declarados=false")
# o problema medido: o T12 da R2 contra o Nos real de hoje (o pre-registro congelado pina o um.py v391 no caminho real)
_t12_r2 = next(t for t in json.loads(BAT.read_bytes())["testes"] if t["id"] == "T12_T13_T14_ATRATOR")
bt_t12_r2, bt_t12_r2_sha = mini_bateria("P_T12_da_R2", ids=("T01_IDENTIDADE",), extra=[_t12_r2])
d_p9, j_p9 = run("R34_P_bateria_R2_T12_contra_o_nos_atual_falha", ["--bancada", B1, "--versao", VR, "--bateria", bt_t12_r2, "--bateria-sha256", bt_t12_r2_sha, "--modo", "ensaio", "--fase", "pre_selo"], 3,
                 veredito_esp="JA_SINCRONIZADA__BATERIA_FALHOU", bancada=B1,
                 extra_ok=lambda j, r: testes(j)["T12_T13_T14_ATRATOR"]["resultado"] == "FALHA" and testes(j)["T01_IDENTIDADE"]["resultado"] == "PASSA"
                 and "Source pin changed" in "".join(p_.read_text(encoding="utf-8", errors="replace") for p_ in (S / "R34_P_bateria_R2_T12_contra_o_nos_atual_falha").rglob("*.vinculo.log")),
                 nota="P (o defeito que motivou o conserto, reproduzido): o T12 da bateria R2 contra o Nos real v393 FALHA -- o pre-registro congelado pina o um.py v391 (Source pin changed)")
# o replay repinado, dentro do run 1a (Nos real v393) e do run 1b (copia v391)
_t12_1a = json.loads(Path(S / "1a" / "recibos" / "T12_T13_T14_ATRATOR.json").read_bytes())
_t12_1b = json.loads(Path(S / "1b" / "recibos" / "T12_T13_T14_ATRATOR.json").read_bytes())
checar("R34_P_run_1a_T12_repinado_so_o_pino_do_um_py_e_o_resto_identico_ao_arquivado", lambda: _t12_1a["veredito"] == "PASSA" and _t12_1a["adendo_de_pino"]["caminhos_que_diferem"] == ["$.source_pins[9].bytes", "$.source_pins[9].path", "$.source_pins[9].sha256"]
       and _t12_1a["adendo_de_pino"]["entrada_do_um_py"]["depois"]["sha256"] == SBM["nos_real"]["um_py"]["sha256"] and _t12_1a["adendo_de_pino"]["entrada_do_um_py"]["antes"]["sha256"] == SBM["nos"]["um_py"]["sha256"]
       and all(r_["passa"] and r_["n_mismatch"] == 0 for r_ in _t12_1a["runs"].values())
       and sorted(_t12_1a["runs"]["T12_optical_r3"]["campos_trocados_no_arquivado"]) == ["$.alpha_assignment_line", "$.preregister_sha256", "$.um_sha256"]
       and sorted(_t12_1a["runs"]["T13_adendo1_r1"]["campos_trocados_no_arquivado"]) == ["$.alpha_source.line", "$.alpha_source.sha256", "$.sources_after[16].sha256", "$.sources_before[16].sha256"],
       nota="P: no run 1a (Nos REAL v393) o pre-registro do atrator difere do congelado SO em bytes e sha256 da entrada do um.py; os 3 runners passam com 0 divergencias; so 3 (T12) e 4 (T13) campos do "
            "resultado arquivado foram trocados por valores independentes (sha do pre-registro-copia, sha do um.py, linha de alpha)", adendo=_t12_1a["adendo_de_pino"]["entrada_do_um_py"])
checar("R34_P_run_1b_T12_repinado_na_copia_v391_so_o_caminho", lambda: _t12_1b["veredito"] == "PASSA" and _t12_1b["adendo_de_pino"]["caminhos_que_diferem"] == ["$.source_pins[9].path"]
       and Path(_t12_1b["adendo_de_pino"]["entrada_do_um_py"]["depois"]["path"]) == NOS / "um.py" and all(r_["passa"] and r_["n_mismatch"] == 0 for r_ in _t12_1b["runs"].values()),
       nota="P: no run 1b (copia v391 do Nos no sandbox) o pino do um.py (mesmo sha, mesmos bytes que o congelado) so muda de CAMINHO: aponta a copia")
# o driver sozinho (subprocesso, -I): pino velho; pre-registro com dois pinos do um.py; runner alterado; resultado arquivado adulterado
SRC_ATR = TUNEL_ATR = Path("C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.ATRATOR")
ATR_ARQ = ("PREREGISTRO_R1.json", "numerical/run_optical_r3.py", "numerical/RUN_MANIFEST_R3.json", "numerical/RESULTADOS_NUMERICOS_R3.json", "ADENDO1/PREREGISTRO_ADENDO1_R1.json",
           "ADENDO1/numerical/run_adendo1_r1.py", "ADENDO1/numerical/RUN_MANIFEST_R1.json", "ADENDO1/numerical/RESULTADOS_ADENDO1_R1.json", "review/verify_affine_control_r1.py",
           "review/ADENDO_CONTROLE_AFIM_R1.json")
DRV_N = {"n": 0}


def src_atrator(nome, mut=None):
    d_ = FX / "atrator_src" / nome
    for rel_ in ATR_ARQ:
        (d_ / rel_).parent.mkdir(parents=True, exist_ok=True)
        (d_ / rel_).write_bytes((TUNEL_ATR / rel_).read_bytes())
    if mut:
        mut(d_)
    return d_


def pino_arquivo(nome, versao, sha_, bytes_):
    p_ = FX / ("PINO_UM_PY_%s.json" % nome)
    p_.write_bytes(json.dumps(dict(contrato="PINO_UM_PY_R3_4", versao=versao, um_py=dict(sha256=sha_, bytes=bytes_), selo_sha256="0" * 64, fonte_dos_pinos=dict(origem="controle"))).encode("utf-8"))
    return p_


def driver(nome, src, pino, nos_dir=NOS_STAND, sha_=None, bytes_=None):
    DRV_N["n"] += 1
    dst, out_ = FX / "atrator_dst" / ("%s_%d" % (nome, DRV_N["n"])), FX / "atrator_dst" / ("%s_%d.json" % (nome, DRV_N["n"]))
    dst.parent.mkdir(parents=True, exist_ok=True)
    r_ = subprocess.run([PY, "-I", "-B", "-X", "utf8", str(DRV_BAT), str(src), str(dst), str(out_), str(pino), str(nos_dir), sha_ or SBM["nos_real"]["um_py"]["sha256"],
                         str(bytes_ or SBM["nos_real"]["um_py"]["bytes"])], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900, stdin=subprocess.DEVNULL)
    res_ = json.loads(out_.read_bytes()) if out_.exists() else None
    return r_.returncode, res_, dst


_pino_ok = pino_arquivo("ok", VR, SBM["nos_real"]["um_py"]["sha256"], SBM["nos_real"]["um_py"]["bytes"])
rc_d, res_d, dst_d = driver("ok", src_atrator("ok"), _pino_ok)
checar("R34_P_driver_sozinho_contraprova_passa_com_o_pino_certo", lambda: rc_d == 0 and res_d["veredito"] == "PASSA" and res_d["adendo_de_pino"]["caminhos_que_diferem"] == ["$.source_pins[9].bytes", "$.source_pins[9].path", "$.source_pins[9].sha256"],
       nota="P: o driver R3.4 sozinho (contra o Nos real) com o pino da cadeia certo: PASSA")
_pino_velho = pino_arquivo("velho", "v391", SBM["nos"]["um_py"]["sha256"], SBM["nos"]["um_py"]["bytes"])
rc_d, res_d, dst_d = driver("pino_velho", src_atrator("pv"), _pino_velho)
checar("R34_P_driver_pino_velho_na_fonte_recusa_sem_rodar_runner", lambda: rc_d == 1 and res_d["veredito"] == "FALHA" and res_d["motivo"].startswith("PINO_VELHO") and not (dst_d / "numerical").exists()
       and not (dst_d / "PREREGISTRO_R1.json").exists(), nota="P (o conserto pedido, no teste): o pino da cadeia diz v391 e o esboco mediu v393: o driver FALHA com PINO_VELHO antes de copiar ou rodar qualquer runner")
rc_d, res_d, dst_d = driver("sha_medido_errado", src_atrator("sme"), _pino_ok, sha_="9" * 64)
checar("R34_P_driver_marcador_diverge_do_pino_recusa", lambda: rc_d == 1 and res_d["motivo"].startswith("PINO_VELHO") and not (dst_d / "numerical").exists(),
       nota="P: o {um_py_sha256} que o esboco mediu nao e o do pino da cadeia: PINO_VELHO")
rc_d, res_d, dst_d = driver("um_py_mudou", src_atrator("umm"), pino_arquivo("falso", VR, "9" * 64, 1), sha_="9" * 64, bytes_=1)
checar("R34_P_driver_um_py_do_disco_diferente_do_medido_recusa", lambda: rc_d == 1 and res_d["motivo"].startswith("UM_PY_MUDOU_DEPOIS_DA_MEDIDA") and not (dst_d / "numerical").exists(),
       nota="P: o pino e o marcador concordam, mas o um.py em disco nao e esse: o driver confere o arquivo de verdade")


def _dois_pinos_do_um_py(d_):
    p_ = d_ / "PREREGISTRO_R1.json"
    j_ = json.loads(p_.read_bytes())
    j_["source_pins"].append(dict(next(x for x in j_["source_pins"] if Path(x["path"]).name == "um.py")))
    p_.write_bytes(json.dumps(j_, indent=2).encode("utf-8"))


rc_d, res_d, dst_d = driver("dois_pinos", src_atrator("dp", _dois_pinos_do_um_py), _pino_ok)
checar("R34_P_driver_preregistro_com_dois_pinos_do_um_py_recusa", lambda: rc_d == 1 and res_d["motivo"].startswith("PREREGISTRO_SEM_PINO_UNICO_DO_UM_PY") and not (dst_d / "numerical").exists(),
       nota="P: o repino so e feito num pre-registro com UM pino do um.py")


def _runner_alterado(d_):
    p_ = d_ / "numerical" / "run_optical_r3.py"
    p_.write_bytes(p_.read_bytes() + b"\n# alterado\n")


rc_d, res_d, dst_d = driver("runner_alterado", src_atrator("ra", _runner_alterado), _pino_ok)
checar("R34_P_driver_runner_congelado_alterado_falha", lambda: rc_d == 1 and res_d["veredito"] == "FALHA" and res_d["runs"]["T12_optical_r3"]["passa"] is False and res_d["runs"]["T12_optical_r3"]["exit"] != 0,
       nota="P: o runner congelado alterado (um comentario a mais) e recusado pelo proprio RUN_MANIFEST (script_sha256): o repino do pre-registro nao enfraquece a integridade do runner")


def _arquivado_adulterado(d_):
    p_ = d_ / "numerical" / "RESULTADOS_NUMERICOS_R3.json"
    j_ = json.loads(p_.read_bytes())
    j_["lambda"] = j_["lambda"] * 1.000001
    p_.write_bytes(json.dumps(j_, indent=2).encode("utf-8"))


rc_d, res_d, dst_d = driver("arquivado_adulterado", src_atrator("aa", _arquivado_adulterado), _pino_ok)
checar("R34_P_driver_resultado_arquivado_adulterado_falha", lambda: rc_d == 1 and res_d["runs"]["T12_optical_r3"]["passa"] is False and res_d["runs"]["T12_optical_r3"]["n_mismatch"] >= 1
       and res_d["runs"]["T13_adendo1_r1"]["passa"] is True, nota="P: a comparacao com o arquivado e real (nao vacua): um numero do arquivado mudado de 1e-6 relativo reprova o T12")


def _arquivado_com_sha_do_um_py_errado(d_):
    p_ = d_ / "numerical" / "RESULTADOS_NUMERICOS_R3.json"
    j_ = json.loads(p_.read_bytes())
    j_["alpha_assignment_line"] = 1
    p_.write_bytes(json.dumps(j_, indent=2).encode("utf-8"))


rc_d, res_d, dst_d = driver("linha_de_alpha_errada", src_atrator("la", _arquivado_com_sha_do_um_py_errado), _pino_ok)
checar("R34_P_driver_o_campo_trocado_vem_do_valor_independente_nao_do_arquivado", lambda: rc_d == 0 and res_d["veredito"] == "PASSA" and res_d["um_py_medido"]["linha_de_alpha"] == 5584
       and "$.alpha_assignment_line" in res_d["runs"]["T12_optical_r3"]["campos_trocados_no_arquivado"],
       nota="P: o campo alpha_assignment_line do arquivado e SUBSTITUIDO pela linha de alpha do um.py MEDIDO (calculada pelo driver, regex dos runners): um arquivado com outra linha nao muda o "
            "veredito; o que o driver exige e que o runner NOVO escreva essa linha (o runner le o um.py de verdade)")

# ================================================================ R3.4 (M): os modulos de auditoria (NetworkProofAuditR3/R7/R8 da v394)
PRE393 = dict(kernel_anterior=dict(raiz_sha256=NI392["kernel"]["raiz_sha256"], audit_sha256=NI392["kernel"]["audit_sha256"], impressao_formal=NI392["kernel"]["impressao_formal"]))


def _k3(nome, mut):
    k_ = copy.deepcopy(K393_OBJ)
    mut(k_)
    p_ = FX / ("KERNEL_RECIBO_R34_%s.json" % nome)
    p_.write_bytes(json.dumps(k_, ensure_ascii=False, indent=1).encode("utf-8"))
    return p_


def _ku3(nome, kp, contem, ni=None, aceita=False, pre=PRE393, nota="", sandbox=False):
    passa_, det_, pino_ = MOD.verificar_kernel_recibo(kp, "v393", ni or NI393, sha(kp), pre, sandbox, CRIT393_OBJ)
    ok_ = (passa_ is True) if aceita else (passa_ is False and contem in det_)
    _registrar(dict(controle=nome, nivel="unitario", detalhe=det_[:400], esperado_no_detalhe=contem, aceita_esperado=aceita, recibo=str(kp), recibo_sha256=sha(kp), nota=nota), ok_)
    return pino_ or {}


PINO_M = _ku3("R34_M_recibo_R3_4_com_modulo_de_auditoria_listado_e_fonte_so_de_comandos_aceito", K393, None, aceita=True,
              nota="M: o recibo no contrato KERNEL_RECIBO_R3_4: a pedra C (com declaracao) e o modulo de auditoria (so import + run_cmd, sem declaracoes) listado em modulos_de_auditoria; "
                   "o ANTES cruzado com o recibo pre-selo; aceito")
checar("R34_M_o_pino_registra_o_modulo_de_auditoria_e_a_contagem", lambda: PINO_M["modulos_de_auditoria"]["lista"] == ["TGLExt/AuditoriaSinteticaC.lean"] and PINO_M["modulos_de_auditoria"]["fontes_conferidas_por_script"] is True
       and PINO_M["modulos_de_auditoria"]["contagem_de_comandos"]["TGLExt/AuditoriaSinteticaC.lean"]["run_cmd"] == 1 and PINO_M["contrato"] == "KERNEL_RECIBO_R3_4" and PINO_M["n_declaracoes_das_pedras"] == 1,
       nota="M: o pino do recibo do kernel registra o modulo, os comandos contados e o limite declarado", modulos=PINO_M.get("modulos_de_auditoria"))
_ku3("R34_M_sem_a_lista_o_modulo_sem_declaracoes_e_recusado_pela_N1k", _k3("sem_lista", lambda k: k.pop("modulos_de_auditoria")), "exige declaracoes",
     nota="M (o conserto): sem o modulo em modulos_de_auditoria a N1k segue valendo (era o defeito da v394: 3 pedras so com run_cmd recusavam o recibo)")
_ku3("R34_M_contrato_R3_2_sem_lista_o_modulo_e_recusado", _k3("contrato_r32", lambda k: (k.update(contrato="KERNEL_RECIBO_R3_2"), k.pop("modulos_de_auditoria"))), "exige declaracoes",
     nota="M: o contrato antigo (R3_2) segue admitido, com a N1k de sempre")
_ku3("R34_M_contrato_R3_2_com_a_lista_e_recusado", _k3("contrato_r32_com_lista", lambda k: k.update(contrato="KERNEL_RECIBO_R3_2")), "so existe no contrato", nota="M: a lista so existe no contrato R3_4")
_ku3("R34_M_contrato_desconhecido_e_recusado", _k3("contrato_desconhecido", lambda k: k.update(contrato="KERNEL_RECIBO_R3_3")), "contrato=", nota="M: so R3_2 e R3_4")
_ku3("R34_M_lista_nao_e_lista", _k3("lista_texto", lambda k: k.update(modulos_de_auditoria="TGLExt/AuditoriaSinteticaC.lean")), "MODULOS_DE_AUDITORIA_INVALIDOS")
_ku3("R34_M_lista_vazia", _k3("lista_vazia", lambda k: k.update(modulos_de_auditoria=[])), "MODULOS_DE_AUDITORIA_INVALIDOS")
_ku3("R34_M_lista_com_repeticao", _k3("lista_repetida", lambda k: k.update(modulos_de_auditoria=["TGLExt/AuditoriaSinteticaC.lean"] * 2)), "MODULOS_DE_AUDITORIA_INVALIDOS")
_ku3("R34_M_lista_com_item_que_nao_e_texto", _k3("lista_item_numero", lambda k: k.update(modulos_de_auditoria=[1])), "MODULOS_DE_AUDITORIA_INVALIDOS")
_ku3("R34_M_lista_nomeia_arquivo_que_nao_e_pedra_do_recibo", _k3("lista_fora_das_pedras", lambda k: k.update(modulos_de_auditoria=["TGLExt/AuditoriaSinteticaC.lean", "TGLExt/Outro.lean"])),
     "MODULO_DE_AUDITORIA_FORA_DAS_PEDRAS")
_ku3("R34_M_modulo_listado_traz_declaracoes", _k3("auditoria_com_declaracoes", lambda k: next(p for p in k["pedras"] if p["path"].endswith("AuditoriaSinteticaC.lean")).update(declaracoes=["TGLExt.PedraSinteticaC.tres"])),
     "MODULO_DE_AUDITORIA_COM_DECLARACOES", nota="M: um modulo de auditoria nao declara nada (se declarasse seria pedra comum): ambiguidade recusada")
_ku3("R34_M_pedra_com_declaracao_listada_como_auditoria_para_fugir_da_N1k", _k3("pedra_comum_listada", lambda k: (k.update(modulos_de_auditoria=["TGLExt/AuditoriaSinteticaC.lean", "TGLExt/PedraSinteticaC.lean"]),
                                                                                                              next(p for p in k["pedras"] if p["path"].endswith("PedraSinteticaC.lean")).pop("declaracoes"))),
     "MODULO_DE_AUDITORIA_FORA_DA_LISTA_DE_COMANDOS", nota="M: listar uma pedra que DECLARA (theorem) como auditoria, tirando-lhe as declaracoes, nao a dispensa: a fonte tem `theorem` e a varredura recusa")
_ku3("R34_M_pedra_comum_sem_declaracoes_fora_da_lista_recusada", _k3("pedra_sem_declaracoes", lambda k: (k.update(modulos_de_auditoria=["TGLExt/AuditoriaSinteticaC.lean"]),
                                                                                                    next(p for p in k["pedras"] if p["path"].endswith("PedraSinteticaC.lean")).pop("declaracoes"))),
     "exige declaracoes", nota="M: so o que esta na lista e dispensado; a outra pedra sem declaracoes segue recusada pela N1k")


def variante_auditoria(nome, texto):
    """(recibo, nos) com a fonte do modulo de auditoria trocada por `texto` (a arvore, o manifesto do kernel re-pinado no selo e o recibo seguem coerentes)."""
    arv_ = AT34 / ("arv_" + nome)
    copiar_sem_juncao(FX / "kernel_src_v393s", arv_)
    b_ = texto.encode("utf-8")
    (arv_ / "TGLExt" / "AuditoriaSinteticaC.lean").write_bytes(b_)
    d_ = AT34 / ("nos_" + nome)
    d_.mkdir(parents=True)
    for f_ in ("um.py", "um_absoluto.json"):
        shutil.copyfile(NOS393 / f_, d_ / f_)
    man_ = json.loads((NOS393 / "tgl_kernel_proof_manifest.json").read_bytes())
    man_["formal_files_sha256"]["TGLExt/AuditoriaSinteticaC.lean"] = sha_b(b_)
    mb_ = json.dumps(man_, ensure_ascii=False, indent=1).encode("utf-8")
    (d_ / "tgl_kernel_proof_manifest.json").write_bytes(mb_)
    selo_ = json.loads((NOS393 / "um_absoluto_selo.json").read_bytes())
    selo_["sha256"]["tgl_kernel_proof_manifest.json"] = sha_b(mb_)
    (d_ / "um_absoluto_selo.json").write_bytes(json.dumps(selo_, ensure_ascii=False, indent=1).encode("utf-8"))
    kp_ = _k3("fonte_" + nome, lambda k: (k.update(arvore=str(arv_)), next(p for p in k["pedras"] if p["path"].endswith("AuditoriaSinteticaC.lean")).update(sha256=sha_b(b_))))
    return kp_, MOD.ler_nos(d_, "v393")


AUD_BASE = (FX / "kernel_src_v393s" / "TGLExt" / "AuditoriaSinteticaC.lean").read_text(encoding="utf-8")
_kp, _ni = variante_auditoria("base_identica", AUD_BASE)
_ku3("R34_M_variante_base_identica_aceita", _kp, None, ni=_ni, aceita=True, nota="M: contraprova do helper: a fonte inalterada passa pelo mesmo caminho das variantes")
VARIANTES_AUD = (
    ("theorem_no_topo", AUD_BASE + "\ntheorem escondido : 1 = 1 := rfl\n", "comando de topo fora da lista"),
    ("theorem_indentado_depois_do_corpo", AUD_BASE + "  theorem escondido : 1 = 1 := rfl\n", "palavra proibida no corpo"),
    ("def_no_topo", AUD_BASE + "def x := 1\n", "comando de topo fora da lista"),
    ("axiom_no_corpo", AUD_BASE.replace("  let mut n := 0\n", "  let mut n := 0\n  axiom perigo : False\n"), "palavra proibida no corpo"),
    ("sorry_no_corpo", AUD_BASE.replace("  let mut n := 0\n", "  let mut n := sorry\n"), "palavra proibida no corpo"),
    ("addDecl_no_corpo", AUD_BASE.replace("  let mut n := 0\n", "  let mut n := 0\n  addDecl (.axiomDecl default)\n"), "palavra proibida no corpo"),
    ("escrita_de_arquivo_no_corpo", AUD_BASE.replace("  let mut n := 0\n", "  let mut n := 0\n  IO.FS.writeFile \"x\" \"y\"\n"), "palavra proibida no corpo"),
    ("processo_no_corpo", AUD_BASE.replace("  let mut n := 0\n", "  let mut n := 0\n  let _ \u2190 IO.Process.output { cmd := \"calc\" }\n"), "palavra proibida no corpo"),
    ("comentario_de_bloco", AUD_BASE.replace("import Lean\n", "/- theorem escondido -/\nimport Lean\n"), "comentario de bloco"),
    ("comando_desconhecido_example", AUD_BASE + "example : True := trivial\n", "comando de topo fora da lista"),
    ("namespace", AUD_BASE + "namespace X\n", "comando de topo fora da lista"),
    ("set_option", AUD_BASE.replace("import Lean\n", "import Lean\nset_option maxRecDepth 100000\n"), "comando de topo fora da lista"),
    ("caractere_invisivel", AUD_BASE.replace("import Lean\n", "import Le\u200ban\n"), "caractere de controle ou de formato"),
    ("linha_indentada_fora_do_corpo", AUD_BASE.replace("import Lean\n", "import Lean\n  theorem escondido : 1 = 1 := rfl\n"), "linha indentada fora de um corpo"),
    ("so_imports_nenhum_comando_de_auditoria", "import TGLExt.PedraSinteticaC\nimport Lean\n", "nao audita nada"),
    ("import_com_lixo", AUD_BASE.replace("import Lean\n", "import Lean; theorem x : True := trivial\n"), "comando de topo fora da lista"),
)
for nome_, texto_, contem_ in VARIANTES_AUD:
    _kp, _ni = variante_auditoria(nome_, texto_)
    _ku3("R34_M_fonte_%s_recusada" % nome_, _kp, contem_, ni=_ni, nota="M: a fonte do modulo de auditoria com UMA coisa a mais (%s): a varredura por script recusa (MODULO_DE_AUDITORIA_FORA_DA_LISTA_DE_COMANDOS)" % nome_)
# a varredura sozinha (pura): aceita as formas validas, recusa as invalidas
_okp = MOD.auditar_fonte_de_auditoria
checar("R34_M_varredura_aceita_import_open_print_axioms_e_run_cmd", lambda: _okp("import TGLExt.B\nopen Lean in\nrun_cmd do\n  IO.println \"x\"\n#print axioms A.B.c\n-- comentario\n\n")["ok"]
       and _okp("#print axioms X\n")["contagem"]["print_axioms"] == 1, nota="M (unitario): as formas validas")
checar("R34_M_varredura_recusa_texto_vazio_e_so_comentario", lambda: not _okp("")["ok"] and not _okp("-- so comentario\n")["ok"], nota="M (unitario): nada a auditar = recusa")
checar("R34_M_varredura_palavras_dentro_de_nome_nao_sao_a_palavra", lambda: (lambda r_: (not r_["ok"]) and "'defaults'" in r_["motivo"])(_okp("run_cmd do\n  let defaults := 1\n  let instances := 2\n  let theorem_count := 3\n")),
       nota="M (unitario, R3.5): na R3.4 a lista de PROIBICAO olhava a palavra inteira e aceitava `defaults`, `instances`, `theorem_count`; na lista de PERMISSAO estrita um local fora da lista e recusado (e o motivo nomeia o local)")
checar("R34_M_varredura_CRLF_e_tab", lambda: _okp("import Lean\r\nrun_cmd do\r\n\tIO.println \"x\"\r\n")["ok"] and not _okp("import Lean\r\nrun_cmd do\r\n\ttheorem x : True := trivial\r\n")["ok"],
       nota="M (unitario): CRLF e tab nao escondem nem acusam")
# as fontes REAIS dos tres modulos da v394 (so lidas) passam na varredura, e o recibo real da v394 tem exatamente esses tres sem declaracoes
# O snapshot (R3_4/evidencias): a copia de bytes do KERNEL_RECIBO_v394.json (contrato R3_2, 190 pedras, feito as 13:57 de 19/10 -- a pasta v394 e viva) e das 3 fontes de auditoria, conferidas contra o recibo.
EVID = AQUI / "evidencias"
SNAP_RECIBO, SNAP_FONTES = EVID / "KERNEL_RECIBO_v394_SNAPSHOT_R3_2.json", EVID / "fontes_reais_v394"
KR394 = json.loads(SNAP_RECIBO.read_bytes())
SEM_DECL = sorted(p["path"] for p in KR394["pedras"] if not p.get("declaracoes"))
FONTES_AUD_REAIS = {p: SNAP_FONTES / p for p in SEM_DECL}
checar("R34_M_recibo_real_v394_tem_exatamente_tres_pedras_sem_declaracoes", lambda: SEM_DECL == ["TGLExt/F1Fecho394/NetworkProofAuditR3.lean", "TGLExt/F1Fecho394/NetworkProofAuditR7.lean",
                                                                                              "TGLExt/F1Fecho394/NetworkProofAuditR8.lean"] and KR394["contrato"] == "KERNEL_RECIBO_R3_2" and len(KR394["pedras"]) >= 189,
       nota="M (dado real): no KERNEL_RECIBO_v394 (snapshot pinado, %d pedras) as pedras sem declaracoes sao exatamente as 3 de auditoria" % len(KR394["pedras"]), pedras_sem_declaracoes=SEM_DECL,
       contrato=KR394["contrato"], snapshot=_pinar(SNAP_RECIBO), n_pedras=len(KR394["pedras"]))
for rel_, caminho_ in FONTES_AUD_REAIS.items():
    pedra_ = next(p for p in KR394["pedras"] if p["path"] == rel_)
    checar("R34_M_fonte_real_%s_confere_com_o_recibo_e_passa_na_varredura" % Path(rel_).stem,
           (lambda caminho_=caminho_, pedra_=pedra_: caminho_.is_file() and sha(caminho_) == pedra_["sha256"] and _okp(caminho_.read_text(encoding="utf-8"))["ok"]),
           nota="M (dado real): a fonte REAL %s (sha256 igual ao do recibo da v394) so tem comandos de auditoria" % rel_, fonte=str(caminho_),
           contagem=(_okp(caminho_.read_text(encoding="utf-8"))["contagem"] if caminho_.is_file() else None))

# --- M: o derivador do recibo R3_4 a partir do R3_2 (derivar_recibo_kernel_r3_4.py)
DERIV = AQUI / "derivar_recibo_kernel_r3_4.py"


def derivar(nome, recibo):
    saida = FX / ("KERNEL_RECIBO_derivado_%s.json" % nome)
    r_ = subprocess.run([PY, "-I", "-B", "-X", "utf8", str(DERIV), "--recibo", str(recibo), "--saida", str(saida)], capture_output=True, text=True, encoding="utf-8", errors="replace",
                        timeout=300, stdin=subprocess.DEVNULL)
    return r_.returncode, r_.stdout + r_.stderr, saida


_snap_mini = dict(KR394, arvore=str(SNAP_FONTES))        # o snapshot com a arvore apontando para a mini-arvore das 3 fontes (o derivador so le as fontes das pedras sem declaracoes)
_snap_mini_p = FX / "KERNEL_RECIBO_v394_SNAPSHOT_mini_arvore.json"
_snap_mini_p.write_bytes(json.dumps(_snap_mini, ensure_ascii=False, indent=1).encode("utf-8"))
rc_dv, out_dv, sd_dv = derivar("real_v394", _snap_mini_p)
checar("R34_M_derivador_a_partir_do_recibo_real_v394_lista_as_tres_e_so_muda_isso", lambda: rc_dv == 0 and json.loads(sd_dv.read_bytes())["modulos_de_auditoria"] == SEM_DECL
       and json.loads(sd_dv.read_bytes())["contrato"] == "KERNEL_RECIBO_R3_4"
       and {k_: v_ for k_, v_ in json.loads(sd_dv.read_bytes()).items() if k_ not in ("contrato", "modulos_de_auditoria", "derivado_de")} == {k_: v_ for k_, v_ in _snap_mini.items() if k_ != "contrato"}
       and json.loads(sd_dv.read_bytes())["derivado_de"]["sha256"] == sha(_snap_mini_p),
       nota="M (dado real): o derivador, sobre o snapshot do KERNEL_RECIBO_v394 (R3_2, %d pedras; so a arvore aponta para a mini-arvore das 3 fontes), lista exatamente as 3 pedras sem declaracoes "
            "(fontes conferidas pelo sha do recibo e pela varredura) e NADA mais muda (logs, hashes, criterios, pedras); o recibo derivado (contrato R3_4) e a proposta para a gerencia pinar" % len(KR394["pedras"]),
       saida=out_dv[:300])
rc_dv2, out_dv2, _ = derivar("sem_pedra_sem_declaracoes", K_OK)
checar("R34_M_derivador_recusa_recibo_sem_pedra_sem_declaracoes", lambda: rc_dv2 != 0 and "NENHUMA_PEDRA_SEM_DECLARACOES" in out_dv2, nota="o recibo sintetico v392 (todas as pedras declaram): nada a listar", saida=out_dv2[:200])
rc_dv3, out_dv3, _ = derivar("ja_tem_a_lista", K393)
checar("R34_M_derivador_recusa_recibo_que_ja_e_R3_4", lambda: rc_dv3 != 0 and ("CONTRATO_DE_ORIGEM" in out_dv3 or "JA_TEM_MODULOS_DE_AUDITORIA" in out_dv3), nota="o recibo ja esta no contrato R3_4", saida=out_dv3[:200])
_kp_t, _ni_t = variante_auditoria("deriv_teorema", AUD_BASE + "\ntheorem escondido : 1 = 1 := rfl\n")
_k_t = json.loads(_kp_t.read_bytes())
_k_t["contrato"] = "KERNEL_RECIBO_R3_2"
_k_t.pop("modulos_de_auditoria")
_kp_t2 = FX / "KERNEL_RECIBO_R32_com_teorema_no_modulo.json"
_kp_t2.write_bytes(json.dumps(_k_t, ensure_ascii=False, indent=1).encode("utf-8"))
rc_dv4, out_dv4, _ = derivar("modulo_com_teorema", _kp_t2)
checar("R34_M_derivador_recusa_pedra_sem_declaracoes_que_nao_e_so_de_auditoria", lambda: rc_dv4 != 0 and "PEDRA_SEM_DECLARACOES_QUE_NAO_E_DE_AUDITORIA" in out_dv4,
       nota="a pedra sem declaracoes registradas cuja fonte TEM um theorem nao e listada: o derivador recusa (nao se lista o que declara)", saida=out_dv4[:240])
_arv_f = AT34 / "arv_deriv_fonte_diferente"
copiar_sem_juncao(FX / "kernel_src_v393s", _arv_f)
(_arv_f / "TGLExt" / "AuditoriaSinteticaC.lean").write_bytes((_arv_f / "TGLExt" / "AuditoriaSinteticaC.lean").read_bytes() + b"-- mudado\n")
_k_f = copy.deepcopy(K393_OBJ)
_k_f["contrato"] = "KERNEL_RECIBO_R3_2"
_k_f.pop("modulos_de_auditoria")
_k_f["arvore"] = str(_arv_f)
_kp_f = FX / "KERNEL_RECIBO_R32_fonte_diferente.json"
_kp_f.write_bytes(json.dumps(_k_f, ensure_ascii=False, indent=1).encode("utf-8"))
rc_dv5, out_dv5, _ = derivar("fonte_diferente", _kp_f)
checar("R34_M_derivador_recusa_fonte_que_nao_e_a_do_recibo", lambda: rc_dv5 != 0 and "FONTE_NAO_E_A_DO_RECIBO" in out_dv5, nota="a arvore tem outra fonte (um comentario a mais): o sha do recibo nao confere", saida=out_dv5[:200])

# ================================================================ R3.5 (M): a lista de PERMISSAO estrita do modulo de auditoria -- cada evasao da revisao independente de 19/10 (B-M) e as minhas
# cada controle monta a fonte do modulo (a fixture sintetica + UMA coisa a mais), re-pina o recibo e o selo do sandbox e chama verificar_kernel_recibo (o caminho real do B(n)): recusa com o token nomeado
AUD_PERM = "palavra proibida no corpo"
EVASOES_AUD = (
    # as cinco da revisao independente (EXAME_DELTA_E_R3_4.md, B-M), exatas
    ("Lean_addDecl_qualificado", AUD_BASE + "  Lean.addDecl (.axiomDecl default)\n", "'Lean.addDecl'"),
    ("Lean_modifyEnv_qualificado", AUD_BASE + "  Lean.modifyEnv (fun e => e)\n", "'Lean.modifyEnv'"),
    ("Lean_Meta_evalExpr_qualificado", AUD_BASE + "  let _ \u2190 Lean.Meta.evalExpr Nat (mkConst `Nat) (mkConst `Nat)\n", "'Lean.Meta.evalExpr'"),
    ("open_IO_FS_in_mais_writeFile", AUD_BASE.replace("open Lean in", "open IO.FS in") + "  writeFile \"x\" \"y\"\n", "open fora da lista de permissao"),
    ("open_IO_in_mais_Process_output", AUD_BASE.replace("open Lean in", "open IO in") + "  let _ \u2190 Process.output { cmd := \"calc\" }\n", "open fora da lista de permissao"),
    # as mesmas, com o `open` permitido: o corpo sozinho recusa
    ("writeFile_com_open_Lean", AUD_BASE + "  writeFile \"x\" \"y\"\n", "'writeFile'"),
    ("Process_output_com_open_Lean", AUD_BASE + "  let _ \u2190 Process.output { cmd := \"calc\" }\n", "'Process.output'"),
    ("addDecl_nu_com_open_Lean", AUD_BASE + "  addDecl (.axiomDecl default)\n", "'addDecl'"),
    ("modifyEnv_nu_com_open_Lean", AUD_BASE + "  modifyEnv (fun e => e)\n", "'modifyEnv'"),
    # variantes de qualificacao, metodo e campo
    ("root_Lean_addDecl", AUD_BASE + "  _root_.Lean.addDecl (.axiomDecl default)\n", "'_root_.Lean.addDecl'"),
    ("IO_FS_writeFile_completo", AUD_BASE + "  IO.FS.writeFile \"x\" \"y\"\n", "'IO.FS.writeFile'"),
    ("IO_Process_spawn", AUD_BASE + "  let _ \u2190 IO.Process.spawn { cmd := \"calc\" }\n", "'IO.Process.spawn'"),
    ("System_FilePath", AUD_BASE + "  let _ := System.FilePath.mk \"x\"\n", "'System.FilePath.mk'"),
    ("env_addDecl_como_metodo_do_local", AUD_BASE + "  let _ := env.addDecl\n", "'env.addDecl'"),
    ("campo_depois_de_parenteses", AUD_BASE + "  let _ := (env).modifyEnv\n", "'.modifyEnv'"),
    ("campo_no_inicio_da_linha", AUD_BASE + "  .writeFile\n", "campo fora da lista de permissao"),
    ("tab_como_indentacao_nao_esconde", AUD_BASE + "\tLean.addDecl 1\n", "'Lean.addDecl'"),
    # sintaxe: o que nao e palavra, local, funcao, metodo, nome, numero, texto ou sinal da lista
    ("interpolacao_de_termo_em_throwError", AUD_BASE + "  throwError \"x {IO.FS.readFile n}\"\n", "interpolacao"),
    ("dois_comandos_na_linha_com_ponto_e_virgula", AUD_BASE + "  let n := 1; let m := 2\n", "caractere fora da lista de permissao: ';'"),
    ("antiquotacao_cifrao", AUD_BASE + "  let n := $m\n", "caractere fora da lista de permissao: '$'"),
    ("comentario_no_fim_da_linha", AUD_BASE + "  let n := 1 -- IO.FS.writeFile\n", "caractere fora da lista de permissao: '-'"),
    ("include_str", AUD_BASE + "  let n := include_str \"/etc/hosts\"\n", "'include_str'"),
    ("unsafe", AUD_BASE + "  unsafe pure ()\n", "'unsafe'"),
    ("nome_com_crase_fora_da_lista", AUD_BASE + "  let n := `Foo.bar\n", "nome com crase fora da lista"),
    ("homoglifo_cirilico_no_identificador", AUD_BASE + "  L\u0435an.addDecl 1\n", AUD_PERM),
    ("local_fora_da_lista", AUD_BASE + "  let defaults := 1\n", "'defaults'"),
    ("numero_colado_a_identificador", AUD_BASE + "  let n := 1addDecl\n", "'addDecl'"),
    ("escape_fora_da_lista_no_texto", AUD_BASE + "  IO.println \"\\x41\"\n", "escape fora da lista"),
    ("texto_sem_fechamento", AUD_BASE + "  IO.println \"abc\n", "literal de texto sem fechamento"),
    # comandos de topo: open so de Lean, import so de Lean/TGLExt/TGL, nada na mesma linha
    ("open_Lean_Meta_in", AUD_BASE.replace("open Lean in", "open Lean.Meta in"), "open fora da lista de permissao"),
    ("open_Lean_IO_dois_namespaces", AUD_BASE.replace("open Lean in", "open Lean IO in"), "open fora da lista de permissao"),
    ("open_IO_sem_in", AUD_BASE.replace("open Lean in", "open IO"), "open fora da lista de permissao"),
    ("import_Mathlib", AUD_BASE.replace("import Lean\n", "import Mathlib\n"), "comando de topo fora da lista"),
    ("import_Lean_Elab_Command_qualificado", AUD_BASE.replace("import Lean\n", "import Lean.Elab.Command\n"), "comando de topo fora da lista"),
    ("run_cmd_com_comando_na_mesma_linha", AUD_BASE.replace("run_cmd do\n", "run_cmd IO.FS.writeFile \"x\" \"y\"\n"), "comando de topo fora da lista"),
    ("open_Lean_in_com_theorem_na_mesma_linha", AUD_BASE.replace("open Lean in\n", "open Lean in theorem x : True := trivial\n"), "comando de topo fora da lista"),
)
for nome_, texto_, contem_ in EVASOES_AUD:
    _kp, _ni = variante_auditoria("r35_" + nome_, texto_)
    _ku3("R35_M_evasao_%s_recusada" % nome_, _kp, contem_, ni=_ni,
         nota="M (R3.5, lista de PERMISSAO estrita): a fonte do modulo de auditoria com a evasao %s: o B(n) recusa (MODULO_DE_AUDITORIA_FORA_DA_LISTA_DE_COMANDOS) e o detalhe nomeia o token" % nome_)
_kp, _ni = variante_auditoria("r35_contraprova_base", AUD_BASE)
_ku3("R35_M_contraprova_a_fixture_inalterada_passa_pelo_mesmo_caminho", _kp, None, ni=_ni, aceita=True, nota="M: a contraprova do helper das evasoes: a fixture sem a evasao passa pela lista de permissao")
_fr = {n_: (SNAP_FONTES / "TGLExt" / "F1Fecho394" / ("NetworkProofAudit%s.lean" % n_)).read_text(encoding="utf-8") for n_ in ("R3", "R7", "R8")}
_cr = {n_: _okp(t_) for n_, t_ in _fr.items()}
checar("R35_M_as_tres_fontes_reais_passam_na_lista_de_permissao_e_a_contagem_confere",
       lambda: all(c_["ok"] for c_ in _cr.values()) and _cr["R3"]["contagem"]["print_axioms"] == 936 and _cr["R3"]["contagem"]["tokens"] == 0
       and _cr["R7"]["contagem"]["run_cmd"] == 1 and _cr["R8"]["contagem"]["run_cmd"] == 1 and _cr["R7"]["contagem"]["tokens"] == _cr["R8"]["contagem"]["tokens"] > 100
       and _cr["R7"]["contagem"]["open_"] == 1 and _cr["R8"]["contagem"]["open_"] == 1,
       nota="M (dado real): as tres fontes REAIS (NetworkProofAuditR3/R7/R8, copias de bytes em evidencias/) passam na lista de permissao estrita: R3 so #print axioms; R7 e R8 um run_cmd com o mesmo corpo",
       contagens={n_: c_["contagem"] for n_, c_ in _cr.items()})
checar("R35_M_o_vocabulario_do_corpo_e_fechado_e_pequeno", lambda: len(MOD.AUD_CORPO_GLOBAIS) == 8 and len(MOD.AUD_CORPO_LOCAIS) == 11 and MOD.AUD_OPEN_PERMITIDOS == frozenset(("Lean",))
       and not (MOD.AUD_CORPO_GLOBAIS | MOD.AUD_CORPO_PALAVRAS | MOD.AUD_CORPO_METODOS) & {"addDecl", "modifyEnv", "evalExpr", "writeFile", "Process", "output", "spawn", "include_str", "unsafe", "sorry", "axiom"},
       nota="M: a lista de permissao tem so 8 funcoes globais, 11 locais e o namespace Lean; nenhum nome de escrita de ambiente, de arquivo, de processo, de avaliacao ou de axioma entra nela",
       globais=sorted(MOD.AUD_CORPO_GLOBAIS), locais=sorted(MOD.AUD_CORPO_LOCAIS), metodos=sorted(MOD.AUD_CORPO_METODOS))
# o derivador tambem usa a lista de permissao: nao lista (nem aceita) o modulo com a evasao
for nome_, texto_ in (("Lean_addDecl_qualificado", AUD_BASE + "  Lean.addDecl (.axiomDecl default)\n"), ("open_IO_FS_mais_writeFile", AUD_BASE.replace("open Lean in", "open IO.FS in") + "  writeFile \"x\" \"y\"\n")):
    _kp_d, _ = variante_auditoria("r35d_" + nome_, texto_)
    _kd = json.loads(_kp_d.read_bytes())
    _kd["contrato"] = "KERNEL_RECIBO_R3_2"
    _kd.pop("modulos_de_auditoria")
    _kp_d2 = FX / ("KERNEL_RECIBO_R35_deriv_%s.json" % nome_)
    _kp_d2.write_bytes(json.dumps(_kd, ensure_ascii=False, indent=1).encode("utf-8"))
    rc_x, out_x, _ = derivar("r35_" + nome_, _kp_d2)
    checar("R35_M_derivador_recusa_%s" % nome_, lambda rc_x=rc_x, out_x=out_x: rc_x != 0 and "PEDRA_SEM_DECLARACOES_QUE_NAO_E_DE_AUDITORIA" in out_x,
           nota="M: o derivador (derivar_recibo_kernel_r3_4.py) usa a mesma lista de permissao: a pedra sem declaracoes cuja fonte tem a evasao %s NAO e listada em modulos_de_auditoria" % nome_, saida=out_x[:240])

# ================================================================ R3.5 (V): o recibo pre_selo REAL da R3.4 (gerado ANTES da instalacao da v394) continua valendo sob a R3.5
REC_REAL = AQUI / "recibo_pre_selo_v394" / "RECIBO_SINCRONIZACAO_v393_20261019_134158.json"
PINO_REC = json.loads((AQUI / "PINO_RECIBO_PRE_SELO_v394_R3_4.json").read_bytes())
CAD_V = AQUI / "CADEIA_DE_SELOS_v394.json"
BASE393 = WORK / "cadeia_de_selo" / "v394" / "base_v393"
BASE392 = WORK / "cadeia_de_selo" / "v393" / "base_v392"
_cad_v = MOD.carregar_cadeia_de_selos(CAD_V, sha(CAD_V))
_ant_prod2 = MOD.estado_anterior(PROD, MOD.carregar_canonical(PROD)[0])


def _conf_real(rec=REC_REAL, ant=None, sha_=None, selo=None, kman=None, cad="padrao"):
    """o MESMO caminho que o B(n) pos_selo usa: conferir_recibo_pre_selo contra a Bancada de PRODUCAO (so leitura), o selo e o manifesto do kernel da v393 (custodia) e a cadeia."""
    return MOD.conferir_recibo_pre_selo(rec, ant or _ant_prod2, MOD.PRODUCAO, False, sha_ or sha(rec), selo or (BASE393 / "um_absoluto_selo.json"),
                                        kman or (BASE393 / "tgl_kernel_proof_manifest.json"), _cad_v if cad == "padrao" else cad)


def _lendo(fn):
    """roda fn() registrando todo caminho aberto por Path.read_bytes/Path.read_text/open (para provar o que a conferencia NAO le)."""
    import builtins
    lidos = []
    rb, rt, op = Path.read_bytes, Path.read_text, builtins.open

    def _rb(self, *a, **k):
        lidos.append(str(self))
        return rb(self, *a, **k)

    def _rt(self, *a, **k):
        lidos.append(str(self))
        return rt(self, *a, **k)

    def _op(f, *a, **k):
        lidos.append(str(f))
        return op(f, *a, **k)
    Path.read_bytes, Path.read_text, builtins.open = _rb, _rt, _op
    try:
        r_ = fn()
    finally:
        Path.read_bytes, Path.read_text, builtins.open = rb, rt, op
    return r_, lidos


_r_real, _lidos_real = _lendo(_conf_real)
_rec_real = json.loads(REC_REAL.read_bytes())
checar("R35_V_recibo_pre_selo_real_da_R3_4_e_aceito_pela_R3_5",
       lambda: _r_real["veredito"] == PINO_REC["veredito"] and _r_real["salto"]["de"]["versao"] == "v392" and _r_real["salto"]["ate"]["versao"] == "v393" and _r_real["salto"]["versoes_puladas"] == ["v393"]
       and _r_real["salto"]["proxima_a_selar"] == "v394" and _r_real["sha256"] == PINO_REC["sha256"] == sha(REC_REAL) and _r_real["bateria"]["falha"] == 0
       and _rec_real["script_sha256"] == sha(R34 / "sincronizar_bancada.py") and _rec_real["script_sha256"] != sha(SYNC) and _r_real["versao"] == "v393",
       nota="V (o requisito): o recibo pre_selo REAL gerado pela R3.4 antes da instalacao da v394 (salto v392 a v393, proxima a selar v394, bateria passou) e aceito, SEM mudar um byte, pela conferencia da R3.5 "
            "contra a Bancada de PRODUCAO real (so lida); o recibo traz o script_sha256 do esboco R3.4, diferente do da R3.5", veredito=_r_real["veredito"], salto=_r_real["salto"],
       script_do_recibo=_rec_real["script_sha256"][:16], script_da_r35=sha(SYNC)[:16])
checar("R35_V_a_conferencia_do_recibo_real_nao_le_o_nos_vivo_nem_escreve", lambda: not any(str(NOS_REAL).lower() in x_.lower() for x_ in _lidos_real) and len(_lidos_real) > 0,
       nota="V: a conferencia do recibo real nao abre nenhum arquivo do Nos REAL (hoje no meio do rito da v394): ela depende da producao, do recibo, da cadeia e das copias de custodia", n_arquivos_lidos=len(_lidos_real),
       amostra=sorted(set(Path(x_).name for x_ in _lidos_real))[:12])


def _recusa_conf(**kw):
    try:
        _conf_real(**kw)
        return None
    except MOD.Recusa as exc:
        return str(exc)


_rc1 = _recusa_conf(cad=None)
checar("R35_V_recibo_pre_selo_real_sem_a_cadeia_e_recusado", lambda: _rc1 is not None and _rc1.startswith("RECIBO_PRE_SELO_SALTO_SEM_CADEIA"), nota="V: o recibo de salto sem a cadeia nao se confere", recusa=_rc1)
_adulterado = FX / "RECIBO_REAL_com_um_byte_mudado.json"
_b_ = bytearray(REC_REAL.read_bytes())
_b_[100] ^= 1
_adulterado.write_bytes(bytes(_b_))
_rc2 = _recusa_conf(rec=_adulterado, sha_=sha(REC_REAL))
checar("R35_V_recibo_pre_selo_real_com_um_byte_mudado_e_recusado", lambda: _rc2 is not None and "RECIBO_PRE_SELO" in _rc2, nota="V: um byte mudado no recibo real: o sha pinado nao confere e a conferencia recusa", recusa=_rc2)
_rc3 = _recusa_conf(ant=MOD.estado_anterior(B1, MOD.carregar_canonical(B1)[0]))
checar("R35_V_recibo_pre_selo_real_contra_outra_bancada_e_recusado", lambda: _rc3 is not None and _rc3.startswith(("RECIBO_PRE_SELO", "CADEIA_DE_SELOS_NAO_PARTE_DA_BANCADA")),
       nota="V: contra uma Bancada que pina v393 (e nao a v392 do recibo), a conferencia recusa (a cadeia nao parte dessa Bancada, ou o recibo nao corresponde a ela)", recusa=_rc3)
_rc4 = _recusa_conf(selo=BASE392 / "um_absoluto_selo.json", kman=BASE392 / "tgl_kernel_proof_manifest.json")
checar("R35_V_recibo_pre_selo_real_com_o_selo_anterior_errado_e_recusado", lambda: _rc4 is not None, nota="V: o selo e o manifesto do kernel da v392 no lugar dos da v393 (o fim da cadeia): a conferencia recusa", recusa=_rc4)

# ================================================================ R3.5 (P): a bateria da v394 contra o um.py CANDIDATO REAL (d19, o instalado), por stand-in (o selo e sintetico; o Nos real esta no meio do rito)
CAND_V394 = WORK / "cadeia_de_selo" / "v394" / "um_v394_candidato_d19.py"
BAT_394S, BAT_394S_SHA, PINO_394S = gerar_bateria_r34("v394s", "v394", NOS394S)
d_v394, j_v394 = run("R35_P_run_bateria_inteira_contra_o_um_py_v394_candidato", ["--bancada", B1S394, "--nos", NOS394S, "--versao", "v394", "--bateria", BAT_394S, "--bateria-sha256", BAT_394S_SHA,
                                                                                   "--modo", "ensaio", "--fase", "pre_selo"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1S394, saida=S / "v394s",
                     extra_ok=lambda j, r: (lambda rec: rec["bateria_resultado"]["falha"] == 0 and rec["bateria_resultado"]["passa"] == 13 and testes(j)["T12_T13_T14_ATRATOR"]["resultado"] == "PASSA"
                                            and rec["bateria"]["pinos_da_versao"]["versao"] == "v394" and rec["bateria"]["pinos_da_versao"]["conferidos_contra_o_nos_lido"] is True
                                            and rec["nos"]["um_py"]["sha256"] == sha(CAND_V394) and isolado(rec, S / "v394s"))(recibo_de(j)),
                     nota="P (a bateria da v394): gerada por script (gerar_bateria_r3_4.py --versao v394) para o stand-in do Nos v394 (o um.py CANDIDATO REAL d19, selo sintetico) e rodada INTEIRA contra a Bancada pinada nele: "
                          "13 PASSA, 0 FALHA, T12/T13/T14 repinados para o um.py v394, pinos da versao conferidos; o T17 so roda no pos_selo")
_t12_v394 = json.loads(Path(S / "v394s" / "recibos" / "T12_T13_T14_ATRATOR.json").read_bytes())
checar("R35_P_o_replay_do_atrator_passa_com_o_um_py_v394_e_a_linha_de_alpha_e_medida", lambda: _t12_v394["veredito"] == "PASSA" and all(r_["passa"] and r_["n_mismatch"] == 0 for r_ in _t12_v394["runs"].values())
       and _t12_v394["adendo_de_pino"]["entrada_do_um_py"]["depois"]["sha256"] == sha(CAND_V394) and _t12_v394["um_py_medido"]["linha_de_alpha"] == 5584,
       nota="P: o replay dos runners congelados da F1.ATRATOR com o um.py v394 (o candidato real): 3 runners, 0 divergencias; o pino do um.py do pre-registro e repinado na copia para o v394; a linha da atribuicao de alpha e MEDIDA",
       adendo=_t12_v394["adendo_de_pino"]["entrada_do_um_py"], linha_de_alpha=_t12_v394["um_py_medido"]["linha_de_alpha"])

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
# --- N2c (R3.1) na re-execucao: o manifesto B3 gravado registra o selo da geracao anterior; sem ele, a referencia falta e recusa
checar("R31_N2c_manifesto_B3_registra_o_selo_anterior",
       lambda: json.loads((B2 / "canonical_contracts.json").read_bytes())["sincronizacao"]["anterior"]["seal_sha_pinado"] == SBM["nos"]["selo"]["sha256"],
       nota="N2c: o bloco sincronizacao.anterior do manifesto B3 (gravado pelo run 2) traz o seal_sha_pinado da v391 copiada; e por ele que o RUN_2bis cruzou o recibo pre-selo")
checar("R32_R31_3_manifesto_B3_registra_o_kernel_anterior",
       lambda: json.loads((B2 / "canonical_contracts.json").read_bytes())["sincronizacao"]["anterior"]["kernel_manifesto_sha256"] == sha(KMAN_ANT),
       nota="R31-3: o bloco sincronizacao.anterior do manifesto B3 (gravado pelo run 2) traz o manifesto do kernel v391 que o selo anterior pina")
checar("R32_R31_3_RUN_2bis_cruzou_pelo_registro_do_manifesto",
       lambda: (lambda rec: rec["recibo_pre_selo"]["kernel_cruzado_com_o_selo_anterior"]["registrado_no_manifesto_da_bancada"] == sha(KMAN_ANT)
                and rec["recibo_pre_selo"]["kernel_manifesto_anterior_sha256"] == sha(KMAN_ANT))(
           json.loads(sorted((S / "RUN_2bis_idempotente").glob("RECIBO_SINCRONIZACAO_*.json"))[-1].read_bytes())),
       nota="R31-3: na re-execucao (ja sincronizada), o pino do selo anterior confere tambem com o que o manifesto B3 registrou")
b2s = RAIZ / "b2s"
copiar_sem_juncao(B2, b2s)
_ms = json.loads((b2s / "canonical_contracts.json").read_bytes())
_ms["sincronizacao"]["anterior"].pop("seal_sha_pinado")
(b2s / "canonical_contracts.json").write_bytes(json.dumps(_ms, ensure_ascii=False, indent=1).encode("utf-8"))
run("R31_N2c_reexecucao_sem_selo_anterior_no_manifesto", ["--bancada", b2s, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox",
                                                          "--modo", "aplicar", "--fase", "pos_selo", "--evento", "SANDBOX:N2c", "--recibo-pre-selo", R1B,
                                                          "--recibo-pre-selo-sha256", sha(R1B), "--kernel-recibo", K_OK, "--kernel-recibo-sha256", K_OK_SHA], 2,
    "RECIBO_PRE_SELO_SEM_REFERENCIA", bancada=b2s,
    nota="N2c: um manifesto ja sincronizado sem o seal_sha_pinado da geracao anterior (ex.: gravado por uma revisao antiga) nao serve de referencia: recusa")
apagar_arvore(b2s)
run("POS_estado_final_b2_v392_ensaio", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT, "--sem-bateria"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B2,
    nota="estado final: b2 sincronizada em v392 (ensaio sem bateria, so leitura)")

# ================================================================ fecho: juncoes desfeitas PRIMEIRO; a producao, o Nos e o livro real intocados
for jj in JUNCOES:
    if jj.is_junction():
        os.rmdir(jj)          # remove a JUNCAO (nunca o alvo)
juncoes_restantes = [str(jj) for jj in JUNCOES if os.path.lexists(jj)]
assert sorted(os.listdir(PROD)) == PROD_LISTA_ANTES, "a lista da producao mudou"
NOS_LISTA_DEPOIS = sorted(os.listdir(NOS_REAL))
NOS_REAL_REGISTRO = dict(itens_antes=len(NOS_LISTA_ANTES), itens_depois=len(NOS_LISTA_DEPOIS), acrescentados=sorted(set(NOS_LISTA_DEPOIS) - set(NOS_LISTA_ANTES)), removidos=sorted(set(NOS_LISTA_ANTES) - set(NOS_LISTA_DEPOIS)),
                         um_py_sha256_antes=NOS_UM_SHA_ANTES, um_py_sha256_depois=sha(NOS_REAL / "um.py"),
                         nota="R3.5: o Nos real esta no meio do rito da v394 (outro processo escreve nele); este script so o LE (a lista e o sha do um.py) e nunca grava nele: a guarda SAIDA_NO_NOS e os controles A5 o provam; o stand-in v393 vem da custodia")
EV_REAL_BYTES_DEPOIS = EVENTOS_REAL.read_bytes()
assert EV_REAL_BYTES_DEPOIS.startswith(EV_REAL_BYTES_ANTES), "o livro real de eventos foi REESCRITO (nao so acrescido)"
EV_N_ANTES, EV_N_DEPOIS = len(EV_REAL_BYTES_ANTES.splitlines()), len(EV_REAL_BYTES_DEPOIS.splitlines())
EV_NOVOS = [json.loads(l) for l in EV_REAL_BYTES_DEPOIS[len(EV_REAL_BYTES_ANTES):].decode("utf-8").splitlines() if l.strip()]
assert not any(e.get("tipo") == "SINCRONIZACAO_BANCADA" for e in EV_NOVOS), "nasceu no livro real um elo SINCRONIZACAO_BANCADA durante os controles"
assert sha(PROD / "canonical_contracts.json") == PROD_MAN_ANTES == SBM["manifesto_producao_sha256"], "o manifesto de producao mudou"
n_pass = sum(1 for x in RES if x["passa"])
nomes = [x["controle"] for x in RES]
assert len(nomes) == len(set(nomes)), "nome de controle repetido"
R32_RES = json.loads((R32 / "CONTROLES_NEGATIVOS_R3_2.json").read_bytes())
R32_NOMES = [c["controle"] for c in R32_RES["controles"]]
faltam_r32 = sorted(set(R32_NOMES) - set(nomes))
R33_RES = json.loads((PASTA_R33 / "CONTROLES_NEGATIVOS_R3_3.json").read_bytes())
R33_NOMES = [c["controle"] for c in R33_RES["controles"]]
faltam_r33 = sorted(set(R33_NOMES) - set(nomes))
R34_RES = json.loads((R34 / "CONTROLES_NEGATIVOS_R3_4.json").read_bytes())
R34_NOMES = [c["controle"] for c in R34_RES["controles"]]
faltam_r34 = sorted(set(R34_NOMES) - set(nomes))
NOVOS_R35 = [x for x in nomes if x not in set(R34_NOMES)]
NOVOS_R33 = [x for x in R33_NOMES if x not in set(R32_NOMES)]
NOVOS_R34 = [x for x in nomes if x not in set(R33_NOMES)]
MUDARAM_R34 = {}
for x_ in RES:
    if x_["controle"] in R33_NOMES and any(str(c_) in (VR, VR_ERRADA) for c_ in (x_.get("comando") or [])):
        MUDARAM_R34.setdefault(x_["controle"], []).append("R3.4: a familia b1 (a copia que pina o Nos REAL) usa a versao do Nos real de hoje (%s) onde a R3.3 usava v391, e o b1 e derivado da "
                                                           "producao ATUAL (B3) re-pinada para esse Nos (montar_sandbox R3.4); a recusa esperada nao mudou" % VR)
for x_, motivo_ in (("RUN_1a_pre_selo_b1_nos_real", "R3.4: contra o Nos REAL v393 (a v391 nao esta mais no caminho real) com a bateria POR VERSAO gerada por script (T12 repinado para o um.py medido); "
                                                     "as conferencias de sha usam SBM.nos_real; o recibo traz pinos_da_versao conferidos"),
                    ("RUN_1b_pre_selo_b2_nos_copia", "R3.4: a copia v391 do Nos vem da custodia (the_boundary_BACKUPS/um_v391_*) e a bateria e a POR VERSAO gerada para ela (T12 repinado, na copia, "
                                                     "para o um.py da copia): o pre-registro congelado pinava o um.py v391 no caminho real, que hoje e v393")):
    if x_ in R33_NOMES:
        MUDARAM_R34.setdefault(x_, []).append(motivo_)
R31_RES = json.loads((R31 / "CONTROLES_NEGATIVOS_R3_1.json").read_bytes())
R31_NOMES = [c["controle"] for c in R31_RES["controles"]]
faltam_r31 = sorted(set(R31_NOMES) - set(nomes))
NOVOS_R32 = [x for x in nomes if x not in set(R31_NOMES)]
MUDARAM_R32 = {}
for x in sorted(set(INJETADOS_SELO)):
    if x in R31_NOMES:
        MUDARAM_R32.setdefault(x, []).append("R31-3: o comando ganhou --selo-anterior/--kernel-manifesto-anterior (a custodia v391 do sandbox), porque o B(n) R3.2 cruza o "
                                             "recibo pre-selo com o pino externo do kernel anterior; o resto do comando e a recusa esperada nao mudaram")
for x, motivo in (("A9_sem_B_nenhum_pycache", "R31-1: sem -B o esboco R3.2 recusa (INTERPRETADOR_NAO_ISOLADO) antes de qualquer import; o controle (agora -I -X utf8, sem -B) "
                                              "confere que nada e gravado e nenhum __pycache__ nasce; a forma valida ficou em R32_A9_com_I_e_B_nenhum_pycache"),
                  ("N5_PYTHONPATH_injetado_nao_chega_ao_teste", "R31-1: o esboco chamado com -I (que inclui -E) em vez de -E"),
                  ("N5_PYTHONPATH_sem_E_recusado", "R31-1: sem -I a recusa e a do topo, INTERPRETADOR_NAO_ISOLADO, antes da guarda AMBIENTE_PYTHON_INJETAVEL (que segue no "
                                                   "codigo como defesa em profundidade, inalcancavel por subprocesso sob -I)"),
                  ("R31_A4_appdata_de_ataque_esboco_com_s", "R31-1: com -s (sem -I) o esboco R3.2 recusa (INTERPRETADOR_NAO_ISOLADO); nenhuma marca; a forma valida e "
                                                            "R32_A4_appdata_de_ataque_esboco_com_I"),
                  ("R31_A4_appdata_de_ataque_esboco_sem_s_residuo_so_no_esboco", "R31-1: sem -I o esboco recusa; o .pth/usercustomize do APPDATA herdado ainda roda no "
                                                                                 "processo do esboco ANTES da 1a linha (residuo da chamada errada), e nada e gravado")):
    if x in R31_NOMES:
        MUDARAM_R32.setdefault(x, []).append(motivo)
for x in ("R31_N2c_selo_e_kernel_de_outro_rito", "R31_N2c_so_o_selo_trocado", "R31_N2c_kernel_que_o_selo_dele_nao_pina", "R31_N2c_recibo_sem_selo",
          "R31_N2c_contraprova_recibo_1b_aceito"):
    if x in R31_NOMES:
        MUDARAM_R32.setdefault(x, []).append("R31-3: a chamada unitaria de conferir_recibo_pre_selo passa o selo e o manifesto do kernel anteriores (custodia do sandbox)")
GERAIS_R32 = ["R31-1: todo subprocesso do esboco roda com -I -B -X utf8 (na R3.1, -B -X utf8); este script roda com -I -B -X utf8",
              "R31-4/12-ter: a fixture do recibo do kernel passou ao contrato KERNEL_RECIBO_R3_2 (+ varredura_tokens) e o build log sintetico traz as linhas "
              "de job do lake; os recibos invalidos sao derivados da fixture nova; o codigo de recusa esperado nao mudou",
              "R31-3: a arvore sintetica ganhou TGLExt/O16/SinteticoO16.lean (fora do manifesto) e o sandbox ganhou fx/custodia_v391/"]
R3_RES = json.loads((R3 / "CONTROLES_NEGATIVOS_R3.json").read_bytes())
R3_NOMES = [c["controle"] for c in R3_RES["controles"]]
faltam_r3 = sorted(set(R3_NOMES) - set(nomes))
NOVOS = [x for x in nomes if x not in set(R3_NOMES)]
FIXTURE_R3_1 = ("a fixture-base do recibo do kernel passou do contrato KERNEL_RECIBO_R3 para KERNEL_RECIBO_R3_1 (toolchain em lista, pedras com declaracoes, "
                "formal_files_antes, criterios so com o medido) e a verificacao recebe o CRITERIOS sintetico pinado; o recibo invalido e derivado da fixture nova; "
                "o codigo de recusa esperado nao mudou")
MUDARAM = {}
for x in sorted(set(INJETADOS)):
    if x in R3_NOMES:
        MUDARAM.setdefault(x, []).append("A3: o comando ganhou --criterios/--criterios-sha256 (o CRITERIOS sintetico pinado), porque o B(n) R3.1 exige os esperados "
                                         "pinados sempre que ha --kernel-recibo; o resto do comando e a recusa esperada nao mudaram")
for x in R3_NOMES:
    if x.startswith(("N1_unit_kernel_recibo_", "A1_kernel_recibo_invalido_", "N1_sub_kernel_recibo_", "N1_unit_")) and x in nomes:
        MUDARAM.setdefault(x, []).append(FIXTURE_R3_1)
for x, motivo in (("N1_sub_kernel_recibo_log_com_sorry", "A1: o controle antigo acrescentava o aviso no formato de ASPAS SIMPLES, o mesmo da regex da R3 -- confirmava-se "
                                                         "a si mesmo; agora acrescenta a linha VERBATIM do aviso real do Lean 4.31 (crases), lida de um log do Nos (so leitura)"),
                  ("N1_unit_kernel_recibo_log_com_sorry", "A1: idem (a linha real com crases); o formato de aspas ficou no controle novo N1_unit_kernel_recibo_log_com_sorry_aspas"),
                  ("N1_unit_kernel_recibo_toolchain_diverge", "N1m: a toolchain divergente do recibo agora e uma LISTA (o formato do contrato R3_1); na R3 era texto"),
                  ("N1_unit_manifesto_toolchain_diverge", "N1m: a toolchain divergente do manifesto agora e uma LISTA; na R3 era texto"),
                  ("N3_decoy_servico_volta_antes_do_recibo_em_estado", "N3a: com o servico ainda no ar depois do rollback (a sonda simulada repete o ultimo valor), o "
                                                                       "codigo passa de APLICACAO_REVERTIDA para o proprio SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO"),
                  ("N5_PYTHONPATH_injetado_nao_chega_ao_teste", "A4: o teste de ambiente T00_AMBIENTE mudou de formato: na R3 exigia PYTHONPATH ausente; na R3.1 o esboco "
                                                                "poe PYTHONPATH = o site do usuario REAL para os netos (so caminho), e o teste exige -s, APPDATA vazio, "
                                                                "nenhum usercustomize e o neto com o site do usuario desligado; o controle confere que o PYTHONPATH e o real, "
                                                                "nao o do ataque"),
                  ("RUN_1a_pre_selo_b1_nos_real", "A4: isolado() exige -E -P -s, o lancador pinado e APPDATA vazio por teste (o run foi refeito)"),
                  ("RUN_1b_pre_selo_b2_nos_copia", "A4: idem"),
                  ("RUN_2_pos_selo_aplicar_b2", "A4: idem; e o T17 pelo contrato KERNEL_RECIBO_R3_1 com o CRITERIOS pinado")):
    if x in nomes:
        MUDARAM.setdefault(x, []).append(motivo)
MUDARAM_R35 = {}
for x_ in sorted(set(INJETADOS_NOS)):
    if x_ in R34_NOMES:
        MUDARAM_R35.setdefault(x_, []).append("R3.5: o comando ganhou --nos <stand-in v393 da custodia (nos_real/)>: o Nos REAL esta no meio do rito da v394 (um.py v394 instalado, selo v393) e nao se le; antes o "
                                              "controle lia o Nos real por omissao; a recusa ou o veredito esperado nao mudou")
for x_, motivo_ in (("A2_B1_replay_prefixo_sandbox_aplicar_b1", "R3.5: a Bancada e b1real (o manifesto pina o caminho REAL do Nos; --nos = stand-in): a guarda A2 recusa antes de qualquer conteudo do Nos importar"),
                    ("A2_B1_replay_juncao_sandbox_aplicar_b1", "R3.5: idem (a juncao aponta b1real)"),
                    ("A2_sandbox_em_copia_que_pina_o_nos_real_ensaio", "R3.5: idem"),
                    ("RUN_1a_pre_selo_b1_nos_real", "R3.5: contra o stand-in v393 da custodia (nos_real/), nao o Nos real; manifesto_anterior.pina_o_nos_real e false"),
                    ("R34_P_run_1a_T12_repinado_so_o_pino_do_um_py_e_o_resto_identico_ao_arquivado", "R3.5: o pino do um.py do pre-registro agora difere tambem em .path (o stand-in nao esta no caminho real do Nos)"),
                    ("R34_P_driver_sozinho_contraprova_passa_com_o_pino_certo", "R3.5: idem"),
                    ("R34_P_bateria_gerada_para_o_nos_real_pina_a_versao_instalada", "R3.5: o Nos 'real' v393 e o stand-in da custodia (os pinos do stand-in sao os do Nos v393 antes da instalacao da v394)"),
                    ("R34_P_gerador_e_determinista_mesma_entrada_mesma_bateria", "R3.5: idem"),
                    ("R34_S_cadeia_real_confere_com_a_producao_e_o_nos_reais", "R3.5: o fim da cadeia e o stand-in v393 (custodia) no lugar do Nos real, que ja e o v394 em instalacao; a producao e a real (so lida)"),
                    ("R34_S_o_selo_nao_pina_o_selo_anterior_medido", "R3.5: medido no selo v393 da custodia (nos_real/), que e o selo real da v393"),
                    ("R34_M_varredura_aceita_import_open_print_axioms_e_run_cmd", "R3.5: o import da amostra passa a ser TGLExt.B (a lista de permissao so admite Lean/TGLExt/TGL)"),
                    ("R34_M_varredura_palavras_dentro_de_nome_nao_sao_a_palavra", "R3.5: INVERTIDO: na lista de PERMISSAO um local fora da lista e recusado (antes, a lista de proibicao aceitava `defaults`, `instances`, `theorem_count`)"),
                    ("R34_M_varredura_CRLF_e_tab", "R3.5: o import da amostra passa a ser `import Lean`")):
    if x_ in R34_NOMES:
        MUDARAM_R35.setdefault(x_, []).append(motivo_)
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.5 (19/10/2026)", raiz=str(RAIZ), script_sha256=sha(SYNC), bateria_sha256=BAT_SHA,
           interpretador_deste_script=dict(isolated=bool(sys.flags.isolated), dont_write_bytecode=bool(sys.flags.dont_write_bytecode), utf8_mode=bool(sys.flags.utf8_mode)),
           n_da_R3_4=len(R34_NOMES), da_R3_4_presentes=len(R34_NOMES) - len(faltam_r34), da_R3_4_ausentes=faltam_r34, n_novos_R3_5=len(NOVOS_R35), novos_R3_5=NOVOS_R35,
           controles_da_R3_4_que_mudaram_de_formato=[dict(controle=k_, motivos=v_) for k_, v_ in sorted(MUDARAM_R35.items())], n_controles_da_R3_4_que_mudaram_de_formato=len(MUDARAM_R35),
           n_da_R3_3=len(R33_NOMES), da_R3_3_presentes=len(R33_NOMES) - len(faltam_r33), da_R3_3_ausentes=faltam_r33, n_novos_R3_4=len(NOVOS_R34), novos_R3_4=NOVOS_R34,
           controles_da_R3_3_que_mudaram_de_formato=[dict(controle=k_, motivos=v_) for k_, v_ in sorted(MUDARAM_R34.items())], n_controles_da_R3_3_que_mudaram_de_formato=len(MUDARAM_R34),
           gerar_bateria_sha256=sha(GEN_BAT), driver_t12_sha256=sha(DRV_BAT), gerar_cadeia_sha256=sha(GERAR_CADEIA), sandbox_manifest_sha256=sha(RAIZ / "SANDBOX_MANIFEST_R3_5.json"),
           n_da_R3_2=len(R32_NOMES), da_R3_2_presentes=len(R32_NOMES) - len(faltam_r32), da_R3_2_ausentes=faltam_r32, n_novos_R3_3=len(NOVOS_R33), novos_R3_3=NOVOS_R33,
           n_da_R3_1=len(R31_NOMES), da_R3_1_presentes=len(R31_NOMES) - len(faltam_r31), da_R3_1_ausentes=faltam_r31, n_novos_R3_2=len(NOVOS_R32), novos_R3_2=NOVOS_R32,
           controles_da_R3_1_que_mudaram_de_formato=[dict(controle=k_, motivos=v_) for k_, v_ in sorted(MUDARAM_R32.items())],
           n_controles_da_R3_1_que_mudaram_de_formato=len(MUDARAM_R32), mudancas_gerais_R3_2=GERAIS_R32,
           custodia_v391_do_sandbox=dict(selo=_pinar(SELO_ANT), kernel_manifest=_pinar(KMAN_ANT)),
           gerar_canais_sha256=sha(GER), montar_sandbox_sha256=sha(AQUI / "montar_sandbox.py"), controles_sha256=sha(Path(__file__)), segundos=round(time.time() - T0, 1),
           criterios_sintetico=dict(path=str(CRIT), sha256=CRIT_SHA), criterios_modelo=dict(path=str(CRIT_MODELO), sha256=sha(CRIT_MODELO)),
           amostra_real_do_sorry=AMOSTRA, site_do_usuario_real=SITE_REAL, lancador_sha256=MOD.LANCADOR_SHA256,
           n=len(RES), passam=n_pass, n_da_R3=len(R3_NOMES), da_R3_presentes=len(R3_NOMES) - len(faltam_r3), da_R3_ausentes=faltam_r3, n_novos_R3_1=len(NOVOS),
           novos_R3_1=NOVOS, controles_da_R3_que_mudaram_de_formato=[dict(controle=k, motivos=v) for k, v in sorted(MUDARAM.items())],
           n_controles_da_R3_que_mudaram_de_formato=len(MUDARAM),
           producao_intocada=dict(lista_igual=True, manifesto_sha256=sha(PROD / "canonical_contracts.json")), nos_real_so_lido=NOS_REAL_REGISTRO, eventos_jsonl_real_sha256=EV_REAL_SHA_ANTES,
           eventos_jsonl_real=dict(sha256_antes=EV_REAL_SHA_ANTES, sha256_depois=sha_b(EV_REAL_BYTES_DEPOIS), so_cresceu=True, linhas_antes=EV_N_ANTES, linhas_depois=EV_N_DEPOIS,
                                   elos_novos_de_outras_sessoes=[dict(seq=e.get("seq"), tipo=e.get("tipo"), quem=e.get("quem")) for e in EV_NOVOS],
                                   nota="o livro e vivo; este script nunca o abre para escrita; confere-se que so cresceu (prefixo de bytes) e que nenhum elo de sincronizacao nasceu"),
           juncoes_criadas=[str(jj) for jj in JUNCOES], juncoes_restantes=juncoes_restantes,
           controles=RES, veredito=("TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" if n_pass == len(RES) and not faltam_r3 and not faltam_r31 and not faltam_r32 and not faltam_r33 and not faltam_r34 and not juncoes_restantes
                                    else "ALGUM_CONTROLE_NAO_RECUSOU"),
           nota="NOT_FALSIFIED nunca e creditacao; nada aqui move o gate; nenhum dado observado; a producao, o Nos e o livro de eventos real foram so lidos (do Nos, alem "
                "da copia do sandbox, um log do bancada_corpus como amostra real do aviso de sorry); a producao foi simulada por decoy EM PROCESSO numa copia (pd/)")
texto = json.dumps(out, ensure_ascii=False, indent=1, default=str)
assert not MOD.contem_palavra(texto), "a palavra guardada apareceu no resultado dos controles"
(AQUI / "CONTROLES_NEGATIVOS_R3_5.json").write_bytes(texto.encode("utf-8"))
print(out["veredito"], "%d/%d" % (n_pass, len(RES)), "R3.1 presentes %d/%d" % (out["da_R3_1_presentes"], len(R31_NOMES)), "R3 presentes %d/%d" % (out["da_R3_presentes"], len(R3_NOMES)),
      "R3.2 presentes %d/%d" % (out["da_R3_2_presentes"], len(R32_NOMES)), "R3.3 presentes %d/%d" % (out["da_R3_3_presentes"], len(R33_NOMES)), "R3.4 presentes %d/%d" % (out["da_R3_4_presentes"], len(R34_NOMES)), "novos R3.5 %d" % len(NOVOS_R35),
      "%.0f s" % out["segundos"])
