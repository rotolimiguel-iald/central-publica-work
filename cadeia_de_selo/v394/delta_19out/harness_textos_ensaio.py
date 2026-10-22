# -*- coding: utf-8 -*-
"""harness_textos_ensaio.py -- DELTA 19/10 (rodada d19c, gerencia c1): o HARNESS DOS TEXTOS DO POS-RITO em modo ENSAIO, SO' LEITURA.
Importa o modulo REAL dos textos (pos_rito\\textos_v394.py, ou o arquivo dado em --textos) e a LEITURA REAL da rodada (pos_rito\\leitura_v394.py) e as executa contra um Nos EMULADO (delta_19out\\falso_nos, montado por
teste_conferidor_positivo.py a partir da pasta do ensaio a seco: o um.py candidato, o kernel com os residuais, o core e o selo que o ensaio computou). Nada de pos_rito e' escrito nem importado com bytecode; nada de Nos
real e' tocado; nenhum rito e' rodado. O que e' EMULADO (e dito): (a) o stdout do rito (rodada_v394_stdout.txt, escrito em falso_nos: so' as linhas que a leitura confere, com a escada lida de ESPERADOS), (b) o aplicado
(APLICADO_AO_CANONICO), (c) a conferencia do rito (a do caminho positivo contra o falso Nos). O resto vem dos arquivos.
Executa _d (a SOMA das bandeiras por grupo), _num e todas as funcoes publicas de texto, passa a guarda P18 em cada saida e confere que a frase de ERRATA da palavra «teoremas» esta nos textos que carregam _num.
uso: python -I -B -X utf8 harness_textos_ensaio.py [--textos <arquivo>] [--rotulo <nome>] [--sem-errata]   (rc 0 = tudo passou)"""
import hashlib, importlib.util, json, os, shutil, sys, time, traceback
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); POS = os.path.join(V, "pos_rito"); FN = os.path.join(HERE, "falso_nos")
sys.path.insert(0, V)
import delta19_v394 as DL  # noqa: E402
from guarda_p18_v394 import violacoes  # noqa: E402
arg = lambda k, d=None: (sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d)
TEXTOS = os.path.abspath(arg("--textos", os.path.join(POS, "textos_v394.py"))); ROTULO = arg("--rotulo", "pos_rito"); SEM_ERRATA = "--sem-errata" in sys.argv
sha = lambda b: hashlib.sha256(b).hexdigest()
OUT_DIR = os.path.join(HERE, "harness_textos_saida", ROTULO)
R = {"rotulo": ROTULO, "textos": TEXTOS, "textos_sha16": sha(open(TEXTOS, "rb").read())[:16], "emulado": ["stdout do rito (rodada_v394_stdout.txt em falso_nos)", "APLICADO_AO_CANONICO", "conferencia do rito (caminho positivo contra o falso Nos)"], "etapas": {}, "problemas": []}


def falha(msg):
    R["problemas"].append(msg); print("  PROBLEMA:", msg)


# ------------------------------------------------------------------ precondicoes (o Nos emulado tem de existir e ser o do ensaio a seco da geracao corrente)
for n in ("um.py", "um_absoluto.json", "um_absoluto_selo.json", "tgl_kernel"):
    if not os.path.exists(os.path.join(FN, n)):
        print("RECUSO: falso_nos incompleto (falta %s): rode antes teste_conferidor_positivo.py" % n); sys.exit(4)
ESP = json.load(open(os.path.join(V, "ESPERADOS_v394.json"), encoding="utf-8"))
um16 = sha(open(os.path.join(FN, "um.py"), "rb").read())[:16]
if um16 != ESP["candidato_sha16"]:
    print("RECUSO: o um.py do falso_nos (%s) != o candidato de ESPERADOS (%s): o falso_nos e' de outra geracao" % (um16, ESP["candidato_sha16"])); sys.exit(4)
CONF = os.path.join(HERE, "conferencia_POSITIVO_FALSO_NOS.json")
C = json.load(open(CONF, encoding="utf-8"))
if C.get("tudo_bate") is not True:
    print("RECUSO: a conferencia positiva contra o falso Nos nao esta TUDO BATE"); sys.exit(4)
R["candidato_sha16"] = um16; R["conferencia_positiva_sha16"] = sha(open(CONF, "rb").read())[:16]

# ------------------------------------------------------------------ (a) o stdout EMULADO do rito: so' as linhas que a leitura confere; a escada vem de ESPERADOS
N_ = ESP["escada"][1]
stdout_emulado = "\n".join(["[v394] EMULADO PELO HARNESS (nao e' o stdout de um rito; so' as linhas que a leitura confere)", "teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED",
                            "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", "RITO_RC=0", ""])
open(os.path.join(FN, "rodada_v394_stdout.txt"), "w", encoding="utf-8", newline="\n").write(stdout_emulado)
# (c) a pasta da conferencia que a leitura procura (HERE/conferidor/conferencia_rito_v394.json), dentro do harness
HC = os.path.join(HERE, "harness_textos_pos_rito_emulada"); os.makedirs(os.path.join(HC, "conferidor"), exist_ok=True)
shutil.copyfile(CONF, os.path.join(HC, "conferidor", "conferencia_rito_v394.json"))


def importar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


# ------------------------------------------------------------------ a LEITURA real, apontada para o falso Nos
print("harness dos textos (ENSAIO, so' leitura) -- rotulo %s; textos %s (sha16 %s); candidato %s" % (ROTULO, os.path.basename(TEXTOS), R["textos_sha16"], um16))
L = importar("leitura_v394_h", os.path.join(POS, "leitura_v394.py"))
L.NOS = FN; L.HERE = HC; L.PK = V
ap = {"um_py_novo": {"sha16": ESP["candidato_sha16"]}, "backups": {"um.py": {"sha16": ESP["origem_sha16"], "backup": "EMULADO_PELO_HARNESS"}}, "ts": time.strftime("%Y%m%d_%H%M%S")}
L._aplicado = lambda: (ap, "EMULADO_PELO_HARNESS")
Vd, P = L.ler()
R["etapas"]["leitura"] = {"problemas": P, "n_pedras": Vd.get("n_pedras"), "teor": Vd.get("teor"), "escada_antes": Vd.get("escada_antes"), "kh": Vd.get("kh"), "registros_novos": Vd.get("registros_novos"), "n_cunhagens": len(Vd.get("verbatins") or {})}
print("  leitura: %d problema(s); %d pedras; escada %s -> %s; %d cunhagens" % (len(P), Vd.get("n_pedras"), Vd.get("escada_antes"), Vd.get("teor"), len(Vd.get("verbatins") or {})))
for p in P:
    falha("leitura: " + p)

# ------------------------------------------------------------------ os TEXTOS reais, apontados para o mesmo falso Nos e para o mesmo pacote
TEXTOS_IMPORTAR = TEXTOS
if not TEXTOS.endswith(".py"):   # a copia ORIGINAL da proposta tem outra extensao: importa uma copia .py dentro da saida do harness (a copia em si nao e' alterada)
    os.makedirs(OUT_DIR, exist_ok=True); TEXTOS_IMPORTAR = os.path.join(OUT_DIR, "textos_v394_copia_importada.py"); shutil.copyfile(TEXTOS, TEXTOS_IMPORTAR)
T = importar("textos_v394_h", TEXTOS_IMPORTAR)
T.NOS = FN; T.PK = V; T._CACHE.clear()
FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_grupos_txt", lambda: T._grupos_txt(T._d(Vd))), ("_kh_errata", lambda: T._kh_errata(Vd)),
           ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")), ("_lado_c1", lambda: T._lado_c1(Vd)), ("_criterio", lambda: T._criterio(Vd)),
           ("_criterio_curto", lambda: T._criterio(Vd, curto=True)), ("_criterio_mini", lambda: T._criterio_mini(Vd)), ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)),
           ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)), ("core_memory", lambda: T.core_memory(Vd)),
           ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)),
           ("topico_novo", lambda: T.topico_novo(Vd)), ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("verbete", lambda: T.verbete(Vd)),
           ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd))]
CARREGAM_NUM = {"_num", "_num_sem_veredito", "linhagem", "atlas", "core_memory", "topico_novo", "verbete"}   # os textos que embutem _num (o texto do kernel com a errata)
os.makedirs(OUT_DIR, exist_ok=True)
d_ = None; ERR = DL.ERRATA_TEOREMAS_PT
for nome, f in FUNCOES:
    e = {"ok": False}
    try:
        r = f()
        if nome == "_d":
            d_ = r
            e["numeros"] = {k: r[k] for k in ("n_flags", "g_t", "g_q", "g_r", "n_out_flags", "n_t", "n_q", "n_r", "n_tg", "n_f1", "n_out", "depois", "n_cun", "formais_n") if k in r}
            # a SOMA que o assert confere, refeita aqui por fora: grupos nomeados + outros == total das bandeiras novas
            if all(k in r for k in ("g_t", "g_q", "g_r")):
                e["soma_por_grupo"] = r["g_t"] + r["g_q"] + r["g_r"] + r["n_out_flags"]; e["soma_fecha"] = bool(e["soma_por_grupo"] == r["n_flags"] == ESP["n_bandeiras_novas"])
            else:
                e["soma_fecha"] = False
        else:
            assert isinstance(r, str) and r.strip(), "texto vazio"
            v = violacoes(r)
            e["bytes"] = len(r.encode("utf-8")); e["sha16"] = sha(r.encode("utf-8"))[:16]; e["guarda_p18"] = [list(x) for x in v][:3]
            open(os.path.join(OUT_DIR, nome + ".txt"), "w", encoding="utf-8", newline="\n").write(r)
            if nome in CARREGAM_NUM and not SEM_ERRATA:
                e["tem_errata_teoremas"] = ERR in r
            if v:
                falha("%s: guarda P18 achou %s" % (nome, v[:2]))
            if nome in CARREGAM_NUM and not SEM_ERRATA and ERR not in r:
                falha("%s: a frase de errata da palavra «teoremas» nao esta no texto" % nome)
        e["ok"] = True
    except BaseException as ex:  # noqa: BLE001
        e["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); e["onde"] = traceback.format_exc().strip().splitlines()[-3:]
        falha("%s: %s" % (nome, e["erro"]))
        if nome == "_d" and "bandeiras novas nao somam" in str(ex):
            e["a_soma_nao_fecha"] = True
    R["etapas"][nome] = e
    print("  %-20s %s%s" % (nome, "OK " if e["ok"] else "FALHOU", (" -- " + e["erro"][:200]) if not e["ok"] else ""))
R["soma_fecha"] = bool((R["etapas"].get("_d") or {}).get("soma_fecha"))
R["tudo_passou"] = bool(not R["problemas"] and all(e["ok"] for k_, e in R["etapas"].items() if k_ != "leitura") and R["soma_fecha"])
R["veredito"] = "TUDO PASSOU: a soma fecha, os textos rendem, a guarda P18 esta limpa" if R["tudo_passou"] else "NAO PASSOU (ver problemas)"
if d_:
    print("  soma por grupo: tempo %s + quadratica %s + rede %s + outros %s = %s (bandeiras novas %s; ESPERADOS %s)" % (d_["g_t"], d_["g_q"], d_["g_r"], d_["n_out_flags"], (d_["g_t"] + d_["g_q"] + d_["g_r"] + d_["n_out_flags"]) if all(k in d_ for k in ("g_t", "g_q", "g_r")) else "?", d_["n_flags"], ESP["n_bandeiras_novas"]))
saida = os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_%s.json" % ROTULO)
json.dump(R, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("VEREDITO DO HARNESS (%s): %s" % (ROTULO, R["veredito"])); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)
