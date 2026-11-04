# -*- coding: utf-8 -*-
"""gerar_manifesto_03nov.py -- manifesto com sha256 (lido do disco) de TUDO o que a parametrizacao de 03/11/2026 produziu. Criacao exclusiva; nao toca nenhum outro arquivo."""
import hashlib
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPEL = {
    "PINOS_D_V1.json": "pinos do guarda novo: V1, 10 eventos sem hold, GPS, strain (manifesto O4), arvore de codigo, copias RO, semente (compromisso), runtime WSL",
    "SEMENTE_D_COMPROMISSO.json": "compromisso (sha256) da semente de cegueira; o valor nunca foi impresso e mora em ~/.iald_privado",
    "DESENHO_C2_03nov.json": "desenho das injecoes C2 em off-source real dos eventos de D (10/20/50 analises)",
    "PODER_RAMO_B_ANTES_DE_ABRIR.json": "RASCUNHO de planejamento do poder (sem dado); o estagio cego real grava PODER_RAMO_B_ANTES_DE_ABRIR_REAL.json",
    "JOBS_D_V1.PROPOSTA.json": "proposta de jobs (10 cegos + 50 C2) validada pelo guarda e pelo pe_runner original; NAO congelada (D2 aberto)",
    "ESCOLHAS_DO_DESENHO_03nov.json": "escolhas do desenho ditas antes, com onde vivem e o que mudam",
    "PARTITURA_D_03nov.md": "partitura ao operador (o que decide, o que nao, o que o negativo significa, custo, as tres opcoes)",
    "SMOKE_03nov.md": "o que rodou, tempos e resultados da fumaca sintetica",
    "TESTES_03nov_resultado.json": "saida dos 20 testes sinteticos (Windows)",
    "SMOKE_WSL_saida.json": "saida da fumaca no WSL (injecao C2 pelo injetor original, fatia de verossimilhanca em ruido zero, anti-CLI, runtime)",
    "runtime_wsl.json": "versoes do runtime /opt/lal_env",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    arquivos = {}
    for p in sorted(HERE.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or p.name == "MANIFESTO_PARAMETRIZACAO_03nov.json" or p.suffix in (".pending", ".tmp") or ".bak_" in p.name:
            continue
        rel = p.relative_to(HERE).as_posix()
        papel = PAPEL.get(rel) or ("codigo (pinado em PINOS_D_V1.json)" if rel.startswith("codigo_D/") else
                                    "copia SOMENTE-LEITURA byte-identica de e2_code_v1_1_2 (nao editar)" if rel.startswith("copias_somente_leitura/") else "script/auxiliar")
        arquivos[rel] = {"sha256": sha(p), "bytes": p.stat().st_size, "papel": papel}
    pinos = json.loads((HERE / "PINOS_D_V1.json").read_text(encoding="utf-8"))
    m = {"titulo": "Manifesto da parametrizacao do teste D (ramo B do ringdown) de 03/11/2026", "gerado_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "v1_sha256": pinos["v1"]["json_sha256"], "pinos_sha256": sha(HERE / "PINOS_D_V1.json"), "semente_compromisso_sha256": pinos["semente"]["compromisso_sha256"],
         "estado": "PARAMETRIZADO_SEM_LANCAR: nenhum dado de D aberto; nenhuma PE; relogio novo NAO aberto; V1 intocado; Chatgpt\\ intocado; um.py/selo/kernel/gate intocados",
         "falta_para_lancar": ["decisao do operador sobre a opcao (a)/(c)/(b) e o tamanho de C2 (10/20/50)", "F4.1 mede o custo ate convergir e fixa D2 (amostrador e parede)",
                               "pe_runner_D.py e run_controlled_D.py (troca mecanica de import; guard_D tem a API), lancador de fila com a regra D5, congelar_D.py (JOBS_D_V1.json + CONGELAMENTO_D.json)",
                               "ato de abrir o relogio (guard_D.abrir_relogio) com a ordem de lancamento", "registrar o sha256 dos pinos no Mapa como carimbo antes de qualquer PE"],
         "arquivos": arquivos}
    raw = (json.dumps(m, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    with open(HERE / "MANIFESTO_PARAMETRIZACAO_03nov.json", "xb") as f:
        f.write(raw)
    print("manifesto", hashlib.sha256(raw).hexdigest(), "| arquivos", len(arquivos))


if __name__ == "__main__":
    main()
