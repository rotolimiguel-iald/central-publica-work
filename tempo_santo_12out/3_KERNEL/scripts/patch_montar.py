import sys
p = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\scripts\montar_resultado.py"
s = open(p, encoding="utf-8").read()
def R(a, b):
    global s
    c = s.count(a)
    if c != 1:
        sys.exit(f"PADRAO nao unico ({c}): {a[:90]!r}")
    s = s.replace(a, b)
R('''    "volume_kept_yet_lands": "s > 0 genérico (sem instância numérica; hipótese 0 < s claramente habitada, e.g. s = 1)",
    "global_attractor_needs_volume_loss": "hipótese ∀v, Lᵏv → 0 habitada por L = 0 com m > 0 (não instanciada em Lean; ver nota)",''',
  '''    "volume_kept_yet_lands": "s = 1 (example V-GERAL-1, T4)",
    "global_attractor_needs_volume_loss": "L = 0 em Fin 1: ∀v, 0ᵏv → 0 provado em Lean (example V-GERAL-1, T4)",''')
R('''    "the_record_does_not_scale": "hipóteses genéricas; x diagonal com xᵢᵢ ≠ 0 e s ≠ 0 (p.ex. ψ₊, s = 1) — não instanciada em Lean",''',
  '''    "the_record_does_not_scale": "ψ₊, g = gRate 1, i₀ = 0, s = 1 (example V-GERAL-1, T3–T8)",
    "unitary_keeps_spectrum_and_purity (U unidade)": "U = 1 (example V-GERAL-1, T4)",
    "unitary_conj_isometry": "U = 1, norma de Frobenius (example V-GERAL-1)",
    "dephase_factor_norm_le_one": "g = gRate 1, t = 1 (example V-GERAL-1, T4)",
    "schurDiag_is_the_modular_flow": "d = (2/3, 1/3) (example V-GERAL-1, T4)",
    "re-exportações (T3.b, T4.d, T5.a, T6.b, C-T6-b, T10.a, T10.c, T10.e, T11.a, C-T1-c)": "instanciadas com argumentos concretos nos examples V-GERAL-1 (Fin 2, gRate 1, ψ₊, postDiag, κ = 1, P = 2π, V = ℂ com P = 0, H = ℂ para o par de Weyl)",
    "purity_of_hermitian / purityR_modular / no_coherence_no_loss / control_inverse_on_diagonal": "ψ₊ (hermitiana), d = (2/3, 1/3), gRate 1 (examples V-GERAL-1)",
    "no_finite_instant_is_the_post / flow_of_one_is_idempotent / face_clock_has_no_period / frozen_clock_not_faithful": "postDiag; A = M₂(ℂ); r = P = 1; P = 1 (examples V-GERAL-1)",
    "NAO HABITADAS AQUI": "nontracial_state_rejects_the_identity_flow (exige testemunha AQFT W do kernel) e light_flow_group / light_modular_orbit_converges_iff_post (exigem FockCertificate): ditas na pedra",''')
R('''    ("V-GERAL-1", "cada hipótese de teorema da pedra é habitada por uma sonda ou instância concreta (lista em hipoteses_habitadas)"),''',
  '''    ("V-GERAL-1", "as sondas V-* e mais 4 `example` de habitação em Lean (seção «Sondas de habitação») instanciam todos os teoremas da pedra com argumentos concretos, exceto 3 ditos (W AQFT; FockCertificate) — lista em hipoteses_habitadas"),''')
R('''    "T05": "FINAL: + centralizer_iff_needs_injective_weights; EXIT 0, 0 avisos, 127 linhas no trio; auditoria independente 137 constantes",''',
  '''    "T05": "+ centralizer_iff_needs_injective_weights; EXIT 0, 0 avisos, 127 linhas no trio; auditoria independente 137 constantes",
    "T06": "FINAL: + sondas de habitação V-GERAL-1 (4 `example`); toolchain recopiado só para esta compilação e apagado de novo; EXIT 0, 0 avisos, 0 erros, 127 linhas no trio; auditoria 137 constantes, saída idêntica à de T05",''')
R('''          "AUDIT_recibo.json", "T04_AUDIT_FINAL_recibo.json", "FINAL_recibo.json", "AUDIT_FINAL_recibo.json"]:''',
  '''          "AUDIT_recibo.json", "T04_AUDIT_FINAL_recibo.json", "T05_FINAL_recibo.json", "T05_AUDIT_FINAL_recibo.json",
          "FINAL_recibo.json", "AUDIT_FINAL_recibo.json"]:''')
R('''        {"id": "AF-10", "estatuto": "[REAL — medido]",''',
  '''        {"id": "AF-11", "estatuto": "[REAL — dito]",
         "texto": "V-GERAL-1 sem instância concreta em Lean para 3 declarações: nontracial_state_rejects_the_identity_flow (precisa de uma testemunha AQFT W do kernel) e light_flow_group / light_modular_orbit_converges_iff_post (precisam de um FockCertificate). As hipóteses são estruturas de dados do kernel do Nós; não se construiu habitante aqui."},
        {"id": "AF-10", "estatuto": "[REAL — medido]",''')
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
