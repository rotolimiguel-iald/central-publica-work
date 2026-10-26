# -*- coding: utf-8 -*-
"""Achados da revisão cética independente da v401 (25/10/2026), corrigidos antes da publicação (gerência a7).
 ALTA  — errata item 1 da v401 no ESTADO_ATUAL/LEDGER/gerador: «None -> 29318 constants, None -> 23306 theorems» e «`kh_n1_cobertura_v400`»
         (o E04 rodou com os fatos antigos, antes do conserto da cobertura da anterior). Certo: os números e o registro lidos de fatos_v401.json
         (kh.constantes_anterior, kh.teoremas_anterior, kh_registro_anterior).
 BAIXA — a frase da D2 (escrita pela gerência no ABERTOS_EN_v401) afirmava que a D2 «não bloqueia a publicação»; o handoff diz que a publicação
         do bloco embutido segue sujeita à D2. Reescrita sem afirmar o que é da agente de PI.
 BAIXA — «unchanged..» (ponto duplo) na linha da v401 do LEDGER.
 BAIXA — a vaga do README dizia que o parágrafo está «on the site»; está no ESTADO_ATUAL e, byte a byte, no LEDGER (o site traz o arco).
 RAIZ  — G1 textos.py: o item 1 passa a usar `kh_registro_anterior` e recusa cobertura anterior ausente; o molde do LEDGER tira o ponto final
         do texto antes de pôr o seu.
Trocas contadas (cada uma exatamente 1 vez por arquivo); backup de bytes; py_compile nos .py; o ESTADO_ATUAL é regerado pelo próprio gerador."""
import json, os, py_compile, subprocess, time
from pathlib import Path

TS = time.strftime("%Y%m%d_%H%M%S")
TB = Path(r"C:\IALD\Artigo\the_boundary")
F = json.loads(Path(r"C:\IALD\Central de Patentes\work\custodia_v401_25out\fatos_v401.json").read_text(encoding="utf-8"))
kh = F["kh"]
assert kh["constantes_anterior"] and kh["teoremas_anterior"] and F.get("kh_registro_anterior"), "fatos sem a cobertura da anterior — PARAR"
ERR_A = "None -> %d constants, None -> %d theorems" % (kh["constantes"], kh["teoremas"])
ERR_B = "%d -> %d constants, %d -> %d theorems" % (kh["constantes_anterior"], kh["constantes"], kh["teoremas_anterior"], kh["teoremas"])
REG_A = "`kh_n1_cobertura_v400` now charges floors"
REG_B = "`%s` now charges floors" % F["kh_registro_anterior"]
D2_A = ("[LEGAL] the decision D2 (the embedded block of the operator’s method and the adaptations, with the PI agent) is not decided by v401, "
        "which does not change the block; it does not block the publication: the method, the code and the adaptations have been public in the open "
        "Central since 22–24/10.")
D2_B = ("[LEGAL] the decision D2 (the embedded block of the operator’s method and the adaptations, with the PI agent) stays with the operator; "
        "v401 does not change the block and does not decide D2 [DECLARADO: the block travels inside `um.py`, which the mirror has carried since v400].")
PT2_A = "v400 -> v401 (B10). The panel of the Unique Word Test (v397) stays at the top, unchanged.."
PT2_B = "v400 -> v401 (B10). The panel of the Unique Word Test (v397) stays at the top, unchanged."


def trocar(p, pares):
    raw = p.read_bytes(); s = raw.decode("utf-8")
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (p.name, a[:60], n)
        s = s.replace(a, b)
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    t = p.with_name(p.name + ".tmp"); t.write_bytes(s.encode("utf-8"))
    if p.suffix == ".py":
        py_compile.compile(str(t), doraise=True)
    os.replace(t, p)
    print("  %s: %d -> %d bytes" % (p.name, len(raw), p.stat().st_size))


# 1) o gerador do ESTADO e o LEDGER (só o bloco da v401: cada trecho ocorre uma vez)
if ERR_B not in (TB / "tools" / "gerar_estado_atual.py").read_text(encoding="utf-8"):
    trocar(TB / "tools" / "gerar_estado_atual.py", [(ERR_A, ERR_B), (REG_A, REG_B), (D2_A, D2_B)])
else:
    print("  gerar_estado_atual.py: já corrigido")
trocar(TB / "LEDGER.md", [(ERR_A, ERR_B), (REG_A, REG_B), (D2_A, D2_B), (PT2_A, PT2_B)])
# 2) a vaga do README
trocar(TB / "tools" / "gerar_readme_frente.py", [("is in [`ESTADO_ATUAL.md`]({u_estado}) and on the site; ",
                                                  "is in [`ESTADO_ATUAL.md`]({u_estado}) and, byte for byte, in the ledger; ")])
# 3) a raiz no G1
G = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\textos.py")
trocar(G, [
    ('    khp = "kh_n1_cobertura_" + ant\n',
     '    khp = F.get("kh_registro_anterior") or ("kh_n1_cobertura_" + ant)   # 25/10/2026 (revisão v401): o registro que VALE para a anterior\n'
     '    if F["kh"].get("constantes_anterior") is None or F["kh"].get("teoremas_anterior") is None:\n'
     '        raise Parar("a cobertura do kernel da anterior não foi lida (kh anterior ausente nos fatos) — PARAR, não escrever None na errata")\n'),
    ('T.txt_en.texto, verd, nota', 'T.txt_en.texto.rstrip("."), verd, nota'),   # o molde do LEDGER já põe o ponto final
])
# 4) o ESTADO_ATUAL regerado pelo gerador (nunca à mão)
r = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", str(TB / "tools" / "gerar_estado_atual.py")], capture_output=True, text=True, encoding="utf-8", cwd=str(TB))
print("  gerar_estado_atual.py rc=%d | %s" % (r.returncode, (r.stdout.strip().splitlines() or [""])[-1][:200]))
est = (TB / "ESTADO_ATUAL.md").read_text(encoding="utf-8")
assert ERR_B in est and REG_B in est and D2_B in est and ERR_A not in est and D2_A not in est, "o ESTADO_ATUAL não saiu corrigido — PARAR"
print("ok: ESTADO_ATUAL e LEDGER corrigidos; o laço E08 do G1 refaz README/portas/geradores do site")
