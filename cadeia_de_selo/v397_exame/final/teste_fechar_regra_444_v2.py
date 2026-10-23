# -*- coding: utf-8 -*-
"""teste_fechar_regra_444_v2.py -- exame final v397 (c1, 23/10/2026), item 7 sobre o candidato NOVO: no sandbox do fechar montado pelo harness do preparador sobre a MINHA
copia do pacote, o fechar_v397.py RECUSA (rc 2, sem handoff) quando a REGRA DO 4,44 falha -- (a) o item do 4,44 sem a linha dos 5 sigma; (b) sem o p calibrado; (c) a frase do
operador parafraseada -- e volta a FECHAR (rc 0) com o arquivo restaurado. Mutacoes POR LINHA, so' na copia runtime_quadro_v397.py do sandbox (a que o fechar importa).
uso: python -I -B -X utf8 teste_fechar_regra_444_v2.py <SB> <sufixo>"""
import hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
SB, SUF = sys.argv[1], sys.argv[2]
PKS = os.path.join(SB, "work", "cadeia_de_selo", "v397"); POS = os.path.join(PKS, "pos_rito")
RQ = os.path.join(PKS, "runtime_quadro_v397.py"); ORIG = open(RQ, "rb").read(); src = ORIG.decode("utf-8")
HANDOFFS = [os.path.join(SB, "memory", "handoff-v397-custodia.md"), os.path.join(SB, "nos", "HANDOFF_v397_CUSTODIA.md")]
def roda(nome):
    for h in HANDOFFS:
        if os.path.exists(h):
            os.remove(h)
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(POS, "fechar_v397.py")], cwd=POS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    open(os.path.join(H, "fechar_%s_%s_out.txt" % (SUF, nome)), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    return {"rc": p.returncode, "recusou": p.returncode == 2 and "FECHAR RECUSADO" in p.stdout, "handoff_escrito": any(os.path.exists(h) for h in HANDOFFS), "msg": [l[:600] for l in p.stdout.splitlines() if "RECUSADO" in l or "FECHADO" in l][:2]}
L = src.split("\n"); iN = [i for i, l in enumerate(L) if "> - **O número:** z_disc = %s (calibrado; p unilateral %s): " in l]
assert len(iN) == 1, "a linha do 4,44 no quadro md nao e' unica"
iN = iN[0]; lin = L[iN]
def mut_a(l):   # tira a linha dos 5 sigma (e o '(%s < 5)' que ela carrega) do item do 4,44
    m = re.sub(r", mas a discriminação a 5σ.*?\[REAL\]\.", ". [REAL].", l, count=1); return m.replace("% (zd_, pd_, zd_)", "% (zd_, pd_)")
def mut_b(l):   # tira o p calibrado do item do 4,44
    return l.replace("(calibrado; p unilateral %s): ", "(calibrado): ", 1).replace("% (zd_, pd_, zd_)", "% (zd_, zd_)")
MUT = {"a_item_do_4_44_sem_a_linha_dos_5_sigma": ("linha", mut_a), "b_item_do_4_44_sem_o_p_calibrado": ("linha", mut_b),
       "c_frase_do_operador_parafraseada": ("troca", ('_V397_FRASE_444 = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"', '_V397_FRASE_444 = "o 5σ é o cala a boca; 4,44 é um silêncio forçado pela lógica"'))}
R = {"sandbox": SB, "runtime_quadro_sha16_original": hashlib.sha256(ORIG).hexdigest()[:16], "casos": {}}
for nome, (kind, f) in MUT.items():
    if kind == "linha":
        nl = f(lin); ok = nl != lin; novo = "\n".join(L[:iN] + [nl] + L[iN + 1:])
    else:
        ok = src.count(f[0]) == 1; novo = src.replace(f[0], f[1], 1)
    R["casos"][nome] = {"mutacao_aplicada": ok}
    if not ok:
        continue
    open(RQ, "wb").write(novo.encode("utf-8"))
    try:
        R["casos"][nome].update(roda(nome))
    finally:
        open(RQ, "wb").write(ORIG)
R["casos"]["d_restaurado_fecha_de_novo"] = roda("restaurado")
R["runtime_quadro_restaurado"] = open(RQ, "rb").read() == ORIG
R["prova"] = all(v.get("mutacao_aplicada") and v.get("recusou") and not v.get("handoff_escrito") for k, v in R["casos"].items() if k.startswith(("a_", "b_", "c_"))) and R["casos"]["d_restaurado_fecha_de_novo"]["rc"] == 0 and R["casos"]["d_restaurado_fecha_de_novo"]["handoff_escrito"]
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open(os.path.join(H, "TESTE_FECHAR_REGRA_444_%s.json" % SUF), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
