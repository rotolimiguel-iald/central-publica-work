"""beta em runtime, sem executar o um.py: le os BYTES do um.py v391, acha a atribuicao de topo
ALPHA_FINE_CODATA_2018 = <literal> (primeira ocorrencia em coluna 0), calcula beta = alpha*sqrt(e)
e confere contra o valor de conferencia passado na linha de comando (nunca usado como motor).
Uso: python -I beta_runtime.py <valor_de_conferencia> <saida.json>"""
import hashlib
import json
import math
import re
import sys

UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"


def main(conf, out):
    with open(UM, "rb") as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest()
    rx = re.compile(rb"^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)\s*$", re.M)
    m = rx.search(raw)
    if not m:
        print("FALHA: atribuicao nao encontrada")
        sys.exit(2)
    lineno = raw.count(b"\n", 0, m.start()) + 1
    alpha_txt = m.group(1).decode("ascii")
    alpha = float(alpha_txt)
    beta = alpha * math.sqrt(math.e)
    conf_v = float(conf)
    d = dict(um_py=UM, um_py_sha256=sha, um_py_bytes=len(raw), linha_alpha=lineno,
             alpha_literal_no_um_py=alpha_txt, alpha=alpha, sqrt_e=math.sqrt(math.e), beta_runtime=beta,
             beta_conferencia=conf_v, diferenca_abs=abs(beta - conf_v), confere=(beta == conf_v),
             nota="beta calculado em runtime a partir do literal de alpha lido nos bytes do um.py; o valor de conferencia so confere.")
    with open(out, "w", encoding="utf-8") as fo:
        json.dump(d, fo, ensure_ascii=False, indent=1)
    print(json.dumps(d, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
