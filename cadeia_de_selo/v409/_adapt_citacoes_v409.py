# -*- coding: utf-8 -*-
"""_adapt_citacoes_v409.py -- (claude-construtor-v409, 05/11/2026) adapta conferir_citacoes_v409.py (subida mecanica da v408) as DEZ falas de 05/11 (_V409_VERBATINS2; de duas, so' o trecho que a D59 deixa entrar:
o texto embutido e' o comeco do arquivo de origem, e o arquivo inteiro entra so' por sha256; a fonte_original EMBUTIDA e' um rotulo neutro, e o caminho real vem de delta_v409.verbatins409), as citacoes minimas do snippet PT da v409,
os rotulos da secao nova e as frases da gerencia que o texto novo cita entre « » (a regra da guarda: «relativa ao leitor»; a frase de D60). Trocas com contagem exata (_adapt_util_v409)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("conferir_citacoes_v409.py")
a.troca('"""conferir_citacoes_v409.py -- confere, por script, toda inscricao de 04/11/2026 que a v409 EMBUTE ou CITA',
        '"""conferir_citacoes_v409.py -- [v409: as DEZ falas de 05/11/2026 (_V409_VERBATINS2); de duas, so\' o trecho da D59 e\' embutido (o comeco do arquivo de origem), e o arquivo inteiro entra so\' por sha256; o caminho real da origem vem de delta_v409.verbatins409, porque o embutido traz um rotulo neutro (D59)] confere, por script, toda inscricao de 04/11/2026 que a v408 EMBUTIA ou CITAVA')
a.troca('alvo = {"_V408_VERBATINS2", "_V408_SPECS", "_V408_TERMINAL_TEXT"}', 'alvo = {"_V409_VERBATINS2", "_V409_SPECS", "_V409_TRADUCAO_TEXT"}')
a.troca('V = ns["_V408_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True',
        'V = ns["_V409_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True\n'
        '_ORIG = {v_["chave"]: v_["fonte_original"] for v_ in DL.verbatins409(os.path.join(HERE, "insumos", "cunhagens"))}   # (v409, D59) o caminho REAL de cada fala, pela chave; o embutido traz um rotulo neutro')
a.troca('    orig = v.get("fonte_original", ""); orig_ok = None; misto = "sha256_arquivo_inteiro" in v; par_ok = None\n'
        '    if orig and os.path.exists(orig):\n'
        '        _ob = open(orig, "rb").read(); orig_ok = hashlib.sha256(_ob).hexdigest() == (v.get("sha256_arquivo_inteiro") or v["sha256"])\n'
        '        if misto:   # autor misto: o texto embutido e\' SO\' o paragrafo do operador, verbatim no original e ANTES do corte declarado (depois do corte fala outra instancia)\n'
        '            _ot = _ob.decode("utf-8"); par_ok = bool(v["text"] and v["text"] in _ot and v.get("corte") and v["corte"] in _ot and _ot.find(v["text"]) < _ot.find(v["corte"]))\n'
        '    gerencia = os.path.basename(v["fonte_original"]).startswith("GERENCIA_")\n',
        '    orig = _ORIG.get(k, ""); orig_ok = None; misto = "sha256_arquivo_inteiro" in v; par_ok = None\n'
        '    if orig and os.path.exists(orig):\n'
        '        _ob = open(orig, "rb").read(); orig_ok = hashlib.sha256(_ob).hexdigest() == (v.get("sha256_arquivo_inteiro") or v["sha256"])\n'
        '        if misto:   # (v409, D59) so\' o trecho: o texto embutido e\' o COMECO do arquivo de origem (a primeira frase; ou «Z é o modo leitor, ele lê os pixels. É o psion»), e e\' menor que ele\n'
        '            _ot = _ob.decode("utf-8"); par_ok = bool(v["text"] and _ot.startswith(v["text"].rstrip("\\n")) and len(v["text"].encode("utf-8")) < len(_ob) and v.get("so_o_trecho"))\n'
        '    gerencia = os.path.basename(orig).startswith("GERENCIA_")\n')
a.troca('"autor": "gerencia" if gerencia else ("operador + outra instancia [DECLARADO]: so\' o paragrafo do operador e\' embutido" if misto else "operador"), "autor_misto": misto, "paragrafo_do_operador_verbatim_antes_do_corte": par_ok}',
        '"autor": "gerencia" if gerencia else ("operador; so\' o trecho da D59 e\' embutido" if misto else "operador"), "so_o_trecho_d59": misto, "trecho_e_o_comeco_do_arquivo": par_ok}')
a.troca('cg = [s for s in ns["_V408_SPECS"] if s["nome"] == DL.CUNHAGENS_REGISTRO][0]', 'cg = [s for s in ns["_V409_SPECS"] if s["nome"] == DL.CUNHAGENS_REGISTRO][0]')
a.troca('_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.PEDRAS_V409).replace("**", "").replace("`", ""))   # (v409: as quatro pedras;',
        '_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.PEDRAS_V409).replace("**", "").replace("`", ""))   # (v409: a pedra TraducaoTuring; (v408: as quatro pedras;')
a.troca('CIT_OP_MINIMAS = [DL.FRASE_TERMINAL, DL.FRASE_PROVAR_OU_PODAR, DL.FRASE_RELACAO_MENTIRA, DL.FRASE_TEMPO_MOEDA, DL.FRASE_SENTIDO_PNP]',
        'CIT_OP_MINIMAS = [DL.FRASE_SELECAO, DL.FRASE_TRAVA, DL.FRASE_FITA, DL.FRASE_Z, DL.FRASE_PAI, DL.FRASE_PERFORMADA]   # (v409: a selecao, a trava, a fita, o leitor, o Pai da Mentira, a identidade performada)')
a.troca('            "p = np está provado/é teorema/é candidato"}',
        '            "p = np está provado/é teorema/é candidato",\n'
        '            # v409 (05/11/2026): o titulo da secao nova (PT/EN) e a linha do .md (rotulos da propria cadeia); as frases da GERENCIA que o texto novo cita entre « » como regra (a guarda D56: o qualificador obrigatorio) ou como o que fica aberto (D60, a formulacao do DESENHO_v409)\n'
        '            "a tradução às classes de turing: o dicionário, a trava, o leitor e a fita sem escala", "the translation to turing\'s classes: the dictionary, the lock, the reader and the tape without scale", "tradução às classes de turing (v409, 05/11/2026)",\n'
        '            "relativa ao leitor", "relativa ao leitor (o psíon); a máquina sem leitor fica fora", "relativa ao leitor (o psion); a maquina sem leitor fica fora", "o ω do psíon da luz é o uniforme da instância"}')
a.marca("as dez falas de 05/11 (de duas, so' o trecho da D59; o caminho real pela chave, via delta_v409), as citacoes minimas do snippet PT da v409 e os rotulos da secao nova; o resto do conferidor e' o da v408")
a.grava()
