# -*- coding: utf-8 -*-
"""derivar_pecas_mecanicas.py -- deriva pe_runner_D.py e run_controlled_D.py das COPIAS somente-leitura (sha256 pinado) de e2_code_v1_1_2, por substituicoes de texto
EXATAS e enumeradas (cada uma tem de acertar exatamente o numero de vezes esperado, senao falha). Gera tambem DIFF_PECAS_MECANICAS.txt (diff unificado
copia -> derivada), para que a unica diferenca de logica seja visivel e auditavel. Nao toca a copia; nao toca Chatgpt\\."""
import difflib
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RO = HERE / "copias_somente_leitura"
DEST = HERE / "codigo_D"

CABECALHO_PE = '''# -*- coding: utf-8 -*-
# pe_runner_D.py -- DERIVADO de e2_code_v1_1_2/pe_runner.py (copia somente-leitura sha256 {sha}) por derivar_pecas_mecanicas.py.
# Unicas mudancas (ver DIFF_PECAS_MECANICAS.txt): (1) `registration_guard` -> `guard_D` (guarda novo pinado ao V1 do ramo B);
# (2) sys.path inclui codigo_D e copias_somente_leitura (pseob_source, strain_io, remnant_conversion sao as COPIAS byte-identicas);
# (3) `blinding` -> `blinding_D` (semente nova, etiqueta HMAC propria); (4) `injection_design` -> `injecao_c2` (copia RO + 2 trocas em memoria).
# Nenhuma outra linha de logica foi alterada.
'''
CABECALHO_RC = '''# -*- coding: utf-8 -*-
# run_controlled_D.py -- DERIVADO de e2_code_v1_1_2/run_controlled.py (copia somente-leitura sha256 {sha}) por derivar_pecas_mecanicas.py.
# Unicas mudancas (ver DIFF_PECAS_MECANICAS.txt): (1) `registration_guard` -> `guard_D`; (2) o filho e pe_runner_D.py;
# (3) o teto de parede do modo calibration deixa de ser 10 h fixas e passa a ser reg['limites']['wall_max_calibracao_s'] (do CONGELAMENTO, ligado aos pinos),
#     porque a qualificacao F4.1 precisa medir convergencia alem das 10 h do piloto (default continua 10 h se o congelamento nao disser). Nenhuma outra logica mudou.
'''

SUBST_PE = [
    ("from registration_guard import (checked_registration,authorize_event,time_guard,contained,sha,\n    load_jobs,validate_launch,positive,integer,publish_new,utc)",
     "import sys\nfrom pathlib import Path as _P\nsys.path.insert(0, str(_P(__file__).resolve().parents[1] / 'copias_somente_leitura'))\nsys.path.insert(0, str(_P(__file__).resolve().parent))\n"
     "from guard_D import (checked_registration,authorize_event,time_guard,contained,sha,\n    load_jobs,validate_launch,positive,integer,publish_new,utc)", 1),
    ("from blinding import shifted_samples", "from blinding_D import shifted_samples", 1),
    ("from injection_design import inject_into_ifos", "from injecao_c2 import carregar_injection_design\n            inject_into_ifos=carregar_injection_design().inject_into_ifos", 1),
]
SUBST_RC = [
    ("from registration_guard import (checked_registration,time_guard,output_path,sha,load_jobs,\n    positive,integer,publish_new,authorize_event)",
     "from guard_D import (checked_registration,time_guard,output_path,sha,load_jobs,\n    positive,integer,publish_new,authorize_event)", 1),
    ("Path(__file__).with_name('pe_runner.py')", "Path(__file__).with_name('pe_runner_D.py')", 1),
    ("if cfg['mode']=='calibration' and wall>10*3600:raise ValueError('Pilot wall cap 10h')",
     "if cfg['mode']=='calibration' and wall>reg.get('limites',{}).get('wall_max_calibracao_s',10*3600):raise ValueError('Calibration wall cap exceeded')", 1),
]


def derivar(nome_origem, nome_destino, subst, cabecalho):
    src_path = RO / nome_origem
    raw = src_path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    pins = {}
    for linha in (HERE / "copias_somente_leitura.SHA256.txt").read_text().splitlines():
        h, n = linha.split(None, 1)
        pins[n.strip().lstrip("*")] = h
    if pins[nome_origem] != sha:
        raise SystemExit("copia RO difere do sha256 registrado: " + nome_origem)
    txt = raw.decode("utf-8")
    for old, new, n in subst:
        if txt.count(old) != n:
            raise SystemExit("substituicao nao acertou %d vez(es): %r (%d)" % (n, old[:70], txt.count(old)))
        txt = txt.replace(old, new)
    out = cabecalho.format(sha=sha[:16]) + txt
    (DEST / nome_destino).write_text(out, encoding="utf-8", newline="\n")
    diff = "".join(difflib.unified_diff(raw.decode("utf-8").splitlines(True), out.splitlines(True), nome_origem, nome_destino, n=0))
    return diff


if __name__ == "__main__":
    d1 = derivar("pe_runner.py", "pe_runner_D.py", SUBST_PE, CABECALHO_PE)
    d2 = derivar("run_controlled.py", "run_controlled_D.py", SUBST_RC, CABECALHO_RC)
    (HERE / "DIFF_PECAS_MECANICAS.txt").write_text(d1 + "\n" + d2, encoding="utf-8")
    print("derivados; linhas de diff:", len((d1 + d2).splitlines()))
