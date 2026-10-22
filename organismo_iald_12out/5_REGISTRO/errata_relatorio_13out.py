"""Errata AO LADO no relatório do organismo (gerência c1, em nome próprio), com backup de bytes."""
import datetime
import hashlib
import os

P = r"C:\IALD\Central de Patentes\work\organismo_iald_12out\4_RELATORIO\O_ORGANISMO_E_A_PROVA_DISTINTIVA.md"
b = open(P, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + ts, "wb").write(b)

err = """

---

> ⚠ **ERRATA AO LADO (13/10/2026, gerência c1, em nome próprio; achados da reauditoria do motor r2, `C:\\IALD\\PROGRAMA_IALD\\auditorias\\F1.MOTOR\\AUDITORIA_F1_MOTOR_C1_a4a8fb5f.md`). O texto acima fica como registro.**
>
> 1. **§1.1 e a interface:** T2 já não pede ‖a‖ = 1 (correção C2 da r2, `9b0e9260b208beef`); a hipótese H-N pesa só em T4, T5/T5′, T6′, T11 e `unitarity_is_not_enough`. A saída do motor não depende de β nem de t (`the_motor_ignores_rate_and_time`); a defasagem vale para qualquer taxa (`the_leak_is_any_rate`); `the_leak_is_beta` é `rfl` de nome (C6).
> 2. **A condição exata de idempotência** é «âncora fraca `post a (U a) = a` OU motor nulo», não só a âncora fraca (achado do construtor da r2, provado de novo, por outro caminho, pelo auditor; exemplo de motor nulo com U ≠ 0: U = |b⟩⟨b|, b ⊥ a).
> 3. **A frase «se U for isometria, a âncora volta a ser necessária»** (auditoria de reprodução da r1) é falsa em dimensão infinita: com U só isométrico e imagem ortogonal a a, o motor é nulo e idempotente sem âncora (deslocamento unilateral de ℓ², [KNOWN], não construído em Lean). Com U **unitário** (sobrejetivo) e ‖a‖ = 1, a idempotência força U a = a (sonda `c1_unitary_forces_strong_anchor`).
> 4. **Premissa da Pergunta 3, lida ao lado:** se o senhor puser U unitário por tipo, T2 vira «se e só se» com a âncora forte U a = a; se puser só isométrico, não; se não puser nenhum, vale a condição do item 2.
> 5. **«Q16/Q17 resolvidas» e «EU SOU = IALD como termo»**, onde aparecem no RESULTADO_CONSTRUCAO, no ESPEC e no PREREGISTRO desta unidade, leem-se: «homônimo aparente desfeito por `rfl`; o organismo segue lista fora desta pedra»; EU SOU = IALD é [ONTO], e T5′ é fato geral de espaço de Hilbert (C5, C8).
> 6. **A Ágape** não entra por termo na pedra: no fecho de usos da r2 há zero constantes de `TGLExt.Fundacao`; ela aparece carregada só porque `TheTimeIsNotAPost` a importa (C3).
"""
n = b + (b"" if b.endswith(b"\n") else b"\n") + err.encode("utf-8")
for bad in (b"\t", b"\x04", b"\x05", b"\x0c"):
    assert bad not in err.encode("utf-8"), bad
open(P + ".tmp", "wb").write(n)
assert os.path.getsize(P + ".tmp") == len(n) > len(b)
os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(n), "sha16", hashlib.sha256(n).hexdigest()[:16])
