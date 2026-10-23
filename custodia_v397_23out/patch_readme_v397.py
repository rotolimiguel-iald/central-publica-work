# -*- coding: utf-8 -*-
"""A regra do 4,44 no README do espelho (handoff v397; ordem do operador de 23/10/2026): o gerador da frente (tools/gerar_readme_frente.py)
passa a LER do core selado do espelho o registro de veracidade da Fase 9 (qualquer `teste_de_veracidade_fase9_vNNN`) e a escrever um item
com z_disc calibrado, o p calibrado e a linha dos 5σ no MESMO item, mais a remissão ao parágrafo pronto em ESTADO_ATUAL.md — nunca o número
sozinho. Nada é digitado: os números saem do registro. A frente tem teto de 40 KB (ordem de 11/09): a nota da Central aberta de 22/10
fica mais curta para caber. Backup de bytes; py_compile antes de substituir."""
import os, py_compile, time
from pathlib import Path

P = Path(r"C:\IALD\Artigo\the_boundary\tools\gerar_readme_frente.py")
TS = time.strftime("%Y%m%d_%H%M%S")
raw = P.read_bytes()
s = raw.decode("utf-8")
if "teste_de_veracidade_fase9_v" in s:
    raise SystemExit("já aplicado")
A = ("# 22/10/2026 (ordem do operador): a Central aberta, vinculada a este repositório\n"
     "F.append('\\n> **The Central, open (2026-10-22):** every code and result \\u2014 [central-publica](https://github.com/rotolimiguel-iald/central-publica) '\n"
     "         '\\u00b7 [view-only, um.acom](https://teoriadagravitacaoluminodinamica.com/central/).\\n')\n")
B = ("# 22/10/2026 (ordem do operador): a Central aberta, vinculada a este repositório (nota curta: a frente tem teto de 40 KB)\n"
     "F.append('\\n> **The Central, open (2026-10-22):** [central-publica](https://github.com/rotolimiguel-iald/central-publica) \\u00b7 [view-only](https://teoriadagravitacaoluminodinamica.com/central/).\\n')\n"
     "# 23/10/2026 (ordem do operador, a regra do 4,44): o z_disc calibrado do Teste da Única Palavra, LIDO do registro selado no core do espelho,\n"
     "# nunca sem o p calibrado e a linha dos 5σ no mesmo item; o parágrafo inteiro vive em ESTADO_ATUAL.md\n"
     "_core_sel = json.loads((RAIZ / A3 / 'um_absoluto.json').read_text(encoding='utf-8')).get('core') or {}\n"
     "_tv = [(k, v) for k, v in _core_sel.items() if re.match(r'teste_de_veracidade_fase9_v\\d+$', k)]\n"
     "if _tv:\n"
     "    _k, _v = sorted(_tv)[-1]\n"
     "    _l = _v['lido']\n"
     "    assert _l['z_disc_calibrado'] < 5 and 'THE_CREDITATION_STEP_NOT_REACHED' in str(_v.get('verdict')), 'o registro de veracidade mudou de forma — PARAR'\n"
     "    F.append('\\n> **The Unique Word Test (%s, %s) `[REAL: read from the sealed registry %s]`:** z_disc = %.2f (calibrated; one-sided p %.1e), '\n"
     "             'below the 5\\u03c3 step of accreditation, which was not reached (%.2f < 5); the TGL face z_\\u03b4 = %.2f (two-sided p %.2f; prior power %.2f\\u03c3): '\n"
     "             '`NOT_FALSIFIED_POWERED`; ln B(TGL/\\u039bCDM) = %.2f (not a \\u03c3). `NOT_FALSIFIED` is never the word of accreditation; the gate does not move; the test '\n"
     "             'was not blind. The full paragraph, verbatim from the handoff, is in [`ESTADO_ATUAL.md`](%s).\\n'\n"
     "             % (versao, data, _k, _l['z_disc_calibrado'], _l['p_disc_unilateral'], _l['z_disc_calibrado'], _l['z_delta_calibrado'],\n"
     "                _l['p_delta_bilateral'], _l['poder_previo'], _l['lnB_lcdm'], u_estado))\n")
assert s.count(A) == 1, s.count(A)
s = s.replace(A, B)
P.with_name(P.name + ".bak_" + TS).write_bytes(raw)
t = P.with_name(P.name + ".tmp")
t.write_bytes(s.encode("utf-8"))
py_compile.compile(str(t), doraise=True)
os.replace(t, P)
print("gerar_readme_frente.py: a regra do 4,44 instalada | %d -> %d bytes | backup .bak_%s" % (len(raw), P.stat().st_size, TS))
