# -*- coding: utf-8 -*-
"""teste_fechar_regra_444.py -- exame final v397 (c1, 23/10/2026), item 7: PROVA, no sandbox do fechar (copia isolada em v397_exame\\sb, montada pelo harness do preparador),
que fechar_v397.py RECUSA (rc 2, sem handoff) quando a REGRA DO 4,44 falha: (a) o item do 4,44 sem a linha dos 5 sigma; (b) o item do 4,44 sem o p calibrado; (c) a frase do
operador parafraseada; e que volta a FECHAR (rc 0) com o arquivo restaurado. A mutacao e' feita SO' na copia runtime_quadro_v397.py do sandbox (a que o fechar importa)."""
import json, os, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
SB = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v397_exame\sb"
PKS = os.path.join(SB, "work", "cadeia_de_selo", "v397"); POS = os.path.join(PKS, "pos_rito")
RQ = os.path.join(PKS, "runtime_quadro_v397.py"); ORIG = open(RQ, "rb").read()
HANDOFFS = [os.path.join(SB, "memory", "handoff-v397-custodia.md"), os.path.join(SB, "nos", "HANDOFF_v397_CUSTODIA.md")]
def roda(nome):
    for h in HANDOFFS:
        if os.path.exists(h):
            os.remove(h)
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(POS, "fechar_v397.py")], cwd=POS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    open(os.path.join(H, "fechar_%s_out.txt" % nome), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    return {"rc": p.returncode, "recusou": p.returncode == 2 and "FECHAR RECUSADO" in p.stdout, "handoff_escrito": any(os.path.exists(h) for h in HANDOFFS), "msg": [l for l in p.stdout.splitlines() if "RECUSADO" in l or "FECHADO" in l][:2]}
MUT = {
 "a_item_do_4_44_sem_a_linha_dos_5_sigma": (", mas a discriminação a 5σ, o degrau da creditação, **não foi alcançada** (%s < 5); `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego (os centros dos leitores são públicos) [REAL].\" % (zd_, pd_, zd_)",
                                            ". [REAL].\" % (zd_, pd_)"),
 "b_item_do_4_44_sem_o_p_calibrado": ("> - **O número:** z_disc = %s (calibrado; p unilateral %s): ", "> - **O número:** z_disc = %s (calibrado; p unilateral n/d): "),
 "c_frase_do_operador_parafraseada": ('_V397_FRASE_444 = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"', '_V397_FRASE_444 = "o 5σ é o cala a boca; 4,44 é um silêncio forçado pela lógica"'),
}
R = {"sandbox": SB, "runtime_quadro_sha16_original": __import__("hashlib").sha256(ORIG).hexdigest()[:16], "casos": {}}
src = ORIG.decode("utf-8")
for nome, (a, b) in MUT.items():
    if nome == "b_item_do_4_44_sem_o_p_calibrado":
        # tira o p do item 1 (a tupla % (zd_, pd_, zd_) vira (zd_, zd_))
        a2 = "(calibrado; p unilateral %s): Λ sem β *não ecoa* [leitura do operador], mas a discriminação a 5σ, o degrau da creditação, **não foi alcançada** (%s < 5); `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego (os centros dos leitores são públicos) [REAL].\" % (zd_, pd_, zd_)"
        b2 = "(calibrado): Λ sem β *não ecoa* [leitura do operador], mas a discriminação a 5σ, o degrau da creditação, **não foi alcançada** (%s < 5); `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego (os centros dos leitores são públicos) [REAL].\" % (zd_, zd_)"
        a, b = a2, b2
    n = src.count(a)
    R["casos"][nome] = {"trecho_unico_na_fonte": n == 1}
    if n != 1:
        continue
    open(RQ, "wb").write(src.replace(a, b, 1).encode("utf-8"))
    try:
        R["casos"][nome].update(roda(nome))
    finally:
        open(RQ, "wb").write(ORIG)
R["casos"]["d_restaurado_fecha_de_novo"] = roda("restaurado")
R["runtime_quadro_restaurado"] = open(RQ, "rb").read() == ORIG
R["prova"] = all(v.get("recusou") and not v.get("handoff_escrito") for k, v in R["casos"].items() if k.startswith(("a_", "b_", "c_"))) and R["casos"]["d_restaurado_fecha_de_novo"]["rc"] == 0 and R["casos"]["d_restaurado_fecha_de_novo"]["handoff_escrito"]
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open(os.path.join(H, "TESTE_FECHAR_REGRA_444.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
