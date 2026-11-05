# -*- coding: utf-8 -*-
"""Cria work/iald_v407_20261104 copiando SO' as ferramentas da release anterior (v406), com bytes identicos, e grava COPIA_DA_V406.json.
Nao copia resultados (pacotes, plano, recibos, pareceres, deployment.json): deploy_controlled.py recusaria 'Existing deployment' e os recibos antigos se confundiriam com os novos.
Cada destino e' aberto com 'xb' (nunca sobrescreve). Hash lido por script."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

O = Path(r"C:\IALD\Central de Patentes\work\iald_v406_20261103")
D = Path(r"C:\IALD\Central de Patentes\work\iald_v407_20261104")

# (nome na v406, nome na v407)
ARQ = [
    ("release_cfg.py", "release_cfg.py"),
    ("task.py", "task.py"),
    ("mission_step.py", "mission_step.py"),
    ("verify_sources.py", "verify_sources.py"),
    ("verify_installed.py", "verify_installed.py"),
    ("deploy_controlled.py", "deploy_controlled.py"),
    ("maintenance.py", "maintenance.py"),
    ("transaction.py", "transaction.py"),
    ("measure_shared_capsules.py", "measure_shared_capsules.py"),
    ("builder_measurements.py", "builder_measurements.py"),
    ("exercita_busca.py", "exercita_busca.py"),
    ("run_construcao.sh", "run_construcao.sh"),
    ("run_etapa1_v406.sh", "run_etapa1_v407.sh"),
    ("run_etapa2_v406.sh", "run_etapa2_v407.sh"),
    ("check_literais_v406.py", "check_literais_v407.py"),
    ("fechar_registros.py", "fechar_registros.py"),
    ("LICOES_v406.md", "LICOES_v406.md"),
    ("LICOES_v406_AO_LADO.md", "LICOES_v406_AO_LADO.md"),
    ("app/prepare.py", "app/prepare.py"),
    ("app/finalize.py", "app/finalize.py"),
    ("app/count_final_public.py", "app/count_final_public.py"),
    ("app/validate_plan.py", "app/validate_plan.py"),
    ("app/preflight_offline.py", "app/preflight_offline.py"),
    ("app/RELEASE.json", "app/RELEASE.json"),
    ("app/build/fit_memory.py", "app/build/fit_memory.py"),
    ("app/build/fit_transport.py", "app/build/fit_transport.py"),
    ("app/build/haiku_codec.py", "app/build/haiku_codec.py"),
    ("review/review_app.py", "review/review_app.py"),
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    if D.exists():
        raise SystemExit("PARADA: " + str(D) + " ja existe; nada foi copiado.")
    D.mkdir(parents=True)
    linhas = []
    for src_rel, dst_rel in ARQ:
        src, dst = O / src_rel, D / dst_rel
        raw = src.read_bytes()
        dst.parent.mkdir(parents=True, exist_ok=True)
        with dst.open("xb") as f:
            f.write(raw)
        assert dst.read_bytes() == raw
        linhas.append({"arquivo_v406": src_rel.replace("/", "\\"), "arquivo_v407": dst_rel.replace("/", "\\"), "sha256_v406": sha(raw), "bytes": len(raw)})
    nao_copiado = sorted(p.name + ("\\" if p.is_dir() else "") for p in O.iterdir() if p.name not in {a for a, _ in ARQ})
    rec = {
        "origem": str(O), "destino": str(D),
        "o_que_copiou": "so' as ferramentas (scripts, codec, RELEASE.json, as duas licoes da v406); bytes identicos aos da v406 antes de qualquer edicao; tres arquivos mudam de nome (run_etapa1/2 e check_literais)",
        "arquivos": linhas,
        "nao_copiado_da_origem_nivel_1": nao_copiado,
        "porque": "resultados da v406 (pacotes, plano, recibos, pareceres, deployment.json) nao se levam: deploy_controlled.py recusa 'Existing deployment' e os recibos antigos se confundiriam com os da v407",
    }
    with (D / "COPIA_DA_V406.json").open("xb") as f:
        f.write(json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
    with (D / "criar_v407.py").open("xb") as f:
        f.write(Path(__file__).read_bytes())
    print(json.dumps({"copiados": len(linhas), "destino": str(D), "nao_copiado_nivel_1": len(nao_copiado)}, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
