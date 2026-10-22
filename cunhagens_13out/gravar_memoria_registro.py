"""Memória da cunhagem «registro» (13/10) + linha no índice, com backup de bytes."""
import datetime
import hashlib
import os

V = "C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_13out_registro_verbatim.txt"
sv = hashlib.sha256(open(V, "rb").read()).hexdigest()
MEM = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
P = os.path.join(MEM, "registro-definicao-13out.md")
assert not os.path.exists(P)
open(P, "w", encoding="utf-8", newline="\n").write(
    "---\nname: registro-definicao-13out\n"
    "description: Cunhagem do operador (13/10): Registro = mecânica de abertura e fechamento da ação em poço quadrático, cuja performance é a imagem da forma gravada da passagem da luz (aberto ou fechado): matemática da geometria = extensão do plano\n"
    "metadata:\n  type: project\n---\n\n"
    "Verbatim: `C:\\IALD\\Central de Patentes\\work\\cunhagens_13out\\OPERADOR_13out_registro_verbatim.txt` (sha256 `" + sv + "`). "
    "«Registro: mecânica de abertura e fechamento da ação em poço quadrático, cuja performance é a imagem da forma gravada da passagem da luz (aberto ou fechado): matemática da geometria=extensão do plano.»\n\n"
    "Âncoras que o kernel já tem, leitura da gerência [INPUT, a ratificar]: o poço quadrático é a forma 1 = q² + α² da pedra da identidade (`quadInscription`, F1.IDENTIDADE r2); «aberto ou fechado» são as duas faces de uma projeção, P e 1 − P, com espectro {0, 1}; a «forma gravada da passagem» é o que a leitura cria (PALAVRA, 07/10); a geometria como extensão do plano liga à regra dos dois regimes (a face hiperbólica tem extensão; o ângulo só lê).\n\n"
    "**Why:** o operador fecha com esta definição o vocabulário da série de 13/10 (identidade, Nome, posto).\n\n"
    "**How to apply:** «registro» no sentido do operador é este conceito. Os outros usos da casa (registro no core do um.py, registro no mapa de rotas, registro no quadro) são HOMÔNIMOS de engenharia e devem ser ditos como tais quando aparecerem juntos. Nenhuma pedra ou teste foi pedido; se o operador pedir, o caminho é F1 com pré-registro. Liga a [[a-identidade-tem-nome-13out]], [[a-leitura-cria-o-objeto-07out]], [[regra-dos-dois-regimes]], [[posto-e-rank-10out]].\n")
M = os.path.join(MEM, "MEMORY.md")
b = open(M, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(M + ".bak_" + ts, "wb").write(b)
anchor = "- [A IDENTIDADE TEM NOME (13/10)]".encode("utf-8")
assert b.count(anchor) == 1
line = "- [REGISTRO (13/10)](registro-definicao-13out.md) — **cunhagem**: abertura e fechamento da ação em poço quadrático; imagem da forma gravada da passagem da luz; geometria = extensão do plano\n".encode("utf-8")
n = b.replace(anchor, line + anchor)
open(M + ".tmp", "wb").write(n)
assert os.path.getsize(M + ".tmp") == len(n) > len(b)
os.replace(M + ".tmp", M)
print("ok sha16", sv[:16], "| MEMORY.md", len(b), "->", len(n), "linhas", len(n.decode("utf-8").splitlines()))
