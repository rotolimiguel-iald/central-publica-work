# -*- coding: utf-8 -*-
"""patch_esboco_r35.py (R3.5, 19/10/2026) -- aplica ao sincronizar_bancada.py da R3.4 (copia de bytes em R3_5) o UNICO conserto da R3.5: a lista de permissao estrita do modulo de auditoria.
Guarda a copia pristina em _construcao/sincronizar_bancada_R3_4_original.py (para o diff) e escreve o novo esboco por arquivo temporario + os.replace.
uso: python -I -B -X utf8 patch_esboco_r35.py"""
import hashlib
import os
import sys
sys.dont_write_bytecode = True
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
ESB = AQUI / "sincronizar_bancada.py"
ORIG = AQUI / "_construcao" / "sincronizar_bancada_R3_4_original.py"
R34 = AQUI.parent / "R3_4" / "sincronizar_bancada.py"      # a referencia: o esboco da R3.4 no disco (nenhum hash digitado)

raw = ESB.read_bytes()
assert raw == R34.read_bytes(), "o esboco de partida nao e, byte a byte, o da R3.4"
if not ORIG.exists():
    with open(ORIG, "xb") as f:
        f.write(raw)
t = raw.decode("utf-8")
assert "\r" not in t

constantes = (AQUI / "_construcao" / "bloco_constantes_auditoria_r35.txt").read_text(encoding="utf-8")
funcao = (AQUI / "_construcao" / "bloco_funcao_auditoria_r35.txt").read_text(encoding="utf-8")
assert constantes.endswith("\n") and funcao.endswith("\n\n")


def cortar(t, ini, fim, novo):
    assert t.count(ini) == 1 and t.count(fim) == 1, (ini[:60], t.count(ini), fim[:60], t.count(fim))
    a, b = t.index(ini), t.index(fim)
    assert a < b
    return t[:a] + novo + t[b:]


def sub(t, velho, novo):
    assert t.count(velho) == 1, (velho[:80], t.count(velho))
    return t.replace(velho, novo)


t = cortar(t, "# R3.4 (M): o modulo de auditoria so tem comandos de auditoria (import, open, #print axioms, run_cmd);", "# N5/N16: a gramatica FECHADA do comando de um teste", constantes)
t = cortar(t, "def auditar_fonte_de_auditoria(texto):", "CRITERIOS_TIPOS = dict(", funcao)
t = sub(t, 'REVISAO = "R3.4 (19/10/2026)"', 'REVISAO = "R3.5 (19/10/2026)"')
t = sub(t, "vincula a Bancada Um ao um.py selado.  REVISAO R3.4 (19/10/2026).", "vincula a Bancada Um ao um.py selado.  REVISAO R3.5 (19/10/2026).")
paragrafo = (
    "R3.5 (19/10/2026): um conserto pedido pela revisao independente de 19/10 (EXAME_DELTA_E_R3_4.md, B-M), antes do B(n) da v394: o filtro dos MODULOS DE AUDITORIA da R3.4 era lista de PROIBICAO e deixava passar\n"
    "`Lean.addDecl`, `Lean.modifyEnv` e `Lean.Meta.evalExpr` qualificados, `open IO.FS in` + `writeFile` e `open IO in` + `Process.output`. Agora e lista de PERMISSAO ESTRITA (auditar_fonte_de_auditoria):\n"
    "comandos de topo = (so) `import` de Lean/TGLExt/TGL, `open` de Lean, #print axioms e run_cmd; no corpo do run_cmd, um vocabulario FECHADO (palavras, locais, funcoes, metodos, nomes) -- o das fontes reais\n"
    "NetworkProofAuditR3/R7/R8 da v394; o que nao esta na lista e recusado, qualificado ou nao. O resto e a R3.4, byte a byte: os contratos (CADEIA_DE_SELOS_R3_4, SALTO_R3_4, KERNEL_RECIBO_R3_4, BATERIA_R3_4),\n"
    "a conferencia do recibo pre_selo e o formato dos recibos nao mudam, e o recibo pre_selo da R3.4 (gerado antes da instalacao da v394) segue valendo (conferido por controle).\n\n")
t = sub(t, "R3.4 (19/10/2026): tres consertos pedidos pela gerencia c1 (F0.6)", paragrafo + "R3.4 (19/10/2026): tres consertos pedidos pela gerencia c1 (F0.6)")
t = sub(t, 'limite="o corpo do run_cmd e codigo executado na compilacao: o script confere comandos de topo e uma lista fechada de palavras; nao prova a inocuidade semantica do corpo"',
        'limite="o corpo do run_cmd e codigo executado na compilacao: o script confere os comandos de topo e um vocabulario FECHADO de permissao no corpo (R3.5); nao prova a inocuidade semantica do corpo"')
tmp = ESB.with_name(ESB.name + ".tmp_r35")
with open(tmp, "xb") as f:
    f.write(t.encode("utf-8"))
assert tmp.stat().st_size > len(raw) - 3000
os.replace(tmp, ESB)
print("ok", hashlib.sha256(ESB.read_bytes()).hexdigest()[:16], len(raw), "->", ESB.stat().st_size)
