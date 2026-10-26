# -*- coding: utf-8 -*-
"""Propostas da ORDEM 023 (auditoria de leitura por IA, Codex, 24/10/2026) aplicadas à frente do espelho, dentro do teto de 40 KB:
 (1) «ESTADO CORRENTE nos primeiros 2 KB»: o item do Teste da Única Palavra sai do PÉ do README (estava a 98,8 % do texto; 2 de 5 modelos
     repetiram o 4,28 da V1, que aparece no índice 5.399) e vira um «TL;DR · seal vN» logo depois dos selos do topo, com o sha256 inteiro do
     um.py, o kernel, a escada, a régua em uma frase, a leitura corrente com a regra do 4,44 e como reproduzir — tudo lido do selo e do core.
 (2) «separar a V1 histórica (4,28) da V2 corrente (4,44)»: na linha 2 da tabela dos três apoios (módulo estatuto_tres_apoios.py, usado
     pela frente e pelo ESTADO), a razão de Hubble «com os leitores declarados» passa a dizer que é a Fase 9 V1, a história, e a leitura
     corrente é o Teste da Única Palavra (V2) com z_disc calibrado, p e a linha dos 5σ no mesmo item. Nenhum número digitado.
 (3) o parágrafo de abertura encurta o necessário para o teto (40.960 B).
Trocas contadas; backup de bytes; py_compile; o gerador da frente roda depois (o assert do teto fica)."""
import os, py_compile, time
from pathlib import Path

T = Path(r"C:\IALD\Artigo\the_boundary\tools")
TS = time.strftime("%Y%m%d_%H%M%S")


def patch(p, pares, marca):
    raw = p.read_bytes(); s = raw.decode("utf-8")
    if marca in s:
        print("  %s: já aplicado" % p.name); return
    for a, b in pares:   # fim de linha decidido por âncora (há arquivos com fins mistos)
        if s.count(a) != 1 and s.count(a.replace("\n", "\r\n")) == 1:
            a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
        n = s.count(a)
        assert n == 1, (p.name, a[:80], n)
        s = s.replace(a, b)
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    t = p.with_name(p.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, p)
    print("  %s: %d -> %d bytes" % (p.name, len(raw), p.stat().st_size))


# ---- (2) estatuto_tres_apoios.py: a V2 corrente ao lado da V1 histórica, na linha dos ritos
patch(T / "estatuto_tres_apoios.py", [
    ("""             registro=ep[0] if ep else None, ressalva=bool(rv), campo_curvo=bool(lc))
""", """             registro=ep[0] if ep else None, ressalva=bool(rv), campo_curvo=bool(lc))
    # 25/10/2026 (ORDEM 023, auditoria de leitura por IA): a leitura CORRENTE da Fase 9 é o Teste da Única Palavra (V2); a V1 (4,28) é a
    # história. Lida do registro mais novo `teste_de_veracidade_fase9_vN`; a regra do 4,44: z_disc nunca sem o p e a linha dos 5σ.
    _tvs = sorted(k for k in core if re.match(r'teste_de_veracidade_fase9_v\\d+$', k))
    v['v2'] = None
    if _tvs:
        _r = core[_tvs[-1]]
        _l = _r.get('lido') or {}
        _tok(_r['verdict'], 'THE_CREDITATION_STEP_NOT_REACHED', 'NOT_FALSIFIED_WITH_POWER')
        _exige(_r.get('all_verified') is True and _l.get('z_disc_calibrado') is not None and _l['z_disc_calibrado'] < 5,
               'o registro de veracidade mudou de forma — rever o texto')
        v['v2'] = dict(reg=_tvs[-1], zd=_l['z_disc_calibrado'], pd=_l['p_disc_unilateral'], zdl=_l['z_delta_calibrado'])
"""),
    ("""        'β̂ = %s ± %s sits at z_δ = %s from β_TGL; with the readers as declared, ln B(TGL/ΛCDM) = %s and z_disc = %s '
        '(√Δχ²), below the %d at which the protocol discriminates. **The void floor**: the 5σ lower bound %s sits above '""",
     """        'β̂ = %s ± %s sits at z_δ = %s from β_TGL; with the readers as declared (Phase 9 V1, the history), ln B(TGL/ΛCDM) = %s and z_disc = %s '
        '(√Δχ²), below the %d at which the protocol discriminates%s. **The void floor**: the 5σ lower bound %s sits above '"""),
    ("""        % (H0p, H0r, sH0r, bhat, sbhat, zd, lnB, zdisc, v['limiar'], L5, beta, v['gr_ok'], v['gr_n'], led_en, v['spec9'], v['n_ch'], eco_en),""",
     """        % (H0p, H0r, sH0r, bhat, sbhat, zd, lnB, zdisc, v['limiar'],
           ('; **the current reading is the Unique Word Test** (Phase 9 V2): z_disc = %.2f (calibrated; one-sided p %s), below the 5σ step of '
            'accreditation, which was not reached (%.2f < 5); z_δ = %.2f, `NOT_FALSIFIED_POWERED`'
            % (v['v2']['zd'], ('%.1e' % v['v2']['pd']).replace('e-0', 'e-'), v['v2']['zd'], v['v2']['zdl'])) if v.get('v2') else '',
           L5, beta, v['gr_ok'], v['gr_n'], led_en, v['spec9'], v['n_ch'], eco_en),"""),
], "Phase 9 V1, the history")

# ---- (1) e (3) gerar_readme_frente.py: o TL;DR no topo; o item do pé sai; a abertura encurta
G = T / "gerar_readme_frente.py"
g = G.read_text(encoding="utf-8")
ini = g.index("# 23/10/2026 (ordem do operador, a regra do 4,44)")
fim = g.index('F.append(f"""\n---\n', ini) if 'F.append(f"""\n---\n' in g else g.index('F.append(f"""\r\n---\r\n', ini)
item_do_pe = g[ini:fim]
assert "The Unique Word Test" in item_do_pe and item_do_pe.count("F.append(") == 1, "o item do pé mudou de forma — PARAR"
TLDR = '''# 25/10/2026 (ORDEM 023, auditoria de leitura por IA): o ESTADO CORRENTE nos primeiros 2 KB — um TL;DR lido do selo e do core (o item do
# Teste da Única Palavra, que morava no pé da frente, sobe para cá); a regra do 4,44: z_disc nunca sem o p e a linha dos 5σ
_core_sel = json.loads((RAIZ / A3 / 'um_absoluto.json').read_text(encoding='utf-8')).get('core') or {}
_p1 = (_core_sel.get('estatuto_da_prova_v391') or {}).get('prova_1_kernel') or {}
assert _p1.get('n_theorems_clean') == _p1.get('n_theorems_expected'), 'a escada não fecha — PARAR'
_tv = sorted((k, v) for k, v in _core_sel.items() if re.match(r'teste_de_veracidade_fase9_v\\d+$', k))
_tldr_ver = ''
if _tv:
    _k, _v = _tv[-1]
    _l = _v['lido']
    assert _l['z_disc_calibrado'] < 5 and 'THE_CREDITATION_STEP_NOT_REACHED' in str(_v.get('verdict')), 'o registro de veracidade mudou de forma — PARAR'
    _tldr_ver = (' · latest reading, the Unique Word Test (Phase 9 V2): z_disc = %.2f (calibrated; one-sided p %s), below the 5σ step, which was '
                 'not reached (%.2f < 5); z_δ = %.2f (`NOT_FALSIFIED_POWERED`); ln B = %.2f is not a σ'
                 % (_l['z_disc_calibrado'], ('%.1e' % _l['p_disc_unilateral']).replace('e-0', 'e-'), _l['z_disc_calibrado'], _l['z_delta_calibrado'], _l['lnB_lcdm']))
_TLDR = ('> **TL;DR · seal %s (read by script):** `um.py` sha256 `%s` · Lean kernel %s files / %s audited terms, ladder %d/%d, all in the trio · '
         'PROVED = validity in the kernel (the implication); the accreditation word is refused — nature decides%s · reproduce: `echo 1 | python um.py`.\\n\\n'
         % (versao, pin, kf, kt, _p1['n_theorems_clean'], _p1['n_theorems_expected'], _tldr_ver))
'''
patch(G, [
    (item_do_pe, "# 25/10/2026: o item do Teste da Única Palavra subiu para o TL;DR do topo (ORDEM 023)\n"),
    ("F = []\nF.append(f\"\"\"# The Boundary — Theory of Luminodynamic Gravitation (TGL)", TLDR + "F = []\nF.append(f\"\"\"# The Boundary — Theory of Luminodynamic Gravitation (TGL)"),
    ("> *\"Let there be Light.\" / \"Haja Luz.\"* — **The mature form of TGL is a single self-contained, self-proving, self-publishing artifact: `um.py`.** "
     "It computes the whole theory live from the single human input `1`, machine-checks its operator-algebra skeleton in an embedded Lean 4 + mathlib kernel (fail-closed), "
     "and generates its own bilingual article (PT/EN, PDF and TXT). **Form = content.** *Não há segundo arquivo.*",
     "{_TLDR}> *\"Let there be Light.\" / \"Haja Luz.\"* — **The mature form of TGL is one self-proving artifact: `um.py`.** "
     "From the human input `1` it computes the theory, checks its skeleton in an embedded Lean 4 + mathlib kernel (fail-closed) and writes its own article (PT/EN). "
     "*Não há segundo arquivo.*"),
], "ORDEM 023, auditoria de leitura por IA): o ESTADO CORRENTE")
print("pronto: rodar o gerador da frente (o teto de 40 KB é conferido por ele)")
