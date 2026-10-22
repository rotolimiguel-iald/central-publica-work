# -*- coding: utf-8 -*-
"""medir_pinos_r3_4.py (R3.4, 19/10/2026) -- SO LEITURA: mede, por script, os sha256 e tamanhos dos entregaveis da R3.4 e dos insumos que a R3.4 cita (R3.3, cadeia, Nos, producao), e grava
R3_4/PINOS_R3_4.json (arquivo NOVO). Nenhum hash e digitado: todos sao lidos dos arquivos. uso: python -I -B -X utf8 medir_pinos_r3_4.py <saida.json>"""
import sys
sys.dont_write_bytecode = True
import datetime, hashlib, json, os
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
R33 = AQUI.parent / "R3_3"
CADEIA = Path("C:/IALD/Central de Patentes/work/cadeia_de_selo")
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
PROD = Path("C:/IALD/Bancada_Um")


def pinar(p):
    p = Path(p)
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return dict(path=str(p), bytes=p.stat().st_size, sha256=h.hexdigest())


entregaveis = ["sincronizar_bancada.py", "controles_negativos_r3_4.py", "montar_sandbox.py", "gerar_cadeia_de_selos.py", "gerar_bateria_r3_4.py", "derivar_recibo_kernel_r3_4.py",
               "bateria_r3_4/t12_t14_atrator_r3_4.py", "bateria_r3_4/PINO_UM_PY_v393.json", "BATERIA_VINCULO_v393.json", "CADEIA_DE_SELOS_v394.json", "CRITERIOS_V392.json",
               "KERNEL_RECIBO_v394_R3_4.json", "CONTROLES_NEGATIVOS_R3_4.json", "DIFF_R3_3_R3_4.patch", "VERIFICACAO_DIFF_R3_4.json", "RESULTADO_R3_4.md",
               "PINOS_BN_v394.R3_4.json", "PINO_RECIBO_PRE_SELO_v394_R3_4.json", "registro_mapa_F0.6_R3_4.json", "evidencias/VERIFICACAO_RECIBO_PRE_SELO_REAL.json"]
rec_dir = AQUI / "recibo_pre_selo_v394"
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.4 (19/10/2026)",
           r3_3_base=dict(sincronizar_bancada=pinar(R33 / "sincronizar_bancada.py"), controles=pinar(R33 / "controles_negativos_r3_3.py"), montar_sandbox=pinar(R33 / "montar_sandbox.py"),
                          controles_json=pinar(R33 / "CONTROLES_NEGATIVOS_R3_3.json"), resultado=pinar(R33 / "RESULTADO_R3_3.md"),
                          nota="a base: o esboco R3.3 (71507fd02b70b115) conferido antes de tocar"),
           entregaveis={n: (pinar(AQUI / n) if (AQUI / n).is_file() else "AUSENTE") for n in entregaveis},
           recibo_pre_selo_real={p.relative_to(rec_dir).as_posix(): pinar(p) for p in sorted(rec_dir.rglob("*")) if p.is_file()} if rec_dir.is_dir() else None,
           evidencias={p.relative_to(AQUI).as_posix(): pinar(p) for p in sorted((AQUI / "evidencias").rglob("*")) if p.is_file()},
           auxiliares_de_construcao={p.relative_to(AQUI).as_posix(): pinar(p) for p in sorted((AQUI / "_construcao").glob("*")) if p.is_file()},
           bancada_de_producao_lida=dict(manifesto=pinar(PROD / "canonical_contracts.json")),
           nos_lido={n: pinar(NOS / n) for n in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json")},
           cadeia_de_selo_lida={str(p.relative_to(CADEIA)): pinar(p) for p in sorted(list(CADEIA.glob("v39[234]/base_v*/*")) + [CADEIA / "v393" / "APLICADO_AO_CANONICO_20261014_172946.json", CADEIA / "v393" / "PINOS_BN_v393.json",
                                                                                                                                     CADEIA / "v394" / "PINOS_BN_v394.json"]) if p.is_file()},
           nota="[REAL] lido dos arquivos por script; o hash de RESULTADO_R3_4.md e dos arquivos gerados depois dele pode mudar se alguem os editar; este arquivo mede o estado no fim da construcao")
p = Path(sys.argv[1])
with open(p, "xb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
print(p, len(out["entregaveis"]), sum(1 for v in out["entregaveis"].values() if v == "AUSENTE"), "ausentes")
