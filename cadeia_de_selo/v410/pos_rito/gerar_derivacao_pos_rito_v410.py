# -*- coding: utf-8 -*-
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] a SUITE descreve tambem a PARTE 2 da retomada de 09/11 (a pedra AEscala, D82 a D87, nomes ratificados; o recibo documental HMS/13, D80; P = nP na forma da D81 e o Clay na forma canonica, D83/D84; os QUATRO registros com funcao; DOIS modulos; a secao README da custodia, D85): a descricao de cada arquivo ganha o sufixo _PT2 (numeros e ids LIDOS do delta); ganha o arquivo opcional ADAPTACAO_PARTE2_SONNET_B.json. SO' LE.
# [ADAPTADO v410, 09/11/2026, Sonnet (adaptacao do pos-rito; fork D), a servico do claude-construtor-v410] a SUITE descreve tambem a RETOMADA de 09/11 (os AO LADO do DESENHO: a secao 6 da pedra, D71 a D76, E30, os dois registros com funcao iald2_v410 e h0dn_bg1_v410 e as falas de 06 a 09/11); ganha os dois arquivos novos da retomada (NOTA_ESPERADOS_H0DN_v410.md e ADAPTACAO_09nov_SONNET.json, opcionais). SO' LE.
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v409 FINAL (_bump_copia_v410.py): a SUITE descreve a v410 (IALD2; os papeis, as datas e os autores de 06/11: fork A = o pos_rito inteiro e o orquestrador); o montador, a semente e o fragmento SAO usados na v410. SO' LE; a gerencia revisa antes do rito (nao e' versao selada).
"""gerar_derivacao_pos_rito_v410.py -- REGISTRA (SO' LE; nao deriva, nao sobrescreve nada) a proveniencia dos scripts do pos_rito da v410.
Na v410 a suite do pos_rito e' a SEMENTE mecanica de derivar_encanamento_v410.py (lote F) sobre o arquivo FINAL da cadeia v409 (o que foi USADO no pos-rito real da v409): o numero de versao subido por script (401 -> 409 e 409 -> 410, com a protecao dos nomes nascidos no um.py), mais as regras do lote F (os rotulos B(n), a lista de registros do chain,
o cabecalho do chain, o sufixo dos backups do Atlas e a marca TEXTO_A_REESCREVER_V410 nos arquivos de narrativa). A ADAPTACAO (o que o pos-rito diz da v410: IALD2, o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD relativo ao leitor, o signo e o seletor, com os numeros lidos do rito) foi feita em 06/11/2026 pela claude-construtor-v410 (fork A), pelos _adapt_*_v410.py desta pasta (trocas de contagem exata com backup de bytes), pelo montador (textos_v410.semente + textos_v410_novo.pysnip -> textos_v410.py) e por reescrita onde o corpo era o da v409 (registrar_mapa_v410.py, gerar_x_custodia_v410.py, textos_custodia_handoff_v410.py); a marca TEXTO_A_REESCREVER_V410 nao pode sobrar em nenhum arquivo (o p00 confere). A RETOMADA de 09/11/2026 (os AO LADO do DESENHO: a secao 6 da pedra, D71 a D76, E30, os dois registros com funcao e as falas de 06 a 09/11) foi feita pelo agente Sonnet de adaptacao do pos-rito (forks A a D), por script com backup de bytes e asserts de contagem, e esta' registrada em pos_rito\\ADAPTACAO_09nov_SONNET.json.
Este script apenas recalcula, em MEMORIA e com o proprio motor (derivar_v410_motor.bump), a semente PURA de cada arquivo (so' o mapa de versoes) e a compara com o arquivo atual.
Para cada arquivo do pos_rito que tem origem na v409 grava o sha256 da origem, o da semente pura (recalculada agora), o do arquivo atual, o estado (SEMENTE_PURA | DIFERE_DA_SEMENTE_PURA: regras do lote F ou edicao a mao) e o tamanho do diff (linhas trocadas); os que nao tem origem (escritos de novo) ficam listados como tais.
Escreve so' pos_rito/DERIVACAO_v410.json (com backup de bytes do anterior). NUNCA executa nenhum dos scripts; so' ast.parse. Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v410.py   (rc 0 = gravou; rc 1 = algum arquivo sem origem lida ou com sintaxe invalida)"""
import ast, difflib, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
sys.argv = sys.argv[:1]
import derivar_v410_motor as M  # noqa: E402
import delta_v410 as DL  # noqa: E402   (09/11: os numeros e os ids das descricoes da retomada saem do delta, nunca digitados)
assert "D73" in DL.DECISOES_V410 and "D75" in DL.DECISOES_V410
_RET09 = ("; 09/11 (retomada, Sonnet): adaptado ao DESENHO + AO LADO de 09/11 (%d falas de 06 a 09/11 -- de %d so' o trecho --, %s, %s, a secao 6 da pedra, os registros com funcao %s -- o segundo, pre-registrado; nenhum dado observado lido --, D73 e D75; ver ADAPTACAO_09nov_SONNET.json)"
          % (DL.N_FALAS_V410, len(DL.VERBATIM_SO_O_TRECHO), DL.DECISOES_ROTULO, " e ".join(e_.split()[0] for e_ in DL.ERRATAS_V410), " e ".join(DL.REGISTROS_FUNCAO)))

_PT2 = ("; 09/11 (parte 2, Sonnet B): a pedra AEscala (%s: nomes ratificados, D87), o recibo documental HMS/13 (D80), P = nP na forma da D81 e o Clay na forma canonica (D83/D84), %d registros com funcao (%s), %d modulos no bundle (%s), as %d falas de 06 a 09/11 e as decisoes %s; ver ADAPTACAO_PARTE2_SONNET_B.json"
        % (DL.MODULO_AESCALA, len(DL.REGISTROS_FUNCAO), ", ".join(DL.REGISTROS_FUNCAO), DL.N_BUNDLE, ", ".join(DL.BUNDLE_RELS), DL.N_FALAS_V410, DL.DECISOES_ROTULO))
assert "D87" in DL.DECISOES_V410 and len(DL.REGISTROS_FUNCAO) > 2 and DL.N_BUNDLE == len(DL.BUNDLE_RELS) > 1, "o delta nao e' o da parte 2 (a D87 na lista; mais de dois registros com funcao; mais de um modulo)"

sha = lambda b: hashlib.sha256(b).hexdigest()
V409_POS = os.path.join(os.path.dirname(PK), "v409", "pos_rito")
# a suite do pos_rito: (nome na v410, nome da origem na v409, papel). Os tres primeiros blocos sao os da tarefa A1 (encanamento do pos-rito, fila da memoria); os demais sao de outros agentes e entram so' para o registro.
SUITE = (
    ("chain_pos_rito_v410.sh", "chain_pos_rito_v409.sh", "fork A, 06/11: a cadeia (passos 0..14) com o passo da fila da memoria; REGS da v410 (os QUATRO registros com funcao, na ordem de delta_v410.REGISTROS_FUNCAO, mais cunhagens_v410 e kh_n1_cobertura_v410), o rotulo B19, o sufixo _v409 dos backups do inventario; 09/11 (parte 2): REGS com os seis nomes (os passos 3 e 9 os exigem nas superficies)" + _PT2),
    ("superficies_v410.py", "superficies_v409.py", "fork A, 06/11: as superficies (diretorio de memoria por V410_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B); so' as notas mudaram (os blocos vem do textos_v410.py); 09/11 (fork D): a guarda ganha a obrigacao D72 (onde H0DN aparecer, a frase pre-registrado; nenhum dado observado lido, literal, no mesmo texto) e os nomes ratificados (D74) nas notas" + _PT2 + "; guarda das obrigacoes da parte 2: HMS/13 (D80) e o Clay na forma canonica (D83/D84)"),
    ("fechar_v410.py", "fechar_v409.py", "fork A, 06/11: o fechar (manifesto com registros_v410/v409/v408/v407/v406 e registros_funcao_v410 (iald2 e h0dn_bg1_v410)/v409 (traducao)/v408 (tetelestai)/v407 (psion)/v406, arquivo, diffs, handoff); 09/11 (fork D): exige V['h0dn'] selado e sem vetor observado lido, leva h0dn_bg1_v410_resumo no manifesto e as guardas D72 no handoff" + _PT2 + "; exige V['fecho'], V['a_escala'], V['h0dn'] e V['hms13'] selados, leva registros_funcao_v410 com os quatro, a_escala_v410_resumo e h0dn_fontes_hms13_v410_resumo no manifesto, e as guardas D80/D83/D84/D87 no handoff"),
    ("b3_recibo_v410.py", "b3_recibo_v409.py", "fork A, 06/11: o recibo do B(n), passo SIMPLES B18 -> B19; so' as notas mudaram"),
    ("gerar_derivacao_pos_rito_v410.py", "gerar_derivacao_pos_rito_v409.py", "fork A, 06/11: este registro (so' le)"),
    ("harness_fechar_sandbox_v410.py", "harness_fechar_sandbox_v409.py", "fork A, 06/11: o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA e os controles negativos da v410 (a IALD2; a traducao, o tetelestai, o psion e o fechamento herdados; D65); 09/11 (fork D): os controles negativos do h0dn_bg1_v410 (vetor observado lido, token proibido, sem a frase obrigatoria, cabeca de 5 sigma), de E30, D72 e D76, e a etapa 2e do handoff" + _PT2 + "; o stub do harness com os seis nomes, os controles negativos da escala e do HMS/13 e as expectativas do manifesto e do handoff"),
    ("fila_memoria_v410.py", "fila_memoria_v409.py", "fork A, 06/11: as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar), chamadas pelo chain e pelo harness; so' as notas mudaram; 09/11: conferido, e' generico (nao lista falas, decisoes nem registros); parte 2: conferido de novo, sem mudanca de corpo"),
    ("leitura_v410.py", "leitura_v409.py", "fork A, 06/11: a leitura da rodada adaptada a IALD2 (o modulo IALD2, as ancoras lidas de delta_v410, nenhuma chave antiga muda; o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados e os registros anteriores recriados)" + _RET09 + _PT2 + "; os quatro blocos `>>> veredito <<<` do stdout (IALD2, A ESCALA, H0DN x BG1, H0DN FONTES HMS/13), a linha-resumo no formato novo, V['a_escala'] e V['hms13']"),
    ("textos_v410.py", "textos_v409.py", "fork A, 06/11: os textos da v410, MONTADOS (montar_textos_v410.py: semente + fragmento): o paragrafo novo (sem nota ao lado do paragrafo da v409), o handoff, as superficies, o topico novo" + "" + _RET09 + _PT2 + "; a secao da escala (a pedra AEscala; o Clay na forma canonica, D83/D84), o recibo HMS/13 na secao do H0DN, as 23 falas e os numeros por modulo"),
    ("harness_textos_ensaio_v410.py", "harness_textos_ensaio_v409.py", "fork A, 06/11: o harness do pos-rito adaptado a IALD2 (controles negativos dos registros novos e dos herdados, D65)" + "" + _RET09 + _PT2 + "; os controles negativos da escala e do HMS/13 (parte 2)"),
    ("registrar_mapa_v410.py", "registrar_mapa_v409.py", "fork A, 06/11: REESCRITO para a v410: a rota nova (o id esta em registrar_mapa_v410.NOVA), as anotacoes nas rotas de 06/11 e a errata E29 ao lado" + "" + _RET09 + _PT2 + "; a anotacao do recibo HMS/13 na rota do y_obs e a referencia a rota da pedra AEscala (a rota da preparacao; nada registrado agora)"),
    ("textos_custodia_handoff_v410.py", "textos_custodia_handoff_v409.py", "fork A, 06/11: REESCRITO para a v410: os sete textos da custodia (roda ENCADEADO no fim do S6, pelo orquestrador; a chain nao o chama)" + "" + _RET09 + _PT2 + "; a secao README (o que fica evidente, D85) e os sete textos com a escala, o Clay na forma canonica e o HMS/13"),
    ("gerar_x_custodia_v410.py", "gerar_x_custodia_v409.py", "fork A, 06/11: REESCRITO para a v410: o rascunho do post longo do X (numeros do selo e do core; a ordem e as cunhagens por delta_v410.FRASE_*; sem o 4,44; D65)" + "" + _RET09 + _PT2 + "; a escala, o Clay na forma canonica e o recibo HMS/13 no post"),
    ("montar_textos_v410.py", "montar_textos_v409.py", "fork A, 06/11: o montador (semente + fragmento -> textos_v410.py); DELETAR ganha _d56, errata_v409_bloco e MARC_ERR_*" + "" + _RET09 + ""),
    ("textos_v410_novo.pysnip", "textos_v409_novo.pysnip", "fork A, 06/11: o fragmento da v410 (as definicoes da IALD2; __HEADER__)" + "" + _RET09 + _PT2 + ""),
    ("textos_v410.semente", "textos_v409.py", "fork A, 06/11: a semente = textos_v409.py FINAL (montado) com os rotulos subidos, a marca trocada e o fim de linha normalizado para LF"),
    ("adaptar_pos_rito_v410.py", None, "OPCIONAL: o adaptador comum da v409; na v410 cada _adapt_*_v410.py e' autonomo"),
    ("NOTA_ESPERADOS_H0DN_v410.md", None, "OPCIONAL, Sonnet, 09/11: as chaves que o gerar_esperados_v410 tera de emitir para o registro h0dn_bg1_v410 (D72: pre-registrado; nenhum dado observado lido)"),
    ("ADAPTACAO_PARTE2_SONNET_B.json", None, "OPCIONAL, Sonnet B, 09/11 (parte 2): o registro da adaptacao do pos-rito a pedra AEscala, ao recibo HMS/13 e aos quatro registros com funcao (arquivos tocados com sha16 antes/depois, o que nao se verifica sem o ensaio, achados); fica na pasta da cadeia (v410), nao em pos_rito"),
    ("ADAPTACAO_09nov_SONNET.json", None, "OPCIONAL, Sonnet, 09/11: o registro da retomada de 09/11 (arquivos tocados com sha16 antes/depois, testes com rc, pendencias)"),
)
OPCIONAIS = {"adaptar_pos_rito_v410.py", "NOTA_ESPERADOS_H0DN_v410.md", "ADAPTACAO_09nov_SONNET.json", "ADAPTACAO_PARTE2_SONNET_B.json"}
SUITE = SUITE + tuple((f_, None, "claude-construtor-v410, 06/11: adaptador (trocas de contagem exata com asserts e backup de bytes)") for f_ in sorted(os.listdir(HERE)) if f_.startswith("_adapt_") and f_.endswith("_v410.py"))
rel = []; ruim = []
for nome, origem, papel in SUITE:
    p = os.path.join(HERE, nome)
    if not os.path.isfile(p):
        if nome in OPCIONAIS:
            rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE_OPCIONAL (nao faz parte da v410; listado so' porque o molde v409 o tinha)"}); continue
        rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE"}); ruim.append(nome); continue
    atual = open(p, "rb").read()
    r = {"arquivo": nome, "papel": papel, "bytes": len(atual), "sha256": sha(atual)}
    if nome.endswith(".py"):
        try:
            ast.parse(atual.decode("utf-8"))
            r["ast_parse"] = True
        except SyntaxError as e:
            r["ast_parse"] = False; r["erro"] = repr(e)[:200]; ruim.append(nome)
    if origem is None:
        r["estado"] = "ESCRITO_DE_NOVO_SEM_ORIGEM"
    else:
        po = os.path.join(V409_POS, origem)
        if not os.path.isfile(po):
            r["estado"] = "ORIGEM_V409_AUSENTE"; ruim.append(nome)
        else:
            raw = open(po, "rb").read()
            semente = M.bump(raw.decode("utf-8"), (), "v409").encode("utf-8")
            r["origem_v409"] = {"path": po, "sha256": sha(raw)}
            r["semente_mecanica_sha256"] = sha(semente)
            if semente == atual:
                r["estado"] = "SEMENTE_PURA"
            else:
                r["estado"] = "DIFERE_DA_SEMENTE_PURA__regras_do_lote_F_ou_edicao_a_mao"
                a_, b_ = semente.decode("utf-8").splitlines(), atual.decode("utf-8").splitlines()
                sm = difflib.SequenceMatcher(None, a_, b_, autojunk=False)
                r["diff_contra_a_semente"] = {"linhas_da_semente": len(a_), "linhas_do_arquivo": len(b_), "linhas_trocadas_ou_novas": sum((j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")}
    rel.append(r)
    print("%-38s %-34s %s" % (nome, r["estado"], r["sha256"][:12]))
out = {"contrato": "DERIVACAO_POS_RITO_v410", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "executado": False,
       "origem": "pos_rito da v409 FINAL (a cadeia usada no pos-rito real da v409), rotulos 409 -> 410 por script (_bump_copia_v410.py, semente pura); a adaptacao foi feita pela claude-construtor-v410 (fork A) em 06/11/2026 pelos _adapt_*_v410.py desta pasta, pelo montador dos textos e por reescrita onde o corpo era o da v409 (registrar_mapa, gerar_x_custodia, textos_custodia_handoff); a marca TEXTO_A_REESCREVER_V410 nao pode sobrar em nenhum arquivo (o p00 confere)",
       "arquivos": rel, "nota": "so' le: nenhum script foi executado nem sobrescrito; a semente de cada arquivo e' RECALCULADA em memoria pelo motor a cada vez (hash nunca digitado)"}
dst = os.path.join(HERE, "DERIVACAO_v410.json")
if os.path.exists(dst):
    raw = open(dst, "rb").read(); bk = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(dst + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(dst + ".tmp", dst)
print("DERIVACAO_v410.json gravado (%d arquivos registrados; problemas: %s)" % (len(rel), ruim or "nenhum"))
sys.exit(1 if ruim else 0)
