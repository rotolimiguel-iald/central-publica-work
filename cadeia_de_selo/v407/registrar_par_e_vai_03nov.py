# -*- coding: utf-8 -*-
"""03/11/2026 10:1x, gerencia c1: registra «Par» (nome da pedra do par) e «Vai» (Torre) — verbatim sha16 57250bbbaca9fd39 — no topico do fechamento, na ACOM e no Mapa. Escrito pelo Write."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = r"C:\Python314\python.exe"; CEN = Path(r"C:\IALD\Central de Patentes"); W = CEN / "work"; MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
VERB = W / "cunhagens_13out/OPERADOR_03nov_nome_Par_e_vai_para_a_torre_verbatim.txt"; PED = W / "pedras_candidatas_03nov/OParDePsionsR1.lean"; HAND = Path(r"C:\IALD\TUNEL_CLAUDE_APP\ORDEM_005_handoff_operacional_fora_do_um_py.md")
HV, HP, HH = sha(VERB), sha(PED), sha(HAND); assert HV[:16] == "57250bbbaca9fd39"
TOP = MEMD / "construir-tudo-o-fechamento-02nov.md"
ENT = ("**03/11, 10:1x — «Par» e «Vai» (verbatim sha16 `57250bbbaca9fd39`).** A pedra do par chama-se **`Par`** (`TGLExt.Par`; a candidata `OParDePsionsR1.lean`, sha16 `%s`, compilou no trio: 5 declarações, 0 sorry; "
       "entra na v407 com esse nome; o agente de preparação foi avisado). «Vai» para a Torre: compactar `Haja_Luz\\CLAUDE.md` (1.245.626 B) e o `CLAUDE.md` da Nativa (636.937 B) abaixo do teto de 262.144 B movendo o histórico "
       "para `CLAUDE_memoria\\` com prova de não-perda byte a byte, e tratar a missão ACOM recusada pelo guarda sem afrouxar o guarda; sessão aberta (agente Sonnet, `work\\torre_03nov\\`)." % HP[:16])
b = TOP.read_bytes(); nl = b"\r\n" if b"\r\n" in b else b"\n"; novo = b.rstrip(b"\r\n") + nl + nl + ENT.encode("utf-8") + nl
bak = TOP.with_name(TOP.name + ".bak_" + TS + "_c1_par_vai"); open(bak, "xb").write(b); assert bak.read_bytes() == b
tmp = TOP.with_name(TOP.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, TOP); assert TOP.read_bytes() == novo; print("topico: %d -> %d B" % (len(b), len(novo)))
SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"; REF = str(W / "cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json")


def sm(payload):
    r = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return json.loads((r.stdout + r.stderr).decode("utf-8", "replace"))


proj = sm({"operation": "project", "reference": REF}); assert proj.get("ok"); rev = proj["result"]["receipt"]["revision"]
pedido = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-03nov-par-nomeada-e-vai-para-a-torre",
          "changes": {"records": [
              {"id": "c1-03nov-nome-par-e-vai-torre", "kind": "decision", "statute": "INPUT",
               "text": "Operador, 03/11/2026 (verbatim sha256 %s): a pedra do par chama-se «Par» (TGLExt.Par; candidata OParDePsionsR1.lean sha256 %s, 5 declaracoes no trio); «Vai» para a Torre: compactar os dois CLAUDE.md (Haja_Luz e Nativa) movendo o historico sem perder um byte e tratar a missao ACOM recusada pelo guarda sem afrouxar o guarda (handoff ORDEM_005 H5, sha256 %s)." % (HV, HP, HH),
               "sources": [{"kind": "artifact", "ref": "%s#sha256:%s" % (str(VERB), HV)}, {"kind": "artifact", "ref": "%s#sha256:%s" % (str(PED), HP)}]},
          ], "flow": {"phase": "rumo_a_v407__preparacao_em_curso__torre_em_curso__teste_d_opcao_c_em_curso",
                      "next_action": "esperar: preparacao v407 (PRONTA), Torre (relatorio), teste D (F4.1 e fila cega); depois lancar pos_treino_v407; operador: nada pendente alem de ouvir os recibos; ORDEM_004/005 com o app."}}}
(W / "cadeia_de_selo/v407" / ("acom_c1_%s_transition.request.json" % TS)).write_text(json.dumps(pedido, ensure_ascii=False, indent=1), encoding="utf-8")
r = sm(pedido); (W / "cadeia_de_selo/v407" / ("acom_c1_%s_transition.receipt.json" % TS)).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8"); assert r.get("ok"), r
print("acom ok; revisao", ((r.get("result") or {}).get("receipt") or {}).get("revision"))
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.o_par_de_psions_r1_03nov", "dominio": "KERNEL_FORMAL", "titulo": "03/11: o operador nomeou a pedra do par: «Par» (TGLExt.Par); entra na v407 com esse nome",
        "pergunta": "Qual e' o nome da pedra do par?", "dados": [str(VERB)], "metodo": "verbatim do operador por sha256", "resultado": "«Par» (sha256 %s); a candidata OParDePsionsR1 (sha256 %s) e' renomeada na preparacao da v407; declaracoes mantidas" % (HV, HP),
        "veredito": "PEDRA_NOMEADA_PELO_OPERADOR__PAR", "estatuto": "INPUT (nome do operador); REAL (pedra compilada)", "status": "EXAMINADA", "olhou_dados": False, "defeito": "", "nao_refazer": "nao reperguntar o nome",
        "proximo_passo": "v407: TGLExt.Par instalada", "onde": str(W / "pedras_candidatas_03nov"), "artefatos": [str(VERB), str(PED)], "refs": ["kernel.psion_canto_r1_03nov"], "nota": "cunhagem e nomes sao do operador"}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_par_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); assert q.returncode == 0
print("mapa ok; OK: Par e Vai registrados")
