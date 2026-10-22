# -*- coding: utf-8 -*-
r"""recibo_reensaio_r2.py -- RECIBO do reensaio R2 da face otica (F1.TEMPO, 5_R2/2_REENSAIO).

Le tudo por script; escreve SO em 5_R2/2_REENSAIO: TENTATIVAS.json (todas as tentativas, do runner R2 e da reproducao V4,
com a leitura ao lado) e RECIBO_REENSAIO_R2.json (sha256 de todo arquivo desta pasta; os dois FREEZE; hora UTC de
inicio; impressoes digitais do kernel; ACOM; V4; vereditos; e a prova de que a R1 ficou intacta: nenhum arquivo fora
desta pasta, dentro de tempo_santo_12out, tem mtime posterior a criacao desta pasta, e as listas de hashes da R1 que
existem (RECIBO_OPTICO.json, FREEZE.json, FREEZE_R2.json) conferem). So biblioteca padrao: python -I -X utf8.
"""
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.basename(HERE) != "2_REENSAIO":
    sys.exit("RECUSA: fora de 5_R2/2_REENSAIO")
W = os.path.dirname(os.path.dirname(HERE))
# instante de criacao desta pasta, lido do stdout do shell no momento da criacao (date -u): 2026-10-12T23:13:50Z
CRIADA_EM_UTC = "2026-10-12T23:13:50+00:00"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            c = fh.read(1 << 22)
            if not c:
                break
            h.update(c)
    return h.hexdigest(), os.path.getsize(p)


def write(name, obj):
    path = os.path.join(HERE, name)
    assert os.path.commonpath([os.path.abspath(path), HERE]) == HERE
    data = (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    assert os.path.getsize(tmp) == len(data)
    os.replace(tmp, path)
    return hashlib.sha256(data).hexdigest(), len(data)


def load(p):
    return json.load(open(p, encoding="utf-8"))


def listar(d):
    out = {}
    for dp, dn, fn in os.walk(d):
        dn.sort()
        for f in sorted(fn):
            p = os.path.join(dp, f)
            out[os.path.relpath(p, d).replace("\\", "/")] = dict(zip(("sha256", "bytes"), sha(p)))
    return out


def main():
    res = load(os.path.join(HERE, "RESULTADO_REENSAIO_R2.json"))
    fa = load(os.path.join(HERE, "saidas", "FINGERPRINT_REENSAIO_ANTES.json"))
    fd = load(os.path.join(HERE, "saidas", "FINGERPRINT_REENSAIO_DEPOIS.json"))
    cf = load(os.path.join(HERE, "saidas", "CONFERENCIA_FREEZES_R2.json"))
    acom = load(os.path.join(HERE, "saidas", "ACOM_RECIBO_PROJECAO_REENSAIO_R2.json"))
    v4 = load(os.path.join(HERE, "2_OPTICO", "RESULTADO_OPTICO.json"))
    r1 = load(os.path.join(W, "2_OPTICO", "RESULTADO_OPTICO.json"))

    # --- tentativas (runner R2 e reproducao V4), com a leitura ao lado
    tents = []
    leitura = {
        "tentativas/tentativa_001_infra": "ensaio a seco do runner R2 (--infra): conferencias dos FREEZE, preflight R1, beta, modelo e parametros; nenhum teste do ADENDO medido; valido.",
        "tentativas/tentativa_002_ensaio": "O ENSAIO R2 (unico ensaio com veredito). Resultado copiado para a raiz: RESULTADO_REENSAIO_R2.json, reensaio_r2.log, T9c_float_E2_por_k.tsv.",
        "2_OPTICO/tentativas/tentativa_001_ensaio": "V4: reproducao da R1 pelo runner da R1 copiado byte a byte (regra da R1, SEM ADENDO), comparada criterio a criterio com a R1 pelo runner R2; nao recebe os rotulos T9.o'/O-f'.",
    }
    for base in ("tentativas", os.path.join("2_OPTICO", "tentativas")):
        bd = os.path.join(HERE, base)
        if not os.path.isdir(bd):
            continue
        for d in sorted(os.listdir(bd)):
            p = os.path.join(bd, d)
            rel = (base + "/" + d).replace("\\", "/")
            tents.append({"tentativa": rel, "arquivos": listar(p), "leitura": leitura.get(rel, "")})
    s_tent = write("TENTATIVAS.json", {"nota": "todas as tentativas preservadas; leitura ao lado, nunca por cima; nada da R1 sobrescrito",
                                       "runner_r2_sha256": sha(os.path.join(HERE, "reensaio_r2.py"))[0],
                                       "runner_r1_copiado_sha256": sha(os.path.join(HERE, "2_OPTICO", "run_optico.py"))[0],
                                       "tentativas": tents})

    # --- R1 intacta: mtimes fora desta pasta e listas de hashes existentes
    criada = datetime.fromisoformat(CRIADA_EM_UTC)
    newer = []
    n_out = 0
    maxm = 0.0
    for dp, dn, fn in os.walk(W):
        if os.path.abspath(dp).startswith(os.path.abspath(HERE)):
            dn[:] = []
            continue
        for f in fn:
            p = os.path.join(dp, f)
            m = os.stat(p).st_mtime
            n_out += 1
            maxm = max(maxm, m)
            if datetime.fromtimestamp(m, timezone.utc) >= criada:
                newer.append({"arquivo": os.path.relpath(p, W).replace("\\", "/"), "mtime_utc": datetime.fromtimestamp(m, timezone.utc).isoformat()})
    rec_opt = load(os.path.join(W, "2_OPTICO", "RECIBO_OPTICO.json"))["arquivos_de_2_OPTICO"]
    dif_opt = [k for k, v in rec_opt.items() if sha(os.path.join(W, "2_OPTICO", k.replace("/", os.sep)))[0] != v["sha256"]]
    # classificacao: o registro congelado da R1 (0_LEVANTAMENTO, 1_PREREGISTRO, 2_OPTICO sem rodada_2, 3_KERNEL sem rodada_2,
    # 4_RELATORIO) e o ADENDO congelado (5_R2/0_ADENDO) NAO podem ter mtime posterior; 2_OPTICO/rodada_2 e 3_KERNEL/rodada_2
    # (observados antes do FREEZE_R2, tentativas preservadas de outro ator) e as pastas irmas de 5_R2 (p. ex. 1_PEDRA, a trilha da
    # pedra corrigida) sao escritas de OUTRO ator em curso: ficam listadas como observadas, sem atribuir autoria.
    def classe(rel):
        if rel.startswith("2_OPTICO/rodada_2/") or rel.startswith("3_KERNEL/rodada_2/"):
            return "rodada_2 de outro ator (observada antes do FREEZE_R2; tentativa preservada)"
        if rel.startswith("5_R2/") and not rel.startswith("5_R2/0_ADENDO/"):
            return "pasta irma de 5_R2 (outro ator em curso)"
        return "REGISTRO CONGELADO (R1 ou 0_ADENDO) — nao pode mudar"
    for n in newer:
        n["classe"] = classe(n["arquivo"])
    congelado_tocado = [n for n in newer if n["classe"].startswith("REGISTRO CONGELADO")]
    intacta = {"criada_em_utc_esta_pasta": CRIADA_EM_UTC, "arquivos_fora_desta_pasta_em_tempo_santo_12out": n_out,
               "mtime_max_fora_utc": datetime.fromtimestamp(maxm, timezone.utc).isoformat(),
               "arquivos_fora_com_mtime_posterior_a_criacao": newer,
               "registro_congelado_R1_ou_0_ADENDO_com_mtime_posterior": congelado_tocado,
               "registro_congelado_intacto_por_mtime": not congelado_tocado,
               "nota": ("os escritores deste runner (write_json_atomic, write_text_atomic, copy_bytes_atomic) recusam qualquer caminho fora de "
                        "5_R2/2_REENSAIO; arquivos de outros atores com mtime posterior ficam listados como observados, sem atribuir autoria"),
               "RECIBO_OPTICO_R1_arquivos_listados": len(rec_opt), "RECIBO_OPTICO_R1_arquivos_com_hash_diferente": dif_opt,
               "FREEZE_R1_e_FREEZE_R2_conferidos": {"arquivo": "saidas/CONFERENCIA_FREEZES_R2.json", "n_checks": cf["n_checks"], "n_falhas": cf["n_falhas"], "all_ok": cf["all_ok"]}}

    # --- arquivos desta pasta
    files = listar(HERE)
    files.pop("RECIBO_REENSAIO_R2.json", None)
    kernel = {"antes_externa": {"meta": fa["meta_sha256"], "src": fa["src_sha256"], "taken_at": fa["taken_at"], "files": fa["files"]},
              "inicio_runner_r2": {"meta": res["impressao_digital_kernel"]["inicio"]["meta_sha256"], "src": res["impressao_digital_kernel"]["inicio"]["src_sha256"]},
              "fim_runner_r2": {"meta": res["impressao_digital_kernel"]["fim"]["meta_sha256"], "src": res["impressao_digital_kernel"]["fim"]["src_sha256"]},
              "inicio_runner_v4": {"meta": v4["impressao_digital_kernel"]["inicio"]["meta_sha256"], "src": v4["impressao_digital_kernel"]["inicio"]["src_sha256"]},
              "fim_runner_v4": {"meta": v4["impressao_digital_kernel"]["fim"]["meta_sha256"], "src": v4["impressao_digital_kernel"]["fim"]["src_sha256"]},
              "depois_externa": {"meta": fd["meta_sha256"], "src": fd["src_sha256"], "taken_at": fd["taken_at"], "files": fd["files"]},
              "R1_e_FREEZE_R2": {"meta": "b1b47447ac30f7c74ad33b200bd2a3025987650a13593038ddc7465de6fab21f", "src": "911cb40b9de1a8bb3bdd0789d5af3f718fa98ee9f0b1f5fcd6ffa4abb616bd3d"}}
    metas = {v["meta"] for v in kernel.values()}
    srcs = {v["src"] for v in kernel.values()}
    kernel["todas_iguais"] = (len(metas) == 1 and len(srcs) == 1)
    recibo = {
        "documento": "RECIBO do reensaio R2 da face otica F1.TEMPO (O-f' e T9.o'(c) sob o ADENDO UNIFORME) — reensaiador otico, gerencia c1",
        "gerado_em_utc": datetime.now(timezone.utc).isoformat(), "gerado_em_local": time.strftime("%Y-%m-%d %H:%M:%S"),
        "freeze_conferido": {"FREEZE_R1_sha256": res["freeze"]["FREEZE_R1"]["sha256"], "FREEZE_R1_bytes": res["freeze"]["FREEZE_R1"]["bytes"],
                             "FREEZE_R2_sha256": res["freeze"]["FREEZE_R2"]["sha256"], "FREEZE_R2_bytes": res["freeze"]["FREEZE_R2"]["bytes"],
                             "FREEZE_R2_congelado_em_utc": res["freeze"]["FREEZE_R2"]["congelado_em_utc"],
                             "conferencia_externa": "saidas/CONFERENCIA_FREEZES_R2.json (%d itens, %d falhas)" % (cf["n_checks"], cf["n_falhas"]),
                             "conferencia_no_runner_r2": "%d itens, %d falhas; preflight R1 %d itens, %d falhas" % (res["freeze"]["n"], len(res["freeze"]["falhas"]), res["preflight_R1"]["n"], len(res["preflight_R1"]["falhas"]))},
        "ensaio_R2": {"tentativa": res["tentativa"], "inicio_utc": res["inicio_utc"], "fim_utc": res["fim_utc"],
                      "segundos_depois_do_FREEZE_R2": res["segundos_depois_do_FREEZE_R2"], "valido": res["valido"], "motivos_de_INVALIDO": res["motivos_de_INVALIDO"],
                      "runner_r2": res["runner_r2"], "implementacao_normativa_importada": res["implementacao_normativa_importada"],
                      "runner_r1_copiado_importado": res["runner_r1_copiado_importado"], "semente": res["semente"]},
        "um_py": {"sha256": res["beta"]["um_py_sha256"], "executado": False, "linha_alpha_embutida": res["beta"]["linha_alpha"],
                  "linha_alpha_topo": res["beta"]["SEALED_CODATA_ALPHA_linha"], "beta_runtime": res["beta"]["beta_runtime"],
                  "dif_conferencia": res["beta"]["dif_abs_conferencia"], "estatuto": res["beta"]["estatuto"]},
        "impressao_digital_tgl_kernel": kernel,
        "lean": "nenhum (o reensaio otico nao compila Lean; nenhum toolchain, .lake ou cache copiado; nada a apagar)",
        "vereditos_R2": {"T9.o'(c)": res["T9.o'(c)"]["resultado"], "O-f'": res["O-f'"]["resultado"], "T9.o'": res["T9.o'"]["resultado"], "T4.o'": res["T4.o'"]["resultado"],
                         "quadro_ao_lado": res["quadro_ao_lado"]},
        "V4_reproducao_R1": {k: res["V4_reproducao_R1"][k] for k in ("n_criterios", "n_vereditos_por_criterio_iguais", "n_medidas_bit_a_bit_iguais", "n_medidas_diferentes",
                                                                    "controles_todos_iguais", "por_afirmacao_todos_iguais", "valido_v4", "reproduz_a_R1_em_todo_criterio", "runner_igual")},
        "acom": {"arquivo": "saidas/ACOM_RECIBO_PROJECAO_REENSAIO_R2.json", "so_projecao_de_leitura": True, "db_inalterado": acom["db_inalterado_pela_projecao"],
                 "receipt_revision": acom["receipt"]["revision"], "state_sha256": acom["receipt"]["state_sha256"], "nota": "sem referencia propria; nenhum init e nenhuma transition (atos da gerencia); o script e copia byte a byte do da pasta 0_ADENDO"},
        "R1_intacta": intacta,
        "tentativas": {"arquivo": "TENTATIVAS.json", "sha256": s_tent[0]},
        "arquivos_de_2_REENSAIO": files,
        "nada_escrito_fora": ("Escrito SO em 5_R2/2_REENSAIO. Nada no quadro, no mapa, na memoria (ACOM so projecao de leitura), no tunel, no Nos, no kernel do Nos, "
                              "na Bancada, no site ou no git. O um.py nao foi executado (bytes lidos por regex/ast). Nenhum Lean rodado. Nenhum dado observado; nenhum "
                              "provedor remoto; nenhuma chamada paga. Python com -B (sem .pyc); stdout temporarios apagados; scratchpad nao usado."),
    }
    s_rec = write("RECIBO_REENSAIO_R2.json", recibo)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"TENTATIVAS": s_tent, "RECIBO": s_rec, "n_arquivos": len(files), "kernel_todas_iguais": kernel["todas_iguais"],
                      "registro_congelado_intacto_por_mtime": intacta["registro_congelado_intacto_por_mtime"],
                      "n_arquivos_fora_com_mtime_posterior": len(newer), "classes": sorted({n["classe"] for n in newer}),
                      "RECIBO_OPTICO_R1_diferentes": intacta["RECIBO_OPTICO_R1_arquivos_com_hash_diferente"],
                      "mtime_max_fora_utc": intacta["mtime_max_fora_utc"], "vereditos": recibo["vereditos_R2"]["quadro_ao_lado"]["T9.o'"] + "/" + recibo["vereditos_R2"]["quadro_ao_lado"]["T4.o'"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
