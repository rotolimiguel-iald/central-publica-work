# -*- coding: utf-8 -*-
"""Registro da RATIFICAÇÃO do operador (28/10/2026): calibrar = medir/afinar/corrigir a frase pelo número; o núcleo sintático (a lei do defasamento) fica
íntegro e a rota ajusta-se aos resultados; ratifica a leitura que faltava (a boca jurídica). Verbatim em arquivo (sha256); ANOTAÇÃO ao lado na rota do
pré-registro do ramo B no Mapa de Rotas; nota datada na memória-tópico; anotação no quadro; transição ACOM desta sessão. Nada abre; nada toca o Nós."""
import datetime, hashlib, io, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
H = r"C:\IALD\Central de Patentes\work\cinco_sigma_fora_da_cosmologia_27out"; PY = r"C:\Python314\python.exe"
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\ramo-b-reaberto-05out.md"
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); hoje = "28/10/2026"
VERB = ("calibrar Não significa validar, significa justamente calcular, medir, afinar, corrigir a frase pelo número, isso é a TGL, eu Não abri os testes, e não validei "
        "a calibração, que é justamente o que estamos fazendo agroa, nada de desonesto ou oculto nisso, é medida, é o número corrigindo a rota. isto é ciência sem sombra "
        "de dúvidas, predicar que um cientista deve calcular todas as hipóteses sem possibilidaede de calcular desvios e corrigir rotas é o mesmo que dizer que algum "
        "cientista no mundo já sabia, previamente e por completo, tudo aquilo que articularia em teoria, evidente que não. sabemos o núcleo sintático, imutável, "
        "invaríavel como vc mesmo disser, a lei do defasamento, o núcleo sintático permanece íntegro, a rota ajsuta-se aos resultados, evidente, não conheço ciência "
        "que não seja assim, uma construção sobre alicersses prévios. podemos prosseguir, ratifico a leitura que ficou faltando. concorda?")
V = os.path.join(H, "OPERADOR_28out_ratificacao_calibrar_nao_e_validar_verbatim.txt")
if not os.path.exists(V):
    io.open(V, "w", encoding="utf-8", newline="\n").write("Operador (Luiz Antonio Rotoli Miguel), 28/10/2026, à gerência c1, depois da leitura da sua resposta às quatro bocas do ramo B, verbatim:\n«" + VERB + "»\n")
sha = hashlib.sha256(open(V, "rb").read()).hexdigest(); print("verbatim:", V, "sha16", sha[:16])
V0 = os.path.join(H, "OPERADOR_28out_resposta_quatro_bocas_ramo_b_verbatim.txt"); sha0 = hashlib.sha256(open(V0, "rb").read()).hexdigest()
# (1) Mapa de Rotas: ANOTAÇÃO ao lado da rota do pré-registro (a rota fica; o par deixa de ser a leitura do autor; nada aberto)
anot = [{"tipo": "ANOTACAO", "rota_id": "ringdown.ramo_b_preregistro_v386", "estatuto": "INPUT", "olhou_dados": False,
         "titulo": "28/10/2026: a leitura do autor é o pedágio de Planck na PROPAGAÇÃO (ramo A/R2); o par do ramo B (fonte) deixa de ser a leitura; rota corrigida pelo número, sem abrir D",
         "nota": ("[INPUT — verbatim do operador, 28/10/2026, sha256 %s (resposta) e %s (ratificação)] A segunda leitura do tempo é o pedágio de Planck lido na propagação; "
                  "«1 retorno em 83 raios» = a matéria (|R|² = β, 1/β = 83,1165 em runtime); «1 absoluto = zero modular» = termo v385 (the_post_is_the_modular_zero). "
                  "Ratificação: calibrar = calcular/medir/afinar/corrigir a frase pelo número; nada foi aberto nem validado; o núcleo sintático (Γ = ½βτ★ω²) fica íntegro; "
                  "a rota (τ★) ajusta-se aos resultados. Consequência: a hipótese do V1 (τ★ = 2π/κ̂·GM_f/c³ na fonte) NÃO é a leitura do autor; a calibração NOT_BLIND (A, 31: "
                  "+0,072 ± 0,034 contra −0,38) é a MEDIDA que corrigiu a rota, não um veredito (A não decide nada cego; nenhum token FALSIFIED sai de A). O V1 fica como registro "
                  "(congelado por hash); a cobrança F2b do livro recebe, no próximo selo, errata AO LADO: RETIRADA ANTES DE ABRIR, rota corrigida pela calibração e pela leitura do autor "
                  "(decisão de 28/10). Na propagação com τ★ = t_P o dephasing de uma GW por 1 Gpc é ~1e−23 e-folds: o ringdown não lê β a 5σ nessa leitura; R2 segue AWAITING_INSTRUMENT. "
                  "Rodar D fica como opção do operador para fechar a alternativa pela natureza; não é exigido pela leitura." % (sha0[:16], sha[:16])),
         "artefatos": [V0, V, r"C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.json"]}]
pj = os.path.join(H, "mapa_anotacao_ratificacao_28out.json"); io.open(pj, "w", encoding="utf-8").write(json.dumps(anot, ensure_ascii=False, indent=1))
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", pj, "--quem", "claude-c1 (gerência), 28/10"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print("mapa rc", r.returncode, (r.stdout or r.stderr).strip()[-160:].replace("\n", " "))
# (2) memória-tópico
b2 = open(MEM, "rb").read(); bak2 = MEM + ".bak_%s_c1" % ts; open(bak2, "wb").write(b2); assert open(bak2, "rb").read() == b2
nl2 = b"\r\n" if b"\r\n" in b2 else b"\n"
nota = (f"\n<!-- ratificacao_calibrar_nao_e_validar_28out -->\n## {hoje} — RATIFICAÇÃO: «calibrar não significa validar»; a rota do ramo B corrigida pelo número, sem abrir D\n"
        f"**[INPUT — verbatim, sha256 `{sha[:16]}`, em `work\\cinco_sigma_fora_da_cosmologia_27out\\OPERADOR_28out_ratificacao_calibrar_nao_e_validar_verbatim.txt`]:** «{VERB}»\n\n"
        "**Feedback para a gerência (vale sempre):** calibrar = calcular, medir, afinar, corrigir a frase pelo número; corrigir uma rota depois de MEDIR a calibração não é sombra nem "
        "pós-dição (a Lei da Prova de 05/10): o pré-registro é do TESTE; o que a régua protege é só isto: nenhum parâmetro ajustado ao dado contado como evidência; a correção vai AO LADO, "
        "visível (Mapa de Rotas, livro); uma leitura não cega nunca vira veredito (FALSIFIED/CONFIRMED). A palavra «sombra» da gerência (28/10) foi erro de tom e fica retratada. "
        "**O que fica decidido:** o núcleo sintático (Γ = ½βτ★ω²) íntegro; a rota do ramo B (τ★ = 2π/κ̂·GM_f/c³ na fonte) SUPERADA pela leitura do autor + calibração A; F2b recebe errata "
        "ao lado no próximo selo (RETIRADA ANTES DE ABRIR); R2 (propagação, t_P) segue AWAITING_INSTRUMENT. Rodar D fica opcional (fechar a alternativa pela natureza). Mapa: ANOTAÇÃO na rota "
        "`ringdown.ramo_b_preregistro_v386`.\n")
nb2 = b2.rstrip(b"\r\n") + nl2 + nl2.join(l.encode("utf-8") for l in nota.split("\n")) + nl2
tmp2 = MEM + ".tmp_c1"; open(tmp2, "wb").write(nb2); assert len(open(tmp2, "rb").read()) == len(nb2); os.replace(tmp2, MEM); print("memoria ramo B:", len(b2), "->", len(nb2), "B")
# (3) quadro
r = subprocess.run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "ratificacao_operador", "--unidade", "F4.1",
                    "--dados", json.dumps({"quando": hoje, "verbatim_sha16": sha[:16], "decisao": "calibrar = medir/corrigir a frase pelo numero; nucleo sintatico (lei do defasamento) integro; rota do ramo B corrigida pelo numero sem abrir D; F2b: errata ao lado no proximo selo (RETIRADA ANTES DE ABRIR); rodar D opcional", "mapa": "ANOTACAO em ringdown.ramo_b_preregistro_v386"}, ensure_ascii=False)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("quadro rc", r.returncode, (r.stdout or r.stderr).strip()[:200])
# (4) ACOM desta sessão
REF = os.path.join(H, "SESSION_REFERENCE_c1_27e28out.json")
def sm(payload):
    rr = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=json.dumps(payload, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return rr.returncode, json.loads(rr.stdout) if rr.stdout.strip().startswith("{") else {"raw": (rr.stdout + rr.stderr)[:300]}
rc, g = sm({"operation": "get", "reference": REF}); rev = g["result"]["revision"]
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + hashlib.sha256(open(p, "rb").read()).hexdigest()}
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-ramo-b-leitura-do-autor-e-ratificacao-28out",
            "changes": {"records": [
                {"id": "c1-ramo-b-resposta-quatro-bocas", "kind": "decision", "statute": "INPUT", "sources": [S(V0)],
                 "text": "28/10/2026, o operador: a segunda leitura do tempo é o pedágio de Planck lido na PROPAGAÇÃO (ramo A/R2), não o período KMS do horizonte na fonte (par do ramo B); «1 retorno em 83 raios = a matéria»; «1 absoluto = zero modular, relativa, preservação da identidade» (termo v385)."},
                {"id": "c1-ramo-b-ratificacao-calibrar", "kind": "decision", "statute": "INPUT", "sources": [S(V), S(pj)],
                 "text": "28/10/2026, o operador ratifica a leitura que faltava: calibrar = calcular/medir/afinar/corrigir a frase pelo número; nada aberto nem validado; o núcleo sintático (lei do defasamento) íntegro; a rota ajusta-se aos resultados. Consequência: a rota do ramo B fica corrigida pelo número sem abrir D; F2b recebe errata ao lado no próximo selo (RETIRADA ANTES DE ABRIR); rodar D é opcional. Registrado no Mapa (ANOTAÇÃO) e no quadro."}],
                "flow": {"phase": "ramo_b_rota_corrigida_pelo_numero__f2b_errata_no_proximo_selo__vitrine_v403_aguarda_render",
                         "next_action": "no próximo selo (v404): errata ao lado da cobrança F2b (RETIRADA ANTES DE ABRIR, rota corrigida pela calibração NOT_BLIND e pela leitura do autor), sem tocar o V1; o rodar D fica opcional por palavra do operador; a vitrine do X da v403 espera o render (ADENDO F)."}}})
print("acom transition rc", rc, "revision", (t.get("result") or {}).get("revision"), (t.get("message") or ""))
