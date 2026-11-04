# -*- coding: utf-8 -*-
"""abrir_relogio_03nov.py -- ATO DE LANCAMENTO da opcao (c): escreve ORDEM_LANCAMENTO_D_03nov.json citando como ordem o VERBATIM do operador (caminho + sha256 lido do arquivo)
e abre o relogio novo com guard_D.abrir_relogio (prazo de 21 dias, ligado ao hash dos pinos). Criacao exclusiva; roda UMA vez, depois do congelamento e ANTES de qualquer PE."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "codigo_D"))
import guard_D as G  # noqa: E402

VERBATIM = Path("C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_03nov_decisoes_psion_graviton_estado_ligado_projetor_4x4_nomes_ratificados_teste_d_opcao_c_motor_banho_holografico_verbatim.txt")
VERBATIM_SHA16_DA_GERENCIA = "73466598d3419fb0"
PRAZO_DIAS = 21


def main():
    raw = VERBATIM.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha.startswith(VERBATIM_SHA16_DA_GERENCIA), "verbatim difere do sha16 informado pela gerencia"
    ordem = {"opcao": "c", "ordem_operador_sha256": sha, "ordem_operador_caminho": str(VERBATIM).replace(chr(92), "/"), "ordem_operador_bytes": len(raw),
             "decidido_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "citacao_operador": "concordo com c, porque se o teste nao tiver poder nao vou inseri-lo no um.py (03/11/2026; a partitura PARTITURA_D_03nov.md foi lida a ele pela gerencia antes)",
             "escopo": "OPCAO (c): F4.1 sintetica + 10 analises CEGAS de D ate o ESTAGIO CEGO; a ABERTURA e outra decisao do operador, com o poder real na mao",
             "quem_executa": "agente de parametrizacao D (sonnet) por claude-c1"}
    p = HERE / "ORDEM_LANCAMENTO_D_03nov.json"
    with open(p, "xb") as f:
        f.write((json.dumps(ordem, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode())
    r = G.abrir_relogio(PRAZO_DIAS, p)
    print("ORDEM_LANCAMENTO sha256", hashlib.sha256(p.read_bytes()).hexdigest())
    print("RELOGIO_D.json sha256", hashlib.sha256(G.RELOGIO.read_bytes()).hexdigest(), "| inicio", r["start_utc"], "| prazo", r["hard_deadline_utc"])


if __name__ == "__main__":
    main()
