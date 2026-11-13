# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411 (retomada)] o COMPLEMENTO do recibo do kernel da v411 (pedido do fork B e do fork A: o B(n) e o pos-rito consomem vinculo\CRITERIOS e varredura_tokens)
"""complementar_recibo_kernel_v411.py -- SO' MEDE (nenhum build, nenhum Audit: o kernel do k411c esta' medido e nao se refaz) e acrescenta ao kernel\\KERNEL_RECIBO_v411.json, no molde do recibo da v410
(contrato KERNEL_RECIBO_R3_2), o que o pos_build da v411 nao gravava: (1) `varredura_tokens` (a varredura RECURSIVA das fontes .lean do sandbox C:\\t\\k411c\\final, sem .lake, com os tokens proibidos do proprio um.py
da v410 selada, comentarios e strings retirados pela funcao do um.py); (2) `criterios` na forma da v410 ({nome: {"medido": v}}: J1 = diferenca dos TOTAIS do KH-N1 v411 - v410, as entradas antigas do Audit com a mesma
lista de axiomas do axiom_report da base, os tokens proibidos, r1 ausente, as declaracoes novas no trio -- vacuo: nao ha'); os booleanos da v411 ficam em `criterios_da_v411`; (3) kernel\\vinculo\\CRITERIOS_v411.json
(contrato CRITERIOS_R3_1, x19 = 'nao': o recibo nao lista modulo, a v411 nao tem pedra nova); (4) kernel\\LOGS_COPIADOS_v411.json (sha256 e bytes dos tres logs, a linha TOTAL). O KH_N1_v411.json NAO e' tocado
(e' fonte do candidato). Backup de BYTES antes; escrita por .tmp; idempotente nos valores. uso: python -B -X utf8 complementar_recibo_kernel_v411.py"""
import datetime, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
import base_um_v410 as B  # noqa: E402
KD = os.path.join(HERE, DL.KERNEL_DIR); VD = os.path.join(HERE, "vinculo")
rd = lambda p: open(p, "rb").read(); sha = lambda b: hashlib.sha256(b).hexdigest()
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
REC_P = os.path.join(KD, "KERNEL_RECIBO_v411.json"); rec = json.loads(rd(REC_P).decode("utf-8"))
kh = json.load(open(os.path.join(KD, "KH_N1_v411.json"), encoding="utf-8")); kh10 = json.load(open(os.path.join(DL.V410, "kernel", "KH_N1_v410.json"), encoding="utf-8"))
core0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto.json"), encoding="utf-8"))["core"]
NS = B.carregar(["_lean_strip_comments_and_strings", "_LEAN_FORBIDDEN_TOKENS"])
TOKS = list(NS["_LEAN_FORBIDDEN_TOKENS"]); strip_ = NS["_lean_strip_comments_and_strings"]
# (1) a varredura recursiva das fontes do sandbox (sem .lake)
n_lean = n_o16 = 0; hits = []; hits_probe = []; links = []; baks = []
pilha = [DL.SANDBOX]
while pilha:
    d_ = pilha.pop()
    with os.scandir(d_) as it_:
        for e_ in it_:
            if e_.name == ".lake":
                continue
            if ".bak" in e_.name:
                baks.append(e_.path)
            if e_.is_junction() or e_.is_symlink():
                links.append(e_.path)
            elif e_.is_dir(follow_symlinks=False):
                pilha.append(e_.path)
            elif e_.is_file(follow_symlinks=False) and e_.name.lower().endswith(".lean"):
                n_lean += 1; rel_ = os.path.relpath(e_.path, DL.SANDBOX).replace(os.sep, "/"); n_o16 += rel_.startswith("TGLExt/O16/")
                code_ = strip_(rd(e_.path).decode("utf-8"))
                for tok_ in TOKS:
                    if re.search(r"\b%s\b" % re.escape(tok_), code_):
                        (hits_probe if os.path.basename(rel_).startswith("Probe") else hits).append("%s:%s" % (rel_, tok_))
rec10 = json.load(open(os.path.join(DL.V410, "kernel", "KERNEL_RECIBO_v410.json"), encoding="utf-8"))
# (2) as entradas antigas do Audit (os nomes do TGL/Audit.lean do sandbox) com a MESMA lista de axiomas do axiom_report da base
au = rd(os.path.join(KD, "audit.log")).decode("utf-8", "replace")
axm = {m_.group(1): [x_.strip() for x_ in m_.group(2).replace("\n", " ").split(",") if x_.strip()] for m_ in re.finditer(r"(?m)^'(.+)' depends on axioms: \[([^\]]*)\]", au)}
axm.update({m_.group(1): [] for m_ in re.finditer(r"(?m)^'(.+)' does not depend on any axioms", au)})
axr0 = (core0.get("kernel_formalization") or {}).get("axiom_report") or {}
nomes_antigos = sorted(set(re.findall(r"(?m)^#print axioms (\S+)", rd(os.path.join(DL.SANDBOX, "TGL", "Audit.lean")).decode("utf-8"))))
iguais_ant = sum(1 for n_ in nomes_antigos if n_.lstrip("@") in axm and set(axm[n_.lstrip("@")]) == set(axr0.get(n_.lstrip("@"), ["?"])))
tot, tot10 = kh["linha_TOTAL"], kh10["linha_TOTAL"]
j1 = [tot["decl"] - tot10["decl"], tot["thm"] - tot10["thm"], tot["fora_do_trio"]]
criterios = {"j1_declaracoes": j1[0], "j1_teoremas": j1[1], "j1_fora_do_trio": j1[2], "audit_entradas_antigas_identicas": iguais_ant, "tokens_proibidos": len(hits),
             "r1_ausente": not os.path.exists(os.path.join(DL.SANDBOX, "TGLExt", "TheSingularityReadsTheAttractor.lean")), "declaracoes_novas_no_trio": True}
conf = {"varredura_sem_link_nem_bak": not links and not baks, "zero_tokens_proibidos": not hits, "contagens_iguais_as_da_v410": n_lean == rec10["varredura_tokens"]["arquivos_lean"] and n_o16 == rec10["varredura_tokens"]["arquivos_lean_em_TGLExt_O16"],
        "j1_zero_sem_modulo_novo": j1 == [0, 0, 0], "entradas_antigas_todas_identicas": iguais_ant == len(nomes_antigos) > 0, "nenhuma_pedra_no_recibo": rec.get("pedras") == []}
print(json.dumps({"varredura": {"arquivos_lean": n_lean, "em_O16": n_o16, "hits": hits[:5], "hits_probe": len(hits_probe)}, "criterios": criterios, "conferencias": conf}, ensure_ascii=False))
assert all(conf.values()), ("o complemento do recibo nao fecha", conf)
novo = dict(rec)
if "criterios_da_v411" not in novo:
    novo["criterios_da_v411"] = rec.get("criterios")
novo["criterios"] = {k_: {"medido": v_} for k_, v_ in criterios.items()}
novo["varredura_tokens"] = {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16, "raiz_da_varredura": DL.SANDBOX.replace("\\", "/"), "sem_lake": True, "hits_em_Probe": len(hits_probe)}
novo["complemento"] = {"por": "complementar_recibo_kernel_v411.py (claude-construtor-v411, retomada, 12/11/2026)", "nota": "so' medicao (nenhum build/Audit refeito); molde: o recibo da v410"}
logs = {n_: {"bytes": len(rd(os.path.join(KD, n_))), "sha256": sha(rd(os.path.join(KD, n_))), "origem": os.path.join(KD, n_), "copiado": False} for n_ in ("lake_build.log", "audit.log", "construir_marcas.txt")}
logs["cobertura_linha"] = tot
crit = {"contrato": "CRITERIOS_R3_1", "versao": "v411", "preenchido": True, "x19": "nao", "esperados": criterios,
        "origem": "[DERIVED] preenchido pela PREPARACAO com a medicao do kernel\\KERNEL_RECIBO_v411.json (J1 = diferenca dos TOTAIS do KH-N1 v411 - v410 = zero: a v411 nao tem modulo novo). x19='nao': o recibo v411 nao lista modulo "
                  "(a LightNetStandardWedgeDataBGL.lean ja' esta no kernel desde a v392; R31-6: 'sim' <=> a pedra consta do recibo); a gerencia confere e pina o sha256 antes do B(n).",
        "nota": "NOT_FALSIFIED nunca e creditacao; nada aqui move o gate"}
os.makedirs(VD, exist_ok=True)
for p_, obj_ in ((REC_P, novo), (os.path.join(KD, "LOGS_COPIADOS_v411.json"), logs), (os.path.join(VD, "CRITERIOS_v411.json"), crit)):
    b_ = json.dumps(obj_, ensure_ascii=False, indent=1).encode("utf-8")
    if os.path.exists(p_):
        if rd(p_) == b_:
            print("igual:", os.path.basename(p_)); continue
        open(p_ + ".bak_" + TS, "wb").write(rd(p_))
    open(p_ + ".tmp", "wb").write(b_); assert os.path.getsize(p_ + ".tmp") == len(b_); os.replace(p_ + ".tmp", p_); print("gravado:", p_, sha(b_)[:16])
