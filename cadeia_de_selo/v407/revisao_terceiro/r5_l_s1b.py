# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R2), item E: a trava S1b (orquestrador/pos_treino_v407.py, lido; ensaiada aqui com ORQ/LOG/ESTADO redirecionados para _orq_sandbox, NUNCA main, NUNCA o Nos real).
Casos: arquivos_revisados integros -> abre; um arquivo de pos_rito alterado -> fecha; pos_treino alterado -> fecha; aprovada string -> fecha; sha16 de outro candidato -> fecha; aprovada False -> fecha;
arquivo listado mas ausente / arquivos_revisados ausente -> (registrar o comportamento)."""
import importlib.util, json, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
spec = importlib.util.spec_from_file_location("pos_treino_rev9", R + "orquestrador/pos_treino_v407.py"); O = importlib.util.module_from_spec(spec); sys.modules["pos_treino_rev9"] = O; spec.loader.exec_module(O)
meu = Path(R + "revisao_terceiro/_orq_sandbox"); meu.mkdir(exist_ok=True)
O.ORQ = meu; O.LOG = meu / "orq_r5.log"; O.ESTADO = meu / "ESTADO_r5_l.json"
O.parar_pedido = lambda: False
gravados = []
O.gravar = lambda e_: gravados.append(1)
def _sleep(s): raise SystemExit("FECHADA (ficou esperando)")
O.time.sleep = _sleep
cand = O.sha16(O.PK / "um_v407_candidato.py")
s = lambda rel: hashlib.sha256((O.PK / rel).read_bytes()).hexdigest()[:16]
tmp = meu / "REV_FAKE_R2.json"; O.REV = tmp
arqs = {"pos_rito/textos_v407.py": s("pos_rito/textos_v407.py"), "pos_rito/textos_v407_novo.pysnip": s("pos_rito/textos_v407_novo.pysnip"),
        "pos_rito/textos_custodia_handoff_v407_03nov.py": s("pos_rito/textos_custodia_handoff_v407_03nov.py"), "orquestrador/pos_treino_v407.py": s("orquestrador/pos_treino_v407.py"),
        "runtime_v407.py": s("runtime_v407.py"), "carimbar_stdout_v407.py": s("carimbar_stdout_v407.py"), "rito_v407.sh": s("rito_v407.sh"), "pos_rito/fila_memoria_v407.py": s("pos_rito/fila_memoria_v407.py"), "orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md": s("orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md")}
def rodar(nome, rev):
    tmp.write_text(json.dumps(rev), encoding="utf-8"); O.REV = tmp
    e = {"passos": {}}
    try:
        r = O.s1b_revisao(e); print("%-70s -> %s" % (nome, "ABRE (True)" if r else "retornou %r" % r), "| passos:", list(e["passos"]))
    except SystemExit as ex:
        print("%-70s -> %s" % (nome, ex))
rodar("1. aprovada True + candidato certo + arquivos_revisados integros", {"aprovada": True, "candidato_sha16": cand, "revisor": "teste", "arquivos_revisados": arqs})
a2 = dict(arqs); a2["pos_rito/textos_v407.py"] = "0" * 16
rodar("2. um arquivo de pos_rito com sha16 diferente (alterado depois)", {"aprovada": True, "candidato_sha16": cand, "arquivos_revisados": a2})
a3 = dict(arqs); a3["orquestrador/pos_treino_v407.py"] = "f" * 16
rodar("3. o proprio pos_treino_v407.py alterado", {"aprovada": True, "candidato_sha16": cand, "arquivos_revisados": a3})
rodar("4. aprovada string 'true'", {"aprovada": "true", "candidato_sha16": cand, "arquivos_revisados": arqs})
rodar("5. candidato_sha16 de outro candidato", {"aprovada": True, "candidato_sha16": "0" * 16, "arquivos_revisados": arqs})
rodar("6. aprovada False", {"aprovada": False, "candidato_sha16": cand, "arquivos_revisados": arqs})
a7 = dict(arqs); a7["pos_rito/arquivo_que_nao_existe.py"] = "1" * 16
rodar("7. (comportamento) arquivo listado mas AUSENTE no disco", {"aprovada": True, "candidato_sha16": cand, "arquivos_revisados": a7})
rodar("8. (comportamento) sem o campo arquivos_revisados", {"aprovada": True, "candidato_sha16": cand})
rodar("9. (comportamento) arquivos_revisados vazio {}", {"aprovada": True, "candidato_sha16": cand, "arquivos_revisados": {}})
a10 = dict(arqs); a10["../ESTADO_FORA.json"] = "1" * 16
rodar("10. (comportamento) caminho com .. (fora de PK)", {"aprovada": True, "candidato_sha16": cand, "arquivos_revisados": a10})

for k_ in ("carimbar_stdout_v407.py", "rito_v407.sh", "pos_rito/fila_memoria_v407.py", "orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md"):
    a_ = dict(arqs); a_[k_] = "0" * 16
    rodar("11. (R5) %s alterado" % k_, {"aprovada": True, "candidato_sha16": cand, "arquivos_revisados": a_})
print("gravar() chamado (redirecionado, nada escrito no ESTADO real):", len(gravados))
