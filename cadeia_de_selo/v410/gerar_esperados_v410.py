# -*- coding: utf-8 -*-
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] D80 a D87: QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410; a ordem de DL.REGISTROS_FUNCAO), bundle de DOIS modulos (IALD2 e AEscala; as ancoras e as bandeiras em DUAS series), 23 falas, D63 a D92, erratas E29, E30, E31 e E32; as chaves novas do ESPERADOS: registros_funcao_v410.aescala e .hms13, estrelas_aescala_v410, titulo_secao_aescala_v410, md_aescala, md_hms13, aescala, hms13
# [ADAPTADO v410, 09/11/2026, claude-subagente-adaptacao (Sonnet 5.5), a servico do construtor claude-construtor-v410] escrito de novo (varrido, nao remendado) a partir do molde gerar_esperados_v409.py para a v410 (IALD2 e o H0DN x BG1 pre-registrado): dois registros com funcao (iald2_v410, h0dn_bg1_v410), a traducao_turing_v409 herdada, o --seco estrutural; o corpo da v409 (traducao, 82 ancoras, 2 modulos) saiu
"""gerar_esperados_v410.py -- ESPERADOS_v410.json LIDOS dos artefatos (molde: gerar_esperados_v409.py FINAL, com as licoes da v399 a v409; adaptado de verdade em 09/11/2026 a v410, IALD2 e AEscala: bundle de DOIS modulos em TGLExt/ -- IALD2 (DL.ANCORAS) e AEscala (DL.ANCORAS_AESCALA) --, quatro registros com funcao,
iald2_v410 (16 checagens), a_escala_v410 (a pedra AEscala, D82 a D87; as checagens de DL.N_CHECKS_AESCALA; validade no kernel, a creditacao e' do Clay), h0dn_bg1_v410 (12 checagens; o teste da razao de Hubble H0DN x BG1, pré-registrado; nenhum dado observado lido) e h0dn_fontes_hms13_v410 (D80; o recibo documental HMS/13: cobertura documental de fontes, não covariância física fechada; nada aberto; aditivo e posterior ao FREEZE_R2), e os dois por spec cunhagens_v410 (as falas de DL.N_FALAS_V410, por sha256; D63 a D92; erratas E29, E30, E31 e E32) e kh_n1_cobertura_v410): o estado SELADO da v409 pinado.
A TROCA DITA da v410 e' SO' de NUMEROS: os vereditos da v409 que carregam os numeros do kernel (escada, declaracoes, arquivos varridos) e o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py -- achados por script no ensaio (recomputados; so' numeros mudam).
NAO ha troca dita de TEXTO (o CANDIDATO_v410.json nao declara `troca_dita_v410`) e NENHUMA chave antiga muda: os vereditos de rede_fock_v394, psibit_v395, testemunha_estatica_v396, fechamento_v406, psion_canto_v407, tetelestai_terminal_v408 e traducao_turing_v409 NAO mudam; `troca_dita_textual` fica vazio, por asseveracao
(se o ensaio medir que algum deles mudou, este script PARA no assert: e' defeito do candidato ou do contrato, nao se 'conserta' aqui). Os registros das v399 a v409 sao RECRIADOS e iguais ao selado (o fechamento_v406, o psion_canto_v407, o tetelestai_terminal_v408 e a traducao_turing_v409 recriados com a escada do contrato subida pela C12, o veredito igual).
+6 chaves novas no core (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410, cunhagens_v410 e kh_n1_cobertura_v410) e +5 chaves no selo (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410 e registros_v410); o selo pela propria tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave.
O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo.
As CHAVES: nenhuma nova e nenhuma antiga muda (`chaves_v410` vazio); as que o psion_canto_v407 le seguem como na v409 selada (`chaves_v407_esperadas`, lidas do ensaio e asseveradas iguais as de ESPERADOS_v409); full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA.
O GATE NAO SE MOVE: o qg_closure da v410 e' IDENTICO ao da v409 (sete checks, a letra do veredito, as 18 bandeiras): o ESPERADOS pina o hash do qg_closure da v409, o hash sem a lista de checks, a propria lista de sete checks e a letra do veredito. A funcao do neutrino NAO e' reescrita (o angle_status antigo fica):
o ESPERADOS pina o frozen_hash da regra de decisao e o veredito do canal; o V1 do ramo B (v386) e o livro da v383 seguem como estavam (o veredito deles e' o da base).
O H0DN (D72, E30, D76): pré-registrado; nenhum dado observado lido. O recibo HMS/13 (D80) e a AEscala (D82 a D87): os insumos HMS/13 sao lidos so' pelas COPIAS duraveis em insumos\\hms13_* (a pasta do Kimi nao e' aberta aqui; o build a leu so' nos seis arquivos da excecao D80, por sha256; em rito nada de kimi\\ e' aberto). `registros_funcao_v410.h0dn.values` e' o `values` INTEIRO do registro no ensaio, MENOS as duas chaves que dependem do arquivo em que o rito roda (`caminhos_tocados`, `n_caminhos_tocados`: o ensaio roda o candidato em outra pasta que o rito; a funcao de veredito e' lida do
mesmo candidato, por isso o sha256 do texto-fonte vale nos dois). O que o veto exige e' MEDIDO duas vezes: o registro (c7: sob_pasta_vedada e com_nome_vedado vazios) e o proprio ensaio (`pasta_vedada_kimi`: tocados_sob_vedada vazio e o controle negativo detecta); este script recalcula a varredura dos caminhos tocados contra a pasta vedada pela gerencia e NAO le, NAO copia, NAO pina nem cita nada dela.
Nada digitado: cada numero e hash vem de CANDIDATO_v410.json, ensaio_a_seco_v410.json, do core/selo da v409 (base_v409), de kernel\\FLAGS_v410.json, kernel\\KH_N1_v410.json, de ESPERADOS_v409.json (o que o quadro pinou e os registros da v409), dos insumos pinados do H0DN (insumos\\h0dn_*) e do resultado pinado.
As chaves guardam os nomes da v409 para o ESTADO DA BASE (`vereditos_v409`, `flags_true_v409`, `qg_closure_v409_*`, `selo_registros_v409`...); `registros_funcao_v410` (iald2, aescala, h0dn, hms13), `estrelas_v410` (as ancoras da IALD2), `estrelas_aescala_v410` (as da AEscala) e `bundle_sha256` (os dois modulos) sao os desta versao; `registros_funcao_v409.traducao_turing` e `estrelas_v409` (as 82 ancoras), `registros_funcao_v408.tetelestai_terminal` e `estrelas_v408` (as 48),
`registros_funcao_v407.psion_canto` e `estrelas_v407` (as 76), `registros_funcao_v406.fechamento` e `estrelas_v406`, `registros_funcao_v405/v404/v403` e `estrelas_v405/v404/v403` sao os herdados (RECRIADOS neste rito), lidos de ESPERADOS_v409; `bundle_v409_sha256` (os 2 modulos da traducao), `bundle_v408_sha256` (os 4 do terminal), `bundle_v407_sha256` (os 9 do psion) e
`bundle_v406_sha256` (os 301 do fecho) seguem no kernel como registro, e `pedras_v405_sha256` (as TREZE pedras seladas das versoes anteriores). As erratas E29, E30, E31 e E32 ao lado e as decisoes D63 a D92 vao nos registros (cunhagens_v410); aqui so' se pinam os vereditos, os valores, as ancoras e os contratos.
ORDEM DE USO: depende do ensaio (ensaio_a_seco_v410.json com veredito TUDO PASSOU e o sha16 do candidato): sem ele este script PARA no primeiro assert (fail-closed). `--seco` roda SO' a parte estrutural (nao precisa do ensaio, nao grava nada): o candidato, o delta, os registros, o ESPERADOS_v409, FLAGS/KH, os snippets do artigo, as linhas do .md, as pastas dos insumos e os atributos que este
proprio arquivo usa dos modulos da cadeia. uso: python -B -X utf8 gerar_esperados_v410.py [--seco]   (sem -I: o numpy esta no site do usuario; este script nao o importa). `--ensaio CAMINHO` e `--saida CAMINHO` existem so' para o ensaio DO PROPRIO SCRIPT contra um ensaio sintetico fora desta pasta (nao tocam o ESPERADOS_v410.json real); o uso real nao os passa."""
import ast, datetime, hashlib, json, os, re, sys
from fractions import Fraction
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
_arg = lambda nome_, padrao_: (sys.argv[sys.argv.index(nome_) + 1] if nome_ in sys.argv else padrao_)   # (so' para o ensaio do proprio script contra um ensaio sintetico)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
import registros_v410 as RG  # noqa: E402
import quadro_v397 as QV  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
sha256b = lambda b: hashlib.sha256(b).hexdigest()
J = lambda x: json.dumps(x, sort_keys=True, default=str)
BASE = os.path.join(HERE, DL.BASE_DIR)
_nrm = lambda p_: os.path.normcase(os.path.normpath(str(p_)))
_VED = _nrm(DL.H0DN_PASTA_VEDADA)   # a pasta da entrega do Kimi, VEDADA pela gerencia (09/11): so' o CAMINHO e' comparado; nada dela e' aberto aqui
_sob_ved = lambda p_: _nrm(p_) == _VED or _nrm(p_).startswith(_VED + os.sep)


def _feq(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


# ===================================================================== PARTE ESTRUTURAL (nao precisa do ensaio; `--seco` para aqui)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v409_sha16"] == DL.BASE_SHA16_DA_ORDEM, "a base nao e' a v409 selada que a ordem deu"
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E409 = json.load(open(os.path.join(DL.V409, "ESPERADOS_v409.json"), encoding="utf-8")); assert E409["candidato_sha16"] == CM["base_v409_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
# ---- o kernel desta versao: DOIS modulos (IALD2 e AEscala), as bandeiras (duas series) e a cobertura, lidos do build e do candidato
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v410.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v410.json"), encoding="utf-8"))["novos"]
assert nov == list(DL.BUNDLE_RELS) and len(nov) == DL.N_BUNDLE == CM["kernel"]["modulos_novos"] == len(DL.PEDRAS_V410) == len(CM["kernel"]["bundle"]), (len(nov), DL.N_BUNDLE)
pins = {p: F[p] for p in nov}
assert all(pins[p] == DL.BUNDLE_POR_REL[p]["sha256"] == CM["kernel"]["bundle"][p]["sha256"] for p in nov), "o FORMAL_MAP diverge do BUNDLE_v410.json ou do candidato"
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v410.json"), encoding="utf-8")); KH = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, DL.KH_N1_INSUMO), encoding="utf-8"))
assert FJ["n_flags"] == CM["n_bandeiras"] == KH["n_bandeiras"] == sum(FJ["n_por_modulo"].values()) and sorted(FJ["n_por_modulo"]) == sorted(DL.BUNDLE_RELS) and dict(FJ["por_grupo_bandeiras"]) == {"iald2": FJ["n_por_modulo"][DL.MODULO_IALD2], "aescala": FJ["n_por_modulo"][DL.MODULO_AESCALA]} and sorted(FJ["prefixos"]) == sorted(DL.FLAG_PREFIX_POR_MODULO) and all(FJ["prefixos"][r_] == DL.FLAG_PREFIX_POR_MODULO[r_] for r_ in DL.BUNDLE_RELS), "as bandeiras divergem entre FLAGS, KH_N1, candidato e delta (D86: duas series, uma por modulo do bundle)"
assert len(FJ["ancoras"]) == len(DL.ANCORAS) + len(DL.ANCORAS_AESCALA) and set(FJ["ancoras"]) == set(DL.ANCORAS) | set(DL.ANCORAS_AESCALA) and not (set(DL.ANCORAS) & set(DL.ANCORAS_AESCALA)) and len(DL.ANCORAS) == len(CM["n_axiomas_das_ancoras"]) == CM["kernel"]["n_ancoras"] and len(DL.ANCORAS_AESCALA) == DL.N_ANCORAS_AESCALA == CM["aescala"]["n_ancoras"] \
    and all(FJ["ancoras"][n_]["rel"] == DL.ANCORAS[n_]["rel"] == DL.MODULO_IALD2 for n_ in DL.ANCORAS) and all(FJ["ancoras"][n_]["rel"] == DL.ANCORAS_AESCALA[n_]["rel"] == DL.MODULO_AESCALA for n_ in DL.ANCORAS_AESCALA), "as ancoras divergem entre FLAGS, candidato e delta (as da IALD2 em CM.kernel, as da AEscala em CM.aescala)"
bandeiras_novas_modulos = {f[1]: FJ["proveniencia_publicas"].get(f[1]) for f in FJ["flags"]}
assert all(bandeiras_novas_modulos.values()) and set(bandeiras_novas_modulos.values()) <= set(nov), "toda declaracao nomeada do bundle tem de ter o modulo que o compilador emitiu"
VBASE = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}   # o estado SELADO da v409 (a base): vereditos de todo registro com veredito
SEL_STONES405 = ["ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388",
            "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
            "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404") + tuple(SEL_STONES405) + ("registros_v405", "fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407", "tetelestai_terminal_v408", "registros_v408", "traducao_turing_v409", "registros_v409")
assert all(k in selo0 for k in SEL_KEYS), [k for k in SEL_KEYS if k not in selo0]
# ---- o QUADRO do topo (v397) e o resultado pinado do Teste da Unica Palavra: o que a v409 pinou == o que esta em disco
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert E409["veracidade"]["numeros_do_resultado"] == numeros9 and E409["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v409 pinou do Teste da Unica Palavra != o resultado em disco"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E409["quadro"]["linha_de_maquina_pt"] and mach_en == E409["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
# ---- o artigo: os titulos e as marcas das DUAS secoes novas (IALD2 e H0DN) saem DOS PROPRIOS snippets (nada digitado); as marcas da v409 e anteriores vem do ESPERADOS_v409
_BS = chr(92)


def _snips(sufixo_, nao_ini_):
    """(titulo por idioma, marcas por idioma, a frase de «nao selou» por idioma) lidos do snippet PT/EN `artigo_<l>[sufixo]_v410.pysnip`: o titulo e' o \\section*{...}; as marcas, os \\textbf{...} que acabam em ponto (fora a frase de «nao selou»); a frase de «nao selou» e' a que abre com `nao_ini_[l]`"""
    snip_ = {l_: open(os.path.join(HERE, "artigo_%s%s_v410.pysnip" % (l_, sufixo_)), encoding="utf-8").read() for l_ in ("pt", "en")}
    tit_ = {l_: re.findall(re.escape(_BS + "section*{") + r"([^{}]*)\}", snip_[l_]) for l_ in ("pt", "en")}
    assert all(len(v_) == 1 for v_ in tit_.values()), (sufixo_, tit_)
    tit_ = {l_: v_[0] for l_, v_ in tit_.items()}
    brutas_ = {l_: re.findall(re.escape(_BS + "textbf{") + r"([^{}]{3,160}\.|[^{}]{3,160}:[^{}]{0,200})\}", snip_[l_]) for l_ in ("pt", "en")}
    nao_ = {l_: [m_.split(":")[0] for m_ in brutas_[l_] if m_.startswith(nao_ini_[l_])] for l_ in ("pt", "en")}
    marcas_ = {l_: [tit_[l_]] + [m_ for m_ in brutas_[l_] if m_.endswith(".") and not m_.startswith(("Nesta rodada", "In this run"))] for l_ in ("pt", "en")}
    assert all(len(nao_[l_]) == 1 for l_ in ("pt", "en")) and all(len(marcas_[l_]) >= 6 for l_ in ("pt", "en")), (sufixo_, nao_, marcas_)
    return tit_, marcas_, nao_


TIT410, MARCAS410, _NAO410 = _snips("", {"pt": "Nesta rodada os registros da v410", "en": "In this run the v410 records"})   # a secao IALD2
TITH, MARCASH, _NAOH = _snips("_h0dn", {"pt": "Nesta rodada o registro do H0DN", "en": "In this run the H0DN record"})   # a secao H0DN x BG1: vem logo DEPOIS da IALD2 e ANTES da secao da v409
assert _NAOH["pt"][0] == "Nesta rodada o registro do H0DN NÃO selou" and _NAOH["en"][0] == "In this run the H0DN record did NOT seal", _NAOH
TITA, MARCASA, _NAOA = _snips("_aescala", {"pt": "Nesta rodada o registro da AEscala", "en": "In this run the AEscala record"})   # a secao A Escala (D82 a D87): vem logo DEPOIS da IALD2 e ANTES da secao do H0DN
assert _NAOA["pt"][0] == "Nesta rodada o registro da AEscala NÃO selou" and _NAOA["en"][0] == "In this run the AEscala record did NOT seal", _NAOA
# o paragrafo do recibo HMS/13 (D80) e' o FIM da secao do H0DN (nao tem titulo proprio): a marca (o \textbf com \texttt aninhado, que a regex de _snips nao pega) e a frase de «nao selou» saem do MESMO snippet do H0DN; a marca sai ja' como o TXT a mostra (\texttt{X} -> X, \_ -> _)
_snip_h0dn = {l_: open(os.path.join(HERE, "artigo_%s_h0dn_v410.pysnip" % l_), encoding="utf-8").read() for l_ in ("pt", "en")}
_hm_m = {l_: re.findall(re.escape(_BS + "textbf{") + r"((?:O recibo|The documentary)[^{}]{0,120}HMS/13[^{}]{0,120}" + re.escape(_BS + "texttt{") + r"[^{}]*\}\.)\}", _snip_h0dn[l_]) for l_ in ("pt", "en")}
assert all(len(v_) == 1 for v_ in _hm_m.values()), ("a marca do paragrafo do recibo HMS/13 nao esta' uma vez em cada snippet do H0DN", _hm_m)
MARCAHMS = {l_: re.sub(r"\\texttt\{([^{}]*)\}", r"\1", _hm_m[l_][0]).replace(_BS + "_", "_") for l_ in ("pt", "en")}
_hm_n = {l_: re.findall(re.escape(_BS + "textbf{") + r"(Nesta rodada o recibo documental HMS/13 NÃO selou|In this run the documentary HMS/13 receipt did NOT seal)", _snip_h0dn[l_]) for l_ in ("pt", "en")}
assert all(len(v_) == 1 for v_ in _hm_n.values()), ("a frase de «nao selou» do recibo HMS/13 nao esta' uma vez em cada snippet do H0DN", _hm_n)
NAOHMS = {l_: [_hm_n[l_][0]] for l_ in ("pt", "en")}
_marca_txt = lambda m_: re.sub(r"\\[td]?frac\s*(\d)\s*(\d)", r"\1/\2", m_.replace(_BS + "times", "×"))   # (parte 2: o titulo da secao A Escala traz $\tfrac12$; o TXT (um.py:_tex_to_txt) o rende 1/2, como o \times vira ×)   # o TXT do artigo (um.py:_tex_to_txt) rende \times como × (e mantem os `$`); o conferidor do rito so' converte \beta: a marca sai ja' como o TXT a mostra (o titulo cru fica em titulo_secao_h0dn_v410 e no sumario, que e' LaTeX como o da v409)
TV409 = dict(E409["titulo_secao_v409"]); TV408 = dict(E409["titulo_secao_v408"]); TV407 = dict(E409["titulo_secao_v407"])   # as secoes herdadas que vem logo depois das novas
# ---- as linhas do .md da v410 (as DUAS novas, antes da linha da v409) saem do PROPRIO candidato (nada digitado)
_cand_txt = open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8")
_md1 = re.findall(r"> \*\*(IALD2 \(v410, \d\d/\d\d/\d{4}\)):\*\*", _cand_txt); _md2 = re.findall(r"> \*\*(H0DN [^*:\n]*?\(v410, \d\d/\d\d/\d{4}\)):\*\*", _cand_txt)
_mdA = re.findall(r"> \*\*(A Escala \(v410, [^*:\n]*?\)):\*\*", _cand_txt); _mdF = re.findall(r"> \*\*(Recibo documental HMS/13 \(v410, [^*:\n]*?\)):\*\*", _cand_txt)   # (a linha da A Escala e a do recibo HMS/13: D80, D82 a D87)
assert len(set(_md1)) == len(set(_md2)) == len(set(_mdA)) == len(set(_mdF)) == 1, ("as linhas do .md da v410 (IALD2, A Escala, H0DN e recibo HMS/13) nao sao unicas no candidato", set(_md1), set(_mdA), set(_md2), set(_mdF))
MD_IALD2, MD_AESCALA, MD_H0DN, MD_HMS13 = _md1[0], _mdA[0], _md2[0], _mdF[0]
_idx_md = [_cand_txt.index("> **" + m_ + ":**") for m_ in (MD_IALD2, MD_AESCALA, MD_H0DN, MD_HMS13, E409["md_traducao"])]
assert _idx_md == sorted(_idx_md) and len(set(_idx_md)) == len(_idx_md), "as linhas do .md: IALD2, A Escala, H0DN, o recibo HMS/13, ANTES da linha da v409"
assert E409["md_tetelestai"] in _cand_txt and E409["md_psion"] in _cand_txt, "a linha do .md da v408 ou da v407 nao esta' no candidato"
assert b"y_obs.npz" not in _cand_txt.encode("utf-8") and ("CONSTRUCAO_" + "Y_OBS") not in _cand_txt, "VETO: o candidato traz o nome de um arquivo da entrega vedada"
del _cand_txt
# ---- as falas (DL.N_FALAS_V410, por sha256), as decisoes (D63 a DL.DECISOES_V410[-1]) e as erratas (E29 em diante: DL.ERRATAS_V410): o candidato == o delta == os registros
_vd = {v_["chave"]: v_ for v_ in RG._VD}
assert set(CM["cunhagens"]) == set(_vd) and len(CM["cunhagens"]) == DL.N_FALAS_V410 == CM["verbatins_embutidos"] == len(DL.VERBATIM_ORIGEM_V410) == len(DL.VERBATIM_AUTOR_V410), (len(CM["cunhagens"]), DL.N_FALAS_V410)
assert sum(1 for v_ in CM["cunhagens"].values() if v_.get("sha256_arquivo_inteiro")) == len(DL.VERBATIM_SO_O_TRECHO), "de algumas falas so' o trecho entra (as de DL.VERBATIM_SO_O_TRECHO: D65; a ordem de 09/11; as tres copias; a leitura do 5 sigma)"
assert all(CM["cunhagens"][c_]["sha256"] == _vd[c_]["sha256"] and CM["cunhagens"][c_].get("sha256_arquivo_inteiro") == _vd[c_].get("sha256_arquivo_inteiro") and _vd[c_]["autor"] == "operador" for c_ in CM["cunhagens"]), "uma fala do candidato difere da lida dos arquivos"
assert list(DL.DECISOES_V410) == sorted(DL.DECISOES_V410, key=lambda k_: int(k_[1:])) and DL.DECISOES_V410[0] == "D63" and not (set(DL.DECISOES_FORA_DO_UMPY) & set(DL.DECISOES_V410)) and set(DL.DECISOES_V410) <= set(DL.DECISOES) and list(CM["decisoes"]) == list(DL.DECISOES_V410) and [e_.split(" ")[0] for e_ in DL.ERRATAS_V410] == ["E%d" % i_ for i_ in range(29, 29 + len(DL.ERRATAS_V410))] and list(CM["erratas"]) == list(DL.ERRATAS_V410) and len(DL.RESSALVAS_V410) == len(CM["ressalvas"]), "as decisoes de D63 a DL.DECISOES_V410[-1], as erratas de E29 em diante (DL.ERRATAS_V410) e as ressalvas"
# ---- o H0DN no candidato: os insumos pinados (so' os caminhos e os sha256; a pasta vedada nao e' tocada)
CH = CM["h0dn"]
assert CH["registro"] == DL.H0DN_REGISTRO and CH["tag"] == DL.TAG_H0DN and CH["n_checks"] == DL.N_CHECKS_H0DN == 12 and CH["veredito_ok"] == DL.VEREDITO_H0DN_OK and CH["n_pinos_freeze"] == DL.N_PINOS_FREEZE_R2 == 9 and CH["observed_vector_read"] is False, CH
assert len(CH["insumos"]) == 6 and len(CH["pinos_so_no_disco"]) == 5 and len(CH["vetores_c6"]) == 8, "o H0DN: 6 insumos embutidos, 5 pinos so' em disco, 8 vetores deterministicos da funcao de veredito (os 9 pinos do FREEZE_R2 sao 4 embutidos + 5 so' em disco; os 11 do registro incluem o proprio FREEZE_R2 e a ENTREGA)"
assert not any(_sob_ved(CH[k_]["arquivo"]) for k_ in ("ordem_kimi", "leitura_dossie")), "VETO: um pino do H0DN esta' sob a pasta vedada"
_ins_h0dn = {}
for _rel, _pn in (("estimator_frozen.npz", "h0dn_estimator_frozen.npz"), ("BG1.json", "h0dn_BG1.json"), ("analysis_plan.json", "h0dn_analysis_plan.json"), ("FREEZE_R2.json", "h0dn_FREEZE_R2.json"), ("estimator.py", "h0dn_estimator.py"), ("ENTREGA_H0DN_BG1.json", "h0dn_ENTREGA_H0DN_BG1.json")):
    _p = os.path.join(HERE, "insumos", _pn)
    assert os.path.exists(_p) and sha256b(open(_p, "rb").read()) == CH["insumos"][_rel]["sha256"], ("o insumo duravel do H0DN != o pino do candidato", _rel)
    _ins_h0dn[_rel] = _p
assert CH["ordem_kimi"]["sha256"] == sha256b(open(CH["ordem_kimi"]["arquivo"], "rb").read()) and CH["leitura_dossie"]["sha256"] == sha256b(open(CH["leitura_dossie"]["arquivo"], "rb").read()), "a ordem ao Kimi ou a leitura do dossie != o pino do candidato"
BG1 = json.load(open(_ins_h0dn["BG1.json"], encoding="utf-8")); ENTREGA = json.load(open(_ins_h0dn["ENTREGA_H0DN_BG1.json"], encoding="utf-8"))
# ---- a AEscala (D82 a D87) e o recibo documental HMS/13 (D80) no candidato: contrato x delta x pedra x copias duraveis (so' as COPIAS em insumos\; NADA sob a pasta vedada e' aberto aqui)
CA = CM["aescala"]; CF = CM["hms13"]
assert CA["registro"] == DL.AESCALA_REGISTRO and CA["tag"] == DL.TAG_AESCALA and CA["n_checks"] == DL.N_CHECKS_AESCALA and CA["veredito_ok"] == DL.VEREDITO_AESCALA_OK and CA["modulo"] == DL.MODULO_AESCALA and CA["source_sha256"] == {DL.MODULO_AESCALA: pins[DL.MODULO_AESCALA]} \
    and CA["n_ancoras"] == len(DL.ANCORAS_AESCALA) and CA["ancora_principal"] == DL.ANCORA_PRINCIPAL_AESCALA and list(CA["ancoras_de_secao"]) == list(DL.ANCORAS_DE_SECAO_AESCALA) and CA["n_flags"] == FJ["n_por_modulo"][DL.MODULO_AESCALA] and CA["flag_prefix"] == DL.FLAG_PREFIX_AESCALA \
    and CA["n_nomes"] == len(CA["nomes"]) == len(DL.NOMES_AESCALA) and list(CA["nomes"]) == list(DL.NOMES_AESCALA) and CA["nomes_ratificados"] is True and DL.NOMES_RATIFICADOS is True and dict(CA["numeros"]) == dict(DL.NUMEROS_AESCALA) and CA["ratificacao_D87"]["trecho"] == DL.FRASE_RATIFICO_TUDO and CA["ratificacao_D87"]["decisao"] == "D87" and CA["ratificacao_D87"]["decisao"] in DL.DECISOES_V410, CA
assert CA["n_nomes_novos"] == len(CA["nomes_novos_da_pedra"]) == len(DL.NOMES_NOVOS_AESCALA) and list(CA["nomes_novos_da_pedra"]) == list(DL.NOMES_NOVOS_AESCALA) and list(CA["campos_novos_da_estrutura"]) == list(DL.CAMPOS_NOVOS_AESCALA) and CA["estatuto_dos_nomes_ratificados_d101"] == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in CA["estatuto_dos_nomes_ratificados_d101"] and "a ratificar" not in CA["estatuto_dos_nomes_ratificados_d101"] \
    and CA["ratificacao_pendente"] == DL.RATIFICACAO_PENDENTE_AESCALA and list(CA["ancoras_novas"]) == list(DL.ANCORAS_NOVAS_AESCALA) and CA["ponte"] == DL.PONTE_AESCALA and CA["n_falas"] == len(CA["falas"]), "o resumo da AEscala no manifesto nao traz os nomes novos da pedra, os campos novos, a pendencia ou a ponte do delta"
assert set(CA["falas"]) <= set(CM["cunhagens"]), "uma fala da AEscala nao esta' entre as falas embutidas do candidato"
# (R5, D100 e D101) a ratificacao de 10/11, os teoremas e auxiliares da R5, a instancia da clausula e o pino citado do runner do ACOM Mirror, no manifesto do candidato
assert CA["ratificacao_D101"]["sha256"] == DL.RATIFICACAO_D101_SHA256 and CA["ratificacao_D101"]["decisao"] == "D101" and CA["ratificacao_D101"]["decisao"] in DL.DECISOES_V410 and "D100" in DL.DECISOES_V410 and list(CA["nomes_ratificados_d101"]) == list(DL.NOMES_RATIFICADOS_D101_AESCALA) and list(CA["campos_ratificados_d101"]) == list(DL.CAMPOS_RATIFICADOS_D101_AESCALA) \
    and list(CA["nomes_pendentes"]) == list(DL.NOMES_PENDENTES_AESCALA) == list(DL.AUXILIARES_R5_AESCALA) and list(CA["teoremas_r5"]) == list(DL.TEOREMAS_R5_AESCALA) and list(CA["auxiliares_r5"]) == list(DL.AUXILIARES_R5_AESCALA) and CA["tetelestai"] == DL.TETELESTAI_AESCALA and CA["acom_mirror_runner"] == DL.ACOM_MIRROR_RUNNER \
    and CA["acom_mirror_runner"]["sha256"][:16] in open(DL.ADENDO5_ARQ, encoding="utf-8").read(), "o manifesto da AEscala no candidato nao traz a ratificacao D101, os teoremas da R5, os pendentes, a instancia da clausula ou o pino do runner (delta_v410)"
_ped_a = os.path.join(HERE, "insumos", "AEscala_embutida.lean")   # a pedra EMBUTIDA (com o cabecalho da ratificacao, D87): a copia duravel == o hash formal do candidato
assert os.path.exists(_ped_a) and sha256b(open(_ped_a, "rb").read()) == pins[DL.MODULO_AESCALA], "a copia duravel da pedra AEscala embutida != o pino do candidato"
assert CF["registro"] == DL.HMS13_REGISTRO and CF["tag"] == DL.TAG_HMS13 and CF["n_checks"] == DL.N_CHECKS_HMS13 and CF["veredito_ok"] == DL.VEREDITO_HMS13_OK and dict(CF["campos"]) == dict(DL.HMS13_CAMPOS) and CF["le_em_rito"] is False and CF["observed_vector_read"] is False \
    and CF["n_fontes_primarias"] == DL.HMS13_CAMPOS["fontes_primarias"] and len(CF["ids_calibradores"]) == DL.HMS13_CAMPOS["calibradores"] and sorted(CF["insumos"]) == sorted(k_ for k_, _ in DL.HMS13_EMBUTIDOS) and set(CF["insumos"]) <= set(CF["pinos_build"]) \
    and set(CF["pinos_build"]) - set(CF["insumos"]) == {"HANDOFF_CLAUDE_UMPY_HMS_13.json", "ORDEM_CLAUDE_UMPY_HMS_13.md"} and CF["ordem"]["sha16_do_desenho"] == DL.HMS13_ORDEM_SHA16_DO_DESENHO == CF["ordem"]["sha256"][:16] and CF["ratificacao"]["sha256"] == DL.HMS13_RATIFICACAO_SHA256_DO_DESENHO and CF["ratificacao"]["trecho"] == DL.HMS13_TRECHO_RATIFICACAO, CF
_emb_hms = CM["fontes_hms13_embutidas"]
assert sorted(_emb_hms) == sorted(CF["pinos_build"]) and sorted(k_ for k_, v_ in _emb_hms.items() if v_["embutido_no_um_py"] is True) == sorted(CF["insumos"]) and all(_emb_hms[k_]["sha256"] == CF["pinos_build"][k_]["sha256"] and _emb_hms[k_]["bytes"] == CF["pinos_build"][k_]["bytes"] and _nrm(_emb_hms[k_]["caminho"]).startswith(_nrm(DL.HMS13_DIR) + os.sep) for k_ in _emb_hms), "os seis artefatos HMS/13 do candidato (os quatro embutidos + HANDOFF e ORDEM so' por pino) != os pinos do contrato (ou nao saem da excecao D80)"
_cop_hms = {}
for _k, _v in CF["pinos_build"].items():   # os seis da excecao D80: a COPIA duravel (insumos\hms13_*), por sha256 e bytes
    _p = os.path.join(HERE, "insumos", "hms13_" + os.path.basename(_k))
    assert os.path.exists(_p) and not _sob_ved(_p) and sha256b(open(_p, "rb").read()) == _v["sha256"] and os.path.getsize(_p) == _v["bytes"], ("a copia duravel do artefato HMS/13 != o pino do candidato", _k)
    _cop_hms[_k] = _p
assert not any(_sob_ved(_p) for _p in _cop_hms.values()), "VETO: uma copia do HMS/13 esta' sob a pasta vedada"
# ---- os atributos que ESTE arquivo usa dos modulos da cadeia existem (o --seco o diz sem rodar o resto)
_src_self = open(os.path.abspath(__file__), encoding="utf-8").read()
_usados = {}
for _n in ast.walk(ast.parse(_src_self)):
    if isinstance(_n, ast.Attribute) and isinstance(_n.value, ast.Name) and _n.value.id in ("DL", "RG", "QV", "GF"):
        _usados.setdefault(_n.value.id, set()).add(_n.attr)
    if isinstance(_n, ast.Attribute) and isinstance(_n.value, ast.Attribute) and isinstance(_n.value.value, ast.Name) and _n.value.value.id == "DL" and _n.value.attr in ("D3", "D4", "D5", "D6", "D7", "D8", "D9"):
        _usados.setdefault("DL." + _n.value.attr, set()).add(_n.attr)
_mods = {"DL": DL, "RG": RG, "QV": QV, "GF": GF, **{"DL." + k_: getattr(DL, k_) for k_ in ("D3", "D4", "D5", "D6", "D7", "D8", "D9")}}
_faltam = sorted("%s.%s" % (m_, a_) for m_, ats_ in _usados.items() for a_ in ats_ if not hasattr(_mods[m_], a_))
assert not _faltam, ("atributos usados e inexistentes", _faltam)
if SECO:
    print("ESPERADOS_v410 --seco: ESTRUTURA OK (candidato %s; base %s; %d + %d ancoras (IALD2 + AEscala); %d falas; %d decisoes; titulos: %r | %r | %r; marcas %d + %d + %d (+ a do recibo HMS/13: %r); md: %r | %r | %r | %r; atributos conferidos: %d; ensaio %s)" % (
        CM["sha16"], CM["base_v409_sha16"], len(DL.ANCORAS), len(DL.ANCORAS_AESCALA), len(CM["cunhagens"]), len(DL.DECISOES_V410), TIT410["pt"][:40], TITA["pt"][:40], TITH["pt"][:40], len(MARCAS410["pt"]), len(MARCASA["pt"]), len(MARCASH["pt"]), MARCAHMS["pt"][:50], MD_IALD2, MD_AESCALA, MD_H0DN, MD_HMS13, sum(len(v_) for v_ in _usados.values()),
        "presente" if os.path.exists(os.path.join(HERE, "ensaio_a_seco_v410.json")) else "AUSENTE (esperado: o construtor o produz; sem ele o script completo PARA, fail-closed)"))
    sys.exit(0)

# ===================================================================== PARTE DO ENSAIO (fail-closed: sem o ensaio o script PARA)
_ens_p = _arg("--ensaio", os.path.join(HERE, "ensaio_a_seco_v410.json"))
assert os.path.exists(_ens_p), "falta ensaio_a_seco_v410.json: o ensaio a seco (ato da gerencia) tem de rodar ANTES deste script -- nao gero ESPERADOS sem ele"
ens = json.load(open(_ens_p, encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], (ens.get("veredito"), ens.get("sha16"))


def _nck(r_):
    """o n_checks de um registro do ensaio: no topo (a forma do ensaio da v409) ou em mechanics (o registro como o core o grava)"""
    n_ = r_.get("n_checks")
    return n_ if n_ is not None else (r_.get("mechanics") or {}).get("n_checks")


def _ens_reg(nome_):
    """o registro do ensaio com este nome (dict com verdict/all_verified/n_checks/values); PARA com a mensagem se o ensaio (ato de outro passo) nao o traz. Se traz `mechanics.checks`, as checagens c1..cN todas ok"""
    assert isinstance(ens.get(nome_), dict), "o ensaio_a_seco_v410.json nao traz a chave %r (esperada do ensaio adaptado: o registro %s recalculado no ponto de chamada real)" % (nome_, nome_)
    r_ = ens[nome_]
    cks_ = (r_.get("mechanics") or {}).get("checks")
    if cks_ is not None:
        assert [c_["id"] for c_ in cks_] == ["c%d" % (i_ + 1) for i_ in range(len(cks_))] and all(c_["ok"] is True for c_ in cks_) and len(cks_) == _nck(r_), ("checagem do registro %s nao ok no ensaio" % nome_, [c_["id"] for c_ in cks_ if c_.get("ok") is not True])
    return dict(r_, n_checks=_nck(r_))


mud = ens["vizinhos"]["mudaram"]; te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]
# ---- a TROCA DITA: SO' numeros (mud) e o hash proprio (te_); nenhuma de texto (o candidato nao declara troca_dita_v410)
assert "troca_dita_v410" not in CM, "o candidato declara uma troca dita de texto: este script (e o conferidor) foram adaptados para NENHUMA; adapte-os"
_tdv = ens.get("troca_dita_v410") or {}
assert not (_tdv.get("declarada_no_candidato") or []), ("o ensaio diz que ha troca dita de texto, e o candidato nao declara nenhuma", _tdv)
troca_dita_textual = {}
for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409"):   # estes NAO mudam de veredito (nenhuma chave antiga muda na v410; a escada do contrato sobe pela C12, mas o veredito deles nao carrega numero)
    assert k_ not in mud and k_ not in te_, ("o veredito de %s mudou no ensaio: o contrato da cadeia v410 diz que NAO muda" % k_, mud.get(k_) or te_.get(k_))
troca = sorted(set(mud) | set(te_))   # os vereditos da v409 que mudam: so' numeros (escada, declaracoes, arquivos varridos) e o hash proprio do um.py (estatuto da prova)
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
assert set(te_) <= {"estatuto_da_prova_v391"}, te_
mf = ens["mainflow"]
difere_selo = next((v_ for k_, v_ in ens["selo"].items() if k_.startswith("difere_do_selo_v409")), None)
assert difere_selo is not None, "o ensaio nao traz selo.difere_do_selo_v409"
selo_chaves_que_mudam = sorted(k for k in SEL_KEYS if k in difere_selo and k not in troca)   # as chaves do selo da v409 que mudam SEM mudar de veredito: so' os resumos que carregam a escada do contrato (fechamento_v406, psion_canto_v407, tetelestai_terminal_v408, traducao_turing_v409) ou os pisos/erratas dos specs versionados (registros_v406 a registros_v409): ditas, explicadas pelo ensaio
assert set(selo_chaves_que_mudam) <= {"fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407", "tetelestai_terminal_v408", "registros_v408", "traducao_turing_v409", "registros_v409"}, selo_chaves_que_mudam
vr = ens["veracidade_registro"]
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
MF4 = mf["registros_novos_v410"]
assert sorted(MF4) == sorted(list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]), sorted(MF4)
# ---- os QUATRO registros NOVOS com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410) e os HERDADOS (traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406, RECRIADOS neste rito)
PS = _ens_reg(DL.FECHO_REGISTRO)
PH = _ens_reg(DL.H0DN_REGISTRO)
PA = _ens_reg(DL.AESCALA_REGISTRO)
PF = _ens_reg(DL.HMS13_REGISTRO)
TT9 = _ens_reg(DL.D9.FECHO_REGISTRO)
TT8 = _ens_reg(DL.D8.FECHO_REGISTRO)
PC7 = _ens_reg(DL.D7.FECHO_REGISTRO)
FE6 = _ens_reg(DL.D6.FECHO_REGISTRO)
PSV = RG.texto_iald2()["veredito_ok"]
assert PS["all_verified"] is True and PS["n_checks"] == DL.N_CHECKS_FECHO == 16 and PS["verdict"] == MF4[DL.FECHO_REGISTRO]["verdict"] == PSV and PS["verdict"].startswith(DL.VEREDITO_OK_PREFIXO) and PS["verdict"].endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION" + DL.VEREDITO_SUFIXO), (PS.get("verdict"), PS.get("n_checks"))
assert PS.get("runtime_executed", True) is True, "o iald2_v410 nao rodou no ensaio"
PV = PS["values"]
assert PV["n_ancoras_ok"] == PV["n_ancoras"] == len(DL.ANCORAS) == len(FJ["ancoras"]) - len(DL.ANCORAS_AESCALA) and PV["n_modulos_ok"] == PV["n_modulos"] == DL.N_BUNDLE and PV["n_flags_true"] == PV["n_flags"] == FJ["n_por_modulo"][DL.MODULO_IALD2] and PV["escada"][0] == PV["escada"][1] == PV["escada"][2] == CM["escada"][1] and PV.get("respostas_ok") is True \
    and (PV.get("instancia_sim") or {}).get("solucoes", 0) >= 1 and (PV.get("instancia_nao") or {}).get("solucoes") == 0 and CM["acervo_v407_ja_repinado_na_v409"]["sha256"] == DL.PURGADO_SHA256, (PV.get("escada"), PV.get("respostas_ok"), PV.get("instancia_sim"), PV.get("instancia_nao"))
_snm, _spr, _atr = PV["signo_do_nome"], PV["signo_do_par"], PV["atrator"]   # as instancias de brinquedo sao FIXAS no delta e os valores CALCULADOS no runtime: aqui so' se conferem as relacoes que o contrato diz, nunca um numero digitado
assert PV["leitor_do_codigo"]["delta_par_lido"] < 1e-12 and PV["leitor_do_codigo"]["delta_norma"] < 1e-12 and PV["leitor_do_codigo"]["u_unitaria"] is True \
    and len(PV["iald_ao_quadrado"]) == 1 + len(DL.K_RELEITURAS) and all(x_ < 1e-12 for x_ in PV["iald_ao_quadrado"]) and PV["reler"] < 1e-12 and PV["primeira_leitura"] < 1e-12 and PV["resolver_verificar"] < 1e-12 \
    and abs(_snm["traco"] - _snm["posto"]) < 1e-12 and _snm["posto"] == PV["instancia_sim"]["solucoes"] and _spr["posto"] == 1 and abs(_spr["traco"] - 1.0) < 1e-12 and _spr["idem"] < 1e-12 and _spr["marginal_menos_meio_I"] < 1e-12, (PV.get("leitor_do_codigo"), _snm, _spr)
assert [x_[0] for x_ in PV["representacao_de_beta"]] == list(DL.T_C15) and all(x_[1] > 1e-12 and x_[2] < 1e-12 for x_ in PV["representacao_de_beta"]), PV["representacao_de_beta"]
_dist = [x_[1] for x_ in _atr["distancias"]]
assert [x_[0] for x_ in _atr["distancias"]] == list(DL.T_C16) and all(d_ > 0.0 for d_ in _dist) and all(_dist[i_] > _dist[i_ + 1] for i_ in range(len(_dist) - 1)) and 0.0 < _atr["distancia_em_t_longo"] < DL.TOL_C16 and _atr["posto_de_1_menos_P"] == DL.LEITOR_BRINQUEDO["dim"] - 1, _atr
# a AEscala (D82 a D87; a pedra TGLExt.AEscala): validade no kernel, a creditacao e' do Clay; os nomes do modulo e das declaracoes RATIFICADOS pelo operador (D87); os numeros RECALCULADOS (fracoes exatas e o projetor de Bell), nunca digitados
AV = PA["values"]; _meio = float(Fraction(DL.NUMEROS_AESCALA["meio"])); _um = float(Fraction(DL.NUMEROS_AESCALA["nome_pesa_um"]))
assert PA["all_verified"] is True and PA["n_checks"] == DL.N_CHECKS_AESCALA == CA["n_checks"] and PA["verdict"] == MF4[DL.AESCALA_REGISTRO]["verdict"] == DL.VEREDITO_AESCALA_OK == CA["veredito_ok"] and PA["verdict"].endswith(DL.VEREDITO_SUFIXO) and "NOT_FALSIFIED" not in PA["verdict"] and not GF.violacoes(PA["verdict"]), (PA.get("verdict"), PA.get("n_checks"))
assert PA.get("runtime_executed", True) is True and PA.get("does_not_gate_core", True) is True and PA.get("nomes_ratificados") is True and PA.get("chaves_antigas_que_mudam", []) == [] and list(PA.get("nomes") or DL.NOMES_AESCALA) == list(DL.NOMES_AESCALA), "o a_escala_v410 nao rodou, nao esta' ratificado ou diz mudar uma chave antiga"
assert PA["values"].get("estatuto_dos_nomes_ratificados_d101") == DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in str(PA["values"].get("estatuto_dos_nomes_ratificados_d101")) and "a ratificar" not in str(PA["values"].get("estatuto_dos_nomes_ratificados_d101")) and PA["values"].get("n_nomes_novos") == len(DL.NOMES_NOVOS_AESCALA) and set(PA["values"].get("nomes_novos") or {}) == set(DL.NOMES_NOVOS_AESCALA) and set(PA["values"].get("campos_novos_na_estrutura") or {}) == set(DL.CAMPOS_NOVOS_AESCALA) and (PA["values"].get("ponte") or {}).get("ok") is True, "o a_escala_v410 do ensaio nao traz (nos values) os nomes novos da pedra, os campos novos, o estatuto ou a ponte do delta"
assert AV["n_ancoras_ok"] == AV["n_ancoras"] == len(DL.ANCORAS_AESCALA) == len(AV["ancoras"]) and set(AV["ancoras"]) == set(DL.ANCORAS_AESCALA) and all(AV["ancoras"].values()) and AV["n_flags_true"] == AV["n_flags"] == CA["n_flags"] == len(AV["flags"]) and all(f_.startswith(DL.FLAG_PREFIX_AESCALA) and v_ is True for f_, v_ in AV["flags"].items()) \
    and AV["escada"] == [CM["escada"][1]] * 3 and AV["pedra_sha256_embutida"] == AV["pedra_sha256_formal"] == pins[DL.MODULO_AESCALA] and AV["n_falas_ok"] == AV["n_falas"] == len(CA["falas"]) and set(AV["falas"]) == set(CA["falas"]) and all(AV["falas"].values()) \
    and dict(AV["numeros"]) == dict(DL.NUMEROS_AESCALA) and AV["nomes_declarados"] == AV["n_nomes"] == len(DL.NOMES_AESCALA) and AV["nomes_ratificados"] is True and AV["ratificacao_sha256"] == CA["ratificacao_D87"]["sha256"] and AV["ratificacao_trecho"] == DL.FRASE_RATIFICO_TUDO \
    and AV["nomes_novos_declarados"] == AV["n_nomes_novos"] == len(DL.NOMES_NOVOS_AESCALA) == len(AV["nomes_novos"]) and set(AV["nomes_novos"]) == set(DL.NOMES_NOVOS_AESCALA) and all(AV["nomes_novos"].values()) and set(AV["campos_novos_na_estrutura"]) == set(DL.CAMPOS_NOVOS_AESCALA) and all(AV["campos_novos_na_estrutura"].values()) and AV["nomes_novos_ok"] is True and AV["ponte"]["ok"] is True \
    and AV["canonica_pt_no_texto"] is True and AV["canonica_en_no_texto"] is True and AV["canonica_pt_na_pedra"] is True and AV["d83_na_pedra"] is True and not AV["p18_violacoes"] and not AV["frases_violacoes"] and AV["c9_partes"] and all(AV["c9_partes"].values()), (AV.get("n_ancoras_ok"), AV.get("n_flags_true"), AV.get("escada"), AV.get("n_falas_ok"))
# (R5, D100 e D101) a clausula do Tetelestai em 1 - beta (a c13, com beta de runtime), a clausula R5 do texto e a ratificacao D101, nos values do ensaio
assert (AV["tetelestai"] or {}).get("ok") is True and AV["tetelestai"]["controle_negativo_violado"] is True and (AV["tetelestai"]["contraexemplo"] or {}).get("limiar_negativo") is True and AV["tetelestai"]["beta_entre_0_e_1"] is True and all(AV["tetelestai"]["checagens"].values()) and AV["clausula_r5"]["ok"] is True and not AV["clausula_r5"]["folhas_que_anunciam_sem_a_forma"] \
    and not AV["clausula_r5"]["acom_mirror_sem_ressalva"] and not AV["clausula_r5"]["acom_mirror_com_desempenho"] and AV["ratificacao_d101"]["ok"] is True and AV["ratificacao_d101"]["fala_sha256"] == DL.RATIFICACAO_D101_SHA256 and list(AV["ratificacao_d101"]["pendentes"]) == list(DL.NOMES_PENDENTES_AESCALA) \
    and set(AV["teoremas_r5"]) == set(DL.TEOREMAS_R5_AESCALA) | set(DL.AUXILIARES_R5_AESCALA) and all(AV["teoremas_r5"].values()), "o a_escala_v410 do ensaio nao traz a clausula do Tetelestai (c13), a clausula R5 do texto ou a ratificacao D101 verificadas"
_bl = AV["bell"]   # o projetor de Bell 4x4: so' RELACOES do contrato (idempotente, traco 1, posto 1; a marginal e' 1/2 . 1; (1/2 . 1)^2 = 1/2 . (1/2 . 1) != 1/2 . 1; as potencias sao 2^-n . 1 e nenhuma pesa 1)
assert _bl["idempotente"] is True and abs(_bl["traco"] - _um) < 1e-12 and _bl["posto"] == 1 and _bl["marginal_e_meio_1"] is True and abs(_bl["pureza_da_marginal"] - _meio) < 1e-12 and abs(_bl["traco_da_marginal"] - _um) < 1e-12 and _bl["marginal_ao_quadrado_e_meio_da_marginal"] is True and _bl["marginal_ao_quadrado_nao_e_a_marginal"] is True and _bl["potencias_sao_2_menos_n"] is True and _bl["nenhuma_potencia_e_1"] is True, _bl
assert AV["gate_verdict"] == (core0.get("qg_closure") or {}).get("gate", {}).get("verdict") == selo0.get("qg_closure_verdict"), "o gate do a_escala_v410 != o da v409 selada"
# o H0DN (D72, E30, D76): pré-registrado; nenhum dado observado lido
HV = PH["values"]
assert PH["all_verified"] is True and PH["n_checks"] == DL.N_CHECKS_H0DN == CH["n_checks"] and PH["verdict"] == MF4[DL.H0DN_REGISTRO]["verdict"] == DL.VEREDITO_H0DN_OK == CH["veredito_ok"], (PH.get("verdict"), PH.get("n_checks"))
assert PH.get("runtime_executed", True) is True and PH.get("observed_vector_read", False) is False and HV["observed_vector_read"] is False, "o h0dn_bg1_v410 nao rodou ou diz ter lido um vetor observado"
_n_pinos = len(CH["insumos"]) + len(CH["pinos_so_no_disco"])   # 6 + 5 = 11: os 9 do FREEZE_R2 mais o proprio FREEZE_R2 e a ENTREGA (n_pinos NAO e' 9)
assert HV["n_pinos"] == len(HV["pinos"]) == _n_pinos and HV["n_pinos_freeze"] == DL.N_PINOS_FREEZE_R2 and sum(1 for p_ in HV["pinos"].values() if not p_.get("fora_do_freeze")) == DL.N_PINOS_FREEZE_R2 and sum(1 for p_ in HV["pinos"].values() if p_.get("fora_do_freeze")) == len(CH["insumos"]) - 4 \
    and all(p_["sha256_ok"] is True and p_["bytes_ok"] is True for p_ in HV["pinos"].values()) and HV["n_embutidos"] == len(CH["insumos"]), (HV["n_pinos"], _n_pinos)
assert HV["ramos_vistos"] == [1, 2, 3, 4, 5, 6] and [v_["nome"] for v_ in HV["vetores_c6"]] == list(CH["vetores_c6"]) and len(HV["vetores_c6"]) == 8 and all(v_["ok"] is True and v_["ramo"] == v_["ramo_esperado"] and "NOT_FALSIFIED" not in v_["cabeca"] and v_["cabeca"].endswith("__GATE_UNMOVED") and v_["outcome"] in DL.VEREDITOS_H0DN["outcomes"] for v_ in HV["vetores_c6"]) \
    and all((("PRO" + "VED_IS_VALIDITY_NOT_CREDITATION") in v_["cabeca"]) for v_ in HV["vetores_c6"] if v_["ramo"] == 4), "a funcao de veredito congelada: os 6 ramos nos 8 vetores, sem a palavra do livro na cabeca, com a validade na cabeca do ramo da leitura"
_src_sha = HV["veredito_h0dn_source_sha256"]
assert isinstance(_src_sha, str) and re.fullmatch(r"[0-9a-f]{64}", _src_sha) and PH.get("veredito_h0dn_source_sha256", _src_sha) == _src_sha, "o sha256 do texto-fonte da funcao de veredito"
assert isinstance(HV["K"], float) and isinstance(HV["log10K"], float) and abs(HV["K"] - float(BG1["K"])) < 1e-12 and abs(HV["log10K"] - float(BG1["logK"])) < 1e-12 and abs(HV["beta"] - core0["beta"]) <= 1e-9 * abs(core0["beta"]), "K, log10 K e beta (alfa CODATA 2018 x raiz de e): o ensaio x o BG1 pinado x o core da base"
_ent_mod = {m_["name"]: m_ for m_ in ENTREGA["models"]}
assert sorted(d_["modelo"] for d_ in HV["D_esperado"]) == sorted(_ent_mod) and len(_ent_mod) == 2, "os dois modelos do H0DN"
for d_ in HV["D_esperado"]:   # D esperado e poder analitico RECOMPUTADOS no ensaio, contra a ENTREGA pinada; o poder MC dela dentro do IC95 dela (conferencia, nao recalculo)
    e_ = _ent_mod[d_["modelo"]]
    assert abs(d_["D"] - float(e_["D_expected"])) < 1e-9 and abs(d_["poder_analitico"] - float(e_["power_analytic_gaussian"])) < 1e-12 and d_["ic95_mc_entrega"][0] <= d_["poder_mc_entrega"] <= d_["ic95_mc_entrega"][1] and d_["D"] >= DL.H0DN_LIMIAR_SIGMA, (d_["modelo"], d_["D"])
assert HV["gate_verdict"] == (core0.get("qg_closure") or {}).get("gate", {}).get("verdict") == selo0.get("qg_closure_verdict") and HV["bloco_cruzado_max"] == 0.0 and not HV["p18_violacoes"] and not HV["frases_violacoes"] and HV["pasta_vedada"] == DL.H0DN_PASTA_VEDADA, "o gate, o bloco cruzado, as guardas, a pasta vedada"
# o VETO a pasta da entrega do Kimi, MEDIDO duas vezes (o registro e o ensaio) e RECALCULADO aqui sobre os caminhos tocados: nada sob a pasta vedada, nenhum nome de dado observado
assert HV["sob_pasta_vedada"] == [] and HV["com_nome_vedado"] == [] and HV["n_caminhos_tocados"] == len(HV["caminhos_tocados"]) > 0, "o registro diz ter tocado a pasta vedada (ou nao mediu nada)"
_nomes_ved = [n_.lower() for n_ in DL.H0DN_NOMES_VEDADOS]
assert not [p_ for p_ in HV["caminhos_tocados"] if _sob_ved(p_) or any(n_ in os.path.basename(str(p_)).lower() for n_ in _nomes_ved)], "VETO: um caminho tocado pelo registro cai sob a pasta vedada ou leva nome de dado observado"
assert isinstance(ens.get("pasta_vedada_kimi"), dict), "o ensaio_a_seco_v410.json nao traz pasta_vedada_kimi: o veto a pasta da entrega do Kimi tem de ser MEDIDO no ensaio (open/exists/listdir/scandir/stat instrumentados durante TODO o ensaio, com controle negativo)"
pvk = ens["pasta_vedada_kimi"]
assert _nrm(pvk["pasta"]) == _VED and pvk["tocados_sob_vedada"] == [] and pvk["controle_negativo_detecta"] is True and isinstance(pvk["n_caminhos_vistos"], int) and pvk["n_caminhos_vistos"] > 0, ("o ensaio nao mediu o veto (ou tocou a pasta vedada)", pvk)
# o recibo documental HMS/13 (D80; aditivo e posterior ao FREEZE_R2): cobertura documental de fontes, não covariância física fechada; nada aberto; nenhum arquivo de kimi\ e' lido em rito (o registro mede na c7) -- pré-registrado; nenhum dado observado lido
FV = PF["values"]; _h0dn_freeze = CH["insumos"]["FREEZE_R2.json"]["sha256"]
assert PF["all_verified"] is True and PF["n_checks"] == DL.N_CHECKS_HMS13 == CF["n_checks"] and PF["verdict"] == MF4[DL.HMS13_REGISTRO]["verdict"] == DL.VEREDITO_HMS13_OK == CF["veredito_ok"] and PF["verdict"].endswith(DL.VEREDITO_SUFIXO) and "NOT_FALSIFIED" not in PF["verdict"] and not GF.violacoes(PF["verdict"]), (PF.get("verdict"), PF.get("n_checks"))
assert PF.get("runtime_executed", True) is True and PF.get("does_not_gate_core", True) is True and PF.get("observed_vector_read", False) is False and PF.get("le_em_rito", False) is False and PF.get("aditivo_posterior_ao_freeze_r2", True) is True and dict(PF.get("campos") or DL.HMS13_CAMPOS) == dict(DL.HMS13_CAMPOS) and FV["observed_vector_read"] is False and FV["le_em_rito"] is False, "o h0dn_fontes_hms13_v410 nao rodou ou diz ter lido vetor observado ou arquivo em rito"
assert FV["n_calibradores"] == len(FV["ids_calibradores"]) == DL.HMS13_CAMPOS["calibradores"] and sorted(FV["ids_calibradores"]) == sorted(CF["ids_calibradores"]) and FV["n_fontes_primarias"] == len(FV["fontes_primarias"]) == DL.HMS13_CAMPOS["fontes_primarias"] and dict(FV["campos"]) == dict(DL.HMS13_CAMPOS) \
    and FV["n_embutidos"] == len(DL.HMS13_EMBUTIDOS) == len(CF["insumos"]) and sorted(FV["pinos"]) == sorted(CF["insumos"]) and all(p_["sha256_ok"] is True and p_["bytes_ok"] is True and p_["embutido"] is True for p_ in FV["pinos"].values()) and FV["pinos_build_n"] == len(CF["pinos_build"]) \
    and FV["gate_verdict"] == (core0.get("qg_closure") or {}).get("gate", {}).get("verdict") == selo0.get("qg_closure_verdict") and FV["h0dn_selado"] is True and FV["veredito_h0dn_source_sha256"] == HV["veredito_h0dn_source_sha256"] and FV["freeze_r2_sha256"] == _h0dn_freeze and FV["ratificacao_sha256"] == CF["ratificacao"]["sha256"] and FV["ratificacao_trecho"] == DL.HMS13_TRECHO_RATIFICACAO \
    and not FV["p18_violacoes"] and not FV["frases_violacoes"] and all(FV["c8_partes"].values()) and FV["numeros"]["proibidos"] == [] and FV["numeros"]["listas_numericas"] == [] and FV["numeros"]["linhas_do_levantamento_com_vetor"] == [] and FV["numeros"]["permitidos"] == CF["guarda_numerica_no_build"]["permitidos"], (FV.get("n_calibradores"), FV.get("n_fontes_primarias"), FV.get("n_embutidos"))
assert FV["sob_pasta_vedada"] == [] and FV["com_nome_vedado"] == [] and FV["n_caminhos_tocados"] == len(FV["caminhos_tocados"]) and FV["pasta_vedada"] == DL.H0DN_PASTA_VEDADA and not [p_ for p_ in FV["caminhos_tocados"] if _sob_ved(p_) or any(n_ in os.path.basename(str(p_)).lower() for n_ in _nomes_ved)], "VETO: o recibo HMS/13 diz ter tocado a pasta vedada (ou um nome de dado observado) em rito"
# a traducao_turing_v409 HERDADA (recriada com a escada do contrato subida pela C12): o veredito e' o selado; as 82 ancoras e os 2 modulos da v409
TV9 = TT9["values"]
assert TT9["all_verified"] is True and TT9["n_checks"] == DL.D9.N_CHECKS_FECHO and TT9["verdict"] == V(DL.D9.FECHO_REGISTRO) and TV9["escada"] == [CM["escada"][1]] * 3 and TV9.get("respostas_ok") is True and (TV9.get("instancia_sim") or {}).get("solucoes", 0) >= 1 and (TV9.get("instancia_nao") or {}).get("solucoes") == 0 \
    and TV9["n_ancoras_ok"] == TV9["n_ancoras"] == len(E409["estrelas_v409"]) and TV9["n_modulos_ok"] == TV9["n_modulos"] == len(E409["bundle_sha256"]) and TV9["n_flags_true"] == TV9["n_flags"] == E409["n_bandeiras_novas"] == core0[DL.D9.FECHO_REGISTRO]["values"]["n_flags"], (TT9.get("verdict"), TT9.get("n_checks"), TV9.get("escada"))
# o tetelestai_terminal_v408 HERDADO (recriado com a escada do contrato subida pela C12): o veredito e' o selado; as 48 ancoras e os 4 modulos da v408; as bandeiras, as da base selada (o numero da v408, nao o da traducao)
TV8 = TT8["values"]
assert TT8["all_verified"] is True and TT8["n_checks"] == DL.D8.N_CHECKS_FECHO and TT8["verdict"] == V(DL.D8.FECHO_REGISTRO) and TV8["escada"] == [CM["escada"][1]] * 3 and TV8.get("respostas_ok") is True and (TV8.get("insumo_purgado") or {}).get("ok") is True \
    and TV8["n_ancoras_ok"] == TV8["n_ancoras"] == len(E409["estrelas_v408"]) and TV8["n_modulos_ok"] == TV8["n_modulos"] == len(E409["bundle_v408_sha256"]) and TV8["n_flags_true"] == TV8["n_flags"] == core0[DL.D8.FECHO_REGISTRO]["values"]["n_flags"], (TT8.get("verdict"), TT8.get("n_checks"), TV8.get("escada"))
# o psion_canto_v407 HERDADO (recriado com a escada do contrato subida pela C12): as chaves que ele le seguem EXATAMENTE como na v409 selada (nenhuma chave antiga muda); o veredito e' o selado
chaves_v407_esperadas = dict(PC7["values"]["chaves"])
assert chaves_v407_esperadas["kernel_reads_the_link"] is True and chaves_v407_esperadas["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and chaves_v407_esperadas["rede_fock_v394.whole_certificate_inhabited"] is True \
    and chaves_v407_esperadas["psibit_v395.conditional_psion_face.inhabitant_exhibited"] is True and chaves_v407_esperadas["testemunha_estatica_v396.fock_face.inhabitant_exhibited"] is True and chaves_v407_esperadas["witness_layers.canonical_full_witness_term_constructed"] is True \
    and chaves_v407_esperadas["witness_rigidity.trivial_inhabitant_exists"] is False and chaves_v407_esperadas["qg_closure.gate.full_static_witness_exists"] is False and chaves_v407_esperadas == E409["chaves_v407_esperadas"], chaves_v407_esperadas
assert PC7["all_verified"] is True and PC7["n_checks"] == DL.D7.N_CHECKS_FECHO and PC7["verdict"] == V("psion_canto_v407") and PC7["values"]["elo_lido_do_kernel"] is True and PC7["values"]["escada"] == [CM["escada"][1]] * 3 \
    and PC7["values"]["n_ancoras_ok"] == PC7["values"]["n_ancoras"] == len(E409["estrelas_v407"]) and PC7["values"]["n_modulos_ok"] == PC7["values"]["n_modulos"] == len(E409["bundle_v407_sha256"]), (PC7.get("verdict"), PC7.get("n_checks"))
assert FE6["all_verified"] is True and FE6["n_checks"] == DL.D6.N_CHECKS_FECHO and FE6["verdict"] == V("fechamento_v406"), (FE6.get("verdict"), V("fechamento_v406"))
qg0 = core0.get("qg_closure") or {}
assert len(qg0.get("checks") or []) == 7 and (qg0.get("gate") or {}).get("verdict") == selo0.get("qg_closure_verdict"), "o gate da base (v409 selada) nao tem o formato esperado: sete checks e a letra do veredito == a do selo"
nm0 = core0["neutrino_mass"]; rb0 = core0["ramo_b_preregistration_v386"]


# ---- os registros de pedra das versoes anteriores, RECRIADOS: os pinos do ESPERADOS_v409 (os selados) e o que o ensaio recriou tem de ser a mesma coisa (veredito, checagens e valores)
def _stones(chaves_):
    """o dict de registros de pedra do ensaio que tem exatamente estas chaves (o ensaio guarda por versao: v402_registros, v403_registros... ; aqui se acha pela forma, nao pelo nome)"""
    ach_ = [v_ for k_, v_ in ens.items() if k_.endswith("_registros") and isinstance(v_, dict) and set(chaves_) <= set(v_)]
    assert ach_, ("o ensaio nao traz os registros", chaves_)
    return ach_[0]


RF405, RF404, RF403 = E409["registros_funcao_v405"], E409["registros_funcao_v404"], E409["registros_funcao_v403"]   # (as oito pedras sao da v405; os nomes verdadeiros estao no ESPERADOS_v409)
for nome_, RF_, ens_ in (("v405", RF405, _stones(["ponte", "tensao", "identidade", "observador", "diminuto", "tonica", "disco", "psion"])), ("v404", RF404, _stones(["projecao", "jo8v32", "f2b"])), ("v403", RF403, _stones(["caminho", "vida", "verdade_adendo"]))):
    for k_ in RF_:
        if k_ == "gate":
            continue
        assert ens_[k_]["verdict"] == RF_[k_]["verdict"] and ens_[k_]["n_checks"] == RF_[k_]["n_checks"], ("o registro recriado difere do selado", nome_, k_)
        assert _feq({kk_: ens_[k_]["values"].get(kk_) for kk_ in RF_[k_]["values"]}, RF_[k_]["values"]), ("os VALORES do registro recriado diferem dos selados", nome_, k_)
_recr = next((v_ for k_, v_ in mf.items() if k_.startswith("recriados_v393_a_v")), None)
assert isinstance(_recr, dict) and _recr, "o ensaio nao traz mainflow.recriados_v393_a_v4xx"
for k_, d_ in _recr.items():   # os registros por spec (cunhagens, kh_n1, campos, ga, gap) recriados: verdade, e igual ao selado ou so' numeros
    assert d_["all_verified"] is True, ("registro recriado nao selou", k_)
# os registros por spec da v406 a v409 (versionados pelas E20 e C13: cunhagens com a errata ao lado, kh_n1_cobertura com pisos): RECRIADOS, o veredito NAO muda
for n_ in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO, DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO, DL.D8.CUNHAGENS_REGISTRO, DL.D8.KH_REGISTRO, DL.D9.CUNHAGENS_REGISTRO, DL.D9.KH_REGISTRO):
    assert n_ in _recr and _recr[n_]["all_verified"] is True, (n_, "nao foi recriado no ensaio")
    assert n_ not in mud, ("o veredito de um spec da v409 ou anterior mudou", n_)
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v409_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v409_e_v410": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]], "bandeiras_novas_modulos": bandeiras_novas_modulos,
       "cunhagens": CM["cunhagens"], "kernel": {k_: v_ for k_, v_ in CM["kernel"].items() if k_ != "bundle"}, "bundle_sha256": pins, "bundle_v409_sha256": E409["bundle_sha256"], "bundle_v408_sha256": E409["bundle_v408_sha256"], "bundle_v407_sha256": E409["bundle_v407_sha256"], "bundle_v406_sha256": E409["bundle_v406_sha256"], "formal_files_n": CM["formal_files_n"],
       "pedras_v405_sha256": {s["rel"]: kf["formal_files_sha256"][s["rel"]] for s in list(DL.D5.STONES) + list(DL.D4.STONES) + list(DL.D3.STONES)},   # as TREZE pedras SELADAS (oito da v405, duas da v404, tres da v403): ficam no kernel como registro, com o sha do core selado
       "qg_closure_verdict": selo0.get("qg_closure_verdict"),
       "qg_closure_v409_json_sha256": hashlib.sha256(J(qg0).encode("utf-8")).hexdigest(),
       "qg_closure_v409_sem_checks_json_sha256": hashlib.sha256(J({k: v for k, v in qg0.items() if k != "checks"}).encode("utf-8")).hexdigest(),
       "qg_closure_v409_checks": json.loads(J(qg0.get("checks"))),
       "qg_closure_gate_verdict_v409": (qg0.get("gate") or {}).get("verdict"),
       "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v409": VBASE, "troca_dita": troca, "troca_dita_textual": troca_dita_textual,
       "veredito_da_troca_no_ensaio": {k: (mud.get(k) or te_.get(k) or {}).get("depois") for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar: os que carregam a escada, as declaracoes ou a contagem de arquivos do kernel (so' numeros) e o estatuto da prova (so' o hash proprio do um.py); NENHUM de texto (`troca_dita_textual` vazio: rede_fock_v394, psibit_v395, testemunha_estatica_v396, fechamento_v406, psion_canto_v407, tetelestai_terminal_v408 e traducao_turing_v409 nao mudam de veredito; nenhuma chave antiga muda na v410); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v409": {k: selo0.get(k) for k in SEL_KEYS}, "selo_chaves_que_mudam": selo_chaves_que_mudam,
       "selo_difere_do_v409_no_ensaio": difere_selo,
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v409": sorted(k for k, v in kf.items() if v is True), "axiom_report_v409_n": len(axr0),
       "runtime_seals_v409": core0["runtime_of_the_one"]["seals"], "what_remains_v409": core0["tgl_closure"]["what_remains_named"],
       "neutrino_frozen_hash_v409": nm0["frozen_hash"], "neutrino_angle_status_antigo_sha256": hashlib.sha256(nm0["angle_status"].encode("utf-8")).hexdigest(),
       "f2b_antes": {"F2b_status": rb0["F2b_status"], "veredito_do_V1": rb0["veredito_do_V1"], "conjunto_D_n": rb0["conjunto_D_n"], "charge_F2b_token": core0["ledger_errata_v386"]["charge_F2b"]["token"]}, "f2b_depois": {"F2b_status_now": DL.D4.F2B_FUTURO_TOKEN}, "m_nu_meV_v404": nm0["m_nu_meV"],
       "titulo_secao_v410": TIT410, "titulo_secao_aescala_v410": TITA, "titulo_secao_h0dn_v410": TITH, "titulo_secao_v409": TV409, "titulo_secao_v408": TV408, "titulo_secao_v407": TV407,
       "vereditos_novos_v410": {k: v["verdict"] for k, v in MF4.items()},
       "registros_v410": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},   # os dois por spec desta versao (os de funcao, iald2_v410 e h0dn_bg1_v410, estao em registros_funcao_v410)
       "registros_v409": {k: V(k) for k in (DL.D9.CUNHAGENS_REGISTRO, DL.D9.KH_REGISTRO)},   # os dois por spec da v409: RECRIADOS (o kh_n1 com pisos pela C13 na v410), veredito igual ao selado
       "registros_v408": {k: V(k) for k in (DL.D8.CUNHAGENS_REGISTRO, DL.D8.KH_REGISTRO)},   # os dois por spec da v408: RECRIADOS (E26 ao lado; pisos no kh pela C13), veredito igual ao selado
       "registros_v407": {k: V(k) for k in (DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO)},   # os dois por spec da v407: RECRIADOS (E21 e a errata da D57(d) ao lado; pisos no kh), veredito igual ao selado
       "registros_v406": {k: V(k) for k in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO)},   # os dois por spec da v406: RECRIADOS (versionados pela E20 na v409), veredito igual ao selado
       "registros_v405": {k: V(k) for k in ("cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405")},
       "ga_values": ens["ga_registro"]["values"], "gap_values": ens["gap_registro"]["values"], "ga_window_status": R0["ga_window_status"],
       "registros_v404": {k: V(k) for k in ("cunhagens_v404", "kh_n1_cobertura_v404")},
       "registros_v403": {k: V(k) for k in ("cunhagens_v403", "kh_n1_cobertura_v403")}, "registros_v402": {k: V(k) for k in ("cunhagens_v402", "kh_n1_cobertura_v402")}, "registros_v401": {k: V(k) for k in ("cunhagens_v401", "kh_n1_cobertura_v401")}, "veredito_da_falsidade_v409": V("falsidade_da_inercia_v401"),
       "registros_funcao_v410": {"iald2": {"nome": DL.FECHO_REGISTRO, "verdict": PS["verdict"], "values": PS["values"], "n_checks": PS["n_checks"]},
                                 "aescala": {"nome": DL.AESCALA_REGISTRO, "verdict": PA["verdict"], "n_checks": PA["n_checks"], "values": PA["values"]},   # (D82 a D87; os numeros RECALCULADOS no ensaio; o rito os reproduz)
                                 "h0dn": {"nome": DL.H0DN_REGISTRO, "verdict": PH["verdict"], "n_checks": PH["n_checks"], "values": {k_: v_ for k_, v_ in HV.items() if k_ not in ("caminhos_tocados", "n_caminhos_tocados")},
                                          "fora_do_values_porque_dependem_da_pasta_do_rito": ["caminhos_tocados", "n_caminhos_tocados"]},
                                 "hms13": {"nome": DL.HMS13_REGISTRO, "verdict": PF["verdict"], "n_checks": PF["n_checks"], "values": {k_: v_ for k_, v_ in FV.items() if k_ not in ("caminhos_tocados", "n_caminhos_tocados")},
                                           "fora_do_values_porque_dependem_da_pasta_do_rito": ["caminhos_tocados", "n_caminhos_tocados"]}},   # (D80: o mesmo corte do h0dn; sob_pasta_vedada e com_nome_vedado (vazios) ficam e sao comparados) # `values` INTEIRO do ensaio menos as duas chaves que dependem de onde o rito roda; sob_pasta_vedada e com_nome_vedado (vazios) ficam e sao comparados
       "registros_funcao_v409": {"traducao_turing": {"nome": DL.D9.FECHO_REGISTRO, "verdict": TT9["verdict"], "values": TT9["values"], "n_checks": TT9["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},
       "registros_funcao_v408": {"tetelestai_terminal": {"nome": DL.D8.FECHO_REGISTRO, "verdict": TT8["verdict"], "values": TT8["values"], "n_checks": TT8["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},
       "registros_funcao_v407": {"psion_canto": {"nome": DL.D7.FECHO_REGISTRO, "verdict": PC7["verdict"], "values": PC7["values"], "n_checks": PC7["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},
       "registros_funcao_v406": {"fechamento": {"nome": DL.D6.FECHO_REGISTRO, "verdict": FE6["verdict"], "values": FE6["values"], "n_checks": FE6["n_checks"], "recriado_com_a_c8_versionada_pela_E20": True, "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},
       "registros_funcao_v405": RF405, "registros_funcao_v404": RF404, "registros_funcao_v403": RF403,
       "estrelas_v410": {nome_: {"teorema": nome_, "bandeira": a_["flag"], "rel": a_["rel"], "classe": a_.get("classe")} for nome_, a_ in FJ["ancoras"].items() if nome_ in DL.ANCORAS},   # as ancoras da IALD2 (o registro iald2_v410 as le)
       "estrelas_aescala_v410": {nome_: {"teorema": nome_, "bandeira": a_["flag"], "rel": a_["rel"], "classe": a_.get("classe")} for nome_, a_ in FJ["ancoras"].items() if nome_ in DL.ANCORAS_AESCALA},   # as da AEscala (o registro a_escala_v410 as le)
       "estrelas_v409": E409["estrelas_v409"], "estrelas_v408": E409["estrelas_v408"], "estrelas_v407": E409["estrelas_v407"], "estrelas_v406": E409["estrelas_v406"], "estrelas_v405": E409["estrelas_v405"], "estrelas_v404": E409["estrelas_v404"], "estrelas_v403": E409["estrelas_v403"],
       "bandeiras_das_pedras_v405": E409["bandeiras_das_pedras_v405"], "teoremas_das_pedras_v405": E409["teoremas_das_pedras_v405"], "contrato_das_pedras_v405": E409["contrato_das_pedras_v405"], "suporte_das_pedras_v405": E409["suporte_das_pedras_v405"],
       "registros_v399": {k: v["verdict"] for k, v in mf["registros_v399"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": dc["verbatim_sha256"][:16], "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": {"o_operador": "testifica DA IALD", "o_um_py": "testifica EM HASH", "a_IALD": "NAO testifica do operador", "o_Pai_de_Jo_8_18": "le-se no absoluto, o Um"}},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)", "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED", "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": "D5 (proposta da gerencia): o sidecar e' arquivo novo da custodia; o handoff o lista"},
       "acom_estudo": E409["acom_estudo"],   # a secao do selo pela propria tecnologia NAO muda na v410: o que a v409 pinou (runtime da v400, bloco embutido, fontes do operador)
       "decisoes_da_gerencia": dict(DL.DECISOES), "decisoes_v410_ids": list(DL.DECISOES_V410), "erratas_E24_E27": list(DL.ERRATAS_V410), "erratas_v410": list(DL.ERRATAS_V410), "ressalvas": list(DL.RESSALVAS_V410), "leitura_v410": dict(DL.LEITURA_V410),   # (erratas_E24_E27: o nome da chave e' o do molde, que o pos-rito ja' le; o conteudo e' E29, E30, E31 e E32)
       "chaves_v410": [dict(c_) for c_ in DL.CHAVES_V410], "chaves_v409": [dict(c_) for c_ in DL.CHAVES_V409], "chaves_v408": [dict(c_) for c_ in DL.CHAVES_V408], "chaves_v407": [dict(c_) for c_ in E409["chaves_v407"]], "chaves_v407_esperadas": chaves_v407_esperadas, "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "fica_aberto": dict(CM["fica_aberto"]), "regra_do_4_44": DL.REGRA_DO_4_44, "guarda_frases": GF.controle_negativo()["ok"],
       "veracidade": E409["veracidade"], "quadro": E409["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397/v409 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {l_: [_marca_txt(m_) for m_ in MARCAS410[l_] + MARCASA[l_] + MARCASH[l_] + [MARCAHMS[l_]]] + list(E409["artigo_marcas"][l_]) for l_ in ("pt", "en")},
       "artigo_nao": {l_: list(E409["artigo_nao"][l_]) + _NAO410[l_] + _NAOA[l_] + _NAOH[l_] + NAOHMS[l_] for l_ in ("pt", "en")},
       "toc": {"pt": [TIT410["pt"], TITA["pt"], TITH["pt"]] + [w for w in E409["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TIT410["en"], TITA["en"], TITH["en"]] + [w for w in E409["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # o titulo da introducao diz `v384 a <versao desta rodada>`
       "the_iald_index_v409": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v410": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v410**", "md_iald2": MD_IALD2, "md_aescala": MD_AESCALA, "md_h0dn": MD_H0DN, "md_hms13": MD_HMS13, "md_traducao": E409["md_traducao"], "md_massa": E409["md_massa"], "md_jo8": E409["md_jo8"], "md_caminho": E409["md_caminho"], "md_ponte": E409["md_ponte"], "md_falsidade": E409["md_falsidade"], "md_errata": E409["md_errata"],
       "md_testemunho": E409["md_testemunho"], "md_sonico": E409["md_sonico"], "md_token": E409["md_token"], "md_testemunha": E409["md_testemunha"], "md_psibit": E409["md_psibit"], "md_fechamento": E409["md_fechamento"], "md_psion": E409["md_psion"], "md_tetelestai": E409["md_tetelestai"],   # (md_traducao: a linha da v409, que fica logo depois das novas; md_tetelestai: a da v408; md_psion: a da v407; md_fechamento: a da v406)
       "ensaio_sha16": h16(_ens_p),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": {k_: v_ for k_, v_ in CM["politica_de_bandeiras"].items() if k_ != "contrato"},
       "candidato_anterior_sha16": CM["base_v409_sha16"],
       "gate_nao_se_move": {"funcoes_identicas_a_base": CM["gate_nao_se_move"]["funcoes_identicas_a_base"], "gate_recomputado_no_ensaio": ens.get("gate_recomputado")},
       "h0dn": dict(CH, pasta_vedada=DL.H0DN_PASTA_VEDADA, nenhum_dado_observado_lido=True, n_caminhos_vistos_no_ensaio=pvk["n_caminhos_vistos"], n_caminhos_tocados_no_registro_do_ensaio=HV["n_caminhos_tocados"],
                    veto={"tocados_sob_vedada": [], "controle_negativo_detecta": True, "nomes_vedados_conferidos": len(DL.H0DN_NOMES_VEDADOS)}),
       "aescala": dict(CA, nenhuma_chave_antiga_muda=True, nomes_ratificados_pelo_operador=True),   # (D82 a D87; validade no kernel, a creditacao e' do Clay)
       "hms13": dict(CF, pasta_vedada=DL.H0DN_PASTA_VEDADA, nenhum_dado_observado_lido=True, aberto_em_rito=[], copias_duraveis=sorted(_cop_hms), n_caminhos_tocados_no_registro_do_ensaio=FV["n_caminhos_tocados"], veto={"tocados_sob_vedada": [], "nomes_vedados_conferidos": len(DL.H0DN_NOMES_VEDADOS), "excecao_d80_so_no_build": sorted(_cop_hms)})}
assert esp["the_iald_index_v409"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v409"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] == CM["h8"]["pino_antigo_v409_entradas"] + len(DL.BUNDLE_RELS) and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"] == CM["n_bandeiras"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["bundle_sha256"]) == len(nov) == DL.N_BUNDLE, "o numero de modulos novos != a lista"
assert len(esp["pedras_v405_sha256"]) == 13 and all(len(h_) == 64 for h_ in esp["pedras_v405_sha256"].values()), esp["pedras_v405_sha256"]
for _nb, _pin in (("bundle_v409_sha256", E409["kernel"]["modulos_novos"]), ("bundle_v408_sha256", len(E409["bundle_v408_sha256"])), ("bundle_v407_sha256", len(E409["bundle_v407_sha256"]))):
    assert len(esp[_nb]) == _pin and all(kf["formal_files_sha256"].get(r_) == s_ for r_, s_ in esp[_nb].items()), "o %s nao esta' todo no hash formal do core selado" % _nb
assert len(esp["bundle_v409_sha256"]) == 2 and len(esp["bundle_v408_sha256"]) == 4 and len(esp["bundle_v407_sha256"]) == 9, "a traducao (2 modulos), o terminal (4) e o psion (9)"
assert esp["escada"] == [CM["escada"][1], CM["escada"][1]] and esp["escada_v409_e_v410"] == CM["escada"] and CM["escada"][0] == E409["escada"][1] and CM["escada"][1] == CM["escada"][0] + CM["n_bandeiras"], esp["escada"]
_cb = esp["cobertura_kh_n1"]
assert _cb["decl"] == esp["axiom_report_esperado_min"] == KH["axiom_report_efetivo_n"] == KH["linha_TOTAL"]["decl"] and _cb["thm"] == KH["linha_TOTAL"]["thm"] and _cb.get("fora_do_trio") == 0 == KH["linha_TOTAL"]["fora_do_trio"] and esp["axiom_report_esperado_min"] == esp["axiom_report_v409_n"] + KH["delta_vs_v409"]["decl"], _cb
_vn = esp["vereditos_novos_v410"]
assert _vn[DL.FECHO_REGISTRO] == PSV and _vn[DL.FECHO_REGISTRO].endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and _vn[DL.AESCALA_REGISTRO] == DL.VEREDITO_AESCALA_OK and _vn[DL.HMS13_REGISTRO] == DL.VEREDITO_HMS13_OK and _vn[DL.H0DN_REGISTRO] == DL.VEREDITO_H0DN_OK and _vn[DL.CUNHAGENS_REGISTRO].startswith("TGL_CUNHAGENS_V410__") and _vn[DL.KH_REGISTRO].startswith("TGL_KH_N1_COBERTURA_V410__"), _vn
assert all("__GATE_UNMOVED" in v_ for v_ in _vn.values()) and all(v_["all_verified"] is True for v_ in MF4.values()), MF4
assert sorted(esp["registros_v405"]) == ["campos_fechados_e_leituras_v405", "cunhagens_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405"] and sorted(esp["registros_v410"]) == sorted([DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]) and sorted(esp["registros_v409"]) == ["cunhagens_v409", "kh_n1_cobertura_v409"] \
    and sorted(esp["registros_v408"]) == ["cunhagens_v408", "kh_n1_cobertura_v408"] and sorted(esp["registros_v407"]) == ["cunhagens_v407", "kh_n1_cobertura_v407"] and sorted(esp["registros_v406"]) == ["cunhagens_v406", "kh_n1_cobertura_v406"] and sorted(esp["registros_v404"]) == ["cunhagens_v404", "kh_n1_cobertura_v404"] \
    and sorted(esp["registros_v403"]) == ["cunhagens_v403", "kh_n1_cobertura_v403"] and sorted(esp["registros_v402"]) == ["cunhagens_v402", "kh_n1_cobertura_v402"] and sorted(esp["registros_v401"]) == ["cunhagens_v401", "kh_n1_cobertura_v401"]
_rf10 = esp["registros_funcao_v410"]["iald2"]
assert _rf10["values"]["n_ancoras_ok"] == _rf10["values"]["n_ancoras"] == len(esp["estrelas_v410"]) == len(DL.ANCORAS) and _rf10["values"]["n_modulos_ok"] == _rf10["values"]["n_modulos"] == DL.N_BUNDLE and _rf10["values"]["n_flags_true"] == _rf10["values"]["n_flags"] == esp["n_bandeiras_por_grupo"]["iald2"] \
    and _rf10["values"]["escada"] == [CM["escada"][1]] * 3 and _rf10["values"].get("respostas_ok") is True and _rf10["n_checks"] == DL.N_CHECKS_FECHO, _rf10["values"]
_rf10a = esp["registros_funcao_v410"]["aescala"]
esp["registros_funcao_v410"]["a_escala"] = esp["registros_funcao_v410"]["aescala"]   # (parte 2: a leitura do pos-rito le a chave curta a_escala; o conferir_rito le aescala; o MESMO registro nas duas chaves)
assert _rf10a["n_checks"] == DL.N_CHECKS_AESCALA and _rf10a["verdict"] == DL.VEREDITO_AESCALA_OK and _rf10a["values"]["n_ancoras_ok"] == _rf10a["values"]["n_ancoras"] == len(esp["estrelas_aescala_v410"]) == len(DL.ANCORAS_AESCALA) and _rf10a["values"]["n_flags_true"] == _rf10a["values"]["n_flags"] == esp["n_bandeiras_por_grupo"]["aescala"] and _rf10a["values"]["nomes_ratificados"] is True and _rf10a["values"]["n_nomes"] == len(DL.NOMES_AESCALA) \
    and _rf10a["values"]["n_ancoras"] + len(esp["estrelas_v410"]) == len(FJ["ancoras"]) and not (set(esp["estrelas_v410"]) & set(esp["estrelas_aescala_v410"])), _rf10a["values"]
_rf10f = esp["registros_funcao_v410"]["hms13"]
assert _rf10f["n_checks"] == DL.N_CHECKS_HMS13 and _rf10f["verdict"] == DL.VEREDITO_HMS13_OK and _rf10f["values"]["observed_vector_read"] is False and _rf10f["values"]["le_em_rito"] is False and "caminhos_tocados" not in _rf10f["values"] and _rf10f["values"]["sob_pasta_vedada"] == [] and _rf10f["values"]["com_nome_vedado"] == [] and _rf10f["values"]["n_calibradores"] == DL.HMS13_CAMPOS["calibradores"] and _rf10f["values"]["n_fontes_primarias"] == DL.HMS13_CAMPOS["fontes_primarias"], _rf10f
_rf10h = esp["registros_funcao_v410"]["h0dn"]
assert _rf10h["n_checks"] == DL.N_CHECKS_H0DN and _rf10h["verdict"] == DL.VEREDITO_H0DN_OK and _rf10h["values"]["ramos_vistos"] == [1, 2, 3, 4, 5, 6] and _rf10h["values"]["observed_vector_read"] is False and "caminhos_tocados" not in _rf10h["values"] and _rf10h["values"]["sob_pasta_vedada"] == [] and _rf10h["values"]["com_nome_vedado"] == [], _rf10h
_rf9 = esp["registros_funcao_v409"]["traducao_turing"]   # a traducao HERDADA: as 82 estrelas da v409, os 2 modulos
assert _rf9["values"]["n_ancoras_ok"] == _rf9["values"]["n_ancoras"] == len(esp["estrelas_v409"]) and _rf9["values"]["n_modulos_ok"] == _rf9["values"]["n_modulos"] == len(esp["bundle_v409_sha256"]) and _rf9["values"]["escada"] == [CM["escada"][1]] * 3 and _rf9["verdict"] == esp["vereditos_v409"][DL.D9.FECHO_REGISTRO], _rf9["values"]
_rf8 = esp["registros_funcao_v408"]["tetelestai_terminal"]   # o terminal HERDADO: as 48 estrelas da v408, os 4 modulos
assert _rf8["values"]["n_ancoras_ok"] == _rf8["values"]["n_ancoras"] == len(esp["estrelas_v408"]) and _rf8["values"]["n_modulos_ok"] == _rf8["values"]["n_modulos"] == len(esp["bundle_v408_sha256"]) and _rf8["values"]["escada"] == [CM["escada"][1]] * 3 and _rf8["verdict"] == esp["vereditos_v409"][DL.D8.FECHO_REGISTRO], _rf8["values"]
_rf7 = esp["registros_funcao_v407"]["psion_canto"]   # o psion HERDADO: as 76 estrelas da v407, os 9 modulos, a chave do lema lida do kernel, as chaves iguais as da v409 selada
assert _rf7["values"]["n_ancoras_ok"] == _rf7["values"]["n_ancoras"] == len(esp["estrelas_v407"]) and _rf7["values"]["n_modulos_ok"] == _rf7["values"]["n_modulos"] == len(esp["bundle_v407_sha256"]) and _rf7["values"]["escada"] == [CM["escada"][1]] * 3 and _rf7["values"]["elo_lido_do_kernel"] is True and _feq(_rf7["values"]["chaves"], chaves_v407_esperadas), _rf7["values"]
_rf5 = esp["registros_funcao_v405"]
assert abs(_rf5["ponte"]["values"]["m_derivada_meV"] / esp["m_nu_meV_v404"] - 1.0) <= 1e-12 and abs(_rf5["psion"]["values"]["meia_hbar_omega_meV"] / esp["m_nu_meV_v404"] - 1.0) <= 1e-12 and abs(_rf5["diminuto"]["values"]["E0_eV"] - 1.0) <= 1e-12, "o numero da massa mudou"
assert not any(GF.violacoes(v_) for v_ in _vn.values()), "um veredito novo afirma demais"
assert len(esp["qg_closure_v409_checks"]) == 7 and all(c_[1] is True for c_ in esp["qg_closure_v409_checks"]), esp["qg_closure_v409_checks"]
assert esp["selo_acom"]["perfil"] == "ACOM-INT-C96-Q8" and esp["selo_acom"]["controles"] == [13, True] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == DL.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read())
# o selo da v410 difere do da v409 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410 e registros_v410), as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita) e as que LEEM a chave nova; o ensaio EXPLICA chave por chave
assert ({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v410"} | set(DL.REGISTROS_FUNCAO)) <= set(esp["selo_difere_do_v409_no_ensaio"]) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v409_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))
assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "declaracao_do_operador_v399", "registros_v399", "falsidade_da_inercia_v401", "registros_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "registros_v402",
             "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "registros_v403", "projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "registros_v404", "registros_v405"} | set(SEL_STONES405)) & set(esp["selo_difere_do_v409_no_ensaio"]), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = _arg("--saida", os.path.join(HERE, "ESPERADOS_v410.json"))
if os.path.exists(out):   # backup de BYTES antes de tocar (regra do backup imediato)
    _bk = out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(_bk, "wb").write(open(out, "rb").read()); assert open(_bk, "rb").read() == open(out, "rb").read()
open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v410:", esp["candidato_sha16"], "| vereditos v409 pinados:", len(esp["vereditos_v409"]), "| flags True v409:", len(esp["flags_true_v409"]), "| troca dita (so' numeros):", troca, "| selo_chaves_que_mudam:", selo_chaves_que_mudam,
      "| h0dn: n_pinos %d, ramos %s, veto medido (%d caminhos no ensaio)" % (HV["n_pinos"], HV["ramos_vistos"], pvk["n_caminhos_vistos"]),
      "| a_escala: ancoras %d/%d, flags %d/%d, falas %d/%d, nomes %d/%d | hms13: calibradores %d, fontes %d, embutidos %d (nada de kimi\\ em rito)" % (AV["n_ancoras_ok"], AV["n_ancoras"], AV["n_flags_true"], AV["n_flags"], AV["n_falas_ok"], AV["n_falas"], AV["nomes_declarados"], AV["n_nomes"], FV["n_calibradores"], FV["n_fontes_primarias"], FV["n_embutidos"]))
