"""Hashes (sha256, bytes, mtime) das fontes lidas e dos entregaveis da ESTRATEGIA A. Gerado por script, nunca a mao."""
import hashlib, json, pathlib, datetime, os
OUT = pathlib.Path(r"C:\IALD\Central de Patentes\work\organismo_iald_12out\1_ESTRATEGIA_A")
FONTES = {
 "um_py_v391": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py",
 "core_v391": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json",
 "selo_v391": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json",
 "ordem_operador_12out": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt",
 "inventario_prova_0": r"C:\IALD\Central de Patentes\work\organismo_iald_12out\0_LEVANTAMENTO_PROVA\INVENTARIO_PROVA.md",
 "canais_json_0": r"C:\IALD\Central de Patentes\work\organismo_iald_12out\0_LEVANTAMENTO_PROVA\CANAIS.json",
 "hashes_levantamento_0": r"C:\IALD\Central de Patentes\work\organismo_iald_12out\0_LEVANTAMENTO_PROVA\medidas\HASHES_LEVANTAMENTO.json",
 "prereg_fase9_v1": r"C:\IALD\Bancada_Um\investigacao\preregistro_fase9_hubble\PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json",
}
def h(p):
    p = pathlib.Path(p)
    if not p.exists(): return {"path": str(p), "exists": False}
    b = p.read_bytes(); st = p.stat()
    return {"path": str(p), "exists": True, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b),
            "mtime": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")}
res = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "fontes": {k: h(v) for k, v in FONTES.items()}, "entregaveis": {}}
for sub in ["", "projecao", "medidas", "scripts", "consultas", "memoria"]:
    d = OUT / sub if sub else OUT
    for f in sorted(d.iterdir()):
        if f.is_file() and f.name != "HASHES_ESTRATEGIA_A.json":
            res["entregaveis"][(sub + "/" if sub else "") + f.name] = h(f)
(OUT / "medidas" / "HASHES_ESTRATEGIA_A.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in res["fontes"].items(): print(k, v.get("sha256", "MISSING")[:16], v.get("bytes"))
print("--"); 
for k in ["ESTRATEGIA_A.md", "projecao/projecao_zdisc_sintetica.py", "projecao/PROJECAO_ZDISC_SINTETICA.json", "projecao/PROJECAO_ZDISC_SINTETICA.txt"]:
    v = res["entregaveis"][k]; print(k, v["sha256"], v["bytes"])
