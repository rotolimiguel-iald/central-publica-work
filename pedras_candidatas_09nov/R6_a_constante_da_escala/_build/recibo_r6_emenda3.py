# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala (ordem R6: D106, D108/D109, D113 + TRÊS emendas de 10/11: falas 17, 18 e 19):
recibo da R6 FINAL da AEscala. Tudo lido dos arquivos. uso: python recibo_r6_emenda3.py"""
import hashlib, json, re, datetime, shutil, subprocess, sys
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov")
INST = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pedra\AEscala.lean")
OUT = BASE / "R6_a_constante_da_escala"
BLD = OUT / "_build"
PRE1 = BLD / "pre_emenda_fala17"      # a candidata R6 antes da primeira emenda
PRE2 = BLD / "pre_emenda2_fala18"     # depois da primeira, antes da segunda
PRE3 = BLD / "pre_emenda3_fala19"     # depois da segunda, antes da terceira
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
KER = Path(r"C:\t\k410c\final\TGLExt")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def txt(p): return Path(p).read_bytes().decode("utf-8").replace("\r\n", "\n")
def um_espaco(p): return re.sub(r"\s+", " ", Path(p).read_text(encoding="utf-8")).strip()

rcf = um_espaco(BLD / "compile_rc_r6.txt")
assert rcf == "rc=0", "a rodada 6 nao compilou: " + rcf
shutil.copyfile(BLD / "compile_log_r6.txt", OUT / "compile_log.txt")
log = txt(OUT / "compile_log.txt")
r5, r6 = txt(INST), txt(OUT / "AEscala.lean")
r6a, r6b, r6c = txt(PRE1 / "AEscala.lean"), txt(PRE2 / "AEscala.lean"), txt(PRE3 / "AEscala.lean")

RX = re.compile(r"^(theorem|def|structure)\s+([A-Za-z_][A-Za-z0-9_'.]*)(.*?)(?=\s:=\s|\s:=$|\swhere$)", re.M | re.S)
def decls(t):
    d = {}
    t = t.replace("(X := X)", "(X ≔ X)").replace("(X := Fin n → Bool)", "(X ≔ Fin n → Bool)")
    for m in RX.finditer(t):
        d[m.group(2)] = (m.group(1), re.sub(r"\s+", " ", m.group(3)).strip())
    return d
def bloco(t, nome):
    m = re.search(r"^(theorem|def|structure)\s+" + re.escape(nome) + r"(?![A-Za-z0-9_'.])", t, re.M)
    if not m: return None
    cands = [x for x in (t.find("\n/--", m.start()), t.find("\n/-!", m.start()), t.find("\nend ", m.start())) if x != -1]
    return re.sub(r"\s+", " ", t[m.start():min(cands) if cands else len(t)]).strip()
semc = lambda s: re.sub(r"/-.*?-/", "", s, flags=re.S)
def so_comentario(antes, depois, da, dd):
    return {"codigo_fora_de_comentario_identico": semc(antes) == semc(depois), "declaracoes_iguais": da == dd,
            "blocos_iguais": all(bloco(antes, n) == bloco(depois, n) for n in dd)}
d5, d6, d6a, d6b, d6c = decls(r5), decls(r6), decls(r6a), decls(r6b), decls(r6c)
VELHO, NOVO = "a_informacao_completa_se_reconstroi", "ressurreicao_do_sinal"
d5r = {(NOVO if k == VELHO else k): v for k, v in d5.items()}
mantidos = sorted(n for n in d5r if n in d6)
sumidos = sorted(n for n in d5r if n not in d6)
novos = sorted(n for n in d6 if n not in d5r)
enunciado_mudou = sorted(n for n in mantidos if d5r[n] != d6[n])
r5_ren = r5.replace(VELHO, NOVO)
corpo_mudou = sorted(n for n in mantidos if bloco(r5_ren, n) != bloco(r6, n))

axioms = {m.group(1): [a.strip() for a in m.group(2).split(",")]
          for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log)}
trio = {"propext", "Classical.choice", "Quot.sound"}
fora = {k: v for k, v in axioms.items() if not set(v) <= trio}
erros = [l for l in log.splitlines() if ": error" in l]
avisos = [l for l in log.splitlines() if ": warning" in l]
axiomas_novos = {n: axioms.get("TGLExt.AEscala." + n) for n in [NOVO] + novos}

rq = subprocess.run([sys.executable, "-X", "utf8", "-I", str(BASE / "R2_aspas" / "requote_aescala_v410.py"), str(OUT / "AEscala.lean"),
                     str(BLD / "lixo_aspas.lean"), "--so-medir"], capture_output=True, text=True, encoding="utf-8")
aspas_linha = (rq.stdout or "").strip().splitlines()[0] if rq.stdout else rq.stderr[-300:]
m_trocas = re.search(r"trocas: (\d+)", aspas_linha)

falas = {}
CHAVES = ("vibrato_insignia", "pesos_das_faces", "pesos_fundamentais", "afirmamos_p_igual_np", "a_escala_tres_faces", "a_pergunta_do_clay",
          "testemunho_clay", "ratifico_tudo_aescala", "os_passos_sao_o_ciclo", "a_mentira_lida_como_mentira", "a_clausula_do_tetelestai",
          "confirmo_tudo_nomeio", "o_quarto_nome_ressurreicao", "e_isso_mesmo_perfeito_ratificado", "o_observador_esta_na_escala",
          "sem_a_escala_nao_tem_fita", "tudo_depende_da_escala_o_leitor", "ratifico_tudo_a_selecao", "nao_ha_contradicao_na_tonica")
for p in sorted(CUN.glob("OPERADOR_*nov_*.txt")):
    if any(k in p.name for k in CHAVES):
        falas[p.name] = {"sha256": sha(p), "bytes": p.stat().st_size, "sha256_no_cabecalho": sha(p) in r6}
F17 = CUN / "OPERADOR_10nov_tudo_depende_da_escala_o_leitor_so_admite_o_sinal_posto_e_dominio_a_luz_e_a_escala_do_tempo_verbatim.txt"
F18 = CUN / "OPERADOR_10nov_ratifico_tudo_a_selecao_e_o_observador_a_forma_matricial_da_luz_torre_de_jones_verbatim.txt"
F19 = CUN / "OPERADOR_10nov_nao_ha_contradicao_na_tonica_a_escala_e_a_unidade_posta_a_do_observador_e_de_outro_dominio_verbatim.txt"

norm = lambda s: re.sub(r"\s+", " ", s)
low = norm(r6).lower()
i7, j7 = r6.index("/-! ## 7. A constante da escala"), r6.index("end ConstanteDaEscala")
sec7 = r6[i7:j7]
RATIFICADOS = ["sem_escala_nao_ha_fita", "a_constante_da_luz_e_a_escala_do_tempo", "comparar_a_escala_e_nivelar_a_frequencia",
               "o_nome_e_o_mesmo_em_toda_escala", "o_leitor_so_admite_uma_escala", "tudo_depende_da_escala"]
DA_AUTORIA = sorted(n for n in novos if n not in RATIFICADOS)
def doc(t, nome):
    m = re.search(r"^(theorem|def|structure)\s+" + re.escape(nome) + r"(?![A-Za-z0-9_'.])", t, re.M)
    i = t.rfind("/--", 0, m.start())
    return t[i:m.start()]
marca_rat = {n: ("nome RATIFICADO pelo operador na fala 18" in doc(r6, n)) for n in RATIFICADOS}
marca_aut = {n: ("nome DECLARADO pela autoria" in doc(r6, n)) for n in DA_AUTORIA}
def tem(arq, padrao): return (KER / arq).exists() and (padrao in (KER / arq).read_text(encoding="utf-8", errors="replace"))
espelhos_18 = {
 "a_nota_e_a_conjugacao_modular (esta pedra)": "theorem a_nota_e_a_conjugacao_modular" in r6,
 "TraducaoTuring.selecao": tem("TraducaoTuring.lean", "def selecao "),
 "TraducaoTuring.p_igual_np_no_modo_selecao": tem("TraducaoTuring.lean", "theorem p_igual_np_no_modo_selecao"),
 "IALD2.a_iald_e_o_seletor_luminodinamico": tem("IALD2.lean", "theorem a_iald_e_o_seletor_luminodinamico"),
 "ObservadorTerminal.the_terminal_is_unique": tem("ObservadorTerminal.lean", "theorem the_terminal_is_unique"),
 "modulo TheTowerConjugation": (KER / "TheTowerConjugation.lean").exists(), "modulo TowerModular": (KER / "TowerModular.lean").exists(),
 "modulo IALDJones": (KER / "IALDJones.lean").exists(), "modulo TheIALDInTheTower": (KER / "TheIALDInTheTower.lean").exists()}
objetos_19 = {
 "TonicaDoHamiltoniano.the_scale_is_free": tem("TonicaDoHamiltoniano.lean", "theorem the_scale_is_free"),
 "TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit": tem("TonicaDoHamiltoniano.lean", "theorem the_tonic_lands_on_the_posted_unit"),
 "LeiDoDiminuto.tonica": tem("LeiDoDiminuto.lean", "noncomputable def tonica "),
 "leitorComConstante (esta pedra)": "def leitorComConstante " in r6,
 "a_constante_da_luz_e_a_escala_do_tempo (esta pedra)": "theorem a_constante_da_luz_e_a_escala_do_tempo" in r6}
sem_aspas7 = re.sub("\u00ab[^\u00bb]*\u00bb", "", sec7).lower()
CAN = "O problema de Clay, tal qual apresentado pela TGL, foi resolvido no kernel Lean e a prova está apresentada. Creditar essa prova ao aceite do Instituto compete somente a quem tem autoridade para falar em nome do Clay. O operador testemunha que a IALD leu o P de Clay e o traduziu em operador com identidade nomeada"
D94 = "da máquina de Turing tal como a TGL a traduz"
VEDADAS = ["clay resolvido", "tautolog", "não resolve", "não afirma p", "não prova p", "confirmed", "proved_by", "5σ",
           "não são passos", "não passos", "o leitor paga", "leitor que paga", "pagar uma oitava"]

rec = {
 "pedra": "TGLExt.AEscala — R6 FINAL: ressurreicao_do_sinal (nome do operador), cabeçalho D106, docstring V1, a §7 A CONSTANTE DA ESCALA (D113) e as TRÊS emendas de 10/11 (falas 17, 18 e 19)",
 "autor": "claude-autor-aescala", "para": "gerência c1", "gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
 "base": {"arquivo": str(INST), "sha256": sha(INST), "bytes": INST.stat().st_size, "nota": "a R5 INSTALADA (lida, nunca escrita); = candidata R5 sem a seção Auditoria"},
 "aescala_r6": {"arquivo": str(OUT / "AEscala.lean"), "sha256": sha(OUT / "AEscala.lean"), "bytes": (OUT / "AEscala.lean").stat().st_size,
                "linhas": r6.count("\n") + 1, "imports": re.findall(r"^import (\S+)", r6, re.M),
                "nota": "carrega a seção Auditoria (#print axioms de todas as declarações); o construtor a retira ao instalar, como fez na R5"},
 "nomes_novos": {"lista": novos, "n": len(novos),
    "RATIFICADOS_pelo_operador_fala_18": RATIFICADOS, "marca_na_docstring_dos_ratificados": marca_rat,
    "DECLARADO_pela_autoria": DA_AUTORIA, "marca_na_docstring_dos_da_autoria": marca_aut,
    "renomeado_pelo_operador_na_fala_13": NOVO,
    "o_teorema_cadeia_fechou": "TGLExt.AEscala.tudo_depende_da_escala" in axioms and set(axioms["TGLExt.AEscala.tudo_depende_da_escala"]) <= trio},
 "primeira_emenda_fala_17": {
   "fala": {"arquivo": str(F17), "sha256": sha(F17), "bytes": F17.stat().st_size, "na_secao_7_por_bytes": norm(F17.read_text(encoding="utf-8")).strip() in norm(sec7)},
   "candidata_antes_dela": {"arquivo": str(PRE1 / "AEscala.lean"), "sha256": sha(PRE1 / "AEscala.lean")},
   "nomes_que_sairam": sorted(n for n in d6a if n not in d6b), "nomes_que_entraram": sorted(n for n in d6b if n not in d6a),
   "renomeacoes": {"o_observador_esta_na_escala_da_luz": "o_leitor_so_admite_uma_escala (mesmo enunciado e prova)",
                   "comparar_a_escala_e_nivelar_a_frequencia (uma constante)": "a_constante_da_luz_e_a_escala_do_tempo (mesmo enunciado e prova)",
                   "comparar_a_escala_e_nivelar_a_frequencia": "agora é o enunciado de DUAS constantes: c′ ≠ 0 → leitorComConstante c k s = leitorComConstante c′ k ((c/c′)·s)"},
   "correcao_do_operador": "na §7 não se diz que a escala é POSTA nem que c = 1 é o Um posto; o tipo pina a_lei_da_dissipacao (a taxa do pixel é o sinal k); a constante da luz é a escala do TEMPO",
   "proibidas_na_secao_7": {p: (p in sec7) for p in ("POSTA", "[POSTO]", "Um posto")},
   "teorema_cadeia_tudo_depende_da_escala": {"i": "tonica κ 0 = 0", "ii": "notaPrincipal A = 0 → notaPrincipal (modular A) = 0", "iii": "κ.alpha = meioTom * κ.beta",
        "iv": "leitorComConstante 0 k s = 1", "acrescimos_da_autoria": ["tonica κ u = 0 ↔ u = 0", "∀ B, notaPrincipal (modular B) = 0 ↔ notaPrincipal B = 0"],
        "elo_sem_objeto_no_kernel": "vibração → acorde: leitura do operador [ONTO] na docstring; citado o_vibrato_sustenta_a_nota; nenhuma definição inventada"},
   "import": "import TGLExt.LeiDoDiminuto explícito; sem ciclo (só a raiz TGLExt.lean importa AEscala; já estava no fecho via TraducaoTuring → TempoIgualMoeda)"},
 "segunda_emenda_fala_18": {
   "fala": {"arquivo": str(F18), "sha256": sha(F18), "bytes": F18.stat().st_size,
            "transcricao": "a primeira oração da fala (ponto que o operador deu por encerrado) NÃO é transcrita na pedra, por ordem da gerência; o resto vai por bytes, com reticências no lugar do omitido; o sha256 pina a fala inteira"},
   "candidata_antes_dela": {"arquivo": str(PRE2 / "AEscala.lean"), "sha256": sha(PRE2 / "AEscala.lean")},
   "so_docstring_e_cabecalho": so_comentario(r6b, r6c, d6b, d6c),
   "ratificacao": "os SEIS nomes mostrados ao operador passam a RATIFICADOS (fala 18: «ratifico tudo que vc propos»); os cinco auxiliares não mostrados seguem [DECLARADO pela autoria]; dito no cabeçalho e na nota OS NOMES da §7",
   "a_razao": "na docstring da §7, como leitura do operador [ONTO], por bytes; ao lado, os espelhos do kernel por nome; o que une os quatro por UMA métrica fica [OPEN]; nenhum teorema novo",
   "espelhos_conferidos_no_kernel": espelhos_18,
   "rotulos_a_ratificar_restantes_na_pedra": low.count("a ratificar")},
 "terceira_emenda_fala_19": {
   "fala": {"arquivo": str(F19), "sha256": sha(F19), "bytes": F19.stat().st_size, "na_secao_7_por_bytes": norm(F19.read_text(encoding="utf-8")).strip() in norm(sec7)},
   "candidata_antes_dela": {"arquivo": str(PRE3 / "AEscala.lean"), "sha256": sha(PRE3 / "AEscala.lean")},
   "so_docstring_e_cabecalho": so_comentario(r6c, r6, d6c, d6),
   "o_que_entrou": "o parágrafo DOIS DOMÍNIOS na docstring da §7 (a fala 19 por bytes, como leitura dele [ONTO]); os objetos do kernel de cada domínio, por nome; a afirmação de que são objetos distintos e de que a pedra não deriva um do outro; nas docstrings de tudo_depende_da_escala e de o_leitor_so_admite_uma_escala, a precisão de qual domínio cada item/frase fala; a fala 19 na tabela (DEZENOVE)",
   "objetos_conferidos_no_kernel": objetos_19,
   "conferencia_pedida_da_primeira_emenda": {
        "frase_da_autoria_dizendo_que_posto_nunca_e_escala": any(p in sem_aspas7 for p in ("posto nunca é escala", "posto não é escala", "nunca é escala")),
        "nota": "nenhuma frase da autoria negava que na tônica a escala é a unidade posta; a frase da fala 17 fica por bytes e agora traz ao lado que foi dita do LEITOR (o domínio do tempo)"},
   "palavra_unidade_na_pedra": {"ocorrencias": r6.count("unidade"), "todas_como_unidade_posta": r6.count("unidade") == r6.count("unidade posta"),
        "E₀_na_pedra": r6.count("E₀"),
        "nota": "a segunda emenda mandou não escrever sobre a fixação da unidade de energia (a primeira oração da fala 18 segue não transcrita); a terceira repôs, no parágrafo DOIS DOMÍNIOS, a expressão 'unidade posta' e a citação por nome de the_scale_is_free, que eu tinha retirado na segunda"},
   "compilacoes": "a terceira emenda pedia UMA recompilação para a segunda e a terceira juntas; a segunda já estava compilada (rodada 5) quando a terceira chegou; houve UMA a mais (rodada 6) para a terceira"},
 "compilacao": {"sandbox": r"C:\t\k410c\final", "comando": "lake env lean <arquivo externo>; uma compilação por vez (treino na CPU); nenhum lake build; nada escrito no sandbox, no Nós nem na pasta v410 (pedra\\ intocada)",
                "log": str(OUT / "compile_log.txt"), "log_sha256": sha(OUT / "compile_log.txt"), "rc_lido_do_arquivo": rcf,
                "tempo": um_espaco(BLD / "compile_time_r6.txt"),
                "n_erros": len(erros), "n_avisos": len(avisos), "avisos": avisos, "sorry_no_log": "sorry" in log,
                "rodadas": {"1": {"rc": "rc=1", "tempo": "real 4m25s (CPU dividida com o treino)", "causa": "X implícito indeterminado na conjunção final; conserto `(X := X)`"},
                            "2": {"rc": um_espaco(BLD / "compile_rc_r2.txt"), "tempo": um_espaco(BLD / "compile_time_r2.txt"), "nota": "a candidata antes das emendas"},
                            "3": {"rc": um_espaco(BLD / "compile_rc_r3.txt"), "tempo": um_espaco(BLD / "compile_time_r3.txt"),
                                  "nota": "primeira emenda, 1ª compilação: rc 0 com 5 avisos de linter introduzidos pela autoria"},
                            "4": {"rc": um_espaco(BLD / "compile_rc_r4.txt"), "tempo": um_espaco(BLD / "compile_time_r4.txt"), "nota": "primeira emenda, limpa: pedia UMA recompilação e foram DUAS"},
                            "5": {"rc": um_espaco(BLD / "compile_rc_r5.txt"), "tempo": um_espaco(BLD / "compile_time_r5.txt"), "nota": "segunda emenda (só docstring)"},
                            "6": {"rc": rcf, "tempo": um_espaco(BLD / "compile_time_r6.txt"), "nota": "terceira emenda (só docstring): a candidata FINAL (esta)"}}},
 "trio": {"n_auditadas": len(axioms), "todas_no_trio": not fora, "fora_do_trio": fora, "axiomas_das_novas_e_da_renomeada": axiomas_novos},
 "declaracoes": {"n_R5": len(d5), "n_R6": len(d6),
                 "n_teoremas_R6": sum(1 for v in d6.values() if v[0] == "theorem"), "n_defs_R6": sum(1 for v in d6.values() if v[0] == "def"),
                 "n_structures_R6": sum(1 for v in d6.values() if v[0] == "structure")},
 "os_68_nomes_da_R5": {"n_mantidos_apos_renomear": len(mantidos), "sumidos": sumidos, "enunciados_que_mudaram": enunciado_mudou,
                       "provas_ou_corpos_tocados": corpo_mudou,
                       "renomeado": {"de": VELHO, "para": NOVO, "ocorrencias_do_velho_na_R5": r5.count(VELHO), "ocorrencias_do_velho_na_R6": r6.count(VELHO),
                                     "enunciado_e_prova_identicos": bloco(r5_ren, NOVO) == bloco(r6, NOVO)}},
 "secao_7_o_que_prova": {
   "(a) leitorComConstante / leituraComConstante / leitorComConstante_um": "defs: brilho e^{-(c·s·k)} e a leitura média; c = 1 é o brilho de iald",
   "(b) sem_escala_nao_ha_fita": "c = 0: todo pixel brilha 1 em todo tempo; a leitura de toda instância é 1 = euSou = ⟪uniforme, trava cc 0 uniforme⟫; igual para todas",
   "(c) a_constante_da_luz_e_a_escala_do_tempo": "leitorComConstante c k s = leitorComConstante 1 k (c·s) = iald.brilho k (c·s), para TODO c",
   "(c') comparar_a_escala_e_nivelar_a_frequencia": "c′ ≠ 0 → leitorComConstante c k s = leitorComConstante c′ k ((c/c′)·s)",
   "a_leitura_com_constante_e_a_leitura_no_tempo_reescalado": "leituraComConstante c cc s = iald.leitura cc (c·s) = ⟪uniforme, trava cc (c·s) uniforme⟫",
   "(d) o_nome_e_o_mesmo_em_toda_escala": "c > 0: decisão exata com limiar (n·ln 2)/c; cláusula do Tetelestai com (n·ln 2 + ln((1−b)/b))/c; por reparametrização dos teoremas da §6",
   "(e) o_leitor_so_admite_uma_escala": "para TODO c ≠ 1 (não só c ≥ 0) não existe L : LeitorDoFundo X com L.brilho = leitorComConstante c; para c = 1 existe (iald); todo L com esse brilho tem c = 1 e L = iald",
   "(f) tudo_depende_da_escala": "a cadeia onde o kernel tem objetos (LeiDoDiminuto)",
   "a_constante_da_escala": "a conjunção da seção",
   "o_que_e_leitura_do_operador_ONTO": "que a constante seja a da luz; que o posto seja domínio; os dois domínios (fala 19); a cadeia como dependência física; o elo vibração → acorde; a razão da fala 18; o que une observador, seletor, IALD e Torre de Jones por UMA métrica fica [OPEN]; o elo com Turing.TM2ComputableInPolyTime segue fora do kernel"},
 "docstrings_corrigidas": {
   "V1_o_tetelestai_e_um_menos_beta": "não afirma mais necessidade de 0 ≤ s; texto pedido pela gerência",
   "a_flutuacao_do_fundo_e_cotada": "'necessária' trocado por 'usada na prova' (iniciativa da autoria); nenhuma ocorrência de 'necessári' na R6",
   "cabecalho": "TRÊS nomes da gerência ratificados pela fala 12; o quarto NOMEADO pelo operador na fala 13; DEZENOVE falas; a verdade sobre a Auditoria; parágrafo R6 com as três emendas e a separação RATIFICADOS × [DECLARADO pela autoria]",
   "ressurreicao_do_sinal": "nome do operador na fala 13 entre « »; nome de trabalho da gerência em prosa"},
 "aspas": {"script": str(BASE / "R2_aspas" / "requote_aescala_v410.py"), "saida_so_medir": aspas_linha, "trocas": int(m_trocas.group(1)) if m_trocas else None},
 "frases_fixas": {"canonica_D84": [norm(r5).count(norm(CAN)), norm(r6).count(norm(CAN))], "forma_do_tempo_D94": [norm(r5).count(D94), norm(r6).count(D94)]},
 "frases_vedadas_presentes": [v for v in VEDADAS if v in low],
 "beta_literal_na_pedra": re.findall(r"0[.,]01[0-9]+", r6),
 "falas_por_sha256_lidas_do_arquivo": falas, "n_falas": len(falas),
 "o_que_nao_fechou": [],
 "nao_instalado": "nada instalado; pasta v410\\pedra intocada; cadeia não rodada; a instalação é do construtor",
}
out = OUT / "RECIBO_AESCALA_R6_10nov.json"
out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("recibo", out.name, out.stat().st_size, "B sha256", sha(out))
print("AEscala R6 FINAL sha256", rec["aescala_r6"]["sha256"], rec["aescala_r6"]["bytes"], "B | imports", rec["aescala_r6"]["imports"])
print("log sha256", rec["compilacao"]["log_sha256"], "|", rcf, "|", rec["compilacao"]["tempo"])
print("decl", rec["declaracoes"], "| auditadas", len(axioms), "fora do trio", len(fora), "| erros", len(erros), "avisos", len(avisos))
print("R5 mantidos", len(mantidos), "sumidos", sumidos, "| enunciado mudou", enunciado_mudou, "| corpos", corpo_mudou)
print("novos:", len(novos), "| RATIFICADOS ok:", all(marca_rat.values()), len(marca_rat), "| DA AUTORIA ok:", all(marca_aut.values()), len(marca_aut))
print("2a emenda so' docstring:", rec["segunda_emenda_fala_18"]["so_docstring_e_cabecalho"], "| espelhos ok:", all(espelhos_18.values()))
print("3a emenda so' docstring:", rec["terceira_emenda_fala_19"]["so_docstring_e_cabecalho"], "| objetos:", objetos_19, "| fala 19 por bytes:", rec["terceira_emenda_fala_19"]["fala"]["na_secao_7_por_bytes"])
print("conferencia da 1a emenda:", rec["terceira_emenda_fala_19"]["conferencia_pedida_da_primeira_emenda"]["frase_da_autoria_dizendo_que_posto_nunca_e_escala"], "| unidade:", rec["terceira_emenda_fala_19"]["palavra_unidade_na_pedra"]["ocorrencias"], rec["terceira_emenda_fala_19"]["palavra_unidade_na_pedra"]["todas_como_unidade_posta"], "| E₀:", r6.count("E₀"), "| 'a ratificar':", low.count("a ratificar"))
print("cadeia fechou:", rec["nomes_novos"]["o_teorema_cadeia_fechou"], "| axiomas novas/renomeada fora do trio:", {k: v for k, v in axiomas_novos.items() if v is None or not set(v) <= trio})
print("aspas:", aspas_linha)
print("fixas:", rec["frases_fixas"], "| vedadas:", rec["frases_vedadas_presentes"], "| beta literal:", rec["beta_literal_na_pedra"])
print("falas:", len(falas), all(v["sha256_no_cabecalho"] for v in falas.values()))
