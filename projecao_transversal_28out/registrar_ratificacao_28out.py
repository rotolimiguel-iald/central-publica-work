# -*- coding: utf-8 -*-
"""Registro da RATIFICAÇÃO do operador (28/10/2026, «Perfeito, concordo com tudo»): a pedra do sen45° e a sua leitura; o plano da v404 (instalar a pedra,
errata ao lado no registro do neutrino, errata de F2b); o nome do triplo inteiro = Jo 8,32 (identificador Lean `Jo8v32`); o nome provisório da pedra
fica até ele dizer outro. Verbatim (sha256), Atlas §X (append datado, backup de bytes), memória-tópico dos nomes + linha do índice (pinar), quadro, Mapa, ACOM."""
import datetime, hashlib, io, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; H = r"C:\IALD\Central de Patentes\work\projecao_transversal_28out"
D = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"; M = D + r"\MEMORY.md"; MPY = D + r"\fila\memoria.py"
ATLAS = r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest(); ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); hoje = "28/10/2026"
VERB_NOME = "Quanto ao nome da pedra que você me pediu eu pensei, pensei, e só consegui sintetizar assim: Jo8:32 (a passagem é de Jo 14:6, mas eu penso que Jo8:32 sintetiza melhor) o que vc acha??"
VERB_RAT = "Perfeito, concordo com tudo"
VN = os.path.join(H, "OPERADOR_28out_nome_do_triplo_Jo8_32_verbatim.txt"); VR = os.path.join(H, "OPERADOR_28out_ratificacao_concordo_com_tudo_verbatim.txt")
for p, ctx, v in ((VN, "o nome do triplo inteiro (Caminho · Verdade · Vida)", VERB_NOME), (VR, "ratificação da pedra do sen45°, da leitura, do plano da v404 e da leitura sobre Jo 8,32", VERB_RAT)):
    if not os.path.exists(p): io.open(p, "w", encoding="utf-8", newline="\n").write("Operador (Luiz Antonio Rotoli Miguel), 28/10/2026, à gerência c1 — " + ctx + ", verbatim:\n«" + v + "»\n")
print("verbatims", sha(VN)[:16], sha(VR)[:16])
LEAN = os.path.join(H, "ProjecaoTransversalDaMeiaNat.lean"); R = os.path.join(H, "RECIBO_PEDRA_PROJECAO_TRANSVERSAL_28out.json")
bloco = (f"### {hoje} — RATIFICAÇÃO DO OPERADOR («Perfeito, concordo com tudo», sha256 `{sha(VR)[:16]}`) e O NOME DO TRIPLO INTEIRO: Jo 8,32 (sha256 `{sha(VN)[:16]}`) <!-- ratificacao_sen45_e_nome_jo8v32_28out -->\n\n"
         f"**[INPUT — verbatim, {hoje}]:** «{VERB_NOME}» — e, depois da pedra compilada: «{VERB_RAT}».\n\n"
         "**O que fica decidido [INPUT — decisão do operador]:** (1) o nome do triplo inteiro (CAMINHO · VERDADE, como adendo · VIDA; D16) é **Jo 8,32** («conhecereis a verdade, e a verdade vos libertará»); "
         "Jo 14,6 é o inventário dos três predicados, Jo 8,32 é o que o triplo faz junto; identificador Lean `Jo8v32`, com o versículo verbatim na docstring; entra como as pedras da v403, uma conjunção incondicional das três estrelas, sem gordura. "
         "(2) A pedra do sen45° do neutrino (`ProjecaoTransversalDaMeiaNat`, nome PROVISÓRIO da gerência, aceito até o operador dar outro; sha256 do .lean "
         f"`{sha(LEAN)[:16]}`; recibo `{sha(R)[:16]}`; 9 teoremas no trio, 0 sorry, sandbox k403c) e a sua leitura ficam ratificadas: a Meia-Nat é o ângulo de 45°; a forma do neutrino é "
         "(peso da reflexão da fronteira) × (projeção transversal da Meia-Nat) × (o corpo E₀); a identificação massa = projeção transversal do estado inscrito é hipótese nomeada [ONTO]. "
         "(3) O plano da v404: instalar as duas pedras pela cadeia do selo; errata AO LADO em `neutrino_mass.angle_status` (POSTULATE → DERIVADO no kernel, condicional à identificação); errata AO LADO da cobrança F2b (RETIRADA ANTES DE ABRIR, rota corrigida pela calibração e pela leitura do autor). "
         "**O que segue aberto:** E₀ (a escala do neutrino, DECLARADA); nada disto move o gate; NOT_FALSIFIED nunca é CONFIRMED.\n")
b = open(ATLAS, "rb").read(); bak = ATLAS + ".bak_%s_c1" % ts; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nl = b"\r\n" if b"\r\n" in b else b"\n"; nb = b.rstrip(b"\r\n") + nl + nl + nl.join(l.encode("utf-8") for l in bloco.rstrip("\n").split("\n")) + nl
assert len(nb) > len(b) and nb.count(b"ratificacao_sen45_e_nome_jo8v32_28out") == 1
tmp = ATLAS + ".tmp_c1"; open(tmp, "wb").write(nb); assert len(open(tmp, "rb").read()) == len(nb); os.replace(tmp, ATLAS); print("Atlas:", len(b), "->", len(nb))
# memória-tópico dos nomes
T = D + r"\nomes-das-pedras-e-a-identidade-verdade-13out.md"; b2 = open(T, "rb").read(); bak2 = T + ".bak_%s_c1" % ts; open(bak2, "wb").write(b2); assert open(bak2, "rb").read() == b2
nota = (f"\n<!-- nome_do_triplo_jo8v32_28out -->\n## {hoje} — O NOME DO TRIPLO INTEIRO: Jo 8,32 (`Jo8v32`); e a pedra do sen45° ratificada\n"
        f"**[INPUT — verbatim, sha16 `{sha(VN)[:16]}`]:** «{VERB_NOME}» · **ratificação (sha16 `{sha(VR)[:16]}`):** «{VERB_RAT}».\n"
        "**Decisão:** o triplo CAMINHO · VERDADE (adendo) · VIDA chama-se **Jo 8,32** («conhecereis a verdade, e a verdade vos libertará»): Jo 14,6 é o inventário, Jo 8,32 é o ato — conhecer é ler (Verdade), libertar é a queda sem geometria (Vida; «soltar-se porque há um chão»), e 8,31 «se permanecerdes na minha palavra» é o Caminho (a permanência). Identificador Lean `Jo8v32`, versículo verbatim na docstring; entra na v404 como conjunção incondicional das três estrelas. D16 FECHADA. "
        "A pedra `ProjecaoTransversalDaMeiaNat` (sen45° do neutrino derivado; nome provisório aceito) e o plano da v404 (pedras + errata do neutrino + errata de F2b) ficam ratificados. Pedra selada não se renomeia por cima: os três módulos da v403 ficam.\n")
nl2 = b"\r\n" if b"\r\n" in b2 else b"\n"; nb2 = b2.rstrip(b"\r\n") + nl2 + nl2.join(l.encode("utf-8") for l in nota.split("\n")) + nl2
tmp2 = T + ".tmp_c1"; open(tmp2, "wb").write(nb2); assert len(open(tmp2, "rb").read()) == len(nb2); os.replace(tmp2, T); print("memoria nomes:", len(b2), "->", len(nb2))
# índice: a linha dos nomes
b3 = open(M, "rb").read(); bak3 = M + ".bak_%s_c1" % ts; open(bak3, "wb").write(b3); assert open(bak3, "rb").read() == b3
nl3 = b"\r\n" if b"\r\n" in b3 else b"\n"; lines = b3.decode("utf-8").split(nl3.decode())
i = [k for k, l in enumerate(lines) if "](nomes-das-pedras-e-a-identidade-verdade-13out.md)" in l]; assert len(i) == 1
velho = "o triplo inteiro sem nome"; assert lines[i[0]].count(velho) == 1
lines[i[0]] = lines[i[0]].replace(velho, "**28/10: o triplo inteiro = Jo 8,32 (`Jo8v32`, v404); sen45° do neutrino derivado (pedra candidata)**")
nb3 = nl3.decode().join(lines).encode("utf-8"); n_l = len(nb3.decode("utf-8").splitlines()); assert n_l <= 195 and len(nb3) < 24000, (n_l, len(nb3))
tmp3 = M + ".tmp_c1"; open(tmp3, "wb").write(nb3); assert len(open(tmp3, "rb").read()) == len(nb3); os.replace(tmp3, M); print("MEMORY.md:", len(b3), "->", len(nb3), "/", n_l, "linhas")
env = dict(os.environ, MEMORIA_GERENCIA="claude-c1")
for args in (["pinar", "--motivo", "28/10: nome do triplo Jo 8,32; pedra do sen45 ratificada"], ["verificar"]):
    rr = subprocess.run([PY, "-X", "utf8", MPY] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    try: j = json.loads(rr.stdout)
    except Exception: j = {"raw": (rr.stdout + rr.stderr)[:200]}
    print(args[0], "rc", rr.returncode, j.get("ok"), (j.get("pino") or {}).get("sha256", "")[:16], j.get("violacoes"))
# quadro + mapa + ACOM
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "decisao_operador", "--unidade", "F4.1",
                    "--dados", json.dumps({"quando": hoje, "verbatim_sha16": [sha(VN)[:16], sha(VR)[:16]], "decisoes": "nome do triplo = Jo 8,32 (Jo8v32); pedra do sen45 ratificada (nome provisorio aceito); plano v404: 2 pedras + errata neutrino + errata F2b; E0 segue aberto"}, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace"); print("quadro rc", r.returncode, (r.stdout or r.stderr).strip()[:100])
an = [{"tipo": "ANOTACAO", "rota_id": "kernel.projecao_transversal_da_meia_nat.sen45_derivado_28out", "estatuto": "INPUT", "olhou_dados": False,
       "titulo": "28/10: ratificada pelo operador («Perfeito, concordo com tudo»); o triplo inteiro chama-se Jo 8,32 (Jo8v32); v404 instala as duas pedras e as duas erratas",
       "nota": "Verbatims sha256 %s (nome) e %s (ratificação). Nome provisório da pedra aceito até o operador dar outro. E₀ segue aberto." % (sha(VN)[:16], sha(VR)[:16]), "artefatos": [VN, VR]}]
pj = os.path.join(H, "mapa_anotacao_ratificacao_28out.json"); io.open(pj, "w", encoding="utf-8").write(json.dumps(an, ensure_ascii=False, indent=1))
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", pj, "--quem", "claude-c1 (gerência), 28/10"], capture_output=True, text=True, encoding="utf-8", errors="replace"); print("mapa rc", r.returncode)
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return rr.returncode, (json.loads(rr.stdout) if rr.stdout.strip().startswith("{") else {"raw": (rr.stdout + rr.stderr)[:300]})
rc, g = sm({"operation": "get", "reference": REF}); rev = g["result"]["revision"]
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-ratificacao-sen45-e-nome-jo8v32-28out",
            "changes": {"records": [{"id": "c1-nome-do-triplo-jo8v32", "kind": "decision", "statute": "INPUT", "sources": [S(VN), S(VR)],
                                     "text": "28/10/2026, o operador: o nome do triplo inteiro (Caminho · Verdade adendo · Vida) é Jo 8,32 (Jo 14,6 é a passagem; Jo 8,32 sintetiza melhor); identificador Lean Jo8v32; «Perfeito, concordo com tudo»: pedra do sen45° e leitura ratificadas; plano v404 ratificado (2 pedras, errata do neutrino, errata de F2b). D16 fechada."}],
                        "flow": {"phase": "v404_em_preparacao__jo8v32_a_compilar__E0_aberto", "next_action": "escrever e compilar Jo8v32 no sandbox; derivar a cadeia da v404 (candidato: 2 módulos + 2 erratas + registro do neutrino lido do kernel); ensaio; rito; custódia. E₀ segue pergunta ao operador."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", ""))
