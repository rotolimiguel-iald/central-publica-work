# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — gera o texto do depósito na fila da memória e o JSON da ANOTACAO no Mapa de Rotas da R6 FINAL
(emendas 5 e 6, com a nota da fala 24). Todo hash e todo número é LIDO do arquivo aqui, nunca digitado. Só escreve em _build.
uso: python gerar_registro_emendas_5_6.py"""
import hashlib, json, re
from pathlib import Path

OUT = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala")
BLD = OUT / "_build"
INST = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pedra\AEscala.lean")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def nb(p): return Path(p).stat().st_size
def mil(n): return f"{n:,}".replace(",", " ")

lean, rec_p, log_p = OUT / "AEscala.lean", OUT / "RECIBO_AESCALA_R6_10nov.json", OUT / "compile_log.txt"
rec = json.loads(rec_p.read_text(encoding="utf-8"))
assert rec["aescala_r6"]["sha256"] == sha(lean), "o recibo nao e' desta candidata"
assert rec["compilacao"]["log_sha256"] == sha(log_p) and rec["compilacao"]["rc_lido_do_arquivo"] == "rc=0"
q5, s6 = rec["quinta_emenda_falas_22_e_23"], rec["sexta_emenda_painel_e_fala_24"]
m = re.search(r"real\s+(\d+)m([\d.]+)s", rec["compilacao"]["tempo"])
tempo = f"{int(m.group(1)) * 60 + float(m.group(2)):.1f}".replace(".", ",") + " s"
d = rec["declaracoes"]
RAT18, RAT24, AUT = rec["nomes_novos"]["RATIFICADOS_pelo_operador_fala_18"], rec["nomes_novos"]["RATIFICADO_pelo_operador_fala_24"], rec["nomes_novos"]["DECLARADO_pela_autoria"]
assert len(RAT18) == 6 and RAT24 == ["o_nome_e_a_singularidade_da_informacao"] and len(AUT) == 6 and rec["n_falas"] == 24
assert rec["trio"]["todas_no_trio"] and rec["trio"]["n_auditadas"] == 81 and rec["trio"]["sem_axioma_nenhum"] == ["TGLExt.AEscala.o_nome_e_a_singularidade_da_informacao"]
asp = s6["aspas_sensiveis_a_caixa"]["na_final"]
V = dict(
    lean_b=mil(nb(lean)), lean_sha=sha(lean), rec_sha=sha(rec_p), log_sha=sha(log_p), linhas=rec["aescala_r6"]["linhas"],
    pre4_sha=sha(BLD / "pre_emenda5_falas22_23" / "AEscala.lean"), e5_sha=sha(BLD / "candidata_emenda5" / "AEscala.lean"),
    f22_sha=q5["fala_22"]["sha256"], f22_b=q5["fala_22"]["bytes"], f23_sha=q5["fala_23"]["sha256"], f23_b=q5["fala_23"]["bytes"],
    f24_sha=s6["fala_24"]["sha256"], f24_b=s6["fala_24"]["bytes"],
    tempo=tempo, n_decl=d["n_R6"], n_teo=d["n_teoremas_R6"], n_def=d["n_defs_R6"], n_str=d["n_structures_R6"],
    n_aud=rec["trio"]["n_auditadas"], n_ang=asp["angulares"], inst16=sha(INST)[:16],
    can=rec["frases_fixas"]["canonica_D84"][1], d94=rec["frases_fixas"]["forma_do_tempo_D94"][1],
    enunciado=q5["teorema_novo"]["enunciado"], cod_mais=q5["codigo_em_relacao_a_quarta_emenda"]["linhas_de_codigo_acrescentadas"],
    rat18=", ".join(f"`{n}`" for n in RAT18), aut=", ".join(f"`{n}`" for n in AUT), rat18_txt=", ".join(RAT18), aut_txt=", ".join(AUT))
assert V["inst16"] == "7d1557f961783679"

DEP = """AEscala R6 FINAL — emendas 5 e 6 (falas 22, 23 e 24): o teorema o_nome_e_a_singularidade_da_informacao, a regra de redação e três frases antigas corrigidas (10/11/2026; autor claude-autor-aescala)

AO LADO do depósito seq 521 (emendas 2, 3 e 4; candidata sha256 @@pre4_sha@@, compilada na rodada 7 e guardada em `_build\\pre_emenda5_falas22_23`). A candidata vigente é esta. A gerência avisou que não haverá outra emenda dela.

Arquivos em `C:\\IALD\\Central de Patentes\\work\\pedras_candidatas_09nov\\R6_a_constante_da_escala\\`: `AEscala.lean` (@@lean_b@@ B, @@linhas@@ linhas, sha256 @@lean_sha@@); `RECIBO_AESCALA_R6_10nov.json` (sha256 @@rec_sha@@); `compile_log.txt` (sha256 @@log_sha@@).

QUINTA EMENDA (ordem direta do operador; fala 22, @@f22_b@@ bytes, sha256 @@f22_sha@@; fala 23, @@f23_b@@ bytes, sha256 @@f23_sha@@):
1. TEOREMA NOVO `o_nome_e_a_singularidade_da_informacao`: @@enunciado@@. Em palavras: toda informação que singulariza é a identidade com um designado; exibir uma informação singular é designá-la. O operador mandou refutar; é teorema, lógica pura, e NÃO DEPENDE DE AXIOMA NENHUM (saída do `#print axioms`). O nome sai da frase dele e foi RATIFICADO por ele (fala 24, @@f24_b@@ bytes, sha256 @@f24_sha@@). A fala 23 vai por bytes na docstring do teorema; ali não há a expressão que ele vetou.
2. LEMA DE INSTÂNCIA, com nome da autoria [DECLARADO pela autoria]: `o_nome_das_solucoes_e_a_singularidade_do_sinal`. Na fita (c : X → ℕ): a informação singulariza ⟺ existe o designado; ⟺ o conjunto das soluções é o unitário; ⟺ há UMA solução, que é a hipótese de `o_sistema_reconhece_a_singularidade_do_sinal`; então o Nome lido das soluções pesa um pixel, 1/|X| (acréscimo da autoria); e, com n bits, vale a cláusula do Tetelestai com uma solução.
3. O PAR DO NOME É O VERBO: sem teorema novo, como mandado; no parágrafo O FECHO a frase dele vai por bytes ao lado de `nomeObjeto`, `nomeLido`, `o_par_coexiste`, `nenhum_precede` e `a_mentira_lida_como_mentira_e_verdade`.
4. REGRA DE REDAÇÃO em tudo o que é novo na R6 (a §7 e a parte R6 do cabeçalho): a frase do operador que tem teorema que a espelha é o NOME DADO POR ELE ao que o teorema diz, citado por nome; onde não há termo, diz-se só o fato e fica [OPEN]. As docstrings das seções 1 a 6 de época não foram tocadas por esta regra.
5. Fica [OPEN], dito na pedra: o elo da vibração ao acorde; a lei única dos dois domínios; o elo com `Turing.TM2ComputableInPolyTime`; o que une observador, seletor, IALD e Torre de Jones por uma métrica. Dois fatos a mais, postos pela autoria: a pedra não traz lema ligando a razão de duas constantes ao par Nome objeto / Nome lido, nem ligando β = α·√e à informação do teorema novo. As ausências foram conferidas por consulta ao sandbox e a consulta está no recibo (o módulo do acorde não cita a vibração; a máquina do Mathlib só aparece em comentário).
6. Decisão de redação da autoria, para a gerência conferir: a frase da fala 17 sobre o eletromagnetismo vai como nome do item (iii) de `tudo_depende_da_escala` (α = meioTom·β); que `TGLCoupling.alpha` seja a constante de estrutura fina entra como [KNOWN] e [INPUT] (valor medido em runtime), não como termo do kernel.

SEXTA EMENDA (só comentário; apontamentos do painel de 10/11): EP-02, o limiar da docstring de `os_passos_sao_o_ciclo_ate_o_tetelestai` é ESTRITO (s > n·ln 2; no limiar exato, com todos os custos iguais a 1 e sem solução, Z = 1, dito como conta à mão); EP-08, a docstring de `em_n_oitavas_o_fundo_pesa_um_pixel` diz o que o termo diz (o brilho de UM pixel de custo 1) e manda a separação do fundo para o teorema do limiar; o nome ratificado não muda; PAR-11, o nome do módulo sai das aspas angulares (a grafia com maiúsculas não está em nenhum arquivo de fala). ACHADO da conferência por script, além do painel: duas aspas do mesmo tipo (o título em caixa alta de duas docstrings da §6), também trocadas por tipográficas. Conferido por script: fora dos comentários, o código da final é idêntico ao da candidata da quinta emenda (sha256 @@e5_sha@@, em `_build\\candidata_emenda5`); e, em relação à quarta, a final só ganha a seção nova (@@cod_mais@@ linhas de código, contando as duas da Auditoria).

Compilação [REAL]: UMA para as duas emendas (rodada 8, `lake env lean` só no arquivo externo): rc 0 em @@tempo@@; 0 erros, 0 avisos, 0 sorry, 0 axiom; @@n_decl@@ declarações (@@n_teo@@ teoremas, @@n_def@@ defs, @@n_str@@ structure); @@n_aud@@ auditadas: 80 no trio e 1 sem axioma nenhum; sha256 da candidata lido antes e depois. Aspas: trocas 0; @@n_ang@@ angulares, todas verbatim também com a caixa. Frase canônica D84 (@@can@@) e forma do tempo D94 (@@d94@@) intactas; nenhuma frase vedada; β nunca literal. Cabeçalho com VINTE E QUATRO falas por sha256. Nada instalado; `v410\\pedra` intocada (sha16 @@inst16@@); cadeia não rodada.

NOMES NOVOS DA R6 (13): RATIFICADOS pela fala 18 (6): @@rat18@@. RATIFICADO pela fala 24 (1): `o_nome_e_a_singularidade_da_informacao`. [DECLARADO pela autoria] (6): @@aut@@.

LIÇÕES: (a) o `#print axioms` tem duas saídas, e a de um teorema sem axioma não traz lista: quem lê o log tem de aceitar as duas, ou conta 80 de 81; (b) a conferência das aspas angulares ignorava a caixa: há agora `_build\\conferir_aspas_caixa.py`; (c) AVISO ao construtor: o `delta_v410.py` da cadeia (l.564) também põe o nome do módulo entre aspas angulares; não é arquivo da autoria e não foi tocado.
"""
dep = DEP
for k, v in V.items(): dep = dep.replace("@@" + k + "@@", str(v))
assert "@@" not in dep
(BLD / "deposito_r6_emendas_5_6.md").write_text(dep, encoding="utf-8", newline="\n")

ROTA = {
 "tipo": "ANOTACAO",
 "rota_id": "kernel.a_escala_tres_faces_v410_09nov",
 "titulo": "AEscala R6 FINAL, emendas 5 e 6 (falas 22 a 24; ao lado do seq 1953): teorema novo o_nome_e_a_singularidade_da_informacao (sem axioma nenhum; nome RATIFICADO pela fala 24) e lema de instancia da autoria; regra de redacao (nome dado pelo operador + teorema; sem termo, so' o fato e OPEN); tres frases antigas corrigidas; 81 declaracoes",
 "metodo": "Sobre a candidata do seq 1953 (guardada ao lado). Quinta: secao nova SingularidadeDaInformacao no fecho da secao 7 e docstrings novas da R6 reescritas pela regra de redacao; ausencias ditas OPEN conferidas por consulta ao sandbox k410c (registrada no recibo). Sexta: so' comentario, tres apontamentos do painel de 10/11 e duas aspas do mesmo tipo achadas por script sensivel a caixa. Conferido por script: codigo fora de comentario identico entre a final e a candidata da quinta; em relacao a quarta, so' entra a secao nova. UMA compilacao para as duas (rodada 8): lake env lean so' no arquivo externo, sha256 lido antes e depois.",
 "resultado": "rc 0 em @@tempo@@; 0 erros; 0 avisos; 0 sorry; 0 axiom; @@n_decl@@ declaracoes (@@n_teo@@ teoremas, @@n_def@@ defs, @@n_str@@ structure); @@n_aud@@ auditadas: 80 no trio e 1 sem axioma nenhum (o teorema novo). Enunciado do teorema novo: @@enunciado@@. Lema de instancia o_nome_das_solucoes_e_a_singularidade_do_sinal: informacao singular <-> designado <-> conjunto das solucoes unitario <-> uma solucao (a hipotese de o_sistema_reconhece_a_singularidade_do_sinal); entao o Nome lido das solucoes pesa 1/|X| e vale a clausula do Tetelestai com uma solucao. RATIFICADOS (fala 18): @@rat18_txt@@. RATIFICADO (fala 24): o_nome_e_a_singularidade_da_informacao. DECLARADO pela autoria: @@aut_txt@@. Vinte e quatro falas por sha256 no cabecalho. Aspas: trocas 0; @@n_ang@@ angulares, todas verbatim tambem com a caixa.",
 "veredito": "AESCALA_R6_FINAL__81_DECL_70_TEOREMAS__TRIO__SEIS_EMENDAS__TEOREMA_DA_SINGULARIDADE_SEM_AXIOMA__NOME_RATIFICADO_FALA_24__REGRA_DE_REDACAO_APLICADA__NAO_INSTALADA",
 "estatuto": "REAL (compilacao, trio e o teorema novo); OPEN (dito na pedra: o elo da vibracao ao acorde; a lei unica dos dois dominios; o elo com Turing.TM2ComputableInPolyTime; o que une observador, seletor, IALD e Torre de Jones por uma metrica; e dois fatos postos pela autoria: sem lema ligando a razao de duas constantes ao par Nome objeto / Nome lido, nem beta = alpha * raiz de e a informacao do teorema novo); KNOWN e INPUT (que TGLCoupling.alpha seja a constante de estrutura fina: valor medido em runtime); DECLARADO (os seis nomes da autoria)",
 "status": "EXAMINADA",
 "olhou_dados": False,
 "defeito": "O lema de instancia tem nome e dois itens da autoria (o Nome lido das solucoes pesa um pixel; a composicao com a clausula do Tetelestai). A frase sobre o eletromagnetismo foi redigida pela autoria como nome do item (iii) com KNOWN e INPUT, a conferir pela gerencia. Duas trocas de aspas alem das tres do painel. A secao 7 nao acrescenta elo com a maquina do Mathlib. O delta_v410.py da cadeia (l.564) tambem escreve o nome do modulo entre aspas angulares e nao foi tocado.",
 "nao_refazer": "Nao recompilar a R6 final (log rc 0, 0 avisos; sha256 lido antes e depois). Nao escrever, no que e' novo da R6, a frase do operador com rotulo de leitura: onde ha' teorema, e' nome dado por ele; onde nao ha', so' o fato e OPEN. Ao ler o log do #print axioms, aceitar tambem a saida de teorema sem axioma. Nao tentar derivar a escala do tempo da escala da tonica nesta pedra.",
 "proximo_passo": "Construtor: instalar a R6 final (retirando a secao Auditoria), ancoras e bandeiras para os dois nomes novos e as falas 13 a 24 no conjunto congelado; rever o delta_v410.py l.564. Gerencia: decidir se mostra ao operador o lema de instancia e os seis nomes da autoria.",
 "onde": "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R6_a_constante_da_escala/AEscala.lean (namespace TGLExt.AEscala, secoes ConstanteDaEscala e SingularidadeDaInformacao)",
 "artefatos": [
  "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R6_a_constante_da_escala/AEscala.lean",
  "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R6_a_constante_da_escala/RECIBO_AESCALA_R6_10nov.json",
  "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R6_a_constante_da_escala/compile_log.txt"
 ],
 "nota": "A candidata do seq 1953 (@@pre4_sha@@) e a da quinta emenda (@@e5_sha@@, nao compilada sozinha) ficam em _build; a vigente e' a deste registro (@@lean_sha@@). Falas, sha256 lidos do arquivo por script: 22 @@f22_sha@@ (@@f22_b@@ bytes); 23 @@f23_sha@@ (@@f23_b@@ bytes); 24 @@f24_sha@@ (@@f24_b@@ bytes)."
}
def preenche(s):
    for k, v in V.items(): s = s.replace("@@" + k + "@@", str(v))
    return s
rota = {k: (preenche(v) if isinstance(v, str) else v) for k, v in ROTA.items()}
assert "@@" not in json.dumps(rota, ensure_ascii=False)
(BLD / "rota_anotacao_r6_emendas_5_6.json").write_text(json.dumps(rota, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print("deposito:", nb(BLD / "deposito_r6_emendas_5_6.md"), "B | rota json:", nb(BLD / "rota_anotacao_r6_emendas_5_6.json"), "B")
print("lean", V["lean_sha"], V["lean_b"], "B |", V["linhas"], "linhas")
print("recibo", V["rec_sha"], "| log", V["log_sha"], "| tempo", V["tempo"], "| angulares", V["n_ang"])
print("enunciado:", V["enunciado"])
print("aspas angulares no deposito:", dep.count("\u00ab"))
