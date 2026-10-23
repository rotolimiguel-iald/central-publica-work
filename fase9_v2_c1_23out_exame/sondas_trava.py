# -*- coding: utf-8 -*-
"""sondas_trava.py -- auditoria c1 (23/10/2026), itens 5 e 6: sondas PROPRIAS da trava sobre pacotes SINTETICOS (centros e fontes fabricados) montados
com o synth_package da COPIA do pacote, numa pasta temporaria DESTA pasta. Nenhum dado real; nenhum composto observado."""
import sys, os, json, shutil, builtins, copy, hashlib
sys.dont_write_bytecode = True
H = os.path.dirname(os.path.abspath(__file__)); CP = os.path.join(H, "copia_pacote")
sys.path.insert(0, os.path.join(CP, "runner")); sys.path.insert(0, os.path.join(CP, "testes"))
import f9v2_runner as RUN, f9v2_freeze as FRZ, f9v2_background as BG
import synth_package as SP
TMP = os.path.join(H, "_tmp_sondas")
R = {}
class Contador(BG.SyntheticBackgroundProvider):
    n = 0
    def compute(self):
        Contador.n += 1
        return super().compute()
def novo():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP); return TMP
def tenta(nome, fn, pkg_root):
    Contador.n = 0
    try:
        fn(); R[nome] = {"recusou": False}
    except FRZ.Refusal as e:
        R[nome] = {"recusou": True, "codigo": e.code}
    except Exception as e:
        R[nome] = {"recusou": True, "excecao": type(e).__name__ + ": " + str(e)[:120]}
    R[nome]["fundo_calculado_vezes"] = Contador.n
    R[nome]["saidas_criadas"] = [d for d in os.listdir(pkg_root) if d.startswith("saidas")]
# S1: ato de auditoria falso no recibo
pkg = SP.make_package(novo(), with_freeze=False, provider=Contador())
rec = FRZ.make_freeze_receipt(pkg["root"], "SYNTHETIC_TEST_PACKAGE", "SONDA", "sonda", pkg["spec"]["token"]["base"], extra_atos={"auditoria_c1_runner_aprovada": False})
rb = json.dumps(rec).encode(); open(os.path.join(pkg["root"], *FRZ.FREEZE_REL.split("/")), "wb").write(rb)
open(os.path.join(pkg["root"], *FRZ.OPEN_REL.split("/")), "wb").write(json.dumps(FRZ.make_open_receipt(rb, {"quem": "S", "texto": "s"})).encode())
tenta("S1_auditoria_c1_falsa_no_recibo", lambda: RUN.open_test(pkg["root"], pkg["provider"]), pkg["root"])
# S2: ato de abertura com 'quem' vazio
pkg = SP.make_package(novo(), with_open=False, provider=Contador())
ob = FRZ.make_open_receipt(pkg["freeze_raw"], {"quem": "", "texto": "x"}); open(os.path.join(pkg["root"], *FRZ.OPEN_REL.split("/")), "wb").write(json.dumps(ob).encode())
tenta("S2_abertura_sem_quem", lambda: RUN.open_test(pkg["root"], pkg["provider"]), pkg["root"])
# S3: abertura ausente (o fundo NAO pode ser calculado, nada gravado)
pkg = SP.make_package(novo(), with_open=False, provider=Contador())
tenta("S3_abertura_ausente", lambda: RUN.open_test(pkg["root"], pkg["provider"]), pkg["root"])
# S4: congelamento ausente
pkg = SP.make_package(novo(), with_freeze=False, provider=Contador())
tenta("S4_congelamento_ausente", lambda: RUN.open_test(pkg["root"], pkg["provider"]), pkg["root"])
# S5: ALVOS montado a mao numa SUBPASTA das fontes (depois dos recibos)
pkg = SP.make_package(novo(), provider=Contador())
open(os.path.join(pkg["root"], "fontes", "L2_cchp", "ALVOS_FASE9_LIDOS.json"), "w").write("{}")
tenta("S5_ALVOS_em_subpasta", lambda: RUN.open_test(pkg["root"], pkg["provider"]), pkg["root"])
# S6: recibo de congelamento re-emitido (outro emitente) depois do ato de abertura: a abertura nao se refere a ele
pkg = SP.make_package(novo(), provider=Contador())
rec2 = FRZ.make_freeze_receipt(pkg["root"], "SYNTHETIC_TEST_PACKAGE", "OUTRO", "sonda", pkg["spec"]["token"]["base"])
open(os.path.join(pkg["root"], *FRZ.FREEZE_REL.split("/")), "wb").write(json.dumps(rec2).encode())
tenta("S6_congelamento_trocado_depois_da_abertura", lambda: RUN.open_test(pkg["root"], pkg["provider"]), pkg["root"])
# S7: pacote valido -- cada FONTE e' aberta UMA vez (contagem de open por caminho) e o PODER e' gravado antes de CENTERS_UNSEALED
pkg = SP.make_package(novo(), provider=Contador())
cont = {}; _o = builtins.open
def op(f, mode="r", *a, **k):
    try:
        p = os.path.normcase(os.path.abspath(f))
        cont[p] = cont.get(p, 0) + 1
    except TypeError:
        pass
    return _o(f, mode, *a, **k)
builtins.open = op
try:
    Contador.n = 0; res = RUN.open_test(pkg["root"], pkg["provider"])
finally:
    builtins.open = _o
reg = pkg["register"]
fontes = {rid: cont.get(os.path.normcase(os.path.abspath(os.path.join(pkg["root"], *r["file"].split("/")))), 0) for rid, r in reg["leitores"].items()}
log = res["ordem_de_acesso"]
R["S7_pacote_valido"] = {"veredito_sintetico_prefixo": res["veredito"][:60], "aberturas_por_fonte": fontes, "cada_fonte_uma_vez": all(v == 1 for v in fontes.values()),
                         "ordem": log, "poder_antes_dos_centros": log.index([x for x in log if x.startswith("POWER_WRITTEN")][0]) < log.index("CENTERS_UNSEALED"),
                         "fundo_calculado_vezes": Contador.n, "aviso_sintetico": res["AVISO"]}
shutil.rmtree(TMP, ignore_errors=True)
R["todas_as_sondas_de_recusa_recusaram_sem_calcular_nem_gravar"] = all(v["recusou"] and v["fundo_calculado_vezes"] == 0 and not v["saidas_criadas"] for k, v in R.items() if k.startswith("S") and k != "S7_pacote_valido")
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open("SONDAS_TRAVA.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
