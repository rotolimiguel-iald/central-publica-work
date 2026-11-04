# -*- coding: utf-8 -*-
"""estagio_cego_fila_D.py -- fecha a fila no ESTAGIO CEGO (nunca na abertura). Para cada evento usa a analise primaria ou, se foi ela que nao convergiu, a repeticao D5 aceita;
carrega SO o ANALYST_OUTPUT.json (colunas ja DESLOCADAS pela semente) para extrair o que e invariante ao deslocamento (estagio_cego_D) e grava o HASH dos posteriores
(sha256 dos bytes de ANALYST_OUTPUT.json, do *_result.hdf5 e do PRIVATE_CONVERGENCE.json -- o hdf5 NAO e aberto) e o PODER REAL em
estagio_cego/PODER_RAMO_B_ANTES_DE_ABRIR.json (criacao exclusiva). Nada e impresso alem do sha256 do arquivo e de contagens. Nao desvela, nao abre."""
import hashlib
import json
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
sys.path.insert(0, str(CODE))
import estagio_cego_D as EC  # noqa: E402
import guard_D as G  # noqa: E402
import lancar_fila_D as L  # noqa: E402
import v1_ramo_b as V  # noqa: E402

DESTINO = BASE / "estagio_cego" / "PODER_RAMO_B_ANTES_DE_ABRIR.json"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def coletar(eventos, jobs_existentes=None):
    """Para cada evento: o job aceito (primaria, senao R1). Devolve (saidas, hashes, sem_analise, jobs_usados)."""
    saidas, hashes, sem, usados = {}, {}, {}, {}
    for ev in eventos:
        escolhido = None
        for nome in ("D_" + ev, "D_" + ev + "_R1"):
            info = L.info_job(nome)
            if L.aceito(info):
                escolhido = (nome, info)
                break
        if escolhido is None:
            sem[ev] = {n: L.info_job(n).get("status_controlador") or L.info_job(n).get("status_pe") for n in ("D_" + ev, "D_" + ev + "_R1")}
            continue
        nome, info = escolhido
        out = G.output_path(nome)
        usados[ev] = nome
        h = {"ANALYST_OUTPUT.json": _sha(out / "ANALYST_OUTPUT.json"), "PRIVATE_CONVERGENCE.json": _sha(out / "PRIVATE_CONVERGENCE.json")}
        for r in sorted(out.glob("*result*")):
            if r.is_file():
                h[r.name] = _sha(r)                     # so os bytes; o arquivo nao e aberto
        hashes[nome] = h
        saidas[ev] = json.loads((out / "ANALYST_OUTPUT.json").read_text(encoding="utf-8"))
    return saidas, hashes, sem, usados


def executar(eventos=None, destino=DESTINO):
    reg, dig = G.checked_registration()
    eventos = eventos or list(reg["eventos_d10"])
    v1, _ = V.carregar_v1()
    saidas, hashes, sem, usados = coletar(eventos)
    eg = EC.estagio_cego(saidas, v1)
    eg["hash_dos_posteriores_sha256"] = hashes
    eg["jobs_usados"] = usados
    eg["eventos_sem_analise_aceita"] = sem
    eg["custo_por_job"] = {n: {k: L.info_job(n).get(k) for k in ("wall_s", "cpu_s", "ncall", "delta_logz", "ess")} for n in usados.values()}
    eg["pinos_sha256"] = dig
    eg["aviso"] = ("ESTAGIO CEGO: nenhum valor central de dtau220 foi calculado ou gravado; a abertura exige AUTORIZACAO_ABERTURA_D.json do operador ligada ao sha256 deste arquivo.")
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    h = EC.publicar_estagio_cego(eg, destino)
    return eg, h


if __name__ == "__main__":
    eg, h = executar()
    print("PODER_RAMO_B_ANTES_DE_ABRIR.json sha256", h, "| eventos aceitos", eg["n_eventos_convergidos"], "| poder", round(eg.get("primario", {}).get("poder", float("nan")), 3))
