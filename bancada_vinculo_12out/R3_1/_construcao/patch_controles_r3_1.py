# -*- coding: utf-8 -*-
"""patch_controles_r3_1.py (R3.1, 13/10/2026) -- deriva controles_negativos_r3_1.py dos controles da R3 (9815086af0547a7f, copiados para
R3_1): mantem os 235 (nomes iguais), ajusta os que mudaram de formato (lista com motivo no resultado) e acrescenta os NOVOS da R3.1,
no formato REAL (a linha verbatim do aviso de sorry de um log do Nos; os ataques da reauditoria a61fad96 refeitos).
Substituicoes exatas e unicas; grava por temporario -> confere -> os.replace."""
import sys
sys.dont_write_bytecode = True
import hashlib, os
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
ALVO = AQUI / "controles_negativos_r3_1.py"
txt = ALVO.read_bytes().decode("utf-8")
assert hashlib.sha256(txt.encode("utf-8")).hexdigest().startswith("9815086af0547a7f"), "a copia nao e a R3 pinada"
TROCAS = []


def troca(velho, novo):
    TROCAS.append((velho, novo))


# ------------------------------------------------------------------ cabecalho e caminhos
troca('''"""controles_negativos_r3.py (R3, 13/10/2026) -- roda o sandbox COMPLETO''', '''"""controles_negativos_r3_1.py (R3.1, 13/10/2026) -- os 235 controles da R3 (nomes mantidos; os que mudaram de formato listados com
motivo em CONTROLES_NEGATIVOS_R3_1.json) e os NOVOS da R3.1 (prefixo R31_), um ou mais por achado da reauditoria curta a61fad96 (A1, A1b,
A2, A3, A4, N1k, N1l, N1m, N2c, N3a, N4b), no formato REAL: a linha verbatim do aviso de sorry do Lean 4.31 lida de um log do Nos
(bancada_corpus, so leitura) e os ataques do auditor refeitos. Com --kernel-recibo, todo comando recebe --criterios/--criterios-sha256
(o CRITERIOS sintetico pinado), porque o B(n) R3.1 exige os esperados pinados (A3).
Da R3: roda o sandbox COMPLETO''')
troca('''Saida: R3/CONTROLES_NEGATIVOS_R3.json e <raiz>/s/*. uso: controles_negativos_r3.py <raiz curta C:/t/vb*>"""''',
      '''Saida: R3_1/CONTROLES_NEGATIVOS_R3_1.json e <raiz>/s/*. uso: controles_negativos_r3_1.py <raiz curta C:/t/vb*>"""''')
troca('''SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R3.json").read_text(encoding="utf-8"))''',
      '''SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R3_1.json").read_text(encoding="utf-8"))
R3 = AQUI.parent / "R3"''')

# ------------------------------------------------------------------ run/inproc: injecao dos criterios (A3) registrada
troca('''def run(nome, args, rc_esp, recusa_esp=None, bancada=None, saida=None, flags=("-B", "-X", "utf8"), sync=None, veredito_esp=None, extra_ok=None, nota="",
        env_extra=None):
    """roda o esboco num subprocesso; confere rc, codigo da recusa (prefixo), veredito e que a copia nao mudou (fotografia por sha256)."""
    saida = saida or (S / nome)''', '''def run(nome, args, rc_esp, recusa_esp=None, bancada=None, saida=None, flags=("-B", "-X", "utf8"), sync=None, veredito_esp=None, extra_ok=None, nota="",
        env_extra=None, sem_criterios=False):
    """roda o esboco num subprocesso; confere rc, codigo da recusa (prefixo), veredito e que a copia nao mudou (fotografia por sha256).
    R3.1: com --kernel-recibo e sem --criterios, injeta --criterios/--criterios-sha256 (o CRITERIOS sintetico) e registra o nome."""
    args = com_criterios(nome, args, sem_criterios)
    saida = saida or (S / nome)''')
troca('''def inproc(nome, argv, rc_esp, recusa_esp=None, veredito_esp=None, patches=None, bancada=None, extra_ok=None, nota=""):
    """roda main() EM PROCESSO com atributos do modulo trocados (decoy de producao, sonda do servico simulada, bateria instrumentada).
    Nenhum argumento pode apontar para a producao real nem para o Nos real; os atributos voltam no fim."""''', '''def inproc(nome, argv, rc_esp, recusa_esp=None, veredito_esp=None, patches=None, bancada=None, extra_ok=None, nota="", sem_criterios=False):
    """roda main() EM PROCESSO com atributos do modulo trocados (decoy de producao, sonda do servico simulada, bateria instrumentada).
    Nenhum argumento pode apontar para a producao real nem para o Nos real; os atributos voltam no fim. R3.1: injecao dos criterios."""
    argv = com_criterios(nome, argv, sem_criterios)''')

# ------------------------------------------------------------------ CRITERIOS e amostra real, logo depois de carregar o modulo
troca('''spec.loader.exec_module(MOD)

PROD_LISTA_ANTES = sorted(os.listdir(PROD))''', '''spec.loader.exec_module(MOD)

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


def com_criterios(nome, args, sem_criterios=False):
    a = [str(x) for x in args]
    if not sem_criterios and "--kernel-recibo" in a and "--criterios" not in a and "--criterios-sha256" not in a:
        v_ = a[a.index("--versao") + 1] if "--versao" in a and a.index("--versao") + 1 < len(a) else "v392"
        v_ = v_ if (v_.startswith("v") and v_[1:].isdigit()) else "v392"
        p_, s_ = crit_para(v_)
        INJETADOS.append(nome)
        return a + ["--criterios", str(p_), "--criterios-sha256", s_]
    return a


PROD_LISTA_ANTES = sorted(os.listdir(PROD))''')

# ------------------------------------------------------------------ isolado(): -E -P -s e o lancador (A4)
troca('''def isolado(rec, saida):
    """N5: todo teste executado rodou com -E -P logo apos o interpretador, ambiente sem PYTHON*, cwd numa pasta vazia nova sob --saida."""
    ex = [t for t in rec["bateria_resultado"]["testes"] if t.get("comando_executado")]
    return bool(ex) and all(t["comando_executado"][1:3] == ["-E", "-P"] and Path(t["cwd"]).parent == Path(saida) / "cwd_testes" for t in ex)''',
      '''def isolado(rec, saida):
    """N5 + A4 (R3.1): todo teste executado rodou com -E -P -s logo apos o interpretador e pelo lancador pinado (sha conferido), ambiente
    sem PYTHON* herdado, APPDATA numa pasta vazia nova sob --saida, cwd numa pasta vazia nova sob --saida; o recibo traz o residuo."""
    ex = [t for t in rec["bateria_resultado"]["testes"] if t.get("comando_executado")]
    prep = rec["bateria_resultado"]["isolamento"].get("preparado") or {}
    return bool(ex) and prep.get("lancador", {}).get("sha256") == MOD.LANCADOR_SHA256 and "residuo_declarado" in prep and all(
        t["comando_executado"][1:4] == ["-E", "-P", "-s"] and any(Path(x).name == MOD.LANCADOR_NOME for x in t["comando_executado"])
        and Path(t["cwd"]).parent == Path(saida) / "cwd_testes" and Path(t["isolamento"]["appdata"]).parent == Path(saida) / "appdata_vazio"
        and t["isolamento"]["lancador_sha256"] == MOD.LANCADOR_SHA256 for t in ex)''')

# ------------------------------------------------------------------ decoy(): sem_criterios repassado
troca('''def decoy(nome, rc_esp, recusa_esp=None, veredito_esp=None, sondas=(False,), patches_extra=None, extra_ok=None, nota="", **kw):
    decoy_reset()
    patches = dict(PRODUCAO=PD, EVENTOS_QUADRO=EV_SB, servico_responde=sonda_seq(list(sondas)))
    patches.update(patches_extra or {})
    return inproc(nome, decoy_args(S / nome, **kw), rc_esp, recusa_esp, veredito_esp, patches=patches, bancada=PD, extra_ok=extra_ok, nota=nota)''',
      '''def decoy(nome, rc_esp, recusa_esp=None, veredito_esp=None, sondas=(False,), patches_extra=None, extra_ok=None, nota="", sem_criterios=False, **kw):
    decoy_reset()
    patches = dict(PRODUCAO=PD, EVENTOS_QUADRO=EV_SB, servico_responde=sonda_seq(list(sondas)))
    patches.update(patches_extra or {})
    return inproc(nome, decoy_args(S / nome, **kw), rc_esp, recusa_esp, veredito_esp, patches=patches, bancada=PD, extra_ok=extra_ok, nota=nota,
                  sem_criterios=sem_criterios)''')

# ------------------------------------------------------------------ FIX: o sorry no formato REAL; toolchain em lista
troca('''    log_com_sorry=(kfix("log_com_sorry", lambda k: k.update(build_full_log=log_fix("build_com_sorry", log_b_ok + "TGLExt/PedraSinteticaA.lean:3:8: warning: declaration uses 'sorry'\\n"))),
                   "ocorrencia(s) de sorry"),''', '''    # R3.1 (A1): o controle antigo usava o formato de aspas simples (o mesmo da regex da R3: confirmava-se a si mesmo); agora a linha e
    # a VERBATIM do aviso real do Lean 4.31 (crases), lida de um log do Nos; o de aspas fica num controle proprio
    log_com_sorry=(kfix("log_com_sorry", lambda k: k.update(build_full_log=log_fix("build_com_sorry", log_b_ok + LINHA_REAL.decode("utf-8") + "\\n"))),
                   "ocorrencia(s) de sorry"),
    log_com_sorry_aspas=(kfix("log_com_sorry_aspas", lambda k: k.update(build_full_log=log_fix("build_com_sorry_aspas", log_b_ok + "TGLExt/PedraSinteticaA.lean:3:8: warning: declaration uses 'sorry'\\n"))),
                         "ocorrencia(s) de sorry"),''')
troca('''    toolchain_diverge=(kfix("toolchain_diverge", lambda k: k["toolchain"].update(lean_version="Lean (version 4.30.0)")), "toolchain"),''',
      '''    toolchain_diverge=(kfix("toolchain_diverge", lambda k: k["toolchain"].update(lean_version=["Lean (version 4.30.0)"])), "toolchain"),   # R3.1: lista (N1m)''')
troca('''    passa_ret, det, _ = MOD.verificar_kernel_recibo(kp, "v392", NI392, sha(kp), None, True)
    _registrar(dict(controle="N1_unit_kernel_recibo_%s" % nome''', '''    passa_ret, det, _ = MOD.verificar_kernel_recibo(kp, "v392", NI392, sha(kp), None, True, CRIT_OBJ)
    _registrar(dict(controle="N1_unit_kernel_recibo_%s" % nome''')
troca('''def _unit_k(nome, esperado_ok, contem, ni=None, sha_=None, pre=None, sandbox=True, kp=K_OK, nota=""):
    passa_ret, det, _ = MOD.verificar_kernel_recibo(kp, "v392", ni or NI392, sha_, pre, sandbox)''',
      '''def _unit_k(nome, esperado_ok, contem, ni=None, sha_=None, pre=None, sandbox=True, kp=K_OK, nota=""):
    passa_ret, det, _ = MOD.verificar_kernel_recibo(kp, "v392", ni or NI392, sha_, pre, sandbox, CRIT_OBJ)''')
troca('''ni_tc = dict(NI392, kernel=dict(NI392["kernel"], lean_version="Lean (version 9.9.9)"))''',
      '''ni_tc = dict(NI392, kernel=dict(NI392["kernel"], lean_version=["Lean (version 9.9.9)"]))   # R3.1: lista (N1m)''')

# ------------------------------------------------------------------ o bloco novo do kernel (A1, A1b, A2, A3, N1k, N1l, N1m, N2c unit)
BLOCO_KERNEL = open(Path(__file__).resolve().parent / "bloco_kernel_r3_1.py.txt", encoding="utf-8").read()
troca('''_unit_k("N1_unit_manifesto_toolchain_diverge", False, "toolchain", ni=ni_tc, sha_=K_OK_SHA)
''', '''_unit_k("N1_unit_manifesto_toolchain_diverge", False, "toolchain", ni=ni_tc, sha_=K_OK_SHA)
''' + BLOCO_KERNEL)

# ------------------------------------------------------------------ N5: o teste de ambiente no formato R3.1 (A4)
ini = txt.index('amb = fixture_py("n5e", "teste_ambiente.py",')
fim = txt.index('fixture_py("n5pp", "sitecustomize.py"')
VELHO_AMB = txt[ini:fim]
NOVO_AMB = open(Path(__file__).resolve().parent / "bloco_ambiente_r3_1.py.txt", encoding="utf-8").read()
TROCAS.append((VELHO_AMB, NOVO_AMB))
troca('''    extra_ok=lambda j, r: (lambda ts: ts["T00_AMBIENTE"]["resultado"] == "PASSA" and not any(MARC.iterdir()) and
                           json.loads(Path(S / "N5_PYTHONPATH_injetado_nao_chega_ao_teste" / "recibos" / "T00_AMBIENTE.json").read_text(encoding="utf-8"))["cwd"].startswith(
                               str(S / "N5_PYTHONPATH_injetado_nao_chega_ao_teste" / "cwd_testes")))(testes(j)),''',
      '''    extra_ok=lambda j, r: (lambda ts, amb_: ts["T00_AMBIENTE"]["resultado"] == "PASSA" and not any(MARC.iterdir()) and
                           amb_["cwd"].startswith(str(S / "N5_PYTHONPATH_injetado_nao_chega_ao_teste" / "cwd_testes")) and
                           amb_["pythonpath"] == SITE_REAL and amb_["neto"].get("pythonpath") == SITE_REAL)(
        testes(j), json.loads(Path(S / "N5_PYTHONPATH_injetado_nao_chega_ao_teste" / "recibos" / "T00_AMBIENTE.json").read_text(encoding="utf-8"))),''')

# ------------------------------------------------------------------ A4: os controles novos, depois do N16 e antes do N14
BLOCO_A4 = open(Path(__file__).resolve().parent / "bloco_a4_r3_1.py.txt", encoding="utf-8").read()
troca('''# --- N14: a palavra guardada na saida de um teste e na propria bateria
''', BLOCO_A4 + '''# --- N14: a palavra guardada na saida de um teste e na propria bateria
''')

# ------------------------------------------------------------------ N3a: o controle antigo muda de codigo; os novos do decoy (N2c, N3a, N4b, A1, A3)
troca('''decoy("N3_decoy_servico_volta_antes_do_recibo_em_estado", 2, "APLICACAO_REVERTIDA", sondas=(False, False, False, False, False, True), extra_ok=_so_backup_novo,
      nota="N3: volta depois da troca, antes do recibo em estado/: o manifesto anterior volta byte a byte (rollback) e o contrato sai")''',
      '''decoy("N3_decoy_servico_volta_antes_do_recibo_em_estado", 2, "SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO", sondas=(False, False, False, False, False, True),
      extra_ok=_so_backup_novo,
      nota="N3: volta depois da troca, antes do recibo em estado/: o manifesto anterior volta byte a byte (rollback) e o contrato sai. R3.1 (N3a): o servico "
           "segue no ar depois do rollback (a sonda simulada repete o ultimo valor): o codigo passa a ser o proprio, SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO")''')
BLOCO_DECOY = open(Path(__file__).resolve().parent / "bloco_decoy_r3_1.py.txt", encoding="utf-8").read()
troca('''decoy_reset()

# ================================================================ run 2: o elo B3 na copia b2, com TUDO pinado e encadeado''', BLOCO_DECOY + '''decoy_reset()

# ================================================================ run 2: o elo B3 na copia b2, com TUDO pinado e encadeado''')

# ------------------------------------------------------------------ N2c depois do run 2 (re-execucao sem seal_sha_pinado no manifesto)
BLOCO_POS = open(Path(__file__).resolve().parent / "bloco_pos_run2_r3_1.py.txt", encoding="utf-8").read()
troca('''run("POS_estado_final_b2_v392_ensaio",''', BLOCO_POS + '''run("POS_estado_final_b2_v392_ensaio",''')

# ------------------------------------------------------------------ o fecho: a comparacao e com os 235 da R3; a lista do que mudou
ini = txt.index('R2_NOMES = [c["controle"] for c in json.loads((R2 / "CONTROLES_NEGATIVOS_R2.json").read_bytes())["controles"]]')
fim = txt.index('print(out["veredito"]')
VELHO_FIM = txt[ini:fim]
NOVO_FIM = open(Path(__file__).resolve().parent / "bloco_fecho_r3_1.py.txt", encoding="utf-8").read()
TROCAS.append((VELHO_FIM, NOVO_FIM))
troca('''print(out["veredito"], "%d/%d" % (n_pass, len(RES)), "R2 presentes %d/%d" % (out["da_R2_presentes"], len(R2_NOMES)), "%.0f s" % out["segundos"])''',
      '''print(out["veredito"], "%d/%d" % (n_pass, len(RES)), "R3 presentes %d/%d" % (out["da_R3_presentes"], len(R3_NOMES)), "%.0f s" % out["segundos"])''')

for velho, novo in TROCAS:
    n = txt.count(velho)
    assert n == 1, "troca nao unica (%d): %r" % (n, velho[:120])
    txt = txt.replace(velho, novo, 1)
dados = txt.encode("utf-8")
compile(dados, str(ALVO), "exec")
tmp = ALVO.with_name(ALVO.name + ".tmp_patch")
with open(tmp, "xb") as f:
    f.write(dados)
assert tmp.read_bytes() == dados
os.replace(tmp, ALVO)
assert ALVO.read_bytes() == dados
print("ok", len(TROCAS), "trocas;", hashlib.sha256(dados).hexdigest()[:16], len(dados), "bytes")
