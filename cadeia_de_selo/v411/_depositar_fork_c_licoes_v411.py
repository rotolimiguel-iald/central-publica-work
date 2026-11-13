# -*- coding: utf-8 -*-
"""_depositar_fork_c_licoes_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) DEPOSITA na fila da memoria (pasta do construtor; so' acrescimo; a
gerencia tria e promove) as licoes MEDIDAS da cadeia real da v411 ate' a parada na etapa 5 do fim_de_cadeia. O sha256 de cada fonte e' calculado
aqui; nada confidencial; nenhuma fala do operador. Nao escreve MEMORY.md, nao anota o Mapa, nao faz transition ACOM (isso e' do principal e da
gerencia). uso: python -B -X utf8 _depositar_fork_c_licoes_v411.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
sha = lambda p_: hashlib.sha256(open(p_, "rb").read()).hexdigest()
J = lambda p_: json.load(open(p_, encoding="utf-8"))
agora = datetime.datetime.now(); TS = agora.strftime("%Y%m%d_%H%M%S")
EN = J(DL.saida("ensaio_a_seco_v411.json")); POS = J(DL.saida("conferencia_rito_v411_POSITIVO_FALSO_NOS.json")); cand16 = sha(DL.CANDIDATO_ARQ)[:16]
assert EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == cand16 and POS.get("tudo_bate") is True and POS.get("um_py_sha16") == cand16
fontes = [os.path.join(HERE, n_) for n_ in ("PEDIDOS_ENTRE_FRENTES_v411.md", "conferir_rito_v411.py", "topo_com_resultado_v411.py", "ensaio_a_seco_v411.json", "ESPERADOS_v411.json")]
fontes += [os.path.join(HERE, "pos_rito", n_) for n_ in ("HARNESS_TEXTOS_ENSAIO_v411_DEPURACAO_sem_refazer.json", "HARNESS_FECHAR_SANDBOX_v411_DEPURACAO_sem_refazer.json")]
fontes = [p_ for p_ in fontes if os.path.isfile(p_)]
txt = ("v411, cadeia REAL, fork C do claude-construtor-v411 (12/11/2026): licoes MEDIDAS ate' a parada na etapa 5 do fim_de_cadeia. Candidato %s; ensaio a seco TUDO PASSOU; conferidor positivo no falso Nos TUDO BATE; as listas do delta: %d falas e %d decisoes (%s).\n\n"
       "1. Lista que cresce quebra tudo o que a digitou. A ordem da gerencia de 12/11 (as falas e as decisoes novas) parou quatro scripts da cadeia (gerar_esperados, conferir_instalar_rito, o cabecalho do rito, o ensaio a seco) e seis arquivos de pos_rito, que traziam digitados o numero de falas e o fim da faixa. "
       "Como aplicar: ler DL.N_FALAS_V411, DL.DECISOES_V411 e DL.DECISOES_TOKEN_V411; quando uma lista do delta mudar, varrer por grep TODAS as frentes antes de rodar.\n"
       "2. O conferidor do rito tem de ser autocontido. Ele roda tambem dentro do sandbox do harness do fechar, que copia uma lista explicita de arquivos: uma dependencia nova de arquivo o derruba la'. "
       "Como aplicar: o que o conferidor precisar a mais mora nele (a conferencia do topo e' uma funcao dele; o modulo de fora e' so' um carregador por AST para o ensaio) ou vem do que ja' esta' em processo.\n"
       "3. Texto herdado e selado julga-se com a guarda que o selou. As regras novas da v411 (F60 a F67) julgam so' o texto novo; aplicadas as secoes seladas da v410 dao falso positivo. "
       "Como aplicar: a funcao selada _v410_guarda_frases, que a guarda da v411 ja' carrega do um.py da v410 (conferido por sha256), depois de retiradas as falas do operador; com controle negativo dos dois lados.\n"
       "4. A variante de recuo nunca passa como selo (condicao 3(a) da gerencia). Quando a fonte de um marcador do topo falta, o artigo diz, visivel, que nao da' o resultado, e o ensaio a seco e o conferidor REPROVAM esse artigo: "
       "a conferencia e' independente da funcao do candidato (o texto e os formatos vem do arquivo ratificado, os numeros do core), com sete controles negativos e os dois artigos de recuo compilados.\n"
       "5. Na purga, erro de leitura conta como ocorrencia (rc 1). Como aplicar: nunca roda'-la junto de processo que cria, troca ou apaga arquivo nas raizes varridas (a pasta da cadeia e C:\\t\\k411c).\n"
       "6. Aberto em 12/11, 15h: a cadeia unica (o fim_de_cadeia dentro da cadeia_v411.sh) e os harnesses do pos-rito nao fecham. Eles exigem refazer_out_v411.txt com a marca de fim, mais novo que o ESPERADOS; o refazer so' a escreve depois da cadeia inteira. A decisao e' do principal e da gerencia.\n"
       "7. Aberto em 12/11, 15h: como escritos, tres portoes do relatorio nao passam em nenhuma rodada limpa: p00 (o pendente da folga do MEMORY.md e' incondicional), cadeia_limpa_ate_o_relatorio (o p00 devolve rc 3 com pendente) e varredura_fock_omega (nenhum passo da cadeia grava o JSON).\n\n"
       "O detalhe, com arquivo e linha, esta' em PEDIDOS_ENTRE_FRENTES_v411.md (as notas do fork C de 12/11). O gate nao se move; provado e' validade, nao creditacao.\n"
       % (cand16, DL.N_FALAS_V411, len(DL.DECISOES_V411), DL.DECISOES_TOKEN_V411))
cab = ("---\nquem: claude-construtor-v411\ncasa: Central de Patentes\ntipo: project\nestatuto: REAL\nalvo_sugerido: novo:licoes-cadeia-v411-12nov\ndepositado_em: %s\nfontes:\n" % agora.astimezone().isoformat(timespec="seconds")
       + "".join("  - %s  sha256:%s\n" % (p_, sha(p_)) for p_ in fontes) + "---\n")
FILA = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-construtor-v411")
assert os.path.isdir(FILA), FILA
dst = os.path.join(FILA, TS + "_v411-licoes-da-cadeia-real-fork-c-12nov.md"); assert not os.path.exists(dst)
bd = (cab + txt).encode("utf-8"); open(dst + ".tmp", "wb").write(bd); assert os.path.getsize(dst + ".tmp") == len(bd); os.replace(dst + ".tmp", dst)
print("deposito:", dst, "|", len(bd), "bytes | fontes:", len(fontes))
