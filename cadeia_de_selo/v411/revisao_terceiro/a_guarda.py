src = open("a_a3.py", encoding="utf-8").read().split("rep = {}")[0]
exec(compile(src, "a_a3_head", "exec"))
def g(t):
    for _ in range(40):
        try:
            return ns["_v411_guarda_frases"](t)
        except NameError as e:
            import re as _r
            m = _r.search(r"name '([A-Za-z_0-9]+)' is not defined", str(e))
            f.carregar([m.group(1)], ns)
    raise RuntimeError
P = {
 "confirmacao_simples": "a TGL foi confirmada na natureza",
 "confirmacao_apos_no": "No teste H0DN a TGL foi confirmada.",
 "confirmacao_apos_no2": "O resultado no H0DN confirma beta.",
 "confirmacao_apos_sem": "Sem objeção, o resultado confirma beta.",
 "confirmed_after_no": "In the H0DN test no doubt remains: the theory was confirmed.",
 "confirmed_en": "the theory is confirmed by nature",
 "confirmado_com_nao_antes_longe": "O teste não é cego e a TGL, por tudo isso, está confirmada.",
 "creditacao_mas_confirmado": "a creditação é do observador; beta está confirmado",
 "poder_certificado": "o teste tem poder certificado",
 "power_certified": "the test has certified power",
 "teste_cego": "foi um teste cego",
 "blind": "it was a blind test",
 "independente": "é evidência independente das fases 4 e 5",
 "descoberta": "a descoberta de beta na natureza",
 "discovery": "this discovery of beta",
 "montagem": "o vetor fora do suporte é erro de montagem",
 "beta_lit": "beta = 0,012031",
 "beta_lit_ponto": "beta = 0.012031",
 "pos_dicao_demerito": "é apenas pós-dição, não conta",
 "tgl_nao_provou": "a TGL não provou nada",
 "provado_sem_4": "beta provado na natureza a 6σ no H0DN",
 "ok_4": "O primário do H0DN, sob o modelo de erros publicado, lê 6,11 contra o nulo, provado na natureza a 6σ, validade, não creditação; ao lado, as Cefeidas livres leem 4,38; retrodição sem ajuste, teste não cego.",
}
for k, t in P.items():
    r = g(t)
    print("%-32s -> %s" % (k, [x[0] for x in r] or "PASSA"))
