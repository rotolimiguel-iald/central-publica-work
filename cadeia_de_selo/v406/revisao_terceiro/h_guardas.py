# -*- coding: utf-8 -*-
"""Revisor terceiro v406: (1) as guardas da cadeia (guarda_frases_v406.violacoes, guarda_p18_v406.violacoes) sobre o texto NOVO; (2) as MINHAS regexes independentes (frases proibidas e afirmacoes fortes) em PT e EN;
(3) a cobertura das 8 ressalvas em cada texto publico (regex por ressalva). So le."""
import ast, glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
sys.path.insert(0, R)
import guarda_frases_v406 as GF
import guarda_p18_v406 as G18
d = json.load(open(R + "dry_v406/core_ensaio.json", encoding="utf-8"))["core"]
cs = open(R + "um_v406_candidato.py", "rb").read().decode("utf-8"); L = cs.split("\n")
textos = {}
textos["artigo_pt_pysnip"] = open(R + "artigo_pt_v406.pysnip", encoding="utf-8").read()
textos["artigo_en_pysnip"] = open(R + "artigo_en_v406.pysnip", encoding="utf-8").read()
textos["md_line"] = next(l for l in L if l.lstrip().startswith("md.append(\"> **O fechamento (v406"))
pt = open(R + "dry_v406/dry_v406_pt.txt", encoding="utf-8").read().split("\n"); en = open(R + "dry_v406/dry_v406_en.txt", encoding="utf-8").read().split("\n")
textos["dry_pt_secao"] = "\n".join(pt[104:122]); textos["dry_en_secao"] = "\n".join(en[104:122])
for reg in ("fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406"):
    textos["core:" + reg] = json.dumps(d[reg], ensure_ascii=False)
textos["core:rede_fock_v394(novos)"] = json.dumps({k: d["rede_fock_v394"].get(k) for k in ("verdict", "inhabited_by_v406", "joint_contract_v406", "errata_v406")}, ensure_ascii=False)
textos["core:psibit.cond_face"] = json.dumps(d["psibit_v395"]["conditional_psion_face"], ensure_ascii=False)
textos["core:testemunha.fock_face"] = json.dumps(d["testemunha_estatica_v396"]["fock_face"], ensure_ascii=False)
textos["textos_v406.py"] = open(R + "pos_rito/textos_v406.py", encoding="utf-8").read()
textos["textos_v406_novo.pysnip"] = open(R + "pos_rito/textos_v406_novo.pysnip", encoding="utf-8").read()
res = {}
print("== (1) guardas da cadeia")
for k, t in textos.items():
    a = GF.violacoes(t); b = G18.violacoes(t)
    res[k] = {"guarda_frases": [str(x)[:140] for x in a[:5]], "p18": [str(x)[:140] for x in b[:5]]}
    print("  %-34s frases=%d p18=%d" % (k, len(a), len(b)), ("| " + str(a[:2])[:260] if a else ""), ("| P18 " + str(b[:2])[:260] if b else ""))
print("== (2) minhas regexes")
RX = {
 "tudo_derivado": r"tudo\s+(?:est[aá]\s+|foi\s+|[eé]\s+)?derivad|everything\s+(?:is\s+)?derived",
 "nenhuma_hipotese": r"nenhuma\s+hip[oó]tese\s+resta|no\s+hypothes[ie]s?\s+remain",
 "qg_provada_sem_validade": r"gravita\w+\s+qu[aâ]ntica\s+(?:est[aá]\s+|foi\s+)?(?:provad|confirmad|resolvid)|quantum\s+gravity\s+(?:is\s+|was\s+)?(?:proved|proven|confirmed|solved)",
 "fechamento_completo_ou_confirmado": r"fechamento\s+(?:est[aá]\s+|foi\s+)?(?:completo|confirmad|conclu[ií]d)|closure\s+(?:is\s+|was\s+)?(?:complete|confirmed|done)",
 "confirmado": r"\bconfirmad[oa]\b|\bconfirmed\b",
 "CONFIRMED_token": r"CONFIRMED|PROVED_BY|TGL_PROVED",
 "luz_sem_autovetor_uso": r"(?<!«)a\s+luz\s+n[aã]o\s+tem\s+autovetor",
 "unico_autovetor": r"[uú]nico\s+autovetor|only\s+eigenvector",
 "K_compacto_provado": r"K\s*\(\s*O\s*\)\s*(?:≠|!=)\s*(?:⊥|bot)[^.;]{0,40}(?:provad|teorema|theorem|proved)",
 "prova_da_natureza": r"prova\w*\s+(?:d[ao]s?\s+)?natureza|proves?\s+nature|nature\s+is\s+proved",
 "posdicao_demerito": r"p[oó]s-?di[cç][aã]o|post-?diction",
 "gate_moveu": r"gate\s+(?:se\s+)?moveu|gate\s+moved|moveu\s+o\s+gate",
}
for k in ("dry_pt_secao", "dry_en_secao", "md_line", "core:fechamento_v406", "core:cunhagens_v406", "core:kh_n1_cobertura_v406", "textos_v406_novo.pysnip"):
    t = textos[k]
    for nome, rx in RX.items():
        for m in re.finditer(rx, t, re.I):
            ctx = t[max(0, m.start() - 70):m.end() + 70].replace("\n", " ")
            print("  [%s] %s: ...%s..." % (k, nome, ctx))
print("== (3) cobertura das 8 ressalvas")
RESS = {
 "R1 K(O)!=bot so na cunha": r"K\s*\(\s*O\s*\)|cunha|wedge",
 "R2 nucleo II_inf KNOWN/DECLARADO": r"II\s*(?:\$?_?\{?\\?infty|_inf|∞|_∞|\$_∞\$)|II\$_",
 "R3 traco ENNReal ciclico nao linear": r"ENNReal",
 "R4 R7 Codex x Codex": r"Codex",
 "R5 #eval removidos": r"#eval",
 "R6 R4/R5 fora": r"R4\s*/\s*R5|R4 e R5",
 "R7 duas chaves False por teorema + lema": r"por\s+teorema|by\s+theorem|stay[s]?\s+False\s+by",
 "R8 nome provisorio": r"provis[oó]ri|provisional",
}
for k in ("artigo_pt_pysnip", "artigo_en_pysnip", "md_line", "core:fechamento_v406", "core:cunhagens_v406", "textos_v406_novo.pysnip"):
    t = textos[k]; faltam = [n for n, rx in RESS.items() if not re.search(rx, t, re.I)]
    print("  %-26s faltam: %s" % (k, faltam))
    res[k + ":ressalvas_faltam"] = faltam
# o README paragrafo (par_f) e' montado em _paragrafo_v406_de com ress completas (8) e verificado por verificar_paragrafo_v406: conferir no codigo
src = open(R + "pos_rito/textos_v406.py", encoding="utf-8").read()
print("  README paragrafo: itera fe['ressalvas'] (8) e verificar_paragrafo_v406 cobra cada uma:", "for r_ in DL_.RESSALVAS_V406" in src)
json.dump(res, open(R + "revisao_terceiro/h_guardas_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
