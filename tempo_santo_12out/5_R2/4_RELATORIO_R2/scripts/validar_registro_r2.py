"""Validacao A SECO do registro_mapa_F1.TEMPO_R2.json contra as regras do rotas.py (importa o modulo e chama
_valida; NAO chama registrar; nada e escrito no livro). A ROTA formal.tempo_santo_fluxo_e_dissipacao ainda nao
existe no livro (4_RELATORIO/registro_rota_F1.TEMPO.json deve entrar primeiro, ato da gerencia); por isso o
rota_id e acrescentado ao conjunto de ids SO em memoria, para validar o RESULTADO. Le o livro (bytes) e mede o
sha256 antes e depois para provar que nao mudou. Escreve SO em 4_RELATORIO_R2/saidas."""
import hashlib, importlib.util, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\4_RELATORIO_R2"
MAPA = r"C:\IALD\MAPA_DE_ROTAS"
LIVRO = os.path.join(MAPA, "rotas.jsonl")
REG = os.path.join(W, "registro_mapa_F1.TEMPO_R2.json")
ROTA_R1 = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\4_RELATORIO\registro_rota_F1.TEMPO.json"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


antes = sha(LIVRO)
spec = importlib.util.spec_from_file_location("rotas", os.path.join(MAPA, "rotas.py"))
rotas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rotas)
linhas = open(LIVRO, "rb").read().decode("utf-8").strip().split("\n")
regs = [json.loads(l) for l in linhas]
ids = {r["rota_id"] for r in regs if r.get("tipo") == "ROTA"}
seqs = {r.get("seq") for r in regs}
rid = "formal.tempo_santo_fluxo_e_dissipacao"
ja_existe = rid in ids
out = {"livro": LIVRO, "n_registros": len(regs), "sha256_livro_antes": antes, "rota_ja_existe_no_livro": ja_existe}
rota_r1 = json.load(open(ROTA_R1, encoding="utf-8"))
try:
    vr = rotas._valida(rota_r1, ids, seqs)
    out["ROTA_de_4_RELATORIO_valida_a_seco"] = {"ok": True, "rota_id": vr.get("rota_id"), "dominio": vr.get("dominio"), "status": vr.get("status")}
except Exception as e:
    out["ROTA_de_4_RELATORIO_valida_a_seco"] = {"ok": False, "erro": str(e)}
ids_sim = set(ids) | {rid}
reg = json.load(open(REG, encoding="utf-8"))
try:
    v = rotas._valida(reg, ids_sim, seqs)
    out["RESULTADO_R2_valido_a_seco"] = {"ok": True, "tipo": v["tipo"], "rota_id": v["rota_id"], "status": v.get("status"),
                                         "estatuto": v.get("estatuto"), "n_artefatos": len(v.get("artefatos", [])),
                                         "artefatos_sha16": [a["sha256"][:16] for a in v.get("artefatos", [])],
                                         "campos_texto_len": {k: len(v[k]) for k in rotas.TEXTOS if k in v}}
except Exception as e:
    out["RESULTADO_R2_valido_a_seco"] = {"ok": False, "erro": str(e)}
out["sha256_livro_depois"] = sha(LIVRO)
out["livro_inalterado"] = out["sha256_livro_antes"] == out["sha256_livro_depois"]
out["gerado_em"] = time.strftime("%Y-%m-%dT%H:%M:%S")
json.dump(out, open(os.path.join(W, "saidas", "VALIDACAO_REGISTRO_R2.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False, indent=1))
