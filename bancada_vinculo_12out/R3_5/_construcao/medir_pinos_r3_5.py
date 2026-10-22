# -*- coding: utf-8 -*-
"""medir_pinos_r3_5.py (R3.5, 19/10/2026) -- SO LEITURA: mede, por script, os sha256 e tamanhos dos entregaveis da R3.5, dos insumos que ela cita (R3.4, cadeia, Nos, producao) e dos TRES arquivos da pasta v394 que a R3.5
alterou com backup de bytes (PINOS_BN_v394.json, chain_pos_rito_v394.sh, b3_recibo_v394.py) mais os backups, e grava R3_5/PINOS_R3_5.json (arquivo NOVO). Nenhum hash e digitado: todos sao lidos dos arquivos.
uso: python -I -B -X utf8 medir_pinos_r3_5.py <saida.json>"""
import sys
sys.dont_write_bytecode = True
import datetime, hashlib, json
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
R34 = AQUI.parent / "R3_4"
CADEIA = AQUI.parent.parent / "cadeia_de_selo"
V394 = CADEIA / "v394"
POS = V394 / "pos_rito"
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
PROD = Path("C:/IALD/Bancada_Um")


def pinar(p):
    p = Path(p)
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return dict(path=str(p), bytes=p.stat().st_size, sha256=h.hexdigest())


entregaveis = ["sincronizar_bancada.py", "controles_negativos_r3_5.py", "montar_sandbox.py", "gerar_cadeia_de_selos.py", "gerar_bateria_r3_4.py", "derivar_recibo_kernel_r3_4.py", "bateria_r3_4/t12_t14_atrator_r3_4.py",
               "bateria_r3_4/PINO_UM_PY_v393.json", "BATERIA_VINCULO_v393.json", "CADEIA_DE_SELOS_v394.json", "KERNEL_RECIBO_v394_R3_4.json", "PINO_RECIBO_PRE_SELO_v394_R3_4.json", "CRITERIOS_V392.json",
               "CONTROLES_NEGATIVOS_R3_5.json", "DIFF_R3_4_R3_5.patch", "DIFF_PASSO10_R3_5.patch", "VERIFICACAO_DIFF_R3_5.json", "RESULTADO_R3_5.md", "registro_mapa_F0.6_R3_5.json"]
baks = sorted(list(POS.glob("chain_pos_rito_v394.sh.bak_*")) + list(POS.glob("b3_recibo_v394.py.bak_*")) + list(V394.glob("PINOS_BN_v394.json.bak_*")))
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.5 (19/10/2026)",
           r3_4_base=dict(sincronizar_bancada=pinar(R34 / "sincronizar_bancada.py"), controles=pinar(R34 / "controles_negativos_r3_4.py"), montar_sandbox=pinar(R34 / "montar_sandbox.py"),
                          controles_json=pinar(R34 / "CONTROLES_NEGATIVOS_R3_4.json"), resultado=pinar(R34 / "RESULTADO_R3_4.md"), nota="a base: o esboco R3.4 (o que gerou o recibo pre_selo real)"),
           entregaveis={n: (pinar(AQUI / n) if (AQUI / n).is_file() else "AUSENTE") for n in entregaveis},
           alterados_na_pasta_v394=dict(pinos_bn_fundido=pinar(V394 / "PINOS_BN_v394.json"), chain_re_derivado=pinar(POS / "chain_pos_rito_v394.sh"), helper_re_derivado=pinar(POS / "b3_recibo_v394.py"),
                                        backups_de_bytes={p.name: pinar(p) for p in baks}),
           recibo_pre_selo_real={p.relative_to(AQUI / "recibo_pre_selo_v394").as_posix(): pinar(p) for p in sorted((AQUI / "recibo_pre_selo_v394").rglob("*")) if p.is_file()},
           evidencias={p.relative_to(AQUI).as_posix(): pinar(p) for p in sorted((AQUI / "evidencias").rglob("*")) if p.is_file()},
           auxiliares_de_construcao={p.relative_to(AQUI).as_posix(): pinar(p) for p in sorted((AQUI / "_construcao").glob("*")) if p.is_file()},
           bancada_de_producao_lida=dict(manifesto=pinar(PROD / "canonical_contracts.json")),
           nos_lido_no_fecho={n: pinar(NOS / n) for n in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json")},
           nota="[REAL] lido dos arquivos por script; o Nos esta no meio do rito da v394 no momento da medida (um.py v394, selo/core/manifesto do kernel ainda os da v393 se o rito nao terminou); este arquivo mede o estado no fim da construcao")
p = Path(sys.argv[1])
with open(p, "xb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
print(p, len(out["entregaveis"]), sum(1 for v in out["entregaveis"].values() if v == "AUSENTE"), "ausentes")
