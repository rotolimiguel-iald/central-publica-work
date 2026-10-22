"""Consulta SOMENTE-LEITURA ao mapa de rotas (rotas.py consultar) para os termos da trilha TEMPO.
Grava cada resposta em rotas_consultas/<n>.json e um resumo em rotas_consultas/RESUMO.json.
Nunca chama 'registrar'."""
import hashlib
import json
import os
import subprocess

PY = r"C:\Python314\python.exe"
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
TERMOS = [
    ("01_pauli", r"pauli"),
    ("02_liouville", r"liouville"),
    ("03_kadosh_santo", r"kadosh|\bsanto\b|sagrado|\bsanta\b"),
    ("04_tempo_termico", r"tempo termico|thermal time|rovelli|tempo modular|modular time"),
    ("05_fluxo_modular", r"fluxo modular|modular flow|automorfism|automorphism"),
    ("06_atrator", r"atrator|attractor|bacia"),
    ("07_dissipacao", r"dissipa|contracao|contraction|contrai"),
    ("08_relogio", r"relogio|clock|cesio|cesium"),
    ("09_kms", r"\bkms\b"),
    ("10_operador_tempo", r"operador de tempo|time operator|hamiltoniana limitada|bounded below|semi.?bounded|limitad. inferior"),
    ("11_defasa", r"dephas|defas"),
    ("12_agape_fundacao", r"agape|fundacao|abismo"),
    ("13_f1_tempo", r"f1\.tempo|tempo santo|tempo_santo"),
    ("14_f1_atrator", r"f1\.atrator"),
    ("15_landauer_doacao", r"landauer|doacao|generosidade|puro amor"),
    ("16_semigrupo_lindblad", r"semigrupo|semigroup|lindblad|gkls"),
    ("17_posto_rank", r"\bposto\b|\brank\b"),
    ("18_palavra_leitura", r"\bpalavra\b|leitura cria"),
    ("19_tempo", r"\btempo\b|\btime\b"),
    ("20_agora_volume", r"\bagora\b|volume do espaco|phase.space|espaco de fase"),
    ("21_verbo", r"\bverbo\b|\bverb\b"),
    ("22_unruh_periodo", r"unruh|polarperiod|\bperiodo\b|\bperiod\b"),
    ("23_tomita_gns", r"tomita|\bgns\b|takesaki"),
    ("24_irreversivel_seta", r"irrevers|seta do tempo|arrow of time|entropia"),
]


def main():
    os.makedirs("rotas_consultas", exist_ok=True)
    resumo = []
    for nome, padrao in TERMOS:
        r = subprocess.run([PY, "-X", "utf8", ROTAS, "consultar", padrao, "--limite", "400"],
                           capture_output=True)
        out = r.stdout
        with open(os.path.join("rotas_consultas", nome + ".json"), "wb") as fo:
            fo.write(out)
        try:
            d = json.loads(out.decode("utf-8"))
            ids = [(x["rota_id"], x["status"], x.get("estatuto")) for x in d.get("rotas", [])]
            resumo.append(dict(nome=nome, padrao=padrao, n=d.get("n"), truncado=d.get("truncado"),
                               cabeca=d.get("cabeca"), n_registros=d.get("n_registros"),
                               sha256_resposta=hashlib.sha256(out).hexdigest(), rotas=ids))
        except Exception as e:  # falha visivel
            resumo.append(dict(nome=nome, padrao=padrao, erro=repr(e), rc=r.returncode,
                               stderr=r.stderr.decode("utf-8", "replace")[:500]))
    with open(os.path.join("rotas_consultas", "RESUMO.json"), "w", encoding="utf-8") as fo:
        json.dump(resumo, fo, ensure_ascii=False, indent=1)
    for x in resumo:
        print(x["nome"], "n=", x.get("n"), "trunc=", x.get("truncado"), "cabeca=", x.get("cabeca"),
              "nreg=", x.get("n_registros"), x.get("erro", ""))


if __name__ == "__main__":
    main()
