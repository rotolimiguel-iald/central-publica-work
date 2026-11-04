# -*- coding: utf-8 -*-
"""_adapt_harness_fechar_v407.py -- adapta harness_fechar_sandbox_v407.py (subida mecanica da v406) ao conteudo da v407 (O PSION, O CANTO E O PAR): a V que o fechar usa (reg406d, fecho406, ancoras406, bandeiras406, bundle406, chaves406 ao lado das chaves da v407),
as pastas irmas do delta (v405 tambem), os arquivos de entrada do delta_v407 no sandbox (o manifesto do teste (d), as nove pedras, as falas de 03/11), o topico novo e os controles negativos do fechar sobre o psion_canto_v407, o fechamento_v406 herdado e cunhagens_v407.
Cada troca e' EXATA e conta (assert). Uso: python -B -X utf8 _adapt_harness_fechar_v407.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adaptar_pos_rito_v407 as M

NOME = "harness_fechar_sandbox_v407.py"

MAN_CONST = r'''R = {"inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "problemas": [], "etapas": {}}
# v407: as chaves do MANIFESTO de incorporacao que fechar_v407.py (B1a) grava (nomes versionados: *_v407 = os registros desta versao; *_v406 = os HERDADOS da v406; *_v405 = os treze da v406 selada, e assim por diante)
MAN_CHAVES = ("registros_v407", "registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v407", "registros_funcao_v406", "ancoras_v407", "ancoras_v406", "bandeiras_v407", "bandeiras_v406", "chaves_v407", "chaves_v406", "f2b_errata", "bandeiras_do_gate_recriado",
              "funcoes_v406_recriadas", "funcoes_v405_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas", "pedras_v406_como_registro", "pedras_v405_como_registro", "falsidade_v401", "base_v406", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_v407", "sidecar_acom", "fila_da_memoria")
'''

NEW_CTL_FECHO = r'''_recusa_com_core("fechar_psion_valor_adulterado", "o numero de modulos ok do psion_canto_v407 adulterado no core (8 de 9)", lambda c: c["psion_canto_v407"]["values"].__setitem__("n_modulos_ok", 8))
_recusa_com_core("fechar_fecho406_valor_adulterado", "o numero de modulos ok do fechamento_v406 (herdado) adulterado no core (300 de 301)", lambda c: c["fechamento_v406"]["values"].__setitem__("n_modulos_ok", 300))
_recusa_com_core("fechar_chave_do_lema_false", "a chave do lema (linked_to_the_corner_by_a_lemma) de volta a literal False no core", lambda c: c["testemunha_estatica_v396"]["fock_face"].__setitem__("linked_to_the_corner_by_a_lemma", False))
_recusa_com_core("fechar_fecho_chave_false", "a chave rede_fock_v394.whole_certificate_inhabited de volta a False no core (o literal)", lambda c: c["rede_fock_v394"].__setitem__("whole_certificate_inhabited", False))
_recusa_com_core("fechar_psion_frase_proibida", "uma frase proibida nos limites do psion_canto_v407", lambda c: c["psion_canto_v407"]["limites"].append("o unico autovetor da luz"))
'''

NEW_CTL_CUNH = r'''_recusa_com_core("fechar_inscricao_nao_embutida", "uma inscricao de 03/11 deixou de estar embutida no core (cunhagens_v407)", lambda c: list(c["cunhagens_v407"]["verbatim"].values())[0].__setitem__("embedded_ok", False))
_recusa_com_core("fechar_sem_errata", "falta uma das erratas E18 a E20 (em nome da gerencia) no core", lambda c: c["cunhagens_v407"]["erratas"].pop())
_recusa_com_core("fechar_sem_decisao", "falta uma das decisoes D41 a D47 da gerencia no core", lambda c: c["cunhagens_v407"]["extras"]["decisoes"].pop("D47"))
_recusa_com_core("fechar_leitura_sem_onto", "a leitura de 03/11 dita [REAL] no core (e' ONTO)", lambda c: c["cunhagens_v407"]["extras"]["leituras"].__setitem__("estatuto", "[REAL]"))
_recusa_com_core("fechar_cunhagens_v406_sem_e20", "a errata E20 ao lado de cunhagens_v406 (herdada) ausente do core", lambda c: c["cunhagens_v406"]["erratas"].pop())
'''

NEW_CTL_ANC = r'''for _nm, _ia in (("lema", list(_dm.ANCORAS).index(_dm.ANCORA_LEMA)), ("par", list(_dm.ANCORAS).index(_dm.ANCORA_PAR))):
    _recusa_com_core("fechar_ancora_%s_fora_do_trio" % _nm, "a ancora %s fora do trio no core" % _nm, lambda c, _ia=_ia: c["kernel_formalization"]["axiom_report"].__setitem__(list(_dm.ANCORAS)[_ia], ["propext", "sorryAx"]))
'''

COPIAS_EXTRA = r'''# v407 (desvio do molde, dito): o delta_v407 PINA POR ASSERT o manifesto da parametrizacao do teste (d) (D_TESTE_MANIFESTO, sha16 da ordem): o sandbox o leva (copia de bytes) na mesma posicao relativa, e leva tambem as fontes dos nove modulos (pedra\) e as falas de 03/11 e de todas as versoes anteriores (todo VERBATIM_ORIGEM* do delta)
_man_d_sb = os.path.join(SB, "work", os.path.relpath(_dm.D_TESTE_MANIFESTO, _dm.WK)); os.makedirs(os.path.dirname(_man_d_sb), exist_ok=True); shutil.copyfile(_dm.D_TESTE_MANIFESTO, _man_d_sb)
for _p9 in _dm.PEDRAS_V407:
    shutil.copyfile(_p9["src"], os.path.join(PKS, "pedra", os.path.basename(_p9["src"])))
for _nm_v in [n_ for n_ in dir(_dm) if n_.startswith("VERBATIM_ORIGEM") and isinstance(getattr(_dm, n_), list)]:
    for _o in getattr(_dm, _nm_v):
        shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
'''


def rodar(M_=None):
    M_ = M_ or M
    t, crlf, raw = M_.le(NOME)
    if M_.pula(NOME, t):
        return
    t = M_.tira_cabecalho(t)
    # ---- docstring e textos
    t = M_.sub(t, "o da v407 (o fechamento)", "o da v407 (o psion, o canto e o par)", 2)
    t = M_.sub(t, "(com os 301 modulos novos)", "(com os 9 modulos novos)")
    t = M_.sub(t, "os diffs (os 301 modulos novos)", "os diffs (os 9 modulos novos)")
    t = M_.sub(t, "com um numero do fechamento_v406 adulterado", "com um numero do psion_canto_v407 ou do fechamento_v406 (herdado) adulterado")
    t = M_.sub(t, "uma errata ou uma decisao a menos, com uma pedra", "uma errata ou uma decisao a menos, com uma pedra") if t.count("uma errata ou uma decisao a menos, com uma pedra") == 1 else t
    # ---- constantes do manifesto
    t = M_.sub(t, 'R = {"inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "problemas": [], "etapas": {}}\n', MAN_CONST)
    # ---- STUBs da fila e do fechar
    t = M_.sub(t, "TOPICO_NOVO = 'v407-selada-o-fechamento.md'", "TOPICO_NOVO = 'v407-selada-o-psion-o-canto-e-o-par.md'")
    t = M_.sub(t, "TOPICO_NOVO = \\'v407-selada-o-fechamento.md\\'", "TOPICO_NOVO = \\'v407-selada-o-psion-o-canto-e-o-par.md\\'")
    t = M_.sub(t, "REGS = 'fechamento_v406 cunhagens_v406 kh_n1_cobertura_v406'", "REGS = 'psion_canto_v407 cunhagens_v407 kh_n1_cobertura_v407'")
    t = M_.sub(t, "'reg407': {'cunhagens_v406': {'ok': True}}, 'reg406c': {'cunhagens_v405': {'ok': True}}, 'fecho': {'ok': True}, 'ancoras': {}, 'bandeiras': {}, 'chaves': {}, 'fun406c': {},",
               "'reg407': {'cunhagens_v407': {'ok': True}}, 'reg406d': {'cunhagens_v406': {'ok': True}}, 'reg406c': {'cunhagens_v405': {'ok': True}}, 'reg406b': {}, 'fecho': {'ok': True}, 'fecho406': {'ok': True}, 'ancoras': {}, 'ancoras406': {}, 'bandeiras': {}, 'bandeiras406': {}, 'bundle406': {}, 'chaves': {}, 'chaves406': {}, 'fun406c': {}, 'fun406b': {},")
    # ---- recibos sinteticos do B(n)
    t = M_.sub(t, '"B%d-v407-20261026-R1" % n', '"B%d-v407-20261103-R1" % n')
    # ---- pastas irmas do delta (v405 tambem), pedras seladas, falas
    t = M_.sub(t, 'for _vv in ("v406", "v404", "v403", "v402", "v401", "v400", "v399"):', 'for _vv in ("v406", "v405", "v404", "v403", "v402", "v401", "v400", "v399"):')
    t = M_.sub(t, 'for _vp in ("v406", "v404", "v403", "v402", "v401", "v399"):', 'for _vp in ("v406", "v405", "v404", "v403", "v402", "v401", "v399"):')
    t = M_.sub(t, "os.makedirs(os.path.join(PKS, \"pedra\"), exist_ok=True); shutil.copyfile(_dm.TESTEMUNHA[\"src\"], os.path.join(PKS, \"pedra\", os.path.basename(_dm.TESTEMUNHA[\"src\"])))\n",
               "os.makedirs(os.path.join(PKS, \"pedra\"), exist_ok=True); shutil.copyfile(_dm.TESTEMUNHA[\"src\"], os.path.join(PKS, \"pedra\", os.path.basename(_dm.TESTEMUNHA[\"src\"])))\n")
    t = M_.sub(t, 'assert len(glob.glob(os.path.join(SB, "work", "cunhagens_13out", "*OPERADOR_02nov_*.txt"))) == len(ESP["cunhagens"]), "as falas de 02/11 do operador nao estao todas na pasta do sandbox"',
               NEXT_ASSERT := 'assert len(glob.glob(os.path.join(SB, "work", "cunhagens_13out", "*OPERADOR_03nov_*.txt"))) == len(ESP["cunhagens"]), "as falas de 03/11 do operador nao estao todas na pasta do sandbox"')
    t = M_.sub(t, NEXT_ASSERT + "   # v407: as falas desta versao sao as de 02/11 (as de 30/10 a 01/11 vao junto, para o delta herdado)\n", NEXT_ASSERT + "   # v407: as falas desta versao sao as de 03/11 (as de 02/11 e as anteriores vao junto, para o delta herdado)\n" + COPIAS_EXTRA)
    # ---- controles negativos do fechar
    t = M_.entre_linhas(t, '_recusa_com_core("fechar_fecho_valor_adulterado"', '_recusa_com_core("fechar_psion_adulterado"', NEW_CTL_FECHO)
    t = M_.sub(t, 'cj = json.loads(raw_core.decode("utf-8")); cj["core"]["fechamento_v406"]["values"]["n_modulos_ok"] = 300', 'cj = json.loads(raw_core.decode("utf-8")); cj["core"]["psion_canto_v407"]["values"]["n_modulos_ok"] = 8')
    t = M_.sub(t, "levanta com o numero de modulos do fechamento_v406 adulterado", "levanta com o numero de modulos do psion_canto_v407 adulterado")
    t = M_.entre_linhas(t, '_recusa_com_core("fechar_inscricao_nao_embutida"', '_recusa_com_core("fechar_pedra_v403_adulterada"', NEW_CTL_CUNH)
    t = M_.entre_linhas(t, 'for _nm, _ia in (("topo", 0), ("certificado", 2)):', 'sj = json.loads(raw_sc.decode("utf-8")); sj["objetos"][1]["sha256"] = "0" * 64', NEW_CTL_ANC)
    # ---- as chaves do manifesto
    t = M_.sub(t, 'for k_ in ("registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v407", "ancoras_v407", "bandeiras_v407", "chaves_v407", "f2b_errata", "bandeiras_do_gate_recriado", "funcoes_v406_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas", "pedras_v406_como_registro", "falsidade_v401", "base_v406", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_v407", "sidecar_acom", "fila_da_memoria"):',
               "for k_ in MAN_CHAVES:")
    t = M_.sub(t, 'all(k_ in man_ for k_ in ("registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v407", "ancoras_v407", "bandeiras_v407", "chaves_v407", "f2b_errata", "bandeiras_do_gate_recriado", "falsidade_v401", "readme_paragrafo", "readme_paragrafo_v407", "sidecar_acom", "fila_da_memoria", "b3", "diffs"))',
               "all(k_ in man_ for k_ in MAN_CHAVES if k_ not in ('base_v406', 'insumos_sha16', 'conferidor', 'pedras_v406_como_registro', 'pedras_v405_como_registro', 'funcoes_v406_recriadas', 'funcoes_v405_recriadas', 'funcoes_v403_recriadas', 'funcoes_v402_recriadas'))")
    # ---- textos de impressao e veredito
    t = M_.sub(t, "paragrafo novo (o fechamento) e nota ao lado do da v406 no handoff:", "paragrafo novo (o psion, o canto e o par) e nota ao lado dos anteriores no handoff:")
    t = M_.sub(t, "com a leitura da v407 dita REAL, com uma pedra selada da v406 adulterada", "com a leitura de 03/11 dita REAL, com a chave do lema de volta a False, com uma pedra selada da v406 adulterada")
    t = M_.sub(t, "com um numero da Ponte da Massa, do Ponto Zero do Psion, da errata de F2b ou do gate adulterado", "com um numero do psion_canto_v407, do fechamento_v406 herdado, do Ponto Zero do Psion, da errata de F2b ou do gate adulterado")
    M_.grava(NOME, t, crlf, raw)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rodar(M)
