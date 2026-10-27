# -*- coding: utf-8 -*-
# regras (lote I) de derivar_encanamento_v401.py: o harness do FECHAR em sandbox (harness_fechar_sandbox_v401.py). ORIGEM v399 (mapa 398 -> 400, 399 -> 401) + as licoes da v400 (as pastas irmas v400 e v399 no sandbox, porque o conferidor roda no pacote do sandbox).
# Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas). O que a v401 muda: o paragrafo NOVO e' o da falsidade (o do testemunho segue como esta); os controles negativos usam os registros da v401 (falsidade, cunhagens_v401); o mapa tem 9 registros (1 rota + 8 anotacoes);
# o diff do kernel traz a pedra FalsidadeDaInercia; o manifesto traz registros_v401, falsidade e readme_paragrafo_falsidade.

_HDR_FECHAR_SB = '''"""harness_fechar_sandbox_v401.py -- roda fechar_v401.py e registrar_mapa_v401.py (o main) num SANDBOX inteiro dentro de pos_rito\\\\harness_saida_v401\\\\fechar_sandbox (nada fora dela e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada
nao sao tocados; o mapa de rotas real e' SO' LIDO).  O que o harness_textos_ensaio_v401.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, a copia do sidecar e do selo, o handoff com os DOIS paragrafos do README/site, o aviso de que o do testemunho segue como esta e a lista do sidecar) e o main do registrar_mapa.
Derivado do harness_fechar_sandbox_v399.py (que rodou na v399), com as licoes da v400.
O sandbox e' uma ARVORE ISOLADA: work\\\\cadeia_de_selo\\\\v401 (pacote com ESPERADOS, CANDIDATO, PINOS_BN, base_v400, insumos (o resultado pinado do Teste da Unica Palavra, que mora na v397, ganha uma COPIA em insumos\\\\fase9 so' no sandbox), quadro_v397 e runtime_quadro_v397, o runtime_v401 e o acom_conferencias_v401,
o APLICADO_AO_CANONICO EMULADO, os recibos do B(n) SINTETICOS) + as pastas irmas v400 e v399 (o delta_v401 importa o delta_v400 e este o delta_v399; o runtime da secao e as seis fontes do operador moram na v400) + nos\\\\ (o Nos EMULADO montado de dry_v401, como no harness dos textos, com o SIDECAR gerado pela funcao do proprio candidato)
+ memory\\\\ (a memoria vazia) + work\\\\cunhagens_13out (as falas do operador). O conferidor REAL roda no proprio pacote do sandbox (SEM -I), onde acha tudo pelo caminho da propria pasta. As copias dos scripts (leitura, textos, fechar) trocam SO' as constantes de caminho (o Nos e a pasta de memoria) por caminhos do sandbox;
o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais e' so' essas linhas).
O que ele prova: fechar_v401.py sai com rc 0 e grava o handoff (guarda P18 limpa) com os DOIS paragrafos do README/site entre os marcadores (o do quadro igual ao das funcoes do quadro sobre o core do sandbox e aprovado por T.verificar_paragrafo_readme; o da falsidade (simulacro) da inercia
igual ao gerado do core e aprovado por T.verificar_paragrafo_falsidade), a frase de que o do testemunho de dois SEGUE COMO ESTA e a lista do sidecar (sha256 e veredito), o handoff do Nos, os dois diffs, o manifesto e o arquivo, e copia o sidecar e o selo para v401_selo; RECUSA (rc 2, sem handoff) sem o recibo do religamento,
com um recibo do B(n) que declara salto, com o resultado pinado adulterado (o paragrafo do quadro nao passa na verificacao contra o resultado), com o numero lido do quadro adulterado, com um numero da falsidade adulterado no core, com a direcao do testemunho invertida (registro da v399 recriado), com uma inscricao de 25/10 rotulada como da gerencia,
sem uma ratificacao, com a errata sem SUPERADA e com o sidecar adulterado ou ausente; registrar_mapa_v401.py (main) monta o JSON com 9 registros (a rota nova e oito anotacoes) e imprime o comando. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v400, como no harness dos textos): a prova e' do CODIGO do fechar, nao de um B(n) real.
uso: python -B -X utf8 harness_fechar_sandbox_v401.py [--manter] [--nao-exigir-refazer]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado; sem a flag EXIGE refazer_out_v401.txt com '== FIM' e mais novo que o ESPERADOS; --nao-exigir-refazer: NAO o exige, o resumo DIZ que a regeneracao nao foi comprovada e vai para
HARNESS_FECHAR_SANDBOX_v401_DEPURACAO_sem_refazer.json -- o nome HARNESS_FECHAR_SANDBOX_v401.json so' nasce na rodada que EXIGE o refazer)"""
'''

_SIBLINGS = '''os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)   # o delta acha as falas do operador em ..\\\\..\\\\cunhagens_13out (a partir da pasta do pacote do sandbox): as quatro de 24/10 (os registros da v399 recriados) e as seis de 25/10
_dlx = importlib.util.spec_from_file_location("delta_v401_h", os.path.join(PKG, "delta_v401.py")); _dm = importlib.util.module_from_spec(_dlx); _dlx.loader.exec_module(_dm)
for _o in list(_dm.VERBATIM_ORIGEM) + list(_dm.VERBATIM_ORIGEM_V401):
    shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
assert len(glob.glob(os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_25out_*.txt"))) == len(ESP["cunhagens"]), "as falas de 25/10 do operador nao estao todas na pasta do sandbox"
# v401 (desvio do molde, dito): as pastas irmas que o delta_v401 e o acom_conferencias_v401 importam por caminho (v400 e, por ela, v399), o runtime da secao e as seis fontes do operador (v400), a pedra e as fontes do estudo (v399), o resultado do Teste da Unica Palavra (v397) e o esboco R3.5 da Bancada (C15): copias de bytes, so' o que eles leem
for _vv, _nomes in (("v400", ("delta_v400.py", "acom_conferencias_v400.py", "runtime_v400.py")), ("v399", ("delta_v399.py", "acom_conferencias_v399.py", "runtime_v399.py"))):
    os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", _vv))
    for _n in _nomes:
        shutil.copyfile(os.path.join(os.path.dirname(PKG), _vv, _n), os.path.join(SB, "work", "cadeia_de_selo", _vv, _n))
    shutil.copytree(os.path.join(os.path.dirname(PKG), _vv, "insumos", "acom"), os.path.join(SB, "work", "cadeia_de_selo", _vv, "insumos", "acom"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "pedra"), os.path.join(SB, "work", "cadeia_de_selo", "v399", "pedra"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v397", "insumos", "fase9"), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "fase9"))
os.makedirs(os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
'''

_NEG_1C = '''# ---- 1c. controles negativos do PARAGRAFO NOVO (a falsidade), da DIRECAO do testemunho (registros da v399 recriados), das cunhagens_v401 e do SIDECAR: o numero da falsidade adulterado no core (a leitura e a porta do paragrafo recusam), a direcao invertida, uma inscricao da gerencia,
# a ratificacao ausente, a errata sem SUPERADA e o sidecar adulterado ou ausente => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); sc_p = os.path.join(NOSS, "um_absoluto_selo_acom.json"); raw_sc = open(sc_p, "rb").read()


def _recusa_com_core(nome_sc, nome_ctl, f):
    cj_ = json.loads(raw_core.decode("utf-8")); f(cj_["core"])
    open(core_p, "wb").write(json.dumps(cj_, ensure_ascii=False).encode("utf-8"))
    rc_, so_, se_ = roda("fechar_v401.py", nome_sc)
    NEG.append({"controle": nome_ctl, "rc": rc_, "recusou": rc_ == 2 and "FECHAR RECUSADO" in so_, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v401-custodia.md"))})
    open(core_p, "wb").write(raw_core)


_recusa_com_core("fechar_falsidade_adulterada", "numero da falsidade adulterado no core (custo minimo)", lambda c: c["falsidade_da_inercia_v401"]["values"].__setitem__("min_cost_t_beta_g", 0.0007))
# a PORTA do paragrafo novo isolada: T.paragrafo_falsidade() da copia do sandbox tem de LEVANTAR com o numero da falsidade adulterado no core (a verificacao compara com os numeros de ESPERADOS)
cj = json.loads(raw_core.decode("utf-8")); cj["core"]["falsidade_da_inercia_v401"]["values"]["min_cost_t_beta_g"] = 0.0007
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
import importlib.util as _iu1
_sp1 = _iu1.spec_from_file_location("textos_sb1", os.path.join(POS, "textos_v401.py")); _t1 = _iu1.module_from_spec(_sp1); _sp1.loader.exec_module(_t1)
try:
    _t1.paragrafo_falsidade(); _levanta1 = False
except AssertionError as _ex1:
    _levanta1 = "nao passou nas verificacoes" in str(_ex1)
NEG.append({"controle": "a porta do paragrafo novo (paragrafo_falsidade, chamada pelo fechar) levanta com o numero da falsidade adulterado", "rc": 2 if _levanta1 else 0, "recusou": _levanta1, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v401-custodia.md"))})
open(core_p, "wb").write(raw_core)
_recusa_com_core("fechar_direcao_invertida", "a direcao do testemunho invertida no core (a IALD como quem testifica do operador; declaracao da v399 recriada)", lambda c: c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"].__setitem__("a_IALD", "testifica do operador"))
_recusa_com_core("fechar_gerencia_na_cunhagem", "uma inscricao de 25/10 rotulada como da gerencia no core (as seis sao falas do operador)", lambda c: c["cunhagens_v401"]["extras"]["autor_de_cada_inscricao"].__setitem__(sorted(c["cunhagens_v401"]["extras"]["autor_de_cada_inscricao"])[0], "gerencia"))
_recusa_com_core("fechar_cadeia_onto", "a cadeia derivada dita [ONTO] no core (chain_status)", lambda c: c["falsidade_da_inercia_v401"].__setitem__("chain_status", "ONTO do operador"))
_recusa_com_core("fechar_hipotese_usada", "H_tau dita usada por teorema no core", lambda c: c["falsidade_da_inercia_v401"]["named_hypothesis"].__setitem__("used_by_a_theorem", True))
_recusa_com_core("fechar_sem_ratificacao", "falta uma das oito ratificacoes no core", lambda c: c["cunhagens_v401"]["extras"]["ratificacoes"].pop())
_recusa_com_core("fechar_errata_sem_superada", "a errata ao lado do adendo sem SUPERADA no core", lambda c: c["cunhagens_v401"]["erratas"][0].__setitem__("agora", "mantida"))
_recusa_com_core("fechar_pedra_fora_do_trio", "a pedra FalsidadeDaInercia fora do trio no core", lambda c: c["kernel_formalization"]["axiom_report"].__setitem__(ESP["teoremas_das_pedras"]["falsidade"], ["propext", "sorryAx"]))
sj = json.loads(raw_sc.decode("utf-8")); sj["objetos"][1]["sha256"] = "0" * 64
open(sc_p, "wb").write(json.dumps(sj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v401.py", "fechar_sidecar_adulterado"); NEG.append({"controle": "o sidecar adulterado (sha256 de um objeto)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v401-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
os.remove(sc_p)
rc, so, se = roda("fechar_v401.py", "fechar_sidecar_ausente"); NEG.append({"controle": "o sidecar ausente do Nos", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v401-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
'''

_2C = '''# ---- 2c. o PARAGRAFO NOVO (a falsidade (simulacro) da inercia) nos dois handoffs gravados: igual ao gerado do core do sandbox, entre os marcadores, aprovado pela verificacao propria (e o do handoff do Nos tambem); o handoff DIZ que o paragrafo do testemunho de dois SEGUE COMO ESTA e LISTA o sidecar (sha256 e veredito); o fechar copiou o sidecar e o selo
_core_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]
import importlib.util as _iu3
_sp3 = _iu3.spec_from_file_location("textos_sb3", os.path.join(POS, "textos_v401.py")); _t3 = _iu3.module_from_spec(_sp3); _sp3.loader.exec_module(_t3)
_par_f_esp = _t3._paragrafo_falsidade_de(_core_s); _msi = _t3.MARC_FAL_INI + "\\n"; _msf = "\\n" + _t3.MARC_FAL_FIM
_sc_sha = fsha(os.path.join(NOSS, "um_absoluto_selo_acom.json")); _sc_ver = rdj(os.path.join(NOSS, "um_absoluto_selo_acom.json"))["veredito"]
_ok_tmn = {}
for _nome, _ptxt in (("memory/handoff-v401-custodia.md", ho), ("nos/HANDOFF_v401_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v401_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v401_CUSTODIA.md")) else "")):
    _i = _ptxt.find(_msi); _j = _ptxt.find(_msf)
    _par = _ptxt[_i + len(_msi):_j] if (_i >= 0 and _j > _i) else ""
    _fa = _t3.verificar_paragrafo_falsidade(_par + "\\n" if _par and not _par.endswith("\\n") else _par, _core_s, ESP) if _par else ["sem o bloco"]
    _ok_tmn[_nome] = {"traz_o_bloco": bool(_par), "igual_ao_gerado_do_core": _par.rstrip("\\n") == _par_f_esp.rstrip("\\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3], "direcao_e_atribuicao": _t3.atribuicao_da_gerencia(_ptxt)[:3],
                     "lista_o_sidecar": ("um_absoluto_selo_acom.json" in _ptxt and _sc_sha in _ptxt and _sc_ver in _ptxt), "diz_que_o_testemunho_segue_como_esta": ("SEGUE COMO ESTÁ" in _ptxt and "handoff-v400-custodia.md" in _ptxt)}
R["etapas"]["paragrafo_falsidade_no_handoff"] = _ok_tmn
_ok_cop = {nm_: (os.path.exists(os.path.join(TOOLS, "v401_selo", nm_)) and fsha(os.path.join(TOOLS, "v401_selo", nm_)) == fsha(os.path.join(NOSS, nm_))) for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json")}
R["etapas"]["sidecar_e_selo_copiados_para_v401_selo"] = _ok_cop
print("  paragrafo novo (a falsidade da inercia) no handoff: %s; sidecar e selo copiados para v401_selo: %s" % ({k: (v["traz_o_bloco"] and v["igual_ao_gerado_do_core"] and not v["falhas_da_verificacao"] and not v["guarda_p18"] and not v["direcao_e_atribuicao"] and v["lista_o_sidecar"] and v["diz_que_o_testemunho_segue_como_esta"]) for k, v in _ok_tmn.items()}, _ok_cop))
for _nome, _v in _ok_tmn.items():
    if not (_v["traz_o_bloco"] and _v["igual_ao_gerado_do_core"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"] and not _v["direcao_e_atribuicao"] and _v["lista_o_sidecar"] and _v["diz_que_o_testemunho_segue_como_esta"]):
        falha("o handoff (%s) nao traz o paragrafo novo da falsidade pronto e aprovado, ou nao lista o sidecar, ou nao diz que o do testemunho segue como esta: %s" % (_nome, _v))
if not all(_ok_cop.values()):
    falha("o fechar nao copiou o sidecar e o selo (byte a byte) para v401_selo: %s" % _ok_cop)
'''

_VEREDITO_SB = '''R["veredito"] = "TUDO PASSOU: o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o da falsidade (simulacro) da inercia pela verificacao propria; diz que o do testemunho de dois segue como esta; e lista o sidecar), os diffs, o manifesto e o arquivo, copia o sidecar e o selo para v401_selo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado, com o numero lido adulterado, com um numero da falsidade adulterado, com a direcao do testemunho invertida, com uma inscricao rotulada como da gerencia, sem uma ratificacao, com a errata sem SUPERADA, com a pedra fora do trio e com o sidecar adulterado ou ausente; o registrar_mapa monta o registro (1 rota e 8 anotacoes)" if R["tudo_passou"] else "NAO PASSOU (ver problemas)"
'''

entrada("pos_rito/harness_fechar_sandbox_v399.py", origem="v399", autoral=True, regras=[
    entre('"""harness_fechar_sandbox_v401.py -- roda fechar_v401.py', "import glob, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, time", _HDR_FECHAR_SB, "docstring do harness do fechar"),
    ("\"kernel_modulos_novos_v401.json\", \"delta_v401.py\"", "\"kernel_modulos_novos_v401.json\", \"pedra_sha16_da_ordem.txt\", \"delta_v401.py\"", 1),
    entre('os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)   # o delta acha as falas', 'open(os.path.join(PKS, "rito_horarios_v401.txt")', _SIBLINGS, "falas de 24 e 25/10 e as pastas irmas v400 e v399 no sandbox"),
    entre("# ---- 1c. controles negativos do PARAGRAFO NOVO", "for n in NEG:\n    print(\"  controle negativo do fechar:", _NEG_1C, "controles negativos do paragrafo novo, da direcao, das cunhagens e do sidecar"),
    ('os.path.join(TOOLS, "v401_kernel", "pedras", "TGLExt_Testemunho.lean")', 'os.path.join(TOOLS, "v401_kernel", "pedras", "TGLExt_FalsidadeDaInercia.lean")', 1),
    ('"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/Testemunho.lean" in dk)', '"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/FalsidadeDaInercia.lean" in dk)', 1),
    ('if not ("novos (1)" in dk and "TGLExt/Testemunho.lean" in dk):', 'if not ("novos (1)" in dk and "TGLExt/FalsidadeDaInercia.lean" in dk):', 1),
    ('for k_ in ("registros_v399", "base_v400", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_testemunho", "sidecar_acom"):', 'for k_ in ("registros_v401", "registros_v399", "falsidade", "base_v400", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_falsidade", "sidecar_acom"):', 1),
    entre("# ---- 2c. o PARAGRAFO NOVO (o testemunho de dois)", "# ---- 3. o registrar_mapa (main)", _2C, "o paragrafo novo da falsidade nos dois handoffs"),
    ("ok_m = (rc == 0 and len(reg) == 5 and", "ok_m = (rc == 0 and len(reg) == 9 and", 1),
    ("# ---- 3. o registrar_mapa (main)", "# ---- 3. o registrar_mapa (main): 9 registros (1 rota nova e 8 anotacoes)", 1),
    entre('R["veredito"] = "TUDO PASSOU: o fechar grava o handoff', 'R["nota"] = "recibos do B(n) SINTETICOS', _VEREDITO_SB, "o veredito do harness do fechar"),
])
