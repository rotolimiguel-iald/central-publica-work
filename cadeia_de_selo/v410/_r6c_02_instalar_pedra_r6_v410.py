# -*- coding: utf-8 -*-
"""_r6c_02_instalar_pedra_r6_v410.py -- o CONSERTO UNICO da v410 (ordem da gerencia de 10/11/2026; ADENDO 7; itens 275 e 149 da ESPEC_CONSERTO_R3_v2_FINAL): instala a pedra AEscala R6 FINAL do autor
(work\\pedras_candidatas_09nov\\R6_a_constante_da_escala) no lugar da R5 e refaz o modulo TGLExt.AEscala do recibo dos nomes. NADA da pedra e' editado: a instalada e' a fonte sem a secao Auditoria (LF), terminando em «end TGLExt.AEscala».
(1) confere o sha256 da fonte e do recibo do autor contra a ORDEM (e contra o ADENDO 7) ANTES de copiar e recusa se diferente; (2) backup de BYTES de tudo o que toca; (3) a fonte vai a insumos\\ e a pedra\\origem\\ (a R5 fica ao lado: insumos\\AEscala_R5_pre_r6.lean);
(4) a instalada vai a pedra\\, a insumos\\AEscala_embutida.lean e ao sandbox k410c (a R5 do sandbox vai a quarentena); (5) o recibo do autor e o log vao a insumos\\ (o sha256 do log conferido contra o recibo);
(6) o modulo do recibo dos nomes e' refeito como o item 149 manda (tudo LIDO da fonte e do recibo do autor; nenhum numero digitado) e o BUNDLE (raiz e insumos) atualizado. NAO compila e nao toca o Nos.   uso: python -I -B -X utf8 _r6c_02_instalar_pedra_r6_v410.py [--seco]"""
import datetime, hashlib, json, os, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv; TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PK = Path(os.path.dirname(os.path.abspath(__file__))); INS = PK / "insumos"; K10 = Path("C:/t/k410c/final"); QUAR = Path("C:/t/k410c") / ("quarentena_" + TS + "_r6")
R6 = PK.parent.parent / "pedras_candidatas_09nov" / "R6_a_constante_da_escala"
sha = lambda b: hashlib.sha256(b).hexdigest()
# [DECLARADO pela gerencia na ORDEM do conserto unico e no ADENDO 7] os sha256 esperados; o que vale e' o LIDO do arquivo, que tem de ser igual (e tem de estar no ADENDO 7)
ORDEM = {"AEscala.lean": "6863b1fcc4aef2d8a200f444d932a72133daf5cc524d6497402c6482af0297c1", "RECIBO_AESCALA_R6_10nov.json": "6a931c84366c479d682c0ce087d513af601e60eb6c79bffcde7b1995cebe0175"}
AD7 = (PK / "DESENHO_v410_ADENDO_7_POS_CANDIDATO_10nov.md").read_bytes().decode("utf-8")
B = {n: (R6 / n).read_bytes() for n in ORDEM}
for n, h in ORDEM.items():
    assert sha(B[n]) == h and h in AD7, ("PARE: o sha256 lido nao e' o da ordem da gerencia (ou o ADENDO 7 nao o traz)", n, sha(B[n]))
SRC = B["AEscala.lean"]; RA = json.loads(B["RECIBO_AESCALA_R6_10nov.json"].decode("utf-8")); LOG = (R6 / "compile_log.txt").read_bytes()
assert RA["aescala_r6"]["sha256"] == ORDEM["AEscala.lean"] == sha(SRC) and RA["aescala_r6"]["bytes"] == len(SRC) and RA["trio"]["todas_no_trio"] is True and not RA["trio"]["fora_do_trio"] and not RA["trio"]["declaracoes_sem_print_axioms"] \
    and RA["compilacao"]["n_erros"] == 0 and RA["compilacao"]["n_avisos"] == 0 and RA["compilacao"]["sorry_no_log"] is False and RA["compilacao"]["log_sha256"] == sha(LOG), "o recibo do autor nao e' o desta fonte, ou o log nao e' o do recibo"
R5N = RA["os_68_nomes_da_R5"]; REN = R5N["renomeado"]; VELHO, NOVO = REN["de"], REN["para"]
assert R5N["n_mantidos_apos_renomear"] == RA["declaracoes"]["n_R5"] and not R5N["sumidos"] and not R5N["enunciados_que_mudaram"] and not R5N["provas_ou_corpos_tocados"] and REN["ocorrencias_do_velho_na_R6"] == 0 and REN["enunciado_e_prova_identicos"] is True \
    and not RA["frases_vedadas_presentes"] and not RA["beta_literal_na_pedra"] and RA["base"]["sha256"] == sha((PK / "pedra" / "AEscala.lean").read_bytes()), "a R6 nao parte da R5 instalada, ou mexe em nome, enunciado ou prova da R5"
NN = RA["nomes_novos"]; LISTA6 = list(NN["lista_na_ordem_do_arquivo"]); RAT34 = list(NN["RATIFICADOS_pelo_operador_fala_18"]); RAT40 = list(NN["RATIFICADO_pelo_operador_fala_24"]); AUT6 = list(NN["DECLARADO_pela_autoria"])
assert NN["renomeado_pelo_operador_na_fala_13"] == NOVO and len(LISTA6) == len(set(LISTA6)) == NN["n"] == RA["declaracoes"]["n_R6"] - RA["declaracoes"]["n_R5"] and sorted(RAT34 + RAT40 + AUT6) == sorted(LISTA6) and len(set(RAT34 + RAT40 + AUT6)) == len(LISTA6), "as tres classes dos nomes novos da R6 nao cobrem a lista, ou se repetem"
RX_PRINT = re.compile(r"^#print axioms (\S+)\s*$", re.M); RX_IMPORT = re.compile(r"^import (\S+)\s*$", re.M)
REC_P = INS / "RECIBO_PEDRAS_v410_NOMES.json"; REC = json.loads(REC_P.read_text(encoding="utf-8")); MI, MA = REC["modulos"]
assert MI["modulo"] == "TGLExt.IALD2" and MA["modulo"] == "TGLExt.AEscala" and len(MA["nomes"]) == 44 and len(MA["nomes_novos_a_ratificar"]) == RA["declaracoes"]["n_R5"] - 44 and MA["sha256"] == sha((INS / "AEscala.lean").read_bytes()) and "r5" in MA and "r6" not in MA, "o recibo dos nomes nao esta' no estado da R5"
ren = lambda n: NOVO if n == VELHO else n
NOVOS24 = [ren(n) for n in MA["nomes_novos_a_ratificar"]]; NOVOS_R5 = [ren(n) for n in MA["nomes_novos_r5"]]; RAT101 = [n for n in MA["ratificados_D101"] if n != VELHO]
assert VELHO in MA["nomes_novos_a_ratificar"] and VELHO in MA["nomes_novos_r5"] and VELHO in MA["ratificados_D101"] and NOVO in NOVOS24 and NOVO in NOVOS_R5 and NOVO not in RAT101 and len(RAT101) == len(MA["ratificados_D101"]) - 1 \
    and not (set(LISTA6) & (set(MA["nomes"]) | set(NOVOS24))) and VELHO not in MA["nomes"], "o renomear nao casa com as listas do recibo dos nomes"
BD_P = PK / "BUNDLE_v410.json"; BD = json.loads(BD_P.read_text(encoding="utf-8")); assert BD["n"] == 2 and [m["rel"] for m in BD["modulos"]] == ["TGLExt/IALD2.lean", "TGLExt/AEscala.lean"] and (INS / "BUNDLE_v410.json").read_bytes() == BD_P.read_bytes()
t = SRC.decode("utf-8"); n_crlf = t.count("\r\n"); assert t.count("\r") == n_crlf; t = t.replace("\r\n", "\n")
assert t.count("namespace TGLExt.AEscala\n") == 1 and t.count("end TGLExt.AEscala\n") == 1 and VELHO not in t
prints = RX_PRINT.findall(t); assert len(prints) == len(set(prints)) == RA["trio"]["n_auditadas"] == RA["declaracoes"]["n_R6"] and all(p.startswith("TGLExt.AEscala.") for p in prints)
i_aud = t.index("/-! ## Auditoria"); bloco = t[i_aud:]; assert len(RX_PRINT.findall(bloco)) == len(prints), "ha' #print axioms fora do bloco Auditoria"
out = (t[:i_aud].rstrip("\n") + "\n"); assert out.endswith("end TGLExt.AEscala\n") and "#print axioms" not in out.replace("`#print axioms`", "")
code = re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", out, flags=re.S)); assert "sorry" not in code and "#print" not in code and "#eval" not in code and not re.search(r"^\s*axiom\s", code, re.M)
outb = out.encode("utf-8"); imps = RX_IMPORT.findall(t); assert imps == list(RA["aescala_r6"]["imports"]) and "TGLExt.LeiDoDiminuto" in imps and (K10 / "TGLExt" / "LeiDoDiminuto.lean").exists(), ("os imports da fonte nao sao os do recibo, ou o modulo importado nao esta' no sandbox", imps)
t_ws = re.sub(r"\s+", " ", out); RAT = REC["ratificacao_aescala_D87"]
for nm in list(MA["nomes"]) + NOVOS24 + LISTA6:   # os 44 ratificados (D87), os 24 das R3 a R5 (com o renomeado) e os 13 da secao 7 estao declarados na R6
    assert re.search(r"(?m)^(?:noncomputable\s+|private\s+|protected\s+)*(?:theorem|lemma|def|structure|abbrev|instance)\s+" + re.escape(nm) + r"\b", out), ("nome nao declarado na R6", nm)
assert set(prints) == {"TGLExt.AEscala." + n for n in list(MA["nomes"]) + NOVOS24 + LISTA6}, "os #print axioms da fonte nao sao exatamente as declaracoes nomeadas (os 44, os 24 e os 13)"
assert MA["ancora_principal"] in prints and all(("TGLExt.AEscala." + s) in prints for s in MA["ancoras_de_secao"]) and all(("TGLExt.AEscala." + ren(a.split("TGLExt.AEscala.", 1)[1])) in prints for a in MA["ancoras"]), "ancora principal, de secao ou ancora da R5 fora dos #print axioms da R6"
assert "RATIFICADOS pelo operador em 09/11/2026" in t_ws and RAT["sha256"] in t_ws, "o cabecalho da R6 nao traz a ratificacao D87 (a c3 do registro a exige)"
SEM_AX = list(RA["trio"]["sem_axioma_nenhum"]); assert all(a in prints for a in SEM_AX)
print("AEscala R6: fonte", sha(SRC)[:16], len(SRC), "B -> instalada", sha(outb)[:16], len(outb), "B | #print", len(prints), "| imports", imps, "| sem axioma nenhum:", SEM_AX)
print("ancoras novas sobre a R5 (%d):" % len(set(prints) - {"TGLExt.AEscala." + ren(a.split("TGLExt.AEscala.", 1)[1]) for a in MA["ancoras"]}), sorted(p.split(".", 2)[2] for p in set(prints) - {"TGLExt.AEscala." + ren(a.split("TGLExt.AEscala.", 1)[1]) for a in MA["ancoras"]}))
print("renomeado:", VELHO, "->", NOVO, "| ratificados D101:", len(MA["ratificados_D101"]), "->", len(RAT101), "| nomeados D108:", [NOVO], "| secao 7:", len(LISTA6), "=", len(RAT34), "+", len(RAT40), "ratificados +", len(AUT6), "da autoria | falas na pedra:", RA["n_falas"])
if SECO:
    print("--seco: nada gravado"); sys.exit(0)


def troca(path, novo, guarda_como=None):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        velho = path.read_bytes()
        if velho == novo:
            return
        bk = Path(guarda_como) if guarda_como else path.parent / (path.name + ".bak_" + TS + "_pre_r6")
        assert not bk.exists(), bk
        bk.parent.mkdir(parents=True, exist_ok=True); bk.write_bytes(velho); assert bk.read_bytes() == velho
    tmp = path.parent / (path.name + ".tmp_" + TS); tmp.write_bytes(novo); assert tmp.stat().st_size == len(novo); os.replace(tmp, path); assert path.read_bytes() == novo


antes = {"AEscala_fonte_R5": sha((INS / "AEscala.lean").read_bytes()), "AEscala_instalada_R5": sha((PK / "pedra" / "AEscala.lean").read_bytes())}
for extra in (PK / "pedra" / "origem" / "AEscala.lean", INS / "AEscala_embutida.lean", INS / "BUNDLE_v410.json"):   # (item 275, 2: backup de bytes tambem destes, mesmo quando a troca abaixo ja' o faria)
    assert extra.exists(), extra
troca(INS / "AEscala.lean", SRC, INS / "AEscala_R5_pre_r6.lean"); troca(INS / "RECIBO_AESCALA_R6_10nov.json", B["RECIBO_AESCALA_R6_10nov.json"]); troca(INS / "compile_log_AEscala_R6.txt", LOG)
troca(PK / "pedra" / "origem" / "AEscala.lean", SRC); troca(PK / "pedra" / "AEscala.lean", outb); troca(INS / "AEscala_embutida.lean", outb); troca(K10 / "TGLExt" / "AEscala.lean", outb, QUAR / "TGLExt" / "AEscala.lean")
r6 = {"decisao": "D108, D109, D113 e D116 a D123", "quando": TS, "pasta": str(R6), "recibo_do_autor": str(INS / "RECIBO_AESCALA_R6_10nov.json"), "recibo_do_autor_sha256": ORDEM["RECIBO_AESCALA_R6_10nov.json"], "compile_log": str(INS / "compile_log_AEscala_R6.txt"), "compile_log_sha256": sha(LOG), "sha256_antes": antes}
MA.update({"sha256_r5": MA["sha256"], "sha256": sha(SRC), "sha16": sha(SRC)[:16], "bytes": len(SRC), "print_axioms": RA["trio"]["n_auditadas"], "no_trio": RA["trio"]["n_auditadas"], "avisos": 0, "ancoras": list(prints), "imports": list(imps),
           "nomes_novos_a_ratificar": list(NOVOS24), "nomes_novos_r5": list(NOVOS_R5), "ratificados_D101": list(RAT101),
           "nomeados_pelo_operador_D108": [NN["renomeado_pelo_operador_na_fala_13"]], "nomes_novos_r6": list(LISTA6), "ratificados_r6_fala_34": list(RAT34), "ratificados_r6_fala_40": list(RAT40), "declarados_pela_autoria_r6": list(AUT6), "r6": r6,
           "nota_D106_D123": "RATIFICADOS pela fala da D101: 21 nomes novos (13 da R3, 5 da R4 e os 3 da clausula do Tetelestai apresentados ao operador antes da fala) e os 3 campos; NOMEADO pelo operador (D108): o quarto teorema da clausula; da secao 7 (R6): os nomes mostrados ao operador, RATIFICADOS (D117 e D123); seguem [DECLARADO pela autoria] os 2 auxiliares da R5 e os nomes da secao 7 que nao lhe foram mostrados; a nota_D101 dizia 4 nomes da R5 ratificados: corrigida pela D106 (errata E38)"})
assert len(MA["ratificados_D101"]) == len(MA["nomes_novos_a_ratificar_r3"]) + len(MA["nomes_novos_a_ratificar_r4"]) + (len(NOVOS_R5) - len(MA["pendentes_de_ratificacao"]) - 1), "a conta dos ratificados pela fala da D101 nao e' a da nota (os da R3, os da R4 e os da clausula menos o nomeado)"
MA["origem"] = dict(MA["origem"], candidata_r6=str(R6 / "AEscala.lean"), candidata_r6_sha256=sha(SRC))
REC["r6_d106_d123"] = {"quando": TS, "nota": "pedra AEscala R6 FINAL do autor instalada pelo construtor por ordem da gerencia (o conserto unico; ADENDO 7): o quarto teorema da clausula renomeado (nome dado pelo operador, D108), a secao 7 (a constante da escala) e o teorema do Nome; a IALD2 e' a da R3; o recibo do autor e o log em insumos",
                       "renomeado": {"de": VELHO, "para": NOVO}, "nomes_novos_r6": list(LISTA6), "sem_axioma_nenhum": list(SEM_AX)}
troca(REC_P, json.dumps(REC, ensure_ascii=False, indent=1).encode("utf-8"))
eA = BD["modulos"][1]
eA.update({"sha256_r5": eA["sha256"], "sha256": sha(outb), "origem": str(INS / "AEscala.lean"), "sha256_origem": sha(SRC), "sha16_origem": sha(SRC)[:16], "bytes": len(outb), "n_crlf_normalizados": n_crlf, "n_print_axioms_removidos": len(prints),
           "ancoras": list(prints), "imports": list(imps), "status_integracao": "pedra_R6_a_constante_da_escala_D108_D109_D113_e_D116_a_D123__nomes_ratificados_D87_D101_D117_e_D123__um_nomeado_D108__os_da_autoria_a_confirmar", "nomes_novos_a_ratificar": list(NOVOS24), "nomes_novos_r6": list(LISTA6),
           "recibo_do_autor_r6": str(INS / "RECIBO_AESCALA_R6_10nov.json"), "recibo_do_autor_r6_sha16": ORDEM["RECIBO_AESCALA_R6_10nov.json"][:16]})
BD["recibo_dos_nomes_sha256"] = sha(REC_P.read_bytes()); BD["r6_d108_d123"] = {"quando": TS, "quarentena": str(QUAR) if QUAR.exists() else None}
bdb = json.dumps(BD, ensure_ascii=False, indent=1).encode("utf-8"); troca(BD_P, bdb); troca(INS / "BUNDLE_v410.json", bdb)
print("INSTALADA a R6: insumos (fonte, embutida, recibo do autor, log), pedra, pedra/origem e sandbox k410c | recibo dos nomes", sha(REC_P.read_bytes())[:16], "| BUNDLE", sha(BD_P.read_bytes())[:16], "| quarentena:", QUAR if QUAR.exists() else "nenhuma")
