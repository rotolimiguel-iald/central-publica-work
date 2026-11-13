# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-L-v411] a SUITE descreve a v411 (o teste H0DN x BG1 aberto uma vez; NENHUM modulo novo; UM registro com funcao, h0dn_bg1_v411): os asserts de delta (as decisoes do delta, E41 a E43, um registro com funcao) e as descricoes de cada arquivo substituem as da v410 (IALD2, AEscala, HMS/13, bundle de dois modulos); so' le.
"""gerar_derivacao_pos_rito_v411.py -- REGISTRA (SO' LE; nao deriva, nao sobrescreve nada) a proveniencia dos scripts do pos_rito da v411.
Na v411 a suite do pos_rito parte da SEMENTE mecanica (derivar_v411_motor.bump) sobre o arquivo FINAL da cadeia v410 (o que foi USADO no pos-rito real da v410): o numero de versao subido por script (409 -> 410 e 410 -> 411, com a protecao dos nomes nascidos no um.py). A ADAPTACAO (o que o pos-rito diz da v411: o teste da razao
de Hubble local/fundo, H0DN x BG1, aberto UMA vez em 12/11/2026 depois do commit publico do pre-registro, RECALCULADO no rito dos bytes embutidos; as DUAS linhas juntas, o primario sob o modelo de erros publicado e as Cefeidas livres ao lado; as sete ressalvas; o que o teste nao decide; as decisoes do delta; E41, E42 e E43 ao lado; o kernel sem modulo novo) foi feita em 12/11/2026 pela claude-sonnet-posrito-L-v411,
a servico do claude-construtor-v411, para os dez arquivos desta frente (leitura, textos e o par semente/fragmento, o montador, fechar, superficies, a fila da memoria, o recibo do B(n) e este registro); os demais arquivos da suite (a chain, os harnesses, o mapa, a custodia, o X) sao de outras frentes e entram so' para o registro.
Este script apenas recalcula, em MEMORIA e com o proprio motor (derivar_v411_motor.bump), a semente PURA de cada arquivo (so' o mapa de versoes) e a compara com o arquivo atual. Para cada arquivo do pos_rito que tem origem na v410 grava o sha256 da origem, o da semente pura (recalculada agora), o do arquivo atual, o estado (SEMENTE_PURA | DIFERE_DA_SEMENTE_PURA: regras do lote F ou edicao a mao)
e o tamanho do diff (linhas trocadas); os que nao tem origem (escritos de novo) ficam listados como tais. Escreve so' pos_rito/DERIVACAO_v411.json (com backup de bytes do anterior). NUNCA executa nenhum dos scripts; so' ast.parse.
Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v411.py   (rc 0 = gravou; rc 1 = algum arquivo sem origem lida ou com sintaxe invalida)"""
import ast, difflib, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
sys.argv = sys.argv[:1]
import derivar_v411_motor as M  # noqa: E402
import delta_v411 as DL  # noqa: E402   (os numeros e os ids das descricoes saem do delta, nunca digitados)
assert DL.UM_VERSION == "v411" and DL.FECHO_REGISTRO == "h0dn_bg1_v411" and list(DL.REGISTROS_FUNCAO) == [DL.FECHO_REGISTRO] and all(re.fullmatch(r"D\d{3}", k_) for k_ in DL.DECISOES_V411) and "_".join(DL.DECISOES_V411) == DL.DECISOES_TOKEN_V411 and {"D159", "D162", "D167", "D168", "D169", "D170"} <= set(DL.DECISOES_V411), "o delta nao e' o da v411 (um registro com funcao; as decisoes do delta, com as seis de base)"
assert [e_["id"] for e_ in DL.ERRATAS_V411] == ["E41", "E42", "E43", "E44"] and DL.N_FALAS_V411 == len(DL.FALAS_V411) and DL.N_CHECKS_FECHO == 16, "o delta nao traz as erratas E41 a E43, as falas ou as 16 checagens"
_V411 = ("; 12/11 (claude-sonnet-posrito-L-v411): adaptado de verdade a v411 (%d falas de 11 e 12/11, %s a %s, %s, o registro com funcao %s com %d checagens, os %d registros da v410 recriados, nenhum modulo novo; ver ADAPTACAO_L_v411.json)"
         % (DL.N_FALAS_V411, min(DL.DECISOES_V411), max(DL.DECISOES_V411), ", ".join(e_["id"] for e_ in DL.ERRATAS_V411), DL.FECHO_REGISTRO, DL.N_CHECKS_FECHO, len(DL.REGISTROS_FUNCAO_V410)))
_DE_OUTRA = " (subida mecanica de rotulo da v410; a adaptacao a v411 e' de outra frente do construtor; este registro so' le)"

sha = lambda b: hashlib.sha256(b).hexdigest()
V410_POS = os.path.join(os.path.dirname(PK), "v410", "pos_rito")
# a suite do pos_rito: (nome na v411, nome da origem na v410, papel). Os dez primeiros sao os da frente L; os demais sao de outras frentes e entram so' para o registro.
SUITE = (
    ("leitura_v411.py", "leitura_v410.py", "a leitura da rodada adaptada a v411: le o registro com funcao h0dn_bg1_v411 (V['fecho']: as duas linhas, os atos, as sete ressalvas, o que nao decide), os registros por spec da v411 e os registros da v410 recriados (V['reg410_recriados']); nenhum modulo novo (conferido como ZERO: o kernel e a escada sao os da v410); a linha [v411] do stdout" + _V411),
    ("textos_v411.py", "textos_v410.py", "os textos da v411, MONTADOS (montar_textos_v411.py: semente + fragmento): o diario, o adendo, o Atlas, o core, o topico, o aviso, o verbete, o paragrafo do README e o handoff (sem os blocos da custodia), montados do core selado, com as quatro obrigacoes da guarda no mesmo bloco do primario" + _V411),
    ("textos_v411_novo.pysnip", "textos_v410_novo.pysnip", "o fragmento da v411 (as definicoes do teste aberto; __HEADER__; DELETAR no montador as da IALD2, da AEscala e do HMS/13)" + _V411),
    ("textos_v411.semente", "textos_v410.py", "a semente = textos_v410.py FINAL (montado) com os rotulos subidos pelo motor e o fim de linha normalizado para LF"),
    ("montar_textos_v411.py", "montar_textos_v410.py", "o montador (semente + fragmento -> textos_v411.py); DELETAR passa a incluir os nomes da v410 sem equivalente na v411" + _V411),
    ("fechar_v411.py", "fechar_v410.py", "o fechar: exige V['fecho'] (h0dn_bg1_v411) selado com as 16 checagens, as duas linhas e as sete ressalvas, V['reg410_recriados'] selados e bundle vazio (nenhum modulo novo); manifesto com h0dn_bg1_v411_resumo e registros_v411; guardas das quatro obrigacoes no handoff" + _V411),
    ("superficies_v411.py", "superficies_v410.py", "as superficies (diretorio de memoria por V411_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B); as notas e a guarda das obrigacoes da v411 (as quatro do primario no mesmo bloco)" + _V411),
    ("b3_recibo_v411.py", "b3_recibo_v410.py", "o recibo do B(n), passo SIMPLES B19 -> B20; so' o cabecalho mudou" + _V411),
    ("fila_memoria_v411.py", "fila_memoria_v410.py", "as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar); generico; so' o cabecalho mudou" + _V411),
    ("gerar_derivacao_pos_rito_v411.py", "gerar_derivacao_pos_rito_v410.py", "este registro (so' le)" + _V411),
    ("chain_pos_rito_v411.sh", "chain_pos_rito_v410.sh", "a cadeia (passos 0..14)" + _DE_OUTRA),
    ("harness_fechar_sandbox_v411.py", "harness_fechar_sandbox_v410.py", "o harness do fechar/chain em sandbox" + _DE_OUTRA),
    ("harness_textos_ensaio_v411.py", "harness_textos_ensaio_v410.py", "o harness dos textos em ensaio" + _DE_OUTRA),
    ("registrar_mapa_v411.py", "registrar_mapa_v410.py", "o registro no Mapa de Rotas" + _DE_OUTRA),
    ("textos_custodia_handoff_v411.py", "textos_custodia_handoff_v410.py", "os textos da custodia anexados ao handoff (NOTA_EN, README_*, ESTATUTO_P2_*)" + _DE_OUTRA),
    ("gerar_x_custodia_v411.py", "gerar_x_custodia_v410.py", "o rascunho do post do X" + _DE_OUTRA),
    ("teste_textos_sem_candidato_v411.py", None, "o teste de unidade da frente L: monta um V sintetico do registro offline do ensaio (TESTE_H0DN_OFFLINE_v411_registro.json) e passa cada texto pela guarda de frases (sem o core real)"),
    ("ADAPTACAO_L_v411.json", None, "OPCIONAL, claude-sonnet-posrito-L-v411, 12/11: o registro da adaptacao (arquivos tocados com sha16 antes/depois, o que foi testado e como, o que falta, as chaves de V)"),
)
OPCIONAIS = {"ADAPTACAO_L_v411.json"}
SUITE = SUITE + tuple((f_, None, "claude-construtor-v411, 06/11: adaptador (trocas de contagem exata com asserts e backup de bytes)") for f_ in sorted(os.listdir(HERE)) if f_.startswith("_adapt_") and f_.endswith("_v411.py"))
rel = []; ruim = []
for nome, origem, papel in SUITE:
    p = os.path.join(HERE, nome)
    if not os.path.isfile(p):
        if nome in OPCIONAIS:
            rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE_OPCIONAL (nao faz parte da v411; listado so' porque o molde v410 o tinha)"}); continue
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
        po = os.path.join(V410_POS, origem)
        if not os.path.isfile(po):
            r["estado"] = "ORIGEM_V410_AUSENTE"; ruim.append(nome)
        else:
            raw = open(po, "rb").read()
            semente = M.bump(raw.decode("utf-8"), (), "v410").encode("utf-8")
            r["origem_v410"] = {"path": po, "sha256": sha(raw)}
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
out = {"contrato": "DERIVACAO_POS_RITO_v411", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "executado": False,
       "origem": "pos_rito da v410 FINAL (a cadeia usada no pos-rito real da v410), rotulos 409 -> 410 e 410 -> 411 por script (_bump_copia_v411.py, semente pura); a adaptacao dos dez arquivos da frente L foi feita em 12/11/2026 pela claude-sonnet-posrito-L-v411 a servico do claude-construtor-v411; a marca de subida mecanica de rotulo nao pode sobrar em nenhum arquivo da pasta (o p00 confere)",
       "arquivos": rel, "nota": "so' le: nenhum script foi executado nem sobrescrito; a semente de cada arquivo e' RECALCULADA em memoria pelo motor a cada vez (hash nunca digitado)"}
dst = os.path.join(HERE, "DERIVACAO_v411.json")
if os.path.exists(dst):
    raw = open(dst, "rb").read(); bk = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(dst + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(dst + ".tmp", dst)
print("DERIVACAO_v411.json gravado (%d arquivos registrados; problemas: %s)" % (len(rel), ruim or "nenhum"))
sys.exit(1 if ruim else 0)
