# -*- coding: utf-8 -*-
"""gerar_pino_recibo_pre_selo_v400.py -- escreve PINO_RECIBO_PRE_SELO_v400.json: o PINO do recibo pre_selo do B(n) da v400. O recibo e' o da CADEIA v399 (ensaio_1: gerado e pinado em 24/10 08:58-09:00, em modo ensaio, ANTES da instalacao da v399,
com a producao so' lida), sobre o um.py v398 que a Bancada de producao AINDA pina; a v400 o REUSA porque um recibo novo e' impossivel sem tocar no Nos (medido: salto_r3_4\\SALTO_R3_4_MEDIDO_v400.json). Tudo LIDO dos arquivos por script:
o pino da v399 (PINO_RECIBO_PRE_SELO_v399.json), o recibo em disco, a conferencia pelo PROPRIO esboco R3.5 (bateria_pre_selo\\conferencia_pelo_esboco_v400.json), as fotografias antes/depois da producao (C:\\t\\vb17\\snap) e a medicao do salto.
Recusa se: o recibo em disco != o pino da v399; a conferencia nao aceita; o esboco != o pinado; as listas da producao mudaram. uso: python -I -B -X utf8 gerar_pino_recibo_pre_selo_v400.py"""
import datetime, gzip, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
lj = lambda p: json.load(open(p, encoding="utf-8"))
P9 = lj(os.path.join(DL.V399, "PINO_RECIBO_PRE_SELO_v399.json"))
rb = open(P9["path"], "rb").read()
assert sha(rb) == P9["sha256"], "o recibo pre_selo da v399 mudou desde o pino da v399"
CONF_P = os.path.join(HERE, "bateria_pre_selo", "conferencia_pelo_esboco_v400.json")
conf = lj(CONF_P)
assert conf["esboco_aceita"] is True and conf["utilizavel_como_recibo_pre_selo_do_B_n"] is True and conf["recibo"]["sha256"] == P9["sha256"], "a conferencia pelo esboco nao aceita este recibo"
assert conf["esboco"]["sha256"] == P9["esboco"]["sha256"], "o esboco da conferencia != o do recibo"
SALTO_P = os.path.join(HERE, "salto_r3_4", "SALTO_R3_4_MEDIDO_v400.json")
salto = lj(SALTO_P)
assert salto["veredito"].startswith("SALTO_R3_4_IMPOSSIVEL"), "a medicao do salto nao confirmou"
SN = "C:/t/vb17/snap"
fa, fd = json.load(open(SN + "/fp_bancada_antes.json")), json.load(open(SN + "/fp_bancada_depois.json"))
na, nd = json.loads(gzip.decompress(open(SN + "/fp_nos_antes.json.gz", "rb").read())), json.loads(gzip.decompress(open(SN + "/fp_nos_depois.json.gz", "rb").read()))
lista_sha = lambda L: hashlib.sha256("".join("%s\t%s\t%d\t%d\n" % (r, t, s, m) for r, t, s, m in L).encode("utf-8")).hexdigest()
esc = {"bancada_um": {"antes": len(fa), "depois": len(fd), "identico": fa == fd, "sha256_da_lista": lista_sha(fa)}, "nos": {"antes": len(na), "depois": len(nd), "identico": na == nd, "sha256_da_lista": lista_sha(na)},
       "criterio": "lista (caminho, tipo, tamanho, mtime_ns) de toda a arvore, antes da conferencia e logo depois (snap_producao_v400.py); a Bancada tem a MESMA lista da fotografia do recibo da v399 (c0a6671c...: nada foi gravado nela desde 24/10 08:58)"}
assert esc["bancada_um"]["identico"] and esc["nos"]["identico"], ("a producao ou o Nos mudaram durante a conferencia", esc)
assert esc["bancada_um"]["sha256_da_lista"] == P9["escrita_na_producao"]["bancada_um"]["sha256_da_lista"], "a Bancada de producao mudou desde o recibo da v399 (o recibo e' obsoleto)"
bp = conf["bancada_de_producao_lida"]
assert bp["deployment_id"] == P9["bancada_pina"]["deployment_id"] and bp["version"] == "v398", ("a Bancada de producao nao pina mais a v398", bp)
pino = dict(P9)
pino["contrato"] = "PINO_RECIBO_PRE_SELO_v400_REUSO_DO_RECIBO_DA_CADEIA_v399"
pino["quando"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
pino["origem"] = {"cadeia": "v399", "pino_da_v399": {"path": os.path.join(DL.V399, "PINO_RECIBO_PRE_SELO_v399.json"), "sha256": sha(open(os.path.join(DL.V399, "PINO_RECIBO_PRE_SELO_v399.json"), "rb").read())},
                  "gerado_em": P9["quando"], "modo": "ensaio (producao so' lida)", "antes_da_instalacao_da_v399": True,
                  "nota": "o recibo e' do um.py v398 (o que a Bancada de producao ainda pina), nao do v399: o B(n) da v400 e' um passo simples v398 -> v400 e o esboco R3.5 confere o recibo contra o que a Bancada pina"}
pino["por_que_e_reusado"] = ["o esboco R3.5 so' gera um pre_selo lendo o Nos que o manifesto da Bancada pina (--producao exige o caminho real) e o Nos ja' e' a v399: ler_nos(Nos, v399) RECUSA (ALPHA_LINHA_NAO_UNICA: 2 linhas nao indentadas, a mensagem EXATA do recibo da Bancada) e ler_nos(Nos, v398) RECUSA (SELO_VERSAO_DIFERENTE): "
                             "nenhum recibo pre_selo NOVO e' possivel sem tocar no Nos (medido em %s)" % os.path.relpath(SALTO_P, HERE),
                             "o salto declarado R3.4 tampouco: a cadeia de selos v398 -> v399 e' recusada no elo v399 (CADEIA_DE_SELOS_UM_PY_COM_DECLARACAO_NAO_UNICA)",
                             "T12/T13/T14 so' rodam no pre_selo e pinam o um.py que a Bancada pina (v398): o recibo da v399 os cobre"]
pino["utilizavel_como_recibo_pre_selo_do_B_n"] = True
pino["motivos_de_nao_ser_utilizavel"] = []
pino["conferido_por"] = {"script": os.path.join(HERE, "bateria_pre_selo", "conferir_recibo_pre_selo_v400.py"), "script_sha256": sha(open(os.path.join(HERE, "bateria_pre_selo", "conferir_recibo_pre_selo_v400.py"), "rb").read()),
                         "resultado_em": CONF_P, "resultado_sha256": sha(open(CONF_P, "rb").read()), "funcao": "conferir_recibo_pre_selo do esboco R3.5 (ja_sincronizada=False; sem cadeia; selo e manifesto do kernel anteriores = v400/base_v398), contra a Bancada de producao LIDA em %s" % conf["bancada_de_producao_lida"]["deployment_id"],
                         "esboco_aceita": conf["esboco_aceita"], "condicoes": "%d/%d" % (conf["n_condicoes_ok"], conf["n_condicoes"]), "controles_negativos": "%d/%d recusados como esperado" % (conf["n_controles_como_esperado"], len(conf["controles_negativos"]))}
pino["valido_enquanto"] = {"bancada_pina": {"deployment_id": bp["deployment_id"], "version": bp["version"], "manifesto_sha256": bp["manifesto_sha256"], "um_py_sha256": bp["um_py_pinado"], "seal_sha256": bp["seal_sha_pinado"]},
                           "nota": "um re-pino da producao antes do B(n) da v400 torna o recibo obsoleto: a conferencia do esboco o recusa"}
pino["salto_r3_4_medido"] = {"arquivo": SALTO_P, "sha256": sha(open(SALTO_P, "rb").read()), "veredito": salto["veredito"]}
pino["limites"] = ["T12/T13/T14 so' rodam no pre_selo (fases=['pre_selo'] na bateria): no B(n) da v400 valem por ESTE recibo, medidos contra o um.py v398 (o que a Bancada pina), nao contra o v399 nem o v400 [REAL: bateria v398 e rodar_bateria do esboco R3.5]",
                   "o adendo de pino do T12 espera a ratificacao do dono da F1.ATRATOR [DECLARADO: RESULTADO_R3_5.md, residuos]",
                   "o T17 e o nos_pinado do pos_selo so' se decidem com o selo, o manifesto do kernel e o recibo do kernel REAIS da v400"]
pino["escrita_na_producao"] = esc
pino["escopo"] = "validade matematica e replay documental na face testada; nenhum dado observado; NOT_FALSIFIED nao e creditacao; o gate nao se move"
dest = os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v400.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
open(dest + ".tmp", "w", encoding="utf-8").write(json.dumps(pino, ensure_ascii=False, indent=1)); os.replace(dest + ".tmp", dest)
print(json.dumps({"arquivo": dest, "recibo_sha256": pino["sha256"][:16], "utilizavel": pino["utilizavel_como_recibo_pre_selo_do_B_n"], "bancada_lista_identica": esc["bancada_um"]["identico"], "nos_lista_identica": esc["nos"]["identico"],
                  "bancada_sha_da_lista": esc["bancada_um"]["sha256_da_lista"][:16], "salto": salto["veredito"]}, ensure_ascii=False))
