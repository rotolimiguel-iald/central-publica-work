# -*- coding: utf-8 -*-
"""fundir_pinos_bn_r35.py (R3.5, 19/10/2026) -- FUNDE no PINOS_BN_v394.json VIVO (work/cadeia_de_selo/v394) so o que e da R3.4/R3.5: o esboco R3.5, o esboco R3.4 que gerou o recibo pre_selo, o gerador e o driver da
bateria por versao, o pino do um.py da bateria v393, a cadeia de selos v392->v393, o recibo pre_selo (R3.4, gerado antes da instalacao da v394) e o recibo do kernel R3_4 (com modulos_de_auditoria). NAO copia
a copia da R3.4 (o candidato e os esperados dela estao vencidos): candidato, esperados, criterios e pins_do_candidato ficam como o arquivo vivo os tem. O que a fusao substitui (esboco R3.3, bateria R2, ensaio
pre_selo da R3.3, recibo do kernel R3_2, nota) fica guardado AO LADO, em chaves *_substituido / *_original / nota_anterior. Nenhum hash e digitado: todo sha256 e lido do arquivo.
Backup de BYTES do vivo antes (.bak_<AAAAMMDD_HHMMSS> na mesma pasta), escrita por temporario + os.replace, e releitura. Preserva o formato do vivo (json indent=1, ensure_ascii=False, CRLF, sem newline final).
uso: python -I -B -X utf8 fundir_pinos_bn_r35.py [--ensaio] [--sha-vivo-esperado <prefixo hex>]    (--ensaio: so imprime o resultado; nada e escrito)"""
import argparse
import datetime
import hashlib
import json
import os
import sys
sys.dont_write_bytecode = True
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
R34 = AQUI.parent / "R3_4"
CADEIA = AQUI.parent.parent / "cadeia_de_selo"
V394 = CADEIA / "v394"
VIVO = V394 / "PINOS_BN_v394.json"

ap = argparse.ArgumentParser()
ap.add_argument("--ensaio", action="store_true")
ap.add_argument("--sha-vivo-esperado", default=None)
a = ap.parse_args()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pinar(p, **extra):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=str(p).replace("/", chr(92)), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b), **extra)


def J(p):
    return json.loads(Path(p).read_bytes())


raw_vivo = VIVO.read_bytes()
sha_vivo = hashlib.sha256(raw_vivo).hexdigest()
if a.sha_vivo_esperado and not sha_vivo.startswith(a.sha_vivo_esperado.lower()):
    raise SystemExit("O PINOS_BN vivo mudou: sha256 %s nao comeca por %s (a fusao parte do vivo; releia)" % (sha_vivo, a.sha_vivo_esperado))
vivo = json.loads(raw_vivo.decode("utf-8"))
chaves_vivas = ["criterios", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "esboco_R3_3", "bateria", "recibo_pre_selo", "nota"]
assert list(vivo.keys()) == chaves_vivas, ("o vivo tem outras chaves; releia antes de fundir", list(vivo.keys()))
# o que ja esta no vivo precisa conferir com o disco (o candidato, os esperados, os criterios e os pins ficam como estao)
for k in ("criterios", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "esboco_R3_3", "bateria"):
    assert sha(vivo[k]["path"]) == vivo[k]["sha256"], "o pino vivo %s diverge do arquivo" % k

# ---- as pecas da R3.4/R3.5 (tudo lido do disco)
pino_rec = J(R34 / "PINO_RECIBO_PRE_SELO_v394_R3_4.json")
rec_path = R34 / "recibo_pre_selo_v394" / Path(pino_rec["path"]).name
assert sha(rec_path) == pino_rec["sha256"], "o recibo pre_selo nao e o que o pino registra"
assert pino_rec["utilizavel_como_recibo_pre_selo_do_B_n"] is True and pino_rec["veredito"].startswith("REPINADA_B4__SALTO_v392_v393__ENSAIO")
cad_path = R34 / "CADEIA_DE_SELOS_v394.json"
cad = J(cad_path)
kr_path = R34 / "KERNEL_RECIBO_v394_R3_4.json"
kr = J(kr_path)
assert kr["contrato"] == "KERNEL_RECIBO_R3_4" and kr["derivado_de"]["sha256"] == vivo["kernel_recibo"]["sha256"], "o recibo do kernel R3_4 nao deriva do recibo vivo (R3_2) que o PINOS_BN pina"
bat_path = R34 / "BATERIA_VINCULO_v393.json"
esb5 = AQUI / "sincronizar_bancada.py"
ger_path = AQUI / "gerar_bateria_r3_4.py"
drv_path = AQUI / "bateria_r3_4" / "t12_t14_atrator_r3_4.py"
# o que a R3.5 copiou da R3.4 tem de ser, byte a byte, o da R3.4 (cadeia, bateria, pino, recibo do kernel, driver, gerador)
for rel in ("BATERIA_VINCULO_v393.json", "CADEIA_DE_SELOS_v394.json", "KERNEL_RECIBO_v394_R3_4.json", "PINO_RECIBO_PRE_SELO_v394_R3_4.json", "gerar_bateria_r3_4.py", "gerar_cadeia_de_selos.py", "derivar_recibo_kernel_r3_4.py",
            "bateria_r3_4/t12_t14_atrator_r3_4.py", "bateria_r3_4/PINO_UM_PY_v393.json"):
    assert sha(AQUI / rel) == sha(R34 / rel), "R3_5/%s difere do R3_4" % rel

novo = {}
novo["criterios"] = vivo["criterios"]
novo["kernel_recibo"] = pinar(kr_path, contrato=kr["contrato"], modulos_de_auditoria=kr["modulos_de_auditoria"], n_pedras=len(kr["pedras"]),
                              derivado_de=dict(path=vivo["kernel_recibo"]["path"], sha256=vivo["kernel_recibo"]["sha256"]), por="derivar_recibo_kernel_r3_4.py (R3.4)",
                              nota="o recibo do kernel do pos_selo: o vivo (R3_2) mais contrato, derivado_de e modulos_de_auditoria (os 3 NetworkProofAudit); o R3_2 vivo nao passa na N1k da R3.4/R3.5")
novo["kernel_recibo_R3_2_original"] = vivo["kernel_recibo"]
novo["candidato"] = vivo["candidato"]
novo["esperados"] = vivo["esperados"]
novo["pins_do_candidato"] = vivo["pins_do_candidato"]
novo["esboco_R3_5"] = pinar(esb5, revisao="R3.5 (19/10/2026)", nota="o esboco do B(n) pos_selo da v394 (salto v392 -> v394); R3.4 + a lista de PERMISSAO estrita do modulo de auditoria")
novo["esboco_R3_4_do_recibo_pre_selo"] = pinar(R34 / "sincronizar_bancada.py", revisao="R3.4 (19/10/2026)", nota="o esboco que gerou o recibo pre_selo (script_sha256 do recibo); a R3.5 aceita esse recibo")
novo["esboco_R3_3_substituido"] = vivo["esboco_R3_3"]
novo["gerador_bateria"] = pinar(ger_path, nota="gera a bateria POR VERSAO (depois do selo) a partir dos pinos da cadeia (PINOS_BN: candidato == o um.py do Nos)")
novo["driver_t12_t14"] = pinar(drv_path, nota="o T12/T13/T14: repina o um.py do pre-registro congelado da F1.ATRATOR NA COPIA do replay (adendo declarado no recibo)")
novo["bateria"] = pinar(bat_path, versao=J(bat_path)["versao_bateria"], fase="pre_selo da v394 (Nos v393 instalado)",
                        nota="a bateria do PRE_SELO (a do recibo 0d82d598...); a do POS_SELO e GERADA pelo chain depois do selo (gerador_bateria + bateria_base_R2 + este PINOS_BN) e pinada ao lado em bateria_pos_selo/PINOS_BATERIA_v394.json")
novo["bateria_R2_substituida"] = vivo["bateria"]
novo["bateria_base_R2"] = dict(vivo["bateria"], nota="a base R2 da qual o gerador parte (o mesmo arquivo e sha256 do pino R2 substituido)")
novo["pino_um_py_da_bateria"] = pinar(AQUI / "bateria_r3_4" / "PINO_UM_PY_v393.json", nota="o pino do um.py da bateria v393 (pre_selo)")
novo["cadeia_de_selos"] = pinar(cad_path, contrato=cad["contrato"], n_elos=len(cad["elos"]), versoes=[e["versao"] for e in cad["elos"]], nota="a cadeia de selos v392->v393 (consistencia por hash, nao autenticidade)")
novo["recibo_pre_selo"] = pinar(rec_path, versao_nos=pino_rec["versao_nos"], veredito=pino_rec["veredito"], utilizavel_como_recibo_pre_selo_do_B_n=pino_rec["utilizavel_como_recibo_pre_selo_do_B_n"],
                                pino_do_pino=pinar(R34 / "PINO_RECIBO_PRE_SELO_v394_R3_4.json"), com_salto=dict(de=pino_rec["salto"]["de"]["versao"], ate=pino_rec["salto"]["ate"]["versao"], versoes_puladas=pino_rec["salto"]["versoes_puladas"],
                                                                                                         proxima_a_selar=pino_rec["salto"]["proxima_a_selar"]),
                                nota="o recibo pre_selo REAL da R3.4 (ensaio contra a producao, bateria PASSA), gerado antes da instalacao da v394; vale sob a R3.5 (controle R35_V_*)")
novo["recibo_pre_selo_ensaio_R3_3_substituido"] = vivo["recibo_pre_selo"]
novo["selo_anterior_v393"] = pinar(V394 / "base_v393" / "um_absoluto_selo.json", nota="o selo da v393 (custodia, o FIM da cadeia): --selo-anterior")
novo["kernel_manifesto_anterior_v393"] = pinar(V394 / "base_v393" / "tgl_kernel_proof_manifest.json", nota="o manifesto do kernel da v393 (custodia): --kernel-manifesto-anterior")
assert novo["selo_anterior_v393"]["sha256"] == pino_rec["salto"]["ate"]["selo_sha256"] and novo["kernel_manifesto_anterior_v393"]["sha256"] == pino_rec["salto"]["ate"]["kernel_manifesto_sha256"], "a custodia v393 nao e o fim do salto"
novo["nota"] = ("[REAL] lido dos arquivos por script (fundir_pinos_bn_r35.py, R3.5, %s). FUNDIDO a partir do arquivo vivo (sha256 anterior %s): candidato, esperados, criterios e pins_do_candidato ficam como estavam; entram o esboco "
                "R3.5, a bateria por versao (gerador, driver, base R2; a bateria do pos_selo e gerada pelo chain depois do selo), a cadeia de selos v392->v393, o recibo pre_selo REAL da R3.4 e o recibo do kernel R3_4 "
                "(modulos_de_auditoria). O que saiu de uso esta ao lado em *_substituido / *_original / nota_anterior." % (datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), sha_vivo[:16]))
novo["nota_anterior"] = vivo["nota"]
novo["fusao_r35"] = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), por="fundir_pinos_bn_r35.py (R3.5)", sha256_do_vivo_antes=sha_vivo, bytes_do_vivo_antes=len(raw_vivo),
                         chaves_do_vivo_mantidas=["criterios", "candidato", "esperados", "pins_do_candidato"],
                         nao_copiado="PINOS_BN_v394.R3_4.json (a copia da R3.4): o candidato e os esperados dela estao vencidos")
texto = json.dumps(novo, ensure_ascii=False, indent=1).replace("\n", "\r\n")
if a.ensaio:
    print(texto.replace("\r\n", "\n"))
    print("ENSAIO: nada foi escrito; sha256 do vivo %s; chaves %d -> %d" % (sha_vivo, len(vivo), len(novo)), file=sys.stderr)
    sys.exit(0)
# --- backup de BYTES, escrita por temporario, releitura
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bak = VIVO.with_name(VIVO.name + ".bak_" + stamp)
with open(bak, "xb") as f:
    f.write(raw_vivo)
assert bak.read_bytes() == raw_vivo, "backup de bytes falhou"
if sha(VIVO) != sha_vivo:
    raise SystemExit("o PINOS_BN vivo mudou durante a fusao; nada foi escrito (o backup %s ficou)" % bak)
tmp = VIVO.with_name(VIVO.name + ".tmp_r35")
with open(tmp, "xb") as f:
    f.write(texto.encode("utf-8"))
assert tmp.stat().st_size > len(raw_vivo), "o arquivo fundido nao cresceu"
assert json.loads(tmp.read_bytes().decode("utf-8")) == novo
if sha(VIVO) != sha_vivo:
    tmp.unlink()
    raise SystemExit("o PINOS_BN vivo mudou antes do replace; nada foi escrito (o backup %s ficou)" % bak)
os.replace(tmp, VIVO)
depois = VIVO.read_bytes()
assert json.loads(depois.decode("utf-8")) == novo
print(json.dumps(dict(fundido=str(VIVO), sha256=hashlib.sha256(depois).hexdigest(), bytes=len(depois), sha256_do_vivo_antes=sha_vivo, bytes_antes=len(raw_vivo), backup=str(bak), chaves=len(novo), chaves_do_vivo_mantidas=novo["fusao_r35"]["chaves_do_vivo_mantidas"],
                  chaves_novas=sorted(set(novo) - set(vivo)), chaves_do_vivo_substituidas=["kernel_recibo", "bateria", "recibo_pre_selo", "nota"], chaves_do_vivo_renomeadas=dict(esboco_R3_3="esboco_R3_3_substituido")),
                 ensure_ascii=False))
