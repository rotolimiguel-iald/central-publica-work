# -*- coding: utf-8 -*-
"""adendo_notas_reinicio_v401.py -- ACRESCENTA ao NOTAS_PRE_SELO_v401.txt o adendo do refazimento do pre_selo depois do reinicio do PC (25/10 10:15). Backup de bytes (NOTAS_PRE_SELO_v401.txt.bak_20261025_102100) ja' feito;
nao reescreve o corpo anterior: so' acrescenta (o corpo continua valendo para a Tarefa 2 e para os scripts; recibo, pino, conferencia e prova do corpo ficam SUPERADOS pelos do adendo).
Tudo LIDO dos arquivos na hora. uso: python -I -B -X utf8 adendo_notas_reinicio_v401.py"""
import gzip
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
TS = "20261025_102100"
NOTAS = os.path.join(HERE, "NOTAS_PRE_SELO_v401.txt")
BAK = NOTAS + ".bak_" + TS
raw0 = open(NOTAS, "rb").read()
assert raw0 == open(BAK, "rb").read(), "o NOTAS mudou desde o backup"
assert b"ADENDO 25/10" not in raw0, "o adendo ja' foi acrescentado"
shaf = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
lj = lambda p: json.load(open(p, encoding="utf-8"))
pino_p = os.path.join(V, "PINO_RECIBO_PRE_SELO_v401.json")
prova_p = os.path.join(V, "PROVA_PRODUCAO_INTACTA_v401_pre_selo.json")
conf_p = os.path.join(HERE, "conferencia_pelo_esboco_v401.json")
pino, prova, conf = lj(pino_p), lj(prova_p), lj(conf_p)
rec = lj(pino["path"])
bat = rec["bateria_resultado"]
limp = lj(os.path.join(HERE, "LIMPEZA_SANDBOX_vb18.json"))
pino0 = lj(pino_p + ".bak_" + TS)
prova0 = lj(prova_p + ".bak_" + TS)
b_ban, b_nos = prova["bancada_de_producao"], prova["nos"]
# comparacao com a ultima fotografia ANTERIOR ao reinicio (prova_producao.bak_*: fp_bancada_final e fp_nos_antes) e com a nova
old = os.path.join(HERE, "prova_producao.bak_" + TS)
new = os.path.join(HERE, "prova_producao")
A = lj(os.path.join(old, "fp_bancada_final.json"))
B = lj(os.path.join(new, "fp_bancada_antes.json"))
NA = json.loads(gzip.decompress(open(os.path.join(old, "fp_nos_antes.json.gz"), "rb").read()).decode("utf-8"))
NB = json.loads(gzip.decompress(open(os.path.join(new, "fp_nos_antes.json.gz"), "rb").read()).decode("utf-8"))
DB = {z[0]: z for z in B}
DNB = {z[0]: z for z in NB}
pyc = lambda L: sum(1 for x in L if "__pycache__" in x[0] or x[0].endswith(".pyc"))
tmp = lambda L: [x[0] for x in L if x[0].endswith((".tmp", ".lock", ".pid", ".pyc.tmp")) or ".tmp" in x[0]]
t = ["", "ADENDO 25/10 (PC reiniciado as 10:15; a Bancada foi religada pelo servico, no ar desde 2026-10-25 10:18:32; pre_selo REFEITO; so' o que mudou)",
     "- Antes de rodar: producao ainda pina %s (manifesto sha256 %s) e o Nos e' o v400 (um.py sha16 %s): conferido na hora (canonical_contracts.json, GET /api/contratos e /api/estado: pronta=True, canonical_version v400)."
     % (pino["bancada_pina"]["deployment_id"], pino["valido_enquanto"]["bancada_pina"]["manifesto_sha256"], pino["um_py_sha16_do_nos"]),
     "- Conjunto anterior (pre-reinicio) preservado por renomeacao de bytes com sufixo .bak_%s: ensaio_1, etapa1_stdout.txt, conferencia_pelo_esboco_v401.json, LIMPEZA_SANDBOX_vb18.json, prova_producao, PINO_RECIBO_PRE_SELO_v401.json (sha256 %s), PROVA_PRODUCAO_INTACTA_v401_pre_selo.json (sha256 %s), NOTAS (copia). Estes ficam SUPERADOS pelos novos."
     % (TS, shaf(pino_p + ".bak_" + TS), shaf(prova_p + ".bak_" + TS)),
     "- Ensaio novo (mesmos scripts, --versao v400 --fase pre_selo --modo ensaio; %s a %s UTC): %s, RC %s, bateria %s (%d passa, %d falha, %d nao executado; T12/T13/T14 %s)."
     % (rec["inicio_utc"][11:19], rec["fim_utc"][11:19], rec["veredito"], pino["codigo_de_saida"], bat["veredito"], bat["passa"], bat["falha"], bat["nao_executado"], "/".join(pino["t12_t13_t14_por_corrida"].values())),
     "- Recibo novo %s sha256 %s (anterior %s). PINO_RECIBO_PRE_SELO_v401.json novo sha256 %s (anterior %s); utilizavel_como_recibo_pre_selo_do_B_n=%s; bancada_pina %s/%s."
     % (os.path.basename(pino["path"]), pino["sha256"], pino0["sha256"], shaf(pino_p), shaf(pino_p + ".bak_" + TS), pino["utilizavel_como_recibo_pre_selo_do_B_n"], pino["bancada_pina"]["deployment_id"], pino["bancada_pina"]["version"]),
     "- Conferencia pelo esboco R3.5: aceita=%s; %d/%d condicoes; %d/%d controles negativos; conferencia_pelo_esboco_v401.json sha16 %s."
     % (conf["esboco_aceita"], conf["n_condicoes_ok"], conf["n_condicoes"], conf["n_controles_como_esperado"], len(conf["controles_negativos"]), shaf(conf_p)[:16]),
     "- Producao: Bancada %d/%d/%d entradas (antes/depois/final), Nos %d/%d/%d; listas iguais=%s e %s; chaves iguais nas tres fotografias=%s; producao_intacta=%s; PROVA_PRODUCAO_INTACTA_v401_pre_selo.json novo sha256 %s (anterior %s)."
     % (b_ban["fotografias"]["antes"]["n_entradas"], b_ban["fotografias"]["depois"]["n_entradas"], b_ban["fotografias"]["final"]["n_entradas"], b_nos["fotografias"]["antes"]["n_entradas"], b_nos["fotografias"]["depois"]["n_entradas"], b_nos["fotografias"]["final"]["n_entradas"],
        b_ban["lista_identica_antes_depois_final"], b_nos["lista_identica_antes_depois_final"], all(c["igual_nas_tres"] for c in prova["chaves"]), prova["producao_intacta"], shaf(prova_p), shaf(prova_p + ".bak_" + TS)),
     "- O QUE O REINICIO DEIXOU NA PRODUCAO (lista caminho/tipo/tamanho/mtime da ultima fotografia pre-reinicio contra a primeira pos-reinicio): Bancada adicionados %d, removidos %d, alterados %d; Nos adicionados %d, removidos %d, alterados %d; .pyc/__pycache__ na Bancada: %d antes, %d depois (os 25 ja' existiam); arquivos .tmp/.lock/.pid na Bancada: %s. Nada foi apagado nem alterado por esta tarefa; a lista da Bancada e' a MESMA (sha256 da lista %s) antes e depois do reinicio e da religacao do servico."
     % (len(set(x[0] for x in B) - set(x[0] for x in A)), len(set(x[0] for x in A) - set(x[0] for x in B)), sum(1 for x in A if x[0] in DB and DB[x[0]] != x),
        len(set(x[0] for x in NB) - set(x[0] for x in NA)), len(set(x[0] for x in NA) - set(x[0] for x in NB)), sum(1 for x in NA if x[0] in DNB and DNB[x[0]] != x),
        pyc(A), pyc(B), tmp(B) or "nenhum", prova["bancada_de_producao"]["fotografias"]["final"]["sha256_da_lista"]),
     "- Sandbox %s apagado de novo por limpar_sandbox_vb18.py (%d arquivos, %d pastas, juncoes/links antes de apagar: %d; existe depois: %s; irmaos de C:\\t iguais: %s). Tarefa 2 (servico) NAO foi refeita: os scripts nao dependem do recibo pre_selo; nada executado."
     % (limp["alvo"], limp["arquivos"], limp["pastas"], limp["juncoes_ou_links_antes_de_apagar"], limp["existe_depois"], limp["irmaos_iguais"])]
novo = raw0 + ("\n".join(t) + "\n").encode("utf-8")
with open(NOTAS + ".tmp", "wb") as fh:
    fh.write(novo)
assert os.path.getsize(NOTAS + ".tmp") == len(novo) > len(raw0)
os.replace(NOTAS + ".tmp", NOTAS)
print(NOTAS, len(raw0), "->", len(novo))
print("\n".join(t[1:]))
