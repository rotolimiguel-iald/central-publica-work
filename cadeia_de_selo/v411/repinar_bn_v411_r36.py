# -*- coding: utf-8 -*-
# [AUTORAL v411, 13/11/2026, claude-construtor-r36 (a servico da gerencia c1)] repina o PINOS_BN_v411.json para a R3.6: o recibo do kernel novo (contrato KERNEL_RECIBO_R3_6) e o esboco R3_6
"""repinar_bn_v411_r36.py -- atualiza PINOS_BN_v411.json depois de R3_6\\controles_r3_6.py ter passado inteiro (NAO roda o diff_e_pinos_v411.py): (1) `kernel_recibo`: path igual, sha256 e bytes RELIDOS do
arquivo, contrato, n_pedras, n_modulos e modulos_de_auditoria como o gerador (diff_e_pinos_v411.py, chave kernel_recibo) os escreve; (2) acrescenta `esboco_R3_6` {path, sha256, bytes} (R3_6\\sincronizar_bancada.py), logo
depois de `esboco_R3_5`, que FICA; (3) acrescenta `nota_r36`. O resto do arquivo nao muda (conferido). Formato preservado: indent=1, ensure_ascii=False, fim de linha CRLF (o gerador escreve em modo texto no Windows, sem
quebra final); o ensaio a seco confere que reescrever o arquivo SEM mudar nada reproduz os bytes atuais. Backup de BYTES `.bak_<AAAAMMDD_HHMMSS>_r36`; escrita por temporario + os.replace; confere depois.
Se R3_6\\CONTROLES_R3_6.json nao traz o veredito R3_6_CONFERIDA_POR_SCRIPT, PARA. uso: python -B -X utf8 repinar_bn_v411_r36.py [--executar]"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(p, "rb").read()
sha = lambda b: hashlib.sha256(b).hexdigest()
EXECUTAR = "--executar" in sys.argv[1:]
PIN_P = os.path.join(HERE, "PINOS_BN_v411.json")
R36 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "bancada_vinculo_12out", "R3_6")
ESB6 = os.path.join(R36, "sincronizar_bancada.py")
CTRL = os.path.join(R36, "CONTROLES_R3_6.json")
KR_P = os.path.join(HERE, "kernel", "KERNEL_RECIBO_v411.json")
ctrl = json.load(open(CTRL, encoding="utf-8"))
assert ctrl.get("veredito") == "R3_6_CONFERIDA_POR_SCRIPT", ("os controles da R3.6 nao passaram inteiros: PARO", ctrl.get("veredito"))
assert ctrl["modulos"]["R3_6"]["sha256"] == sha(rd(ESB6)), "o esboco R3_6 mudou depois dos controles: rodar controles_r3_6.py de novo"
raw = rd(PIN_P)
pin = json.loads(raw.decode("utf-8"))
dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1).replace("\n", "\r\n").encode("utf-8")
assert dump(pin) == raw, "o formato do PINOS_BN_v411.json nao e' o que o script reproduz (CRLF, indent=1, ensure_ascii=False, sem quebra final)"
kr = json.loads(rd(KR_P).decode("utf-8"))
assert kr["contrato"] == "KERNEL_RECIBO_R3_6" and kr["versao"] == "v411" and kr["pedras"] == [] and kr["rc"] == 0 and kr.get("versao_sem_pedra_nova") is True, "o recibo do kernel nao e' o R3_6 da v411"
assert os.path.normcase(os.path.normpath(pin["kernel_recibo"]["path"])) == os.path.normcase(os.path.normpath(KR_P)), "o pino kernel_recibo aponta outro arquivo"
assert ctrl["insumos"]["recibo_v411"]["sha256"] == sha(rd(KR_P)), "o recibo do kernel mudou depois dos controles: rodar controles_r3_6.py de novo"
novo = {}
for k_, v_ in pin.items():
    if k_ == "kernel_recibo":
        novo[k_] = {"path": v_["path"], "sha256": sha(rd(KR_P)), "bytes": os.path.getsize(KR_P), "contrato": kr["contrato"], "n_pedras": len(kr["pedras"]), "n_modulos": len(kr["pedras"]), "modulos_de_auditoria": kr.get("modulos_de_auditoria", [])}
    else:
        novo[k_] = v_
    if k_ == "esboco_R3_5":
        assert "esboco_R3_6" not in pin, "o pino esboco_R3_6 ja' existe"
        novo["esboco_R3_6"] = {"path": ESB6, "sha256": sha(rd(ESB6)), "bytes": os.path.getsize(ESB6)}
assert "esboco_R3_6" in novo and novo["esboco_R3_5"] == pin["esboco_R3_5"]
novo["nota_r36"] = ("[R3.6, 13/11/2026, repinagem por repinar_bn_v411_r36.py] o ensaio do B(n) da v411 parou no T17 porque a R3.5 nao tem caminho para uma versao SEM modulo Lean novo; o kernel_recibo agora e' do contrato KERNEL_RECIBO_R3_6 "
                    "(sha256 e bytes relidos do arquivo; o recibo tem formal_files_antes, nos_kernel_impressao, toolchain.lake_version medida e a arvore so-fontes C:/t/k411c/arvore) e o esboco que a cadeia usa passa a ser o esboco_R3_6 "
                    "(R3_6\\sincronizar_bancada.py, conferido por R3_6\\controles_r3_6.py -> CONTROLES_R3_6.json, veredito %s). O esboco_R3_5 FICA como registro (o guarda estatico e o conferidor da preparacao ainda leem a R3_5: os regex sao os mesmos). "
                    "Os demais pinos nao mudaram." % ctrl["veredito"])
mudou = sorted(k for k in novo if novo.get(k) != pin.get(k))
assert mudou == sorted(["kernel_recibo", "esboco_R3_6", "nota_r36"]), ("mudou mais do que devia", mudou)
novo_raw = dump(novo)
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
print(json.dumps({"modo": "EXECUTAR" if EXECUTAR else "ENSAIO_A_SECO", "chaves_que_mudam": mudou, "pinos_atual": {"bytes": len(raw), "sha256": sha(raw)[:16]}, "pinos_novo": {"bytes": len(novo_raw), "sha256": sha(novo_raw)[:16]},
                  "kernel_recibo": {"sha256": novo["kernel_recibo"]["sha256"][:16], "bytes": novo["kernel_recibo"]["bytes"]}, "esboco_R3_6": {"sha256": novo["esboco_R3_6"]["sha256"][:16], "bytes": novo["esboco_R3_6"]["bytes"]}}, ensure_ascii=False))
if not EXECUTAR:
    print("ensaio a seco: nada gravado (use --executar)"); sys.exit(0)
bak = PIN_P + ".bak_" + TS + "_r36"
assert not os.path.exists(bak)
open(bak, "wb").write(raw); assert rd(bak) == raw, "o backup nao e' copia de bytes"
open(PIN_P + ".tmp", "wb").write(novo_raw); assert os.path.getsize(PIN_P + ".tmp") == len(novo_raw)
os.replace(PIN_P + ".tmp", PIN_P)
depois = rd(PIN_P); assert depois == novo_raw and len(depois) > len(raw), "o PINOS_BN gravado nao e' o esperado (restaurar do backup %s)" % bak
chk = json.loads(depois.decode("utf-8"))
bad = [k for k in ("kernel_recibo", "esboco_R3_5", "esboco_R3_6") if sha(rd(chk[k]["path"])) != chk[k]["sha256"]]
assert not bad, ("pino que diverge do arquivo", bad)
print(json.dumps({"gravado": PIN_P, "bytes": len(depois), "sha256": sha(depois), "backup": bak, "backup_sha256": sha(rd(bak))}, ensure_ascii=False))
