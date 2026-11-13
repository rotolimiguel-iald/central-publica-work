# -*- coding: utf-8 -*-
"""_teste_quadro_v411.py -- ENSAIO do quadro do topo, da remissao, da secao (PT/EN) e do quadro .md da v411 (quadro_v411.py) sobre a SAIDA do registro h0dn_bg1_v411 do ensaio offline (TESTE_H0DN_OFFLINE_v411_registro.json):
renderiza tudo, confere que (1) nenhum numero falta (n/d); (2) as duas guardas (P18 e frases da v411) passam em CADA linha/bloco, com a excecao dita: a cabeca do teste pre-registrada (exata, DESENHO 5.1 a) cai na R1 da P18
da v392 (TGL_PRO+VED) -- a P18 e' aplicada com a cabeca retirada, e a guarda de frases sobre o texto inteiro; (3) o LaTeX nao traz beta unicode; (4) controle negativo: tirar a linha das Cefeidas livres do item do primario REPROVA (F67).
Grava TESTE_QUADRO_v411.json e as amostras em amostras_quadro_v411\\. uso: python -B -X utf8 _teste_quadro_v411.py"""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
ns = {"_V411_TEXTOS_DA_GERENCIA": DL.TEXTOS_DA_GERENCIA_V411}   # (revisao de terceiro R1, 12/11 noite: os fechos, os rotulos e a E44 vem do DESENHO, como o gerador os embute; o item da fala do autor saiu: D181)
exec(compile(open(os.path.join(HERE, "quadro_v411.py"), encoding="utf-8").read(), "quadro_v411.py", "exec"), ns)
r = json.load(open(os.path.join(HERE, "TESTE_H0DN_OFFLINE_v411_registro.json"), encoding="utf-8"))
core = {"h0dn_bg1_v411": r}
saidas = {"quadro_pt": ns["_v411_quadro_tex"](r, "pt", DL.TITULO_QUADRO_TOPO_PT), "quadro_en": ns["_v411_quadro_tex"](r, "en", DL.TITULO_QUADRO_TOPO_PT),
          "remissao_pt": [ns["_v411_remissao_tex"]("pt")], "remissao_en": [ns["_v411_remissao_tex"]("en")],
          "secao_pt": ns["_v411_secao_tex"](core, "pt", DL.TITULO_SECAO_PT), "secao_en": ns["_v411_secao_tex"](core, "en", DL.TITULO_SECAO_EN), "md": ns["_v411_quadro_md"](r, DL.TITULO_QUADRO_TOPO_PT), "md_linha": [ns["_v411_linha_md"](r)]}
cab = (r.get("values") or {}).get("primario", {}).get("cabeca_do_teste") or ""
cab_tex = ns["_v411_tt"](cab)
res = {}
ok = True
for k, linhas in saidas.items():
    viol = []
    for i, l in enumerate(linhas):
        p18 = GF.p18_sem_cabeca(l, GF.RAMOS_V411, GF.N_DA_CABECA); fr = GF.violacoes(l)   # (decisao (c): a UNICA excecao da P18, a funcao do um.py)
        if p18 or fr:
            viol.append({"linha": i, "p18": p18[:3], "frases": fr[:3]})
    nd = sum(l.count("n/d") for l in linhas)
    beta_unicode = k not in ("md", "md_linha") and any("β" in l or "α" in l or "σ" in l for l in linhas)
    res[k] = {"n_linhas": len(linhas), "violacoes": viol, "n_d": nd, "beta_unicode_no_tex": beta_unicode}
    ok = ok and not viol and nd == 0 and not beta_unicode
# controle negativo: o item do primario sem a linha das Cefeidas livres tem de reprovar (F67)
item = [l for l in saidas["quadro_pt"] if l.startswith(r"\item \textbf{As duas linhas")][0]
sem_cl = item.split("Ao lado, no mesmo item")[0] + " Retrodição sem ajuste; o teste não é cego; validade, não creditação."
neg = GF.violacoes(sem_cl)
res["controle_negativo_sem_cefeidas"] = {"reprovou": any(v_[0].startswith("F67") for v_ in neg), "violacoes": neg[:2]}
ok = ok and res["controle_negativo_sem_cefeidas"]["reprovou"]
am = os.path.join(HERE, "amostras_quadro_v411"); os.makedirs(am, exist_ok=True)
for k, linhas in saidas.items():
    open(os.path.join(am, k + (".md" if k.startswith("md") else ".tex")), "w", encoding="utf-8", newline="\n").write("\n".join(linhas) + "\n")
res["TUDO_PASSOU"] = bool(ok)
p = os.path.join(HERE, "TESTE_QUADRO_v411.json"); open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print(json.dumps(res, ensure_ascii=False, indent=1)[:3000])
print("TUDO PASSOU" if ok else "FALHOU")
sys.exit(0 if ok else 1)
