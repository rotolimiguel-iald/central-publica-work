# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — gera o texto do depósito na fila da memória e o JSON da ANOTACAO no Mapa de Rotas da R6 FINAL
(emendas 2, 3 e 4 juntas). Todo hash e todo número é LIDO do arquivo aqui, nunca digitado. Só escreve em _build. uso: python gerar_registro_final.py"""
import hashlib, json, re
from pathlib import Path

OUT = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala")
BLD = OUT / "_build"
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
INST = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\pedra\AEscala.lean")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def nb(p): return Path(p).stat().st_size
def mil(n): return f"{n:,}".replace(",", " ")

lean, rec_p, log_p = OUT / "AEscala.lean", OUT / "RECIBO_AESCALA_R6_10nov.json", OUT / "compile_log.txt"
rec = json.loads(rec_p.read_text(encoding="utf-8"))
assert rec["aescala_r6"]["sha256"] == sha(lean), "o recibo nao e' desta candidata"
assert rec["compilacao"]["log_sha256"] == sha(log_p) and rec["compilacao"]["rc_lido_do_arquivo"] == "rc=0"
F = {18: CUN / "OPERADOR_10nov_ratifico_tudo_a_selecao_e_o_observador_a_forma_matricial_da_luz_torre_de_jones_verbatim.txt",
     19: CUN / "OPERADOR_10nov_nao_ha_contradicao_na_tonica_a_escala_e_a_unidade_posta_a_do_observador_e_de_outro_dominio_verbatim.txt",
     20: CUN / "OPERADOR_10nov_o_confronto_de_ideias_nos_faz_avancar_escala_igual_relatividade_verbatim.txt",
     21: CUN / "OPERADOR_10nov_o_que_e_relativo_o_que_e_par_sem_o_par_nao_ha_escala_verbatim.txt"}
pre1, pre2, pre3 = BLD / "pre_emenda_fala17" / "AEscala.lean", BLD / "pre_emenda2_fala18" / "AEscala.lean", BLD / "pre_emenda3_fala19" / "AEscala.lean"
m = re.search(r"real\s+(\d+)m([\d.]+)s", rec["compilacao"]["tempo"])
seg = int(m.group(1)) * 60 + float(m.group(2))
tempo = f"{seg:.1f}".replace(".", ",") + " s"
m2 = re.search(r"angulares restantes: (\d+)", rec["aspas"]["saida_so_medir"])
n_ang = m2.group(1)
d = rec["declaracoes"]
RAT = rec["nomes_novos"]["RATIFICADOS_pelo_operador_fala_18"]
AUT = rec["nomes_novos"]["DECLARADO_pela_autoria"]
assert len(RAT) == 6 and len(AUT) == 5 and rec["n_falas"] == 21 and rec["trio"]["todas_no_trio"] and rec["trio"]["n_auditadas"] == 79
V = dict(
    lean_b=mil(nb(lean)), lean_sha=sha(lean), rec_sha=sha(rec_p), log_sha=sha(log_p),
    pre1_sha=sha(pre1), pre2_sha=sha(pre2), pre3_sha=sha(pre3),
    f18_sha=sha(F[18]), f18_b=nb(F[18]), f19_sha=sha(F[19]), f19_b=nb(F[19]), f20_sha=sha(F[20]), f20_b=nb(F[20]), f21_sha=sha(F[21]), f21_b=nb(F[21]),
    tempo=tempo, n_ang=n_ang, n_decl=d["n_R6"], n_teo=d["n_teoremas_R6"], n_def=d["n_defs_R6"], n_str=d["n_structures_R6"],
    n_aud=rec["trio"]["n_auditadas"], linhas=rec["aescala_r6"]["linhas"], inst16=sha(INST)[:16],
    can=rec["frases_fixas"]["canonica_D84"][1], d94=rec["frases_fixas"]["forma_do_tempo_D94"][1],
    rat=", ".join(f"`{n}`" for n in RAT), aut=", ".join(f"`{n}`" for n in AUT),
    rat_txt=", ".join(RAT), aut_txt=", ".join(AUT))
assert V["inst16"] == "7d1557f961783679"

DEP = """AEscala R6 FINAL — emendas 2, 3 e 4 (falas 18, 19, 20 e 21): só docstring e cabeçalho; a pedra fecha (10/11/2026; autor claude-autor-aescala)

AO LADO dos depósitos seq 519 (a R6 antes das emendas, sha256 {pre1_sha}) e seq 520 (a R6 com a primeira emenda, sha256 {pre2_sha}, guardada em `_build\\pre_emenda2_fala18`). A candidata da segunda emenda (sha256 {pre3_sha}, compilada na rodada 5) não teve depósito próprio e fica como registro em `_build\\pre_emenda3_fala19`. A candidata vigente é esta, e é a FINAL: a gerência avisou que não vem outra emenda.

Arquivos em `C:\\IALD\\Central de Patentes\\work\\pedras_candidatas_09nov\\R6_a_constante_da_escala\\`: `AEscala.lean` ({lean_b} B, {linhas} linhas, sha256 {lean_sha}); `RECIBO_AESCALA_R6_10nov.json` (sha256 {rec_sha}); `compile_log.txt` (sha256 {log_sha}).

O que mudou desde a primeira emenda, SÓ em docstring e cabeçalho (conferido por script contra a candidata da segunda emenda e desta contra a primeira: código fora de comentário idêntico, declarações, enunciados e blocos iguais, imports e seção Auditoria iguais):

1. SEGUNDA EMENDA (fala 18, {f18_b} bytes, sha256 {f18_sha}). RATIFICADOS pelo operador os SEIS nomes da §7 que a gerência lhe mostrou: {rat}. Seguem [DECLARADO pela autoria], porque não lhe foram mostrados: {aut}. Cada docstring carrega a sua marca; o cabeçalho e a nota OS NOMES da §7 dizem o mesmo. A RAZÃO entra na docstring da §7 como leitura do operador [ONTO], por bytes, com os espelhos do kernel ao lado, por nome (`a_nota_e_a_conjugacao_modular`; `TraducaoTuring.selecao` e `p_igual_np_no_modo_selecao`; `IALD2.a_iald_e_o_seletor_luminodinamico`; `ObservadorTerminal.the_terminal_is_unique`; os módulos `TheTowerConjugation`, `TowerModular`, `IALDJones`, `TheIALDInTheTower`). O que une observador, seletor, IALD e Torre de Jones por UMA métrica não é teorema desta pedra: [OPEN]. A primeira oração da fala 18 (ponto que o operador deu por encerrado) NÃO é transcrita na pedra, por ordem da gerência; o sha256 pina a fala inteira.

2. TERCEIRA EMENDA (fala 19, {f19_b} bytes, sha256 {f19_sha}). O parágrafo DOIS DOMÍNIOS na docstring da §7: a fala por bytes, como leitura dele [ONTO]; e os objetos do kernel de cada domínio, por nome. Na TÔNICA (a energia) a escala é a unidade posta: `TonicaDoHamiltoniano.the_scale_is_free`, `TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit`, `LeiDoDiminuto.tonica`. No TEMPO (computação, processamento, relatividade) a escala do observador é a constante da seção: `leitorComConstante`, `a_constante_da_luz_e_a_escala_do_tempo`. São objetos distintos e a pedra NÃO deriva um do outro. Em `tudo_depende_da_escala`, o item (i) fala da escala da tônica e o item (iv) da escala do tempo. A frase da fala 17 sobre o posto fica por bytes, com a nota de que foi dita do LEITOR; conferido no arquivo inteiro que nenhuma frase da autoria diz que posto nunca é escala.

3. QUARTA EMENDA (fala 20, {f20_b} bytes, sha256 {f20_sha}; fala 21, {f21_b} bytes, sha256 {f21_sha}). O parágrafo O FECHO, no fim da docstring de abertura da §7: as duas falas por bytes, como leitura do operador [ONTO] (escala = relatividade; o que é relativo é par; sem o par não há escala); e ao lado o que o kernel PROVA, por nome: uma constante sozinha é absorvida no tempo (`a_constante_da_luz_e_a_escala_do_tempo`); o que resta é a razão de duas (`comparar_a_escala_e_nivelar_a_frequencia`); o invariante (`o_nome_e_o_mesmo_em_toda_escala`); no domínio da tônica, `TonicaDoHamiltoniano.the_scale_is_free` com `TonicaDoHamiltoniano.the_ratio_survives_the_rescaling`; e o par já era a coexistência da pedra (`o_par_coexiste`, `nenhum_precede`, §5). A identificação da escala com a relatividade é leitura dele [ONTO]; a lei ÚNICA dos dois domínios (a tônica e o tempo) não é teorema desta pedra: [OPEN]. Nenhum teorema novo. Acréscimos da autoria no parágrafo, para a gerência ver: as hipóteses dos teoremas citados, entre parênteses (c′ ≠ 0; c > 0), e uma oração de estatuto dizendo que o par da §5 (Nome objeto / Nome lido) e a razão de duas constantes serem o mesmo par é leitura dele, porque a pedra não traz lema ligando um ao outro.

Compilação [REAL]: a candidata final foi compilada UMA vez (rodada 7, `lake env lean` só no arquivo externo): rc 0 em {tempo}; 0 erros, 0 avisos, 0 sorry, 0 axiom; {n_decl} declarações ({n_teo} teoremas, {n_def} defs, {n_str} structure); {n_aud} auditadas, todas no trio; o sha256 da candidata foi lido antes e depois da compilação e é o do arquivo final; o log é byte a byte o da rodada 5, como se espera de emenda só de comentário. Aspas: trocas 0 ({n_ang} angulares, todas verbatim). Frase canônica D84 ({can}) e forma do tempo D94 ({d94}) intactas; nenhuma frase vedada; β nunca literal. Cabeçalho com VINTE E UMA falas por sha256. Nada instalado; `v410\\pedra` intocada (sha16 {inst16} conferido ao gerar o recibo); cadeia não rodada.

CONTA HONESTA e LIÇÃO: a rodada 6 foi DESPERDIÇADA por erro da autoria. A montagem da terceira emenda parou numa conferência do próprio montador (ele contava a palavra que só pode aparecer como “unidade posta” também no NOME DO ARQUIVO da fala 19, que a traz com sublinhado: a conferência estava errada, não a pedra) e a linha de comandos, encadeada por pipe sem `pipefail`, não parou: recompilou o arquivo da segunda emenda, rc 0, sem valor para a terceira. Regra que fica: conferir o código de saída de CADA etapa antes da seguinte e ler o sha256 da candidata antes e depois de compilar. Sete rodadas ao todo na R6 (a ordem original e as quatro emendas).
"""
dep = DEP.format(**V)
(BLD / "deposito_r6_final.md").write_text(dep, encoding="utf-8", newline="\n")

ROTA = {
 "tipo": "ANOTACAO",
 "rota_id": "kernel.a_escala_tres_faces_v410_09nov",
 "titulo": "AEscala R6 FINAL, emendas 2, 3 e 4 juntas (falas 18 a 21; ao lado dos seq 1951 e 1952): seis nomes da secao 7 RATIFICADOS, cinco auxiliares DECLARADO pela autoria; os dois dominios; o fecho (escala = relatividade, leitura do operador); so' docstring e cabecalho; 79 declaracoes no trio; a pedra fecha",
 "metodo": "Sobre a candidata do seq 1952 (guardada ao lado). So' comentarios mudaram: conferido por script (codigo fora de comentario identico, com aninhamento; declaracoes, enunciados e blocos iguais; imports e Auditoria iguais). Objetos do kernel citados conferidos por leitura dos arquivos do sandbox (TonicaDoHamiltoniano, LeiDoDiminuto, TraducaoTuring, IALD2, ObservadorTerminal). A candidata final teve UMA compilacao (rodada 7): lake env lean so' no arquivo externo, com o sha256 lido antes e depois.",
 "resultado": "rc 0 em {tempo}; 0 erros; 0 avisos; 0 sorry; 0 axiom; {n_decl} declaracoes ({n_teo} teoremas, {n_def} defs, {n_str} structure); {n_aud} auditadas, todas no trio; log identico ao da rodada 5. RATIFICADOS (fala 18): {rat_txt}. DECLARADO pela autoria: {aut_txt}. Paragrafo DOIS DOMINIOS (fala 19): na tonica a escala e' a unidade posta (TonicaDoHamiltoniano.the_scale_is_free, the_tonic_lands_on_the_posted_unit, LeiDoDiminuto.tonica); no tempo, a constante da secao (leitorComConstante, a_constante_da_luz_e_a_escala_do_tempo); objetos distintos, a pedra nao deriva um do outro. Paragrafo O FECHO (falas 20 e 21): o kernel prova que uma constante sozinha e' absorvida no tempo, que resta a razao de duas, e o invariante; a identificacao com a relatividade e' leitura do operador. Vinte e uma falas por sha256 no cabecalho. Aspas: trocas 0, {n_ang} angulares verbatim.",
 "veredito": "AESCALA_R6_FINAL__79_DECL_68_TEOREMAS__TRIO__QUATRO_EMENDAS__SEIS_NOMES_RATIFICADOS__CINCO_AUXILIARES_DECLARADOS__LEI_UNICA_DOS_DOIS_DOMINIOS_OPEN__NAO_INSTALADA",
 "estatuto": "REAL (compilacao e trio); ONTO (a razao da fala 18; os dois dominios da fala 19; escala = relatividade e o par, falas 20 e 21; que a constante seja a da luz; que o posto seja dominio; a cadeia como dependencia fisica); OPEN (o que une observador, seletor, IALD e Torre de Jones por uma metrica; a lei unica dos dois dominios, a tonica e o tempo: nenhum dos dois e' teorema desta pedra); DECLARADO (os cinco auxiliares da autoria)",
 "status": "EXAMINADA",
 "olhou_dados": False,
 "defeito": "A rodada 6 foi desperdicada por erro da autoria: a montagem da terceira emenda parou numa conferencia errada do proprio montador e a linha de comandos, sem pipefail, recompilou o arquivo da segunda emenda (rc 0, sem valor). A primeira oracao da fala 18 nao foi transcrita na pedra (ordem da gerencia); o sha256 pina a fala inteira. A secao 7 nao acrescenta elo com a maquina do Mathlib (Turing.TM2ComputableInPolyTime), que segue fora do kernel. No paragrafo O FECHO ha dois acrescimos da autoria (as hipoteses c' != 0 e c > 0 entre parenteses; a oracao dizendo que o par da secao 5 e a razao de duas constantes serem o mesmo par e' leitura do operador, sem lema na pedra).",
 "nao_refazer": "Nao recompilar a R6 final (log rc 0, trio, 0 avisos; sha256 lido antes e depois). Na secao 7, nao escrever que a escala do leitor e' posta, nem voltar ao ponto que o operador deu por encerrado na fala 18. Nao tentar derivar a escala do tempo da escala da tonica (ou o inverso) dentro desta pedra: sao objetos distintos, sem lema de ligacao; a lei unica esta' OPEN.",
 "proximo_passo": "Construtor: instalar a R6 final (retirando a secao Auditoria), ancoras e bandeiras novas, as falas 13 a 21 no conjunto congelado. Gerencia: decidir se mostra ao operador os cinco auxiliares da autoria e os dois acrescimos da autoria no paragrafo O FECHO.",
 "onde": "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R6_a_constante_da_escala/AEscala.lean (namespace TGLExt.AEscala, secao ConstanteDaEscala)",
 "artefatos": [
  "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R6_a_constante_da_escala/AEscala.lean",
  "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R6_a_constante_da_escala/RECIBO_AESCALA_R6_10nov.json",
  "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R6_a_constante_da_escala/compile_log.txt"
 ],
 "nota": "As candidatas dos seq 1951 ({pre1_sha}) e 1952 ({pre2_sha}) e a da segunda emenda ({pre3_sha}, sem registro proprio no mapa) ficam em _build; a vigente e' a deste registro ({lean_sha}). Falas, sha256 lidos do arquivo por script: 18 {f18_sha} ({f18_b} bytes); 19 {f19_sha} ({f19_b} bytes); 20 {f20_sha} ({f20_b} bytes); 21 {f21_sha} ({f21_b} bytes)."
}
rota = {k: (v.format(**V) if isinstance(v, str) else v) for k, v in ROTA.items()}
(BLD / "rota_anotacao_r6_final.json").write_text(json.dumps(rota, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print("deposito:", nb(BLD / "deposito_r6_final.md"), "B | rota json:", nb(BLD / "rota_anotacao_r6_final.json"), "B")
print("lean", V["lean_sha"], V["lean_b"], "B |", V["linhas"], "linhas")
print("recibo", V["rec_sha"])
print("log", V["log_sha"], "| tempo", V["tempo"], "| angulares", V["n_ang"])
print("pre1", V["pre1_sha"][:16], "pre2", V["pre2_sha"][:16], "pre3", V["pre3_sha"][:16])
# as aspas angulares do depósito: só fala do operador (nenhuma aqui)
print("aspas angulares no deposito:", dep.count("\u00ab"), "| chaves nao preenchidas:", bool(re.search(r"\{[a-z0-9_]+\}", dep)))
