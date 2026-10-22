# -*- coding: utf-8 -*-
"""patch de construcao (R3.4, parte 4): os controles M de DADO REAL passam a usar um SNAPSHOT pinado do recibo do kernel da v394 e das 3 fontes de auditoria (R3_4/evidencias), porque a
pasta v394 da cadeia e VIVA (outra sessao reconstruiu o kernel as 13:33-13:51: 190 pedras, arvore em C:/t/k394d). O recibo vivo e so lido pelo finalizar_r3_4.py."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "controles_negativos_r3_4.py"
t = P.read_text(encoding="utf-8")


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:100])
    t = t.replace(old, new)


sub('''V394 = WORK / "cadeia_de_selo" / "v394"
KR394 = json.loads((V394 / "kernel" / "KERNEL_RECIBO_v394.json").read_bytes())
SEM_DECL = sorted(p["path"] for p in KR394["pedras"] if not p.get("declaracoes"))
FONTES_AUD_REAIS = {p: Path(KR394["arvore"]) / p for p in SEM_DECL}
checar("R34_M_recibo_real_v394_tem_exatamente_tres_pedras_sem_declaracoes", lambda: SEM_DECL == ["TGLExt/F1Fecho394/NetworkProofAuditR3.lean", "TGLExt/F1Fecho394/NetworkProofAuditR7.lean",
                                                                                              "TGLExt/F1Fecho394/NetworkProofAuditR8.lean"] and len(KR394["pedras"]) == 189,
       nota="M (dado real): no KERNEL_RECIBO_v394 (so lido) as pedras sem declaracoes sao exatamente as 3 de auditoria (de 189)", pedras_sem_declaracoes=SEM_DECL, contrato=KR394["contrato"])
''', '''# O snapshot (R3_4/evidencias): a copia de bytes do KERNEL_RECIBO_v394.json (contrato R3_2, 190 pedras, feito as 13:57 de 19/10 -- a pasta v394 e viva) e das 3 fontes de auditoria, conferidas contra o recibo.
EVID = AQUI / "evidencias"
SNAP_RECIBO, SNAP_FONTES = EVID / "KERNEL_RECIBO_v394_SNAPSHOT_R3_2.json", EVID / "fontes_reais_v394"
KR394 = json.loads(SNAP_RECIBO.read_bytes())
SEM_DECL = sorted(p["path"] for p in KR394["pedras"] if not p.get("declaracoes"))
FONTES_AUD_REAIS = {p: SNAP_FONTES / p for p in SEM_DECL}
checar("R34_M_recibo_real_v394_tem_exatamente_tres_pedras_sem_declaracoes", lambda: SEM_DECL == ["TGLExt/F1Fecho394/NetworkProofAuditR3.lean", "TGLExt/F1Fecho394/NetworkProofAuditR7.lean",
                                                                                              "TGLExt/F1Fecho394/NetworkProofAuditR8.lean"] and KR394["contrato"] == "KERNEL_RECIBO_R3_2" and len(KR394["pedras"]) >= 189,
       nota="M (dado real): no KERNEL_RECIBO_v394 (snapshot pinado, %d pedras) as pedras sem declaracoes sao exatamente as 3 de auditoria" % len(KR394["pedras"]), pedras_sem_declaracoes=SEM_DECL,
       contrato=KR394["contrato"], snapshot=_pinar(SNAP_RECIBO), n_pedras=len(KR394["pedras"]))
''')
sub('''rc_dv, out_dv, sd_dv = derivar("real_v394", V394 / "kernel" / "KERNEL_RECIBO_v394.json")
checar("R34_M_derivador_a_partir_do_recibo_real_v394_lista_as_tres_e_so_muda_isso", lambda: rc_dv == 0 and json.loads(sd_dv.read_bytes())["modulos_de_auditoria"] == SEM_DECL
       and json.loads(sd_dv.read_bytes())["contrato"] == "KERNEL_RECIBO_R3_4"
       and {k_: v_ for k_, v_ in json.loads(sd_dv.read_bytes()).items() if k_ not in ("contrato", "modulos_de_auditoria", "derivado_de")} == {k_: v_ for k_, v_ in KR394.items() if k_ != "contrato"}
       and json.loads(sd_dv.read_bytes())["derivado_de"]["sha256"] == sha(V394 / "kernel" / "KERNEL_RECIBO_v394.json"),
       nota="M (dado real): o derivador, sobre o KERNEL_RECIBO_v394 (R3_2, so lido), lista exatamente as 3 pedras sem declaracoes (fontes conferidas pelo sha do recibo e pela varredura) e NADA mais muda "
            "(logs, hashes, criterios, pedras); o recibo derivado (contrato R3_4) e a proposta para a gerencia pinar", saida=out_dv[:300])''',
    '''_snap_mini = dict(KR394, arvore=str(SNAP_FONTES))        # o snapshot com a arvore apontando para a mini-arvore das 3 fontes (o derivador so le as fontes das pedras sem declaracoes)
_snap_mini_p = FX / "KERNEL_RECIBO_v394_SNAPSHOT_mini_arvore.json"
_snap_mini_p.write_bytes(json.dumps(_snap_mini, ensure_ascii=False, indent=1).encode("utf-8"))
rc_dv, out_dv, sd_dv = derivar("real_v394", _snap_mini_p)
checar("R34_M_derivador_a_partir_do_recibo_real_v394_lista_as_tres_e_so_muda_isso", lambda: rc_dv == 0 and json.loads(sd_dv.read_bytes())["modulos_de_auditoria"] == SEM_DECL
       and json.loads(sd_dv.read_bytes())["contrato"] == "KERNEL_RECIBO_R3_4"
       and {k_: v_ for k_, v_ in json.loads(sd_dv.read_bytes()).items() if k_ not in ("contrato", "modulos_de_auditoria", "derivado_de")} == {k_: v_ for k_, v_ in _snap_mini.items() if k_ != "contrato"}
       and json.loads(sd_dv.read_bytes())["derivado_de"]["sha256"] == sha(_snap_mini_p),
       nota="M (dado real): o derivador, sobre o snapshot do KERNEL_RECIBO_v394 (R3_2, %d pedras; so a arvore aponta para a mini-arvore das 3 fontes), lista exatamente as 3 pedras sem declaracoes "
            "(fontes conferidas pelo sha do recibo e pela varredura) e NADA mais muda (logs, hashes, criterios, pedras); o recibo derivado (contrato R3_4) e a proposta para a gerencia pinar" % len(KR394["pedras"]),
       saida=out_dv[:300])''')
P.write_text(t, encoding="utf-8", newline="")
print("ok")
