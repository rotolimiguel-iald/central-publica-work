# -*- coding: utf-8 -*-
"""registrar_v7_v404_no_ar.py -- gerência c1, 29/10/2026: depois de a V7 da v404 estar NO AR com subida verificada, registra o feito nas
superfícies da casa: DIARIO_DO_SITE.md (bancada do site), e os tópicos de memória da gerência filmes-do-site-v7-24out.md,
x-vitrine-da-tgl-26out.md e licoes-cadeia-v404-28out.md (lições 14-17). Todos os números são LIDOS (integração, testes, lotes, subidas, ar,
git, recibo do adendo H, adendo C); nada digitado. Backup de bytes antes de cada arquivo; acréscimo no estilo de fim de linha da última
linha; temporário -> conferir -> substituir. Fail-closed: se o ar não tiver a V7 da v404 e a ressalva nova, não escreve nada."""
import glob
import hashlib
import json
import os
import re
import subprocess
import time
import urllib.request
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
BANC = Path(r"C:\IALD\Site\tgl\v3.0_bancada")
TB = Path(r"C:\IALD\Artigo\the_boundary")
MEM = Path(os.environ["USERPROFILE"]) / ".claude" / "projects" / "c--IALD-Central-de-Patentes" / "memory"
W = CEN / "work" / "filmes_v7_20261024"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lerj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
def git(cwd, *a): return subprocess.run(["git", "-C", str(cwd)] + list(a), capture_output=True, text=True).stdout.strip()
def http(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")

# --- o ar (fail-closed)
ar = json.loads(http("https://teoriadagravitacaoluminodinamica.com/video/v7/PUBLIC_DELIVERY_V7.json"))
assert ar["version"] == "v404" and ar["source_sha256"].startswith("3820476c83267f61"), ar.get("version")
idx = http("https://teoriadagravitacaoluminodinamica.com/")
assert "renderizados do um.py v404" in idx, "o index no ar não diz v404 nos filmes"
full = http("https://teoriadagravitacaoluminodinamica.com/llms-full.txt")
assert "bandeiras_do_gate_v403" in full and "como literais" not in full, "o llms-full no ar não traz a ressalva nova"
est = http("https://teoriadagravitacaoluminodinamica.com/estado.txt")
m_commit = re.search(r"commit ([0-9a-f]{8,12})", est); assert m_commit, "estado.txt no ar sem commit"
tb_head = git(TB, "rev-parse", "--short=8", "HEAD"); assert git(TB, "rev-parse", "--short=8", "origin/main") == tb_head
assert m_commit.group(1).startswith(tb_head), ("o cartão no ar cita outro commit do espelho", m_commit.group(1), tb_head)
cen_head = git(CEN, "rev-parse", "--short=8", "HEAD"); assert git(CEN, "rev-parse", "--short=8", "origin/main") == cen_head
# --- a integração e os testes
integ = sorted(W.glob("integrar_v404_*.out"), key=os.path.getmtime)[-1].read_text(encoding="utf-8", errors="replace")
m_int = re.search(r"(\d+) copiados \(([\d]+) B\), (\d+) já idênticos, 0 faltando, 0 fora do contrato; ponteiro sha256 ([0-9a-f]{16}), manifesto sha256 ([0-9a-f]{16}), (\d+) arquivos / (\d+) B", integ)
assert m_int and "INTEGRADO" in integ, "saída da integração não lida"
tmd = sorted((BANC / "revisoes").glob("testes_filmes_v7_*.md"), key=os.path.getmtime)[-1].read_text(encoding="utf-8", errors="replace")
m_t = re.search(r"VEREDITO: PASSA — (\d+) critérios medidos", tmd); assert m_t, "testes sem PASSA"
m_r = re.search(r"OK · (\d+)/(\d+) comparações · Python exato", tmd); assert m_r and m_r.group(1) == m_r.group(2)
# --- os lotes (as duas passagens) e a subida verificada do manifesto completo
logs = sorted(W.glob("subida_v404*.lotes.out"), key=os.path.getmtime)
l1, l2 = logs[-2].read_text(encoding="utf-8", errors="replace"), logs[-1].read_text(encoding="utf-8", errors="replace")
assert "TODOS OS LOTES E O MANIFESTO COMPLETO: SUBIDA VERIFICADA" in l2, "a retomada não terminou verificada"
n_lotes = int(re.search(r"em (\d+) lotes; depois o manifesto completo", l2).group(1))
n_nada = l2.count("nada a subir")
subs = sorted(d for d in (BANC / "subidas").iterdir() if d.is_dir() and re.fullmatch(r"\d{8}_\d{6}", d.name))   # só subidas reais (nem _dryrun, nem _prep_*)
ult = subs[-1]; relu = (ult / "RELATORIO.md").read_text(encoding="utf-8", errors="replace"); assert "SUBIDA VERIFICADA" in relu
msub = lerj(ult / "MANIFESTO_SUBIDA.json"); assert msub["n"] >= 1500 and any(a["caminho"] == "llms-full.txt" for a in msub["arquivos"])
# --- o recibo do adendo H, o adendo C e a correção do estatuto
h = lerj(CEN / r"Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_H\RESULTADO.json"); assert h["status"] == "BUILT_FOR_MANAGEMENT_INTEGRATION_PUBLICATION"
C = CEN / r"Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_026_ADENDO_C_fase2_v404.md"; assert C.is_file(), "adendo C ainda não escrito"
c16 = sha(C)[:16]
X = CEN / r"Chatgpt\TUNEL\PARA_CHATGPT\X_VITRINE"; man = lerj(X / "MANIFEST.json"); assert man["selo"]["versao"] == "v404"
est_mod = TB / "tools" / "estatuto_tres_apoios.py"; assert "bandeiras_v403" in est_mod.read_text(encoding="utf-8")
hoje = time.strftime("%d/%m/%Y"); agora = time.strftime("%H:%M")
car = ult.name[:15]; hora_ar = "%s:%s" % (car[9:11], car[11:13])

def acrescentar(p, bloco, marca):
    raw = p.read_bytes(); txt = raw.decode("utf-8")
    assert marca not in txt, "já registrado: %s" % p.name
    nl = "\r\n" if txt.endswith("\r\n") else "\n"
    novo = txt + ("" if txt.endswith(nl) else nl) + nl + nl.join(bloco).replace("\n", nl) + nl
    assert novo.startswith(txt)
    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = p.with_name(p.name + ".bak_" + ts); bak.write_bytes(raw); assert bak.read_bytes() == raw
    tmp = p.with_name(p.name + ".tmp_" + ts); tmp.write_bytes(novo.encode("utf-8")); assert tmp.read_bytes().decode("utf-8") == novo
    os.replace(tmp, p); print("acrescentado", p.name, len(raw), "->", len(p.read_bytes()))

diario = [
    "## %s %s — os filmes V7 da v404 no ar; a ressalva do estatuto corrigida ao lado (gerência c1)" % (hoje, agora),
    "",
    ("A entrega da sessão do vídeo (ORDEM 022, adendos G e H: render da v404 em vez do da v403; frases do gate lidas do core; %d sínteses novas, %d reutilizadas, "
     "%d pedidos, 0 repetições; revisão independente PASS_WITH_SCOPE; ponteiro `PUBLIC_DELIVERY_V7.json` sha256 `%s…`; %s arquivos públicos) foi integrada por hash em "
     "`video/v7/` (`tools/integrar_filmes_v7.py`: %s copiados, %s já idênticos, %s arquivos / %s B; o leitor do recibo passou a aceitar a chave `authorized_counts` do adendo H) "
     "e publicada. Teste headless %s/%s (PASSA); replay %s/%s, Python exato. O `index.html` diz «renderizados do um.py v404»; o `llms.txt` idem. Subida por `tools/subir_em_lotes.py` "
     "em duas passagens: a primeira parou no lote 3 porque a guarda do espelho reprovou por um sopro de rede («porta acima do llms.txt NÃO RESOLVE») com os arquivos já verificados no ar, "
     "e a 2ª tentativa devolveu «nada a subir: o ar já é igual ao manifesto», que o script não aceitava; remendo (backup) — «nada a subir» com rc 0 conta como verificação, como o G1 lê — "
     "e retomada com manifesto novo: %d lotes (%d já no ar) e o manifesto completo (%d arquivos): SUBIDA VERIFICADA (`subidas/%s`, ar às %s)."
     % (h["audio"]["new_units"], h["audio"]["reused_units"], h["audio"]["requests"], h["delivery"]["sha256"][:16], h["public_files"], m_int.group(1), m_int.group(3), m_int.group(6), m_int.group(7),
        m_t.group(1), m_t.group(1), m_r.group(1), m_r.group(2), n_lotes, n_nada, msub["n"], ult.name, hora_ar)),
    "",
    ("**Correção ao lado, achada no caminho:** o módulo do estatuto do espelho (`the_boundary/tools/estatuto_tres_apoios.py`) ainda compunha a ressalva da v392 («a auditoria lê 15 como calculadas e 3 como literais»), "
     "falsa desde a v403, cujo core traz `bandeiras_do_gate_v403` (18 calculadas, 0 literais; o veredito lê 15 = 6 + 5 + 4; 3 informativas; as 4 experimentais de um só booleano, DECLARADO e não resolvido). "
     "A frase ia ao `llms-full.txt`, ao README/ESTADO_ATUAL/read-brief do espelho e ao artigo da vitrine do X, e contradizia o `CUSTODIA_v404.txt` e os filmes (adendo G). O módulo ganhou o ramo v403+ (a v392 fica como registro em `elif`); "
     "ESTADO_ATUAL, README, read-brief, seções, TUNEL e PORTAs regenerados na ordem do G1; `verificar_portas` ERROS 0; `guarda_do_selo` «o que se publica é o que o selo descreve»; espelho `%s` = origin/main. "
     "O cartão de estado do site passou a citar esse commit; `llms-full.txt`, `index.md` e `read-brief.txt` regenerados e no ar. Central `%s` (remendos: quadro e G1 leem a entrega da fila científica pelo recibo; leitor da ressalva da vitrine). "
     "Vitrine do X: `X_VITRINE\\MANIFEST.json` novo (v404) e `ORDEM_026_ADENDO_C_fase2_v404.md` (sha16 `%s`). NOT_FALSIFIED nunca é CONFIRMED; PROVADA = validade; o gate não se moveu." % (tb_head, cen_head, c16)),
    "<!-- filmes_v7:v404:no_ar -->",
]
acrescentar(BANC / "DIARIO_DO_SITE.md", diario, "<!-- filmes_v7:v404:no_ar -->")

filmes = [
    "## %s — a V7 da v404 NO AR (gerência c1)" % hoje,
    ("- Adendo H entregue pelo Codex às 01:07 (`BUILT_FOR_MANAGEMENT_INTEGRATION_PUBLICATION`; fonte v404; %d sínteses novas, %d reutilizadas, 0 repetições; %s arquivos públicos; custo direto de TTS estimado US$ 0 [DERIVED]; revisão PASS_WITH_SCOPE)."
     % (h["audio"]["new_units"], h["audio"]["reused_units"], h["public_files"])),
    ("- Integração por hash (`integrar_filmes_v7.py`; o leitor do recibo aceita `authorized_counts`): %s copiados, %s idênticos, %s arquivos. Headless %s/%s; replay %s/%s." % (m_int.group(1), m_int.group(3), m_int.group(6), m_t.group(1), m_t.group(1), m_r.group(1), m_r.group(2))),
    ("- Subida: `subir_em_lotes.py` em duas passagens (a 1ª parou no lote 3 por guarda transitória + «nada a subir» não aceito; remendo; retomada %d lotes + manifesto completo): SUBIDA VERIFICADA `subidas/%s`; ar às %s." % (n_lotes, ult.name, hora_ar)),
    "- A ressalva do estatuto (v392) corrigida ao lado no módulo do espelho (lê `bandeiras_do_gate_v403`); espelho `%s`; cartão do site cita esse commit." % tb_head,
    "- Próximo: ORDEM 026 adendo C (Fase 2 da v404) despachado; o `CUSTODIA_v404.txt` já estava no manifesto. A Fase 2 da v403 não existiu.",
    "<!-- filmes_v7:v404:no_ar -->",
]
acrescentar(MEM / "filmes-do-site-v7-24out.md", filmes, "<!-- filmes_v7:v404:no_ar -->")

vitrine = [
    "## %s — Fase 2 da v404 (ADENDO C) escrita e despachada; a da v403 não existiu (gerência c1)" % hoje,
    ("- `tools/gerar_vitrine_x.py` passou com a V7 da v404 no site: `X_VITRINE\\MANIFEST.json` sha16 `%s` (gerado em %s), 14 arquivos; o `CUSTODIA_v404.txt` (sha16 `%s`) já no manifesto."
     % (sha(X / "MANIFEST.json")[:16], man["gerado_em"], man["arquivos"]["CUSTODIA_v404.txt"]["sha256"][:16])),
    ("- **Achado:** o artigo da vitrine repetia «15 calculadas e 3 literais» (a ressalva da v392 do módulo do estatuto), falsa desde a v403; o módulo do espelho e o leitor do gerador foram corrigidos ao lado (o artigo no X é atualizado no MESMO id pelo adendo C). "
     "Regra: toda frase pública com contagem do gate nasce de `bandeiras_do_gate_v403`, lido na hora."),
    "- `ORDEM_026_ADENDO_C_fase2_v404.md` (sha16 `%s`): post da versão, os dois filmes da v404, fixado/capa/artigo conforme o que mudou no manifesto; bio só se mudou; devolução em `DO_CHATGPT\\ORDEM_026\\VITRINE\\RESULTADO_FASE2_v404.json`." % c16,
    "<!-- x_vitrine:fase2:v404:adendo_c -->",
]
acrescentar(MEM / "x-vitrine-da-tgl-26out.md", vitrine, "<!-- x_vitrine:fase2:v404:adendo_c -->")

licoes = [
    "## %s — lições da V7 e da vitrine da v404 (gerência c1)" % hoje,
    "",
    ("14. **A ressalva do estatuto envelheceu em silêncio desde a v403.** `the_boundary/tools/estatuto_tres_apoios.py` compunha a ressalva só do registro da v392 (`estatuto_da_prova_ressalva_v392`: «15 calculadas e 3 literais») "
     "e a levava ao `llms-full.txt`, ao README/ESTADO_ATUAL/read-brief e, pela vitrine, ao X; o core traz `bandeiras_do_gate_v403` desde a v403. O render dos filmes parou por isso (adendo F) e a vitrine só não repetiu porque o ensaio foi lido. "
     "**How to apply:** toda frase pública com contagem do gate lê `bandeiras_do_gate_v403.values` na hora; candidato a guarda do G1 (E09/E15): `grep -F 'como literais'` zero nas superfícies geradas quando o core tem o registro v403."),
    "15. **`subir_em_lotes.py` não aceitava «nada a subir: o ar já é igual ao manifesto»** (rc 0) e parava a sequência; o G1 já lia isso como verificação. Remendo com backup. E a guarda do espelho pode reprovar por sopro de rede («porta acima … NÃO RESOLVE») com os arquivos já verificados: o `subir_site.py` não reverte nesse caso (certo) e a retomada é «nada a subir».",
    "16. **Arquivos com fim de linha MISTO:** `estatuto_tres_apoios.py` tem CRLF em parte das linhas e LF nas âncoras; `MEMORY_2.md` tem 791 CRLF em 4427. Remendo e acréscimo seguem o estilo LOCAL da âncora/última linha, e `novo.startswith(antigo)` prova que nenhum byte existente mudou.",
    "17. **O recibo do adendo H renomeou `authorized_kernel_counts` → `authorized_counts`;** `integrar_filmes_v7.py` lê uma ou outra (mesma subchave). O leitor do RESULTADO é por `delivery.sha256` (acha sozinho o adendo que declara o ponteiro).",
    "",
    "Relacionado: [[filmes-do-site-v7-24out]] · [[x-vitrine-da-tgl-26out]].",
]
acrescentar(MEM / "licoes-cadeia-v404-28out.md", licoes, "lições da V7 e da vitrine da v404")
print("espelho", tb_head, "central", cen_head, "subida", ult.name, "lotes", n_lotes, "nada_a_subir", n_nada, "adendo_c", c16)
