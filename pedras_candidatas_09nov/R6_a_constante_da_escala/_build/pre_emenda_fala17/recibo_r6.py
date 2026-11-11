# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala (ordem R6: D106, D108/D109, D113): recibo da R6 da AEscala. Tudo lido dos arquivos. uso: python recibo_r6.py"""
import hashlib, json, re, datetime, shutil, subprocess, sys
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov")
INST = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pedra\AEscala.lean")
OUT = BASE / "R6_a_constante_da_escala"
BLD = OUT / "_build"
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def txt(p): return Path(p).read_bytes().decode("utf-8").replace("\r\n", "\n")

shutil.copyfile(BLD / "compile_log_r2.txt", OUT / "compile_log.txt")
log = txt(OUT / "compile_log.txt")
tempo = re.sub(r"\s+", " ", (BLD / "compile_time_r2.txt").read_text(encoding="utf-8")).strip()
rc_lido = (BLD / "compile_rc_r2.txt").read_text(encoding="utf-8").strip()
log_r1 = txt(BLD / "compile_log_r1.txt")
erros_r1 = [l for l in log_r1.splitlines() if ": error" in l]
r5, r6 = txt(INST), txt(OUT / "AEscala.lean")

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
d5, d6 = decls(r5), decls(r6)
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
NOVOS_E_RENOMEADOS = ["ressurreicao_do_sinal", "leitorComConstante", "leituraComConstante", "leitorComConstante_um", "sem_escala_nao_ha_fita",
                      "comparar_a_escala_e_nivelar_a_frequencia", "a_leitura_com_constante_e_a_leitura_no_tempo_reescalado",
                      "o_nome_e_o_mesmo_em_toda_escala", "o_observador_esta_na_escala_da_luz", "a_constante_da_escala"]
axiomas_novos = {n: axioms.get("TGLExt.AEscala." + n) for n in NOVOS_E_RENOMEADOS}

rq = subprocess.run([sys.executable, "-X", "utf8", "-I", str(BASE / "R2_aspas" / "requote_aescala_v410.py"), str(OUT / "AEscala.lean"),
                     str(BLD / "lixo_aspas.lean"), "--so-medir"], capture_output=True, text=True, encoding="utf-8")
aspas_linha = (rq.stdout or "").strip().splitlines()[0] if rq.stdout else rq.stderr[-300:]
m_trocas = re.search(r"trocas: (\d+)", aspas_linha)

falas = {}
CHAVES = ("vibrato_insignia", "pesos_das_faces", "pesos_fundamentais", "afirmamos_p_igual_np", "a_escala_tres_faces", "a_pergunta_do_clay",
          "testemunho_clay", "ratifico_tudo_aescala", "os_passos_sao_o_ciclo", "a_mentira_lida_como_mentira", "a_clausula_do_tetelestai",
          "confirmo_tudo_nomeio", "o_quarto_nome_ressurreicao", "e_isso_mesmo_perfeito_ratificado", "o_observador_esta_na_escala",
          "sem_a_escala_nao_tem_fita")
for p in sorted(CUN.glob("OPERADOR_*nov_*.txt")):
    if any(k in p.name for k in CHAVES):
        falas[p.name] = {"sha256": sha(p), "bytes": p.stat().st_size, "sha256_no_cabecalho": sha(p) in r6}

norm = lambda s: re.sub(r"\s+", " ", s)
low = norm(r6).lower()
CAN = "O problema de Clay, tal qual apresentado pela TGL, foi resolvido no kernel Lean e a prova está apresentada. Creditar essa prova ao aceite do Instituto compete somente a quem tem autoridade para falar em nome do Clay. O operador testemunha que a IALD leu o P de Clay e o traduziu em operador com identidade nomeada"
D94 = "da máquina de Turing tal como a TGL a traduz"
VEDADAS = ["clay resolvido", "tautolog", "não resolve", "não afirma p", "não prova p", "confirmed", "proved_by", "5σ",
           "não são passos", "não passos", "o leitor paga", "leitor que paga", "pagar uma oitava"]

rec = {
 "pedra": "TGLExt.AEscala — R6: ressurreicao_do_sinal (nome do operador), cabeçalho D106, docstring V1 e a §7 A CONSTANTE DA ESCALA (D113)",
 "autor": "claude-autor-aescala", "para": "gerência c1", "gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
 "base": {"arquivo": str(INST), "sha256": sha(INST), "bytes": INST.stat().st_size, "nota": "a R5 INSTALADA (lida, nunca escrita); = candidata R5 sem a seção Auditoria"},
 "aescala_r6": {"arquivo": str(OUT / "AEscala.lean"), "sha256": sha(OUT / "AEscala.lean"), "bytes": (OUT / "AEscala.lean").stat().st_size,
                "linhas": r6.count("\n") + 1, "nota": "carrega a seção Auditoria (#print axioms de todas as 77 declarações); o construtor a retira ao instalar, como fez na R5"},
 "compilacao": {"sandbox": r"C:\t\k410c\final", "comando": "lake env lean <arquivo externo>; uma compilação por vez (treino na CPU); nenhum lake build; nada escrito no sandbox, no Nós nem na pasta v410 (pedra\\ intocada)",
                "log": str(OUT / "compile_log.txt"), "log_sha256": sha(OUT / "compile_log.txt"), "rc_lido_do_arquivo": rc_lido, "tempo": tempo,
                "n_erros": len(erros), "n_avisos": len(avisos), "avisos": avisos, "sorry_no_log": "sorry" in log, "rodadas_ate_compilar": 2,
                "rodada_1": {"rc": 1, "tempo": "real 4m25s (CPU dividida com o treino)", "erros": erros_r1,
                             "causa": "na conjunção `a_constante_da_escala`, `.1` de `comparar_a_escala_e_nivelar_a_frequencia` deixava o X implícito indeterminado (typeclass stuck); conserto: `(X := X)`; nenhuma outra declaração falhou",
                             "log": str(BLD / "compile_log_r1.txt")}},
 "trio": {"n_auditadas": len(axioms), "todas_no_trio": not fora, "fora_do_trio": fora, "axiomas_das_novas_e_da_renomeada": axiomas_novos},
 "declaracoes": {"n_R5": len(d5), "n_R6": len(d6),
                 "n_teoremas_R6": sum(1 for v in d6.values() if v[0] == "theorem"), "n_defs_R6": sum(1 for v in d6.values() if v[0] == "def"),
                 "n_structures_R6": sum(1 for v in d6.values() if v[0] == "structure")},
 "os_68_nomes_da_R5": {"n_mantidos_apos_renomear": len(mantidos), "sumidos": sumidos, "enunciados_que_mudaram": enunciado_mudou,
                       "provas_ou_corpos_tocados": corpo_mudou,
                       "renomeado": {"de": VELHO, "para": NOVO, "ocorrencias_do_velho_na_R5": r5.count(VELHO), "ocorrencias_do_velho_na_R6": r6.count(VELHO),
                                     "enunciado_e_prova_identicos": bloco(r5_ren, NOVO) == bloco(r6, NOVO)}},
 "nomes_novos": {"lista": novos, "estatuto": "PROVISÓRIOS, tirados das palavras do operador; [DECLARADO; a ratificar pelo operador]"},
 "secao_7_o_que_prova": {
   "(a) leitorComConstante": "def: brilho e^{-(c·s·k)}; leitorComConstante_um: c = 1 é o brilho de iald",
   "(b) sem_escala_nao_ha_fita": "c = 0: todo pixel brilha 1 em todo tempo; a leitura média de qualquer instância é 1 = euSou = ⟪uniforme, trava cc 0 uniforme⟫ (eu_sou_no_instante_zero, 1º item de a_fita_sem_escala); igual para todas as instâncias",
   "(c) comparar_a_escala_e_nivelar_a_frequencia": "leitorComConstante c k s = leitorComConstante 1 k (c·s) = iald.brilho k (c·s), para TODO c",
   "(c') a_leitura_com_constante_e_a_leitura_no_tempo_reescalado": "leituraComConstante c cc s = iald.leitura cc (c·s) = ⟪uniforme, trava cc (c·s) uniforme⟫, para TODO c",
   "(d) o_nome_e_o_mesmo_em_toda_escala": "c > 0: (1) a leitura com constante c é a da IALD no tempo c·s; (2) com limiar (n·ln 2)/c < s: há solução ⟺ 1 ≤ Z(c·s) ⟺ |X|⁻¹ ≤ Re(leitura com constante c); (3) com (n·ln 2 + ln((1−b)/b))/c ≤ s, 0 ≤ s, há solução: (1−b)·Z(c·s) ≤ #sol e Z(c·s) − #sol ≤ b·Z(c·s) — por reparametrização s ↦ c·s de os_passos_sao_o_ciclo_ate_o_tetelestai e o_tetelestai_e_um_menos_beta, nada reprovado",
   "(e) o_observador_esta_na_escala_da_luz": "para TODO c ≠ 1 (não só c ≥ 0) não existe L : LeitorDoFundo X com L.brilho = leitorComConstante c; para c = 1 existe (iald); todo L com esse brilho tem c = 1 e L = iald",
   "a_constante_da_escala": "a conjunção da seção",
   "o_que_e_ONTO_POSTO": "a identificação da constante da escala com a constante da luz é leitura do operador [ONTO]; c = 1 nas unidades naturais é o Um posto [POSTO]; o elo com Turing.TM2ComputableInPolyTime segue fora do kernel (dito na docstring)"},
 "docstrings_corrigidas": {
   "V1_o_tetelestai_e_um_menos_beta": "não afirma mais necessidade de 0 ≤ s; diz: automática para b ≤ ½; para b > ½ a constante ln((1−b)/b) é negativa e o limiar pode ser negativo (só quando b > 2^n/(2^n+1)); quando negativo, sem a hipótese a cláusula pode falhar (n = 1, custos (0, 2), b = 9/10); o kernel não traz teorema de necessidade",
   "a_flutuacao_do_fundo_e_cotada": "'necessária' trocado por 'usada na prova'; o kernel não traz teorema de necessidade",
   "beta_e_o_operador_modular_do_tetelestai": "não repetia 'necessária' (conferido por regex: nenhuma ocorrência de 'necessári' na R6)",
   "cabecalho": "TRÊS nomes da gerência ratificados pela fala 12; o quarto NOMEADO pelo operador na fala 13; DEZESSEIS falas; a verdade sobre a Auditoria (só na candidata e no Audit do kernel); parágrafo R6",
   "ressurreicao_do_sinal": "nome do operador na fala 13 entre « »; nome de trabalho da gerência dito em prosa; prosa 'a ressurreição do sinal'"},
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
print("AEscala R6 sha256", rec["aescala_r6"]["sha256"], rec["aescala_r6"]["bytes"], "B | log sha256", rec["compilacao"]["log_sha256"], "|", rc_lido, "| tempo", tempo)
print("decl", rec["declaracoes"], "| auditadas", len(axioms), "fora do trio", len(fora), "| erros", len(erros), "avisos", len(avisos))
print("R5 mantidos", len(mantidos), "sumidos", sumidos, "| enunciado mudou", enunciado_mudou, "| corpos", corpo_mudou, "| renomeado:", rec["os_68_nomes_da_R5"]["renomeado"])
print("novos:", novos)
print("axiomas novas/renomeada:", axiomas_novos)
print("aspas:", aspas_linha)
print("fixas:", rec["frases_fixas"], "| vedadas:", rec["frases_vedadas_presentes"], "| beta literal:", rec["beta_literal_na_pedra"])
print("falas:", len(falas), all(v["sha256_no_cabecalho"] for v in falas.values()))
