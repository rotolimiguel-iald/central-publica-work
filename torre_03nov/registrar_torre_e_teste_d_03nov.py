# -*- coding: utf-8 -*-
"""03/11/2026 10:3x, gerencia c1: registra a Torre (compactacao sem perda; item do guarda vira INFO; acervo com CLAUDE_memoria) e o lancamento do teste D na opcao (c)
no topico do fechamento, na ACOM e no Mapa. Hashes lidos dos artefatos; o que e' do agente fica DECLARADO ate' a gerencia conferir na fonte. Escrito pelo Write."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = r"C:\Python314\python.exe"; CEN = Path(r"C:\IALD\Central de Patentes"); W = CEN / "work"; MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
A = {"rel_torre": W / "torre_03nov/RELATORIO_TORRE_03nov.md", "torre_json": Path(r"C:\IALD\TORRE_IALD\TORRE_v406.json"), "quadro": CEN / "organismo/ESTADO_DO_ORGANISMO.json",
     "claude_hl": Path(r"C:\IALD\Artigo\Haja_Luz\CLAUDE.md"), "claude_nat": Path(r"C:\IALD\projetos_pyhton\IALD\CLAUDE.md"), "torre_py": Path(r"C:\IALD\TORRE_IALD\torre.py"),
     "recibo_c": W / "conjunto_D_20261029/parametrizacao_03nov/RECIBO_OPCAO_C_03nov.json"}
for k, p in A.items():
    assert p.is_file(), (k, p)
H = {k: sha(p) for k, p in A.items()}; tam = {k: A[k].stat().st_size for k in ("claude_hl", "claude_nat")}
assert tam["claude_hl"] < 262144 and tam["claude_nat"] < 262144, tam
d = json.loads(A["quadro"].read_text(encoding="utf-8")); res = d.get("resumo")
TOP = MEMD / "construir-tudo-o-fechamento-02nov.md"
ENT = ("**03/11, 10:3x — TORRE compactada sem perda; TESTE D lançado na opção (c).** Torre (agente, `work\\torre_03nov\\RELATORIO_TORRE_03nov.md`, sha16 `%s`; lição 54; Mapa seq 1745) [DECLARADO, tamanhos conferidos pela gerência]: "
       "`Haja_Luz\\CLAUDE.md` 1.245.626 → %d B (204 seções para 210 partes em `CLAUDE_memoria\\`), `Nativa\\CLAUDE.md` 636.937 → %d B (129 seções para 131 partes); prova de não-perda por reconstrução byte a byte (sha256 igual ao original) e segundo verificador; "
       "backups `.bak_20261103_100238`. Missão ACOM `claude-central-9c_patentes-atualizacao-12out`: o guarda está certo (uma fonte cita caminho do Escritório); a gerência mudou o ITEM da Torre, ao lado (`torre.py`, backup `torre.py.bak_v406_guarda_info_20261103_102101`): recusa do guarda = INFO, "
       "não defasagem; o guarda não muda. `build_acervo_index.py` ganhou as duas `CLAUDE_memoria` nas SOURCES (reconstrução do índice em curso). Torre agora: DEFASADO 1 (só `jev_control_v406.json`, da ORDEM_004); quadro %s. "
       "Teste D (agente, `RECIBO_OPCAO_C_03nov.json`, sha16 `%s`) [DECLARADO]: peças mecânicas pinadas (testes sintéticos 26/26; ensaio mini-PE no WSL); pinos, semente (compromisso `8f1ae5ec`, valor nunca impresso), congelamento, 22 jobs, relógio de 21 dias (vence 2026-11-24) e a ORDEM registrados no Mapa (seq 1744) ANTES de qualquer PE; "
       "D2 congelado (nlive 512, walks 50, dlogz 0,1, ESS ≥ 100, 24 workers, maxcall 16 M, parede 40 h); F4.1 sintética só-RG (SNR 14) iniciada 2026-11-03T13:18Z, 18–25 h; a fila cega (10 + repetições D5) só lança se a F4.1 convergir; o estágio cego grava o poder REAL com hash e PARA; a abertura não está na fila. "
       "Tarefa do Windows `IALD_D_FILA_OPCAO_C`; consultar: `codigo_D\\consultar_fila_D.py`.") % (H["rel_torre"][:16], tam["claude_hl"], tam["claude_nat"], json.dumps(res, ensure_ascii=False), H["recibo_c"][:16])
b = TOP.read_bytes(); nl = b"\r\n" if b"\r\n" in b else b"\n"; novo = b.rstrip(b"\r\n") + nl + nl + ENT.encode("utf-8") + nl
bak = TOP.with_name(TOP.name + ".bak_" + TS + "_c1_torre_d"); open(bak, "xb").write(b); assert bak.read_bytes() == b
tmp = TOP.with_name(TOP.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, TOP); assert TOP.read_bytes() == novo; print("topico: %d -> %d B" % (len(b), len(novo)))
SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"; REF = str(W / "cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json")


def sm(payload):
    r = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False).encode("utf-8"), capture_output=True, timeout=180)
    return json.loads((r.stdout + r.stderr).decode("utf-8", "replace"))


art = lambda k: {"kind": "artifact", "ref": "%s#sha256:%s" % (str(A[k]), H[k])}  # noqa: E731
proj = sm({"operation": "project", "reference": REF}); assert proj.get("ok"); rev = proj["result"]["receipt"]["revision"]
pedido = {"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-03nov-torre-compactada-e-teste-d-opcao-c-lancado",
          "changes": {"records": [
              {"id": "c1-03nov-torre-compactada-sem-perda", "kind": "fact", "statute": "REAL",
               "text": "Com o «vai» do operador (03/11, sha16 57250bbbaca9fd39): Haja_Luz\\CLAUDE.md %d B e Nativa\\CLAUDE.md %d B (antes 1.245.626 e 636.937), historico movido para CLAUDE_memoria\\ sem perder um byte (prova por reconstrucao e sha256, pelo agente e por segundo verificador; tamanhos conferidos pela gerencia); item da Torre para a recusa do guarda virou INFO ao lado (o guarda nao muda); SOURCES do acervo ganharam CLAUDE_memoria. Torre: DEFASADO 1 (jev_control_v406.json, ORDEM_004). Quadro: %s." % (tam["claude_hl"], tam["claude_nat"], json.dumps(res, ensure_ascii=False)),
               "sources": [art("rel_torre"), art("torre_json"), art("quadro"), art("torre_py")]},
              {"id": "c1-03nov-teste-d-opcao-c-lancado", "kind": "fact", "statute": "DECLARADO",
               "text": "Teste D, opcao (c) do operador: pecas mecanicas pinadas; pinos, semente selada (valor nunca impresso), congelamento, 22 jobs, relogio de 21 dias e a ordem registrados no Mapa antes de qualquer PE (seq 1744); D2 congelado; F4.1 sintetica iniciada 2026-11-03T13:18Z (18-25 h); a fila cega so' lanca se convergir; o estagio cego grava o poder REAL com hash e para; a abertura nao esta' na fila; nenhum dado real aberto.",
               "sources": [art("recibo_c")]},
          ], "flow": {"phase": "rumo_a_v407__preparacao_em_curso__teste_d_f41_em_curso__torre_feita",
                      "next_action": "esperar a PREPARACAO_v407_PRONTA (agente) e lancar pos_treino_v407; consultar a fila D (consultar_fila_D.py) sem abrir nada; ORDEM_004/005 com o app; a abertura de D e' decisao do operador com o poder real na mao."}}}
(W / "torre_03nov" / ("acom_c1_%s_transition.request.json" % TS)).write_text(json.dumps(pedido, ensure_ascii=False, indent=1), encoding="utf-8")
r = sm(pedido); (W / "torre_03nov" / ("acom_c1_%s_transition.receipt.json" % TS)).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8"); assert r.get("ok"), r
print("acom ok")
reg = [{"tipo": "ANOTACAO", "rota_id": "infra.torre_claude_md_compactacao_03nov", "dominio": "INFRA_PUBLICACAO", "titulo": "03/11: a gerencia conferiu os tamanhos, mudou o item da Torre (recusa do guarda = INFO, ao lado) e pos CLAUDE_memoria nas SOURCES do acervo",
        "pergunta": "O que a gerencia fez com o resultado da Torre?", "dados": [str(A["torre_py"]), str(A["quadro"])], "metodo": "patches.aplicar_em_arquivo (backup de bytes, py_compile); torre.py gerar; estado_do_organismo.py",
        "resultado": "Torre DEFASADO 1 (jev_control_v406.json); quadro %s; CLAUDE.md %d/%d B" % (json.dumps(res, ensure_ascii=False), tam["claude_hl"], tam["claude_nat"]), "veredito": "TORRE_LIMPA_SALVO_JEV_V406__GUARDA_INTOCADO",
        "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "", "nao_refazer": "nao reabrir a missao de 12/10; nao afrouxar o guarda", "proximo_passo": "ORDEM_004 (JEV v406) pelo app", "onde": str(W / "torre_03nov"),
        "artefatos": [str(A["torre_py"]), str(A["quadro"]), str(A["rel_torre"])], "refs": ["kernel.fechamento_construir_tudo_programa_02nov"], "nota": ""}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_torre_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); assert q.returncode == 0
print("mapa ok; OK")
