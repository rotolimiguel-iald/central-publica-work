# -*- coding: utf-8 -*-
"""derivar_instalar_rito_v394.py -- DERIVA MECANICAMENTE, do molde da v393 (cadeia_de_selo/v393), os scripts de instalacao, rito, reversao e sandbox da v394:
  instalar_v394.py, rito_v394.sh, reverter_v394.py, refazer_arvore_v394_pos_selo.py, refazer_sandbox_v394.sh, refazer_sandbox_v394_pos_selo.sh (+ guarda_p18_v394.py, copia de bytes da v393 se ainda nao existir).
A subida de versao e' v393 -> v394 e v392 -> v393 (o 'anterior'); k393 -> k394; os nomes de registros historicos do core NAO sobem (lista PROT). Os poucos pontos que MUDAM de sentido sao editados com
assert de contagem (troca). NAO executa nenhum dos derivados: so' ast.parse (os .py) e sh -n (os .sh). Os derivados NAO foram executados nem revistos por cetico independente: sao atos da gerencia.
Acrescenta tambem kernel_modulos_novos_v394.lista.json (a LISTA dos 189 modulos novos, calculada por diferenca entre o sandbox C:/t/k394/final e o tgl_kernel do Nos, so' leitura) porque o campo 'novos'
de kernel_modulos_novos_v394.json (preparar_kernel_v394.py) sai como CONTAGEM (o `**info` do json.dump sobrescreve a lista): o instalar e o reverter usam a lista de la' se ela vier como lista,
senao a deste arquivo, senao ESPERADOS.pedras_sha256. O tempo esperado do rito e' PARAMETRO lido de kernel/construir_marcas.txt (a medir se ainda nao ha o fim do build).
GRAVA: DERIVACAO_v394.json (sha16 de cada molde e de cada derivado, invariantes, sintaxe, tempo). Reexecutavel: o que ja existe e muda ganha .bak_<STAMP>_c1 (backup de BYTES).
Uso: python -I -B -X utf8 derivar_instalar_rito_v394.py"""
import ast, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); CAD = os.path.dirname(HERE); V3 = os.path.join(CAD, "v393"); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402   (DELTA 19/10: sandbox k394d, logs em kernel_d19, candidato novo, pedra do delta)
STAMP = time.strftime("%Y%m%d_%H%M%S")
C = "C:" + os.sep
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
SB = DL.SANDBOX
_NJ = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))
assert isinstance(_NJ.get("novos"), list) and DL.STONE_REL in _NJ["novos"] and len(set(_NJ["novos"])) == len(_NJ["novos"]), "kernel_modulos_novos_v394.json tem de trazer a LISTA, com a pedra do delta (preparar_kernel_v394.py)"
N_NOVOS = len(_NJ["novos"])   # LIDO da lista dos modulos novos (189 do Codex + a pedra do delta de 19/10): nada digitado
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
# nomes que NAO sobem de versao (registros/chaves historicos do core e arquivos de versoes passadas)
PROT = ["varredura_e_sorry_v392", "estatuto_da_prova_v391", "fundacao_v390", "three_stress_tests_v387", "pedras_v392", "pedras_v393", "regra_consumidor_v393",
        "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "kh_n1_cobertura_v392", "axiom_coverage_v392", "KH_N1_v392", "AO_CLAUDE_INTEGRAR_REGRA_V393"]


def sobe(t):
    for i, p in enumerate(PROT):
        t = t.replace(p, "@@P%d@@" % i)
    t = t.replace("v393", "@@N@@").replace("v392", "v393").replace("@@N@@", "v394")
    t = t.replace("V393", "@@U@@").replace("V392", "V393").replace("@@U@@", "V394")
    t = t.replace("k393", "k394").replace("work393", "work394")
    for i, p in enumerate(PROT):
        t = t.replace("@@P%d@@" % i, p)
    return t


def rd(d, n):
    return open(os.path.join(d, n), "rb").read().decode("utf-8")


def troca(t, old, new, n=1, nome=""):
    assert t.count(old) == n, ("troca", nome or old[:70], t.count(old), n)
    return t.replace(old, new)


def grava(nome, texto):
    p = os.path.join(HERE, nome); b = texto.encode("utf-8")
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + STAMP + "_c1"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + STAMP
    open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b


# ----------------------------------------------------------------------------- o tempo esperado: PARAMETRO lido de kernel/construir_marcas.txt (nunca inventado)
def tempo_build():
    p = os.path.join(HERE, DL.KERNEL_DIR, "construir_marcas.txt")
    if not os.path.isfile(p):
        return {"estado": "a medir", "fonte": None}
    txt = open(p, encoding="utf-8", errors="replace").read()
    ep = dict((k, int(v)) for k, v in re.findall(r"^(epoch_inicio|epoch_build_fim|epoch_audit_fim)=(\d+)", txt, re.M))
    rcs = dict(re.findall(r"^(rc_build|rc_audit)=(\d+)", txt, re.M))
    r = {"fonte": p, "marcas_sha16": sha16(txt.encode("utf-8"))}
    if "epoch_inicio" in ep and "epoch_build_fim" in ep and "epoch_audit_fim" in ep and rcs.get("rc_build") == "0" and rcs.get("rc_audit") == "0":
        b = ep["epoch_build_fim"] - ep["epoch_inicio"]; a = ep["epoch_audit_fim"] - ep["epoch_build_fim"]
        r.update({"estado": "medido", "build_s": b, "audit_s": a, "passagem_s": b + a, "rito_3_passagens_min": round(3 * (b + a) / 60.0, 1)})
    elif "epoch_inicio" in ep and "epoch_build_fim" in ep and rcs.get("rc_build") == "0":
        r.update({"estado": "parcial", "build_s": ep["epoch_build_fim"] - ep["epoch_inicio"], "nota": "o build do sandbox terminou com rc 0; o Audit ainda nao (ou nao terminou com rc 0): Audit e total a medir"})
    elif "epoch_inicio" in ep:
        r.update({"estado": "a medir", "nota": "so' ha o inicio (ou o build nao terminou com rc 0): sem numero"})
    else:
        r.update({"estado": "a medir"})
    return r


TEMPO = tempo_build()
if TEMPO["estado"] == "medido":
    LINHA_TEMPO = ("# TEMPO ESPERADO (v394, parametro lido de kernel/construir_marcas.txt por derivar_instalar_rito_v394.py): no sandbox, 1 lake build = %d s e 1 Audit = %d s (%d s por passagem); o rito faz 3 passagens "
                   "(ordem de grandeza %.1f min so' de build+Audit, fora o resto do um.py). O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato." % (
                       TEMPO["build_s"], TEMPO["audit_s"], TEMPO["passagem_s"], TEMPO["rito_3_passagens_min"]))
elif TEMPO["estado"] == "parcial":
    LINHA_TEMPO = ("# TEMPO ESPERADO (v394, parametro lido de kernel/construir_marcas.txt por derivar_instalar_rito_v394.py): no sandbox, 1 lake build (frio nos modulos novos) = %d s; o Audit e o total do rito: a medir "
                   "(rederivar quando kernel/construir_marcas.txt trouxer o fim do Audit). O rito faz 3 passagens de lake build + Audit; o timeout do lake build DENTRO do um.py (candidato) tem de caber no tempo medido." % TEMPO["build_s"])
else:
    LINHA_TEMPO = ("# TEMPO ESPERADO (v394): a medir (kernel/construir_marcas.txt ainda nao traz o fim do build e do Audit do sandbox; rederivar depois). O rito faz 3 passagens de lake build + Audit e agora compila "
                   "os modulos novos a mais que a v393; o timeout do lake build DENTRO do um.py (candidato) tem de caber no tempo medido.")

# ----------------------------------------------------------------------------- a lista dos 189 modulos novos (sandbox x Nos, so' leitura)
def lean_de(raiz):
    s = set()
    for r, ds, fs in os.walk(os.path.join(raiz, "TGLExt")):
        ds[:] = [d for d in ds if d != ".lake"]
        for f in fs:
            if f.endswith(".lean"):
                s.add(os.path.relpath(os.path.join(r, f), raiz).replace(os.sep, "/"))
    return s


LISTA_INFO = {"estado": "sandbox ausente: lista nao gerada"}
if os.path.isfile(os.path.join(SB, "TGLExt.lean")):
    novos = sorted(lean_de(SB) - lean_de(os.path.join(NOS, "tgl_kernel")))
    removidos = sorted(lean_de(os.path.join(NOS, "tgl_kernel")) - lean_de(SB))
    assert not removidos and sorted(novos) == sorted(_NJ["novos"]) and DL.STONE_REL in novos, ("o sandbox (sandbox x Nos) nao traz exatamente os modulos novos da lista (com a pedra do delta) e nenhum a menos", len(novos), len(_NJ["novos"]), removidos[:3])
    assert all(x.startswith("TGLExt/") for x in novos)
    nj = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "kernel_modulos_novos_v394.json")) else {}
    n_dito = nj.get("novos") if isinstance(nj.get("novos"), int) else (len(nj["novos"]) if isinstance(nj.get("novos"), list) else None)
    assert n_dito in (None, len(novos)), ("kernel_modulos_novos_v394.json diz outro numero", n_dito)
    if isinstance(nj.get("novos"), list):
        assert sorted(nj["novos"]) == novos, "a lista de kernel_modulos_novos_v394.json difere da calculada (sandbox x Nos)"
    doc = {"novos": novos, "n": len(novos), "fonte": "diferenca dos .lean de TGLExt/ entre o sandbox " + SB.replace(os.sep, "/") + " e o tgl_kernel do Nos (v393 instalada); so' leitura",
           "lista_sha16": sha16("\n".join(novos).encode("utf-8")), "campo_novos_do_json_preparar": ("lista" if isinstance(nj.get("novos"), list) else "so a contagem %r (defeito do json.dump de preparar_kernel_v394.py: **info sobrescreve 'novos')" % (nj.get("novos"),))}
    grava("kernel_modulos_novos_v394.lista.json", json.dumps(doc, ensure_ascii=False, indent=1))
    LISTA_INFO = {"estado": "gerada", "n": len(novos), "lista_sha16": doc["lista_sha16"], "campo_novos_do_json_preparar": doc["campo_novos_do_json_preparar"]}

# ============================================================================= instalar_v394.py
src = rd(V3, "instalar_v393.py"); h_inst = sha16(src.encode("utf-8"))
t = sobe(src)
t = troca(t, "(ato da gerencia c1, 13/10/2026)", "(ato da gerencia c1, 19/10/2026)", nome="data do instalar")
t = troca(t, "(a v394 traz 3 pedras: o proprio rito as materializa a partir do corpo embutido)", "(a v394 traz %d modulos novos de kernel: o proprio rito os materializa a partir do corpo embutido)" % N_NOVOS, nome="docstring pedras")
t = troca(t, 'CAND = os.path.join(HERE, "um_v394_candidato.py")', 'CAND = os.path.join(HERE, "%s")' % DL.CANDIDATO, nome="candidato novo")
OLD_G = ('assert os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "Verdade.lean")) and os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", "Posto.lean")), "as pedras da v393 (Verdade, Posto) nao estao no kernel do Nos -- nao instalo"\n'
         'assert not [rel for rel in ESP["pedras_sha256"] if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "alguma das 3 pedras da regra (v394) ja esta no kernel do Nos -- nao instalo"\n')
NEW_G = '''# v394: (a) as 3 pedras da v393 (a regra) JA estao no kernel do Nos (a base instalada e' a v393 selada); (b) NENHUM dos modulos novos da v394 (os do Codex e a pedra do criterio binario de parada) esta la ainda.
# A lista dos modulos novos: kernel_modulos_novos_v394.json (campo 'novos', gerado por preparar_kernel_v394.py) se vier como LISTA; se vier so' a contagem (defeito conhecido do json.dump), a lista de
# kernel_modulos_novos_v394.lista.json (derivar_instalar_rito_v394.py: sandbox x Nos); por fim ESPERADOS.pedras_sha256 / ESPERADOS.kernel.new. Fail-closed em tudo.
_PEDRAS_V393 = ("RuleTruthContract", "TheRuleAndTheFigureOfTruth", "TheRuleInTheContinuousMotor")
assert all(os.path.exists(os.path.join(NOS, "tgl_kernel", "TGLExt", n_ + ".lean")) for n_ in _PEDRAS_V393), "as pedras da v393 (RuleTruthContract, TheRuleAndTheFigureOfTruth, TheRuleInTheContinuousMotor) nao estao no kernel do Nos -- nao instalo"


def _modulos_novos():
    nj = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))
    n_dito = nj["novos"] if isinstance(nj["novos"], int) else len(nj["novos"])
    if isinstance(nj["novos"], list):
        return list(nj["novos"]), n_dito, "kernel_modulos_novos_v394.json[novos]"
    pl = os.path.join(HERE, "kernel_modulos_novos_v394.lista.json")
    if os.path.exists(pl):
        return list(json.load(open(pl, encoding="utf-8"))["novos"]), n_dito, "kernel_modulos_novos_v394.lista.json[novos]"
    return list(ESP.get("pedras_sha256") or ESP["kernel"]["new"]), n_dito, "ESPERADOS_v394(pedras_sha256|kernel.new)"


NOVOS_V394, _N_DITO, _FONTE_NOVOS = _modulos_novos()
assert len(NOVOS_V394) == _N_DITO and len(set(NOVOS_V394)) == _N_DITO and ESP["kernel"]["modulos_novos"] == _N_DITO and all(x_.startswith("TGLExt/") and x_.endswith(".lean") for x_ in NOVOS_V394), ("a lista dos modulos novos nao e' a do ESPERADOS (.lean de TGLExt/)", len(NOVOS_V394), _N_DITO, _FONTE_NOVOS)
assert set(NOVOS_V394) == set(ESP.get("pedras_sha256") or NOVOS_V394), "a lista dos modulos novos difere de ESPERADOS.pedras_sha256 -- nao instalo"
assert not [rel for rel in NOVOS_V394 if os.path.exists(os.path.join(NOS, "tgl_kernel", *rel.split("/")))], "algum dos modulos novos (v394) ja esta no kernel do Nos -- nao instalo"
'''
t = troca(t, OLD_G, NEW_G, nome="guardas das pedras")
t = troca(t, 'ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}\n',
          'ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}\nrec["modulos_novos_v394"] = {"fonte": _FONTE_NOVOS, "n": len(NOVOS_V394), "lista": NOVOS_V394}   # o reverter usa ESTA lista (a que o instalar conferiu)\n', nome="rec modulos novos")
ast.parse(t); INSTALAR = t

# ============================================================================= rito_v394.sh
src = rd(V3, "rito_v393.sh"); h_rito = sha16(src.encode("utf-8"))
r = sobe(src)
r = troca(r, "(ato da gerencia c1, 13/10/2026)", "(ato da gerencia c1, 19/10/2026)", nome="data do rito")
r = troca(r, "3 pedras novas de kernel (a regra) materializadas", "%d modulos novos de kernel (TimeGraviton*, RuleQuadraticResidual, F1Fecho394/* e a pedra do criterio binario de parada) materializados" % N_NOVOS, nome="pedras no rito")
r = troca(r, "os registros por spec e os registros v394 (a regra e o coracao)", "os registros por spec e os seis registros novos do core v394 (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394, kh_n1_cobertura_v394, criterio_binario_de_parada_v394)", nome="registros no rito")
r = troca(r, "# (3a a 10a afericoes, 03-04/10/2026)\n", "# (3a a 10a afericoes, 03-04/10/2026)\n" + LINHA_TEMPO + "\n", nome="linha do tempo")
EXP_SET = 'set -- "/c/IALD/Central de Patentes/work/cadeia_de_selo/v393" "/c/IALD/Central de Patentes/work/cadeia_de_selo/v394"'
assert r.count(EXP_SET) == 1, "a guarda do marcador anterior nao ficou 'set -- <v393> <v394>'"
assert r.count('PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v394"') == 1
RITO = r

# ============================================================================= reverter_v394.py
src = rd(V3, "reverter_v393.py"); h_rev = sha16(src.encode("utf-8"))
v = sobe(src)
v = troca(v, "e poe as 3 pedras da regra em QUARENTENA (nunca apaga).", "e poe os %d modulos novos de kernel da v394 em QUARENTENA (nunca apaga; guarda o caminho relativo)." % N_NOVOS, nome="doc quarentena")
v = troca(v, "Confere ao fim que o um.py voltou a ser a v393 selada (b590c0aa80055e2a).", "Confere ao fim que o um.py voltou a ser a v393 selada (o sha16 e' LIDO de ESPERADOS_v393.json do pacote anterior, nunca digitado).", nome="doc ancora")
v = troca(v, 'T2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")\n',
          '''T2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# --- tudo o que decide a reversao e' LIDO ANTES de qualquer escrita (fail-closed): ESPERADOS_v394, a lista dos modulos novos e a ancora do hash da v393 selada
esp = json.load(open(os.path.join(CAD, "ESPERADOS_v394.json"), encoding="utf-8"))
_aplic = AP.get("modulos_novos_v394") or {}
_lista = list(_aplic.get("lista") or []) or list(esp.get("pedras_sha256") or [])
assert len(_lista) == len(set(_lista)) == len(esp["pedras_sha256"]) and set(_lista) == set(esp["pedras_sha256"]) and all(x_.startswith("TGLExt/") and x_.endswith(".lean") for x_ in _lista), ("a lista dos modulos novos da v394 difere de ESPERADOS.pedras_sha256", len(_lista))
try:
    ANCORA = json.load(open(os.path.join(os.path.dirname(CAD), "v393", "ESPERADOS_v393.json"), encoding="utf-8"))["candidato_sha16"]   # o sha16 do um.py da v393 selada, lido do pacote anterior
except (OSError, ValueError, KeyError):
    ANCORA = None
''', nome="leitura previa")
OLD_Q = '''for nome in esp.get("pedras_sha256", {}):
    p = os.path.join(NOS, "tgl_kernel", *nome.split("/"))
    if os.path.isfile(p):
        shutil.move(p, os.path.join(qd, os.path.basename(p))); rec["quarentena"].append(os.path.basename(p))
'''
NEW_Q = '''rec["quarentena_fonte"] = "APLICADO_AO_CANONICO.modulos_novos_v394.lista" if _aplic.get("lista") else "ESPERADOS.pedras_sha256"
for nome in _lista:
    p = os.path.join(NOS, "tgl_kernel", *nome.split("/"))
    if os.path.isfile(p):
        d_ = os.path.join(qd, *nome.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True)
        shutil.move(p, d_); rec["quarentena"].append(nome)
_dir_f1 = os.path.join(NOS, "tgl_kernel", "TGLExt", "F1Fecho394")
if os.path.isdir(_dir_f1) and not os.listdir(_dir_f1):
    os.rmdir(_dir_f1)   # so' se vazio; o .lake/build (olean) NAO e' limpo, como no molde
'''
v = troca(v, OLD_Q, NEW_Q, nome="quarentena")
v = troca(v, 'rec["ok"] = umsha == esp["origem_sha16"] == "b590c0aa80055e2a"\n',
          'rec["ancora_v393"] = {"fonte": "v393/ESPERADOS_v393.json[candidato_sha16]", "sha16": ANCORA}\nrec["ok"] = umsha == esp["origem_sha16"] and (ANCORA is None or umsha == ANCORA)\n', nome="ok")
assert "b590c0aa80055e2a" not in v, "ficou o hash da v392 digitado no reverter"
ast.parse(v); REVERTER = v

# ============================================================================= refazer_arvore_v394_pos_selo.py
src = rd(V3, "refazer_arvore_v393_pos_selo.py"); h_arv = sha16(src.encode("utf-8"))
a = sobe(src)
a = a.replace(r'ARV = r"C:\t\k394\arvore"', r'ARV = r"C:\t\k394d\arvore"').replace('refaz C:/t/k394/arvore', 'refaz C:/t/k394d/arvore')
assert a.count(r'ARV = r"C:\t\k394d\arvore"') == 1, "ARV nao ficou em k394d"
a = troca(a, '"kernel", "KERNEL_RECIBO_v394.json"', '"%s", "KERNEL_RECIBO_v394.json"' % DL.KERNEL_DIR, nome="recibo na pasta d19")
ast.parse(a); ARVORE = a

# ============================================================================= refazer_sandbox_v394.sh e _pos_selo.sh
src = rd(V3, "refazer_sandbox_v393.sh"); h_sb = sha16(src.encode("utf-8"))
s = sobe(src)
L = s.split("\n")
assert L[0] == "#!/bin/sh" and L[1].startswith("# refaz do ZERO o sandbox B do kernel da v394") and L[2].startswith("# um unico lake build"), L[:3]
L[1] = ("# refaz do ZERO o sandbox B do kernel da v394 (C:/t/k394d/final): copia o kernel que o Nos TEM (a v393 instalada), acrescenta os 189 modulos do Codex (TimeGraviton*, RuleQuadraticResidual, F1Fecho394/*) e a pedra do criterio binario de parada e GERA a raiz e o Audit")
L[2] = ("# (preparar_kernel_v394.py gerar: conferido byte a byte contra a arvore candidate_r8 do Codex), UM unico lake build + Audit (construir_kernel_v394.sh) e o pos-build (pos_build_kernel_v394.py). USAR ANTES de instalar_v394.py: "
        "o `gerar` le o um.py do Nos como a base v393.")
s = "\n".join(L)
s = troca(s, "preparar_kernel_v394.py final", "preparar_kernel_v394.py gerar", nome="modo gerar")
s = s.replace("/c/t/k394", "/c/t/k394d").replace("C:\\t\\k394\\", "C:\\t\\k394d\\")
assert s.count("/c/t/k394d") == 1 and s.count("C:\\t\\k394d\\final") == 1 and s.count("C:\\t\\k394d\\robocopy_final.log") == 1 and "k394\\" not in s.replace("k394d\\", ""), "os caminhos do sandbox nao ficaram em k394d"
GUARDA_SB = ('[ -f "$V/pos_build_kernel_v394.py" ] || { echo "falta pos_build_kernel_v394.py em $V (gerado a parte) -- NAO RODO"; exit 9; }\n'
             '[ -f "$V/preparar_kernel_v394.py" ] && [ -f "$V/construir_kernel_v394.sh" ] || { echo "falta preparar_kernel_v394.py ou construir_kernel_v394.sh -- NAO RODO"; exit 9; }\n')
s = troca(s, 'cd "$V" && python', GUARDA_SB + 'cd "$V" && python', nome="guarda de existencia")
SANDBOX = s
src = rd(V3, "refazer_sandbox_v393_pos_selo.sh"); h_sbp = sha16(src.encode("utf-8"))
SANDBOX_POS = sobe(src)
assert "refazer_arvore_v394_pos_selo.py" in SANDBOX_POS

# ============================================================================= guarda_p18_v394.py: copia de BYTES da v393 (as cinco regras nao mudaram), so' se ainda nao existir
gp = os.path.join(HERE, "guarda_p18_v394.py")
if not os.path.exists(gp):
    open(gp, "wb").write(open(os.path.join(V3, "guarda_p18_v393.py"), "rb").read())
GUARDA_P18 = {"estado": "copia de bytes da v393", "sha16": sha16(open(gp, "rb").read()), "molde_sha16": sha16(open(os.path.join(V3, "guarda_p18_v393.py"), "rb").read())}

# ============================================================================= gravar e conferir
DER = {"instalar_v394.py": INSTALAR, "rito_v394.sh": RITO, "reverter_v394.py": REVERTER, "refazer_arvore_v394_pos_selo.py": ARVORE, "refazer_sandbox_v394.sh": SANDBOX, "refazer_sandbox_v394_pos_selo.sh": SANDBOX_POS}
for n, tx in DER.items():
    grava(n, tx)
sint = {}; falhas = []
for n in DER:
    tx = open(os.path.join(HERE, n), "rb").read().decode("utf-8")
    assert tx == DER[n]
    if n.endswith(".py"):
        ast.parse(tx); sint[n] = "ast.parse ok"
    else:
        rr = subprocess.run(["sh", "-n", os.path.join(HERE, n)], capture_output=True, text=True); sint[n] = "sh -n rc=%d %s" % (rr.returncode, rr.stderr[:200])
        if rr.returncode:
            falhas.append((n, "sh -n"))
    assert "\r" not in tx, ("CR no derivado", n)
# invariantes do molde que TEM de sobreviver (fail-closed, backup de bytes, temporario -> substituir, guardas)
INV = {"instalar_v394.py": ["RECUSO: rodar sem -O", "VIGIA_OK", "o canonico nao e a v393 selada", "open(b, \"wb\").write(data); assert open(b, \"rb\").read() == data", "os.replace(tmp, um)", "tmp = um + \".tmp_instalar_v394_\" + ts",
                            "pilar_anterior_v393_", "APLICADO_AO_CANONICO_%s.json", "CM[\"base_v393_sha16\"]", "ESPERADOS_v394.json", "CANDIDATO_v394.json", DL.CANDIDATO, "kernel_modulos_novos_v394.json",
                            "RuleTruthContract", "TheRuleAndTheFigureOfTruth", "TheRuleInTheContinuousMotor", "== _N_DITO", "NOVOS_V394", "modulos_novos_v394"],
       "rito_v394.sh": ['set -- "/c/IALD/Central de Patentes/work/cadeia_de_selo/v393" "/c/IALD/Central de Patentes/work/cadeia_de_selo/v394"', 'PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v394"', "exit 18", "exit 16", "exit 17", "exit 10", "exit 11", "exit 12",
                        "rodada_v394_stdout.txt", "RITO_RC=", ".rito_v394.pid", "rito_servidor_v394.log", "ESPERADOS_v394.json", "echo 1 | python um.py", "trap 'religar; rm -f", "TEMPO ESPERADO (v394"],
       "reverter_v394.py": ["APLICADO_AO_CANONICO_*.json", "backup ausente ou alterado", "quarentena_pedras_", "tentativa_v394_rito_falhou_", "RECIBO_REVERSAO_", "rodada_v394_stdout.txt", "ESPERADOS_v394.json", "ANCORA", "ESPERADOS_v393.json", "set(_lista) == set(esp[\"pedras_sha256\"])"],
       "refazer_arvore_v394_pos_selo.py": ["KERNEL_RECIBO_v394.json", r'ARV = r"C:\t\k394d\arvore"', "shutil.rmtree(ARV)", "assert os.path.normpath(R[\"arvore\"]) == os.path.normpath(ARV)", "chk(\"links\", links, [])"],
       "refazer_sandbox_v394.sh": ["/c/t/k394d", r"C:\t\k394d\final", "preparar_kernel_v394.py gerar", "construir_kernel_v394.sh", "pos_build_kernel_v394.py", "robocopy"],
       "refazer_sandbox_v394_pos_selo.sh": ["refazer_arvore_v394_pos_selo.py"]}
conf = {}
for n, lst in INV.items():
    tx = DER[n]; conf[n] = {}
    for x in lst:
        ok = x in tx; conf[n][x[:90]] = ok
        if not ok:
            falhas.append((n, x[:90]))
# rotulos que tem de sair corretos para a v394 (sem resto da versao anterior onde o sentido e' 'esta versao')
ROTULOS = {"instalar_v394.py": ["pilar_anterior_v393", "base_v393_sha16", ".tmp_instalar_v394_", "ESPERADOS_v394", "CANDIDATO_v394"],
           "rito_v394.sh": [".rito_v394.pid", "rito_servidor_v394.log", "rito_v394_sinal.txt", "rito_horarios_v394.txt", "rodada_v394_stdout"],
           "reverter_v394.py": ["tentativa_v394_rito_falhou_", "rodada_v394_stdout.txt"], "refazer_arvore_v394_pos_selo.py": ["k394"]}
for n, lst in ROTULOS.items():
    for x in lst:
        if x not in DER[n]:
            falhas.append((n, "rotulo ausente: " + x))
for n, tx in DER.items():
    for m in re.finditer(r"[A-Za-z0-9_\-\.]*39[0-3][A-Za-z0-9_\-\.]*", tx):
        tok = m.group(0).rstrip(".")
        if any(p in tok for p in PROT) or tok in ("instalar_v393.py", "rito_v393.sh", "reverter_v393.py", "refazer_arvore_v393_pos_selo.py", "refazer_sandbox_v393.sh", "refazer_sandbox_v393_pos_selo.sh"):
            continue   # (os nomes dos MOLDES v393 aparecem nas linhas 'Molde:' dos docstrings)
        # permitidos: 'v393'/'k393' apenas como a versao ANTERIOR (base, pilar anterior, ancora, pasta v393, ESPERADOS_v393, pedras da v393, etc.)
        if re.search(r"(?<![A-Za-z0-9])(?:rito|instalar|reverter|ESPERADOS|CANDIDATO|PINOS_BN|rodada|tentativa)_v393|(?:^|_|\.)k393|_sup39|_f39[23]|_p39[23]|V392_|V393_AVISO", tok) and "ESPERADOS_v393.json" not in tok:
            falhas.append((n, "rotulo da versao ANTERIOR onde devia estar a v394: " + tok))
DERJ = {"molde": {"instalar_v393.py": h_inst, "rito_v393.sh": h_rito, "reverter_v393.py": h_rev, "refazer_arvore_v393_pos_selo.py": h_arv, "refazer_sandbox_v393.sh": h_sb, "refazer_sandbox_v393_pos_selo.sh": h_sbp,
                  "derivar_instalar_rito_v393.py": sha16(open(os.path.join(V3, "derivar_instalar_rito_v393.py"), "rb").read())},
        "derivados": {n: sha16(DER[n].encode("utf-8")) for n in DER}, "guarda_p18_v394.py": GUARDA_P18,
        "sobe": "v393 -> v394, v392 -> v393 (anterior), V393 -> V394, V392 -> V393, k393 -> k394, work393 -> work394; PROT (nao sobem): " + ", ".join(PROT),
        "tempo_build": TEMPO, "lista_modulos_novos": LISTA_INFO,
        "invariantes": conf, "sintaxe": sint, "falhas": falhas,
        "defeito_achado_em_preparar_kernel_v394": "json.dump({\"novos\": NOVOS, **info}): info[\"novos\"] (contagem) sobrescreve a lista; kernel_modulos_novos_v394.json sai com novos=189 (int). Correcao sugerida: {**info, \"novos\": NOVOS}. O instalar e o reverter ja tratam as duas formas.",
        "nao_validado": "nenhum derivado foi EXECUTADO nem revisto por cetico independente; so' ast.parse, sh -n, invariantes e rotulos por texto; a execucao exige ESPERADOS_v394.json, CANDIDATO_v394.json e um_v394_candidato.py (gerados por outro processo)"}
grava("DERIVACAO_v394.json", json.dumps(DERJ, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DERJ["derivados"][n]) for n in DER))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("TEMPO:", json.dumps(TEMPO, ensure_ascii=False)); print("LISTA:", json.dumps(LISTA_INFO, ensure_ascii=False))
print("INVARIANTES:", sum(len(x) for x in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)
