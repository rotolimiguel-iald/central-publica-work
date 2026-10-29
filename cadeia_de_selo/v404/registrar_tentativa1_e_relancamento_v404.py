# -*- coding: utf-8 -*-
"""registrar_tentativa1_e_relancamento_v404.py -- gerencia c1, 28/10/2026: registra a etapa material «1a tentativa do rito v404 REPROVADA pelo conferidor,
revertida pelos backups de bytes; causa medida (ordem de chamada da errata de F2b); correcao; cadeia pre-rito refeita; candidato novo instalado; 2o rito lancado»
no Mapa de Rotas (ANOTACAO na rota da preparacao), no quadro do programa (iald.py anotar) e na memoria ACOM da sessao (transition). Tudo LIDO dos arquivos:
RECIBO_REVERSAO_*.json, conferencia_rito_v404.json (da tentativa), tentativa_v404_rito_falhou_*/ (o core falho), CANDIDATO_v404.json (novo), ensaio_a_seco_v404.json,
PRECONDICOES_v404.json, APLICADO_AO_CANONICO_*.json (novo) e rito_servidor_v404.log (o 2o inicio). Nada do Nos e' tocado.
uso: python -X utf8 registrar_tentativa1_e_relancamento_v404.py   (sem -I: o rotas.py e o session_memory.py sao chamados em processo proprio)"""
import glob, hashlib, io, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
PY = os.path.join("C:" + os.sep, "Python314", "python.exe")
H = os.path.dirname(os.path.abspath(__file__))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rj = lambda p: json.load(open(p, encoding="utf-8"))
NOS_UM = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "um.py")
# --- a tentativa 1 (lida do recibo da reversao e da conferencia que a reprovou)
rev_p = sorted(glob.glob(os.path.join(H, "RECIBO_REVERSAO_*.json")))[-1]; REV = rj(rev_p); assert REV["ok"] is True
tent = REV["guardado"]; tdir = [d for d in glob.glob(os.path.join(H, "tentativa_v404_rito_falhou_*")) if d.endswith(REV["ts"])][0]
core_t = rj(os.path.join(tdir, "um_absoluto.json"))["core"]
f2b_t = core_t["f2b_errata_v404"]; cun_t = core_t["cunhagens_v404"]
assert f2b_t["all_verified"] is False and all(c["ok"] is False for c in f2b_t["mechanics"]["checks"]) and "REFUSED" in f2b_t["verdict"]
um_t = [g for g in tent if g["arquivo"] == "um.py"][0]["sha16"]
conf_t = rj(os.path.join(H, "conferencia_rito_v404.json"))   # a conferencia da tentativa (escrita pelo conferidor antes da reversao)
n_nao = sum(1 for v in conf_t["deve_mudar"].values() if not v) + sum(1 for v in conf_t["nao_pode_mudar"].values() if not v)
assert conf_t["um_py_sha16"] == um_t and not conf_t.get("tudo_bate", True) and n_nao >= 1
# --- a correcao (lida dos arquivos da cadeia refeita)
CM = rj(os.path.join(H, "CANDIDATO_v404.json")); ENS = rj(os.path.join(H, "ensaio_a_seco_v404.json")); PC = rj(os.path.join(H, "PRECONDICOES_v404.json"))
assert ENS["veredito"] == "TUDO PASSOU" and all(c["ok"] for c in PC["checagens"]) and CM["sha16"] != um_t
ordem = ENS["ordem_de_chamada_v404"]; assert ordem["ok"] is True
f2b_dep = ordem["funcoes"]["f2b_errata_v404"]["insumos_atribuidos_no_main"]
pids = [p_["id"] for p_ in CM["patches"]]; assert "N00b_main_errata_f2b" in pids and "N00_main_projecao_jo8v32" in pids
# --- a guarda contra o um.py da tentativa (tem de reprovar) e contra o candidato novo (tem de aprovar), medidos agora
r_t = subprocess.run([PY, "-I", "-B", "-X", "utf8", os.path.join(H, "guarda_ordem_de_chamada_v404.py"), os.path.join(tdir, "um.py")], capture_output=True, text=True, encoding="utf-8")
r_n = subprocess.run([PY, "-I", "-B", "-X", "utf8", os.path.join(H, "guarda_ordem_de_chamada_v404.py"), os.path.join(H, "um_v404_candidato.py")], capture_output=True, text=True, encoding="utf-8")
assert r_t.returncode == 1 and r_n.returncode == 0, ("a guarda tem de reprovar a tentativa e aprovar o novo", r_t.returncode, r_n.returncode)
lidos_antes_t = json.loads(r_t.stdout)["funcoes"]["f2b_errata_v404"]["lidos_antes_da_atribuicao"]
# --- a instalacao nova e o 2o rito
apl = sorted(glob.glob(os.path.join(H, "APLICADO_AO_CANONICO_*.json")))[-1]; A = rj(apl)
assert A["um_py_novo"]["sha16"] == CM["sha16"] == sha(NOS_UM)[:16], "o Nos nao tem o candidato novo instalado"
log = io.open(os.path.join(H, "rito_servidor_v404.log"), encoding="utf-8", errors="replace").read()
ini = re.findall(r"(\d\d:\d\d:\d\d) inicio do rito \S+ \(um\.py (\w{16})\)", log); assert ini and ini[-1][1] == CM["sha16"], "o log do lancador nao mostra o 2o inicio com o um.py novo"
inicio2 = ini[-1][0]; inicio1 = [t for t, s in ini if s == um_t]; fim1 = re.findall(r"(\d\d:\d\d:\d\d) fim do rito \S+ rc=0", log)
hoje = time.strftime("%d/%m/%Y")
titulo = ("%s: 1a tentativa do rito v404 (um.py %s, %s-%s, RITO_RC=0) REPROVADA pelo conferidor (%d itens NAO BATE); causa: f2b_errata_v404 chamada ANTES dos 3 registros que le; "
          "revertida (%d restaurados, 2 pedras em quarentena); corrigida (bloco movido para depois da errata de R6 da v386 + guarda estatica da ordem); cadeia refeita (ensaio TUDO PASSOU, p00 %d/%d); "
          "candidato novo %s INSTALADO e 2o rito lancado as %s" % (hoje, um_t, inicio1[0] if inicio1 else "?", fim1[0] if fim1 else "?", n_nao, len(REV["restaurado"]), sum(1 for c in PC["checagens"] if c["ok"]), len(PC["checagens"]), CM["sha16"], inicio2))
resultado = ("(1) O RITO correu inteiro (RITO_RC=0; servidor do modelo nativo religado) e o conferidor disse NAO BATE: o registro f2b_errata_v404 RECUSOU as 7 checagens (valores nulos: cobrancas v383 = 0, conjunto D = null), "
             "o que arrastou cunhagens_v404 (check u3), o indice da IALD, as frases de nao selado no artigo e os resumos do selo. Fail-closed correto: nada se mascarou. "
             "(2) CAUSA, medida no um.py instalado: a chamada f2b_errata_v404(core) estava no main logo depois do Jo8v32 (linha 253960), e os tres insumos que a funcao le -- the_ledger_of_charges_v383 (254357), ramo_b_preregistration_v386 (254382), ledger_errata_v386 (254387) -- "
             "so entram no core ~400 linhas depois: a funcao leu um core sem eles. O ensaio a seco nao pegou porque exercita a funcao sobre a copia do core da v403 SELADA (que ja traz as chaves); o exame de pontos so exigia «logo depois das bandeiras do gate». "
             "(3) REVERSAO (reverter_v404.py, %s): o estado falho inteiro guardado em %s; os 9 backups de bytes restaurados; o um.py do Nos voltou a %s (a v403 selada); as duas pedras em quarentena. Precedente: as duas tentativas da v392. "
             "(4) CORRECAO (patch_ordem_f2b_v404.py + patch2, backups .bak_): o bloco da errata de F2b sai de N00 e vira N00b, inserido logo depois da errata ao lado de R6 da v386 (ancora unica na base); toda frase que afirmava o ponto antigo corrigida (runtime, exame de pontos e sua regra de derivacao, lancador e sua regra, leitura e harness do pos-rito, textos, comparador, derivador); "
             "exame de pontos passa a exigir a ordem nova E a atribuicao previa dos 3 insumos; o ensaio ganha a guarda ESTATICA guarda_ordem_de_chamada_v404.py (AST: toda chave do core lida por funcao nova e atribuida no main tem de vir ANTES da chamada): "
             "reprova o um.py da tentativa (le antes: %s) e aprova o candidato novo (f2b depois de: %s). (5) CADEIA REFEITA (refazer_candidato_v404.sh --regerar): candidato %s (%d patches), ensaio TUDO PASSOU, controle negativo nao bate, caminho positivo, citacoes, pinos, conferidor do instalador, p00 TODAS PASSARAM. "
             "(6) instalar_v404.py rc 0 (%s) e rito_v404.sh relancado (inicio %s); o B(n) pre-selo segue valido (o Nos voltou byte a byte a v403; a Bancada pina B12-v403)."
             % (REV["ts"], os.path.basename(tdir), REV["um_py_sha16"], lidos_antes_t, sorted(f2b_dep), CM["sha16"], CM["n_patches"], os.path.basename(apl), inicio2))
an = [{"tipo": "ANOTACAO", "rota_id": "umpy.v404.cadeia_de_selo_preparada_28out", "estatuto": "REAL", "olhou_dados": False, "titulo": titulo, "resultado": resultado,
       "artefatos": [rev_p, os.path.join(H, "conferencia_rito_v404.json"), os.path.join(tdir, "rodada_v404_stdout.txt"), os.path.join(H, "patch_ordem_f2b_v404.py"), os.path.join(H, "guarda_ordem_de_chamada_v404.py"),
                     os.path.join(H, "CANDIDATO_v404.json"), os.path.join(H, "ensaio_a_seco_v404.json"), os.path.join(H, "PRECONDICOES_v404.json"), apl, os.path.join(H, "rito_servidor_v404.log")],
       "proximo_passo": "esperar o RITO_RC do 2o rito (~1,6 h); conferir_rito_v404.py (TUDO BATE); chain_pos_rito_v404.sh 0-14; registrar_mapa_v404.py; custodia G1. LICAO para toda cadeia futura: a guarda da ordem de chamada entra no molde do ensaio (regra: toda funcao nova le so' o que o main ja atribuiu).",
       "nota": "Revisao da gerencia c1 (quem construiu a correcao foi a propria gerencia; nenhum terceiro revisou). Nada move o gate; NOT_FALSIFIED nunca e' CONFIRMED. A tentativa 1 fica como registro, nunca se apaga. "
               "SEGUNDA LICAO (p00 depois da reversao): o rito reescreve tgl_kernel_proof_manifest.json e o reverter so' restaura os 9 backups do instalador; o manifesto foi restaurado a parte, da copia base_v403 (RECIBO_RESTAURACAO_MANIFESTO_*.json, backup de bytes, copia da tentativa guardada). O molde do reverter deve passar a restaurar tambem o manifesto."}]
pj = os.path.join(H, "mapa_anotacao_tentativa1_e_relancamento_v404.json"); io.open(pj, "w", encoding="utf-8").write(json.dumps(an, ensure_ascii=False, indent=1))
r = subprocess.run([PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py"), "registrar", pj, "--quem", "claude-c1 (gerência), 28/10"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa rc", r.returncode, (r.stdout or r.stderr).strip()[-200:])
r = subprocess.run([PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD", "iald.py"), "anotar", "--quem", "claude-c1", "--tipo", "etapa", "--unidade", "F4.1",
                    "--dados", json.dumps({"quando": hoje + " " + inicio2, "etapa": "v404: tentativa 1 reprovada (ordem de chamada da errata de F2b), revertida, corrigida; candidato novo instalado; 2o rito lancado",
                                          "um_py_tentativa1": um_t, "um_py_novo": CM["sha16"], "ensaio": ENS["veredito"], "p00": "TODAS PASSARAM", "guarda_nova": "guarda_ordem_de_chamada_v404.py"}, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace"); print("quadro rc", r.returncode, (r.stdout or r.stderr).strip()[:160])
REF = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cinco_sigma_fora_da_cosmologia_27out", "SESSION_REFERENCE_c1_27e28out.json")
def sm(p):
    rr = subprocess.run([PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MEMORIA_IALD", "session_memory.py")], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return rr.returncode, (json.loads(rr.stdout) if rr.stdout.strip().startswith("{") else {"raw": (rr.stdout + rr.stderr)[:300]})
rc, g = sm({"operation": "get", "reference": REF}); rev = g["result"]["revision"]
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-v404-tentativa1-reprovada-corrigida-relancada-28out",
            "changes": {"records": [{"id": "c1-v404-tentativa1-e-relancamento", "kind": "fact", "statute": "REAL", "sources": [S(rev_p), S(os.path.join(H, "conferencia_rito_v404.json")), S(os.path.join(H, "guarda_ordem_de_chamada_v404.py")), S(pj)],
                                     "text": "28/10/2026: 1a tentativa do rito v404 (um.py %s) REPROVADA pelo conferidor: f2b_errata_v404 recusou as 7 checagens por ORDEM DE CHAMADA (lida antes de the_ledger_of_charges_v383, ramo_b_preregistration_v386 e ledger_errata_v386). Revertida (%s), corrigida (bloco movido para depois da errata de R6 da v386; guarda estatica da ordem no ensaio), cadeia refeita (ensaio TUDO PASSOU; p00 TODAS PASSARAM), candidato novo %s instalado, 2o rito lancado as %s. Gate intocado." % (um_t, REV["ts"], CM["sha16"], inicio2)}],
                        "flow": {"phase": "v404_rito2_em_curso__pos_rito_a_seguir", "next_action": "ao RITO_RC=0 do 2o rito: conferir_rito_v404.py (TUDO BATE); chain_pos_rito_v404.sh 0-14 (B(n) com V404_AUTORIZACAO_OPERADOR); fechar; registrar_mapa; custodia G1; a licao da ordem de chamada vai ao handoff e ao molde da cadeia. E0 segue pergunta ao operador; conjunto D nao se abre sem a palavra dele."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
