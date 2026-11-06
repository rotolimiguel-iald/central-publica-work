"""Probe the local instrument with a known two-level density matrix, without observations."""
import hashlib
import json
import math
import re
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener

HERE = Path(__file__).resolve().parent
PROGRAM = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
ROOT = "http://127.0.0.1:18777/api/"
OPENER = build_opener(ProxyHandler({}))


def call(endpoint, payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(ROOT + endpoint, data=body, headers={"Content-Type": "application/json"})
    with OPENER.open(request, timeout=20) as response:
        return json.load(response)


def main():
    output = HERE / "BANCADA_SINTETICA.json"
    if output.exists():
        raise FileExistsError("Recibo existente. Use o arquivo para reproduzir os cálculos locais.")
    contract = call("contratos")
    program = PROGRAM.read_bytes()
    if not contract.get("ok") or hashlib.sha256(program).hexdigest() != contract["um_py_sha256"]:
        raise ValueError("Contrato ativo diverge dos bytes do programa")
    alpha_lines = re.findall(rb"^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([0-9.eE+-]+)[ \t]*\r?$", program, re.M)
    if len(alpha_lines) != 1:
        raise ValueError("Constante canônica ausente ou ambígua")
    beta = float(alpha_lines[0]) * math.sqrt(math.e)
    if not math.isclose(beta, contract["beta_tgl"], rel_tol=2e-15):
        raise ValueError("Acoplamento local diverge do instrumento")
    eta = 2 * math.sqrt(beta * (1 - beta))
    matching_time = -2 * math.log(eta) / beta
    # Logical |A>-i|B>, normalized; off-diagonal = +i/2.
    rho = [[[0.5, 0], [0, 0.5]], [[0, -0.5], [0.5, 0]]]
    receipts = {}
    for label, time in (("controle_zero", 0.0), ("tempo_unitario", 1.0),
                        ("equivalencia_algebrica_uma_passagem", matching_time),
                        ("equivalencia_algebrica_duas_passagens", 2 * matching_time)):
        payload = dict(channel="modular_root_dephasing", modular_eigenvalues=[0, 1], s=time, rho=rho)
        result = call("neutrino/sintetico", payload)
        receipts[label] = {"request": payload, "response": result}
    record = {"estatuto": "SIMULACAO_CONDICIONAL", "contract": contract, "beta": beta,
              "eta": eta, "matching_time_dimensionless": matching_time, "samples": receipts}
    with output.open("x", encoding="utf-8") as writer:
        json.dump(record, writer, ensure_ascii=False, indent=2)
    for label, receipt in receipts.items():
        print(label, list(receipt["response"]), str(receipt["response"].get("rho", ""))[:160])


if __name__ == "__main__":
    main()
