"""Registra a investigação do sorry no mapa e acrescenta AO LADO no PLANO_V392 (backup de bytes)."""
import datetime
import hashlib
import json
import os
import subprocess

W = r"C:\IALD\Central de Patentes\work\umpy_sorry_check_13out"
PLANO = r"C:\IALD\PROGRAMA_IALD\exame_12out\J_SINTESE\PLANO_V392.md"
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"


def run(a, cwd=None):
    r = subprocess.run(["python"] + a, capture_output=True, text=True, encoding="utf-8", cwd=cwd)
    return (r.stdout or "") + (r.stderr or "")


for n in ("registro_rota_umpy_sorry.json", "registro_mapa_umpy_sorry.json"):
    o = run([ROTAS, "registrar", os.path.join(W, n), "--quem", "claude-c1 (gerência)"])
    try:
        j = json.loads(o)
        print("mapa", n, j.get("ok"), [g.get("seq") for g in j.get("gravados", [])], j.get("erro"))
    except Exception:
        print("mapa", n, o[-400:])

sh = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
rel = os.path.join(W, "RELATORIO_SORRY_CHECK.md")
prop = os.path.join(W, "PROPOSTA_V392.md")
b = open(PLANO, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(PLANO + ".bak_" + ts, "wb").write(b)
add = ("\n\n---\n\n## 12-ter. AO LADO (13/10/2026, gerência c1, em nome próprio): a detecção de sorry nos controles da bancada\n\n"
       "Achado da reauditoria curta do vínculo (F0.6, R3) e medido por investigação sem rodar o um.py (relatório `" + rel + "`, sha16 " + sh(rel) + "; proposta `" + prop + "`, sha16 " + sh(prop) + "):\n\n"
       "1. `prove_bench_lean_controls` (um.py v391, l.192945) procura o aviso de sorry com aspas simples; o Lean 4.31 o escreve com crases. A barreira está cega [REAL]. Na v391 não teve efeito: os 52 controles positivos não contêm sorry no código-fonte (medido), e o kernel principal decide por `#print axioms` (`sorryAx_absent`), imune ao formato. `bench_lean_controls` não decide o gate.\n"
       "2. A v392 troca a l.192945 por regex que aceita os dois formatos e soma a leitura dos axiomas da saída (proposta A); de preferência um rodapé `collectAxioms` para os 10 positivos sem `#print axioms` (proposta B, a compilar em sandbox antes); e um autoteste sem Lean com a saída `SorryTerm` já embutida (proposta C). Errata ao lado do parágrafo v362 do artigo.\n"
       "3. Achado lateral: a varredura lexical `_LEAN_FORBIDDEN_TOKENS` (l.134595, função na l.134690) não é recursiva e deixa fora 150 `.lean` de `TGLExt/O16`; varrida a árvore inteira, 0 tokens proibidos hoje. A v392 torna a varredura recursiva.\n"
       "4. O mesmo defeito estava no esboço da Bancada (R3-A1); a R3.1 o corrige com controle no formato real.\n\n"
       "Nada aqui move o gate.\n")
n = b + (b"" if b.endswith(b"\n") else b"\n") + add.encode("utf-8")
for bad in (b"\t", b"\x04", b"\x05", b"\x0c"):
    assert bad not in add.encode("utf-8")
open(PLANO + ".tmp", "wb").write(n)
assert os.path.getsize(PLANO + ".tmp") == len(n) > len(b)
os.replace(PLANO + ".tmp", PLANO)
print("plano", len(b), "->", len(n), "sha16", hashlib.sha256(n).hexdigest()[:16])
