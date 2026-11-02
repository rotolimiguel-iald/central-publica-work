# -*- coding: utf-8 -*-
"""aplicar_R2_fecho_v405.py -- a parte de FECHO da errata R2: o relatorio (secao R2, portao da fala excluida, aviso das apontadas), a purga (a fala excluida) e o fechamento (Mapa, fila, ACOM citando a primeira entrega). Contagem exata; tudo ou nada; backup de BYTES. Roda uma vez so'."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
NOVOS = {}


def carrega(arq):
    if arq not in NOVOS:
        NOVOS[arq] = open(os.path.join(HERE, arq), "rb").read().decode("utf-8")
    return NOVOS[arq]


def sub(arq, old, new, n=1):
    s = carrega(arq); c = s.count(old)
    assert c == n, (arq, c, n, old[:100])
    NOVOS[arq] = s.replace(old, new)


# ===================================================================================================== a purga: a fala excluida tambem (padroes por concatenacao, como os outros: este arquivo nao os contem)
P = "purga_v405.py"
sub(P, '''(a palavra de abertura do pedido de reserva e o hash da integra). Os padroes sao montados por concatenacao para este proprio arquivo NAO os conter. Grava purga_v405.json (so contagens e caminhos,
sem os padroes).''', '''(a palavra de abertura do pedido de reserva e o hash da integra), e, AO LADO (errata R2 da gerencia, 01/11/2026), os que contem a fala da lista de exclusao de delta_v405.py (a frase pessoal e o trecho do nome do arquivo). Os padroes sao montados por concatenacao para este proprio arquivo NAO os conter. Grava purga_v405.json (so contagens e caminhos,
sem os padroes).''')
sub(P, '''rx = re.compile(re.escape(PAT_A) + b"|" + re.escape(PAT_B), re.I)
''', '''PAT_C = ("filho Be" + "nto").encode()          # a frase pessoal da fala excluida
PAT_D = ("ratificada_be" + "nto").encode()      # o trecho do nome do arquivo da fala excluida (o delta a exclui pelo sha16, justamente para o nome nao viajar)
rx = re.compile(re.escape(PAT_A) + b"|" + re.escape(PAT_B), re.I)
rx2 = re.compile(re.escape(PAT_C) + b"|" + re.escape(PAT_D), re.I)
''')
sub(P, '''total = 0
for r in raizes:
    achados, n = [], 0
''', '''total = 0; total2 = 0
for r in raizes:
    achados, achados2, n = [], [], 0
''')
sub(P, '''                        if rx.search(b):
                            achados.append(p); break
''', '''                        if rx2.search(b) and p not in achados2:
                            achados2.append(p)
                        if rx.search(b):
                            achados.append(p); break
''')
sub(P, '''    res["raizes"][r] = {"arquivos_varridos": n, "com_ocorrencia": len(achados), "lista": achados}
    total += len(achados)
res["total_com_ocorrencia"] = total
''', '''    res["raizes"][r] = {"arquivos_varridos": n, "com_ocorrencia": len(achados), "lista": achados, "fala_excluida_com_ocorrencia": len(achados2), "fala_excluida_lista": achados2}
    total += len(achados); total2 += len(achados2)
res["total_com_ocorrencia"] = total
res["fala_excluida_total_com_ocorrencia"] = total2
''')
sub(P, '''    print(r, "| varridos", v["arquivos_varridos"], "| com ocorrencia", v["com_ocorrencia"])
    if "--listar" in sys.argv:
        for x in v["lista"]:
            print("   ", x)
print("TOTAL com ocorrencia:", total)
sys.exit(0 if total == 0 else 1)
''', '''    print(r, "| varridos", v["arquivos_varridos"], "| com ocorrencia", v["com_ocorrencia"], "| fala excluida", v["fala_excluida_com_ocorrencia"])
    if "--listar" in sys.argv:
        for x in v["lista"] + v["fala_excluida_lista"]:
            print("   ", x)
print("TOTAL com ocorrencia:", total, "| fala excluida:", total2)
sys.exit(0 if total == 0 and total2 == 0 else 1)
''')

# ===================================================================================================== o relatorio
Z = "gerar_relatorio_v405.py"
sub(Z, '''"guarda_das_frases": bool(GF.get("ok") is True),''', '''"guarda_das_frases": bool(GF.get("ok") is True and GF.get("pedras_limpas") is True and len(GF.get("pedras") or {}) == 8),''')
sub(Z, '''    "purga_da_fala_reservada": bool((tenta("purga_v405.json") or {}).get("total_com_ocorrencia") == 0),
}''', '''    "purga_da_fala_reservada": bool((tenta("purga_v405.json") or {}).get("total_com_ocorrencia") == 0),
    "fala_excluida_fora_dos_artefatos": bool((tenta("purga_v405.json") or {}).get("fala_excluida_total_com_ocorrencia") == 0),
}''')
sub(Z, '''NAO_REVISADO = "as oito pedras, os registros, a moldura, a cadeia inteira e os textos da v405 NAO foram revisados por terceiro (quem constroi nao aprova)"''',
    '''NAO_REVISADO = "este candidato (errata R2) NAO foi revisado por terceiro: a revisao de 01/11 reprovou o anterior, a30f9f0ebf90c277, e a trava do orquestrador fica fechada ate uma nova revisao aprovar; aquela revisao nao examinou o pos-rito, instalar, reverter, rito, B(n) nem o servico da Bancada (quem constroi nao aprova)"
_vp = (CIT.get("varredura_das_pedras") or {})
_cong_r2 = tenta("VERBATIM_CONGELADO_v405.json") or {}
_falas_01nov = sorted(os.path.basename(p_) for p_ in (_cong_r2.get("arquivos") or []) if "OPERADOR_01nov_" in os.path.basename(p_) and "A_IDENTIDADE" not in os.path.basename(p_))
ERRATA_R2 = {"revisao_anterior": {"candidato": "a30f9f0ebf90c277", "veredito": "NAO APROVADA (2 ALTO, 11 MEDIO, 10 BAIXO)", "caderno": "revisao_terceiro/REVISAO_TERCEIRO_v405.md"},
             "falas_embutidas": len(_cong_r2.get("arquivos") or []), "falas_de_01nov_no_glob": _falas_01nov, "falas_novas_desde_o_congelamento_anterior": [], "falas_excluidas_sha16": ["25c09b91c2a226c7"],
             "citacoes_das_pedras": {"conferidas": _vp.get("citacoes_conferidas"), "rotulos": len(_vp.get("rotulos") or []), "reprovadas": len(_vp.get("reprovadas") or []), "apontadas_a_gerencia": _vp.get("apontadas_a_gerencia") or []},
             "guarda_das_frases_nas_pedras": {"limpas": GF.get("pedras_limpas"), "falas_retiradas": sum(v_.get("falas_retiradas", 0) for v_ in (GF.get("pedras") or {}).values())}}''')
sub(Z, '''"hashes": HASHES, "nao_revisado_por_terceiro": NAO_REVISADO, "avisos": AVISOS,''', '''"hashes": HASHES, "nao_revisado_por_terceiro": NAO_REVISADO, "errata_r2": ERRATA_R2, "avisos": AVISOS,''')
sub(Z, '''## 2. Portões (cada linha lida de um arquivo)
''', '''## 1b. A errata R2 (a revisão de terceiro não aprovou `a30f9f0ebf90c277`)

A revisão achou 2 ALTO, 11 MÉDIO e 10 BAIXO, todos de texto, nome ou docstring: nenhuma prova caiu e nenhum número físico estava errado. A gerência corrigiu as oito pedras nas origens (`RECIBO_ERRATA_PEDRAS_R2_01nov.json`); o resto foi refeito aqui, pela cadeia existente.

| achado | o que foi feito |
|---|---|
| 1, 5, 6, 12 (pedras) | resolvidos pela gerência nas pedras; a E12 cita a pedra; D29 usa `FRASE_ALFA_CAUDA` com a grafia dele |
| 2 (homônimo) | token e check antigos fora; «o terminal lê 1» cita `the_fixed_points_read_one_and_zero`; o polo ω aparece como polo, homônimo dito, ligação [ONTO] do operador; checks o6 e o7 |
| 3, 4 (disco) | `E(t)` e `Ω²` são [DEF]; o fluxo é `the_flow_is_the_canonical_law` (check k7 novo); a taxa de dephasing lida como perda de energia é [INPUT/ONTO]; `Ω²` sem cota é [REAL]; a inscrição do zero no infinito e a terceira lei são [ONTO] |
| 7 (lista que não fecha) | «as leituras da cadeia da massa», dez itens, lista declarada não fechada (`lista_de_leituras_fechada = false`), com `meioTom`, `omegaSq`, `½ω = massa`, a hipótese de `area_por_volta_da_massa_inscrita`, `b = 0`, a taxa do disco; `g` e `κ` na moldura do artigo; token e chave novos |
| 8 (dispersão) | [INPUT, Tratado §3], entra como definição (`omegaSq`); só o ponto zero é [KNOWN] |
| 9 (fóton) | `foton_sem_massa` é álgebra de forma genérica; `b = 0` lido como o fóton é [ONTO]; o veredito do registro acompanha |
| 10 (observador) | ressalva dos rótulos e de `medido` no artigo PT/EN |
| 11 (ponto zero) | o que permanece no limite é [ONTO]: nenhum teorema liga os dois |
| 13 | «quatro níveis e cinco posições» |
| BAIXOS de texto e runtime | comentário e `Q_` em `v405_ponte_mechanics`, «a única massa», etiquetas de E12 e Tetelestai, «[DECISÃO da gerência c1…]», «not as a calculation» |
| título da seção | o título fica, porque vem da fala dele; a glosa saiu; a derivação é da forma, dadas as entradas |
| guardas novas | `guarda_frases` varre as oito pedras, com as falas como exceção, e tem controle negativo próprio; `conferir_citacoes` confere as docstrings das pedras, com as pedras FORA do corpus |
| a fala pessoal | lista de exclusão em `delta_v405.py`, por sha16 (o nome do arquivo não viaja); congelado regenerado; portão próprio na purga |

Citações das pedras: {_vp.get('citacoes_conferidas')} conferidas, {len(_vp.get('rotulos') or [])} rótulos listados, {len(_vp.get('reprovadas') or [])} reprovadas. **Apontadas à gerência, sem corrigir:** {'; '.join('%s: «%s» (%s)' % (a_['pedra'], a_['trecho'], a_['por_que']) for a_ in (_vp.get('apontadas_a_gerencia') or [])) or 'nenhuma'}.

Falas: {ERRATA_R2['falas_embutidas']} embutidas; as seis de 01/11 no glob já estavam no congelado anterior, logo nenhuma fala nova entrou. Nenhum nome próprio de terceiro nas demais falas (varredura por capitalizadas, lista de prenomes e termos de parentesco; só aparecem o sobrenome do operador em «ângulo de Miguel», nomes da teoria e IAs).

## 2. Portões (cada linha lida de um arquivo)
''')
sub(Z, '''| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v405.json`, zero ocorrências na pasta e no sandbox do kernel |''',
    '''| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v405.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | {PORTOES['fala_excluida_fora_dos_artefatos']}: `purga_v405.json`, zero ocorrências |''')
sub(Z, '''| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo) |''', '''| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo e as oito pedras, com as falas como exceção) |''')
sub(Z, '''7. A linha do handoff do índice saiu da âncora antiga (as linhas v392–v404 foram consolidadas): a superfície ancora na linha de 30/10 da v405.
''', '''7. A linha do handoff do índice saiu da âncora antiga (as linhas v392–v404 foram consolidadas): a superfície ancora na linha de 30/10 da v405.
8. O corpus de uma conferência de citações não pode conter o texto conferido: as pedras eram corpus da varredura, por isso as citações delas nunca reprovavam.
9. Guarda que não varre a origem deixa o resíduo onde ninguém olha: a moldura estava certa nos textos e errada nas docstrings.
10. Lista de leituras com tamanho fixo no código convida a fechá-la: a chave e as asserções passaram a dizer que a lista não é fechada.
''')

# ===================================================================================================== o fechamento
F = "fechar_preparacao_v405.py"
sub(F, '''"titulo": "v405 preparada (01/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,''',
    '''"titulo": "v405 preparada de novo, errata R2 (01/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,''')
sub(F, '''"nota": "quem constroi nao aprova: " + J["nao_revisado_por_terceiro"], "artefatos":''', '''"nota": "a revisao de terceiro NAO aprovou o candidato anterior, a30f9f0ebf90c277 (2 ALTO, 11 MEDIO, 10 BAIXO; caderno revisao_terceiro/REVISAO_TERCEIRO_v405.md); esta e' a refacao pela errata R2 da gerencia. Quem constroi nao aprova: " + J["nao_revisado_por_terceiro"], "artefatos":''')
sub(F, '''"refs": ["umpy.v404.selada_jo8_32_e_projecao_transversal_28out"]}]
ja = os.path.join(HERE, "registro_mapa_preparacao_v405_ANOTACAO.json")''', '''"refs": ["umpy.v404.selada_jo8_32_e_projecao_transversal_28out"]},
        {"tipo": "ERRATA", "rota_id": "kernel.v405.preparacao_01nov", "corrige": 1600, "estatuto": "REAL", "olhou_dados": False, "titulo": "a anotacao de 16:11 dizia pronta=true para a30f9f0ebf90c277: a revisao de terceiro nao aprovou esse candidato",
         "resultado": "o candidato a30f9f0ebf90c277 foi reprovado pela revisao de terceiro; nenhuma prova caiu e nenhum numero fisico estava errado; o candidato vigente da preparacao e' " + J["candidato_sha16"], "nota": "correcao ao lado; a anotacao anterior fica como registro"}]
ja = os.path.join(HERE, "registro_mapa_preparacao_v405_ANOTACAO.json")''')
sub(F, '''txt = ("v405 preparada em 01/11/2026 por claude-prep-v405 para a gerencia c1 (nada instalado; o rito nao rodou). " + res + ".\\n\\n"''',
    '''txt = ("v405 preparada de novo em 01/11/2026 por claude-prep-v405 para a gerencia c1, pela errata R2, depois de a revisao de terceiro nao aprovar o candidato a30f9f0ebf90c277 (nada instalado; o rito nao rodou). Este deposito substitui o de 16:11 (20261101_161153_v405-preparada.md, seq 187). " + res + ".\\n\\n"''')
sub(F, '''"Licoes novas: (1) nome longo de fala passa do MAX_PATH numa arvore emulada, logo a saida dos harnesses mora em caminho curto; (2) o JSON do rito real tem chaves no topo que o ensaio nao guarda, e a emulacao as le da constante do candidato; (3) a subida de versao funde os rotulos 403 e 404, e as pastas irmas e os registros recriados pedem regra propria; (4) a lista das falas e' congelada em VERBATIM_CONGELADO_v405.json, para que fala nova nao reprove o conferidor nem mude o candidato.\\n\\n"''',
    '''"Licoes novas: (1) nome longo de fala passa do MAX_PATH numa arvore emulada, logo a saida dos harnesses mora em caminho curto; (2) o JSON do rito real tem chaves no topo que o ensaio nao guarda, e a emulacao as le da constante do candidato; (3) a subida de versao funde os rotulos 403 e 404, e as pastas irmas e os registros recriados pedem regra propria; (4) a lista das falas e' congelada em VERBATIM_CONGELADO_v405.json, para que fala nova nao reprove o conferidor nem mude o candidato; (5) o corpus de uma conferencia de citacoes nao pode conter o texto conferido; (6) guarda que nao varre a origem deixa o residuo onde ninguem olha.\\n\\n"''')
sub(F, '''"--alvo", "novo:v405-preparada-01nov", "--casa", "Central de Patentes", "--slug", "v405-preparada",''', '''"--alvo", "novo:v405-preparada-01nov", "--casa", "Central de Patentes", "--slug", "v405-preparada-r2",''')
sub(F, '''req = {"operation": "transition", "reference": ref, "expected_revision": rev, "event_id": "prep-v405-fechada-" + S,''', '''req = {"operation": "transition", "reference": ref, "expected_revision": rev, "event_id": "prep-v405-r2-fechada-" + S,''')

for arq, novo in NOVOS.items():
    compile(novo, arq, "exec")
for arq, novo in NOVOS.items():
    p = os.path.join(HERE, arq); b = open(p, "rb").read()
    bak = p + ".bak_" + TS + "_R2"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    t = p + ".tmp_R2"; open(t, "wb").write(novo.encode("utf-8")); assert os.path.getsize(t) == len(novo.encode("utf-8")) and os.path.getsize(t) > 1000
    os.replace(t, p)
    print(arq, len(b), "->", len(novo.encode("utf-8")))
print("ok, backups .bak_%s_R2" % TS)
