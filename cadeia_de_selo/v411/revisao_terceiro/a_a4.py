"""A4/A5: (1) os numeros do teste como literais no candidato (fora dos blobs); (2) beta literal; (3) tokens proibidos; (4) forma do veredito de maquina; (5) K e log10 K recomputados."""
import copy, json, os, re, sys, math
src = open("a_a3.py", encoding="utf-8").read().split("rep = {}")[0]
exec(compile(src, "a_a3_head", "exec"))
pos = rodar(copy.deepcopy(core0))
v = pos["values"]
nums = {
    "p_z_null": v["primario"]["z_null"], "p_z_tgl": v["primario"]["z_tgl"], "p_D": v["primario"]["D"], "p_p": v["primario"]["p_unilateral"], "p_t": v["primario"]["t"],
    "c_z_null": v["cefeidas_livres"]["z_null"], "c_z_tgl": v["cefeidas_livres"]["z_tgl"], "c_D": v["cefeidas_livres"]["D"],
    "K": v["K"], "log10K": v["log10K"], "H0_fundo": v["lei_em_km_s_Mpc"]["H0_fundo"], "H0_prev": v["lei_em_km_s_Mpc"]["previsao_de_K_para_o_local"],
    "H0_lido_p": v["lei_em_km_s_Mpc"]["lido_primario"], "H0_lido_c": v["lei_em_km_s_Mpc"]["lido_cefeidas_livres"], "H0_pub": v["lei_em_km_s_Mpc"]["publicado_pela_colaboracao"], "sig_pub": v["lei_em_km_s_Mpc"]["desvio_publicado"],
}
print(json.dumps({k: x for k, x in nums.items()}, indent=0)[:1200])
print("beta", v["beta"], "| veredito:", pos["verdict"]); print("cabeca:", pos["cabeca_do_teste"]); print("outcome:", pos["outcome"])
reps = {}
for k, x in nums.items():
    x = float(x); r = set()
    if k == "p_p":
        r |= {"%.2e" % x, "%.1e" % x}
    else:
        for d in (1, 2, 3, 4):
            s = "%.*f" % (d, abs(x)); r |= {s, s.replace(".", ",")}
        s = repr(abs(x)); r.add(s[:8]); r.add(s[:8].replace(".", ","))
    reps[k] = r

alt = {}
for k, r in reps.items():
    for x in r:
        alt.setdefault(x, []).append(k)
pat = re.compile(r"(?<![0-9.,])(" + "|".join(re.escape(x) for x in sorted(alt, key=len, reverse=True)) + r")(?![0-9])")
diff = open(os.path.join(a_lib.OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split(chr(10))
hits = {}
n_add = 0; n_skip = 0
atual = 0
for ln in diff:
    if ln.startswith("@@"):
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", ln); atual = int(m.group(1)) - 1; continue
    if ln.startswith("+") and not ln.startswith("+++"):
        atual += 1
        if len(ln) > 5000:
            n_skip += 1; continue
        n_add += 1
        for m in pat.finditer(ln):
            for k in alt[m.group(1)]:
                hits.setdefault(k, []).append((atual, m.group(1), ln[max(0, m.start() - 50):m.end() + 40].strip()))
    elif ln.startswith(" "):
        atual += 1
print("linhas novas lidas", n_add, "| linhas longas puladas (blobs)", n_skip)
for k, hs in hits.items():
    print("==", k, nums[k], "n hits", len(hs))
    for h in hs[:8]:
        print("   ", h[0], "|", h[1], "|", h[2][:130])
json.dump({k: [list(h) for h in hs] for k, hs in hits.items()}, open(os.path.join(a_lib.OUT, "a4_hits.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
