# -*- coding: utf-8 -*-
"""03/11/2026 06:3x, gerencia c1: o Mapa de Rotas recebe (1) a ANOTACAO da custodia v406 na rota do fechamento e (2) uma ROTA nova do caminho examinado no hospedeiro (Range
intermitente), para que nenhuma IA refaça a investigacao. Artefatos por sha256 calculado pela ferramenta. Escrito pelo Write."""
import datetime, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes"); W = CEN / "work/custodia_v406_03nov"; V6 = CEN / "work/cadeia_de_selo/v406"
SUB = Path("C:/IALD/Site/tgl/v3.0_bancada/subidas"); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
arts1 = [V6 / "orquestrador/ESTADO.json", V6 / "orquestrador/RELATORIO_POS_TREINO_v406.md", CEN / "work/custodia_G1/runs/v406_20261103_055852/RELATORIO.json",
         SUB / "20261103_055922/RELATORIO.md", CEN / "organismo/ESTADO_DO_ORGANISMO.json", W / "RECIBO_SEMANTICA_REV1_v406.json", W / "RECIBO_TRIAGEM_FILA_03nov.json",
         CEN / "work/custodia_G1/LICOES_v400_25out.md", Path("C:/IALD/TORRE_IALD/TORRE_v406.json"), W / "DESPACHO_CODEX_F03_v406.md"]
arts2 = [W / "RECIBO_ERRATA_SUBIR_SITE_RANGE_v406.json", SUB / "20261103_052210/RELATORIO.md", SUB / "20261102_035422/RELATORIO.md", W / "errata_subir_site_range_v406_03nov.py",
         W / "teste_estrito_subir_site_range_03nov.py", W / "errata_site_e17_perna3_v406_03nov.py"]
for a in arts1 + arts2:
    assert a.is_file(), "artefato ausente: %s" % a
reg = [
    {"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
     "titulo": "v406 PUBLICADA (03/11/2026): custodia G1 com 37 passos aplicados; t3 aberto; sete paradas consertadas ao lado (licoes 43-50)",
     "pergunta": "A v406 foi publicada e atualizada em tudo, como o operador ordenou em 02/11? O que ficou aberto e por que?",
     "dados": [str(a) for a in arts1],
     "metodo": "orquestrador pos_treino_v406 (S0-S8; S5, S6c e S7 com decisao da gerencia dita na ESTADO.json); G1 custodiar.py planejar/executar --publicar/auditar em 5 rodadas; conferencias no ar por HTTP (sha256, pino) pela gerencia",
     "resultado": ("PUBLICADA: the_boundary a381c4d1 = origin/main; Central 42f3b0c9 = origin/main; site v406 no ar (subidas verificadas 20261103_025919 e 20261103_055922, a segunda com os 83 arquivos "
                   "da Central publica); Central publica 22/22 no quadro das 06:10 (um.acom sha16 bff9e20b425568bc igual ao local); leitor de IA R1; conferencia final 13/13; ACOM t1/t2; rota custodia.v406; "
                   "Nos vivo; TORRE_v406.json; auditar rc 0 (0 numeros defasados). C19 parou: 7 DEFASADOS fora desta custodia (ACTIVE.json v404 e DELIVERY v406: Codex sem cota ate 04/11 06:37; JEV v406: "
                   "release do app, C21, operador; Torre: CLAUDE.md Haja_Luz 1.245.626 B e Nativa 636.937 B > 262.144 B; missao ACOM 12/10 recusada pelo guarda). Paradas consertadas ao lado: prosa do "
                   "handoff (43), rev1 da semantica (44), EXCL_RAIZ e sufixo do C8 (45-46), estacao do runner (47), camadas v395/v396 do modulo dos 16 (48), Range do hospedeiro (49), ordem das pernas (50). "
                   "Memoria: indice em PUBLICADA, pino 06:01, 15 depositos promovidos."),
     "veredito": "CUSTODIA_V406_PUBLICADA__T3_ABERTO__C19_C20_C17C_PENDENTES_DE_CODEX_OPERADOR_E_TORRE__GATE_INTOCADO",
     "estatuto": "REAL (recibos, relatorios e o ar lidos por script/HTTP); as decisoes abertas sao do operador", "status": "EM_CURSO", "olhou_dados": False,
     "defeito": "o executar da G1 devolve 20 (nao 5) quando os DEFASADOS sao do Codex ou da Torre, e nao do operador: a classificacao nao distingue «de outro agente» de «falha»",
     "nao_refazer": "a custodia nao se refaz: C19/C20/C17C retomam com `custodiar.py executar --versao v406 --publicar` depois do despacho F0.3 (DESPACHO_CODEX_F03_v406.md) e da release do app",
     "proximo_passo": "04/11 06:37: ler a cota do Codex; despacho unico F0.3; depois executar --publicar; decisoes do operador: nomes das pedras, D2, README pinado (D39), D34-D40, app (C21), motor continuo v407, Locaweb/Range",
     "onde": str(W), "artefatos": [str(a) for a in arts1], "refs": ["infra.site_hospedeiro_range_intermitente_03nov"],
     "nota": "NOT_FALSIFIED nunca e' CONFIRMED; validade no kernel nao e' creditacao; nada aqui move gate, selo ou cofre."},
    {"tipo": "ROTA", "rota_id": "infra.site_hospedeiro_range_intermitente_03nov", "dominio": "INFRA_PUBLICACAO",
     "titulo": "O hospedeiro do site (nginx/1.24, Lw-X-Id) deixou de honrar HTTP Range de forma intermitente em 03/11/2026; a subida da Central publica foi revertida com bytes integros",
     "pergunta": "Por que subir_site.py reverteu 86 arquivos com HTTP 200, bytes e sha256 iguais? E' defeito nosso ou do hospedeiro?",
     "dados": [str(a) for a in arts2],
     "metodo": ("comparacao dos relatorios 20261102_035422 (Range 206 nos mesmos tres caminhos) e 20261103_052210 (200); cmp do .htaccess local contra antes/ (iguais); pedidos repetidos com o UA do "
                "script (Range: bytes=0-1023) em arquivos de idades, tipos e tamanhos diferentes, no mesmo no'; controle no raw do GitHub (206)"),
     "resultado": ("02/11 03:54: tgl-atlas.txt, tgl-core.txt, um.acom -> 206. 03/11 05:35: os mesmos -> 200 com arquivo inteiro, bytes e sha256 iguais; 86 arquivos revertidos; ar incoerente (site v406, "
                   "Central v405) ate' 06:09. 03/11 ~05:4x: bom.mp3 206,206,200,200 e depois 200 x6; documents/106/file.md 206,206,206,200; documents/128/file.pdf 206 x6; videos mp4 206 x3; robots.txt (set/2026) "
                   "200; sem relacao com idade, tipo, tamanho, Cache-Control ou Vary; mesmo no' @dinesh0020; .htaccess identico. 05:59 (subida 20261103_055922, 83 arquivos): 0 avisos de Range (voltou a 206)."),
     "veredito": "PAREDE_MEDIDA_NO_HOSPEDEIRO__RANGE_INTERMITENTE__ARQUIVOS_INTEGROS__VERIFICADOR_CORRIGIDO_AO_LADO",
     "estatuto": "REAL (medido por HTTP e nos relatorios)", "status": "EXAMINADA", "olhou_dados": True,
     "defeito": "o verificador reprovava e revertia a subida inteira por um 200 no Range mesmo com bytes e sha256 iguais; a promessa «this site answers 206 (measured)» do read-brief.md nao vale para todo pedido",
     "nao_refazer": "a causa esta' no hospedeiro, nao nos arquivos nem no .htaccess; nao ha' o que investigar do lado do site alem de repetir a medida; o verificador ja' trata o caso como AVISO MEDIDO",
     "proximo_passo": "decisao do operador: avisar a Locaweb; v407: pre-voo mede o Range do hospedeiro antes de qualquer subida; reescrever a frase do read-brief so' depois de medir de novo",
     "onde": "C:/IALD/Site/tgl/v3.0_bancada/tools/subir_site.py (verificar_no_ar, errata ao lado 03/11/2026)", "artefatos": [str(a) for a in arts2],
     "refs": ["kernel.fechamento_construir_tudo_programa_02nov"], "nota": "licoes 49 e 50 do livro da G1"},
]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_v406_custodia_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-500:], q.stderr.decode("utf-8", "replace")[-300:]); assert q.returncode == 0
