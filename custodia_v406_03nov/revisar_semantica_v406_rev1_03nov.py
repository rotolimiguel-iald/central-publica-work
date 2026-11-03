# -*- coding: utf-8 -*-
"""03/11/2026 02:4x, gerencia c1: o C4 da G1 (pre-voo da pedra generica, cofre v406 x cofre v405) reprovou em S8_registro com fora_do_padrao = ["rede_fock_v394"]:
o veredito desse registro muda de LETRA (nao so de digitos e pino) entre a v405 e a v406 — TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CONTRACT_OPEN__GATE_UNMOVED ->
...__JOINT_CERTIFICATE_INHABITED_V406__THREE_JOINT_ITEMS_STILL_OPEN__GATE_UNMOVED — porque whole_certificate_inhabited deixou de ser literal False e passou a ser LIDA do
kernel (physicalFockCertificate), a troca DITA no handoff («troca dita (so numeros, e o veredito de rede_fock_v394, que muda por ordem do fecho)»), conferida pelo registro
selado fechamento_v406 e aprovada pela revisao de terceiro (Sonnet, R3). A ESPEC_CENTRAL §4.3 manda: mudanca de veredito fora do padrao so passa se estiver em
`mudados_permitidos` com motivo, numa REVISAO da semantica gravada AO LADO do rascunho (SEMANTICA_CUSTODIA.rev<n>.json), por revisor distinto de quem rascunhou (o rascunho
e' do script, sem modelo; «ou a gerencia»). Este script grava a rev1 (nunca por cima do rascunho), com o motivo e as fontes por sha256, e CONFERE antes de sair rodando a
propria pedra generica (medir_custodia_generica, so' leitura) sobre os dois cofres: S8 tem de passar e a pedra tem de dar pass=True; senao apaga a rev1 e rc 1.
Nenhum veredito, selo, core ou um.py e' tocado; o gate nao se move; validade no kernel nao e' creditacao. Escrito pelo Write."""
import datetime, hashlib, importlib.util, json, sys
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); OC = CEN / "vault" / "originals_copy"; V, A = "v406", "v405"
CV = OC / ("um_unificado_" + V); NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
rasc_p = CV / "SEMANTICA_CUSTODIA.json"; rev_p = CV / "SEMANTICA_CUSTODIA.rev1.json"
assert rasc_p.is_file() and not rev_p.exists(), "rascunho ausente ou rev1 ja existe"
man = json.loads((CV / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8"))
assert man["semantica_custodia"]["sha256"] == sha(rasc_p) and man["semantica_custodia"]["revisao"] == 0, "o rascunho nao e' o pinado no manifesto"
S0 = json.loads(rasc_p.read_text(encoding="utf-8"))
assert S0["versao"] == V and S0["revisao"] == 0 and S0["revisor"] is None and S0["mudados_permitidos"] == []
core_v = json.loads((CV / "um_absoluto.json").read_text(encoding="utf-8"))["core"]; core_a = json.loads((OC / ("um_unificado_" + A) / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
vd_v, vd_a = core_v["rede_fock_v394"]["verdict"], core_a["rede_fock_v394"]["verdict"]
assert vd_v != vd_a and "JOINT_CERTIFICATE_INHABITED_V406" in vd_v and "JOINT_CONTRACT_OPEN" in vd_a and vd_v.endswith("GATE_UNMOVED"), (vd_v, vd_a)
assert core_v["rede_fock_v394"]["whole_certificate_inhabited"] is True and core_a["rede_fock_v394"]["whole_certificate_inhabited"] is False
assert core_v["fechamento_v406"]["four_keys"]["rede_fock_v394.whole_certificate_inhabited"] is True and core_v["fechamento_v406"]["mechanics"]["passed"] is True
hand = (CV / ("HANDOFF_%s_CUSTODIA.md" % V)).read_text(encoding="utf-8", errors="replace")
assert "o veredito de `rede_fock_v394`, que muda por ordem do fecho" in hand, "a troca dita nao esta' no handoff do cofre"
rev = json.loads((CEN / "work/cadeia_de_selo/v406/revisao_terceiro/REVISAO_TERCEIRO_v406.json").read_text(encoding="utf-8")); assert rev["aprovada"] is True
fontes = {"handoff_no_cofre": {"arquivo": "HANDOFF_v406_CUSTODIA.md", "sha256": sha(CV / "HANDOFF_v406_CUSTODIA.md"), "trecho": "troca dita (so numeros, e o veredito de rede_fock_v394, que muda por ordem do fecho)"},
          "core_no_cofre": {"arquivo": "um_absoluto.json", "sha256": sha(CV / "um_absoluto.json"), "registro": "fechamento_v406 (four_keys.rede_fock_v394.whole_certificate_inhabited = True; mechanics 14/14)"},
          "revisao_de_terceiro": {"arquivo": str(CEN / "work/cadeia_de_selo/v406/revisao_terceiro/REVISAO_TERCEIRO_v406.json"), "sha256": sha(CEN / "work/cadeia_de_selo/v406/revisao_terceiro/REVISAO_TERCEIRO_v406.json"), "aprovada": True, "candidato_sha16": rev["candidato_sha16"]},
          "rascunho": {"arquivo": "SEMANTICA_CUSTODIA.json", "sha256": sha(rasc_p)}}
S1 = dict(S0)
S1.update({"estatuto": "REVISADO (gerencia c1, em nome proprio; o rascunho fica ao lado, intocado)", "revisor": "gerencia c1 (Claude Code, sessao 6da8f00d), distinta do script que rascunhou", "revisao": 1,
           "revisado_em": datetime.datetime.now().isoformat(timespec="seconds"),
           "veredito_camada_sufixo": "SEMANTICA_REVISADA_REV1_PELA_GERENCIA_C1",   # o segmento semantico do veredito do runner (C6) e do modulo dos 16 (C8): a letra diz que houve revisao
           "mudados_permitidos": [{"nome": "rede_fock_v394", "verdict_" + A: vd_a, "verdict_" + V: vd_v,
                                   "motivo": ("troca DITA por ordem do fecho (v406): a chave whole_certificate_inhabited deixou de ser literal False (v394 a v405) e passou a ser LIDA do kernel do rito "
                                              "(physicalFockCertificate, no trio, declarada no modulo do topo), com a errata E14 ao lado; o segmento JOINT_CONTRACT_OPEN vira JOINT_CERTIFICATE_INHABITED_V406__"
                                              "THREE_JOINT_ITEMS_STILL_OPEN (joint_contract_open_v394 fica True: tres itens do contrato conjunto seguem abertos); GATE_UNMOVED permanece. Conferido em runtime pelo "
                                              "registro selado fechamento_v406 (14/14) e aprovado pela revisao de terceiro (R3). Nao e' veredito fisico; o gate nao se move; validade no kernel nao e' creditacao."),
                                   "fontes": fontes}],
           "nota_da_revisao": ("a revisao nao altera as regras dos blocos rascunhadas pelo script (verdict_deve_conter com as negacoes de fechamento_v406, cunhagens_v406 e kh_n1_cobertura_v406; "
                               "os pares de cunhagens); acrescenta so' o que a pedra nao le sozinha: a mudanca de veredito fora do padrao, com motivo e fontes (ESPEC_CENTRAL §4.3).")})
# conferir ANTES de deixar a rev1 no cofre: a pedra generica, so' leitura, sobre os dois cofres
tmp = rev_p.with_name(rev_p.name + ".tmp_" + TS); open(tmp, "xb").write(json.dumps(S1, ensure_ascii=False, indent=1).encode("utf-8")); tmp.replace(rev_p)
spec = importlib.util.spec_from_file_location("custodia_generica", str(CEN / "tools/custodia_g1/generico/custodia_generica.py")); CG = importlib.util.module_from_spec(spec); spec.loader.exec_module(CG)
S_lida = CG.semantica_de_maior_revisao(CV, man); assert S_lida.get("revisao") == 1 and S_lida.get("revisor"), "a pedra nao leu a rev1"
r = CG.medir_custodia_generica(OC, V, A)
ruins = {k: x for k, x in r.get("checks", {}).items() if not x["ok"]}
print("pedra: pass", r.get("pass"), "| semantica", r.get("semantica"), "| ceticos", r.get("ceticos", {}).get("1_reprovou"), r.get("ceticos", {}).get("2_reprovou"), "| erro", r.get("erro"))
print("S8:", json.dumps(r["checks"]["S8_registro"], ensure_ascii=False)[:400])
if not r.get("pass"):
    rev_p.unlink(); print("REPROVADO; rev1 retirada; checks ruins:", json.dumps(ruins, ensure_ascii=False)[:1500]); sys.exit(1)
rec = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "quem": "gerencia c1", "rev1": str(rev_p), "rev1_sha256": sha(rev_p), "rascunho_sha256": sha(rasc_p), "pedra_generica": r,
       "motivo": "C4 reprovou em S8_registro (fora_do_padrao: rede_fock_v394); ESPEC_CENTRAL §4.3: mudados_permitidos com motivo numa revisao ao lado"}
(CEN / "work/custodia_v406_03nov" / "RECIBO_SEMANTICA_REV1_v406.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("rev1 gravada:", rev_p.name, sha(rev_p)[:16], "| recibo RECIBO_SEMANTICA_REV1_v406.json")
