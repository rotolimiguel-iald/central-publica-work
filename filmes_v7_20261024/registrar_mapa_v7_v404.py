# -*- coding: utf-8 -*-
"""registrar_mapa_v7_v404.py -- gerência c1, 29/10/2026: registra no Mapa de Rotas a rota site.filmes.v7.v404 (molde: site.filmes.v7.v402),
com a correção ao lado da ressalva do estatuto na nota. Fatos LIDOS do disco e do ar; o sha256 dos artefatos é calculado pela ferramenta.
Roda só depois de registrar_v7_v404_no_ar.py (exige a marca no DIARIO_DO_SITE.md). Fail-closed."""
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
BANC = Path(r"C:\IALD\Site\tgl\v3.0_bancada")
TB = Path(r"C:\IALD\Artigo\the_boundary")
W = CEN / "work" / "filmes_v7_20261024"
lerj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
def git(cwd, *a): return subprocess.run(["git", "-C", str(cwd)] + list(a), capture_output=True, text=True).stdout.strip()
diario = (BANC / "DIARIO_DO_SITE.md").read_text(encoding="utf-8", errors="replace")
assert "<!-- filmes_v7:v404:no_ar -->" in diario, "registre primeiro o diário (registrar_v7_v404_no_ar.py)"
with urllib.request.urlopen("https://teoriadagravitacaoluminodinamica.com/video/v7/PUBLIC_DELIVERY_V7.json", timeout=60) as r:
    ar = json.loads(r.read().decode("utf-8"))
assert ar["version"] == "v404"
integ = sorted(W.glob("integrar_v404_*.out"), key=os.path.getmtime)[-1].read_text(encoding="utf-8", errors="replace")
m_int = re.search(r"(\d+) copiados \((\d+) B\), (\d+) já idênticos, 0 faltando, 0 fora do contrato; .* (\d+) arquivos / (\d+) B", integ); assert m_int
tmd = sorted((BANC / "revisoes").glob("testes_filmes_v7_*.md"), key=os.path.getmtime)[-1]
t = tmd.read_text(encoding="utf-8", errors="replace")
m_t = re.search(r"VEREDITO: PASSA — (\d+) critérios medidos", t); m_r = re.search(r"OK · (\d+)/(\d+) comparações · Python exato", t); assert m_t and m_r
l2 = sorted(W.glob("subida_v404*.lotes.out"), key=os.path.getmtime)[-1]
assert "TODOS OS LOTES E O MANIFESTO COMPLETO: SUBIDA VERIFICADA" in l2.read_text(encoding="utf-8", errors="replace")
subs = sorted(d for d in (BANC / "subidas").iterdir() if d.is_dir() and re.fullmatch(r"\d{8}_\d{6}", d.name)); ult = subs[-1]   # só subidas reais
H = CEN / r"Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_H\RESULTADO.json"; h = lerj(H)
C = CEN / r"Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_026_ADENDO_C_fase2_v404.md"; assert C.is_file()
X = CEN / r"Chatgpt\TUNEL\PARA_CHATGPT\X_VITRINE\MANIFEST.json"
tb_head = git(TB, "rev-parse", "--short=8", "HEAD"); cen_head = git(CEN, "rev-parse", "--short=8", "HEAD")
reg = {
    "tipo": "ROTA",
    "rota_id": "site.filmes.v7.v404",
    "dominio": "SITE",
    "titulo": "Os dois filmes V7 renderizados da v404 (adendos G e H da ORDEM 022: frases do gate lidas do core, seis sínteses novas) integrados por hash e publicados no site; a ressalva do estatuto corrigida ao lado; a Fase 2 da vitrine do X (adendo C) preparada",
    "pergunta": "a V7 do selo corrente (v404) está no ar, conferida por hash, com as páginas e os textos do site dizendo o que o core diz?",
    "dados": ["entrega da sessão do vídeo (ADENDO_H/RESULTADO.json; ponteiro video_um\\PUBLIC_DELIVERY_V7.json, %s arquivos públicos)" % h["public_files"],
              "selo v404 3820476c83267f61 (Nós, só leitura)", "core: bandeiras_do_gate_v403 (18 calculadas, 0 literais; 15 no veredito)"],
    "metodo": "integrar_filmes_v7.py (cópia por sha256; index/ui/styles; leitor do recibo por delivery.sha256, chave authorized_counts aceita); testar_filmes_v7.py (headless + replay); geradores do site e do espelho na ordem do G1 depois do remendo do módulo do estatuto; gerar_manifesto.py; subir_em_lotes.py (lotes atômicos + manifesto completo; «nada a subir» aceito como verificação); guarda_do_site.py",
    "resultado": "%s copiados (%s B), %s idênticos, %s arquivos; headless %s/%s; replay %s/%s; subida verificada em %s (lotes + manifesto completo; a 1ª passagem parou no lote 3 por guarda transitória de rede com os arquivos já verificados); ar: PUBLIC_DELIVERY_V7 v404, index «renderizados do um.py v404», llms-full com a ressalva de bandeiras_do_gate_v403; espelho %s; Central %s" % (
        m_int.group(1), m_int.group(2), m_int.group(3), m_int.group(4), m_t.group(1), m_t.group(1), m_r.group(1), m_r.group(2), ult.name, tb_head, cen_head),
    "veredito": "FILMES_V7_V404_NO_AR__SUBIDA_VERIFICADA__RESSALVA_DO_ESTATUTO_CORRIGIDA_AO_LADO__VITRINE_X_FASE2_V404_PREPARADA",
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": "o módulo do estatuto do espelho compunha a ressalva da v392 («15 calculadas e 3 literais»), falsa desde a v403, e ela chegou ao llms-full, ao README/ESTADO_ATUAL/read-brief e ao artigo da vitrine; corrigido ao lado (ramo v403+ lê bandeiras_do_gate_v403); durante os lotes o ar fica misto por minutos",
    "nao_refazer": "Os filmes da v404 estão no ar e conferidos; a Fase 2 da v403 não existiu (a V7 da v403 não foi renderizada); a próxima versão parte de um adendo novo da ORDEM 022 e a vitrine só passa com a V7 do selo corrente.",
    "proximo_passo": "O Codex publica a Fase 2 da v404 no X (ADENDO C) e devolve RESULTADO_FASE2_v404.json; a gerência confere e aceita. Candidato a guarda do G1: zero «como literais» nas superfícies geradas quando o core tem bandeiras_do_gate_v403.",
    "onde": "Site\\tgl\\v3.0_bancada\\tools\\integrar_filmes_v7.py; subir_em_lotes.py; the_boundary\\tools\\estatuto_tres_apoios.py; Central\\tools\\gerar_vitrine_x.py",
    "artefatos": [str(H), str(sorted(W.glob("integrar_v404_*.out"), key=os.path.getmtime)[-1]), str(tmd), str(l2), str(ult / "RELATORIO.md"), str(C), str(X), str(BANC / "DIARIO_DO_SITE.md")],
    "refs": ["site.filmes.v7.v402", "iald.ordem022.adendo_c.render_v401", "custodia.v404"],
    "nota": "Correção ao lado (29/10/2026): a frase «15 calculadas e 3 literais» era verdadeira na v392 e fica como registro; desde a v403 o core diz 18 calculadas, 0 literais, 15 lidas pelo veredito (6 + 5 + 4), 3 informativas, e as 4 experimentais derivam de um só booleano [DECLARADO, não resolvido]. NOT_FALSIFIED nunca é CONFIRMED; o gate não se moveu.",
}
pj = W / "registro_mapa_v7_v404.json"
pj.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([sys.executable, "-X", "utf8", r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", str(pj), "--quem", "claude-c1"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout[-900:], r.stderr[-400:], "rc", r.returncode)
assert r.returncode == 0
