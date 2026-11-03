# -*- coding: utf-8 -*-
"""03/11/2026 02:2x: o orquestrador parou em S7 (G1 planejar --seco rc 20: faltavam os sete marcadores opcionais da prosa da custodia no HANDOFF_v406_CUSTODIA.md);
a gerencia anexou os sete textos ao handoff (pos_rito/textos_custodia_handoff_v406_03nov.py: numeros conferidos no core selado; guarda de frases v406 + portao do G1; backup de bytes;
re-lido pelo parser do G1, 7/7, 0 problemas; sha16 do handoff 73f01ac7d4e60a52 -> 7b0548cf47ca2d3d) e relancou a tarefa IALD_pos_treino_v406 (pid 94432, 02:18:31) para o S7
(planejar --seco, executar --publicar, auditar) -> S8 -> S9. Registra a anotacao no Mapa de Rotas (a rota do fechamento), com os artefatos por sha256. Escrito pelo Write."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes"); V6 = CEN / "work/cadeia_de_selo/v406"; NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
rec = json.loads((V6 / "pos_rito/RECIBO_TEXTOS_CUSTODIA_HANDOFF_v406.json").read_text(encoding="utf-8"))
assert rec["sha16_depois"] == s16(NOS / "HANDOFF_v406_CUSTODIA.md"), "o handoff mudou depois do recibo"
assert not rec["parser_g1"]["problemas"] and len(rec["parser_g1"]["corpos"]) >= 10
log = (V6 / "orquestrador/orquestrador.log").read_text(encoding="utf-8", errors="replace")
assert "orquestrador iniciado (pid 94432)" in log, "o relancamento do orquestrador nao esta' no log"
txt = ("v406 pos-rito: o orquestrador parou em S7 (G1 planejar --seco, rc 20) porque o HANDOFF_v406_CUSTODIA.md nao trazia os sete marcadores opcionais da prosa da custodia "
       "(TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN, ARCO_PT, COMMIT; o textos_v406 nao os gera; na v405 a gerencia os anexou a mao). A gerencia anexou os sete textos "
       "ao fim do handoff (numeros lidos do core selado, do selo e do diario e conferidos: 301 modulos, 1794 bandeiras, 8 ancoras, 14 checagens, escada 10066 -> 11860, 33732/26911, pin %s; "
       "guarda de frases v406 e portao do G1: 0 violacoes; ARCO sem aspa simples/<; COMMIT ASCII; sem o 4,44), com backup de bytes (%s); o parser do G1 releu 7/7 corpos, 0 problemas; "
       "sha16 do handoff %s -> %s (o manifesto de incorporacao nao pina o handoff; a mudanca e' ao lado, como na v405). Tarefa IALD_pos_treino_v406 relancada as 02:18:31 (pid 94432) para o S7 "
       "(planejar --seco, executar --publicar, auditar) -> S8 (nativa) -> S9 (relatorio)." % (rec["numeros_lidos"]["pin"], Path(rec["backup"]).name, rec["sha16_antes"], rec["sha16_depois"]))
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL", "titulo": "v406: textos da custodia anexados ao handoff (7 marcadores do G1); orquestrador relancado para S7 (G1 --publicar)",
        "pergunta": "Por que o S7 parou e o que a gerencia fez?", "dados": [str(V6 / "orquestrador/g1_planejar_out.txt"), str(NOS / "HANDOFF_v406_CUSTODIA.md"), str(V6 / "pos_rito/RECIBO_TEXTOS_CUSTODIA_HANDOFF_v406.json")], "olhou_dados": True,
        "metodo": "leitura do g1_planejar_out.txt (rc 20, lista dos marcadores); molde da v405 (blocos no fim do HANDOFF_v405_CUSTODIA.md); custodia_g1/textos.py (NECESSIDADE, portao) e nos.py (RE_MARCADOR, ler_handoff); script com conferencia dos numeros e das guardas antes do acrescimo.",
        "resultado": txt, "veredito": "HANDOFF_COMPLETADO__G1_RELANCADO", "estatuto": "REAL (recibo e log lidos); textos da gerencia c1 em nome proprio", "status": "EM_CURSO",
        "proximo_passo": "esperar S7 (planejar 0/1/5; executar --publicar; auditar), S8 e S9; depois: linha PUBLICADA no indice (ato manual), licoes v406, registro final (Mapa/ACOM/memoria), relatorio ao operador com a partitura.",
        "onde": str(V6), "artefatos": [str(V6 / "pos_rito/textos_custodia_handoff_v406_03nov.py"), str(V6 / "pos_rito/RECIBO_TEXTOS_CUSTODIA_HANDOFF_v406.json"), str(NOS / "HANDOFF_v406_CUSTODIA.md"), str(V6 / "orquestrador/g1_planejar_out.txt")], "refs": []}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_v406_textos_custodia_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-300:]); assert q.returncode == 0
