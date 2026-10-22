# -*- coding: utf-8 -*-
"""Le as linhas ROW da saida da auditoria (logs/aud_r2_SAIDA.txt, elaborador #r2_tabela sobre o ambiente compilado) e
grava TABELA_R1_R2.json e TABELA_R1_R2.md. Confere contra o ADENDO R2: renomeacoes = o mapa; TIPO_MUDOU so nos geradores
de NamedIdentity; nenhuma REMOVIDA. Uso: gerar_tabela.py"""
import os, json, hashlib, collections
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.dirname(R2)
P = os.path.join(R2, "logs", "aud_r2_SAIDA.txt")
raw = open(P, "rb").read()
t = raw.decode("utf-8")
ad = json.load(open(os.path.join(W, "2_PREREGISTRO", "ADENDO_R2.json"), encoding="utf-8"))
mapa = ad["renomeacoes"]["mapa"]
P1, P2 = "TGLExt.TheIdentityHasAName_r1.", "TGLExt.TheIdentityHasAName."
rows = []
for ln in t.splitlines():
    if not ln.startswith("ROW|"):
        continue
    f = ln.split("|")
    st, n1, n2, k1, k2, teqv, tequal, val, internal = f[1:10]
    terased = f[10] if len(f) > 10 else "-"
    bn = "|".join(f[11:]) if len(f) > 11 else "-"
    rows.append({"status": st, "r1": n1.replace(P1, ""), "r2": n2.replace(P2, ""), "tipo_r1": k1, "tipo_r2": k2,
                 "enunciado_eqv": teqv, "enunciado_equal": tequal, "enunciado_equal_sem_nomes_de_binder": terased,
                 "valor_eqv/valor_equal_sem_nomes_de_binder": val, "interna": internal == "true",
                 "diferenca_de_binder": bn})
cont = collections.Counter(r["status"] for r in rows)
cont_pub = collections.Counter(r["status"] for r in rows if not r["interna"])
ger = {"NamedIdentity.casesOn", "NamedIdentity.mk", "NamedIdentity.mk._flat_ctor", "NamedIdentity.mk.inj",
       "NamedIdentity.mk.injEq", "NamedIdentity.mk.noConfusion", "NamedIdentity.mk.sizeOf_spec", "NamedIdentity.rec",
       "NamedIdentity.recOn"}
tipo_mudou = {r["r1"] for r in rows if r["status"] == "TIPO_MUDOU"}
renom = {r["r1"]: r["r2"] for r in rows if r["status"] == "RENOMEADA"}
renom_top = {k: v for k, v in renom.items() if "." not in k}
mantidas_eqv_falso = [r for r in rows if r["status"] in ("MANTIDA", "RENOMEADA") and r["enunciado_eqv"] != "true"]
equal_falso = [r for r in rows if r["status"] in ("MANTIDA", "RENOMEADA") and r["enunciado_equal"] != "true"]
equal_falso_e_erased_falso = [r for r in equal_falso if r["enunciado_equal_sem_nomes_de_binder"] != "true"]
valor_mudou = [r["r1"] for r in rows if r["status"] in ("MANTIDA", "RENOMEADA", "TIPO_MUDOU")
               and r["valor_eqv/valor_equal_sem_nomes_de_binder"] not in ("na/na", "true/true")]
conf = {
    "renomeacoes_de_1o_nivel_iguais_ao_mapa_do_ADENDO": renom_top == mapa,
    "tipo_mudou_so_nos_geradores_de_NamedIdentity": tipo_mudou <= ger,
    "tipo_mudou_lista": sorted(tipo_mudou),
    "removidas": [r["r1"] for r in rows if r["status"] == "REMOVIDA"],
    "mantidas_ou_renomeadas_com_enunciado_diferente_eqv": [r["r1"] for r in mantidas_eqv_falso],
    "Expr_equal_falso_mas_eqv_verdadeiro": [r["r1"] for r in equal_falso],
    "Expr_equal_falso_mesmo_sem_nomes_de_binder": [r["r1"] for r in equal_falso_e_erased_falso],
    "definicoes_com_valor_diferente": valor_mudou,
    "novas": [r["r2"] for r in rows if r["status"] == "NOVA"],
}
out = {"fonte": P, "fonte_sha256": hashlib.sha256(raw).hexdigest(), "n_linhas": len(rows),
       "contagem_todas": dict(cont), "contagem_sem_internas": dict(cont_pub), "conferencias": conf, "linhas": rows}
json.dump(out, open(os.path.join(R2, "TABELA_R1_R2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L = ["TABELA r1 -> r2 — F1.IDENTIDADE — 13/10/2026 (construtor da r2, em nome próprio)", "",
     "Lida do ambiente compilado pelo elaborador `#r2_tabela` (`pedra/AudR2.lean`): a r1 compilada numa cópia com o",
     "namespace trocado (`TGLExt.TheIdentityHasAName_r1`, `pedra/IdR1_TheIdentityHasAName_r1.lean`) e a r2 no mesmo",
     "ambiente. O tipo de cada constante da r1, com os nomes da r1 levados pelo mapa do ADENDO R2, comparado ao tipo da",
     "r2 por `Expr.eqv` (alfa-equivalência), por `Expr.equal` (estrita) e por `Expr.equal` depois de apagar SÓ os nomes",
     "de binder. Para definições, o mesmo com o valor. Fonte: `logs/aud_r2_SAIDA.txt` sha256 " + out["fonte_sha256"] + ".", "",
     "Contagem (todas): " + json.dumps(dict(cont), ensure_ascii=False) + "; sem as internas: " +
     json.dumps(dict(cont_pub), ensure_ascii=False) + ".", "",
     "| status | r1 | r2 | espécie | enunciado eqv | equal | equal sem nomes de binder | valor (eqv / equal sem nomes) |",
     "|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r["interna"]:
        continue
    L.append("| %s | `%s` | `%s` | %s→%s | %s | %s | %s | %s |" % (r["status"], r["r1"], r["r2"], r["tipo_r1"], r["tipo_r2"],
             r["enunciado_eqv"], r["enunciado_equal"], r["enunciado_equal_sem_nomes_de_binder"],
             r["valor_eqv/valor_equal_sem_nomes_de_binder"]))
L += ["", "Internas (nomes com componente `_`, geradas pelo elaborador): " +
      ", ".join("%s `%s`" % (r["status"], r["r2"] if r["r2"] != "-" else r["r1"]) for r in rows if r["interna"]) + ".",
      "", "Conferências contra o ADENDO R2:", "```", json.dumps(conf, ensure_ascii=False, indent=1), "```", ""]
open(os.path.join(R2, "TABELA_R1_R2.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L))
print(json.dumps({"contagem_todas": dict(cont), "contagem_sem_internas": dict(cont_pub), "conferencias": conf},
                 ensure_ascii=False, indent=1))
