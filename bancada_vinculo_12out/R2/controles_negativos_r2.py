# -*- coding: utf-8 -*-
"""controles_negativos_r2.py (R2, 13/10/2026) -- roda o sandbox COMPLETO do vinculo em raiz curta e TODOS os controles negativos:
os 7 da R1 (C1-C7) e os novos, um por achado da auditoria (A1-A13), cada um com a recusa esperada e a prova de que nada foi gravado
na Bancada-copia. Sequencia (tudo dentro de <raiz>, ex. C:\\t\\vb; a producao e o Nos sao SO lidos):
  run 1a  pre_selo ensaio, Bancada b1 (manifesto pina o Nos REAL), Nos real v391 -- a bateria inteira (T16 em raiz curta, T12-T14)
  run 1b  pre_selo ensaio, Bancada b2 (manifesto pina nos\\, copia do Nos v391) -- o recibo pre-selo que o B3 do sandbox encadeia
  controles ANTES do selo (b1/b2 em v391): C1 C2 C3 C4 C5 C6, A2, A5, A7, A8, A9, A10, A11 (unitario), A4 (unitario), A13
  o "selo" do sandbox: nos\\ recebe os bytes de nos_v392\\ (o que o rito faz no caminho pinado)
  controles DEPOIS do selo (b2 em PIN_CHANGED): C7, A1 (recibos invalidos), A3, A4 (subprocesso), A6
  run 2   pos_selo aplicar --sandbox, Bancada b2, evento ENCADEADO 707 do livro de ensaio, recibo pre-selo do run 1b, recibo do kernel
          sintetico valido, bateria pinada por sha256 -- o re-pino B3 na copia
  depois: re-execucao (idempotencia), estado final de b2 conferido
Saida: R2\\CONTROLES_NEGATIVOS_R2.json e <raiz>\\s\\*. uso: controles_negativos_r2.py <raiz curta>"""
import sys
sys.dont_write_bytecode = True
import datetime, hashlib, importlib.util, json, os, shutil, subprocess, time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = Path(sys.argv[1]).resolve()
assert str(RAIZ).lower().startswith("c:\\t\\"), "raiz curta obrigatoria"
PY = sys.executable
SYNC = AQUI / "sincronizar_bancada.py"
BAT = AQUI / "BATERIA_VINCULO.json"
PROD = Path(r"C:\IALD\Bancada_Um")
NOS_REAL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
EVENTOS_REAL = Path(r"C:\IALD\PROGRAMA_IALD\eventos.jsonl")
B1, B2, NOS, NOS392, FX, S = RAIZ / "b1", RAIZ / "b2", RAIZ / "nos", RAIZ / "nos_v392", RAIZ / "fx", RAIZ / "s"
SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R2.json").read_text(encoding="utf-8"))
ELOS = SBM["fx"]["elos_de_ensaio"]
EV_SB = FX / "eventos_sandbox.jsonl"
S.mkdir(exist_ok=True)
T0 = time.time()
RES = []


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha(p):
    return sha_b(Path(p).read_bytes())


def sha_teste(t):
    return sha_b(json.dumps(t, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def foto(bancada):
    """fotografia por sha256 de todos os arquivos da Bancada-copia (prova de 'nada gravado')."""
    bancada = Path(bancada)
    return {str(p.relative_to(bancada)): sha(p) for p in sorted(bancada.rglob("*")) if p.is_file()}


def mini_bateria(nome, ids=("T01_IDENTIDADE", "T15_SONDAS", "T17_LEAN_KERNEL"), extra=(), mutar=None, manter_copias=True):
    """uma bateria derivada da R2 com o subconjunto de testes dado (+ extras), pinada por teste; devolve (path, sha256)."""
    b = json.loads(BAT.read_bytes())
    b["testes"] = [t for t in b["testes"] if t["id"] in ids] + list(extra)
    if not manter_copias:
        b["copias"] = []
    if mutar:
        mutar(b)
    b["testes_sha256"] = {t["id"]: sha_teste(t) for t in b["testes"]}
    b["versao_bateria"] = "VINCULO-13out-R2-controle-" + nome
    p = FX / ("BT_%s.json" % nome)
    p.write_bytes(json.dumps(b, ensure_ascii=False, indent=1).encode("utf-8"))
    return p, sha(p)


def run(nome, args, rc_esp, recusa_esp=None, bancada=None, saida=None, flags=("-B", "-X", "utf8"), sync=None, veredito_esp=None, extra_ok=None, nota=""):
    """roda o esboco; confere rc, codigo da recusa (prefixo) e que a Bancada-copia nao mudou (fotografia por sha256)."""
    saida = saida or (S / nome)
    cmd = [PY, *flags, str(sync or SYNC), "--saida", str(saida)] + [str(x) for x in args]
    antes = foto(bancada) if bancada else None
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    depois = foto(bancada) if bancada else None
    ult = (r.stdout.strip().splitlines() or [""])[-1]
    try:
        j = json.loads(ult)
    except ValueError:
        j = dict(veredito=None, recusa=None, bruto=ult[:400], stderr=r.stderr[-800:])
    intocada = (antes == depois) if bancada else None
    ok = (r.returncode == rc_esp) and (recusa_esp is None or str(j.get("recusa") or "").startswith(recusa_esp)) \
        and (veredito_esp is None or str(j.get("veredito") or "").startswith(veredito_esp)) and (intocada in (True, None))
    extra = None
    if extra_ok is not None:
        try:
            extra = extra_ok(j, r)
        except Exception as exc:   # a prova extra falhou de forma visivel
            extra = "EXCECAO: %r" % (exc,)
        ok = ok and extra is True
    d = dict(controle=nome, nota=nota, comando=[str(x) for x in args], flags=list(flags), rc=r.returncode, rc_esperado=rc_esp, recusa=j.get("recusa"),
             recusa_esperada=recusa_esp, veredito=j.get("veredito"), veredito_esperado=veredito_esp, recibo=j.get("recibo"), recibo_sha256=j.get("recibo_sha256"),
             bancada_copia=str(bancada) if bancada else None, bancada_copia_intocada=intocada, prova_extra=extra, passa=ok)
    if not ok and j.get("bruto") is not None:
        d["bruto"] = j
    RES.append(d)
    print(("PASSA" if ok else "FALHA"), nome, "rc=%s" % r.returncode, (j.get("recusa") or j.get("veredito") or j.get("bruto") or "")[:150], flush=True)
    return d, j


def unit(nome, fn, recusa_esp=None, nota=""):
    """controle unitario: importa o esboco como modulo e chama a funcao; recusa esperada por prefixo (ou None = tem de aceitar)."""
    try:
        r = fn()
        ok = recusa_esp is None
        d = dict(controle=nome, nota=nota, nivel="unitario", aceito=True, retorno=(r if isinstance(r, (dict, str, int, float, bool, type(None))) else str(r)), recusa_esperada=recusa_esp, passa=ok)
    except MOD.Recusa as exc:
        ok = recusa_esp is not None and str(exc).startswith(recusa_esp)
        d = dict(controle=nome, nota=nota, nivel="unitario", aceito=False, recusa=str(exc)[:300], recusa_esperada=recusa_esp, passa=ok)
    RES.append(d)
    print(("PASSA" if ok else "FALHA"), nome, d.get("recusa") or "ACEITO", flush=True)
    return d


spec = importlib.util.spec_from_file_location("sync_r2", SYNC)
MOD = importlib.util.module_from_spec(spec)
sys.modules["sync_r2"] = MOD
spec.loader.exec_module(MOD)

PROD_LISTA_ANTES = sorted(os.listdir(PROD))
NOS_LISTA_ANTES = sorted(os.listdir(NOS_REAL))
EV_REAL_SHA_ANTES = sha(EVENTOS_REAL)

# ================================================================ run 1a e 1b (a bateria inteira, pre_selo, ensaio)
run("RUN_1a_pre_selo_b1_nos_real", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--modo", "ensaio", "--fase", "pre_selo"], 0,
    veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1, saida=S / "1a",
    extra_ok=lambda j, r: (lambda rec: rec["bateria_resultado"]["falha"] == 0 and rec["bateria_resultado"]["passa"] == 13 and
                           {t["id"]: t["resultado"] for t in rec["bateria_resultado"]["testes"]}["T16_DEPLOY_FIXTURE"] == "PASSA" and
                           {t["id"]: t["resultado"] for t in rec["bateria_resultado"]["testes"]}["T12_T13_T14_ATRATOR"] == "PASSA" and
                           rec["nos"]["um_py"]["sha256"] == SBM["nos"]["um_py"]["sha256"] and rec["manifesto_anterior"]["pina_o_nos_real"] is True)(json.loads(Path(j["recibo"]).read_bytes())),
    nota="etapa 1 da cadeia: os testes finais contra a v391 ainda canonica, Nos REAL, bateria inteira (T16 em raiz curta; T12-T14 pre-selo)")
run("RUN_1b_pre_selo_b2_nos_copia", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--modo", "ensaio", "--fase", "pre_selo"], 0,
    veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B2, saida=S / "1b",
    extra_ok=lambda j, r: (lambda rec: rec["bateria_resultado"]["falha"] == 0 and rec["bateria_resultado"]["passa"] == 13 and rec["manifesto_anterior"]["pina_o_nos_real"] is False
                           and rec["manifesto_anterior"]["nos_alvo_e_o_pinado"] is True)(json.loads(Path(j["recibo"]).read_bytes())),
    nota="o mesmo ensaio contra b2 (manifesto pina a copia do Nos): e este recibo que o B3 do sandbox encadeia por hash")
R1A = sorted((S / "1a").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
R1B = sorted((S / "1b").glob("RECIBO_SINCRONIZACAO_*.json"))[-1]
BAT_SHA = sha(BAT)

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
shutil.rmtree(drift)
run("C3_aplicar_sem_evento", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar"], 2, "EVENTO_C1_AUSENTE", bancada=B2)
run("C4_evento_real_nao_nomeia", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--modo", "aplicar", "--evento", "1",
                                  "--recibo-pre-selo", R1B], 2, "EVENTO_TIPO_INVALIDO", bancada=B2,
    nota="o evento seq 1 do quadro REAL (tipo criacao) nao nomeia a gravacao: recusado por tipo, nao por substring; o livro real e so lido")
run("C5_nos_diferente_sem_sandbox", ["--bancada", B1, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "NOS_DIFERENTE_DO_PINADO", bancada=B1)
run("C6_producao_sem_flag", ["--bancada", PROD, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "PRODUCAO_SEM_FLAG")

# --- A2: identidade da Bancada por samefile, em todas as formas de caminho (nenhuma le ou grava a producao: a guarda recusa antes)
jprod = RAIZ / "jprod"
subprocess.run(["cmd", "/c", "mklink", "/J", str(jprod), str(PROD)], capture_output=True)
jb1 = RAIZ / "jb1"
subprocess.run(["cmd", "/c", "mklink", "/J", str(jb1), str(B1)], capture_output=True)
formas_prod = {
    "prefixo_longo": "\\\\?\\" + str(PROD), "unc_localhost": "\\\\localhost\\C$" + str(PROD)[2:], "unc_127": "\\\\127.0.0.1\\C$" + str(PROD)[2:],
    "unc_host": "\\\\%s\\C$%s" % (os.environ.get("COMPUTERNAME", "localhost"), str(PROD)[2:]), "prefixo_unc": "\\\\?\\UNC\\localhost\\C$" + str(PROD)[2:],
    "prefixo_ponto": "\\\\.\\" + str(PROD), "nome_83": r"C:\IALD\BANCAD~1", "minusculas": str(PROD).lower(), "barras_normais": str(PROD).replace("\\", "/"),
    "barra_dupla_e_ponto": str(PROD).replace("\\Bancada", "\\\\Bancada") + "\\.", "unc_barras_normais": "//localhost/C$" + str(PROD)[2:].replace("\\", "/"),
    "juncao": str(jprod), "relativo_pelo_cwd": os.path.relpath(PROD, os.getcwd()),
}
for k, f in formas_prod.items():
    run("A2_producao_%s" % k, ["--bancada", f, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "PRODUCAO_SEM_FLAG",
        extra_ok=lambda j, r: j.get("recibo") is None, nota="forma %r: reconhecida como a producao por identidade; nada gravado (nem recibo)" % f)
run("A2_producao_prefixo_longo_com_producao_e_sandbox", ["--bancada", "\\\\?\\" + str(PROD), "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--producao", "--sandbox"], 2, "SANDBOX_NA_PRODUCAO")
run("A2_unc_nao_local", ["--bancada", r"\\10.255.255.1\C$\IALD\Bancada_Um", "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "CAMINHO_UNC_NAO_LOCAL")
# o ataque B1 da auditoria, refeito: copia cujo manifesto pina o Nos REAL, por prefixo \\?\, com --sandbox aplicar e evento SANDBOX:*
run("A2_B1_replay_prefixo_sandbox_aplicar_b1", ["--bancada", "\\\\?\\" + str(B1), "--versao", "v391", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar",
                                               "--fase", "pos_selo", "--evento", "SANDBOX:B1 prefixo"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1,
    nota="o ataque B1 (ALTA) da auditoria: na R1 gravou o manifesto B3 na copia; na R2 a forma do caminho e normalizada e --sandbox e recusado porque o manifesto pina o Nos real")
run("A2_B1_replay_juncao_sandbox_aplicar_b1", ["--bancada", jb1, "--versao", "v391", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar",
                                              "--fase", "pos_selo", "--evento", "SANDBOX:B1 juncao"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1)
run("A2_sandbox_em_copia_que_pina_o_nos_real_ensaio", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--sandbox"], 2, "SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL", bancada=B1)
run("A2_producao_flag_em_copia_e_aceito_sem_efeito", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--producao"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1,
    nota="--producao numa copia nao e erro (A12 da auditoria): o recibo diz producao=false", extra_ok=lambda j, r: json.loads(Path(j["recibo"]).read_bytes())["producao"] is False)

# --- A5: --saida so dentro das raizes permitidas; nunca sob a producao, o Nos ou a --bancada
def _nada_criado(caminho):
    return lambda j, r: (not Path(caminho).exists()) and j.get("recibo") is None
for k, sd, esp in (("na_producao", PROD / "estado" / "saida_A5", "SAIDA_NA_PRODUCAO"), ("no_nos", NOS_REAL / "saida_A5", "SAIDA_NO_NOS"),
                   ("dentro_da_bancada", B1 / "estado" / "saida_A5", "SAIDA_DENTRO_DA_BANCADA"), ("fora_das_raizes", Path(os.environ.get("TEMP", r"C:\Users")) / "saida_A5_R2", "SAIDA_FORA_DAS_RAIZES_PERMITIDAS"),
                   ("na_producao_por_prefixo", "\\\\?\\" + str(PROD / "estado" / "saida_A5b"), "SAIDA_NA_PRODUCAO"), ("na_producao_por_juncao", jprod / "estado" / "saida_A5c", "SAIDA_NA_PRODUCAO")):
    run("A5_saida_%s" % k, ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, esp, bancada=B1, saida=sd,
        extra_ok=_nada_criado(str(sd).replace("\\\\?\\", "")), nota="a pasta %s nao pode nascer" % sd)
assert sorted(os.listdir(PROD)) == PROD_LISTA_ANTES and sorted(os.listdir(NOS_REAL)) == NOS_LISTA_ANTES, "A5: algo nasceu na producao ou no Nos"

# --- A7: bateria pinada por sha256 (arquivo e teste) e conjunto minimo em aplicar
bt_triv, bt_triv_sha = mini_bateria("trivial", ids=(), extra=[dict(id="T00_TRIVIAL", teste="um teste trivial", fontes=[dict(path=str(SYNC), sha256=sha(SYNC), bytes=SYNC.stat().st_size)],
                                                                   comando=["{py}", "-c", "print('ok')"], cwd="{raiz}", verificacao=dict(tipo="exit0"), fases=["pre_selo", "pos_selo"],
                                                                   obrigatorio_em=["ensaio", "aplicar"], timeout_s=60)], manter_copias=False)
run("A7_bateria_trivial_em_aplicar", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_triv, "--bateria-sha256", bt_triv_sha, "--sandbox", "--modo", "aplicar",
                                      "--evento", "SANDBOX:A7"], 2, "BATERIA_MINIMA_AUSENTE", bancada=B2, nota="o ataque A7 da auditoria: na R1 um teste trivial bastava para gravar")
run("A7_bateria_sem_sha_em_aplicar", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--sandbox", "--modo", "aplicar", "--evento", "SANDBOX:A7"], 2, "BATERIA_SHA_AUSENTE", bancada=B2)
run("A7_bateria_sha_divergente", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--bateria-sha256", "0" * 64, "--sandbox", "--modo", "aplicar", "--evento", "SANDBOX:A7"], 2,
    "BATERIA_SHA_DIVERGE", bancada=B2)
def _mutar_timeout(b):
    b["testes"][0]["timeout_s"] = 1
bt_mut, bt_mut_sha = mini_bateria("teste_adulterado", mutar=_mutar_timeout)
bj = json.loads(bt_mut.read_bytes()); bj["testes"][0]["timeout_s"] = 2; bt_mut.write_bytes(json.dumps(bj, ensure_ascii=False, indent=1).encode("utf-8"))   # o teste muda DEPOIS do pino por teste
run("A7_teste_adulterado_apos_pino", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_mut, "--bateria-sha256", sha(bt_mut), "--sem-bateria"], 2, "BATERIA_TESTE_SHA_DIVERGE", bancada=B2)
bt_vinc, bt_vinc_sha = mini_bateria("marcador_vinculo", mutar=lambda b: b["testes"][0]["comando"].__setitem__(4, "{vinculo}/bateria/t01_identidade.py"))
run("A3_marcador_vinculo_proibido", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_vinc, "--bateria-sha256", bt_vinc_sha, "--sem-bateria"], 2, "MARCADOR_VINCULO_PROIBIDO", bancada=B2,
    nota="o ataque A8/A3 da auditoria: o comando que roda da pasta do esboco e recusado na carga da bateria")

# --- A8: mesma versao, hash diferente do um.py -> SELO_PROGRAMA_DIVERGE (nunca atualizar so o hash); reparo so em aplicar com evento nomeado
b1x = RAIZ / "b1x"
shutil.copytree(B1, b1x)
mx = json.loads((b1x / "canonical_contracts.json").read_bytes())
mx["canonical"]["script"]["sha256"] = "1" * 64
(b1x / "canonical_contracts.json").write_bytes(json.dumps(mx, ensure_ascii=False, indent=1).encode("utf-8"))
run("A8_mesma_versao_hash_diferente", ["--bancada", b1x, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "SELO_PROGRAMA_DIVERGE", bancada=b1x,
    nota="o ataque A5 da auditoria: manifesto v391 com outro sha do um.py; o disco tem a v391 real; na R1 re-pinava a mesma versao")
run("A8_reparo_em_ensaio_recusado", ["--bancada", b1x, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--reparo-de-pino"], 2, "REPARO_SO_EM_APLICAR", bancada=b1x)
shutil.rmtree(b1x)
b2x = RAIZ / "b2x"
shutil.copytree(B2, b2x)
mx = json.loads((b2x / "canonical_contracts.json").read_bytes())
mx["canonical"]["script"]["sha256"] = "1" * 64
(b2x / "canonical_contracts.json").write_bytes(json.dumps(mx, ensure_ascii=False, indent=1).encode("utf-8"))
# um livro de ensaio com um elo de reparo ENCADEADO que nomeia b2x (o livro real segue intocado)
linhas = [l for l in EV_SB.read_text(encoding="utf-8").splitlines() if l.strip()]
ult = json.loads(linhas[-1])
def elo(prev, tipo, quem, dados):
    e = {"seq": prev["seq"] + 1, "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "tipo": tipo, "quem": quem, "dados": dados, "anterior": prev["hash"]}
    e["hash"] = sha_b(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8"))
    return e
nos_um_sha = sha(NOS / "um.py"); nos_selo_sha = sha(NOS / "um_absoluto_selo.json")
e_rep = elo(ult, "SINCRONIZACAO_BANCADA", "claude-c1", dict(versao="v391", bancada=str(b2x), acao="sincronizacao", um_py=nos_um_sha[:16], selo=nos_selo_sha[:16], reparo=True, nota="ENSAIO A8: reparo de pino nomeado"))
e_sem = elo(e_rep, "SINCRONIZACAO_BANCADA", "claude-c1", dict(versao="v391", bancada=str(b2x), acao="sincronizacao", um_py=nos_um_sha[:16], selo=nos_selo_sha[:16], nota="ENSAIO A8: evento SEM reparo"))
ev_rep = FX / "eventos_sandbox_reparo.jsonl"
ev_rep.write_text("\n".join(linhas + [json.dumps(e_rep, ensure_ascii=False), json.dumps(e_sem, ensure_ascii=False)]) + "\n", encoding="utf-8")
bt_min_pre, bt_min_pre_sha = mini_bateria("minima_pre_selo", ids=("T01_IDENTIDADE", "T15_SONDAS"))
run("A8_reparo_com_evento_sem_dados_reparo", ["--bancada", b2x, "--nos", NOS, "--versao", "v391", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--sandbox", "--modo", "aplicar", "--fase", "pre_selo",
                                              "--reparo-de-pino", "--evento", str(e_sem["seq"]), "--eventos", ev_rep], 2, "EVENTO_NAO_AUTORIZA_REPARO", bancada=b2x)
d, j = run("A8_reparo_nomeado_em_evento_aplica", ["--bancada", b2x, "--nos", NOS, "--versao", "v391", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--sandbox", "--modo", "aplicar", "--fase", "pre_selo",
                                                 "--reparo-de-pino", "--evento", str(e_rep["seq"]), "--eventos", ev_rep], 0, veredito_esp="REPINADA_B3__APLICADA",
           extra_ok=lambda j, r: json.loads((b2x / "canonical_contracts.json").read_bytes())["canonical"]["script"]["sha256"] == nos_um_sha and
                                 json.loads(Path(j["recibo"]).read_bytes())["reparo_de_pino_autorizado_por"] == e_rep["seq"],
           nota="o unico caminho admitido para a mesma versao com outro hash: --reparo-de-pino em aplicar, evento c1 encadeado com dados.reparo=true (livro de ensaio; o real intocado)")
shutil.rmtree(b2x)

# --- A9: sem -B, nenhum __pycache__ nasce na Bancada-copia
run("A9_sem_B_nenhum_pycache", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B1, flags=("-X", "utf8"),
    extra_ok=lambda j, r: not any(p.name == "__pycache__" for p in B1.rglob("__pycache__")) and json.loads(Path(j["recibo"]).read_bytes())["python_dont_write_bytecode"] is True,
    nota="o ataque B3 da auditoria: na R1 nascia bancada\\__pycache__\\canonical.*.pyc; na R2 sys.dont_write_bytecode=True no topo")

# --- A10: traversal em code[].path e em copias[].para
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
    nota="o ataque A1 da auditoria: code[].path com '..' escapava de --saida no staging; o canonical.py instalado aceita a entrada, o esboco agora nao")
run("A10_traversal_em_code_path_ja_sincronizada", ["--bancada", b1t, "--versao", "v391", "--bateria", BAT, "--sem-bateria"], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=b1t)
shutil.rmtree(b1t)
bt_cop, bt_cop_sha = mini_bateria("copia_traversal", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["copias"].__setitem__(0, dict(b["copias"][0], para="..\\x_A10.py")))
run("A10_traversal_em_copias_para", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_cop, "--bateria-sha256", bt_cop_sha], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=B2,
    extra_ok=lambda j, r: not (S / "x_A10.py").exists(), nota="o ataque A9 da auditoria: copias[].para com '..' saia de --saida")
bt_abs, bt_abs_sha = mini_bateria("copia_absoluta", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["copias"].__setitem__(0, dict(b["copias"][0], para=str(RAIZ / "fora" / "x_abs_A10.py"))))
run("A10_copia_absoluta", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", bt_abs, "--bateria-sha256", bt_abs_sha], 2, "CAMINHO_RELATIVO_INVALIDO", bancada=B2,
    extra_ok=lambda j, r: not (RAIZ / "fora" / "x_abs_A10.py").exists())

# --- A11 (unitario): UM_VERSION unica na coluna 0; alpha e UM_VERSION sem reatribuicao indentada; o Nos v391 real passa (RUN_1a)
import math
def nos_minusculo(nome, texto):
    d = FX / ("nos_" + nome)
    d.mkdir(exist_ok=True)
    um = texto.encode("utf-8")
    alpha = 7.2973525693e-3
    core = json.dumps(dict(core=dict(beta=alpha * math.sqrt(math.e), qg_closure_verdict="ENSAIO"))).encode("utf-8")
    selo = json.dumps(dict(um_version="v999", sha256={"um.py": sha_b(um), "um_absoluto.json": sha_b(core)})).encode("utf-8")
    (d / "um.py").write_bytes(um); (d / "um_absoluto_selo.json").write_bytes(selo); (d / "um_absoluto.json").write_bytes(core)
    return d
BASE = 'UM_VERSION = "v999"\nALPHA_FINE_CODATA_2018 = 7.2973525693e-3\nx = 1\n'
unit("A11_nos_minusculo_limpo_aceito", lambda: MOD.ler_nos(nos_minusculo("limpo", BASE), "v999")["UM_VERSION"], None, nota="fixture minima: uma linha de cada na coluna 0 -> aceito")
unit("A11_segunda_UM_VERSION_coluna_0", lambda: MOD.ler_nos(nos_minusculo("v_dup", BASE + 'UM_VERSION = "v998"\n'), "v999"), "UM_VERSION_LINHA_NAO_UNICA",
     nota="o ataque A6_v_dup da auditoria: na R1 o esboco lia a PRIMEIRA e o Python executaria a ULTIMA")
unit("A11_alpha_reatribuido_indentado", lambda: MOD.ler_nos(nos_minusculo("a_ind", BASE + 'def f():\n    ALPHA_FINE_CODATA_2018 = 0.5\n'), "v999"), "ALPHA_REATRIBUIDA_INDENTADA",
     nota="o ataque A6_a_ind: decisao R2 = RECUSAR (nao 'limite declarado'): medido zero reatribuicoes indentadas no um.py v391, logo a regra nao custa nada ao canonico e fecha o buraco")
unit("A11_UM_VERSION_reatribuida_indentada", lambda: MOD.ler_nos(nos_minusculo("v_ind", BASE + 'if x:\n    UM_VERSION = "v998"\n'), "v999"), "UM_VERSION_REATRIBUIDA_INDENTADA")
unit("A11_alpha_duplicado_coluna_0", lambda: MOD.ler_nos(nos_minusculo("a_dup", BASE + 'ALPHA_FINE_CODATA_2018=0.5\n'), "v999"), "ALPHA_LINHA_NAO_UNICA")
unit("A11_comparacao_nao_e_atribuicao", lambda: MOD.ler_nos(nos_minusculo("cmp", BASE + 'if x:\n    assert ALPHA_FINE_CODATA_2018 == 7.2973525693e-3\n'), "v999")["UM_VERSION"], None,
     nota="'==' nao e reatribuicao: aceito (a regex exclui '==')")

# --- A4 (unitario): o evento pela cadeia de hash, campos por JSON, negacao recusada
NI = dict(um_py=dict(sha256=sha(NOS392 / "um.py")), selo=dict(sha256=sha(NOS392 / "um_absoluto_selo.json")))
unit("A4_evento_valido_encadeado_aceito", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, EV_SB)["hash"][:16], None,
     nota="elo 707 do livro de ensaio: encadeado, c1, tipo certo, campos por JSON -> aceito (verificado=true, cadeia conferida ate o fim)")
unit("A4_F1_forjado_sem_cadeia", lambda: MOD.verificar_evento("90001", "v392", B2, True, NI, False, FX / "eventos_forjado_sem_cadeia.jsonl"), "EVENTOS_CADEIA_QUEBRADA",
     nota="o ataque A4-F1 da auditoria: evento c1 completo, sem encadear -> na R1 ACEITO; na R2 a cadeia quebra e nada se le dele")
unit("A4_F6_seq_duplicado_encadeado", lambda: MOD.verificar_evento(str(ELOS["valido"]["seq"]), "v392", B2, True, NI, False, FX / "eventos_forjado_seq_duplicado.jsonl"), "EVENTO_SEQ_DUPLICADO")
unit("A4_F2_outra_sessao", lambda: MOD.verificar_evento(str(ELOS["outra_sessao"]["seq"]), "v392", B2, True, NI, False, EV_SB), "EVENTO_NAO_E_DA_C1")
unit("A4_F3_texto_que_nega", lambda: MOD.verificar_evento(str(ELOS["negacao"]["seq"]), "v392", B2, True, NI, False, EV_SB), "EVENTO_COM_NEGACAO",
     nota="o ataque A4-F3: um evento c1 que diz 'NAO sincronizar' e que contem as tres palavras -> na R1 ACEITO; na R2 recusado")
unit("A4_F4_hashes_de_outro_programa", lambda: MOD.verificar_evento(str(ELOS["outro_programa"]["seq"]), "v392", B2, True, NI, False, EV_SB), "EVENTO_NAO_NOMEIA_O_PROGRAMA",
     nota="o ataque A4-F4: um_py/selo de outros hashes -> na R1 ACEITO; na R2 conferidos contra o Nos lido")
unit("A4_F5_outra_versao", lambda: MOD.verificar_evento(str(ELOS["outra_versao"]["seq"]), "v392", B2, True, NI, False, EV_SB), "EVENTO_NAO_NOMEIA_A_VERSAO")
unit("A4_outra_bancada_por_identidade", lambda: MOD.verificar_evento(str(ELOS["outra_bancada"]["seq"]), "v392", B2, True, NI, False, EV_SB), "EVENTO_NAO_NOMEIA_ESTA_BANCADA")
unit("A4_tipo_errado", lambda: MOD.verificar_evento(str(ELOS["tipo_errado"]["seq"]), "v392", B2, True, NI, False, EV_SB), "EVENTO_TIPO_INVALIDO")
unit("A4_sem_acao", lambda: MOD.verificar_evento(str(ELOS["sem_acao"]["seq"]), "v392", B2, True, NI, False, EV_SB), "EVENTO_NAO_NOMEIA_A_SINCRONIZACAO")
unit("A4_F7_evento_real_706_nova_F06", lambda: MOD.verificar_evento("706", "v392", B2, True, NI, False, EV_SB), "EVENTO_TIPO_INVALIDO")
unit("A4_F8_sandbox_literal_fora_do_sandbox", lambda: MOD.verificar_evento("SANDBOX:x", "v392", B2, False, NI, False, EV_SB), "EVENTO_SANDBOX_FORA_DO_SANDBOX")
unit("A4_F10_seq_inexistente", lambda: MOD.verificar_evento("123456789", "v392", B2, True, NI, False, EV_SB), "EVENTO_NAO_ENCONTRADO")
unit("A4_F11_nao_numerico", lambda: MOD.verificar_evento("abc", "v392", B2, True, NI, False, EV_SB), "EVENTO_C1_INVALIDO")
ULT_REAL = json.loads([l for l in EVENTOS_REAL.read_text(encoding="utf-8").splitlines() if l.strip()][-1])["seq"]
unit("A4_livro_real_integro_seq_seguinte_nao_existe_nele", lambda: MOD.verificar_evento(str(ULT_REAL + 1), "v392", B2, True, NI, False, EVENTOS_REAL), "EVENTO_NAO_ENCONTRADO",
     nota="o livro REAL (so lido, %d elos no momento): a cadeia inteira e conferida e o seq seguinte nao existe nele (a recusa cita 'cadeia integra ate o elo N')" % ULT_REAL)
unit("A4_livro_real_ultimo_elo_nao_e_sincronizacao", lambda: MOD.verificar_evento(str(ULT_REAL), "v392", B2, True, NI, False, EVENTOS_REAL), "EVENTO_",
     nota="o ultimo elo real (seq %d) e de outro tipo/outra unidade: recusado por campo, nunca por substring" % ULT_REAL)
run("A4_eventos_alternativo_fora_do_sandbox", ["--bancada", B2, "--nos", NOS, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--eventos", EV_SB], 2, "EVENTOS_ALTERNATIVO_FORA_DO_SANDBOX", bancada=B2)

# --- A13: a guarda de palavra no gerador de canais, aplicada a declaracao inteira
GER = AQUI / "gerar_canais_mcp.py"
decl_limpa = AQUI.parent / "sandbox" / "CANAIS_v391_exemplo.json"
d13 = json.loads(decl_limpa.read_bytes())
d13["canais"][0]["veredito_selado"] = "TGL_X_" + "CONF" + "IRMED"
# a declaracao com o token fica SO EM RAM (a palavra recusada nunca e escrita em disco): o gerador R2 e importado e gerar() chamado direto
spec13 = importlib.util.spec_from_file_location("gerar_canais_r2", GER)
G13 = importlib.util.module_from_spec(spec13); sys.modules["gerar_canais_r2"] = G13; spec13.loader.exec_module(G13)
try:
    G13.gerar(d13, RAIZ / "canais_suja")
    msg13 = "ACEITO (inesperado)"
except SystemExit as exc:
    msg13 = str(exc)
ok13 = msg13.startswith("PALAVRA_PROIBIDA_NA_DECLARACAO") and not (RAIZ / "canais_suja").exists()
RES.append(dict(controle="A13_declaracao_com_token_recusada", nivel="unitario (em RAM)", recusa=msg13, pasta_nasceu=(RAIZ / "canais_suja").exists(), passa=ok13,
                nota="o achado A13: na R1 a declaracao com o token passava pela unica guarda e o gerador escrevia o modulo com o token na tabela CANAIS; na R2 nada nasce (nem a pasta)"))
print(("PASSA" if ok13 else "FALHA"), "A13_declaracao_com_token_recusada", msg13, flush=True)
r13b = subprocess.run([PY, "-B", "-X", "utf8", str(GER), str(decl_limpa), str(RAIZ / "canais")], capture_output=True, text=True, encoding="utf-8", errors="replace")
ger = (RAIZ / "canais" / "GERACAO_RECIBO.json")
ok13b = r13b.returncode == 0 and ger.exists() and (RAIZ / "canais" / "registros_gerados.py").exists()
RES.append(dict(controle="A13_declaracao_limpa_gera", nivel="subprocesso", rc=r13b.returncode, gerados=(json.loads(ger.read_bytes()) if ger.exists() else None), passa=ok13b,
                nota="a declaracao limpa (CANAIS_v391_exemplo.json da R1, extraida por script do um.py v391) gera os quatro arquivos"))
print(("PASSA" if ok13b else "FALHA"), "A13_declaracao_limpa_gera", flush=True)

# ================================================================ o "selo" do sandbox: nos\ recebe os bytes de nos_v392\ (o que o rito faz no caminho pinado)
for f in ("um.py", "um_absoluto_selo.json", "um_absoluto.json"):
    shutil.copyfile(NOS392 / f, NOS / f)
assert sha(NOS / "um.py") == SBM["nos_v392"]["um_py"]["sha256"]
RES.append(dict(controle="SELO_DO_SANDBOX", nivel="montagem", nos_um_py_sha256=sha(NOS / "um.py"), nos_selo_sha256=sha(NOS / "um_absoluto_selo.json"), passa=True,
                nota="nos\\ passou de v391 para o v392 sintetico no MESMO caminho pinado por b2: o canonical.py instalado em b2 deve recusar (PIN_CHANGED)"))
K_OK = FX / "KERNEL_RECIBO_v392_SINTETICO_VALIDO.json"

# ================================================================ controles DEPOIS do selo (b2 em PIN_CHANGED)
# --- C7: bateria com um teste que FALHA, em aplicar com evento sandbox: nada se grava
falha_py = FX / "falha_injetada.py"
falha_py.write_bytes(b"import sys\nprint('falha injetada')\nsys.exit(1)\n")
t_falha = dict(id="T00_FALHA_INJETADA", teste="controle: um teste que falha de proposito", fontes=[dict(path=str(falha_py), sha256=sha(falha_py), bytes=falha_py.stat().st_size)],
               comando=["{py}", "-B", "{fonte:0}"], cwd="{raiz}", verificacao=dict(tipo="exit0"), fases=["pre_selo", "pos_selo"], obrigatorio_em=["ensaio", "aplicar"], timeout_s=60)
bt_c7, bt_c7_sha = mini_bateria("C7_falha", extra=[t_falha])
run("C7_bateria_falha_em_aplicar", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_c7, "--bateria-sha256", bt_c7_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                    "--evento", "SANDBOX:controle C7", "--kernel-recibo", K_OK], 3, veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", bancada=B2,
    extra_ok=lambda j, r: not (B2 / "CONTRATO_CANONICO_B3.md").exists() and {t["id"]: t["resultado"] for t in json.loads(Path(j["recibo"]).read_bytes())["bateria_resultado"]["testes"]} ==
    {"T01_IDENTIDADE": "PASSA", "T15_SONDAS": "PASSA", "T17_LEAN_KERNEL": "PASSA", "T00_FALHA_INJETADA": "FALHA"})

# --- A1: T17 pelo recibo do kernel, sem subprocesso: valido PASSA (dentro do C7 acima e do run 2); invalidos FALHAM
bt_min, bt_min_sha = mini_bateria("minima_pos_selo")
for k in ("sorry", "versao", "log", "um_py"):
    run("A1_kernel_recibo_invalido_%s" % k, ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                            "--evento", "SANDBOX:A1", "--kernel-recibo", FX / ("KERNEL_RECIBO_INVALIDO_%s.json" % k)], 3, veredito_esp="REPINADA_B3__BATERIA_FALHOU__NADA_GRAVADO", bancada=B2,
        extra_ok=lambda j, r: (lambda ts: ts["T17_LEAN_KERNEL"]["resultado"] == "FALHA" and ts["T17_LEAN_KERNEL"].get("comando") is None and "recibo do kernel" in ts["T17_LEAN_KERNEL"]["detalhe"])
        ({t["id"]: t for t in json.loads(Path(j["recibo"]).read_bytes())["bateria_resultado"]["testes"]}),
        nota="o achado A1 (ALTA): na R1 o T17 com --kernel-recibo caia em subprocess.run('(sem comando)') -> ERRO_NAO_PREVISTO; na R2 e lido por hash, sem subprocesso")
run("A1_kernel_recibo_ausente_em_ensaio_NAO_EXECUTADO", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "ensaio",
                                                             "--fase", "pos_selo"], 0, veredito_esp="REPINADA_B3__ENSAIO", bancada=B2,
    extra_ok=lambda j, r: {t["id"]: t["resultado"] for t in json.loads(Path(j["recibo"]).read_bytes())["bateria_resultado"]["testes"]}["T17_LEAN_KERNEL"] == "NAO_EXECUTADO",
    nota="em ensaio sem recibo o T17 fica NAO_EXECUTADO com o motivo (nunca PASSA por omissao)")
bt_t17, _ = mini_bateria("so_T17", ids=("T17_LEAN_KERNEL",), manter_copias=False)
unit("A1_kernel_recibo_ausente_em_aplicar_fora_do_sandbox_FALHA",
     lambda: MOD.rodar_bateria(json.loads(bt_t17.read_bytes()), dict(py=PY, raiz=str(FX / "u"), candidate=str(FX / "u"), nos=str(NOS), versao="v392", recibos=str(FX / "u" / ("rec%d" % int(time.time()))),
                                                                   tunel="", saida=str(FX / "u"), rotulo="u", kernel_recibo=""), FX / "u" / ("rec%d" % int(time.time() * 7)), "aplicar", "pos_selo", False, None,
                               dict(um_py=dict(sha256="x"), selo=dict(sha256="y")), ())["testes"][-1]["resultado"], None,
     nota="unitario: fora do sandbox, aplicar sem --kernel-recibo -> T17 FALHA (o retorno e o resultado do T17)")
assert RES[-1]["retorno"] == "FALHA", RES[-1]
RES[-1]["passa"] = RES[-1]["retorno"] == "FALHA"

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
                           "ADULTERADO" not in Path(t01["log"]["path"]).read_text(encoding="utf-8"))({t["id"]: t for t in json.loads(Path(j["recibo"]).read_bytes())["bateria_resultado"]["testes"]}["T01_IDENTIDADE"]),
    nota="o ataque A8/A3 (ALTA) da auditoria: o esboco copiado para outra pasta com um t01 ADULTERADO ao lado; na R1 o adulterado rodava; na R2 o comando executa o caminho pinado (samefile) e o log nao traz 'ADULTERADO'")
bt_np, bt_np_sha = mini_bateria("py_nao_pinado", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["testes"][0]["comando"].__setitem__(4, str(esb / "bateria" / "t01_identidade.py")))
run("A3_comando_executa_py_nao_pinado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_np, "--bateria-sha256", bt_np_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 3,
    veredito_esp="REPINADA_B3__BATERIA_FALHOU", bancada=B2,
    extra_ok=lambda j, r: "COMANDO_EXECUTA_ARQUIVO_NAO_PINADO" in {t["id"]: t for t in json.loads(Path(j["recibo"]).read_bytes())["bateria_resultado"]["testes"]}["T01_IDENTIDADE"]["detalhe"],
    nota="um comando cujo .py nao e fonte pinada nem copia conferida e recusado ANTES de executar")
t01_fx = FX / "t01_copia_pinada.py"
shutil.copyfile(t01_real, t01_fx)
bt_fx, bt_fx_sha = mini_bateria("fonte_adulterada", ids=("T01_IDENTIDADE", "T15_SONDAS"), mutar=lambda b: b["testes"][0]["fontes"].__setitem__(0, dict(path=str(t01_fx), sha256=sha(t01_fx), bytes=t01_fx.stat().st_size)))
t01_fx.write_bytes(adult)   # a fonte pinada e adulterada DEPOIS do pino
run("A3_fonte_pinada_adulterada_antes_de_rodar", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_fx, "--bateria-sha256", bt_fx_sha, "--sandbox", "--modo", "ensaio", "--fase", "pos_selo"], 3,
    veredito_esp="REPINADA_B3__BATERIA_FALHOU", bancada=B2,
    extra_ok=lambda j, r: (lambda t01: t01["resultado"] == "FALHA" and t01["fontes"][0]["estado"] == "ALTERADA" and "comando" not in t01)({t["id"]: t for t in json.loads(Path(j["recibo"]).read_bytes())["bateria_resultado"]["testes"]}["T01_IDENTIDADE"]),
    nota="o sha256 e conferido ANTES de executar: fonte alterada = FALHA sem subprocesso")

# --- A4 (subprocesso): o evento com negacao e o evento de outro programa, no caminho real do aplicar
run("A4_sub_evento_com_negacao", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                  "--evento", str(ELOS["negacao"]["seq"]), "--eventos", EV_SB, "--kernel-recibo", K_OK], 2, "EVENTO_COM_NEGACAO", bancada=B2)
run("A4_sub_evento_forjado_sem_cadeia", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                         "--evento", "90001", "--eventos", FX / "eventos_forjado_sem_cadeia.jsonl", "--kernel-recibo", K_OK], 2, "EVENTOS_CADEIA_QUEBRADA", bancada=B2)

# --- A6: o recibo pre-selo conferido por identidade
pre_forj = FX / "PRE_forjado.json"
pre_forj.write_bytes(json.dumps(dict(fase="pre_selo", bateria_resultado=dict(veredito="BATERIA_PASSA", testes=[]), versao_alvo="v000", bancada=dict(dir="X:/outra"),
                                     nos=dict(um_py=dict(sha256="0" * 64)), veredito="JA_SINCRONIZADA__ENSAIO__FORJADO")).encode("utf-8"))
run("A6_recibo_pre_selo_forjado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                   "--evento", "SANDBOX:A6", "--kernel-recibo", K_OK, "--recibo-pre-selo", pre_forj], 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=B2,
    nota="o ataque B4 da auditoria: recibo pre-selo forjado (v000, outra bancada, outro um.py) -> na R1 ACEITO e gravou; na R2 recusado por identidade")
run("A6_recibo_pre_selo_de_outra_bancada", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                            "--evento", "SANDBOX:A6", "--kernel-recibo", K_OK, "--recibo-pre-selo", R1A], 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=B2,
    nota="o recibo REAL do run 1a (Bancada b1) usado para b2: mesma versao e mesmo um.py, mas outra Bancada por identidade -> recusado")
rj = json.loads(R1B.read_bytes()); rj["nos"]["um_py"]["sha256"] = "2" * 64
pre_mut = FX / "PRE_1b_um_py_trocado.json"; pre_mut.write_bytes(json.dumps(rj, ensure_ascii=False).encode("utf-8"))
run("A6_recibo_pre_selo_1b_com_um_py_trocado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                                "--evento", "SANDBOX:A6", "--kernel-recibo", K_OK, "--recibo-pre-selo", pre_mut], 2, "RECIBO_PRE_SELO_NAO_CORRESPONDE", bancada=B2)
run("A6_recibo_pre_selo_na_fase_pre_selo", ["--bancada", B1, "--versao", "v391", "--bateria", BAT, "--sem-bateria", "--fase", "pre_selo", "--recibo-pre-selo", R1A], 2, "RECIBO_PRE_SELO_NA_FASE_PRE_SELO", bancada=B1)
run("A6_aplicar_fora_do_sandbox_sem_recibo_pre_selo", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min, "--bateria-sha256", bt_min_sha, "--modo", "aplicar", "--fase", "pos_selo",
                                                       "--evento", "707", "--kernel-recibo", K_OK], 2, "RECIBO_PRE_SELO_AUSENTE", bancada=B2)
run("APLICAR_na_fase_pre_selo_recusado", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", bt_min_pre, "--bateria-sha256", bt_min_pre_sha, "--sandbox", "--modo", "aplicar", "--fase", "pre_selo",
                                          "--evento", "SANDBOX:x"], 2, "APLICAR_SO_NA_FASE_POS_SELO", bancada=B2)

# ================================================================ run 2: o elo B3 na copia b2, com TUDO pinado e encadeado
MAN_B2_ANTES = sha(B2 / "canonical_contracts.json")
d2, j2 = run("RUN_2_pos_selo_aplicar_b2", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                                           "--evento", str(ELOS["valido"]["seq"]), "--eventos", EV_SB, "--recibo-pre-selo", R1B, "--kernel-recibo", K_OK], 0,
             veredito_esp="REPINADA_B3__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", saida=S / "2",
             extra_ok=lambda j, r: (lambda rec: rec["bateria_resultado"]["falha"] == 0 and rec["bateria_resultado"]["passa"] == 13 and rec["bateria_resultado"]["nao_executado"] == 1 and
                                    {t["id"]: t["resultado"] for t in rec["bateria_resultado"]["testes"]}["T17_LEAN_KERNEL"] == "PASSA" and
                                    {t["id"]: t["resultado"] for t in rec["bateria_resultado"]["testes"]}["T16_DEPLOY_FIXTURE"] == "PASSA" and
                                    rec["pino_velho_recusado_pelo_instalado"] == "PIN_CHANGED" and rec["evento_c1"]["verificado"] is True and rec["evento_c1"]["evento"] == ELOS["valido"]["seq"] and
                                    rec["recibo_pre_selo"]["sha256"] == sha(R1B) and rec["manifesto_novo"]["recibo_pre_selo_sha256_encadeado"] == sha(R1B) and
                                    sha(B2 / "canonical_contracts.json") == rec["manifesto_novo"]["sha256"] and sha(rec["aplicacao"]["backup"]) == MAN_B2_ANTES and
                                    (B2 / "CONTRATO_CANONICO_B3.md").exists() and Path(rec["aplicacao"]["copia_do_recibo"]).exists() and rec["aplicacao"]["pos_conferencia"]["ok"] is True and
                                    rec["aplicacao"]["pos_conferencia"]["canonical_version"] == "v392" and rec["nos"]["beta_runtime"] == rec["aplicacao"]["pos_conferencia"]["beta_tgl"].__repr__() and
                                    not any(B2.rglob("__pycache__")))(json.loads(Path(j["recibo"]).read_bytes())),
             nota="o elo B3 do sandbox: o canonical.py instalado em b2 recusou o pino velho (PIN_CHANGED, real, sem sonda em RAM), evento 707 encadeado e verificado, recibo pre-selo do run 1b encadeado no manifesto, T17 pelo recibo do kernel, bateria 13 PASSA (T12-T14 lidos do pre-selo), manifesto B3 gravado em b2 com backup, contrato e recibo em estado\\sincronizacao")
run("RUN_2bis_idempotente", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT, "--bateria-sha256", BAT_SHA, "--sandbox", "--modo", "aplicar", "--fase", "pos_selo",
                             "--evento", str(ELOS["valido"]["seq"]), "--eventos", EV_SB, "--recibo-pre-selo", R1B, "--kernel-recibo", K_OK], 0, veredito_esp="JA_SINCRONIZADA__NADA_A_GRAVAR", bancada=B2,
    nota="repetir o B3 ja aplicado: a bateria roda de novo na copia, nada se grava (idempotencia)")
run("POS_estado_final_b2_v392_ensaio", ["--bancada", B2, "--nos", NOS, "--versao", "v392", "--bateria", BAT, "--sem-bateria"], 0, veredito_esp="JA_SINCRONIZADA__ENSAIO", bancada=B2,
    nota="estado final: b2 sincronizada em v392 (ensaio sem bateria, so leitura)")

# ================================================================ fecho: a producao, o Nos e o livro real intocados
assert sorted(os.listdir(PROD)) == PROD_LISTA_ANTES, "a lista da producao mudou"
assert sorted(os.listdir(NOS_REAL)) == NOS_LISTA_ANTES, "a lista do Nos mudou"
assert sha(EVENTOS_REAL) == EV_REAL_SHA_ANTES, "o livro real de eventos mudou"
assert sha(PROD / "canonical_contracts.json") == SBM["manifesto_producao_sha256"], "o manifesto de producao mudou"
for j in (jprod, jb1):
    if j.exists():
        os.rmdir(j)   # remover a JUNCAO (nao o alvo)
n_pass = sum(1 for x in RES if x["passa"])
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R2 (13/10/2026)", raiz=str(RAIZ), script_sha256=sha(SYNC), bateria_sha256=BAT_SHA,
           gerar_canais_sha256=sha(GER), segundos=round(time.time() - T0, 1), n=len(RES), passam=n_pass,
           producao_intocada=dict(lista_igual=True, manifesto_sha256=sha(PROD / "canonical_contracts.json")), nos_real_intocado=True, eventos_jsonl_real_sha256=EV_REAL_SHA_ANTES,
           controles=RES, veredito=("TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" if n_pass == len(RES) else "ALGUM_CONTROLE_NAO_RECUSOU"),
           nota="NOT_FALSIFIED nunca e creditacao; nada aqui move o gate; nenhum dado observado; a producao, o Nos e o livro de eventos real foram so lidos")
(AQUI / "CONTROLES_NEGATIVOS_R2.json").write_bytes(json.dumps(out, ensure_ascii=False, indent=1, default=str).encode("utf-8"))
print(out["veredito"], "%d/%d" % (n_pass, len(RES)), "%.0f s" % out["segundos"])
