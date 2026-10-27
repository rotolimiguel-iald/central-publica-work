# -*- coding: utf-8 -*-
"""montar_runtime_v400.py -- monta runtime_v400.py, o CODIGO da secao do selo pela propria tecnologia na v400, a partir de runtime_v399.py (o que a v399 SELADA embutiu; pinado por sha256 e conferido contra o um.py base)
com as EDICOES DECLARADAS abaixo, cada uma com contagem exata (o script ABORTA se nao casar). Todas sao da ADAPTACAO da gerencia (o trecho ANTES do primeiro marcador ACOM_EMBUTIDO_INICIO, mais o registro e o seu ponto de chamada);
o BLOCO do operador (acom_mirror.py e acom_crypto.py, do primeiro marcador de inicio ao ultimo de fim) NAO muda: seu hash segue o do manifesto (afc80b740f71ca0a...) e as 5 substituicoes declaradas seguem as 5.
  A1 alfa NAO e' mais redeclarado: a linha `ALPHA_FINE_CODATA_2018 = 0.0072973525693 ...` (coluna 0) e o assert que a comparava com SEALED_CODATA_ALPHA saem; entra um comentario. A Bancada (esboco R3.5, A11) exige UMA so' linha de alfa
     no programa: a v399 trazia duas (a do script embutido do nivel 2, na linha 5584, que e' o texto que o canonical.py da Bancada le, e esta, da secao) e o B(n) pos-selo foi RECUSADO (ALPHA_LINHA_NAO_UNICA: 2 linhas nao indentadas);
  A2 _beta_runtime() le o alfa do PROPRIO programa (SEALED_CODATA_ALPHA, a constante selada do um.py; no um.py v399 o nome ALPHA_FINE_CODATA_2018 so' existia como a redeclaracao da secao: a linha 5584 e' texto dentro do script embutido do nivel 2);
  A3 o registro `selo_pela_propria_tecnologia_v399` (nome nascido no um.py: NAO sobe) deixa de ter a checagem «beta do runtime» tautologica (beta do runtime contra o mesmo alfa x raiz de e): recebe `beta_core` e a checagem confronta com o beta do CORE do rito
     a 1e-9 (sem beta_core a checagem REPROVA: fail-closed); os valores `beta_core` e `rel_beta_vs_core` entram no registro (BAIXA B1 do exame final da v399);
  A4 o ponto de chamada (selo_acom_v399) passa core.get("beta") ao registro;
  A5 uma linha de cabecalho dita a correcao.
Confere, por script (acom_conferencias_v400): C1, C2, C3, C9 (as da v399, sobre o texto v400), C3' e C10 (a secao nao define nem redeclara alfa; as regexes da guarda ALPHA_LINHA_UNICA vem do PROPRIO esboco R3.5 pinado) e C11 (o hash do bloco nao mudou).
Escreve so' em v400: runtime_v400.py e RUNTIME_MONTAGEM_v400.json. Reexecutavel (backup de bytes antes de sobrescrever). uso: python -I -B -X utf8 montar_runtime_v400.py"""
import ast, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
import acom_conferencias_v400 as AC  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
OUT = DL.RUNTIME_V400
IN = DL.RUNTIME_V399
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"      # o pino do esboco R3.5 (PINOS_BN_v399.json); o import o confere contra o disco
edicoes = []
rt9_bytes = open(IN, "rb").read()
rm9 = json.load(open(os.path.join(DL.V399, "RUNTIME_MONTAGEM_v399.json"), encoding="utf-8"))
assert sha(rt9_bytes) == rm9["runtime"]["sha256"], "runtime_v399.py em disco nao e' o que RUNTIME_MONTAGEM_v399.json registra"
um_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")
RT9 = rt9_bytes.decode("utf-8")
assert "\r" not in RT9 and um_base.count(RT9.replace("\n", "\r\n")) == 1, "o runtime da v399 nao esta embutido, uma vez e byte a byte, no um.py base (v399 selada)"


def troca(t, velho, novo, n, nome):
    c = t.count(velho)
    assert c == n, ("edicao declarada nao casa o numero esperado de vezes", nome, c, n, velho[:80])
    edicoes.append({"edicao": nome, "ocorrencias": c})
    return t.replace(velho, novo)


def troca_re(t, pat, novo, n, nome, flags=re.M):
    t2, c = re.subn(pat, lambda m: novo, t, flags=flags)
    assert c == n, ("edicao declarada (regex) nao casa o numero esperado de vezes", nome, c, n, pat[:80])
    edicoes.append({"edicao": nome, "ocorrencias": c})
    return t2


RT = RT9
# A1: a redeclaracao de alfa (3 linhas: a atribuicao na coluna 0, o `if` e o assert) sai
RT = troca_re(RT, r'^ALPHA_FINE_CODATA_2018 = 0\.0072973525693[^\n]*\nif "SEALED_CODATA_ALPHA" in globals\(\):[^\n]*\n    assert SEALED_CODATA_ALPHA == ALPHA_FINE_CODATA_2018[^\n]*\n',
              "# v400 (correcao da v399): o alfa NAO e' redeclarado aqui. E' o do PROPRIO programa -- SEALED_CODATA_ALPHA (a constante selada do um.py): o programa tem UMA so' declaracao de alfa\n"
              "# (a Bancada, esboco R3.5 A11, recusou a v399 por ALPHA_LINHA_NAO_UNICA: esta secao a redeclarava numa linha nao indentada). Sem o nome o modulo nao carrega (NameError): fail-closed.\n",
              1, "A1_alfa_nao_e_redeclarado")
# A2: _beta_runtime le o alfa do programa
RT = troca(RT, "    return ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)\n", "    return SEALED_CODATA_ALPHA * math.sqrt(math.e)      # beta = alfa CODATA 2018 x raiz de e, EM RUNTIME, nunca literal; alfa = o do programa\n", 1, "A2_beta_runtime_le_o_alfa_do_programa")
# A3: o registro: beta_core entra e a checagem deixa de ser tautologica
RT = troca(RT, "def registro_core_v399(b_umpy: bytes, sha256_do_codigo: str = None, amostra: int = 1 << 20) -> Dict[str, Any]:",
           "def registro_core_v399(b_umpy: bytes, sha256_do_codigo: str = None, amostra: int = 1 << 20, beta_core: float = None) -> Dict[str, Any]:", 1, "A3a_assinatura_com_beta_core")
RT = troca(RT, "    beta = _beta_runtime()\n    ok_beta = bool(abs(beta / (ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)) - 1.0) < 1e-15)\n",
           "    beta = _beta_runtime()\n"
           "    # v400 (BAIXA B1 do exame da v399): a checagem NAO e' mais tautologica (o beta do runtime contra o mesmo alfa x raiz de e). Confronta com o beta do CORE do rito, que o main calcula por outro caminho (alfa = sqrt(1-q^2)),\n"
           "    # a 1e-9; sem o beta do core a checagem REPROVA (fail-closed).\n"
           "    rel_beta_core = (abs(beta / float(beta_core) - 1.0) if (beta_core is not None and float(beta_core) > 0.0) else None)\n"
           "    ok_beta = bool(rel_beta_core is not None and rel_beta_core < 1e-9)\n", 1, "A3b_checagem_do_beta_contra_o_core")
RT = troca(RT, '        ("beta do runtime (jamais literal)", ok_beta),\n', '        ("beta do runtime (jamais literal) == o beta do core do rito a 1e-9", ok_beta),\n', 1, "A3c_rotulo_da_checagem")
RT = troca(RT, '        "values": {"beta": beta, "perfil": PERFIL_ID, "bloco_embutido_sha256": ACOM_PROVENIENCIA["bloco_embutido_sha256"],\n                   "tempo_total_s": time.perf_counter() - t0},\n',
           '        "values": {"beta": beta, "beta_core": beta_core, "rel_beta_vs_core": rel_beta_core, "perfil": PERFIL_ID, "bloco_embutido_sha256": ACOM_PROVENIENCIA["bloco_embutido_sha256"],\n                   "tempo_total_s": time.perf_counter() - t0},\n',
           1, "A3d_valores_beta_core")
# A4: o ponto de chamada
RT = troca(RT, "    out_ = registro_core_v399(b_, sha256_do_codigo=sha_file(p_))\n", "    out_ = registro_core_v399(b_, sha256_do_codigo=sha_file(p_), beta_core=core.get(\"beta\"))\n", 1, "A4_ponto_de_chamada_passa_o_beta_do_core")
# A5: o cabecalho diz a correcao
RT = troca(RT, "O gate nao se move. ======================\n\nACOM_PROVENIENCIA = {",
           "O gate nao se move. ======================\n"
           "# v400 (24/10/2026): CORRECAO da v399, so' da ADAPTACAO (o bloco do operador, de ACOM_EMBUTIDO_INICIO a ACOM_EMBUTIDO_FIM, NAO muda; hash abaixo): a secao deixa de redeclarar alfa (a Bancada recusou o B(n) da v399: ALPHA_LINHA_NAO_UNICA) e passa a ler\n"
           "# SEALED_CODATA_ALPHA; a checagem «beta do runtime» do registro passa a confrontar com o beta do core do rito (BAIXA B1 do exame da v399). Nada mais mudou aqui: mesmo selo ACOM, mesmo perfil, mesmos 13 controles, mesmo sidecar.\n"
           "\nACOM_PROVENIENCIA = {", 1, "A5_cabecalho_da_correcao")
ast.parse(RT)
assert "\r" not in RT
# conferencias sobre o texto MONTADO (como vai para o um.py)
# a base (v399 selada) JA traz a secao v399: a colisao (C3) se mede contra a base SEM ela (a secao v400 ocupa o lugar exato da v399)
RT9_CRLF = RT9.replace("\n", "\r\n")
base_sem_secao = um_base.replace(RT9_CRLF, "")
assert len(base_sem_secao) == len(um_base) - len(RT9_CRLF)
nomes_base = AC.nomes_de_nivel_de_modulo(base_sem_secao)
regexes = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
bloco9 = AC.extrair_bloco(RT9)
conf = AC.conferir_secao(RT, nomes_base=nomes_base, regexes=regexes, bloco_v399_sha256=sha(bloco9.encode("utf-8")))
falhas = [k for k, v in conf.items() if not v["ok"]]
assert not falhas, ("conferencia da secao falhou", falhas, {k: conf[k] for k in falhas})
# o texto antigo (v399) reprova C3' e C10: o controle negativo da conferencia (a regra pega o defeito real)
neg = AC.conferir_alfa_unico(RT9, regexes)
assert (not neg["C3p_a_secao_nao_define_ALPHA_FINE_CODATA_2018"]["ok"]) and (not neg["C10_alfa_unico"]["ok"]), "o controle negativo (a secao v399) devia reprovar C3' e C10"
nomes_rt = AC.nomes_de_nivel_de_modulo(RT)
assert nomes_rt == AC.nomes_de_nivel_de_modulo(RT9) - {"ALPHA_FINE_CODATA_2018"}, "os nomes de nivel de modulo da secao devem ser os da v399, menos ALPHA_FINE_CODATA_2018"
for n in ("declaracao_do_operador_v399", "selo_acom_v399", "resumos_do_selo_v399", "selo_acom_sidecar_v399", "registro_core_v399", "sidecar", "selar", "verificar", "controles_negativos", "conferir_bloco_embutido", "ACOM_PROVENIENCIA", "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256"):
    assert n in nomes_rt, ("nome esperado ausente no runtime montado", n)
tmp = AC.A9.extrair_bloco(RT)
assert tmp == bloco9, "o bloco embutido mudou"
if os.path.exists(OUT) and open(OUT, "rb").read().decode("utf-8") != RT:
    bak = OUT + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1"
    open(bak, "wb").write(open(OUT, "rb").read())
open(OUT + ".tmp", "w", encoding="utf-8", newline="\n").write(RT); assert os.path.getsize(OUT + ".tmp") == len(RT.encode("utf-8")); os.replace(OUT + ".tmp", OUT)
rep = {"contrato": "RUNTIME_MONTAGEM_v400", "runtime": {"path": OUT, "sha256": sha(RT.encode("utf-8")), "bytes": len(RT.encode("utf-8")), "linhas": RT.count("\n")},
       "entrada": {"path": IN, "sha256": sha(rt9_bytes), "bytes": len(rt9_bytes), "embutido_no_um_py_base_uma_vez": True},
       "edicoes_declaradas": edicoes, "conferencias": conf, "bloco_embutido_sha256": sha(bloco9.encode("utf-8")), "nomes_de_nivel_de_modulo_do_runtime": len(nomes_rt),
       "esboco": {"path": ESBOCO, "sha256": ESBOCO_SHA256, "regexes": {k: v.pattern for k, v in regexes.items()}},
       "controle_negativo_da_secao_v399": {k: {"ok": v["ok"], "detalhe": v["detalhe"]} for k, v in neg.items()},
       "estatuto": "[REAL] montado e conferido por script; as edicoes sao todas da ADAPTACAO da gerencia (fora do bloco do operador, cujo hash nao mudou); revisao independente: ver o ESTADO (nao feita por quem constroi)"}
json.dump(rep, open(os.path.join(HERE, "RUNTIME_MONTAGEM_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"runtime_sha16": rep["runtime"]["sha256"][:16], "bytes": rep["runtime"]["bytes"], "linhas": rep["runtime"]["linhas"], "edicoes": len(edicoes), "bloco_sha16": rep["bloco_embutido_sha256"][:16], "conferencias": {k: v["ok"] for k, v in conf.items()}}, ensure_ascii=False, indent=1))
