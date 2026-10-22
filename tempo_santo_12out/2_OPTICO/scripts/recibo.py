# -*- coding: utf-8 -*-
"""Recibo da face otica F1.TEMPO (2_OPTICO). Le tudo por script; escreve so em 2_OPTICO.
Gera: ACOM_RECIBO_PROJECAO_OPTICO.json (so o recibo da projecao SO DE LEITURA; o texto projetado nao se copia),
TENTATIVAS.json (todas as tentativas, com a errata ao lado) e RECIBO_OPTICO.json (sha256 de todo arquivo de 2_OPTICO).
Uso: python -B -E -P -X utf8 scripts/recibo.py <caminho_da_projecao_acom_no_scratchpad>"""
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert os.path.basename(HERE) == "2_OPTICO"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest(), os.path.getsize(p)


def write(name, obj):
    path = os.path.join(HERE, name)
    data = (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    assert os.path.getsize(tmp) == len(data)
    os.replace(tmp, path)
    return hashlib.sha256(data).hexdigest(), len(data)


proj_path = sys.argv[1]
raw = open(proj_path, "rb").read()
pj = json.loads(raw.decode("utf-8"))
res = pj["result"]
acom = {"nota": "Recibo da projecao SO DE LEITURA da referencia ACOM da gerencia c1 (session_memory.py, operacao project; "
                "no CLI, project chama so store.get: BEGIN/leitura/ROLLBACK). Guarda-se so o recibo e as contagens; o texto "
                "projetado (memoria do pai) nao se copia. Nenhuma inscricao de contexto filho e nenhuma transition: a tarefa "
                "proibe escrever fora de 2_OPTICO e a transicao de q/p e ato da gerencia.",
        "referencia": "C:\\IALD\\MEMORIA_IALD\\sessions\\claude-c1_exame-geral-12out.json",
        "projecao_feita_em_local": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(proj_path))),
        "receipt": res["receipt"], "n_required_record_ids": len(res["required_record_ids"]),
        "n_included_record_ids": len(res["included_record_ids"]), "n_omitted_record_ids": len(res["omitted_record_ids"]),
        "overflow": res["overflow"], "projection_sha256": res["projection_sha256"],
        "sha256_da_resposta_integral": hashlib.sha256(raw).hexdigest(), "bytes_da_resposta_integral": len(raw),
        "mesma_revisao_e_estado_do_pre_registrador": (res["receipt"]["revision"] == 2 and res["receipt"]["state_sha256"] ==
                                                      "a5f688dfb699a154145e2d79056f2259d951fbdef64f0a718e1858af09058194"),
        "observacao_store": ("memory.sqlite3 mudou as 13:16:58-59 (backup memory.sqlite3.bak_20261012_131658_995705_deaa7cae "
                             "criado pela via de escrita do store), ~2,5 min DEPOIS desta projecao (13:14:19) e sem nenhuma "
                             "operacao de escrita emitida por este agente: escrita de outro ator. Nao conferido quem.")}
s_acom = write("ACOM_RECIBO_PROJECAO_OPTICO.json", acom)

tent_dir = os.path.join(HERE, "tentativas")
tents = []
for d in sorted(os.listdir(tent_dir)):
    p = os.path.join(tent_dir, d)
    files = {f: dict(zip(("sha256", "bytes"), sha(os.path.join(p, f)))) for f in sorted(os.listdir(p))}
    tents.append({"tentativa": d, "arquivos": files})
errata = {
    "tentativa_001_infra": ("ERRO DO RUNNER antes de construir o modelo: KeyError 'beta' em main() (a chave do leitor e "
                            "'beta_runtime'). Preflight 119/119 ok e beta lido = conferencia (dif 0,0) ja registrados no log; "
                            "nenhum autoteste, nenhum subitem pre-registrado foi medido. Correcao: so o nome da chave. "
                            "A tentativa e o log ficam preservados."),
    "tentativa_002_infra": "infraestrutura valida (preflight 119/119; beta dif 0,0; autotestes aprovados; kernel igual); nenhum subitem medido.",
    "tentativa_003_ensaio": ("O ENSAIO (unico ensaio completo). Runner valido; resultado oficial copiado para 2_OPTICO/"
                             "RESULTADO_OPTICO.json, ACHADOS_FORA_DO_PREREGISTRO.json e run_optico.log."),
}
for t in tents:
    t["leitura"] = errata.get(t["tentativa"], "")
s_tent = write("TENTATIVAS.json", {"nota": "todas as tentativas preservadas; errata ao lado, nunca por cima",
                                   "runner_sha256_atual": sha(os.path.join(HERE, "run_optico.py"))[0],
                                   "tentativas": tents})

files = {}
for dp, dn, fn in os.walk(HERE):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, HERE).replace("\\", "/")
        if rel == "RECIBO_OPTICO.json":
            continue
        s, n = sha(p)
        files[rel] = {"sha256": s, "bytes": n}
r = json.load(open(os.path.join(HERE, "RESULTADO_OPTICO.json"), encoding="utf-8"))
fa = json.load(open(os.path.join(HERE, "FINGERPRINT_OPTICO_ANTES.json"), encoding="utf-8"))
fd = json.load(open(os.path.join(HERE, "FINGERPRINT_OPTICO_DEPOIS.json"), encoding="utf-8"))
um_sha = r["beta"]["um_py_sha256"]
recibo = {
    "documento": "RECIBO da face otica F1.TEMPO (construtor otico, gerencia c1)",
    "gerado_em_local": time.strftime("%Y-%m-%d %H:%M:%S"),
    "freeze_conferido": {"FREEZE.json_sha256": "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b",
                         "conferencia_externa": "CONFERENCIA_FREEZE.json (73 itens, 0 falhas)",
                         "conferencia_no_runner": "%d itens, %d falhas" % (r["preflight"]["n"], len(r["preflight"]["falhas"]))},
    "um_py": {"sha256": um_sha, "executado": False, "linha_alpha": r["beta"]["linha_alpha"],
              "beta_runtime": r["beta"]["beta_runtime"], "dif_conferencia": r["beta"]["dif_abs_conferencia"]},
    "impressao_digital_tgl_kernel": {
        "antes_externa": {"meta": fa["meta_sha256"], "src": fa["src_sha256"], "taken_at": fa["taken_at"]},
        "inicio_runner": {"meta": r["impressao_digital_kernel"]["inicio"]["meta_sha256"], "src": r["impressao_digital_kernel"]["inicio"]["src_sha256"]},
        "fim_runner": {"meta": r["impressao_digital_kernel"]["fim"]["meta_sha256"], "src": r["impressao_digital_kernel"]["fim"]["src_sha256"]},
        "depois_externa": {"meta": fd["meta_sha256"], "src": fd["src_sha256"], "taken_at": fd["taken_at"]},
        "todas_iguais": len({fa["meta_sha256"], fd["meta_sha256"], r["impressao_digital_kernel"]["inicio"]["meta_sha256"],
                             r["impressao_digital_kernel"]["fim"]["meta_sha256"]}) == 1 and
                        len({fa["src_sha256"], fd["src_sha256"], r["impressao_digital_kernel"]["inicio"]["src_sha256"],
                             r["impressao_digital_kernel"]["fim"]["src_sha256"]}) == 1},
    "lean": "nenhum (o construtor otico nao compila Lean; nenhum toolchain, .lake ou cache copiado para limpar)",
    "valido": r["valido"],
    "resultado_por_subitem_otico": {k: v["resultado"] for k, v in r["subitens_oticos"].items()},
    "controles_oticos": {k: v["comportou_se_como_registrado"] for k, v in r["controles_oticos"].items()},
    "face_otica_por_afirmacao": {k: v["resultado_da_face_otica"] for k, v in r["por_afirmacao_face_otica"].items()},
    "acom": {"arquivo": "ACOM_RECIBO_PROJECAO_OPTICO.json", "sha256": s_acom[0]},
    "tentativas": {"arquivo": "TENTATIVAS.json", "sha256": s_tent[0]},
    "arquivos_de_2_OPTICO": files,
    "nada_escrito_fora": ("Escrito so em 2_OPTICO. Temporarios desta sessao no scratchpad (projecao ACOM, extratos de leitura, "
                          "stdout do ensaio = conteudo do run_optico.log) apagados depois de conferidos. Mapa: so 'consultar' "
                          "(10 consultas; livro 3636e6c83e1b5ee9 inalterado). ACOM: so projecao de leitura. Nenhum quadro, "
                          "tunel, Nos, kernel, Bancada_Um, site ou git tocado. Python com -B (sem .pyc)."),
}
s_rec = write("RECIBO_OPTICO.json", recibo)
print(json.dumps({"ACOM": s_acom, "TENTATIVAS": s_tent, "RECIBO": s_rec, "n_arquivos": len(files),
                  "kernel_todas_iguais": recibo["impressao_digital_tgl_kernel"]["todas_iguais"]}, indent=1))
