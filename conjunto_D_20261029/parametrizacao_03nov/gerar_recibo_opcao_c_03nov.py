# -*- coding: utf-8 -*-
"""gerar_recibo_opcao_c_03nov.py -- RECIBO_OPCAO_C_03nov.json: o que foi construido/rodado/registrado na execucao da opcao (c) em 03/11/2026, com sha256 lidos dos arquivos,
e os comandos de consulta/parada. Criacao exclusiva. Nao le nenhum posterior."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    cod = {p.name: sha(p) for p in sorted((HERE / "codigo_D").glob("*.py"))}
    arq = {}
    for p in sorted(HERE.rglob("*")):
        rel = p.relative_to(HERE).as_posix()
        if not p.is_file() or "__pycache__" in p.parts or rel.startswith("fila/") or ".bak_" in p.name or p.suffix in (".pending", ".tmp") or p.name == "RECIBO_OPCAO_C_03nov.json":
            continue
        arq[rel] = {"sha256": sha(p), "bytes": p.stat().st_size}
    ens = json.loads((HERE / "ENSAIO_PECAS_saida.json").read_text(encoding="utf-8"))
    rec = {
        "titulo": "Recibo da execucao da OPCAO (c) do teste D, 03/11/2026 (agente parametrizacao D por claude-c1)",
        "ordem": {"verbatim_sha256": json.loads((HERE / "ORDEM_LANCAMENTO_D_03nov.json").read_text())["ordem_operador_sha256"], "texto": "concordo com c, porque se o teste nao tiver poder nao vou inseri-lo no um.py"},
        "registrado_no_Mapa_antes_de_qualquer_PE": {"seq": 1744, "rota": "ringdown.ramo_b_preregistro_v386", "PINOS_D_V1.json": sha(HERE / "PINOS_D_V1.json"),
                                                    "compromisso_semente_sha256": json.loads((HERE / "PINOS_D_V1.json").read_text())["semente"]["compromisso_sha256"],
                                                    "CONGELAMENTO_D.json": sha(HERE / "CONGELAMENTO_D.json"), "JOBS_D_V1.json": sha(HERE / "JOBS_D_V1.json"), "RELOGIO_D.json": sha(HERE / "RELOGIO_D.json"),
                                                    "nota": "os pinos do seq 1737 (primeira parametrizacao) foram SUPERADOS por estes (pecas mecanicas + evento sintetico); nenhuma analise rodou com os antigos (backup .bak_ no mesmo diretorio)"},
        "pecas_novas_em_codigo_D": {k: v for k, v in cod.items() if k in ("pe_runner_D.py", "run_controlled_D.py", "lancar_fila_D.py", "orquestrador_fila_D.py", "estagio_cego_fila_D.py", "congelar_D.py", "consultar_fila_D.py")},
        "ensaio_sintetico_das_pecas_em_ambiente_temporario": ens["etapas"],
        "testes_sinteticos": "26/26 (TESTES_03nov_resultado_v2.json)",
        "como_consultar": {"windows": "C:\\Python314\\python.exe -X utf8 -B \"C:\\IALD\\Central de Patentes\\work\\conjunto_D_20261029\\parametrizacao_03nov\\codigo_D\\consultar_fila_D.py\"  (--json para maquina)",
                           "arquivos": ["fila\\ESTADO_FILA_D.json", "F4_1_CONVERGENCIA.json (quando a sintetica terminar)", "estagio_cego\\PODER_RAMO_B_ANTES_DE_ABRIR.json (ao fim da fila)", "fila\\orquestrador.log"]},
        "como_parar": "wsl.exe -d Ubuntu-24.04 -- pkill -f orquestrador_fila_D.py ; os run_controlled_D em curso terminam sozinhos no teto de parede; remover a tarefa: Unregister-ScheduledTask -TaskName IALD_D_FILA_OPCAO_C -Confirm:$false",
        "regras_enquanto_corre": ["NAO editar nada em codigo_D\\ nem em copias_somente_leitura\\ (cada job novo reconfere a arvore de codigo contra os pinos e recusa se mudou)",
                                  "NAO abrir PRIVATE.log, *_result.hdf5, *_dynesty.pickle nem ANALYST_OUTPUT.json dos jobs D_* (cegueira procedural)", "relogio vence em 21 dias a partir de 2026-11-03T13:17:40Z"],
        "hospedagem": "tarefa agendada do Windows IALD_D_FILA_OPCAO_C (mantem o wsl.exe vivo, independente da sessao do agente) -> orquestrador_fila_D.py no WSL /opt/lal_env",
        "arquivos": arq,
    }
    with open(HERE / "RECIBO_OPCAO_C_03nov.json", "xb") as f:
        f.write((json.dumps(rec, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode())
    print("recibo", sha(HERE / "RECIBO_OPCAO_C_03nov.json"), "| arquivos", len(arq))


if __name__ == "__main__":
    main()
