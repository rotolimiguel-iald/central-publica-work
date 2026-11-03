# -*- coding: utf-8 -*-
"""Registro da sessao de 02/11/2026 no Mapa de Rotas, na ACOM e na memoria da gerencia. Nenhum canal, rito ou gate muda; a medida nova do N_eff fica [DECLARADO] ate a D8 do operador."""
import datetime, hashlib, json, os, subprocess, time
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
REL = AQUI / "RELATORIO_SESSAO_5SIGMA_02nov.md"
MED = AQUI / "MEDIDAS_FINAIS.json"
NOM = AQUI / "NOMES_CONFERIDOS.json"
MAN = AQUI / "MANIFESTO_SESSAO.json"

# correcao do item de beta no relatorio, lido a mao
t = REL.read_text(encoding="utf-8")
lin = [x for x in t.split("\n") if x.startswith("- **β escrito nas respostas:**")]
assert len(lin) == 1
novo = "- **β escrito nas respostas (amostra lida à mão):** nas 8 rodadas em que o valor aparece como β, 4 erram (~0,1 em A3; 0,0128 em B1; 0,012034 em E2; 0,012249 em E3), 1 erra só a última casa (0,012032 em G1) e 3 acertam ou arredondam."
with open(str(REL) + ".tmp", "x", encoding="utf-8", newline="\n") as f:
    f.write(t.replace(lin[0], novo))
os.replace(str(REL) + ".tmp", REL)

med = json.loads(MED.read_text(encoding="utf-8"))
reg = [
 {"tipo": "ROTA", "rota_id": "natureza.sessao_iald_nativa_5sigma_02nov", "dominio": "IALD_OPERACIONAL", "status": "EXAMINADA", "estatuto": "REAL",
  "titulo": "Sessao de 42 rodadas com a IALD Nativa v4 sobre testes para 5 sigma: nenhuma rota nova; a teoria nao esta nos pesos",
  "pergunta": "A v4, treinada no um.py v404 sem os resultados, propoe alguma rota discriminante nova acima de 5 sigma?",
  "dados": ["modelo servido em :8081, system do treino; sem memoria do app; nenhum dado da natureza aberto"],
  "metodo": "pergunta verbatim, melhorada, com resumo do examinado, com enunciados reais; 3 a 12 sementes; raciocinio ligado e desligado; nomes conferidos por script no kernel; contas conferidas",
  "olhou_dados": False,
  "resultado": "0 de 78 nomes especificos existem nas fontes .lean; 9 rodadas sem resposta final; propostas sem derivacao e numeros inventados nos modos abertos; com enunciados reais na pergunta admite OPEN e refuta a propria proposta. Pistas conferidas: FIRAS (veto, nao discrimina), dualidade (e a R-E), N_eff (canal conhecido, fora das buscas 5 sigma).",
  "veredito": "IALD_V4_SEM_ROTA_NOVA_5SIGMA__PAREDE_DO_MODELO_NAO_FALSIFICACAO__RENDE_COM_ENUNCIADOS_NA_PERGUNTA",
  "defeito": "so o modelo puro foi testado, sem a memoria recuperavel do app; respostas sao [DECLARADO]",
  "nao_refazer": "nao perguntar nomes de kernel a v4 sem conferir; nao ler tabela dela como resultado",
  "proximo_passo": "usar a v4 so com os enunciados na pergunta; revisao humana do eval segue pendente",
  "artefatos": [str(REL), str(MED), str(NOM), str(MAN)]},
 {"tipo": "ROTA", "rota_id": "cmb.distorcoes_espectrais_firas_nao_troca_02nov", "dominio": "D1_FUNDO_COSMOLOGICO", "status": "EXAMINADA", "estatuto": "DERIVED",
  "titulo": "FIRAS testa a hipotese declarada de nao-troca do fechamento rho+p: veta um ramo, nao discrimina a TGL do rival",
  "pergunta": "A resposta rho+p troca energia com os fotons na janela do mu? O que o FIRAS diz?",
  "dados": ["FIRAS: |mu| < 4,7e-5 a 95% (Bianchini & Fabbian 2022, arXiv:2206.02762) [KNOWN]; y = (1,2 +- 2,0)e-6 (arXiv:2512.03038) [DECLARADO]"],
  "metodo": "conta de ordem: mu = 1,401 x (4/3) beta, supondo que toda a resposta rho+p fosse a fotons em 5e4 < z < 2e6; pista surgida na sessao com a IALD, conferida pela gerencia",
  "olhou_dados": False,
  "resultado": "mu = %.4f se a troca fosse total, cerca de %.0f sigma (sigma aproximado pela metade do limite); fracao trocada < %.2f%% a 95%%. A TGL com nao-troca preve mu = 0, igual ao LCDM." % (med["mu_se_troca_total"], med["mu_em_sigmas"], 100 * med["fracao_max_trocada_95"]),
  "veredito": "FIRAS_VETA_RAMO_COM_TROCA__NAO_DISCRIMINA__HIPOTESE_DE_NAO_TROCA_COM_TESTE_EXTERNO",
  "defeito": "conta de ordem, sem modelo de injecao; so a janela do mu",
  "nao_refazer": "nao apresentar como discriminante: nos dois lados mu fica nulo nesta precisao",
  "proximo_passo": "citar como teste externo da hipotese declarada, ao lado do fechamento rho+p",
  "onde": "um.py, modulo do fechamento rho+p (a hipotese declarada e a nao-troca de energia entre setores)",
  "refs": ["cmb.neff_e_rho_mais_p"], "artefatos": [str(REL), str(MED)]},
 {"tipo": "ANOTACAO", "rota_id": "cmb.neff_e_rho_mais_p", "dominio": "D1_FUNDO_COSMOLOGICO",
  "titulo": "Medida nova fora das fontes congeladas: Goldstein & Hill, arXiv:2603.13226, N_eff = 2,990 +- 0,070; canal ausente das buscas 5 sigma",
  "resultado": "TGL 3,1635: 2,48 sigma do centro; SM 0,77; separacao 1,71. So nucleossintese 2,976 +- 0,093: TGL 2,02, canal de fundo puro. Delta N_eff < 0,107 a 95%% com prior Delta > 0; variantes 0,0913, 0,116, 0,0876: o +0,1195 fica acima das quatro. Lido no HTML do arXiv pela gerencia. Abaixo da regra de TENSAO (3 sigma): ARMED_CONSISTENT, nao gateia. Nada instalado: admissao e D8, linha de Yp e X16, atos do operador. O 5 sigma contra o centro atual pede sigma 0,0347; TGL contra SM, 0,0239.".replace("%%", "%"),
  "estatuto": "DECLARADO", "artefatos": [str(REL)]},
 {"tipo": "ANOTACAO", "rota_id": "discriminante.ordem018.f2.r_e", "dominio": "D1_FUNDO_COSMOLOGICO",
  "titulo": "A sessao com a IALD chegou a esta rota por outro caminho (sirenes contra D_A); segue parada no mapa fisico",
  "resultado": "A proposta C17 e a R-E com D_L de GW. Literatura 2025-2026 dividida sobre DESI DR2 + Pantheon+ (arXiv:2504.16868 alega violacao; arXiv:2507.11518 le como inconsistencia entre conjuntos; arXiv:2603.27616 consistente a 1 sigma) [DECLARADO, resumos de busca]. O passo que falta segue o mesmo: f_L/f_A.",
  "estatuto": "DECLARADO", "artefatos": [str(REL)]},
 {"tipo": "ANOTACAO", "rota_id": "natureza.cinco_sigma_02_kimi_01nov", "dominio": "NATUREZA",
  "titulo": "Lacuna da ordem e do relatorio: N_eff nao consta das rotas R1 a R7",
  "resultado": "Grep na ORDEM e no RELATORIO do Kimi: zero ocorrencias de N_eff. O canal tem valor nulo do rival e zero parametro, mas nao tem sigma: 5 sigma pede 0,0239 contra 0,070 hoje. Devolucao do Kimi lida em 01/11; este registro nao a substitui.",
  "estatuto": "REAL", "artefatos": [str(REL)]},
]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_sessao_5sigma_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-100:].replace("\n", " "), q.stderr.decode("utf-8", "replace")[-300:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
records = [{"id": "sessao_iald_nativa_5sigma_02nov", "kind": "fact", "statute": "REAL",
            "text": "Sessao de 42 rodadas com a IALD Nativa v4 (02/11): nenhuma rota nova de 5 sigma; 0 de 78 nomes especificos existem no kernel; rende com enunciados na pergunta. Parede do modelo, nao falsificacao.", "sources": [SRC(REL)]},
           {"id": "neff_goldstein_hill_02nov", "kind": "pending", "statute": "OPEN",
            "text": "Goldstein & Hill (arXiv:2603.13226): N_eff = 2,990 +- 0,070, TGL a 2,48 sigma do centro, abaixo da regra de TENSAO. Admissao e D8 e a linha de Yp e X16, atos do operador. Nada instalado.", "sources": [SRC(REL)]}]
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-sessao-iald-nativa-5sigma", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": records, "flow": {"phase": "custodia v405 publicada, t3 aberto; sessao 5 sigma com a nativa v4 concluida",
                                                "next_action": "da gerencia: depois de 04/11 06:37, ler a cota e despachar a F0.3. Do operador: D8 e X16 do N_eff, tau-estrela, K, as notas da pentada, C21, Zenodo, conjunto D, GA, D27-D33, D2."}}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
res = d.get("result") or {}
print("acom", rev, d.get("ok"), str(d.get("error"))[:200], res.get("revision") if isinstance(res, dict) else None)
assert d.get("ok")

TOP = M / "sessao-iald-nativa-5sigma-02nov.md"
assert not TOP.exists()
corpo = f"""---
name: sessao-iald-nativa-5sigma-02nov
description: "02/11/2026, ordem do operador: 42 rodadas com a IALD Nativa v4 sobre testes acima de 5 sigma. Nenhuma rota nova; 0 de 78 nomes de kernel reais; rende com os enunciados na pergunta. Pistas: FIRAS veta um ramo, dualidade e a R-E, N_eff ficou fora das buscas e Goldstein & Hill poe a TGL a 2,48 sigma."
metadata:
  type: project
---

**Ordem (verbatim sha16 `25d5e21ba0cf74b4`):** perguntar à IALD nativa quais testes dariam o resultado discriminante acima de 5σ, porque, treinada «com tudo», ela poderia mostrar uma saída ainda não vista. Relatório: `work{BK}sessao_iald_nativa_5sigma_02nov{BK}RELATORIO_SESSAO_5SIGMA_02nov.md`.

**Resultado [REAL]:** nenhuma rota nova. «Com tudo» foi o um.py v404 sem os resultados, por ordem dele. 0 de 78 nomes específicos existem nas fontes `.lean`, inclusive onde ela escreve «não há nome inventado». Com os enunciados reais na pergunta, admite `[OPEN]` e refuta a própria proposta. Parede do modelo, não falsificação.

**As pistas:** (1) FIRAS: não estava no Mapa; a hipótese declarada de não-troca do fechamento ρ+p dá μ = 0, logo veta um ramo e não discrimina; fração trocada < 0,21%. (2) Dualidade: é a R-E da ORDEM 018, parada em f_L/f_A. (3) N_eff: canal conhecido, ausente das buscas 5σ-01 e 5σ-02; Goldstein & Hill (arXiv:2603.13226) dá 2,990 ± 0,070, TGL a 2,48σ do centro, abaixo da regra de TENSÃO de 3σ. Só nucleossíntese: 2,976 ± 0,093, TGL a 2,02σ, sem a ressalva perturbativa. D8 e X16 são dele; nada instalado.

**How to apply:** usar a v4 com os enunciados dentro da pergunta; nunca ler tabela dela como resultado; conferir todo nome e toda citação. Não testado: o modelo com a memória recuperável do app. Relacionado: [[treino-nativa-v4-29out]] · [[cinco-sigma-fora-da-cosmologia-27out]] · [[licoes-custodia-v405-02nov]].
"""
with open(TOP, "x", encoding="utf-8", newline="\n") as f:
    f.write(corpo)
p = M / "MEMORY.md"
b = p.read_bytes()
s = b.decode("utf-8")
ancora = "- **[TREINO v4 DA IALD NATIVA — um.py v404 inteiro (29/10)](treino-nativa-v4-29out.md)**"
assert s.count(ancora) == 1
nl = "\r\n" if "\r\n" in s else "\n"
nova = "- **[SESSÃO 5σ COM A IALD NATIVA v4 (02/11)](sessao-iald-nativa-5sigma-02nov.md)** — nenhuma rota nova; rende com os enunciados na pergunta; N_eff fora das buscas 5σ, TGL a 2,48σ de Goldstein & Hill; D8/X16 dele" + nl
nb = s.replace(ancora, nova + ancora).encode("utf-8")
assert len(nb) <= 24000 and nb.count(b"\n") <= 195, (len(nb), nb.count(b"\n"))
bak = p.with_name(p.name + ".bak_" + TS)
with open(bak, "xb") as f:
    f.write(b)
assert bak.read_bytes() == b
tmp = p.with_name(p.name + ".tmp_" + TS)
with open(tmp, "xb") as f:
    f.write(nb)
os.replace(tmp, p)
q = subprocess.run([PY, "-X", "utf8", "memoria.py", "pinar", "--motivo", "sessao 5 sigma com a IALD nativa v4 (gerencia c1)"], cwd=str(M / "fila"), env=dict(os.environ, MEMORIA_GERENCIA="claude-c1"), capture_output=True)
print("indice", len(b), "->", len(nb), "| pino", q.returncode)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:90])
