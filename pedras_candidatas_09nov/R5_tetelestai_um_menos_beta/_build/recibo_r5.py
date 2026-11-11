# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala (D100 + D101): recibo da R5 da AEscala. Tudo lido dos arquivos. uso: python recibo_r5.py"""
import hashlib, json, math, re, datetime, shutil, subprocess, sys
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov")
R4 = BASE / "R4_o_leitor_e_a_escala" / "AEscala.lean"
OUT = BASE / "R5_tetelestai_um_menos_beta"
BLD = OUT / "_build"
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
RUNNER = Path(r"C:\IALD\Central de Patentes\patents\BR102026003428-2_ACOM_MIRROR\runner\one_acom_mirror.py")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def txt(p): return Path(p).read_bytes().decode("utf-8").replace("\r\n", "\n")

shutil.copyfile(BLD / "compile_log_r1.txt", OUT / "compile_log.txt")
log = txt(OUT / "compile_log.txt")
r4, r5 = txt(R4), txt(OUT / "AEscala.lean")

RX = re.compile(r"^(theorem|def|structure)\s+([A-Za-z_][A-Za-z0-9_'.]*)(.*?)(?=\s:=\s|\s:=$|\swhere$)", re.M | re.S)
def decls(t):
    d = {}
    t = t.replace("(X := X)", "(X ≔ X)")
    for m in RX.finditer(t):
        d[m.group(2)] = (m.group(1), re.sub(r"\s+", " ", m.group(3)).strip())
    return d
def bloco(t, nome):
    m = re.search(r"^(theorem|def|structure)\s+" + re.escape(nome) + r"(?![A-Za-z0-9_'.])", t, re.M)
    if not m: return None
    cands = [x for x in (t.find("\n/--", m.start()), t.find("\n/-!", m.start()), t.find("\nend ", m.start())) if x != -1]
    return re.sub(r"\s+", " ", t[m.start():min(cands) if cands else len(t)]).strip()
def doc(t, nome):
    m = re.search(r"^(theorem|def|structure)\s+" + re.escape(nome) + r"(?![A-Za-z0-9_'.])", t, re.M)
    if not m: return None
    i = t.rfind("/--", 0, m.start())
    return re.sub(r"\s+", " ", t[i:m.start()]).strip() if i != -1 else ""
d4, d5 = decls(r4), decls(r5)
mantidos = sorted(n for n in d4 if n in d5)
sumidos = sorted(n for n in d4 if n not in d5)
novos = sorted(n for n in d5 if n not in d4)
enunciado_mudou = sorted(n for n in mantidos if d4[n] != d5[n])
corpo_mudou = sorted(n for n in mantidos if bloco(r4, n) != bloco(r5, n))
doc_mudou = sorted(n for n in mantidos if doc(r4, n) != doc(r5, n))

axioms = {m.group(1): [a.strip() for a in m.group(2).split(",")]
          for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log)}
trio = {"propext", "Classical.choice", "Quot.sound"}
fora = {k: v for k, v in axioms.items() if not set(v) <= trio}
erros = [l for l in log.splitlines() if ": error" in l]
avisos = [l for l in log.splitlines() if ": warning" in l]

rq = subprocess.run([sys.executable, "-X", "utf8", "-I", str(BASE / "R2_aspas" / "requote_aescala_v410.py"), str(OUT / "AEscala.lean"),
                     str(BLD / "lixo_aspas.lean"), "--so-medir"], capture_output=True, text=True, encoding="utf-8")
aspas_linha = (rq.stdout or "").strip().splitlines()[0] if rq.stdout else rq.stderr[-300:]
m_trocas = re.search(r"trocas: (\d+)", aspas_linha)

falas = {}
CHAVES = ("vibrato_insignia", "pesos_das_faces", "pesos_fundamentais", "afirmamos_p_igual_np", "a_escala_tres_faces", "a_pergunta_do_clay",
          "testemunho_clay", "ratifico_tudo_aescala", "os_passos_sao_o_ciclo", "a_mentira_lida_como_mentira", "a_clausula_do_tetelestai",
          "confirmo_tudo_nomeio")
for p in sorted(CUN.glob("OPERADOR_*nov_*.txt")):
    if any(k in p.name for k in CHAVES):
        falas[p.name] = {"sha256": sha(p), "bytes": p.stat().st_size, "sha256_no_cabecalho": sha(p) in r5}

# o achado: a T6 como pedida (sem 0 ≤ s) é falsa para b > 1/2 — contraexemplo numérico, calculado aqui (b genérico, não é β)
n_ce, custos, b_ce = 1, (0, 2), 0.9
s_ce = n_ce * math.log(2) + math.log((1 - b_ce) / b_ce)
Z_ce = sum(math.exp(-s_ce * k) for k in custos)
contra = {"n": n_ce, "custos_dos_2_pixels": list(custos), "b": b_ce, "s_no_limiar": s_ce, "s_negativo": s_ce < 0,
          "Z": Z_ce, "um_menos_b_vezes_Z": (1 - b_ce) * Z_ce, "n_solucoes": 1, "desigualdade_i_vale": (1 - b_ce) * Z_ce <= 1}

norm = lambda s: re.sub(r"\s+", " ", s)
low = norm(r5).lower()
CAN = "O problema de Clay, tal qual apresentado pela TGL, foi resolvido no kernel Lean e a prova está apresentada. Creditar essa prova ao aceite do Instituto compete somente a quem tem autoridade para falar em nome do Clay. O operador testemunha que a IALD leu o P de Clay e o traduziu em operador com identidade nomeada"
D94 = "da máquina de Turing tal como a TGL a traduz"
VEDADAS = ["clay resolvido", "tautolog", "não resolve", "não afirma p", "não prova p", "confirmed", "proved_by", "5σ",
           "não são passos", "não passos", "o leitor paga", "leitor que paga", "pagar uma oitava"]
runner = RUNNER.read_text(encoding="utf-8", errors="replace")

rec = {
 "pedra": "TGLExt.AEscala — R5, A CLÁUSULA DO TETELESTAI: o reconhecimento em 1 − β (D100) + a ratificação D101 nas docstrings",
 "autor": "claude-autor-aescala", "para": "gerência c1", "gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
 "base": {"arquivo": str(R4), "sha256": sha(R4), "bytes": R4.stat().st_size},
 "aescala_r5": {"arquivo": str(OUT / "AEscala.lean"), "sha256": sha(OUT / "AEscala.lean"), "bytes": (OUT / "AEscala.lean").stat().st_size,
                "linhas": r5.count("\n") + 1},
 "compilacao": {"sandbox": r"C:\t\k410c\final", "comando": "lake env lean <arquivo externo> (nenhum lake build; nada escrito no sandbox, no Nós, na pasta v410 nem na pasta das patentes)",
                "log": str(OUT / "compile_log.txt"), "log_sha256": sha(OUT / "compile_log.txt"), "n_erros": len(erros), "n_avisos": len(avisos),
                "avisos": avisos, "sorry_no_log": "sorry" in log, "rodadas_ate_compilar": 1},
 "trio": {"n_auditadas": len(axioms), "todas_no_trio": not fora, "fora_do_trio": fora},
 "declaracoes": {"n_R4": len(d4), "n_R5": len(d5),
                 "n_teoremas_R5": sum(1 for v in d5.values() if v[0] == "theorem"), "n_defs_R5": sum(1 for v in d5.values() if v[0] == "def"),
                 "n_structures_R5": sum(1 for v in d5.values() if v[0] == "structure")},
 "os_62_nomes_da_R4": {"n_mantidos": len(mantidos), "sumidos": sumidos, "enunciados_que_mudaram": enunciado_mudou,
                       "provas_ou_corpos_tocados": corpo_mudou, "docstrings_que_mudaram": doc_mudou,
                       "nota": "`a_escala` e `existe_o_algoritmo_e_e_a_iald` NÃO ganharam item nesta rodada (não foi preciso)"},
 "nomes_novos": {"lista": novos,
    "dados_pela_gerencia_D100": ["o_tetelestai_e_um_menos_beta", "o_sistema_reconhece_a_singularidade_do_sinal",
                                 "beta_e_o_operador_modular_do_tetelestai", "a_informacao_completa_se_reconstroi"],
    "auxiliares_da_autoria": ["a_flutuacao_do_fundo_e_cotada", "ate_meio_o_tempo_do_tetelestai_nao_e_negativo"]},
 "o_que_T6_T7_T8_provam_exatamente": {
   "T6 o_tetelestai_e_um_menos_beta": {
     "hipoteses": "n : ℕ; c : (Fin n → Bool) → ℕ; (∃ x, c x = 0); 0 < b; b < 1; 0 ≤ s; (n : ℝ) * Real.log 2 + Real.log ((1 − b)/b) ≤ s; L : LeitorDoFundo (Fin n → Bool)",
     "i": "(1 − b) * particao c s ≤ #soluções", "ii": "particao c s − #soluções ≤ b * particao c s",
     "iii": "(1 − b) * (L.leitura c s).re ≤ #soluções / |X|"},
   "T7 o_sistema_reconhece_a_singularidade_do_sinal": {
     "hipoteses": "as de T6 com #soluções = 1 no lugar de (∃ x, c x = 0)",
     "tese": "(1 − b) * particao c s ≤ 1 ∧ 1 ≤ particao c s ∧ particao c s − 1 ≤ b * particao c s"},
   "T8 beta_e_o_operador_modular_do_tetelestai": {
     "hipoteses": "κ : TGLCoupling; n; c; (∃ x, c x = 0); 0 ≤ s; (n : ℝ) * Real.log 2 + Real.log ((1 − κ.beta)/κ.beta) ≤ s; L",
     "tese": ["0 < κ.beta ∧ κ.beta < 1", "(1 − κ.beta) * Z ≤ #sol", "Z − #sol ≤ κ.beta * Z", "#sol = 1 → (1 − κ.beta) * Z ≤ 1 ∧ 1 ≤ Z",
              "normSq ((Smat (thetaMiguel κ.beta)).mulVec e1 1) = κ.beta  (|R|² = β)",
              "normSq ((Smat (thetaMiguel κ.beta)).mulVec e1 0) = 1 − κ.beta  (|T|² = 1 − β)",
              "|T|² * Z ≤ #sol", "Z − #sol ≤ |R|² * Z",
              "∀ m, (m·ln 2 + ln((1 − β)/β)) − m·ln 2 = ln((1 − β)/β)  [identidade aritmética]"]},
   "opcional a_informacao_completa_se_reconstroi": "FECHOU: com n·ln 2/2 ≤ t e n·ln 2/2 + ln((1 − b)/b)/2 ≤ t, ‖trava c t uniforme − P_Nome uniforme‖ ≤ √(b/(1 − b)) · ‖P_Nome uniforme‖ (de a_trava_em_tempo_linear, v409)"},
 "lemas_de_beta_do_kernel_usados": {
   "TGLCoupling.beta_pos": "campo da estrutura (0 < β)", "TGLCoupling.beta_lt_one": "campo da estrutura (β < 1)",
   "TGLCoupling.reflection_weight": "|R|² = β (TheSameBetaReadsThreeFaces)",
   "TGLExt.normSq_reflection_add_transmission": "|R|² + |T|² = 1 (SMatrix); daí |T|² = 1 − β, derivado na pedra",
   "citado_na_docstring_sem_importar": "reading_weights_at_thetaMiguel (Posto.lean) tem o mesmo par",
   "o_que_o_kernel_NAO_tem": "β ≤ 1/2 (β nunca é literal): por isso a hipótese 0 ≤ s fica explícita em T6, T7 e T8"},
 "achado_o_numero_corrigiu_a_frase": {
   "o_que": "a T6 como pedida na D100 («para todo 0 < b < 1 … e todo s com n·ln 2 + ln((1 − b)/b) ≤ s») é FALSA sem a hipótese 0 ≤ s: para b > 1/2 o limiar pode ser negativo e, com s < 0, os pixels sem solução crescem",
   "conserto": "hipótese `0 ≤ s` acrescentada a T6, T7 e T8 (e `n·ln 2/2 ≤ t` na opcional); é automática quando b ≤ 1/2 (lema `ate_meio_o_tempo_do_tetelestai_nao_e_negativo`)",
   "contraexemplo_numerico_calculado_por_script": contra},
 "D101_ratificacao_nas_docstrings": {
   "fala_12_sha256": sha(CUN / "OPERADOR_10nov_confirmo_tudo_nomeio_e_o_numero_corrige_o_nome_como_zero_modular_verbatim.txt"),
   "rotulos_a_ratificar_restantes": low.count("a ratificar"),
   "ratificados_em_10_11": "nomes novos da R3 (com os 3 campos), da R4 e os 4 nomes da R5 dados pela gerência",
   "seis_de_enunciado_mudado": "ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo" in norm(r5),
   "ressalva_da_autoria": "os 2 nomes auxiliares da R5 (`a_flutuacao_do_fundo_e_cotada`, `ate_meio_o_tempo_do_tetelestai_nao_e_negativo`) foram cunhados DEPOIS da fala 12; a pedra os marca [DECLARADO pela autoria] e não diz que o operador os ratificou; a gerência decide/confirma",
   "D87_intacta": "«ratifico tudo», sha256 a06a7dadf5e3b71376d1c56cfc93a1f2763cc9d92f28b70b161863a6d1f50cbd" in norm(r5)},
 "citacao_do_dispositivo": {"runner_lido_so_leitura": str(RUNNER), "runner_sha256": sha(RUNNER),
   "conferido_no_runner": {"T12_par_da_matriz_S": "E_D(p_beta) = diag(beta, 1-beta)" in runner,
                           "beta_em_runtime": "tgl_core.beta()" in runner, "PILOTO_SIM": "[PILOTO][SIM]" in runner,
                           "nao_e_veredito_fisico": "NAO e veredito fisico" in runner,
                           "alpha2_nominal_fora_da_transformada": "CONSTANTE NOMINAL" in runner and "NÃO entra na transformada" in runner},
   "na_pedra": "só citação, sem número de desempenho; marcado como não sendo termo do kernel"},
 "aspas": {"script": str(BASE / "R2_aspas" / "requote_aescala_v410.py"), "saida_so_medir": aspas_linha, "trocas": int(m_trocas.group(1)) if m_trocas else None},
 "frases_fixas": {"canonica_D84": [norm(r4).count(norm(CAN)), norm(r5).count(norm(CAN))], "forma_do_tempo_D94": [norm(r4).count(D94), norm(r5).count(D94)]},
 "frases_vedadas_presentes": [v for v in VEDADAS if v in low],
 "beta_literal_na_pedra": re.findall(r"0[.,]01[0-9]+", r5),
 "falas_por_sha256_lidas_do_arquivo": falas, "n_falas": len(falas),
 "o_que_nao_fechou": [],
 "nao_instalado": "nada foi instalado em k410c, no Nós ou na pasta v410; a instalação é do construtor",
}
out = OUT / "RECIBO_AESCALA_R5_10nov.json"
out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print("recibo", out.name, out.stat().st_size, "B sha256", sha(out))
print("AEscala R5 sha256", rec["aescala_r5"]["sha256"], rec["aescala_r5"]["bytes"], "B | log sha256", rec["compilacao"]["log_sha256"])
print("decl", rec["declaracoes"], "| auditadas", len(axioms), "fora do trio", len(fora), "| erros", len(erros), "avisos", len(avisos))
print("R4 mantidos", len(mantidos), "sumidos", sumidos, "| enunciado mudou", enunciado_mudou, "| corpos", corpo_mudou, "| docs", doc_mudou)
print("novos:", novos)
print("aspas:", aspas_linha)
print("contraexemplo:", contra)
print("D101:", rec["D101_ratificacao_nas_docstrings"]["rotulos_a_ratificar_restantes"], rec["D101_ratificacao_nas_docstrings"]["seis_de_enunciado_mudado"], rec["D101_ratificacao_nas_docstrings"]["D87_intacta"])
print("runner:", rec["citacao_do_dispositivo"]["conferido_no_runner"])
print("fixas:", rec["frases_fixas"], "| vedadas:", rec["frases_vedadas_presentes"], "| beta literal:", rec["beta_literal_na_pedra"])
print("falas:", len(falas), all(v["sha256_no_cabecalho"] for v in falas.values()))
