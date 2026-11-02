# -*- coding: utf-8 -*-
"""Registra no Mapa de Rotas a Fase 2 da vitrine do X para a v404 (ADENDO C), ACEITA pela gerência c1 em 29/10/2026 (65/65). Lê o aceite
e o recibo do disco; os sha256 dos artefatos são calculados pela ferramenta."""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
W = Path("C:/IALD/Central de Patentes/work/x_vitrine_26out"); T = Path("C:/IALD/Central de Patentes/Chatgpt/TUNEL")
A = json.loads((W / "ACEITE_FASE2_v404_29out.json").read_text(encoding="utf-8")); assert A["veredito"] == "ACEITA"
R = json.loads((T / "DO_CHATGPT/ORDEM_026/VITRINE/RESULTADO_FASE2_v404.json").read_text(encoding="utf-8"))
posts = {it["item"]: it.get("url") for it in R["items"] if it.get("url")}
reg = [{
 "tipo": "ROTA", "rota_id": "vitrine_x.fase2_v404.aceita", "dominio": "F0_PUBLICACAO",
 "titulo": "Vitrine do X, Fase 2 da v404 (ADENDO C): post da versão, os dois filmes V7 da v404, fixado, capa e artigo no mesmo id; aceite da gerência 65/65",
 "pergunta": "A Fase 2 da vitrine saiu para o selo corrente (v404) com os filmes do selo corrente, sem repetir nada e com o artigo dizendo o que o core diz?",
 "dados": ["MANIFEST.json v404 (sha16 cd748ab51def3c1c; pin = sha256 do um.py do Nós)", "RESULTADO_FASE2_v404.json da coordenadora do Codex (COMPLETED_VERIFIED_AWAITING_MANAGEMENT_ACCEPTANCE)"],
 "metodo": "aceite_fase2_v404_29out.py: manifesto = disco = selo; cada arquivo usado disco = recibo = manifesto; posts novos distintos e não repetidos (Fase 1, Fase 2 v402); artigo no mesmo id; perfil/bio/fixado anterior preservados; evidências e capturas por sha256; textos publicados = fonte (sem URL, espaço normalizado); depósito na fila com hash",
 "resultado": "ACEITA %d/%d; 4 posts novos (%s); artigo %s atualizado no mesmo id com «Selo corrente: v404» e a ressalva do gate na forma da v403; conta de %d a %d posts; legenda EN sem segundo espaço; unidade F0.X_VITRINE_20261026 AUDITADA (evento 1356)" % (
     A["n_ok"], A["n_checks"], ", ".join("%s %s" % (k, v.rsplit("/", 1)[-1]) for k, v in posts.items() if k != "artigo"), posts.get("artigo", "").rsplit("/", 1)[-1], R["profile_post_count_before"], R["profile_post_count_after"]),
 "veredito": "VITRINE_X_FASE2_V404_ACEITA_65_65", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
 "defeito": "nenhum no aceite; ressalvas: legenda EN não entra (um espaço por vídeo); a conferência dos textos é contra a evidência de UI gravada pela coordenadora, não contra o X ao vivo",
 "nao_refazer": "não republicar nada da v404 (posts, Destaques, fixado, capa, artigo); a próxima Fase 2 só com a V7 do selo seguinte no ar e MANIFEST novo",
 "proximo_passo": "próxima custódia: CUSTODIA_vNNN.txt → adendo do render (ORDEM 022) → V7 no ar → gerar_vitrine_x.py → adendo da ORDEM 026 → aceite; candidato ao G1: passo que escreve o CUSTODIA e dispara os adendos",
 "onde": "work/x_vitrine_26out/aceite_fase2_v404_29out.py; tools/gerar_vitrine_x.py; work/x_vitrine_26out/gerar_adendo_c_v404.py",
 "artefatos": [str(W / "ACEITE_FASE2_v404_29out.json"), str(T / "DO_CHATGPT/ORDEM_026/VITRINE/RESULTADO_FASE2_v404.json"), str(T / "PARA_CHATGPT/X_VITRINE/MANIFEST.json"), str(T / "PARA_CHATGPT/ORDEM_026_ADENDO_C_fase2_v404.md")],
 "refs": ["site.filmes.v7.v404", "vitrine_x.fase2_v403.bloqueada_pela_v7", "custodia.v404"],
 "nota": "NOT_FALSIFIED nunca é CONFIRMED; PROVADA = validade; o gate não se moveu. O aceite não valida ciência: confere publicação contra manifesto e recibo."}]
pj = W / "rota_mapa_vitrine_fase2_v404_29out.json"; pj.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
r = subprocess.run([sys.executable, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout[-700:], r.stderr[-300:], "rc", r.returncode); assert r.returncode == 0
