#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da FUNCAO DE VEREDITO em dados SINTETICOS (nenhum dado da pergunta): cada ramo da precedencia,
as bordas da banda, da inclinacao, da janela (>= 7 pontos) e do minimo de sementes.
Roda antes do pre-registro; falha fechada (AssertionError) se qualquer caso nao der o esperado.
"""
import os
import sys
import math

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import veredito as V  # noqa: E402

LN2 = math.log(2.0)
GAM = [10 ** (-4 + k / 6.0) for k in range(25)]
XS = [math.log(d / nc) for (d, nc) in V.CONFIGS]
XM = sum(XS) / len(XS)
IDX = {c: i for i, c in enumerate(V.CONFIGS)}


def make_rows(fn, conv=None):
    rows = []
    for (d, nc) in V.CONFIGS:
        for seed in V.SEEDS:
            for gi in range(25):
                ok = True if conv is None else conv(d, nc, seed, gi)
                rows.append(dict(set="t", d=d, nc=nc, seed=seed, gi=gi, gamma=GAM[gi],
                                 O=fn(d, nc, seed, gi), conv=ok, reason=""))
    return rows


def n1_rows(val=0.13, val_d8=None):
    out = []
    for d in sorted({c[0] for c in V.CONFIGS}):
        v = val_d8 if (d == 8 and val_d8 is not None) else val
        for k in range(V.N1_STATES):
            out.append(dict(d=d, k=k, O=v))
    return out


def n3_ok(err=0.0):
    casos = []
    for d in sorted({c[0] for c in V.CONFIGS}):
        for f in (2, 4):
            if d % f == 0:
                alvo = LN2 if f == 2 else 2 * LN2
                casos.append(dict(d=d, posto=d // f, frac=f, O=alvo + err, esperado=alvo, erro_abs=err))
    return dict(casos=casos)


def flat(gi_set, off=0.0):
    return lambda d, nc, seed, gi: LN2 + off if gi in gi_set else LN2 + 0.2


def check(nome, res, esperado, extra=None):
    ok = res["veredito"] == esperado and (extra is None or extra(res))
    print("%-62s -> %-32s %s" % (nome, res["veredito"], "ok" if ok else "FALHOU (esperado %s)" % esperado))
    assert ok, nome


def main():
    plano = lambda d, nc, s, gi: LN2 + 0.003 * ((s - 44) / 2.0)          # tudo em ln 2, ruido pequeno
    baixo = lambda d, nc, s, gi: 0.13                                    # N2: estado quase misto

    # 1. ramo 6
    r = V.decide(make_rows(plano), make_rows(baixo), n1_rows(), n3_ok())
    check("T1 plato em ln 2, N2 baixo, N1 e N3 como previsto", r, "FLOOR_ONE_OCTAVE_NOT_FALSIFIED",
          lambda r: r["P"] and not r["P_N2"] and r["janela"]["n_pontos"] == 25)

    # 2. ramo 5 (N2 tambem satisfaz P)
    r = V.decide(make_rows(plano), make_rows(plano), n1_rows(), n3_ok())
    check("T2 N2 tambem satisfaz P", r, "GENERIC_NOT_TGL")

    # 3. ramo 5 (N1 falha)
    r = V.decide(make_rows(plano), make_rows(baixo), n1_rows(0.13, val_d8=0.25), n3_ok())
    check("T3 N1 falha em d=8 (mediana 0,25)", r, "GENERIC_NOT_TGL")

    # 4. ramo 3: sem plato
    r = V.decide(make_rows(lambda d, nc, s, gi: 1.5 - 0.05 * gi), make_rows(baixo), n1_rows(), n3_ok())
    check("T4 O varia com gamma (sem plato)", r, "NO_UNIVERSAL_FLOOR")

    # 5. janela: 7 pontos (1,0 decada) passa; 6 nao; duas janelas separadas nao somam
    r = V.decide(make_rows(flat(set(range(3, 10)))), make_rows(baixo), n1_rows(), n3_ok())
    check("T5a janela de 7 pontos (1,0 decada)", r, "FLOOR_ONE_OCTAVE_NOT_FALSIFIED",
          lambda r: r["janela"]["n_pontos"] == 7)
    r = V.decide(make_rows(flat(set(range(3, 9)))), make_rows(baixo), n1_rows(), n3_ok())
    check("T5b janela de 6 pontos (0,83 decada)", r, "NO_UNIVERSAL_FLOOR")
    r = V.decide(make_rows(flat(set(range(0, 4)) | set(range(5, 9)))), make_rows(baixo), n1_rows(), n3_ok())
    check("T5c duas janelas de 4 pontos separadas por um buraco", r, "NO_UNIVERSAL_FLOOR")

    # 6. inclinacao
    r = V.decide(make_rows(lambda d, nc, s, gi: LN2 + 0.06 * (math.log(d / nc) - XM)), make_rows(baixo),
                 n1_rows(), n3_ok())
    check("T6a inclinacao 0,06 (dentro da banda)", r, "NO_UNIVERSAL_FLOOR",
          lambda r: r["so_banda_maior_corrida"]["n_pontos"] == 25 and r["so_inclinacao_maior_corrida"] is None)
    r = V.decide(make_rows(lambda d, nc, s, gi: LN2 + 0.04 * (math.log(d / nc) - XM)), make_rows(baixo),
                 n1_rows(), n3_ok())
    check("T6b inclinacao 0,04", r, "FLOOR_ONE_OCTAVE_NOT_FALSIFIED")

    # 7. ramo 1
    r = V.decide(make_rows(plano), make_rows(baixo), n1_rows(), n3_ok(1e-6))
    check("T7 N3 com erro 1e-6", r, "MEASURE_BROKEN")
    r = V.decide(make_rows(plano), make_rows(baixo), n1_rows(), n3_ok(5e-13))
    check("T7b N3 com erro 5e-13 (dentro de 1e-12)", r, "FLOOR_ONE_OCTAVE_NOT_FALSIFIED")

    # 8. ramo 2: mais de 10% sem convergir na principal (mesmo com P aparente)
    r = V.decide(make_rows(plano, conv=lambda d, nc, s, gi: not (d == 8 and gi < 20)),
                 make_rows(baixo), n1_rows(), n3_ok())
    # config (8,2) x 5 sementes x 20 gammas = 100 pontos de 1125 (8,9%): abaixo do corte, decide P (falso: celulas vazias)
    check("T8a 8,9% sem convergir (abaixo do corte)", r, "NO_UNIVERSAL_FLOOR",
          lambda r: r["naoconv_main"] < 0.10)
    r = V.decide(make_rows(plano, conv=lambda d, nc, s, gi: not (d in (8, 10) and gi < 14)),
                 make_rows(baixo), n1_rows(), n3_ok())
    # 2 configs x 5 sementes x 14 gammas = 140 pontos (12,4%)
    check("T8b 12,4% sem convergir", r, "INCONCLUSIVE", lambda r: r["naoconv_main"] > 0.10)

    # 9. ramo 4: P verdadeiro, mas N2 nao converge
    r = V.decide(make_rows(plano), make_rows(baixo, conv=lambda d, nc, s, gi: not (d in (8, 10) and gi < 14)),
                 n1_rows(), n3_ok())
    check("T9 P verdadeiro e N2 com 12,4% sem convergir", r, "INCONCLUSIVE")

    # 10. minimo de sementes por celula: 2 convergidas quebram a janela
    base = lambda d, nc, s, gi: LN2 if gi <= 10 else LN2 + 0.2
    quebra = lambda gi0: (lambda d, nc, s, gi: not (d == 8 and nc == 2 and gi == gi0 and s in (42, 43, 44)))
    r = V.decide(make_rows(base, conv=quebra(3)), make_rows(baixo), n1_rows(), n3_ok())
    check("T10a celula com 2 sementes quebra em gi=3: sobra corrida de 7", r, "FLOOR_ONE_OCTAVE_NOT_FALSIFIED",
          lambda r: r["janela"]["inicio_gi"] == 4 and r["janela"]["n_pontos"] == 7)
    r = V.decide(make_rows(base, conv=quebra(4)), make_rows(baixo), n1_rows(), n3_ok())
    check("T10b quebra em gi=4: corridas de 4 e 6", r, "NO_UNIVERSAL_FLOOR")
    # 3 sementes convergidas bastam
    r = V.decide(make_rows(base, conv=lambda d, nc, s, gi: not (d == 8 and nc == 2 and gi == 4 and s in (42, 43))),
                 make_rows(baixo), n1_rows(), n3_ok())
    check("T10c celula com 3 sementes convergidas ainda vale", r, "FLOOR_ONE_OCTAVE_NOT_FALSIFIED")

    # 11. borda da banda: so a config (12,2) desloca (inclinacao quase nula)
    off = lambda x: (lambda d, nc, s, gi: LN2 + (x if (d, nc) == (12, 2) else 0.0))
    r = V.decide(make_rows(off(0.0499)), make_rows(baixo), n1_rows(), n3_ok())
    check("T11a uma config em ln 2 + 0,0499", r, "FLOOR_ONE_OCTAVE_NOT_FALSIFIED")
    r = V.decide(make_rows(off(0.0501)), make_rows(baixo), n1_rows(), n3_ok())
    check("T11b uma config em ln 2 + 0,0501", r, "NO_UNIVERSAL_FLOOR")

    # 12. o veredito e sempre um dos cinco
    assert all(x in V.VEREDITOS for x in ("FLOOR_ONE_OCTAVE_NOT_FALSIFIED", "NO_UNIVERSAL_FLOOR", "GENERIC_NOT_TGL",
                                          "MEASURE_BROKEN", "INCONCLUSIVE"))
    print("\nTODOS OS CASOS SINTETICOS PASSARAM")


if __name__ == "__main__":
    main()
