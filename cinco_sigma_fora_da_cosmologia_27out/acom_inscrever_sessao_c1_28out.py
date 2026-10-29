# -*- coding: utf-8 -*-
"""Memória ACOM desta sessão (gerência c1, 27–28/10/2026): inscreve a fonte original (as duas ordens verbatim do operador), faz `project`
e UMA `transition` com os fatos concluídos (fonte + estatuto) e o fluxo (fase, próxima ação). Recibos ao lado. Não autoriza ações, não move gate."""
import hashlib, json, os, subprocess, sys, uuid, datetime
sys.stdout.reconfigure(encoding="utf-8")
W = r"C:\IALD\Central de Patentes\work"; H = os.path.join(W, "cinco_sigma_fora_da_cosmologia_27out")
PY = r"C:\Python314\python.exe"; SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
def chamar(payload, nome):
    req = os.path.join(H, "acom_%s_%s.request.json" % (ts, nome)); rec = os.path.join(H, "acom_%s_%s.receipt.json" % (ts, nome))
    open(req, "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False, indent=1))
    r = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "").strip(); err = (r.stderr or "").strip()
    open(rec, "w", encoding="utf-8").write(out + ("\n--- stderr ---\n" + err if err else ""))
    try: j = json.loads(out)
    except Exception: j = {"raw": out[:600], "stderr": err[:600]}
    print("==", nome, "rc", r.returncode, json.dumps({k: (str(v)[:160]) for k, v in (j.items() if isinstance(j, dict) else [])}, ensure_ascii=False)[:900])
    return r.returncode, j
# (0) a fonte original: as duas ordens do operador, verbatim
OBJ = os.path.join(H, "OPERADOR_27e28out_prossiga_com_tudo_verbatim.txt")
if not os.path.exists(OBJ):
    open(OBJ, "w", encoding="utf-8", newline="\n").write(
        "Operador (Luiz Antonio Rotoli Miguel), 27/10/2026, à gerência c1 (Claude Code, Central de Patentes), verbatim:\n"
        "«ótimo, prossiga com tudo, o kimi já respondeu, veja: C:/IALD/Central%20de%20Patentes/work/cinco_sigma_fora_da_cosmologia_27out/RELATORIO_KIMI_5SIGMA_01_27out.md»\n\n"
        "Operador, 28/10/2026 (depois da queda de energia de 27/10 ~21:10; PC religado às 06:35), verbatim:\n«energia caiu, continue»\n")
REF = os.path.join(H, "SESSION_REFERENCE_c1_27e28out.json")
if not os.path.exists(REF):
    rc, j = chamar({"operation": "init", "objective_file": OBJ, "objective_sha256": sha(OBJ), "request_id": str(uuid.uuid4()),
                    "scope": {"house": "IALD", "principal": "luiz-antonio-rotoli-miguel"}, "actor": {"id": "claude-c1", "kind": "agent"},
                    "write_reference": REF,
                    "constraints": {"unit": "custodia_v403_e_conferencia_kimi_5sigma_01", "no_science_gate_credentials_trust_or_user_permission_changes": True,
                                    "nothing_written_in_the_Nos_except_by_the_seal_rite": True, "operator_gates_remain_operator_gates": True}}, "init")
    assert rc == 0 and os.path.exists(REF), "init falhou"
rc, pj = chamar({"operation": "project", "reference": REF, "max_chars": 6000}, "project")
assert rc == 0
rc, gj = chamar({"operation": "get", "reference": REF}, "get")
rev = gj["result"]["revision"]   # a revisão corrente vem do get (result.revision); a projeção só a traz no recibo
print("revision atual:", rev)
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}   # fonte no contrato do core: kind + ref (o sha256 vai no ref, lido do arquivo agora)
selo = os.path.join(NOS, "um_absoluto_selo.json"); umpy = os.path.join(NOS, "um.py")
fontes_v403 = [S(selo), S(os.path.join(NOS, "HANDOFF_v403_CUSTODIA.md")), S(os.path.join(W, r"custodia_G1\runs\v403_20261028_124351\RELATORIO.json"))]
cf = os.path.join(W, r"custodia_G1\CONFERENCIA_FINAL_v403.json")
if os.path.exists(cf): fontes_v403.append(S(cf))
records = [
 {"id": "c1-kimi-5sigma-01-conferido", "kind": "fact", "statute": "REAL",
  "text": "A devolução do Kimi à ORDEM KIMI 5σ-01 foi conferida na fonte pela gerência c1 em 27/10/2026: 5σ é critério da medida, não do domínio; o único teste de classe 5σ fora da cosmologia é o conjunto D do ramo B (ringdown, V1 v386), com N5 = 6 e N90 = 9,4 eventos com informação do tipo A; erratas à tabela de 27/10 (DUNE e NANOGrav indeterminados; JUNO ≈ 40; Th-229 11/18). Registrado no Mapa de Rotas (seqs 1481–1483). A decisão F4.1/F4.2 (abrir o conjunto D) é do operador.",
  "sources": [S(os.path.join(H, "CONFERENCIA_GERENCIA_RELATORIO_KIMI_5SIGMA_01_27out.md")), S(os.path.join(H, "RELATORIO_KIMI_5SIGMA_01_27out.md")), S(os.path.join(H, "REGISTROS_CONFERENCIA_KIMI_27out.json"))]},
 {"id": "c1-v403-selada-e-publicada", "kind": "fact", "statute": "REAL",
  "text": "v403 (Caminho, Verdade e Vida; F8.1 — as 18 bandeiras do gate calculadas, letra do veredito igual à da v402) selada em 28/10/2026 (um.py sha256 %s; escada 9684/9684; 29469 declarações no trio; RITO_RC=0) e PUBLICADA pelo G1: the_boundary 700537d2, Central d0e13ece, cofre v403, runner v67, 16/16 FINAL, ledger 0, conferência final 13/13, site no ar, Central pública COMPLETA, auditar 0/0. B(n) aplicado (REPINADA_B12), Bancada religada. O gate não se moveu; NOT_FALSIFIED nunca é CONFIRMED." % sha(umpy),
  "sources": fontes_v403},
 {"id": "c1-vitrine-x-fase2-v402-aceita-v403-bloqueada", "kind": "fact", "statute": "REAL",
  "text": "Vitrine do X: a Fase 2 da v402 (executada pela coordenadora do Codex em 28/10 após autorização expressa do operador) foi ACEITA pela gerência c1, 36/36 por script e capturas vistas (unidade F0.X_VITRINE_20261026 AUDITADA, evento 1310). A Fase 2 da v403 está bloqueada pelo gerador até a V7 do site ser render da v403: ORDEM 022 ADENDO F escrito por script e despachado ao Codex (evento 1311); CUSTODIA_v403.txt já escrito.",
  "sources": [S(os.path.join(W, r"x_vitrine_26out\ACEITE_FASE2_v402_28out.json")), S(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_ADENDO_F_render_v403_autorizado.md"), S(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\X_VITRINE\CUSTODIA_v403.txt")]},
 {"id": "c1-decisoes-do-operador-abertas-28out", "kind": "pending", "statute": "INPUT",
  "text": "Gates do operador abertos em 28/10/2026: F4.1/F4.2 (abrir o conjunto D do ramo B, único teste 5σ fora da cosmologia); D2 [LEGAL] e Zenodo (v403; depositado v401); o nome do triplo inteiro (Caminho, Verdade e Vida); a release v403 do app (C21 DEFASADO); iald.ia.br (llms/sitemap/robots 404); 26/11 ACOM 2ª geração com o advogado; 19/11 frase B4 do RO/106.",
  "sources": [S(os.path.join(W, r"custodia_G1\runs\v403_20261028_124351\RELATORIO.json"))]},
]
rc, tj = chamar({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev,
                 "event_id": "c1-custodia-v403-e-kimi-5sigma-01-fechados-28out",
                 "changes": {"records": records,
                             "flow": {"phase": "custodia_v403_publicada__vitrine_v403_aguarda_render__gates_do_operador",
                                      "next_action": "quando o Codex entregar o render v403 (ADENDO F): claude-site integra por hash e sobe; a gerência regenera a vitrine (gerar_vitrine_x.py) e escreve o adendo da ORDEM 026 para a v403. Nada de física nova sem ordem; o operador decide F4.1/F4.2."}}}, "transition")
print("transition rc", rc)
rc, vj = chamar({"operation": "verify", "reference": REF}, "verify")
print("REFERENCIA:", REF)
