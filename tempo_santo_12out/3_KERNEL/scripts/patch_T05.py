import sys
p = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\sandbox\TheTimeHasNoRank.lean"
s = open(p, encoding="utf-8").read()
def R(a, b):
    global s
    c = s.count(a)
    if c != 1:
        sys.exit(f"PADRAO nao unico ({c}): {a[:90]!r}")
    s = s.replace(a, b)
R("""/-- Os dois lados de T4.b (ii) VALEM para o posto diagonal (a órbita é constante). -/""",
"""/-- CE-T3b(i): com pesos IGUAIS, ψ₊ é FIXO por todo `σ_t` e NÃO é diagonal — o «se e só se» do centralizador
    (`fixed_sector_is_the_centralizer`) exige a injetividade dos pesos. -/
theorem centralizer_iff_needs_injective_weights :
    (∀ t : ℝ, sigma (rhoD ![(1 : ℝ), 1]) t psiPlus = psiPlus) ∧ psiPlus ≠ diagExpect psiPlus :=
  ⟨fun t => sigma_fixed_of_commute _ _ (by rw [rhoD_equal_weights]; exact Commute.one_left _) t,
    psiPlus_not_diagonal⟩

/-- Os dois lados de T4.b (ii) VALEM para o posto diagonal (a órbita é constante). -/""")
R("""#print axioms TGLExt.TheTimeHasNoRank.dephasing_iff_needs_positive_rates
""", """#print axioms TGLExt.TheTimeHasNoRank.dephasing_iff_needs_positive_rates
#print axioms TGLExt.TheTimeHasNoRank.centralizer_iff_needs_injective_weights
""")
open(p, "w", encoding="utf-8", newline="\n").write(s)
a = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\sandbox\AuditTheTimeHasNoRank.lean"
t = open(a, encoding="utf-8").read()
t = t.rstrip("\n") + "\n#check @TGLExt.TheTimeHasNoRank.centralizer_iff_needs_injective_weights\n"
open(a, "w", encoding="utf-8", newline="\n").write(t)
print("ok", len(s.encode("utf-8")))
