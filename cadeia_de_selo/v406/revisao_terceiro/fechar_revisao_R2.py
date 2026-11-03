# -*- coding: utf-8 -*-
"""Revisor terceiro v406, R2: grava REVISAO_TERCEIRO_v406.json e .md (a R1 fica em _R1/). O sha16 do candidato e' LIDO do arquivo na hora."""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
O = R + "revisao_terceiro/"
cand = hashlib.sha256(open(R + "um_v406_candidato.py", "rb").read()).hexdigest()[:16]
cj = json.load(open(R + "CANDIDATO_v406.json", encoding="utf-8"))["sha16"]
assert cand == cj, ("candidato em disco != CANDIDATO_v406.json", cand, cj)
sha16 = lambda p: hashlib.sha256(open(R + p, "rb").read()).hexdigest()[:16]
rev = {p: sha16(p) for p in ("pos_rito/textos_v406.py", "artigo_pt_v406.pysnip", "artigo_en_v406.pysnip", "runtime_v406.py", "delta_v406.py", "registros_v406.py", "ESPERADOS_v406.json", "PINOS_BN_v406.json")}
quando = datetime.datetime.now().replace(microsecond=0).isoformat()
A = []
def ach(sev, onde, achado, evidencia, fix): A.append({"sev": sev, "onde": onde, "achado": achado, "evidencia": evidencia, "como_corrigir": fix})

ach("MEDIO", "pos_rito/textos_v406.py, _paragrafo_v406_de (linha 792: `ress = ... x.split(\":\")[0] ...`) e verificar_paragrafo_v406 (linha 839: `r_.split(\":\")[0] ... not in par`); sai no README do espelho e no site",
    "O paragrafo pronto do README/site corta cada ressalva no PRIMEIRO dois-pontos. Renderizado sobre o core do ensaio (10 ressalvas): (6) fica «R4/R5 da missao da bancada (identificacao do dispositivo fisico» (perde «seguem bloqueados ... NAO entram nesta versao»); (9) fica com o rotulo UNCOMPILED CANDIDATE e sem «a compilacao que vale e'...»; (10), a ressalva que corrige as frases «o kernel nao habita o certificado», termina «... dizem no presente que o kernel NAO habita o certificado de Fock, leia-se.» sem o que se le; (1) perde «so' na cunha»; (8) perde «os nomes das pedras sao do operador». O verificador usa o MESMO corte, entao nao pega (verificacao: []). Eu nao renderizei esta funcao na R1 e deixei passar a parte que ja existia (R4/R5).",
    "import de pos_rito/textos_v406.py + `_paragrafo_v406_de(core_ensaio)`; `verificar_paragrafo_v406(par, core, esp)` devolve []. A funcao `_limites` e `_ressalvas` ja usam o texto inteiro; so' o paragrafo do README ficou.",
    "Linha 792: `\"; \".join(\"(%d) %s\" % (i + 1, x) for i, x in enumerate(fe[\"ressalvas\"]))`; linha 839: `c_ = _sem_chaves(r_)` (texto inteiro). Nao muda o candidato nem o sha16; so' pos_rito/textos_v406.py. Re-renderizar sobre dry_v406/core_ensaio.json e ver as 10 inteiras.")
ach("BAIXO", "fechamento_v406.diz[1] e nao_diz[2] (entram no paragrafo do README/site)", "«fica para ele ler (regra do posto)» e «a gerencia le essa condicao a ele ao relatar a v406» sao instrucao interna de trabalho dentro de texto publico.", "paragrafo renderizado, item «O certificado de Fock esta habitado por construcao»", "Dizer no texto publico so' «a condicao ... NAO e' testada aqui (v407)»; a leitura ao operador e' ato da gerencia, fora do README.")
ach("BAIXO", "delta_v406.py LEITURA_V406[\"atrito\"]", "«a RESPOSTA DA GERENCIA, que ele leu e seguiu»: ratificacao dele nao esta nas 23 falas (a fala e36df7f1 usa «Atrito constante», o que nao e' ratificar a resposta).", "insumos/cunhagens/69e60a8c..., e36df7f1...", "Tirar «que ele leu e seguiu» ou citar a fala que ratifica.")
ach("BAIXO", "delta_v406.py ERRATA_E14 e RESSALVAS_V406[9]", "A lista dos lugares desatualizados diz «(estatuto, limites, diz, extras)» mas nao cita o VEREDITO de psibit_v395, que segue com o token CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE ao lado de status INHABITED_BY_physicalFockCertificate_V406.", "core_ensaio.json psibit_v395/verdict", "Acrescentar «veredito (o token UNINHABITED e' o nome da data)» a E14 e a ressalva 10.")

fechados = [
 "ALTO 1 (joint_contract_open_v394): FECHADO. psibit_v395 volta a `bool(open_joint_contract)` (True no ensaio) e ganha `joint_contract_items_still_open_v406` (3 itens por conteudo: sem «twenty-one»); rede_fock_v394.joint_contract_v406 escolhe o habitado por conteudo (1 item) e os 3 abertos; conferido no diff e no core do ensaio.",
 "MEDIO 1 (#eval): FECHADO. RESSALVAS_V406[4] com N_EVAL_BLOCOS = 56 e N_EVAL_MODULOS = 15 lidos do BUNDLE (i_eval_diff.py reproduz: 56 blocos, 15 modulos, 44 IO.println + 12 IO.FS, 92 linhas); no contrato (bundle.eval_removidos), no artigo PT e EN («O que entra»), na linha .md e no fechamento_v406.",
 "MEDIO 2 (frases no presente): FECHADO no artigo PT/EN («As quatro chaves»), na ERRATA_E14, na RESSALVAS_V406[9] e nos limites de fechamento_v406. NO README: ver o MEDIO acima (a ressalva 10 sai cortada).",
 "MEDIO 3 (hno): FECHADO. E15, LEITURA_V406[\"um_inscrito\"] e a errata do spec dizem «SOB a hipotese nomeada hno»; gamma_vacuum e exponential_zero sem ela (conferi: gamma_vacuum e exponential_zero nao tem hipotese); 8 ocorrencias de `hno` em cunhagens_v406 + fechamento_v406.",
 "BAIXOS 1 a 11 da R1: FECHADOS (specs comecam pelo estado vigente; .md «tres literais e uma medida»; RESSALVAS[8] do cabecalho, tambem no artigo; `_v406_certificado_habitado` exige all_verified: 2 casos novos, 56/56 ok; modalidade das falas mantida e `atrito` rotulado; E16 reescrita; «compile ...» inteira; o item do 4,44 carrega regra_do_4_44; diz[1] «quanto ao TERMO» e nao_diz com a condicao; 474 modulos + 475 fontes = 474 oleans + o topo, conferido contra o MANIFEST).",
]
n = {s: sum(1 for a in A if a["sev"] == s) for s in ("ALTO", "MEDIO", "BAIXO")}
_fc = json.load(open(O + "c_fail_closed_out.json", encoding="utf-8")); assert all(v.get("ok") is True for v in _fc.values() if "ok" in v)
ressalvas = [
 "Revisao R2: reli SO' o que a coordenacao disse que mudou, mais o que o conserto podia tocar. Reexecutei: AST dos intocados (iguais), diff das tres funcoes, fail-closed (56 casos, 0 falha; +7 do c2), kernel (301 == sandbox == BUNDLE, raiz e Audit iguais; o kernel nao mudou, logo a compilacao propria da R1 vale), hashes (so' pendente o B(n) pre-selo), gate (qg_closure igual a base), guardas (0), citacoes (operador: exatas), specs (so' as checagens ditas), e RENDERIZEI o paragrafo do README sobre o core do ensaio.",
 "Nao examinados (como na R1): B(n) pre-selo; instalar/reverter/rito; duracao do rito; as provas dos 301 modulos; a fisica; fechar_v406.py e leitura_v406.py; os textos de rito (handoff, linhagem) alem das funcoes lidas.",
 "Se o MEDIO for corrigido so' em pos_rito/textos_v406.py, o sha16 do candidato nao muda. Reler so' as linhas 792 e 839 e o paragrafo renderizado basta para a R3.",
 "Textos revisados (sha16 lidos ao fechar): " + "; ".join("%s %s" % kv for kv in rev.items()) + ". Se algum mudar, a revisao dele nao vale.",
]
rotas = ["consultar v406 -> kernel.fechamento_construir_tudo_programa_02nov (EM_CURSO)", "examinado na R2 (para registro pela gerencia): v406.revisao_terceiro.R2 -- verificacao dos consertos da R1 e renderizacao do paragrafo do README (achado: corte nos dois-pontos)"]
saida = {"aprovada": bool(n["ALTO"] == 0 and n["MEDIO"] == 0), "candidato_sha16": cand, "revisor": "revisor terceiro independente (agente Claude Sonnet, pedido da gerencia c1; nao construiu a v406)", "rodada": "R2", "quando": quando,
         "n_alto": n["ALTO"], "n_medio": n["MEDIO"], "n_baixo": n["BAIXO"], "achados": A, "achados_da_R1_fechados": fechados, "ressalvas": ressalvas, "rotas_examinadas": rotas}
json.dump(saida, open(O + "REVISAO_TERCEIRO_v406.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
L = ["# Revisao de terceiro da v406 (R2)", "",
     "Revisor independente (agente Claude Sonnet; nao construi a v406). Candidato `%s`, lido do arquivo ao fechar, %s. **Veredito: %s -- %d ALTO, %d MEDIO, %d BAIXO.** A R1 (1 ALTO, 3 MEDIO, 11 BAIXO) esta em `_R1/`." % (cand, quando, "APROVADA" if saida["aprovada"] else "AINDA NAO APROVADA: um MEDIO, fora do candidato", n["ALTO"], n["MEDIO"], n["BAIXO"]), "",
     "## 1. A R1: o que foi corrigido (conferido por script, nao pela fala da coordenacao)", ""]
L += ["- " + f for f in fechados]
L += ["", "## 2. O que ainda trava", ""]
for a in A:
    if a["sev"] == "MEDIO":
        L += ["- **MEDIO** [%s] %s" % (a["onde"].replace("`", ""), a["achado"]), "  - **Evidencia:** " + a["evidencia"], "  - **Corrigir:** " + a["como_corrigir"].replace("`", ""), ""]
L += ["## 3. BAIXOS novos (nao travam)", ""]
for i, a in enumerate([x for x in A if x["sev"] == "BAIXO"], 1):
    L.append("%d. [%s] %s **Corrigir:** %s" % (i, a["onde"].replace("`", ""), a["achado"], a["como_corrigir"]))
L += ["", "## 4. Ressalvas", ""] + ["- " + r for r in ressalvas]
L += ["", "## 5. Fecho", "", "`aprovada: %s`. O candidato `%s` esta limpo nos itens 1 a 6 do pedido; o unico bloqueio e' o corte das ressalvas no paragrafo do README (pos_rito/textos_v406.py, 2 linhas, sem regerar o candidato). Corrigido isso, a R3 e' so' reler essas duas linhas e o paragrafo renderizado." % (saida["aprovada"], cand)]
open(O + "REVISAO_TERCEIRO_v406.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("R2 gravada:", saida["aprovada"], n, cand, len(L), "linhas")
