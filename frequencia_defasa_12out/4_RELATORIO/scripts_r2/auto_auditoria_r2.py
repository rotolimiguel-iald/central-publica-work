# -*- coding: utf-8 -*-
"""Auto-auditoria do redator r2: varre os artefatos escritos nesta rodada em 4_RELATORIO
(a) pela palavra vedada pela regua (a 'confirmacao' em ingles maiusculo, como veredito);
(b) por beta literal em CODIGO (.py): os digitos de beta (padrao BETA_LIT) so podem aparecer em texto de conferencia;
(c) valida os dois registros do mapa contra os campos do modelo (rotas.py modelo), sem registrar;
(d) grava os sha256 dos artefatos do redator.
"""
import hashlib, json, os, re, subprocess, sys, time
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTEFATOS = ["RELATORIO_FINAL.md", "registro_rota_F1.FREQUENCIA.json", "registro_mapa_F1.FREQUENCIA.json",
             "PINOS_R2.json", "IMPRESSAO_DIGITAL_KERNEL_REDATOR_R2.json", "MANIFESTO_COPIA_AUDITORIAS_R2.json",
             "scripts_r2/pinos_r2.py", "scripts_r2/copiar_auditorias_r2.py", "scripts_r2/impressao_digital_kernel.py",
             "scripts_r2/auto_auditoria_r2.py"]
VEDADA = re.compile(r"\bCONFIRMED\b")            # a palavra vedada como veredito (ingles, maiusculo)
VEDADA_PT = re.compile(r"\bCONFIRMAD[AO]S?\b")   # a mesma, em portugues maiusculo, como veredito
BETA_LIT = re.compile(r"0[.,]0120313004008\d*")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()
out = {"quando_local": time.strftime("%Y-%m-%d %H:%M:%S"), "artefatos": {}, "palavra_vedada": [], "beta_literal_em_codigo": [],
       "beta_literal_em_texto_conferencia": [], "registros_mapa": {}}
for rel in ARTEFATOS:
    p = os.path.join(AQUI, rel)
    if not os.path.exists(p):
        out["artefatos"][rel] = {"AUSENTE": True}; continue
    t = open(p, "rb").read().decode("utf-8", "replace")
    out["artefatos"][rel] = {"bytes": os.path.getsize(p), "sha256": sha(p)}
    for i, l in enumerate(t.split("\n"), 1):
        if VEDADA.search(l) or VEDADA_PT.search(l):
            out["palavra_vedada"].append([rel, i, l.strip()[:120]])
        if BETA_LIT.search(l):
            (out["beta_literal_em_codigo"] if rel.endswith(".py") else out["beta_literal_em_texto_conferencia"]).append([rel, i])
# registros do mapa: campos do modelo
modelo = json.loads(subprocess.run([sys.executable, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "modelo"],
                                   capture_output=True, text=True, encoding="utf-8").stdout)
campos_modelo = set(modelo.keys())
for rel in ["registro_rota_F1.FREQUENCIA.json", "registro_mapa_F1.FREQUENCIA.json"]:
    d = json.load(open(os.path.join(AQUI, rel), encoding="utf-8"))
    faltam = sorted(campos_modelo - set(d.keys()) - {"corrige"})
    sobram = sorted(set(d.keys()) - campos_modelo)
    arte_ok = isinstance(d.get("artefatos"), list) and all(isinstance(a, str) and os.path.exists(a) for a in d["artefatos"])
    out["registros_mapa"][rel] = {"tipo": d.get("tipo"), "rota_id": d.get("rota_id"), "dominio": d.get("dominio"),
        "campos_faltando_do_modelo": faltam, "campos_fora_do_modelo": sobram,
        "artefatos_sao_lista_de_caminhos_existentes": arte_ok, "n_artefatos": len(d.get("artefatos", []))}
out["veredito"] = ("LIMPO" if not out["palavra_vedada"] and not out["beta_literal_em_codigo"]
                   and all(not v["campos_faltando_do_modelo"] and not v["campos_fora_do_modelo"]
                           and v["artefatos_sao_lista_de_caminhos_existentes"] for v in out["registros_mapa"].values())
                   else "FALHA_VISIVEL")
dst = os.path.join(AQUI, "AUTO_AUDITORIA_REDATOR_R2.json")
tmp = dst + ".tmp"
with open(tmp, "w", encoding="utf-8") as f: json.dump(out, f, ensure_ascii=False, indent=1)
os.replace(tmp, dst)
print(json.dumps(out, ensure_ascii=False, indent=1))
