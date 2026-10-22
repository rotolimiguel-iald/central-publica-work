"""Detalhes do core v391: os 11 lancamentos do livro (v383), z por leitor da Fase 9 (v388), escada do neutrino m2, e as chaves do core que casam com temas fora do regex anterior. So leitura."""
import json, re
top = json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json", encoding="utf-8")); core = top["core"]
print("=== LIVRO DE COBRANCAS v383: lancamentos ===")
for e in core["the_ledger_of_charges_v383"]["ledger"]:
    print(f"- {e.get('id')} | lado={e.get('side')} | registro={e.get('register')} | lei={str(e.get('law'))[:110]} | core_key={e.get('core_key')} | outcome={e.get('outcome')} | how={e.get('how')} | number_read={e.get('number_read')} | in_rule={e.get('in_rule')} | numbers={json.dumps(e.get('numbers_read'), ensure_ascii=False)[:160]}")
print("\n=== FASE 9 abertura v388: z por leitor ===")
n = core["hubble_ratio_opening_v388"]["numbers"]
print(json.dumps({k: n[k] for k in n if k in ("H0_bg","H0_local_previsto","media_GLS_locais","sigma_GLS_locais","beta_hat","sigma_beta","z_delta","z_disc","lnB","z_por_leitor","leitores","readers")}, ensure_ascii=False, indent=0)[:3000])
print("\n=== NEUTRINO m2: escada datada e regra ===")
v = core["neutrino_m2"]["values"]
print(json.dumps({k: v[k] for k in v if k not in ("beta",)}, ensure_ascii=False)[:2500])
print("\n=== N_eff: escada ===")
print(json.dumps(core["neff_channel"]["values"].get("escada_projetada"), ensure_ascii=False)[:1200])
print("\n=== chaves do core por tema (fora do regex anterior) ===")
pat = re.compile(r"shapiro|nmc|lpi|cassini|siren|sirene|gw_|three_clock|radical|bbn|planck|desi|pantheon|kappa|shear|lens|redshift|graviton|mass|quantum|pillar|alpha_free|evento|event2|mcmc", re.I)
print([k for k in core if pat.search(k)])
for k in ("neutrino_shapiro", "neutrino_shapiro_protocol", "three_clock_radical", "three_clocks", "alpha_free", "quantum_pillar_v384"):
    if k in core:
        vv = core[k]; print(f"\n#### {k}: verdict={vv.get('verdict') if isinstance(vv, dict) else vv}")
        if isinstance(vv, dict):
            for sk in ("theorem","values","statuses","frozen"):
                if sk in vv: print(f"  - {sk}: {json.dumps(vv[sk], ensure_ascii=False)[:700]}")
