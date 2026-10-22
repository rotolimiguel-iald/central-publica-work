# -*- coding: utf-8 -*-
"""v394, elo B(n), fase pre_selo: gera PINO_RECIBO_PRE_SELO_v394.json a partir do recibo do ensaio (tudo LIDO dos arquivos, por script).
Nao grava nada na Bancada, no Nos nem no tunel. Escreve so o PINO (um arquivo)."""
import glob
import hashlib
import json
import os
import sys


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


V = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo", "v394")
ENS = os.path.join(V, "bateria_pre_selo", "ensaio_1")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
BAN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
V392 = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo", "v392", "vinculo")
SP = sys.argv[1]  # pasta dos instantaneos (antes/depois) da Bancada e do Nos

rec_p = glob.glob(os.path.join(ENS, "RECIBO_SINCRONIZACAO_v393_*.json"))
assert len(rec_p) == 1, rec_p
rec_p = rec_p[0]
r = json.load(open(rec_p, encoding="utf-8"))
bat = r["bateria_resultado"]
testes = {t["id"]: t for t in bat["testes"]}

t12 = json.load(open(os.path.join(ENS, "recibos", "T12_T13_T14_ATRATOR.json"), encoding="utf-8"))
sub = {k: ("PASSA" if v.get("passa") else "FALHA") for k, v in t12["runs"].items()}

# pino que o pre-registro congelado do F1.ATRATOR grava para o um.py (lido do arquivo)
pr = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.ATRATOR", "PREREGISTRO_R1.json")
prj = json.load(open(pr, encoding="utf-8"))
pin_um = [x for x in prj["source_pins"] if os.path.basename(x["path"]) == "um.py"][0]
pinos_ok, pinos_mudou = 0, []
for x in prj["source_pins"]:
    if sha(x["path"]) == x["sha256"]:
        pinos_ok += 1
    else:
        pinos_mudou.append(x["path"])


def fp_igual(a, b):
    ja = json.load(open(os.path.join(SP, a), encoding="utf-8"))
    jb = json.load(open(os.path.join(SP, b), encoding="utf-8"))
    return dict(antes=len(ja), depois=len(jb), identico=(ja == jb))


esboco = os.path.join(V392, "sincronizar_bancada.py")
bateria = os.path.join(V392, "BATERIA_VINCULO.json")
stdout = os.path.join(V, "bateria_pre_selo", "etapa1_stdout.txt")

pino = dict(
    contrato="PINO_RECIBO_PRE_SELO_v394_ENSAIO",
    quando=r.get("inicio_utc"),
    path=rec_p,
    sha256=sha(rec_p),
    bytes=os.path.getsize(rec_p),
    versao_nos=r["nos"]["UM_VERSION"],
    um_py_sha16_do_nos=r["nos"]["um_py"]["sha256"][:16],
    bancada_pina=dict(version=r["manifesto_anterior"]["version"], deployment_id=r["manifesto_anterior"]["deployment_id"],
                      um_py_sha16=r["manifesto_anterior"]["um_py_pinado"][:16], estado_do_contrato_instalado=r["manifesto_anterior"]["estado_do_contrato_instalado"]),
    comando_exato=("python -I -B -X utf8 \"%s\" --bancada \"%s\" --producao --nos \"%s\" --versao v393 --fase pre_selo --modo ensaio "
                   "--bateria \"%s\" --bateria-sha256 %s --saida \"%s\"") % (esboco, BAN, NOS, bateria, sha(bateria), ENS),
    lancador=os.path.join(V, "bateria_pre_selo", "rodar_ensaio_1_pre_selo_v394.sh"),
    stdout=dict(path=stdout, sha256=sha(stdout)),
    esboco=dict(path=esboco, sha256=sha(esboco)),
    bateria=dict(path=bateria, sha256=sha(bateria), versao=bat and r["bateria"].get("versao")),
    veredito=r["veredito"],
    codigo_de_saida=3,
    contagens=dict(n=bat["n"], passa=bat["passa"], falha=bat["falha"], nao_executado=bat["nao_executado"], veredito_bateria=bat["veredito"]),
    por_teste={k: testes[k]["resultado"] for k in testes},
    t12_t13_t14_por_corrida=sub,
    causa_da_falha=dict(
        teste="T12_T13_T14_ATRATOR (T12 e T13 FALHAM, T14 PASSA)",
        erro_t12="ValueError: Source pin changed: <Nos>\\um.py (run_optical_r3.py, check_preregistered_sources)",
        erro_t13="ValueError: RECUSA_SOURCE_CHANGED: <Nos>\\um.py (run_adendo1_r1.py, source_snapshot)",
        pino_do_preregistro_para_o_um_py=dict(path=pin_um["path"], sha256=pin_um["sha256"], sha16=pin_um["sha256"][:16]),
        um_py_do_nos_agora_sha16=sha(os.path.join(NOS, "um.py"))[:16],
        outros_pinos_do_preregistro=dict(conferem=pinos_ok, total=len(prj["source_pins"]), mudaram=pinos_mudou),
        leitura="os runners congelados do F1.ATRATOR (sha pinados na bateria R2) exigem o um.py v391 no caminho do Nos; so passam enquanto o Nos tem a v391",
    ),
    utilizavel_como_recibo_pre_selo_do_B_n=False,
    motivos_de_nao_ser_utilizavel=[
        "bateria_resultado.veredito=BATERIA_FALHOU (conferir_recibo_pre_selo exige BATERIA_PASSA)",
        "veredito=%s (conferir_recibo_pre_selo exige prefixo JA_SINCRONIZADA__ENSAIO)" % r["veredito"],
        "versao_alvo=v393 mas a Bancada pina v392 (conferir_recibo_pre_selo exige versao_alvo == versao pinada na Bancada no momento do B(n))",
        "nos.um_py do recibo = v393 mas o um.py antes pinado pela Bancada = v392 (b590c0aa80055e2a)",
    ],
    nao_executados_fora_da_bateria_R2=dict(T18_T22="NAO_EXECUTADO: nao fazem parte da bateria R2 do esboco; o conjunto do precedente v392 (rodada2/p12/p12_replays.py) grava na pasta v392 e no sandbox C:/t/p12, fora da area de escrita desta tarefa; T21/T22 leem os bytes do um.py do Nos e comparam pins com o arquivo (v391), resultado contra a v393 nao medido"),
    escrita_na_producao=dict(
        bancada_um=fp_igual("fp_bancada_antes.json", "fp_bancada_depois.json"),
        nos=fp_igual("fp_nos_antes.json", "fp_nos_depois.json"),
        criterio="lista (caminho, tamanho, mtime_ns) de toda a arvore antes e depois do ensaio",
    ),
    escopo="validade matematica e replay documental na face testada; nenhum dado observado; NOT_FALSIFIED nao e creditacao; o gate nao se move",
)
dest = os.path.join(V, "PINO_RECIBO_PRE_SELO_v394.json")
data = (json.dumps(pino, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
if os.path.exists(dest):
    raise SystemExit("PINO ja existe: " + dest)
tmp = dest + ".tmp"
with open(tmp, "wb") as fh:
    fh.write(data)
if os.path.getsize(tmp) != len(data):
    raise SystemExit("tamanho do temporario nao confere")
os.replace(tmp, dest)
print(dest, sha(dest))
print(json.dumps(pino["contagens"]), pino["veredito"])
