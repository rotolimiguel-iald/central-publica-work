# -*- coding: utf-8 -*-
"""sonda_abertura_unica.py -- 2a rodada (delta B4): abertura unica em pacotes SINTETICOS montados com o synth_package da COPIA corrigida.
Ordem medida por instrumentacao de builtins.open e os.open. Nenhum dado real."""
import sys, os, json, shutil, builtins
sys.dont_write_bytecode = True
H = os.path.dirname(os.path.abspath(__file__)); CP = os.path.join(H, "copia_pacote_B")
sys.path.insert(0, os.path.join(CP, "runner")); sys.path.insert(0, os.path.join(CP, "testes"))
import f9v2_runner as RUN, f9v2_freeze as FRZ, f9v2_background as BG
import synth_package as SP
TMP = os.path.join(H, "_tmp"); R = {}
def novo():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP); return TMP
def code_of(fn):
    try:
        fn(); return "SEM_RECUSA"
    except FRZ.Refusal as e:
        return e.code
    except Exception as e:
        return type(e).__name__
# A: ordem marcador x primeira fonte, e a 2a abertura
pkg = SP.make_package(novo()); root = pkg["root"]
srcs = {os.path.normcase(os.path.abspath(os.path.join(root, *r["file"].split("/")))) for r in pkg["register"]["leitores"].values()}
marker = os.path.normcase(os.path.abspath(os.path.join(root, *FRZ.MARKER_REL.split("/"))))
ev = []; _o, _oo = builtins.open, os.open
def op(f, mode="r", *a, **k):
    try:
        p = os.path.normcase(os.path.abspath(f))
        if p in srcs: ev.append(("fonte", p))
    except TypeError:
        pass
    return _o(f, mode, *a, **k)
def oo(p, flags, *a, **k):
    if os.path.normcase(os.path.abspath(p)) == marker: ev.append(("marcador_os_open", p))
    return _oo(p, flags, *a, **k)
builtins.open, os.open = op, oo
try:
    c1 = code_of(lambda: RUN.open_test(root, pkg["provider"]))
finally:
    builtins.open, os.open = _o, _oo
i_m = next(i for i, e in enumerate(ev) if e[0] == "marcador_os_open"); i_f = next(i for i, e in enumerate(ev) if e[0] == "fonte")
R["A_primeira_abertura"] = c1; R["A_marcador_antes_da_primeira_fonte"] = i_m < i_f; R["A_aberturas_de_fonte"] = sum(1 for e in ev if e[0] == "fonte")
R["A_marcador"] = json.load(open(os.path.join(root, *FRZ.MARKER_REL.split("/")), encoding="utf-8"))
c2 = code_of(lambda: RUN.open_test(root, pkg["provider"]))
R["A_segunda_abertura"] = c2; R["A_registros_de_recusa"] = sorted(f for f in os.listdir(os.path.join(root, "freeze")) if f.startswith("REGISTRO_DE_RECUSA_"))
R["A_resultados_gravados"] = sorted(os.listdir(os.path.join(root, "saidas_sinteticas")))
# B: recusa ANTES do marcador (sem abertura) nao cria marcador
pkg = SP.make_package(novo(), with_open=False); root = pkg["root"]
R["B_sem_abertura"] = code_of(lambda: RUN.open_test(root, pkg["provider"])); R["B_marcador_criado"] = os.path.exists(os.path.join(root, *FRZ.MARKER_REL.split("/")))
# C: recusa DEPOIS do marcador por motivo de ambiente (fundo divergente): grava registro e CONSOME a abertura
pkg = SP.make_package(novo()); root = pkg["root"]
bad = BG.SyntheticBackgroundProvider(H0=68.60)
R["C_fundo_divergente"] = code_of(lambda: RUN.open_test(root, bad))
R["C_marcador_criado"] = os.path.exists(os.path.join(root, *FRZ.MARKER_REL.split("/")))
R["C_registros"] = len([f for f in os.listdir(os.path.join(root, "freeze")) if f.startswith("REGISTRO_DE_RECUSA_")])
R["C_retentativa_com_fundo_certo"] = code_of(lambda: RUN.open_test(root, pkg["provider"]))
shutil.rmtree(TMP, ignore_errors=True)
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open("SONDA_ABERTURA_UNICA.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
