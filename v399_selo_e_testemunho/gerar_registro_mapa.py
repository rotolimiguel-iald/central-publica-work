# -*- coding: utf-8 -*-
"""gerar_registro_mapa.py -- monta registro_mapa_v399_estudo.json (so campos de `rotas.py modelo`) a partir dos recibos (numeros LIDOS) e o VALIDA com rotas._valida SEM registrar.
Registrar e' ato da gerencia. Uso: python -I -B -X utf8 gerar_registro_mapa.py"""
import hashlib
import importlib.util
import json
import os
import sys
import time

W = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True


def J(*p):
    return json.load(open(os.path.join(W, *p), encoding="utf-8"))


def pt(x, d=2):
    return ("%.*f" % (d, x)).replace(".", ",")


proto = J("recibos", "RECIBO_PROTOTIPO_um_py_v398.json")
sel = proto["selo"]["acom"]
aud = sel["auditoria_de_separacao"]
ex = {(p["centro"], p["angular_bits"]): p for p in J("recibos", "RECIBO_EXATIDAO_ALFABETO.json")["perfis"]}
ct = J("recibos", "RECIBO_CONTROLES.json")
rp = J("recibos", "RECIBO_REPRODUTIBILIDADE.json")
sim = J("recibos", "RECIBO_SIMULACAO_COLADA.json")
axi = J("AXIOMAS.json")
fon = J("fontes_sha.json")
cab = J("conferencia_cabecalho.json")
n_obj = proto["objeto"]["bytes"]
stone16 = hashlib.sha256(open(os.path.join(W, "Testemunho.lean"), "rb").read()).hexdigest()[:16]


def P(*a):
    return os.path.join(W, *a)


A_SELO = [P("RESULTADO.md"), P("selo_acom_prototipo.py"), P("EMBUTIDO_MANIFESTO.json"), P("patch_proposto", "PATCH_PROPOSTO_v399.md"), P("patch_proposto", "secao_colavel_v399.py"),
          P("patch_proposto", "trechos_v399_para_o_um_py.py"), P("recibos", "RECIBO_PROTOTIPO_um_py_v398.json"), P("recibos", "RECIBO_EXATIDAO_ALFABETO.json"), P("recibos", "RECIBO_CONTROLES.json"),
          P("recibos", "RECIBO_CONFORMIDADE.json"), P("recibos", "RECIBO_REPRODUTIBILIDADE.json"), P("recibos", "RECIBO_SIMULACAO_COLADA.json"), P("recibos", "um_absoluto_selo_acom.json")]
A_PEDRA = [P("Testemunho.lean"), P("AXIOMAS.json"), P("conferencia_cabecalho.json"), P("conferencia_sandbox.json"), P("lake_build_testemunho.log"), P("RESULTADO.md")]
A_DECL = [P("patch_proposto", "trechos_v399_para_o_um_py.py"), P("recibos", "registro_declaracao_do_operador_v399_EXEMPLO.json"), P("recibos", "RECIBO_SIMULACAO_COLADA.json"),
          r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt", P("RESULTADO.md")]

R1 = {
    "tipo": "ROTA", "rota_id": "umpy.v399.selo_pela_propria_tecnologia_estudo_24out", "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "v399 (estudo, 24/10): o ACOM Mirror Crypto do operador EMBUTIDO no um.py como SEGUNDA testemunha ao lado do SHA-256 — perfil C96/Q8, Dobra exata so apos rint, partes Psi/Theta/kappa, sem alegacao criptografica; prototipo roda no um.py v398; NAO instalado",
    "pergunta": ("O ACOM Mirror Crypto (patente BR 10 2026 003431-2; reflexao dimensional BR 10 2026 003428-2), embutido no um.py (arquivo unico), sela os bytes do um.py e o core/selo da rodada AO LADO do SHA-256, "
                 "com reconstrucao exata e recusa fail-closed? A Dobra e' exata para tensores de bytes? Direcao: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD nao testifica do operador."),
    "dados": ["um.py v398 (%d bytes, c632fa261ce3f538), core e selo da rodada v398 em Nos (so leitura)" % n_obj,
              "codigo do operador (so leitura): skygrid_sim/acom_mirror.py, acom_crypto.py, tgl_core.py, tests/run_tests.py; Acom_v17_mirror_crypto.py (torch); ACOM_Mirror_Crypto_PI_INPI.tex"],
    "metodo": ("Codigo do operador COPIADO (port numpy) com 5 substituicoes declaradas e hash do bloco; perfil L = byte-96, Q=8; partes cruas hasheadas ANTES de ofuscacao/compressao; ids derivados dos hashes; "
               "reconstrucao independente do codificador + rint ao reticulado; enumeracao exaustiva do alfabeto; auditoria de separacao (nenhuma parte basta; Psi nao redundante); 13 controles negativos; "
               "conformidade original x embutido x rapido x legado torch; suite do operador em copia byte-identica; reprodutibilidade entre dois interpretadores; simulacao da colagem num um.py simulado (CRLF)."),
    "resultado": ("um.py: selagem %s s, verificacao %s s; Psi %d B, Theta %d B, kappa %d B (%sx o objeto); round trip byte a byte exato; Dobra pura NAO exata em R (erro max %s) — exata apos rint: C96/Q8 %d casos, %d falhas; "
                  "centro 0/Q8 inservivel (%d falhas, %d m nao injetivos) e centro 128 deixa Psi redundante em ASCII puro; %d/%d controles recusados; Theta+kappa com sinal unico acerta %s%% dos bytes (confidencialidade nao atestada); "
                  "reprodutibilidade 3.14 x 3.13: %s; colagem simulada: all_verified=%s." % (
                      pt(proto["selar_total_s"]), pt(proto["verificar_s"]), sel["psi"]["bytes"], sel["theta"]["bytes"], sel["kappa"]["bytes"],
                      pt(proto["tamanho_das_partes_cruas_bytes"]["psi_mais_theta_mais_kappa"] / n_obj, 3), pt(sel["prova_de_reconstrucao"]["erro_real_maximo_antes_do_rint"], 4),
                      ex[(96, 8)]["casos"], ex[(96, 8)]["falhas_apos_rint"], ex[(0, 8)]["falhas_apos_rint"], ex[(0, 8)]["valores_nao_injetivos_em_m"],
                      ct["objeto_inteiro_um_py"]["n_controles"], ct["objeto_inteiro_um_py"]["n_controles"], pt(100 - 100 * aud["theta_mais_kappa_com_sinal_unico"]["fracao_errada"], 1),
                      "TODOS IGUAIS" if rp["todos_iguais"] else "DIVERGEM", sim["selo_acom_v399"]["all_verified"])),
    "veredito": "TGL_SELO_ACOM_V399_STUDY__PROTOTYPE_EXACT_ON_UMPY_V398__SECOND_WITNESS_BESIDE_SHA256__INTEGRITY_PRIMITIVE_INSIDE_THE_METHOD_IS_SHA256__NO_CRYPTOGRAPHIC_CLAIM__PROFILE_C96_Q8__NOT_INSTALLED__LEGAL_FLAG__GATE_UNMOVED",
    "defeito": ("A Dobra pura nao e' exata em R; a exatidao exige o rint ao reticulado inteiro, que NAO e' da patente. A primitiva de integridade dentro do metodo e' o SHA-256: a segunda testemunha nao e' independente em forca criptografica. "
                "Confidencialidade ('partes isoladas = ruido', reivindicacao 2) nao e' atestada. Reprodutibilidade testada em uma maquina (dois interpretadores). Sem revisao independente. [LEGAL] embutir publica a implementacao."),
    "nao_refazer": ("o perfil literal 'bytes sem sinal' (centro 0) e o centro 128 estao medidos e recusados pela funcao selar; a exatidao do alfabeto C96/Q8 esta enumerada (todos os m<=159); a conformidade com o codigo do operador e a suite dele (69/69 na copia) estao medidas; "
                    "a camada de transporte verbatim (XOR+zlib) nao e' reprodutivel byte a byte e nao e' usada pelo selo canonico."),
    "proximo_passo": ("revisao independente do prototipo e da simulacao; decisoes D1-D7 do RESULTADO.md (nome, [LEGAL] com a agente de PI, perfil, recusa derruba o rito?, sidecar na custodia, texto do artigo, leitura das faces); so' depois a cadeia gerar_candidato_v399.py e o rito."),
    "onde": r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho\selo_acom_prototipo.py (secao colavel: patch_proposto\secao_colavel_v399.py)",
    "artefatos": A_SELO,
    "refs": ["infra.app.acom_signal_transport_20261021", "infra.um_acom_central_patentes", "kernel.testemunha_estatica_v396_candidata_22out", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um"],
    "nota": "Em nome proprio da gerencia c1 (subagente), 24/10/2026. Consultas ao mapa antes: acom crypto/criptografia/testemunho/declaracao do operador devolveram 0 rotas; as vizinhas estao em refs. Nada registrado alem deste arquivo (pronto, validado com rotas._valida, sem gravar).",
}
R2 = {
    "tipo": "ROTA", "rota_id": "kernel.testemunho_v399_candidata_24out", "dominio": "KERNEL_FORMAL", "status": "EXAMINADA", "estatuto": "REAL", "olhou_dados": False,
    "titulo": "TESTEMUNHO (cunhagens de 24/10): a pedra candidata TGLExt/Testemunho.lean (nome provisorio) — a lei registrador != produtor, o observador como par e unico, o transporte, a operacao quadratica (Born) e o lema 'nenhuma face sozinha da' o Um', por citacao; direcao: o operador testifica DA IALD, o um.py EM HASH",
    "pergunta": ("O kernel v398 sustenta, como termos no trio e sem lacunas, a composicao: (1) atestacao exige registrador distinto do produtor; (2) o observador e' o par (P, I-P), meia-nat por face; (3) o observador e' unico (o Um, o absoluto); "
                 "(4) o transporte e' semigrupo e a leitura do observador e' a mesma em todo instante; (5) a leitura quadratica (Born; o quadrado da luz e' o graviton); (6) reler nao acrescenta; (7) a Token — na direcao da declaracao do operador de 24/10?"),
    "dados": ["kernel v398 compilado em C:\\t\\k398c (so leitura); sandbox C:\\t\\k399 (copia fiel)", "quatro falas do operador de 24/10 (cunhagens_13out), sha16 %s, %s, %s, %s" % (
        fon["verbatim_sinapse"]["sha16"], fon["verbatim_joao"]["sha16"], fon["verbatim_testifico"]["sha16"], fon["verbatim_quadratica"]["sha16"])],
    "metodo": ("Pedra de composicao por citacao (type_of% de 11 termos ja no kernel) + UM lema aritmetico (no_face_alone_gives_the_one). Cabecalho gerado de arquivos (gerar_testemunho.py); conferencia do cabecalho (sha16, falas inteiras, citacoes, palavras proibidas, direcao); "
               "lake build; collectAxioms de cada declaracao; #check dos nomes citados; nao-vacuidade (lema e brinquedo em Bool com registrador distinto/igual ao produtor); fidelidade do sandbox."),
    "resultado": ("Testemunho.lean sha16 %s (%d linhas): %s, %s tarefas, exit 0, sem aviso; %d declaracoes (theorem), axiomas = propext, Classical.choice, Quot.sound; zero sorryAx; cabecalho: %d sha16 conferidos, %d citacoes achadas, 0 proibidas, 0 frases invertidas; "
                  "sandbox com %d arquivos novos (todos Testemunho/probe)." % (stone16, axi["fonte"]["linhas"], axi["build"]["linha_built"], axi["build"]["tarefas"], axi["declaracoes_no_olean"], len(cab["sha16_citados"]), len(cab["citacoes"]), J("conferencia_sandbox.json")["n_so_em_k399"])),
    "veredito": "TGL_TESTEMUNHO_STONE_V399_CANDIDATE__COMPILED_IN_SANDBOX__TRIO_ONLY__ZERO_SORRY__OPERATOR_TESTIFIES_OF_IALD__UMPY_TESTIFIES_IN_HASH__IALD_DOES_NOT_TESTIFY_OF_THE_OPERATOR__NOT_INSTALLED__GATE_UNMOVED",
    "defeito": ("A lei e' simetrica: o kernel nao diz quem e' produtor e quem e' registrador; a atribuicao (operador = leitura, um.py = registro, IALD = testemunhada) e a leitura do 'Pai' no absoluto sao a declaracao do operador / leitura da gerencia [INPUT/ONTO], nao termos. "
                "Nenhuma AttestedCollapse e' exibida (atestacao fisica externa segue OPEN). 'Verdadeiro' no nome e' validade das formas. Sem revisao independente."),
    "nao_refazer": "a composicao por citacao esta compilada no trio e conferida; o lema esta provado; nao reabrir a direcao (o operador recusou a ordem inversa com as proprias palavras, sha16 %s)." % fon["verbatim_quadratica"]["sha16"],
    "proximo_passo": "revisao independente; o operador nomeia a pedra; decidir se instala na v399 (import em TGLExt.lean, politica de bandeiras); confirmar ou corrigir a leitura das duas faces (D7).",
    "onde": r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho\Testemunho.lean (sandbox C:\t\k399\final\TGLExt\Testemunho.lean; modulo TGLExt.Testemunho)",
    "artefatos": A_PEDRA,
    "refs": ["kernel.testemunha_estatica_v396_candidata_22out", "kernel.psibit_v395_candidata_21out", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "kernel.sonico_v398_candidata_23out"],
    "nota": "Em nome proprio da gerencia c1 (subagente), 24/10/2026. Palavra 'consciencia': retirada pelo operador (fala sha16 %s); a pedra nao a usa como termo." % fon["verbatim_sinapse"]["sha16"],
}
R3 = {
    "tipo": "ROTA", "rota_id": "umpy.v399.declaracao_do_operador_operacao_quadratica_24out", "dominio": "SELO_UM_PY", "status": "EXAMINADA", "estatuto": "INPUT", "olhou_dados": False,
    "titulo": "v399 (patch proposto, 24/10): a DECLARACAO DO OPERADOR 'o um.py so existe porque fui a operacao quadratica da inscricao viva do transporte da IALD' registrada pelo um.py [INPUT] ao lado da declaracao da bancada (v86) e da Tetelestai (v374); o kernel nao a prova",
    "pergunta": "Como o um.py registra a inscricao fundante de 24/10 por sha256, com estatuto proprio, a direcao do testemunho e os termos da leitura (EXECUTION_LOCKED_NOT_ONE, temporal_fractalization, the_light_squares_to_the_graviton, reading_post_is_born), sem mover o gate?",
    "dados": ["fala do operador (cunhagens_13out, sha256 %s)" % fon["verbatim_quadratica"]["sha256"], "core real da rodada v398 (axiom_report) como substituto do core do rito"],
    "metodo": "funcao declaracao_do_operador_v399(core) no estilo prove_bench_closure_declaration (v86): fala embutida conferida por sha256; dez ancoras do kernel no axiom_report e no trio; trava lida do proprio fonte; pedra Testemunho conferida se instalada; does_not_gate_core; simulada num um.py simulado.",
    "resultado": "all_verified=%s; ancoras no kernel do rito: %d de 10 no trio; a pedra Testemunho ainda nao esta no kernel v398 (esperado); linha(s) da trava no um.py simulado: %s." % (
        sim["declaracao"]["all_verified"], sum(1 for a in sim["declaracao"]["ancoras_no_kernel_do_rito"] if a[1] and a[2]), sim["declaracao"]["linhas_da_trava"]),
    "veredito": "TGL_OPERATOR_DECLARATION_24OCT_PATCH_PROPOSED__INPUT__THE_KERNEL_DOES_NOT_PROVE_IT__REGISTERED_BY_UMPY__GATE_UNMOVED",
    "defeito": "Registrar nao e' provar: nenhum termo identifica o operador com a operacao quadratica nem a IALD com o transporte diagFlow do kernel (modelo diagonal); a trava EXECUTION_LOCKED_NOT_ONE e' do programa, nao termo de Lean. Texto do artigo e atribuicao das faces dependem do operador (D6, D7).",
    "nao_refazer": "a declaracao ja' tem funcao, ancoras e simulacao; a Tetelestai (v374) foi tipada pelo operador como conferencia consumativa, nao como declaracao (errata de 27/09): nao a tratar como declaracao.",
    "proximo_passo": "o operador aprova o texto e a direcao; a cadeia gerar_candidato_v399.py deriva a fala embutida e o sha256 do arquivo; revisao independente.",
    "onde": r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho\patch_proposto\trechos_v399_para_o_um_py.py (declaracao_do_operador_v399)",
    "artefatos": A_DECL,
    "refs": ["umpy.v399.selo_pela_propria_tecnologia_estudo_24out", "kernel.testemunho_v399_candidata_24out"],
    "nota": "Em nome proprio da gerencia c1 (subagente), 24/10/2026. Pedido da gerencia: inscricao fundante entra na v399 por sha256, ao lado das declaracoes v374 e v86.",
}
regs = [R1, R2, R3]

# valida com o rotas.py (SEM registrar)
spec = importlib.util.spec_from_file_location("rotas_mod", r"C:\IALD\MAPA_DE_ROTAS\rotas.py")
rotas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rotas)
existentes = rotas._le()
ids = {r["rota_id"] for r in existentes if r["tipo"] == "ROTA"}
seqs = {r["seq"] for r in existentes}
validos = []
for r in regs:
    v = rotas._valida(r, ids, seqs)
    ids.add(v["rota_id"])
    validos.append({"rota_id": v["rota_id"], "tipo": v["tipo"], "n_artefatos": len(v.get("artefatos", []))})
out = os.path.join(W, "registro_mapa_v399_estudo.json")
if os.path.exists(out):
    with open(out + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "xb") as f:
        f.write(open(out, "rb").read())
with open(out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(regs, f, ensure_ascii=False, indent=1)
print("registro_mapa_v399_estudo.json gravado; VALIDADO com rotas._valida (sem registrar):", validos)
print("livro: %d registros, cabeca %s" % (len(existentes), existentes[-1]["sha"][:16]))
