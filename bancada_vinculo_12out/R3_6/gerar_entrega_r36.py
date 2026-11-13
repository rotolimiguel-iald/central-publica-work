# -*- coding: utf-8 -*-
"""gerar_entrega_r36.py (R3.6, 13/11/2026) -- gera, LENDO os arquivos (nenhum hash digitado), o DIFF_R3_5_R3_6.patch, o PINOS_R3_6.json e o ENTREGA_R3_6.json. Ordem: o diff; os pinos (sha256 e bytes de cada entregavel);
a entrega (hashes antes/depois de cada arquivo tocado, backups, contagens dos controles, o que ficou por fazer). So' escreve em R3_6; nao toca em mais nada. uso: python -B -X utf8 gerar_entrega_r36.py"""
import datetime, difflib, glob, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R36 = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(R36)
V = os.path.join(os.path.dirname(BASE), "cadeia_de_selo", "v411")
rd = lambda p: open(p, "rb").read()
sha = lambda b: hashlib.sha256(b).hexdigest()
J = os.path.join
ESB5, ESB6 = J(BASE, "R3_5", "sincronizar_bancada.py"), J(R36, "sincronizar_bancada.py")
AGORA = datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def gravar(p, b):
    if os.path.exists(p):
        open(p + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(rd(p))
    open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b)
    os.replace(p + ".tmp", p)


# 1. o diff unificado R3_5 -> R3_6 (a R3_5 nao e' tocada)
t5, t6 = rd(ESB5).decode("utf-8").split("\n"), rd(ESB6).decode("utf-8").split("\n")
dif = "\n".join(difflib.unified_diff(t5, t6, "R3_5/sincronizar_bancada.py", "R3_6/sincronizar_bancada.py", lineterm="", n=3)) + "\n"
gravar(J(R36, "DIFF_R3_5_R3_6.patch"), dif.encode("utf-8"))
n_add = sum(1 for l in dif.split("\n") if l.startswith("+") and not l.startswith("+++")); n_rem = sum(1 for l in dif.split("\n") if l.startswith("-") and not l.startswith("---"))

# 2. os pinos dos entregaveis
ent = {"esboco_R3_6": J(R36, "sincronizar_bancada.py"), "esboco_R3_5_so_leitura": ESB5, "controles_r3_6.py": J(R36, "controles_r3_6.py"), "CONTROLES_R3_6.json": J(R36, "CONTROLES_R3_6.json"),
       "DIFF_R3_5_R3_6.patch": J(R36, "DIFF_R3_5_R3_6.patch"), "RESULTADO_R3_6.md": J(R36, "RESULTADO_R3_6.md"), "gerar_entrega_r36.py": J(R36, "gerar_entrega_r36.py"),
       "complementar_recibo_kernel_v411_r36.py": J(V, "complementar_recibo_kernel_v411_r36.py"), "repinar_bn_v411_r36.py": J(V, "repinar_bn_v411_r36.py"),
       "KERNEL_RECIBO_v411.json": J(V, "kernel", "KERNEL_RECIBO_v411.json"), "PINOS_BN_v411.json": J(V, "PINOS_BN_v411.json"), "chain_pos_rito_v411.sh": J(V, "pos_rito", "chain_pos_rito_v411.sh")}
pinos = {k: {"path": p, "sha256": sha(rd(p)), "bytes": os.path.getsize(p)} for k, p in ent.items()}
pinos["_nota"] = "lido dos arquivos por script (gerar_entrega_r36.py, %s); a R3_5 e' so' leitura e esta aqui para provar que nao mudou (sha256 igual ao pino esboco_R3_5 do PINOS_BN_v411)" % AGORA
gravar(J(R36, "PINOS_R3_6.json"), json.dumps(pinos, ensure_ascii=False, indent=1).encode("utf-8"))

# 3. a entrega
ctrl = json.load(open(J(R36, "CONTROLES_R3_6.json"), encoding="utf-8"))
pbn = json.load(open(ent["PINOS_BN_v411.json"], encoding="utf-8"))


def antes_depois(p):
    baks = sorted(glob.glob(p + ".bak_*"))
    return {"path": p, "depois": {"sha256": sha(rd(p)), "bytes": os.path.getsize(p)},
            "antes": ([{"backup": b, "sha256": sha(rd(b)), "bytes": os.path.getsize(b)} for b in baks] if baks else "arquivo NOVO (nao existia)")}


entrega = {"entrega": "R3.6 (13/11/2026): contrato KERNEL_RECIBO_R3_6 do elo B(n) para versao SEM pedra nova", "quando": AGORA, "veredito_dos_controles": ctrl["veredito"], "totais_dos_controles": ctrl["totais"],
           "esboco_R3_5_intacto": sha(rd(ESB5)) == pbn["esboco_R3_5"]["sha256"],
           "diff_r3_5_r3_6": {"linhas_acrescentadas": n_add, "linhas_removidas": n_rem},
           "tocados_ou_criados": {"esboco_R3_6": antes_depois(ent["esboco_R3_6"]), "controles_r3_6.py": antes_depois(ent["controles_r3_6.py"]), "CONTROLES_R3_6.json": antes_depois(ent["CONTROLES_R3_6.json"]),
                                  "complementar_recibo_kernel_v411_r36.py": antes_depois(ent["complementar_recibo_kernel_v411_r36.py"]), "repinar_bn_v411_r36.py": antes_depois(ent["repinar_bn_v411_r36.py"]),
                                  "KERNEL_RECIBO_v411.json": antes_depois(ent["KERNEL_RECIBO_v411.json"]), "PINOS_BN_v411.json": antes_depois(ent["PINOS_BN_v411.json"]), "chain_pos_rito_v411.sh": antes_depois(ent["chain_pos_rito_v411.sh"]),
                                  "DIFF_R3_5_R3_6.patch": antes_depois(ent["DIFF_R3_5_R3_6.patch"]), "PINOS_R3_6.json": antes_depois(J(R36, "PINOS_R3_6.json")), "RESULTADO_R3_6.md": antes_depois(ent["RESULTADO_R3_6.md"])},
           "arvore_refeita": {"path": "C:\\t\\k411c\\arvore", "por": "refazer_arvore_v411_pos_selo.py (rc 0: ok, 0 pedras, 1761 .lean, 156 em O16, 0 divergencias)", "nota": "nao existia antes (rmtree de caminho inexistente); a arvore agora tem 1761 .lean e nenhuma juncao"},
           "pinos_bn_novos": {k: {"sha256": pbn[k]["sha256"], "bytes": pbn[k]["bytes"]} for k in ("kernel_recibo", "esboco_R3_6")},
           "nao_feito_ou_por_fazer": ["a suite completa de 596 controles da R3.5 NAO foi re-rodada (limite dito no RESULTADO_R3_6.md)",
                                      "a cadeia (chain_pos_rito_v411.sh), o orquestrador e a ferramenta contra a producao NAO foram executados: o passo 10 (ensaio) e' da gerencia",
                                      "PINOS_BN_v411.json mudou: qualquer pino do proprio PINOS_BN em outro artefato da preparacao (ex.: PRONTO_POS_RITO_v411.json, p00) deve ser regenerado/relido pela gerencia",
                                      "guardas_estaticas_bancada_v411.py, conferir_rito_v411.py, ensaio_a_seco_v411.py e gerar_candidato_v411.py seguem lendo o esboco R3_5 (so' os regex do um.py candidato; nao tocados)",
                                      "revisao independente (quem construiu nao aprova) e registro no Mapa de Rotas: da gerencia"]}
gravar(J(R36, "ENTREGA_R3_6.json"), json.dumps(entrega, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps({"diff": {"+": n_add, "-": n_rem}, "pinos": {k: v["sha256"][:16] for k, v in pinos.items() if isinstance(v, dict)}, "entrega_sha16": sha(rd(J(R36, "ENTREGA_R3_6.json")))[:16]}, ensure_ascii=False))
