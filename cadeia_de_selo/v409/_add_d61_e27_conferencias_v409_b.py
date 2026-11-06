# -*- coding: utf-8 -*-
"""_add_d61_e27_conferencias_v409_b.py -- (claude-construtor-v409, 05/11/2026) a CONTINUACAO da parte 2 (_add_d61_e27_conferencias_v409.py parou no harness dos textos: o que ele espera da mensagem
das decisoes aparece TRES vezes, nao duas; as partes ate' a leitura do pos-rito ja' estavam gravadas). Daqui em diante, as mesmas trocas, com a contagem certa: o harness, o mapa, os textos do pos-rito e o rotulo do conferidor de citacoes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("pos_rito/harness_textos_ensaio_v409.py")
a.troca('espera="cunhagens_v409: as erratas E24 a E26"', 'espera="cunhagens_v409: as erratas E24 a E27"', n=4)
a.troca('espera="cunhagens_v409: as decisoes D55 a D60"', 'espera="cunhagens_v409: as decisoes D55 a D61"', n=3)
a.grava()
a = Arq("pos_rito/registrar_mapa_v409.py")
a.troca('''    assert n_trecho == 2, "a v409 tem exatamente duas falas de que so' o trecho entra (D59)"''', '''    assert n_trecho == len(DL_.VERBATIM_SO_O_TRECHO) == 3, "a v409 tem exatamente tres falas de que so' o trecho entra (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional)"''')
a.troca('''all(("D%d" % i) in dec for i in range(55, 61)), "faltam decisoes D55 a D60 no registro"''', '''all(("D%d" % i) in dec for i in range(55, 62)), "faltam decisoes D55 a D61 no registro"''')
a.troca('''    assert sorted(E) == ["E24", "E25", "E26"], "as erratas do registro nao sao E24 a E26"''', '''    assert sorted(E) == ["E24", "E25", "E26", "E27"], "as erratas do registro nao sao E24 a E27"''')
a.troca("as erratas E24 a E26 e as decisoes D55", "as erratas E24 a E27 e as decisoes D55")
a.troca("de %d delas so' o trecho que a D59 deixa entrar;", "de %d delas so' o trecho (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional);")
a.grava()

# ------------------------------------------------------------------------------------------------ o pos-rito: os textos (o fragmento novo; o textos_v409.py e' REMONTADO pelo montar_textos_v409.py)
a = Arq("pos_rito/textos_v409_novo.pysnip")
a.troca('''        assert sum(1 for d in out.values() if d["trecho"]) == 2, "a v409 tem exatamente duas inscricoes so' com o trecho (D59)"''',
        '''        assert sum(1 for d in out.values() if d["trecho"]) == len(_dl().VERBATIM_SO_O_TRECHO) == 3, "a v409 tem exatamente tres inscricoes so' com o trecho (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional)"''')
a.troca('''"z": _sha_por("z_e_o_modo_leitor"), "clay": _sha_por("clay_eu_sou"), "pai": _sha_por("nome_proprio_pai_da_mentira"), "performada": _sha_por("identidade_performada")}''',
        '''"z": _sha_por("z_e_o_modo_leitor"), "clay": _sha_por("clay_eu_sou"), "pai": _sha_por("nome_proprio_pai_da_mentira"), "performada": _sha_por("identidade_performada"),
          "sorry": _sha_por("o_dispositivo_e_o_no_sorry"), "ratifica": _sha_por("d61_ratificada")}''')
a.troca('''("z", DL_.N_Z), ("clay", DL_.N_CLAY), ("pai", DL_.N_PAI), ("performada", DL_.N_PERFORMADA))), "os sha16 das falas != os que a ordem da gerencia deu"''',
        '''("z", DL_.N_Z), ("clay", DL_.N_CLAY), ("pai", DL_.N_PAI), ("performada", DL_.N_PERFORMADA), ("sorry", DL_.N_SORRY), ("ratifica", DL_.N_RATIFICA_D61))), "os sha16 das falas != os que a ordem da gerencia deu"''')
a.troca('''de {nt} delas só o trecho que a D59 deixa entrar é embutido e citável, e o arquivo inteiro entra só por sha256; nenhuma é da gerência); "
             "as erratas E24 a E26 e a dos pisos (em nome próprio da gerência c1); as decisões D55 a D60; as leituras e as ressalvas ({nck} checagens, todas passaram)",''',
        '''de {nt} delas só o trecho é embutido e citável, de duas pela D59 e de uma, a ratificação da D61, porque o resto é aviso operacional, e o arquivo inteiro entra só por sha256; nenhuma é da gerência); "
             "as erratas E24 a E27 e a dos pisos (em nome próprio da gerência c1); as decisões D55 a D61 (a D61, a leitura jurídica do kernel, ratificada pelo operador); as leituras e as ressalvas ({nck} checagens, todas passaram)",''')
a.troca('''    assert all(k in ds for k in ks), "as decisoes D55 a D60 nao estao no registro cunhagens_v409"''', '''    assert all(k in ds for k in ks), "as decisoes D55 a D61 nao estao no registro cunhagens_v409"''')
a.troca('''        return _f("{n} inscrições embutidas por sha256 (todas falas do operador; de {nt} delas só o trecho que a D59 deixa entrar) — a ordem da tradução `{t}`; as respostas às perguntas nas quatro línguas `{r}`, `{tr}`, `{fi}`, `{z}`, `{c}`, `{p}`, `{pe}`; a ordem da v409 e a ratificação dos nomes `{o}`",
                  n=len(fl), nt=d["n_trecho"], t=ss["traducao"], r=ss["resposta"], tr=ss["trava"], fi=ss["fita"], z=ss["z"], c=ss["clay"], p=ss["pai"], pe=ss["performada"], o=ss["ordem"])''',
        '''        return _f("{n} inscrições embutidas por sha256 (todas falas do operador; de {nt} delas só o trecho: duas pela D59, uma pelo aviso operacional) — a ordem da tradução `{t}`; as respostas às perguntas nas quatro línguas `{r}`, `{tr}`, `{fi}`, `{z}`, `{c}`, `{p}`, `{pe}`; a ordem da v409 e a ratificação dos nomes `{o}`; a leitura jurídica do kernel `{so}` e a ratificação dela `{ra}` (D61)",
                  n=len(fl), nt=d["n_trecho"], t=ss["traducao"], r=ss["resposta"], tr=ss["trava"], fi=ss["fita"], z=ss["z"], c=ss["clay"], p=ss["pai"], pe=ss["performada"], o=ss["ordem"], so=ss["sorry"], ra=ss["ratifica"])''')
a.troca('''("fala do operador; só o trecho que a D59 deixa entrar é embutido, e o arquivo inteiro entra só por sha256" if dd["trecho"] else "fala do operador")''',
        '''("fala do operador; só o trecho é embutido (%s), e o arquivo inteiro entra só por sha256" % ("D59" if "d61_ratificada" not in dd["nome"] else "o resto é aviso operacional") if dd["trecho"] else "fala do operador")''')
a.troca('''("clay", DL_.FRASE_CLAY), ("pai", DL_.FRASE_PAI), ("perf", DL_.FRASE_PERFORMADA))}''', '''("clay", DL_.FRASE_CLAY), ("pai", DL_.FRASE_PAI), ("perf", DL_.FRASE_PERFORMADA), ("sorry", DL_.FRASE_DISPOSITIVO), ("rat", DL_.FRASE_RATIFICA_D61))}''')
a.troca('''(de {nt} delas só o trecho que a D59 deixa entrar é embutido; o resto delas entra só por sha256); "''', '''(de {nt} delas só o trecho é embutido, de duas pela D59 e de uma porque o resto é aviso operacional; o resto delas entra só por sha256); "''')
a.troca('''e a ordem da v409, que ratifica os nomes dados pela gerência (`{s9}`): {ordem}. "''',
        '''e a ordem da v409, que ratifica os nomes dados pela gerência (`{s9}`): {ordem}; e, na tarde, a leitura jurídica do kernel (`{s10}`): {sorry}, e a ratificação dela (`{s11}`): {rat} (D61). "''')
a.troca('''s7=ss["pai"], s8=ss["performada"], s9=ss["ordem"], **q)''', '''s7=ss["pai"], s8=ss["performada"], s9=ss["ordem"], s10=ss["sorry"], s11=ss["ratifica"], **q)''')
a.troca('''"as erratas E24 a E26 (da gerência, em nome próprio) e as decisões D55 a D60 estão no registro `cunhagens_v409`;''', '''"as erratas E24 a E27 (da gerência, em nome próprio) e as decisões D55 a D61 (a D61 ratificada pelo operador) estão no registro `cunhagens_v409`;''')
a.troca("das duas da D59 só o trecho que fica está em `insumos` e entra no espelho, e o arquivo inteiro fica fora: publicá-lo é decisão do operador)",
        "das três de que só o trecho entra (duas da D59; uma, a ratificação da D61, cujo resto é aviso operacional) só o trecho que fica está em `insumos` e entra no espelho, e o arquivo inteiro fica fora: publicar o resto das duas da D59 é decisão do operador)")
a.grava()

# ------------------------------------------------------------------------------------------------ o conferir_citacoes (so' o rotulo)
a = Arq("conferir_citacoes_v409.py")
a.troca('''"""conferir_citacoes_v409.py -- [v409: as DEZ falas de 05/11/2026 (_V409_VERBATINS2); de duas, so' o trecho da D59 e' embutido''', '''"""conferir_citacoes_v409.py -- [v409: as DOZE falas de 05/11/2026 (_V409_VERBATINS2; as duas ultimas dos AO LADO do DESENHO); de tres, so' o trecho e' embutido (duas pela D59; uma pelo aviso operacional)''')
a.grava()
