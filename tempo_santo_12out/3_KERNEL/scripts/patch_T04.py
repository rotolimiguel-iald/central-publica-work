import sys
p = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\sandbox\TheTimeHasNoRank.lean"
s = open(p, encoding="utf-8").read()
def R(a, b):
    global s
    c = s.count(a)
    if c != 1:
        sys.exit(f"PADRAO nao unico ({c}): {a[:90]!r}")
    s = s.replace(a, b)
R("""/-- Sonda V-T2-b: `A = M₂(ℂ)` com a norma de operador L2, `V = 1`, `H = 0`, `s = 1` — as hipóteses de T2.b
    (álgebra de Banach unital não trivial) são habitadas. -/
set_option maxHeartbeats 4000000 in
theorem probe_bounded_spectral_translation : True := by""", """set_option maxHeartbeats 4000000 in
/-- Sonda V-T2-b: `A = M₂(ℂ)` com a norma de operador L2, `V = 1`, `H = 0`, `s = 1` — as hipóteses de T2.b
    (álgebra de Banach unital não trivial) são habitadas. -/
theorem probe_bounded_spectral_translation : True := by""")
R("""    ((1 : ℂˣ)⁻¹ : ℂ) * 0 * ((1 : ℂˣ) : ℂ) ≠ 0 + algebraMap ℂ ℂ 1 :=
  no_bounded_spectral_translation 1 0 one_ne_zero""", """    (((1 : ℂˣ)⁻¹ : ℂˣ) : ℂ) * 0 * ((1 : ℂˣ) : ℂ) ≠ 0 + algebraMap ℂ ℂ 1 :=
  no_bounded_spectral_translation (A := ℂ) 1 0 one_ne_zero""")
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok", len(s.encode("utf-8")))
