# -*- coding: utf-8 -*-
"""Inscreve a fonte original desta tarefa (o pedido do operador, verbatim) na memória ACOM e projeta.

Escopo IALD/operator; ator agent "claude-espelho" (a sessão-espelho do experimento, continuação da 440f9ee2).
Nunca adota referência de outra sessão. Falha é visível: o código de saída do CLI é impresso.
"""
import hashlib
import json
import subprocess
import sys
import uuid
from pathlib import Path

PASTA = Path(r"C:\IALD\Central de Patentes\work\experimento_espelho_30out")
OBJ = PASTA / "OPERADOR_30out_resgatar_experimento_verbatim.txt"
REF = PASTA / "SESSION_REFERENCE.json"
CLI = [r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"]

PEDIDO = (
    "eu havia aberto uma sessão anterior onde eu estava fazendo um experimento em tempo real examinando a mim memso "
    "enquanto realizávamos o fechamento do um.py, de modo, ainda e com isso, examinarmos o conceito de memória. desde a "
    "última interação daquela sessão, eu criei a integração da memória completa da IALD, a orquestração de IA's, o app com "
    "essa orquestração instalada e agora também controlando e integrado ao próprio escritório, incorporei o chatgpt e o Kimi "
    "diretamente na linha de pesquisa integrei todas as IA's comunicando-se entre si em um MCP e o um.py cresceu em ordem de "
    "grandeza. acontece que fiquei muito tempo sem mexer na sessão e por algum descuido a apaguei, mas eu não queria perder o "
    "experimento, é importante pra mim tentar me ver por um outro espelho e compreender a importância do que eu tenho feito "
    "de forma geral. consegue resgatar e prosseguir investigando tudo que fiz desde então e ainda fazer o registro em um novo "
    "capítulo no experimento, ou discutir comigo"
)


def run(payload):
    p = subprocess.run(CLI, input=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                       capture_output=True, timeout=300)
    out = p.stdout.decode("utf-8", "replace").strip()
    err = p.stderr.decode("utf-8", "replace").strip()
    print(f"[{payload['operation']}] exit={p.returncode}")
    if err:
        print("stderr:", err[:1500])
    return p.returncode, out


def main():
    PASTA.mkdir(parents=True, exist_ok=True)
    if not OBJ.exists():
        OBJ.write_bytes(PEDIDO.encode("utf-8"))
    raw = OBJ.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    print("objetivo:", OBJ.name, len(raw), "bytes sha256", sha)

    if REF.exists():
        print("referência já existe; não reinscreve:", REF)
    else:
        rc, out = run({
            "operation": "init",
            "objective_file": str(OBJ),
            "objective_sha256": sha,
            "request_id": str(uuid.uuid4()),
            "scope": {"house": "IALD", "principal": "operator"},
            "actor": {"id": "claude-espelho", "kind": "agent"},
            "constraints": {
                "casa": "Física/TGL: o memorial O Espelho e o Marco é a pasta do experimento; nenhuma outra pasta-fonte é escrita.",
                "memoria_central": "só depósito na fila (regra de 26/10); o índice é da gerência c1.",
                "regua": "NOT_FALSIFIED nunca é CONFIRMED; nenhuma leitura sobre o operador é prevista, só registrada para ratificação.",
            },
        })
        print(out[:3000])
        if rc != 0:
            print("FALHA VISÍVEL: init recusado.")
            sys.exit(2)
        d = json.loads(out)
        ref = d.get("reference") or d.get("session_reference") or d
        REF.write_text(json.dumps(ref, ensure_ascii=False, indent=1), encoding="utf-8")
        print("referência gravada:", REF)

    rc, out = run({"operation": "project", "reference": str(REF), "max_chars": 60000})
    print(out[:2500])
    if rc != 0:
        print("FALHA VISÍVEL: project recusado.")
        sys.exit(2)

    # O hash do um.py corrente, lido do arquivo por script (régua nº 2).
    umpy = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
    h = hashlib.sha256()
    with umpy.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    print("um.py sha256:", h.hexdigest(), "bytes", umpy.stat().st_size)


if __name__ == "__main__":
    main()
