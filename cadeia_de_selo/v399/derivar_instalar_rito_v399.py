# -*- coding: utf-8 -*-
"""derivar_instalar_rito_v399.py -- DERIVA MECANICAMENTE, do rito_v398.sh FINAL (o que rodou em 23/10), o lancador do rito da v399: rito_v399.sh (a subida de versao e' v398 -> v399 e v397 -> v398, o 'anterior' da guarda do marcador;
o cabecalho descritivo e a linha do tempo esperado sao ESCRITOS para a v399, o resto e' a maquinaria inteira da v398, com as afericoes dela). Os outros scripts de instalacao/reversao/sandbox da v399 (instalar_v399.py, reverter_v399.py,
refazer_arvore_v399_pos_selo.py, refazer_sandbox_v399.sh, refazer_sandbox_v399_pos_selo.sh) sao autorais (a v399 e' um delta de UM modulo: ler o numero da lista, nunca digitar) e este script os CONFERE (ast.parse, sh -n e invariantes
por texto). O tempo esperado e' PARAMETRO lido de kernel/construir_marcas.txt. NAO executa nenhum derivado: so' ast.parse (os .py) e sh -n (os .sh). Os derivados NAO foram executados nem revistos por cetico independente.
GRAVA: DERIVACAO_v399.json (sha16 de cada molde e de cada derivado, invariantes, sintaxe, tempo). Reexecutavel: o que ja existe e muda ganha .bak_<STAMP>_c1 (backup de BYTES). Uso: python -I -B -X utf8 derivar_instalar_rito_v399.py"""
import ast, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v399 as DL  # noqa: E402
V4 = DL.V398
STAMP = time.strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
rd = lambda d, n: open(os.path.join(d, n), "rb").read().decode("utf-8")
_NJ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v399.json"), encoding="utf-8"))
assert isinstance(_NJ.get("novos"), list) and _NJ["novos"] == list(DL.STONE_RELS), "kernel_modulos_novos_v399.json tem de trazer a LISTA com a pedra Testemunho"
N_NOVOS = len(_NJ["novos"])   # LIDO da lista: nada digitado


def sobe(t):
    """v398 -> v399, v397 -> v398 (o 'anterior'), V398 -> V399, V397 -> V398, k398c -> k399c, k397 -> k398."""
    t = t.replace("v398", "@@A@@").replace("v397", "v398").replace("@@A@@", "v399")
    t = t.replace("V398", "@@B@@").replace("V397", "V398").replace("@@B@@", "V399")
    t = t.replace("k398c", "k399c").replace("k397", "k398")
    return t


def grava(nome, texto):
    p = os.path.join(HERE, nome); b = texto.encode("utf-8")
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + STAMP + "_c1"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + STAMP
    open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


def troca(t, old, new, n=1, nome=""):
    assert t.count(old) == n, ("troca", nome or old[:70], t.count(old), n)
    return t.replace(old, new)


# ----------------------------------------------------------------------------- o tempo esperado: PARAMETRO lido de kernel/construir_marcas.txt (nunca inventado)
def tempo_build():
    p = os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt")
    if not os.path.isfile(p):
        return {"estado": "a medir", "fonte": None}
    txt = open(p, encoding="utf-8", errors="replace").read()
    ep = dict((k, int(v)) for k, v in re.findall(r"^(epoch_inicio|epoch_build_fim|epoch_audit_fim)=(\d+)", txt, re.M))
    rcs = dict(re.findall(r"^(rc_build|rc_audit)=(\d+)", txt, re.M))
    r = {"fonte": p, "marcas_sha16": sha16(txt.encode("utf-8"))}
    if len(ep) == 3 and rcs.get("rc_build") == "0" and rcs.get("rc_audit") == "0":
        b = ep["epoch_build_fim"] - ep["epoch_inicio"]; a = ep["epoch_audit_fim"] - ep["epoch_build_fim"]
        r.update({"estado": "medido", "build_s": b, "audit_s": a, "passagem_s": b + a, "rito_3_passagens_min": round(3 * (b + a) / 60.0, 1)})
    else:
        r.update({"estado": "a medir"})
    return r


TEMPO = tempo_build()
assert TEMPO["estado"] == "medido", "kernel/construir_marcas.txt nao traz o fim do build e do Audit com rc 0: rode construir_kernel_v399.sh antes"
LINHA_TEMPO = ("# TEMPO ESPERADO (v399, parametro lido de kernel/construir_marcas.txt por derivar_instalar_rito_v399.py): no sandbox, 1 lake build INCREMENTAL (a v398 e a pedra nova, Testemunho, ja' estao compiladas em .lake/build, a pedra isolada; mudam a raiz TGLExt e o Audit) = %d s e 1 Audit = %d s "
               "(%d s por passagem); o rito faz 3 passagens de build + Audit (ordem de grandeza %.1f min so' de lake, fora o resto do um.py; no Nos o primeiro build compila a pedra a frio, dezenas de segundos a mais). "
               "O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato." % (TEMPO["build_s"], TEMPO["audit_s"], TEMPO["passagem_s"], TEMPO["rito_3_passagens_min"]))
CABECALHO = ["# O RITO v399 (ato da gerencia c1, 24/10/2026): roda o um.py v399 instalado no Nos -- %d modulo novo de kernel (TGLExt/Testemunho, nome PROVISORIO: quem nomeia e' o operador; o numero e' lido de kernel_modulos_novos_v399.json) materializado a partir do corpo embutido, kernel e Audit" % N_NOVOS,
             "# construidos pelo proprio um.py, os registros com FUNCAO selo_pela_propria_tecnologia_v399 (o metodo do operador, EMBUTIDO, sela o um.py AO LADO do SHA-256) e declaracao_do_operador_v399 (chamados no main, logo depois da afinacao das cordas), o SIDECAR um_absoluto_selo_acom.json (escrito depois da ultima escrita do selo) e os registros por spec novos do core v399 (cunhagens_v399, com as quatro inscricoes de 24/10; kh_n1_cobertura_v399). O QUADRO do Teste da Unica Palavra segue no topo. O PILAR QUANTICO NAO roda de novo: reaproveitado pela chave do cache (_QP_REUSE_V386",
             "# segue no um.py; TGL_RITE_CHECKPOINT DESLIGADO). Molde: rito_v398.sh herdado com as afericoes dele, trocados os nomes, o pacote (a propria pasta da cadeia v399) e a",
             "# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v399_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA."]

# ============================================================================= rito_v399.sh
src = rd(V4, "rito_v398.sh"); h_rito = sha16(src.encode("utf-8"))
L = src.split("\n")
assert L[0] == "#!/bin/sh" and L[1].startswith("# O RITO v398 (ato da gerencia c1, 23/10/2026)") and L[4].startswith("# guarda do marcador anterior: echo 1 | python um.py no Nos, stdout canonico em rodada_v398_stdout.txt"), (L[1][:60], L[4][:60])
corpo = "\n".join(L[5:])   # depois do cabecalho descritivo de 4 linhas
r = sobe(corpo)
# a linha do tempo esperado da v398 (ja' bumpada para v399 no texto) e' substituida pela medida desta cadeia
rx = re.compile(r"(?m)^# TEMPO ESPERADO \(v399,[^\n]*\n"); assert len(rx.findall(r)) == 1, "a linha TEMPO ESPERADO do molde nao e' unica"
r = rx.sub(lambda m_: LINHA_TEMPO + "\n", r)
RITO = "\n".join([L[0]] + CABECALHO) + "\n" + r
EXP_SET = 'set -- "/c/IALD/Central de Patentes/work/cadeia_de_selo/v398" "/c/IALD/Central de Patentes/work/cadeia_de_selo/v399"'
assert RITO.count(EXP_SET) == 1, "a guarda do marcador anterior nao ficou 'set -- <v398> <v399>'"
assert RITO.count('PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v399"') == 1 and "v397" not in RITO
DER = {"rito_v399.sh": RITO}

# ============================================================================= gravar e conferir
for n, tx in DER.items():
    grava(n, tx)
AUTORAIS = ["instalar_v399.py", "reverter_v399.py", "refazer_arvore_v399_pos_selo.py", "refazer_sandbox_v399.sh", "refazer_sandbox_v399_pos_selo.sh"]
TODOS = dict(DER); TODOS.update({n: open(os.path.join(HERE, n), "rb").read().decode("utf-8") for n in AUTORAIS})
sint = {}; falhas = []
for n, tx in TODOS.items():
    if n.endswith(".py"):
        ast.parse(tx); sint[n] = "ast.parse ok"
    else:
        rr = subprocess.run(["sh", "-n", os.path.join(HERE, n)], capture_output=True, text=True); sint[n] = "sh -n rc=%d %s" % (rr.returncode, rr.stderr[:200])
        if rr.returncode:
            falhas.append((n, "sh -n"))
    assert "\r" not in tx, ("CR no script", n)
# invariantes do molde que TEM de sobreviver (fail-closed, backup de bytes, temporario -> substituir, guardas) e rotulos desta versao
INV = {"instalar_v399.py": ["RECUSO: rodar sem -O", "VIGIA_OK", "o canonico nao e a v398 selada", "open(b, \"wb\").write(data); assert open(b, \"rb\").read() == data", "os.replace(tmp, um)", "tmp = um + \".tmp_instalar_v399_\" + ts",
                            "pilar_anterior_v398_", "APLICADO_AO_CANONICO_%s.json", "ESPERADOS_v399.json", "CANDIDATO_v399.json", "um_v399_candidato.py", "kernel_modulos_novos_v399.json", "PINO_RECIBO_PRE_SELO_v399.json",
                            "utilizavel_como_recibo_pre_selo_do_B_n", "NOVOS_V399", "modulos_novos_v399", "ESP[\"kernel\"][\"modulos_novos\"]", "len(NOVOS_V399)"],
       "reverter_v399.py": ["APLICADO_AO_CANONICO_*.json", "backup ausente ou alterado", "quarentena_pedras_", "tentativa_v399_rito_falhou_", "RECIBO_REVERSAO_", "rodada_v399_stdout.txt", "ESPERADOS_v399.json", "ANCORA", "ESPERADOS_v398.json", "set(_lista) == set(esp[\"pedras_sha256\"])", "modulos_novos_v399"],
       "rito_v399.sh": [EXP_SET, 'PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v399"', "exit 18", "exit 16", "exit 17", "exit 10", "exit 11", "exit 12", "rodada_v399_stdout.txt", "RITO_RC=", ".rito_v399.pid", "rito_servidor_v399.log", "ESPERADOS_v399.json",
                        "echo 1 | python um.py", "trap 'religar; rm -f", "TEMPO ESPERADO (v399", "kernel_modulos_novos_v399.json"],
       "refazer_arvore_v399_pos_selo.py": ["KERNEL_RECIBO_v399.json", r'ARV = r"C:\t\k399c\arvore"', "shutil.rmtree(ARV)", "assert os.path.normpath(R[\"arvore\"]) == os.path.normpath(ARV)", "chk(\"links\", links, [])"],
       "refazer_sandbox_v399.sh": ["/c/t/k399c", r"C:\t\k399c\final", "preparar_kernel_v399.py gerar", "construir_kernel_v399.sh", "pos_build_kernel_v399.py", "robocopy"],
       "refazer_sandbox_v399_pos_selo.sh": ["refazer_arvore_v399_pos_selo.py"]}
conf = {}
for n, lst in INV.items():
    tx = TODOS[n]; conf[n] = {}
    for x in lst:
        ok = x in tx; conf[n][x[:90]] = ok
        if not ok:
            falhas.append((n, x[:90]))
# rotulos: nenhum resto de v393/k393/k398d onde o sentido e' 'esta versao'; v398 so' como a versao ANTERIOR
for n, tx in TODOS.items():
    tx2 = tx.replace("ESPERADOS_v398.json", "").replace("cadeia_de_selo/v398", "").replace("cadeia_de_selo\\v398", "")   # as referencias legitimas a versao ANTERIOR (a ancora e a guarda do marcador)
    tx2 = re.sub(r"Molde: [A-Za-z0-9_\.]+_v398\.(?:py|sh)", "", tx2)   # a linha 'Molde:' cita o arquivo da versao anterior de que este deriva
    m_ = re.findall(r"(?<![A-Za-z0-9])(?:rito|instalar|reverter|ESPERADOS|CANDIDATO|rodada|tentativa)_v398[A-Za-z0-9_\.]*", tx2)
    if m_:
        falhas.append((n, "rotulo da versao ANTERIOR onde devia estar a v399: %s" % sorted(set(m_))[:4]))
    for tok in ("k398d", "k397", "work398", "v397"):
        if tok in tx:
            falhas.append((n, "resto de " + tok))
DERJ = {"molde": {"rito_v398.sh": h_rito}, "derivados": {n: sha16(DER[n].encode("utf-8")) for n in DER}, "autorais": {n: sha16(TODOS[n].encode("utf-8")) for n in AUTORAIS},
        "sobe": "v398 -> v399, v397 -> v398 (anterior), V398 -> V399, V397 -> V398, k398c -> k399c, k397 -> k398; o cabecalho descritivo de 4 linhas e a linha TEMPO ESPERADO sao ESCRITOS para a v399",
        "tempo_build": TEMPO, "n_modulos_novos_da_lista": N_NOVOS, "invariantes": conf, "sintaxe": sint, "falhas": falhas,
        "nao_validado": "nenhum derivado foi EXECUTADO nem revisto por cetico independente; so' ast.parse, sh -n, invariantes e rotulos por texto; a execucao exige ESPERADOS_v399.json, CANDIDATO_v399.json, um_v399_candidato.py e PINO_RECIBO_PRE_SELO_v399.json"}
grava("DERIVACAO_v399.json", json.dumps(DERJ, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DERJ["derivados"][n]) for n in DER), "| AUTORAIS:", ", ".join("%s %s" % (n, DERJ["autorais"][n]) for n in AUTORAIS))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("TEMPO:", json.dumps(TEMPO, ensure_ascii=False))
print("INVARIANTES:", sum(len(x) for x in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)
