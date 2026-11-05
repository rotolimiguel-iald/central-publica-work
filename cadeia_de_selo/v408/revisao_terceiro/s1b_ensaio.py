# -*- coding: utf-8 -*-
"""Revisor terceiro v408 (R2): a trava S1b (orquestrador/pos_treino_v408.py:s1b_revisao, LIDA; importada com ORQ/LOG/ESTADO redirecionados para _orq_sandbox; NUNCA main, NUNCA o Nos) contra a MINHA revisao
(REVISAO_TERCEIRO_v408.json): deve ABRIR com ela e FECHAR com cada alteracao. A espera usa time.sleep: aqui sleep levanta SystemExit (= 'ficou esperando', fechada)."""
import importlib.util, json, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
spec = importlib.util.spec_from_file_location("pos_treino_rev_s1b", R + "orquestrador/pos_treino_v408.py"); O = importlib.util.module_from_spec(spec); sys.modules["pos_treino_rev_s1b"] = O; spec.loader.exec_module(O)
meu = Path(R + "revisao_terceiro/_orq_sandbox"); meu.mkdir(exist_ok=True)
O.ORQ = meu; O.LOG = meu / "orq_s1b.log"; O.ESTADO = meu / "ESTADO_s1b.json"
O.parar_pedido = lambda: False
gravados = []; O.gravar = lambda e_: gravados.append(1)
def _sleep(s): raise SystemExit("FECHADA (ficou esperando)")
O.time.sleep = _sleep
real = json.load(open(R + "revisao_terceiro/REVISAO_TERCEIRO_v408.json", encoding="utf-8"))
tmp = meu / "REV_FAKE_R2.json"
res = []
def rodar(nome, rev, quer_abrir):
    tmp.write_text(json.dumps(rev), encoding="utf-8"); O.REV = tmp
    e = {"passos": {}}
    try:
        r = O.s1b_revisao(e); abre = bool(r)
    except SystemExit:
        abre = False
    ok = (abre == quer_abrir); res.append(ok)
    print("%-72s -> %s %s" % (nome, "ABRE" if abre else "FECHADA", "(esperado)" if ok else "(INESPERADO)"))
rodar("1. a revisao REAL (aprovada, candidato certo, 22 arquivos)", real, True)
import copy
r = copy.deepcopy(real); r["arquivos_revisados"]["pos_rito/textos_custodia_handoff_v408.py"] = "0" * 16; rodar("2. um arquivo de pos_rito com sha16 diferente", r, False)
r = copy.deepcopy(real); r["arquivos_revisados"]["orquestrador/pos_treino_v408.py"] = "f" * 16; rodar("3. o proprio pos_treino alterado", r, False)
r = copy.deepcopy(real); r["arquivos_revisados"]["pedra/PIgualNP.lean"] = "1" * 16; rodar("4. a pedra PIgualNP alterada", r, False)
r = copy.deepcopy(real); r["aprovada"] = "true"; rodar("5. aprovada string 'true'", r, False)
r = copy.deepcopy(real); r["candidato_sha16"] = "c55c4a7f2753b589"; rodar("6. candidato_sha16 da R1 (outro candidato)", r, False)
r = copy.deepcopy(real); r["aprovada"] = False; rodar("7. aprovada False", r, False)
print("gravar() chamado:", len(gravados), "| todos como esperado:", all(res))
