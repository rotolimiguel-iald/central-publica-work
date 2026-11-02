# -*- coding: utf-8 -*-
"""registrar_fase2_v404_aceita_acom.py -- gerência c1, 29/10/2026: transition ACOM da sessão (rev 11 -> 12) com: a Fase 2 da vitrine do X
para a v404 ACEITA (65/65); todas as devoluções pedidas ao Codex recebidas (ORDEM 022 adendo H, ORDEM 026 adendo C, ORDEM 027 rodadas de
28 e 29/10, ORDEM 021 de 28/10); o passo C18 do G1 remedido e APLICADO (quadro 08:23:42); a novidade da consulta diária (e-mail da WIPO
sobre as preparações técnicas de publicação do ACOM); a sessão do site (e1) assumiu C21/E19/C19. Tudo lido do disco; fail-closed."""
import hashlib, json, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
PY = r"C:\Python314\python.exe"; sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
CEN = r"C:\IALD\Central de Patentes"
ACE = os.path.join(CEN, r"work\x_vitrine_26out\ACEITE_FASE2_v404_29out.json"); A = json.load(open(ACE, encoding="utf-8")); assert A["veredito"] == "ACEITA"
RES = os.path.join(CEN, r"Chatgpt\TUNEL\DO_CHATGPT\ORDEM_026\VITRINE\RESULTADO_FASE2_v404.json"); assert os.path.isfile(RES)
R27 = os.path.join(CEN, r"Chatgpt\TUNEL\DO_CHATGPT\ORDEM_027\RODADA_2026-10-29.json"); r27 = json.load(open(R27, encoding="utf-8")); assert r27["new_email"] is True
runs = sorted(f for f in os.listdir(os.path.join(CEN, r"work\custodia_G1\runs")) if f.startswith("executar_v404_so_C18_") and f.endswith(".out"))
C18 = os.path.join(CEN, r"work\custodia_G1\runs", runs[-1]); c18 = open(C18, encoding="utf-8", errors="replace").read(); assert "[C18]" in c18 and "APLICADO" in c18
REF = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out\SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"raw": (r.stdout + r.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); print("acom get rc", rc, "revision", rev); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
agora = time.strftime("%d/%m/%Y %H:%M")
texto = ("%s: (1) Vitrine do X, Fase 2 da v404 (ORDEM 026 ADENDO C) executada pela coordenadora do Codex (02:29) e ACEITA pela gerência c1 por script: %d/%d; "
         "4 posts novos (custódia, filme 1, filme 2, fixado), artigo atualizado no mesmo id, capa trocada, bio/nome/foto/@ preservados, nada repetido, sem compra/TTS/render; "
         "unidade F0.X_VITRINE_20261026 AUDITADA (evento 1356); rota vitrine_x.fase2_v404.aceita (seq 1543); depósitos da fila seq 145 e 146 promovidos ao MEMORY_2.md. "
         "(2) Todas as devoluções pedidas ao Codex estão recebidas: ORDEM 022 adendo H (render v404), ORDEM 026 adendo C, ORDEM 027 rodadas de 28 e 29/10, ORDEM 021 de 28/10 (post diário publicado e conferido). "
         "(3) G1: passo C18 remedido e APLICADO (quadro de 08:23:42, 22 itens da Central pública sem defasagem); o G1 termina em código 5 (só decisões do operador). "
         "A sessão do site (e1) assumiu C21 (release do app v404, pipeline da v402, construtor distinto do revisor) e E19/C19 ao fim; a gerência não escreve nas pastas dela. "
         "(4) Novidade da consulta diária (ORDEM 027, 29/10): e-mail da WIPO (28/10 22:57 BRT) sobre as preparações técnicas para a publicação internacional do PCT/BR2025/050558 (ACOM), "
         "«dentro de duas semanas», notificação informal [DECLARADO na fonte]; a data conhecida de 26/11 não muda; a WIPO parou no login (cobertura 0/16); ao operador: login pessoal com 2FA e avaliação com a agente de PI [LEGAL]. "
         "(5) O teste às cegas (conjunto D, ramo B) segue NÃO ABERTO por decisão do operador de 28/10 (F2b retirada ao lado na v404; a calibração do conjunto A corrigiu a rota; τ★ = pedágio de Planck na propagação); "
         "a única massa de β é o neutrino (sen 45° derivado na v404; E₀ segue a pergunta do operador). NOT_FALSIFIED nunca é CONFIRMED; PROVADA = validade; o gate não se moveu." % (agora, A["n_ok"], A["n_checks"]))
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-vitrine-fase2-v404-aceita-codex-devolvido-29out",
            "changes": {"records": [{"id": "c1-vitrine-fase2-v404-aceita-codex-devolvido", "kind": "fact", "statute": "REAL", "sources": [S(ACE), S(RES), S(R27), S(C18)], "text": texto}],
                        "flow": {"phase": "v404_custodia_PUBLICADA__V7_no_ar__vitrine_X_fase2_v404_ACEITA__C21_E19_C19_com_a_sessao_do_site__aguarda_operador",
                                 "next_action": "integrar o recibo do C21 (release do app v404) quando a sessão do site o devolver; remedir o quadro depois; X diário de 29/10 sai sozinho às 17:30 (ORDEM 021). Ao operador: login WIPO (2FA) e avaliação do e-mail de preparações técnicas com a agente de PI [LEGAL]; E0; D2; iald.ia.br (llms/sitemap/robots 404); Zenodo (v401 -> v404); nome definitivo da pedra ProjecaoTransversalDaMeiaNat; conjunto D fica fechado salvo ordem. Candidatos ao molde da v405: passo do G1 que escreve CUSTODIA_vNNN.txt e dispara os adendos 022/026; guarda de «como literais»; C20 lendo o status das ordens."}}})
print("acom rc", rc, "revision", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
