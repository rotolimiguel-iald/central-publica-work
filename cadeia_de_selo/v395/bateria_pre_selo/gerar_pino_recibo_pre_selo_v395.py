# -*- coding: utf-8 -*-
"""gerar_pino_recibo_pre_selo_v395.py -- gera PINO_RECIBO_PRE_SELO_v395.json e PROVA_PRODUCAO_INTACTA_v395_pre_selo.json (em v395\\) a partir do recibo do ensaio, do stdout, do lancador,
dos pinos do esboco e da bateria, da conferencia pelo esboco (conferencia_pelo_esboco_v395.json) e das fotografias da producao (antes / depois / final). TUDO LIDO dos arquivos, por script;
nada digitado de memoria. Nao grava na Bancada, no Nos nem no tunel: escreve so' os dois JSON em v395\\ e copia as listas de arquivos para v395\\bateria_pre_selo\\prova_producao\\.
Molde: v394\\bateria_pre_selo\\gerar_pino_recibo_pre_selo_v394.py (mesmas chaves do pino; aqui o ensaio PASSA e a regra e' aplicada pela funcao do proprio esboco).
uso: python -I -B -X utf8 gerar_pino_recibo_pre_selo_v395.py <pasta das fotografias (C:\\t\\vb12\\snap)>"""
import sys

sys.dont_write_bytecode = True
import glob
import gzip
import hashlib
import json
import os
import shutil
import socket
import time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
V4 = os.path.join(os.path.dirname(V), "v394")
SP = os.path.abspath(sys.argv[1])
DEST_PROVA = os.path.join(HERE, "prova_producao")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def lj(p):
    return json.load(open(p, encoding="utf-8"))


# ---- o recibo, o stdout, o lancador, os pinos
rps = glob.glob(os.path.join(HERE, "ensaio_1", "RECIBO_SINCRONIZACAO_v394_*.json"))
assert len(rps) == 1, rps
REC = rps[0]
raw = open(REC, "rb").read()
RSHA = hashlib.sha256(raw).hexdigest()
r = json.loads(raw.decode("utf-8"))
STDOUT = os.path.join(HERE, "etapa1_stdout.txt")
LANC = os.path.join(HERE, "rodar_ensaio_1_pre_selo_v395.sh")
pbn = lj(os.path.join(V4, "PINOS_BN_v394.json"))
pbat = lj(os.path.join(V4, "bateria_pos_selo", "PINOS_BATERIA_v394.json"))
ESB, ESB_SHA = pbn["esboco_R3_5"]["path"], pbn["esboco_R3_5"]["sha256"]
BAT, BAT_SHA = pbat["bateria"]["path"], pbat["bateria"]["sha256"]
assert sha(ESB) == ESB_SHA and sha(BAT) == BAT_SHA, "esboco ou bateria em disco diferem dos pinos"
assert r["script_sha256"] == ESB_SHA and r["bateria"]["sha256"] == BAT_SHA, "o recibo nao foi gerado com o esboco/bateria pinados"
linhas = open(STDOUT, encoding="utf-8").read().splitlines()
imp = json.loads([l for l in linhas if l.strip().startswith("{")][-1])
RC = int([l for l in linhas if l.startswith("ETAPA1_RC=")][-1].split("=", 1)[1])
assert imp["recibo_sha256"] == RSHA and os.path.samefile(imp["recibo"], REC), "o stdout nao cita este recibo"
conf_p = os.path.join(HERE, "conferencia_pelo_esboco_v395.json")
conf = lj(conf_p)
assert conf["recibo"]["sha256"] == RSHA and conf["esboco"]["sha256"] == ESB_SHA, "a conferencia e' de outro recibo/esboco"

bat = r["bateria_resultado"]
testes = {t["id"]: t for t in bat["testes"]}
t12 = lj(os.path.join(HERE, "ensaio_1", "recibos", "T12_T13_T14_ATRATOR.json"))
sub = {k: ("PASSA" if v.get("passa") else "FALHA") for k, v in t12["runs"].items()}
mant = r["manifesto_anterior"]

# ---- o comando exato: o argv REAL registrado no recibo (sys.orig_argv), com o executavel escrito como `python`
argv = list(r["python_isolado"]["orig_argv"])
cmd = "python " + " ".join(('"%s"' % a) if (("\\" in a) or (" " in a)) else a for a in argv[1:])

# ---- a prova de que a producao so' foi lida: tres fotografias (antes do ensaio, logo depois, depois de tudo que esta tarefa leu)
ROT = ("antes", "depois", "final")


def sha_lista(lista):
    h = hashlib.sha256()
    for rel, t, s, m in lista:
        h.update(("%s\t%s\t%d\t%d\n" % (rel, t, s, m)).encode("utf-8"))
    return h.hexdigest()


def carregar(rot):
    ch = lj(os.path.join(SP, "chaves_%s.json" % rot))
    ban = lj(os.path.join(SP, "fp_bancada_%s.json" % rot))
    nos = json.loads(gzip.decompress(open(os.path.join(SP, "fp_nos_%s.json.gz" % rot), "rb").read()).decode("utf-8"))
    assert sha_lista(ban) == ch["bancada"]["sha256_da_lista"], "lista da Bancada (%s) nao bate com o resumo" % rot
    assert sha_lista(nos) == ch["nos"]["sha256_da_lista"], "lista do Nos (%s) nao bate com o resumo" % rot
    return ch, ban, nos


snaps = {rot: carregar(rot) for rot in ROT}


def difere(a, b):
    da = {x[0]: tuple(x[1:]) for x in a}
    db = {x[0]: tuple(x[1:]) for x in b}
    add, rem = sorted(set(db) - set(da)), sorted(set(da) - set(db))
    alt = sorted(k for k in set(da) & set(db) if da[k] != db[k])
    return {"adicionados": add[:50], "removidos": rem[:50], "alterados": alt[:50], "n_adicionados": len(add), "n_removidos": len(rem), "n_alterados": len(alt)}


def bloco(nome):
    out = {"raiz": snaps["antes"][0][nome]["raiz"], "fotografias": {}}
    for rot in ROT:
        ch = snaps[rot][0]
        out["fotografias"][rot] = {k: ch[nome][k] for k in ("quando",) if k in ch[nome]}
        out["fotografias"][rot].update({"quando": ch["quando"], "n_entradas": ch[nome]["n_entradas"], "n_arquivos": ch[nome]["n_arquivos"], "n_pastas": ch[nome]["n_pastas"],
                                        "bytes_arquivos": ch[nome]["bytes_arquivos"], "sha256_da_lista": ch[nome]["sha256_da_lista"], "erros_de_leitura": len(ch[nome]["erros_de_leitura"])})
    idx = 1 if nome == "bancada" else 2
    d1 = difere(snaps["antes"][idx], snaps["depois"][idx])
    d2 = difere(snaps["antes"][idx], snaps["final"][idx])
    out["diferencas_antes_depois"] = d1
    out["diferencas_antes_final"] = d2
    out["lista_identica_antes_depois_final"] = (d1["n_adicionados"] + d1["n_removidos"] + d1["n_alterados"] + d2["n_adicionados"] + d2["n_removidos"] + d2["n_alterados"] == 0
                                               and len({snaps[rot][0][nome]["sha256_da_lista"] for rot in ROT}) == 1)
    return out


b_ban, b_nos = bloco("bancada"), bloco("nos")
chaves = []
for i, c in enumerate(snaps["antes"][0]["chaves"]):
    iguais = all(snaps[rot][0]["chaves"][i]["sha256"] == c["sha256"] and snaps[rot][0]["chaves"][i]["bytes"] == c["bytes"] for rot in ROT)
    chaves.append({"dono": c["dono"], "arquivo": c["arquivo"], "path": c["path"], "bytes": c["bytes"], "sha256_antes": c["sha256"],
                   "sha256_depois": snaps["depois"][0]["chaves"][i]["sha256"], "sha256_final": snaps["final"][0]["chaves"][i]["sha256"], "igual_nas_tres": iguais})
n_pyc = {rot: sum(1 for x in snaps[rot][1] if "__pycache__" in x[0] or x[0].endswith(".pyc")) for rot in ROT}
tudo_igual = b_ban["lista_identica_antes_depois_final"] and b_nos["lista_identica_antes_depois_final"] and all(c["igual_nas_tres"] for c in chaves)


def porta_no_ar():
    s = socket.socket()
    s.settimeout(1.5)
    try:
        return s.connect_ex(("127.0.0.1", 18777)) == 0
    finally:
        s.close()


# copia das listas (so' as da Bancada, pequenas, e a do Nos "antes" compactada) para a pasta de evidencia
os.makedirs(DEST_PROVA, exist_ok=True)
copiados = []
for rot in ROT:
    for nome in ("chaves_%s.json" % rot, "fp_bancada_%s.json" % rot) + (("fp_nos_antes.json.gz",) if rot == "antes" else ()):
        src, dst = os.path.join(SP, nome), os.path.join(DEST_PROVA, nome)
        if os.path.exists(dst):
            assert open(src, "rb").read() == open(dst, "rb").read(), "ja existe e difere: " + dst
        else:
            shutil.copyfile(src, dst)
        assert sha(src) == sha(dst)
        copiados.append({"path": dst, "bytes": os.path.getsize(dst), "sha256": sha(dst)})

prova = {
    "contrato": "PROVA_PRODUCAO_INTACTA_v395_pre_selo",
    "quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "o_que_se_prova": ("o ensaio pre_selo da v395 (esboco R3.5, --modo ensaio, bateria da v394) so' LEU a Bancada de producao e o Nos: a lista (caminho, tipo, tamanho, mtime_ns) de toda a arvore de cada um, "
                       "o sha256 do manifesto canonico da Bancada e o sha256 do um.py do Nos (e do selo, do core e do manifesto do kernel) sao os mesmos antes do ensaio, logo depois e depois da conferencia do recibo"),
    "ensaio": {"recibo": REC, "recibo_sha256": RSHA, "inicio_utc": r["inicio_utc"], "fim_utc": r["fim_utc"], "modo": r["modo"], "fase": r["fase"], "veredito": r["veredito"],
               "lancador": LANC, "lancador_sha256": sha(LANC), "script_de_fotografia": {"path": os.path.join(HERE, "snap_producao_v395.py"), "sha256": sha(os.path.join(HERE, "snap_producao_v395.py"))}},
    "producao_intacta": tudo_igual,
    "manifesto_canonico_da_bancada": next(c for c in chaves if c["arquivo"] == "canonical_contracts.json"),
    "um_py_do_nos": next(c for c in chaves if c["arquivo"] == "um.py"),
    "chaves": chaves,
    "bancada_de_producao": b_ban,
    "nos": b_nos,
    "arquivos_pyc_ou_pycache_na_bancada": n_pyc,
    "servico_da_bancada": {"porta_18777_no_ar_ao_gerar_esta_prova": porta_no_ar(),
                           "nota": "observacao por conexao TCP; esta tarefa nao parou nem religou o servico (nenhum comando de processo foi emitido)"},
    "copias_das_listas": copiados,
    "esta_tarefa_escreveu_so_em": [V + "\\bateria_pre_selo\\ (ensaio_1, scripts, stdout, conferencia, prova_producao)", V + "\\PINO_RECIBO_PRE_SELO_v395.json", V + "\\PROVA_PRODUCAO_INTACTA_v395_pre_selo.json",
                                   V + "\\bancada_B3_servico\\ (tres scripts derivados, sem executar)", "C:\\t\\vb12 (sandbox curto, apagado no fim)"],
    "escopo": "so leitura da producao; nada gravado na Bancada nem no Nos; NOT_FALSIFIED nao e creditacao; o gate nao se move",
}

# ---- o pino (as chaves do PINO_RECIBO_PRE_SELO_v394, mais as que a passagem do ensaio permite)
pv = r["bateria"].get("pinos_da_versao") or {}
adendo = (t12.get("adendo_de_pino") or {}).get("entrada_do_um_py")
motivos = list(conf["motivos_de_nao_ser_utilizavel"])
if not tudo_igual:
    motivos.append("a producao NAO esta intacta: ver PROVA_PRODUCAO_INTACTA_v395_pre_selo.json")
utilizavel = bool(conf["utilizavel_como_recibo_pre_selo_do_B_n"] and conf["esboco_aceita"] and conf["n_controles_como_esperado"] == len(conf["controles_negativos"])
                  and conf["n_condicoes_ok"] == conf["n_condicoes"] and bat["veredito"] == "BATERIA_PASSA" and r["veredito"].startswith("JA_SINCRONIZADA__ENSAIO") and RC == 0 and tudo_igual)
pino = dict(
    contrato="PINO_RECIBO_PRE_SELO_v395_ENSAIO",
    quando=r.get("inicio_utc"),
    path=REC,
    sha256=RSHA,
    bytes=len(raw),
    versao_nos=r["nos"]["UM_VERSION"],
    um_py_sha16_do_nos=r["nos"]["um_py"]["sha256"][:16],
    bancada_pina=dict(version=mant["version"], deployment_id=mant["deployment_id"], um_py_sha16=mant["um_py_pinado"][:16],
                      estado_do_contrato_instalado=mant["estado_do_contrato_instalado"]),
    comando_exato=cmd,
    lancador=LANC,
    lancador_sha256=sha(LANC),
    stdout=dict(path=STDOUT, sha256=sha(STDOUT)),
    esboco=dict(path=ESB, sha256=sha(ESB)),
    bateria=dict(path=BAT, sha256=sha(BAT), versao=r["bateria"].get("versao")),
    veredito=r["veredito"],
    codigo_de_saida=RC,
    contagens=dict(n=bat["n"], passa=bat["passa"], falha=bat["falha"], nao_executado=bat["nao_executado"], veredito_bateria=bat["veredito"]),
    por_teste={k: testes[k]["resultado"] for k in testes},
    t12_t13_t14_por_corrida=sub,
    adendo_de_pino_do_t12=adendo,
    pinos_da_versao={k: pv.get(k) for k in ("declarados", "conferidos_contra_o_nos_lido", "versao", "um_py_sha256", "um_py_bytes", "selo_sha256", "testes_que_pinam_o_um_py")},
    utilizavel_como_recibo_pre_selo_do_B_n=utilizavel,
    motivos_de_nao_ser_utilizavel=motivos,
    conferido_por=dict(script=os.path.join(HERE, "conferir_recibo_pre_selo_v395.py"), script_sha256=conf["script"]["sha256"], resultado_em=conf_p, resultado_sha256=sha(conf_p),
                       funcao="conferir_recibo_pre_selo do esboco R3.5 (ja_sincronizada=False; sem cadeia; selo e manifesto do kernel anteriores = v395/base_v394)",
                       esboco_aceita=conf["esboco_aceita"], condicoes="%d/%d" % (conf["n_condicoes_ok"], conf["n_condicoes"]),
                       controles_negativos="%d/%d recusados como esperado" % (conf["n_controles_como_esperado"], len(conf["controles_negativos"]))),
    valido_enquanto=dict(bancada_pina=dict(deployment_id=mant["deployment_id"], version=mant["version"], manifesto_sha256=mant["sha256"], um_py_sha256=mant["um_py_pinado"],
                                            seal_sha256=mant["seal_sha_pinado"]),
                         nota="um re-pino da producao antes do B(n) da v395 torna o recibo obsoleto: a conferencia do esboco o recusa"),
    nao_executados=dict(T17_LEAN_KERNEL=testes["T17_LEAN_KERNEL"]["detalhe"]),
    limites=[
        "T12/T13/T14 so' rodam no pre_selo (fases=['pre_selo'] na bateria): no B(n) da v395 valem por ESTE recibo, medidos contra o um.py v394 (o Nos de hoje), nao contra o um.py v395 [REAL: bateria v394 e rodar_bateria do esboco R3.5]",
        "o adendo de pino do T12 (pre-registro do F1.ATRATOR repinado na COPIA para o um.py medido) espera a ratificacao do dono da F1.ATRATOR [DECLARADO: RESULTADO_R3_5.md, residuos]",
        "o T17 e o nos_pinado do pos_selo so' se decidem com o selo, o manifesto do kernel e o recibo do kernel REAIS da v395",
    ],
    escrita_na_producao=dict(
        bancada_um=dict(antes=b_ban["fotografias"]["antes"]["n_entradas"], depois=b_ban["fotografias"]["final"]["n_entradas"], identico=b_ban["lista_identica_antes_depois_final"],
                        sha256_da_lista=b_ban["fotografias"]["final"]["sha256_da_lista"]),
        nos=dict(antes=b_nos["fotografias"]["antes"]["n_entradas"], depois=b_nos["fotografias"]["final"]["n_entradas"], identico=b_nos["lista_identica_antes_depois_final"],
                 sha256_da_lista=b_nos["fotografias"]["final"]["sha256_da_lista"]),
        criterio="lista (caminho, tipo, tamanho, mtime_ns) de toda a arvore, antes do ensaio, logo depois e depois da conferencia do recibo; prova completa em PROVA_PRODUCAO_INTACTA_v395_pre_selo.json",
    ),
    escopo="validade matematica e replay documental na face testada; nenhum dado observado; NOT_FALSIFIED nao e creditacao; o gate nao se move",
)


def gravar_novo(dest, obj):
    if os.path.exists(dest):
        raise SystemExit("ja existe, nao sobrescrevo: " + dest)
    dados = (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    with open(dest + ".tmp", "wb") as fh:
        fh.write(dados)
    if os.path.getsize(dest + ".tmp") != len(dados):
        raise SystemExit("tamanho do temporario nao confere: " + dest)
    os.replace(dest + ".tmp", dest)
    return dest


d_prova = gravar_novo(os.path.join(V, "PROVA_PRODUCAO_INTACTA_v395_pre_selo.json"), prova)
d_pino = gravar_novo(os.path.join(V, "PINO_RECIBO_PRE_SELO_v395.json"), pino)
print(d_pino, sha(d_pino))
print(d_prova, sha(d_prova))
print(json.dumps(pino["contagens"]), pino["veredito"], "utilizavel=%s" % pino["utilizavel_como_recibo_pre_selo_do_B_n"], "producao_intacta=%s" % tudo_igual)
