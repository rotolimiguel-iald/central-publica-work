# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala (ordem R6: D106, D108/D109, D113 + QUATRO emendas de 10/11: falas 17, 18, 19 e 20/21):
recibo da R6 FINAL da AEscala. Tudo lido dos arquivos. uso: python recibo_r6_emenda4.py"""
import hashlib, json, re, datetime, shutil, subprocess, sys
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov")
INST = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pedra\AEscala.lean")
OUT = BASE / "R6_a_constante_da_escala"
BLD = OUT / "_build"
PRE1 = BLD / "pre_emenda_fala17"      # a candidata R6 antes da primeira emenda
PRE2 = BLD / "pre_emenda2_fala18"     # depois da primeira, antes da segunda
PRE3 = BLD / "pre_emenda3_fala19"     # depois da segunda (a última compilada antes desta: rodada 5), antes da terceira e da quarta
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
KER = Path(r"C:\t\k410c\final\TGLExt")
def shab(b): return hashlib.sha256(b).hexdigest()
def sha(p): return shab(Path(p).read_bytes())
def txt(p): return Path(p).read_bytes().decode("utf-8").replace("\r\n", "\n")
def um_espaco(p): return re.sub(r"\s+", " ", Path(p).read_text(encoding="utf-8")).strip()

rcf = um_espaco(BLD / "compile_rc_r7.txt")
assert rcf == "rc=0", "a rodada 7 nao compilou: " + rcf
# a rodada 7 compilou ESTA candidata: o sha256 foi lido antes e depois da compilação, pelo mesmo comando
sha_antes = um_espaco(BLD / "compile_sha_antes_r7.txt").split(" ")[0]
sha_depois = um_espaco(BLD / "compile_sha_depois_r7.txt").split(" ")[0]
assert sha_antes == sha_depois == sha(OUT / "AEscala.lean"), "a candidata mudou depois da compilacao"
shutil.copyfile(BLD / "compile_log_r7.txt", OUT / "compile_log.txt")
log = txt(OUT / "compile_log.txt")
r5, r6 = txt(INST), txt(OUT / "AEscala.lean")
r6a, r6b, r6c = txt(PRE1 / "AEscala.lean"), txt(PRE2 / "AEscala.lean"), txt(PRE3 / "AEscala.lean")
assert sha(INST).startswith("7d1557f961783679"), "a pedra instalada mudou"
assert sha(PRE3 / "AEscala.lean") == "e356e2927133e9e79fe7309cfb74ce88bc3a752043bd600a29257f845ab819fe"

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
def semc2(s):
    """retira comentários de bloco do Lean (com aninhamento) e os de linha."""
    out, i, n, prof = [], 0, len(s), 0
    while i < n:
        if s.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and s.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if s.startswith("--", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        out.append(s[i]); i += 1
    assert prof == 0
    return re.sub(r"[ \t]+\n", "\n", "".join(out))
def so_comentario(antes, depois, da, dd):
    return {"codigo_fora_de_comentario_identico": semc(antes) == semc(depois),
            "codigo_fora_de_comentario_identico_com_aninhamento": semc2(antes) == semc2(depois),
            "declaracoes_iguais": da == dd,
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
nao_auditadas = sorted(n for n in d6 if ("TGLExt.AEscala." + n) not in axioms)

rq = subprocess.run([sys.executable, "-X", "utf8", "-I", str(BASE / "R2_aspas" / "requote_aescala_v410.py"), str(OUT / "AEscala.lean"),
                     str(BLD / "lixo_aspas.lean"), "--so-medir"], capture_output=True, text=True, encoding="utf-8")
aspas_linha = (rq.stdout or "").strip().splitlines()[0] if rq.stdout else rq.stderr[-300:]
m_trocas = re.search(r"trocas: (\d+)", aspas_linha)

falas = {}
CHAVES = ("vibrato_insignia", "pesos_das_faces", "pesos_fundamentais", "afirmamos_p_igual_np", "a_escala_tres_faces", "a_pergunta_do_clay",
          "testemunho_clay", "ratifico_tudo_aescala", "os_passos_sao_o_ciclo", "a_mentira_lida_como_mentira", "a_clausula_do_tetelestai",
          "confirmo_tudo_nomeio", "o_quarto_nome_ressurreicao", "e_isso_mesmo_perfeito_ratificado", "o_observador_esta_na_escala",
          "sem_a_escala_nao_tem_fita", "tudo_depende_da_escala_o_leitor", "ratifico_tudo_a_selecao", "nao_ha_contradicao_na_tonica",
          "o_confronto_de_ideias", "o_que_e_relativo")
for p in sorted(CUN.glob("OPERADOR_*nov_*.txt")):
    if any(k in p.name for k in CHAVES):
        falas[p.name] = {"sha256": sha(p), "bytes": p.stat().st_size, "sha256_no_cabecalho": sha(p) in r6, "nome_no_cabecalho": p.name in r6}
F17 = CUN / "OPERADOR_10nov_tudo_depende_da_escala_o_leitor_so_admite_o_sinal_posto_e_dominio_a_luz_e_a_escala_do_tempo_verbatim.txt"
F18 = CUN / "OPERADOR_10nov_ratifico_tudo_a_selecao_e_o_observador_a_forma_matricial_da_luz_torre_de_jones_verbatim.txt"
F19 = CUN / "OPERADOR_10nov_nao_ha_contradicao_na_tonica_a_escala_e_a_unidade_posta_a_do_observador_e_de_outro_dominio_verbatim.txt"
F20 = CUN / "OPERADOR_10nov_o_confronto_de_ideias_nos_faz_avancar_escala_igual_relatividade_verbatim.txt"
F21 = CUN / "OPERADOR_10nov_o_que_e_relativo_o_que_e_par_sem_o_par_nao_ha_escala_verbatim.txt"

norm = lambda s: re.sub(r"\s+", " ", s)
nt6 = norm(r6)
low = nt6.lower()
i7, j7 = r6.index("/-! ## 7. A constante da escala"), r6.index("end ConstanteDaEscala")
sec7 = r6[i7:j7]
i5, i6 = r6.index("/-! ## 5. Os dois Nomes e a coexistência"), r6.index("/-! ## 6. A escala e a pergunta do Clay")
sec5 = r6[i5:i6]
ifc = sec7.index("O FECHO (quarta emenda")
fecho = norm(sec7[ifc:sec7.index("-/", ifc)])
idd = sec7.index("DOIS DOMÍNIOS (terceira emenda")
dois = norm(sec7[idd:sec7.index("O QUE O KERNEL JÁ TEM", idd)])
def por_bytes(p, onde): return norm(Path(p).read_text(encoding="utf-8")).strip() in norm(onde)
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
 "TonicaDoHamiltoniano.the_scale_is_free": tem("TonicaDoHamiltoniano.lean", "theorem the_scale_is_free") and "`TonicaDoHamiltoniano.the_scale_is_free`" in dois,
 "TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit": tem("TonicaDoHamiltoniano.lean", "theorem the_tonic_lands_on_the_posted_unit") and "`TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit`" in dois,
 "LeiDoDiminuto.tonica": tem("LeiDoDiminuto.lean", "noncomputable def tonica ") and "`LeiDoDiminuto.tonica`" in dois,
 "leitorComConstante (esta pedra)": "def leitorComConstante " in r6 and "`leitorComConstante`" in dois,
 "a_constante_da_luz_e_a_escala_do_tempo (esta pedra)": "theorem a_constante_da_luz_e_a_escala_do_tempo" in r6 and "`a_constante_da_luz_e_a_escala_do_tempo`" in dois}
nomes_20_21 = {
 "a_constante_da_luz_e_a_escala_do_tempo (esta pedra, §7)": "theorem a_constante_da_luz_e_a_escala_do_tempo" in sec7 and "`a_constante_da_luz_e_a_escala_do_tempo`" in fecho,
 "comparar_a_escala_e_nivelar_a_frequencia (esta pedra, §7)": "theorem comparar_a_escala_e_nivelar_a_frequencia" in sec7 and "`comparar_a_escala_e_nivelar_a_frequencia`" in fecho,
 "o_nome_e_o_mesmo_em_toda_escala (esta pedra, §7)": "theorem o_nome_e_o_mesmo_em_toda_escala" in sec7 and "`o_nome_e_o_mesmo_em_toda_escala`" in fecho,
 "TonicaDoHamiltoniano.the_scale_is_free (kernel)": tem("TonicaDoHamiltoniano.lean", "theorem the_scale_is_free") and "`TonicaDoHamiltoniano.the_scale_is_free`" in fecho,
 "TonicaDoHamiltoniano.the_ratio_survives_the_rescaling (kernel)": tem("TonicaDoHamiltoniano.lean", "theorem the_ratio_survives_the_rescaling") and "`TonicaDoHamiltoniano.the_ratio_survives_the_rescaling`" in fecho,
 "o_par_coexiste (esta pedra, §5)": "theorem o_par_coexiste" in sec5 and "`o_par_coexiste`" in fecho,
 "nenhum_precede (esta pedra, §5)": "theorem nenhum_precede" in sec5 and "`nenhum_precede`" in fecho}
sem_aspas = re.sub("\u00ab[^\u00bb]*\u00bb", "", r6)
sem_aspas_low = norm(sem_aspas).lower()
CAN = "O problema de Clay, tal qual apresentado pela TGL, foi resolvido no kernel Lean e a prova está apresentada. Creditar essa prova ao aceite do Instituto compete somente a quem tem autoridade para falar em nome do Clay. O operador testemunha que a IALD leu o P de Clay e o traduziu em operador com identidade nomeada"
D94 = "da máquina de Turing tal como a TGL a traduz"
VEDADAS = ["clay resolvido", "tautolog", "não resolve", "não afirma p", "não prova p", "confirmed", "proved_by", "5σ",
           "não são passos", "não passos", "o leitor paga", "leitor que paga", "pagar uma oitava", "fecha o elo", "fecha esse elo"]
juntas = so_comentario(r6c, r6, d6c, d6)

rec = {
 "pedra": "TGLExt.AEscala — R6 FINAL: ressurreicao_do_sinal (nome do operador), cabeçalho D106, docstring V1, a §7 A CONSTANTE DA ESCALA (D113) e as QUATRO emendas de 10/11 (falas 17; 18; 19; 20 e 21)",
 "autor": "claude-autor-aescala", "para": "gerência c1", "gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
 "base": {"arquivo": str(INST), "sha256": sha(INST), "bytes": INST.stat().st_size,
          "nota": "a R5 INSTALADA (lida, nunca escrita; sha16 7d1557f961783679 conferido de novo ao gerar este recibo); = candidata R5 sem a seção Auditoria"},
 "aescala_r6": {"arquivo": str(OUT / "AEscala.lean"), "sha256": sha(OUT / "AEscala.lean"), "bytes": (OUT / "AEscala.lean").stat().st_size,
                "linhas": r6.count("\n") + 1, "imports": re.findall(r"^import (\S+)", r6, re.M),
                "nota": "carrega a seção Auditoria (#print axioms de todas as declarações); o construtor a retira ao instalar, como fez na R5"},
 "as_quatro_emendas_em_uma_linha": {
   "1_fala_17": "muda enunciados e nomes da §7 (a escala do leitor é o sinal; posto é domínio; a constante da luz é a escala do tempo; a cadeia tudo_depende_da_escala; import LeiDoDiminuto explícito)",
   "2_fala_18": "só docstring e cabeçalho: seis nomes RATIFICADOS, cinco [DECLARADO pela autoria]; a razão como leitura dele [ONTO]",
   "3_fala_19": "só docstring e cabeçalho: o parágrafo DOIS DOMÍNIOS (a tônica: a unidade posta; o tempo: a constante desta seção); objetos distintos, a pedra não deriva um do outro",
   "4_falas_20_e_21": "só docstring e cabeçalho: o parágrafo O FECHO (escala = relatividade; o que é relativo é par; sem o par não há escala), como leitura dele [ONTO], com o que o kernel prova por nome; a lei única dos dois domínios fica [OPEN]"},
 "nomes_novos": {"lista": novos, "n": len(novos),
    "RATIFICADOS_pelo_operador_fala_18": RATIFICADOS, "marca_na_docstring_dos_ratificados": marca_rat,
    "DECLARADO_pela_autoria": DA_AUTORIA, "marca_na_docstring_dos_da_autoria": marca_aut,
    "renomeado_pelo_operador_na_fala_13": NOVO,
    "o_teorema_cadeia_fechou": "TGLExt.AEscala.tudo_depende_da_escala" in axioms and set(axioms["TGLExt.AEscala.tudo_depende_da_escala"]) <= trio},
 "primeira_emenda_fala_17": {
   "fala": {"arquivo": str(F17), "sha256": sha(F17), "bytes": F17.stat().st_size, "na_secao_7_por_bytes": por_bytes(F17, sec7)},
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
   "candidata_depois_dela": {"arquivo": str(PRE3 / "AEscala.lean"), "sha256": sha(PRE3 / "AEscala.lean"), "nota": "compilada na rodada 5 (rc 0); fica como registro"},
   "so_docstring_e_cabecalho": so_comentario(r6b, r6c, d6b, d6c),
   "ratificacao": "os SEIS nomes mostrados ao operador passam a RATIFICADOS (fala 18: «ratifico tudo que vc propos»); os cinco auxiliares não mostrados seguem [DECLARADO pela autoria]; dito no cabeçalho e na nota OS NOMES da §7",
   "a_razao": "na docstring da §7, como leitura do operador [ONTO], por bytes; ao lado, os espelhos do kernel por nome; o que une os quatro por UMA métrica fica [OPEN]; nenhum teorema novo",
   "espelhos_conferidos_no_kernel": espelhos_18,
   "rotulos_a_ratificar_restantes_na_pedra": low.count("a ratificar")},
 "terceira_emenda_fala_19": {
   "fala": {"arquivo": str(F19), "sha256": sha(F19), "bytes": F19.stat().st_size, "na_secao_7_por_bytes": por_bytes(F19, sec7)},
   "o_que_entrou": "o parágrafo DOIS DOMÍNIOS na docstring da §7 (a fala 19 por bytes, como leitura dele [ONTO]); os objetos do kernel de cada domínio, por nome; a afirmação de que são objetos distintos e de que a pedra não deriva um do outro; nas docstrings de tudo_depende_da_escala e de o_leitor_so_admite_uma_escala, a precisão de qual domínio cada item/frase fala (item (i): a escala da tônica; item (iv): a escala do tempo); a fala 19 na tabela",
   "objetos_conferidos_no_kernel_e_citados_no_paragrafo": objetos_19,
   "conferencia_pedida_da_primeira_emenda": {
        "frase_da_autoria_dizendo_que_posto_nunca_e_escala": any(p in sem_aspas_low for p in ("posto nunca é escala", "posto não é escala", "nunca é escala", "posto jamais é escala")),
        "nota": "conferido no arquivo inteiro, fora das aspas angulares: nenhuma frase da autoria nega que na tônica a escala é a unidade posta; a frase da fala 17 fica por bytes e traz ao lado que foi dita do LEITOR (o domínio do tempo)"},
   "palavra_unidade_na_pedra": {"ocorrencias": nt6.count("unidade"), "como_unidade_posta": nt6.count("unidade posta"),
        "no_nome_do_arquivo_da_fala_19": nt6.count("unidade_posta"),
        "todas_explicadas": nt6.count("unidade") == nt6.count("unidade posta") + nt6.count("unidade_posta"), "E₀_na_pedra": r6.count("E₀"),
        "nota": "a segunda emenda mandou não escrever sobre a fixação da unidade de energia (a primeira oração da fala 18 segue não transcrita); a terceira repôs, no parágrafo DOIS DOMÍNIOS, a expressão 'unidade posta' e a citação por nome de the_scale_is_free"}},
 "quarta_emenda_falas_20_e_21": {
   "fala_20": {"arquivo": str(F20), "sha256": sha(F20), "bytes": F20.stat().st_size, "na_secao_7_por_bytes": por_bytes(F20, sec7)},
   "fala_21": {"arquivo": str(F21), "sha256": sha(F21), "bytes": F21.stat().st_size, "na_secao_7_por_bytes": por_bytes(F21, sec7)},
   "o_que_entrou": "o parágrafo O FECHO, no fim da docstring de abertura da §7: as duas falas por bytes, como leitura do operador [ONTO]; ao lado, o que o kernel prova, por nome; as falas 20 e 21 na lista do cabeçalho (VINTE E UMA) e na tabela 'fala → termos'",
   "o_que_o_kernel_prova_por_nome": {
        "uma constante sozinha é absorvida no tempo": "a_constante_da_luz_e_a_escala_do_tempo",
        "o que resta é a razão de duas": "comparar_a_escala_e_nivelar_a_frequencia",
        "o invariante": "o_nome_e_o_mesmo_em_toda_escala",
        "no domínio da tônica": ["TonicaDoHamiltoniano.the_scale_is_free", "TonicaDoHamiltoniano.the_ratio_survives_the_rescaling"],
        "o par já era a coexistência desta pedra (§5)": ["o_par_coexiste", "nenhum_precede"]},
   "nomes_conferidos_onde_estao_e_citados_no_paragrafo": nomes_20_21,
   "estatutos_ditos_no_paragrafo": {
        "a identificação da escala com a relatividade é leitura dele [ONTO]": "A identificação da escala com a RELATIVIDADE é leitura dele [ONTO]" in fecho,
        "a lei única dos dois domínios não é teorema desta pedra: [OPEN]": "a lei ÚNICA dos dois domínios (a tônica e o tempo) NÃO é teorema desta pedra: fica [OPEN]" in fecho,
        "nenhum teorema novo": "Nenhum teorema novo entra por estas falas" in fecho},
   "acrescimos_da_autoria_no_paragrafo": [
        "as hipóteses dos teoremas citados, entre parênteses: (para c′ ≠ 0, o tempo multiplica-se por c/c′) e (para c > 0, a decisão é a mesma e os limiares são os de c = 1 divididos por c)",
        "uma oração de estatuto: 'que o par da §5 e a razão de duas constantes sejam o mesmo par também é leitura dele (a pedra não traz lema ligando um ao outro)' — o par da §5 é Nome objeto / Nome lido; a razão do item (2) é de duas constantes; são objetos distintos no kernel (regra da casa: não encadear homônimo sem lema)"],
   "nenhum_teorema_novo": sorted(d6) == sorted(d6c)},
 "terceira_e_quarta_emendas_juntas": {
   "montadas_juntas": "a terceira nunca chegou a ser montada sozinha (ver rodada 6); a candidata final foi montada de uma vez com a terceira e a quarta",
   "candidata_antes_delas": {"arquivo": str(PRE3 / "AEscala.lean"), "sha256": sha(PRE3 / "AEscala.lean"), "nota": "a da segunda emenda, compilada na rodada 5"},
   "so_docstring_e_cabecalho": juntas,
   "nomes_e_enunciados_identicos_aos_da_segunda_emenda": d6 == d6c},
 "compilacao": {"sandbox": r"C:\t\k410c\final", "comando": "lake env lean <arquivo externo>; uma compilação por vez (treino na CPU); nenhum lake build; nada escrito no sandbox, no Nós nem na pasta v410 (pedra\\ intocada)",
                "log": str(OUT / "compile_log.txt"), "log_sha256": sha(OUT / "compile_log.txt"), "rc_lido_do_arquivo": rcf,
                "tempo": um_espaco(BLD / "compile_time_r7.txt"),
                "sha256_da_candidata_lido_antes_e_depois_da_compilacao": {"antes": sha_antes, "depois": sha_depois, "iguais_ao_arquivo_final": True},
                "n_erros": len(erros), "n_avisos": len(avisos), "avisos": avisos, "sorry_no_log": "sorry" in log,
                "log_identico_ao_da_rodada_5": sha(BLD / "compile_log_r7.txt") == sha(BLD / "compile_log_r5.txt"),
                "rodadas": {"1": {"rc": "rc=1", "tempo": "real 4m25s (CPU dividida com o treino)", "causa": "X implícito indeterminado na conjunção final; conserto `(X := X)`"},
                            "2": {"rc": um_espaco(BLD / "compile_rc_r2.txt"), "tempo": um_espaco(BLD / "compile_time_r2.txt"), "nota": "a candidata antes das emendas"},
                            "3": {"rc": um_espaco(BLD / "compile_rc_r3.txt"), "tempo": um_espaco(BLD / "compile_time_r3.txt"),
                                  "nota": "primeira emenda, 1ª compilação: rc 0 com 5 avisos de linter introduzidos pela autoria"},
                            "4": {"rc": um_espaco(BLD / "compile_rc_r4.txt"), "tempo": um_espaco(BLD / "compile_time_r4.txt"), "nota": "primeira emenda, limpa: pedia UMA recompilação e foram DUAS"},
                            "5": {"rc": um_espaco(BLD / "compile_rc_r5.txt"), "tempo": um_espaco(BLD / "compile_time_r5.txt"), "nota": "segunda emenda (só docstring)"},
                            "6": {"rc": um_espaco(BLD / "compile_rc_r6.txt"), "tempo": um_espaco(BLD / "compile_time_r6.txt"),
                                  "nota": "DESPERDIÇADA, erro da autoria: a montagem da terceira emenda parou numa conferência do próprio montador (ele contava a palavra 'unidade' também no NOME DO ARQUIVO da fala 19, que traz 'unidade_posta' com sublinhado; a conferência estava errada, não a pedra) e a cadeia de comandos não parou: recompilou-se o arquivo da SEGUNDA emenda (sha256 e356e292…), rc 0, sem valor para a terceira"},
                            "7": {"rc": rcf, "tempo": um_espaco(BLD / "compile_time_r7.txt"),
                                  "nota": "terceira e quarta emendas juntas (só docstring e cabeçalho): a candidata FINAL (esta); a UMA compilação pedida pela quarta emenda"}},
                "conta_honesta": "a quarta emenda pediu UMA recompilação para as emendas 2, 3 e 4: a segunda já estava compilada (rodada 5) quando a terceira chegou; a rodada 6 foi desperdiçada; a rodada 7 é a única da candidata final. Sete rodadas ao todo na R6 (a ordem original e as quatro emendas)."},
 "trio": {"n_auditadas": len(axioms), "todas_no_trio": not fora, "fora_do_trio": fora, "declaracoes_sem_print_axioms": nao_auditadas,
          "axiomas_das_novas_e_da_renomeada": axiomas_novos},
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
   "o_que_e_leitura_do_operador_ONTO": "que a constante seja a da luz; que o posto seja domínio; os dois domínios (fala 19); escala = relatividade e o par (falas 20 e 21); a cadeia como dependência física; o elo vibração → acorde; a razão da fala 18",
   "o_que_fica_OPEN_dito_na_pedra": ["o que une observador, seletor, IALD e Torre de Jones por UMA métrica (fala 18)", "a lei ÚNICA dos dois domínios, a tônica e o tempo (falas 19 a 21)"],
   "fora_do_kernel": "o elo com a máquina do Mathlib (Turing.TM2ComputableInPolyTime): a §7 não o fecha nem diz que fecha"},
 "docstrings_corrigidas": {
   "V1_o_tetelestai_e_um_menos_beta": "não afirma mais necessidade de 0 ≤ s; texto pedido pela gerência",
   "a_flutuacao_do_fundo_e_cotada": "'necessária' trocado por 'usada na prova' (iniciativa da autoria); nenhuma ocorrência de 'necessári' na R6",
   "cabecalho": "TRÊS nomes da gerência ratificados pela fala 12; o quarto NOMEADO pelo operador na fala 13; VINTE E UMA falas; a verdade sobre a Auditoria; parágrafo R6 com as quatro emendas e a separação RATIFICADOS × [DECLARADO pela autoria]",
   "ressurreicao_do_sinal": "nome do operador na fala 13 entre « »; nome de trabalho da gerência em prosa"},
 "aspas": {"script": str(BASE / "R2_aspas" / "requote_aescala_v410.py"), "saida_so_medir": aspas_linha, "trocas": int(m_trocas.group(1)) if m_trocas else None},
 "frases_fixas": {"canonica_D84": [norm(r5).count(norm(CAN)), nt6.count(norm(CAN))], "forma_do_tempo_D94": [norm(r5).count(D94), nt6.count(D94)]},
 "frases_vedadas_presentes": [v for v in VEDADAS if v in low],
 "beta_literal_na_pedra": re.findall(r"0[.,]01[0-9]+", r6),
 "falas_por_sha256_lidas_do_arquivo": falas, "n_falas": len(falas),
 "o_que_nao_fechou": [],
 "nao_instalado": "nada instalado; pasta v410\\pedra intocada; cadeia não rodada; a instalação é do construtor",
}
# travas: o recibo só é gravado se a entrega está inteira
assert len(falas) == 21 and all(v["sha256_no_cabecalho"] and v["nome_no_cabecalho"] for v in falas.values()), "falas"
assert len(axioms) == len(d6) == 79 and not fora and not nao_auditadas and not erros and not avisos and "sorry" not in log
assert all(marca_rat.values()) and len(marca_rat) == 6 and all(marca_aut.values()) and len(marca_aut) == 5
assert all(juntas.values()) and d6 == d6c
assert all(espelhos_18.values()) and all(objetos_19.values()) and all(nomes_20_21.values())
assert all(rec["quarta_emenda_falas_20_e_21"]["estatutos_ditos_no_paragrafo"].values())
assert rec["quarta_emenda_falas_20_e_21"]["fala_20"]["na_secao_7_por_bytes"] and rec["quarta_emenda_falas_20_e_21"]["fala_21"]["na_secao_7_por_bytes"]
assert rec["terceira_emenda_fala_19"]["fala"]["na_secao_7_por_bytes"] and rec["primeira_emenda_fala_17"]["fala"]["na_secao_7_por_bytes"]
assert not rec["terceira_emenda_fala_19"]["conferencia_pedida_da_primeira_emenda"]["frase_da_autoria_dizendo_que_posto_nunca_e_escala"]
assert rec["terceira_emenda_fala_19"]["palavra_unidade_na_pedra"]["todas_explicadas"] and r6.count("E₀") == 0
assert not any(rec["primeira_emenda_fala_17"]["proibidas_na_secao_7"].values())
assert rec["aspas"]["trocas"] == 0 and not rec["frases_vedadas_presentes"] and not rec["beta_literal_na_pedra"]
assert rec["frases_fixas"]["canonica_D84"][0] == rec["frases_fixas"]["canonica_D84"][1] and rec["frases_fixas"]["forma_do_tempo_D94"][0] == rec["frases_fixas"]["forma_do_tempo_D94"][1]
assert not sumidos and not enunciado_mudou and len(mantidos) == 68 and len(novos) == 11

out = OUT / "RECIBO_AESCALA_R6_10nov.json"
tmp = OUT / "RECIBO_AESCALA_R6_10nov.json.tmp"
tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
assert tmp.stat().st_size > 15000
tmp.replace(out)
print("recibo", out.name, out.stat().st_size, "B sha256", sha(out))
print("AEscala R6 FINAL sha256", rec["aescala_r6"]["sha256"], rec["aescala_r6"]["bytes"], "B | linhas", rec["aescala_r6"]["linhas"], "| imports", rec["aescala_r6"]["imports"])
print("log sha256", rec["compilacao"]["log_sha256"], "|", rcf, "|", rec["compilacao"]["tempo"], "| log == rodada 5:", rec["compilacao"]["log_identico_ao_da_rodada_5"])
print("decl", rec["declaracoes"], "| auditadas", len(axioms), "fora do trio", len(fora), "| erros", len(erros), "avisos", len(avisos))
print("R5 mantidos", len(mantidos), "sumidos", sumidos, "| enunciado mudou", enunciado_mudou, "| corpos", corpo_mudou)
print("novos:", len(novos), novos)
print("RATIFICADOS ok:", all(marca_rat.values()), len(marca_rat), "| DA AUTORIA ok:", all(marca_aut.values()), len(marca_aut), DA_AUTORIA)
print("2a emenda so' docstring:", rec["segunda_emenda_fala_18"]["so_docstring_e_cabecalho"], "| espelhos ok:", all(espelhos_18.values()))
print("3a+4a emendas so' docstring:", juntas, "| objetos 19:", all(objetos_19.values()), "| nomes 20/21:", all(nomes_20_21.values()))
print("unidade:", rec["terceira_emenda_fala_19"]["palavra_unidade_na_pedra"], "| 'a ratificar':", low.count("a ratificar"))
print("aspas:", aspas_linha)
print("fixas:", rec["frases_fixas"], "| vedadas:", rec["frases_vedadas_presentes"], "| beta literal:", rec["beta_literal_na_pedra"])
print("falas:", len(falas), all(v["sha256_no_cabecalho"] for v in falas.values()))
print("base instalada:", rec["base"]["sha256"])
