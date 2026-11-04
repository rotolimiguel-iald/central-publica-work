# -*- coding: utf-8 -*-
"""registrar_mapa_opcao_c_03nov.py -- monta (e, com --registrar, registra) a ANOTACAO do Mapa de Rotas com os sha256 de PINOS_D_V1.json, do compromisso da semente,
de CONGELAMENTO_D.json, do relogio e da ordem de lancamento, LIDOS DOS ARQUIVOS, ANTES de qualquer PE. Uso: python registrar_mapa_opcao_c_03nov.py [--registrar]"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "codigo_D"))
import guard_D as G  # noqa: E402


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    pinos = json.loads(G.PINOS.read_text(encoding="utf-8"))
    rel = json.loads(G.RELOGIO.read_text(encoding="utf-8"))
    h = {"PINOS_D_V1.json": sha(G.PINOS), "SEMENTE_D_COMPROMISSO.json": sha(HERE / "SEMENTE_D_COMPROMISSO.json"), "compromisso_da_semente_(sha256 dos 32 bytes)": pinos["semente"]["compromisso_sha256"],
         "CONGELAMENTO_D.json": sha(G.CONGELAMENTO), "JOBS_D_V1.json": sha(G.JOBS), "RELOGIO_D.json": sha(G.RELOGIO), "ORDEM_LANCAMENTO_D_03nov.json": sha(HERE / "ORDEM_LANCAMENTO_D_03nov.json")}
    assert pinos["semente"]["compromisso_sha256"] == json.loads((HERE / "SEMENTE_D_COMPROMISSO.json").read_text())["compromisso_sha256"]
    assert rel["pinos_sha256"] == h["PINOS_D_V1.json"]
    base = str(HERE).replace(chr(92), "/")
    reg = [{
        "tipo": "ANOTACAO", "rota_id": "ringdown.ramo_b_preregistro_v386", "dominio": "RINGDOWN", "status": "EM_CURSO", "estatuto": "REAL", "olhou_dados": False,
        "titulo": "03/11/2026: OPCAO (c) autorizada pelo operador; pinos, semente, congelamento e relogio novo REGISTRADOS por hash ANTES de qualquer analise (agente parametrizacao D por claude-c1)",
        "pergunta": "A fila da opcao (c) do conjunto D foi congelada e carimbada antes de qualquer PE?",
        "dados": ["verbatim do operador 03/11 (sha256 " + json.loads((HERE / "ORDEM_LANCAMENTO_D_03nov.json").read_text())["ordem_operador_sha256"] + "): concordo com c, porque se o teste nao tiver poder nao vou inseri-lo no um.py",
                  "nenhum dado de D aberto; nenhuma PE ate este registro"],
        "metodo": "sha256 lidos dos arquivos por script (registrar_mapa_opcao_c_03nov.py): " + "; ".join("%s=%s" % (k, v) for k, v in h.items()),
        "resultado": "PINOS_D_V1.json " + h["PINOS_D_V1.json"] + " | compromisso da semente " + pinos["semente"]["compromisso_sha256"] + " | CONGELAMENTO_D.json " + h["CONGELAMENTO_D.json"] +
                     " | JOBS_D_V1.json " + h["JOBS_D_V1.json"] + " | RELOGIO_D.json " + h["RELOGIO_D.json"] + " (inicio " + rel["start_utc"] + ", prazo " + rel["hard_deadline_utc"] + ", " + str(rel["prazo_dias"]) +
                     " dias, opcao " + rel["opcao"] + "). Fila: F4.1 sintetica so-RG SNR 14 (amostrador congelado 512/50, ate 16 M chamadas, 30 h) -> 10 analises cegas de D, 2 em paralelo x 24 workers, "
                     "regra D5 (1 repeticao por bandeira de convergencia) -> estagio cego automatico (hash dos posteriores + poder real); a ABERTURA nao esta na fila.",
        "veredito": "TGL_RAMO_B_SET_D__OPTION_C_FROZEN_AND_CLOCK_OPENED__HASHES_REGISTERED_BEFORE_ANY_PE__NOTHING_OPENED__GATE_UNTOUCHED",
        "defeito": "a PE completa nunca convergiu na casa; F4.1 mede se o amostrador congelado converge no teto; se nao convergir a fila nao lanca (parede medida)",
        "proximo_passo": "F4.1 -> (se convergir) fila de 10 cegas -> estagio cego -> o operador decide a abertura com o poder real na mao",
        "onde": base,
        "artefatos": [base + "/" + n for n in ("PINOS_D_V1.json", "SEMENTE_D_COMPROMISSO.json", "CONGELAMENTO_D.json", "JOBS_D_V1.json", "RELOGIO_D.json", "ORDEM_LANCAMENTO_D_03nov.json", "DIFF_PECAS_MECANICAS.txt", "ENSAIO_PECAS_saida.json")],
        "nota": "NOT_FALSIFIED nunca e CONFIRMED; o gate nao se move; semente nunca impressa.",
    }]
    out = HERE / "rota_mapa_opcao_c_03nov.json"
    out.write_text(json.dumps(reg, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(h, indent=1))
    if "--registrar" in sys.argv:
        r = subprocess.run([sys.executable, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(out), "--quem", "agente parametrizacao D (sonnet) por claude-c1"], capture_output=True, text=True, encoding="utf-8")
        print(r.stdout[-600:], r.stderr[-400:])


if __name__ == "__main__":
    main()
