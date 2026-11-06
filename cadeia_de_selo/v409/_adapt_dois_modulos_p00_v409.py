# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_p00_v409.py -- (claude-construtor-v409, 05/11/2026) o p00 da v409 passa ao bundle de DOIS modulos (TraducaoTuring refeita da R9 + ParNaFaceDeFock; AO LADO mais novo do DESENHO_v409.md):
a raiz com os dois imports, 82 ancoras (as principais lidas do DL), 13 falas (de tres, so' o trecho), e a conferencia da pedra feita para CADA uma das duas (origem == pino do bundle; v409\\pedra == insumos == embutida no
candidato == sandbox == ESPERADOS == BUNDLE). Nenhuma conferencia relaxada: os numeros sobem com o conteudo, as igualdades ficam."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("p00_precondicoes_v409.py")
a.troca("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a v409: 1 modulo (TraducaoTuring), 62 ancoras (oito principais), 10 falas (de duas, so' o trecho da D59, a fonte inteira so' por sha256);",
        "# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a v409: 2 modulos (TraducaoTuring, refeita da R9, e ParNaFaceDeFock; ordem «tudo na v409»), 82 ancoras (13 principais), 13 falas (de tres, so' o trecho; a fonte inteira so' por sha256);")
a.troca("(A traducao as classes de Turing: bundle de 1 modulo em TGLExt/, registro traducao_turing_v409, 62 ancoras, 10 falas de 05/11, de duas so' o trecho da D59; nenhuma chave antiga muda).",
        "(A traducao as classes de Turing e o par na face de Fock: bundle de 2 modulos em TGLExt/, registro traducao_turing_v409, 82 ancoras, 13 falas de 05/11, de tres so' o trecho; nenhuma chave antiga muda).")
a.troca('''raiz_ok_ = imports_ == ["import " + m_ for m_ in DL.BUNDLE_MODS] and len(imports_) == DL.N_BUNDLE == 1''',
        '''raiz_ok_ = imports_ == ["import " + m_ for m_ in DL.BUNDLE_MODS] and len(imports_) == DL.N_BUNDLE == 2''')
a.troca('''cond_ = bool(nov_ == list(DL.BUNDLE_RELS) and len(bf_) == DL.N_BUNDLE == 1 and''', '''cond_ = bool(nov_ == list(DL.BUNDLE_RELS) and len(bf_) == DL.N_BUNDLE == 2 and''')
a.troca('''and len(vb_) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 == 12 and set(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409.values())''',
        '''and len(vb_) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 == 13 and set(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409.values())''')
a.troca('''return bool(len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 62 == len(fj_["ancoras"])''', '''return bool(len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 82 == len(fj_["ancoras"])''')
a.troca('''dep("as 62 ancoras (#print axioms deixados pela autora das provas, lidos da fonte de origem, nunca digitados): DL.ANCORAS == o FLAGS_v409.json == o n_axiomas_das_ancoras do candidato; cada uma no modulo do bundle e so' no trio; as oito ancoras principais (p_igual_np_no_modo_selecao, a_traducao, a_trava_no_nome, a_fita_e_o_hamiltoniano_oculto, z_e_o_modo_leitor, a_fita_sem_escala, o_pai_da_mentira, a_identidade_performada) estao entre elas, a primeira e' a ancora principal; as bandeiras novas somam n_por_modulo", {}, _ancoras_ok)''',
        '''dep("as 82 ancoras dos DOIS modulos (#print axioms deixados pela autora das provas, lidos da fonte de origem, nunca digitados): DL.ANCORAS == o FLAGS_v409.json == o n_axiomas_das_ancoras do candidato; cada uma no modulo do bundle e so' no trio; as %d ancoras principais (%s) estao entre elas, a primeira e' a ancora principal; as bandeiras novas somam n_por_modulo" % (len(DL.ANCORAS_PRINCIPAIS), ", ".join(n_.split(".")[-1] for n_ in DL.ANCORAS_PRINCIPAIS)), {}, _ancoras_ok)''')
a.troca('''== len(CM["cunhagens"]) == DL.N_FALAS_V409 == 12, {"embutidas": len(_cong["arquivos"]),''', '''== len(CM["cunhagens"]) == DL.N_FALAS_V409 == 13, {"embutidas": len(_cong["arquivos"]),''')
a.troca('''chk("as 12 falas de 05/11 (todas do operador; de tres, so' o trecho: duas pela D59, uma pelo aviso operacional):''', '''chk("as 13 falas de 05/11 (todas do operador; de tres, so' o trecho: duas pela D59, uma pelo aviso operacional):''')
a.troca('''o manifesto traz exatamente as 12 entradas cunhagens/ e cada uma == o arquivo",''', '''o manifesto traz exatamente as 13 entradas cunhagens/ e cada uma == o arquivo",''')
a.troca('''len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V409 == 12 and len(_vb12) == DL.N_FALAS_V409''', '''len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V409 == 13 and len(_vb12) == DL.N_FALAS_V409''')
a.troca('''dep("[v408] a conferencia de citacoes conferiu a docstring da pedra TraducaoTuring (zero reprovada;''', '''dep("[v408] a conferencia de citacoes conferiu as docstrings das pedras da v409 (zero reprovada;''')
# a conferencia da pedra para CADA uma das duas (a da TraducaoTuring fica; a da ParNaFaceDeFock entra com a mesma cadeia de igualdades)
_ANCORA_PEDRA = '''ML_ = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")'''
a.troca(_ANCORA_PEDRA, '''for _p0 in [p_ for p_ in DL.PEDRAS_V409 if p_["rel"] != DL.TESTEMUNHA["rel"]]:   # (v409, dois modulos) a OUTRA pedra: a mesma cadeia de igualdades da TraducaoTuring
    dep("a %s (a segunda pedra da v409, ordem «tudo na v409»): a fonte de origem (a copia duravel em v409\\\\insumos) == o pino do bundle (sha256_origem); a copia normalizada v409\\\\pedra == a copia duravel pinada (insumos\\\\%s_embutida.lean) == a EMBUTIDA no candidato == a do sandbox == o pino dos ESPERADOS (bundle_sha256) == o sha256 do BUNDLE_v409.json" % (_p0["name"], _p0["name"]), {"ESPERADOS_v409.json": ESP},
        lambda _p0=_p0: (sha(rd(_p0["origem"])) == DL.BUNDLE_POR_REL[_p0["rel"]]["sha256_origem"] == _p0["sha256_origem"]
                         and sha(rd(_p0["src"])) == sha(rd(os.path.join(HERE, "insumos", "%s_embutida.lean" % _p0["name"]))) == sha(E1[_p0["rel"]].encode("utf-8")) == sha(rd(os.path.join(KS, *_p0["rel"].split("/")))) == ESP["bundle_sha256"][_p0["rel"]] == DL.BUNDLE_POR_REL[_p0["rel"]]["sha256"], sha(rd(_p0["origem"]))[:16]))
''' + _ANCORA_PEDRA)
a.grava()
