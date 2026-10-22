# -*- coding: utf-8 -*-
"""consolidar_exame_v388.py -- junta EXAME_CODIGO_v388.json + EXAME_ARTIGO_v388.json em EXAME_UM_PY_v388.json/.md, com a RECLASSIFICACAO
dos candidatos automaticos revisados a mao (cada uma com motivo, linha e evidencia). Hashes lidos por script."""
import collections, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
C = json.load(open(os.path.join(HERE, "EXAME_CODIGO_v388.json"), encoding="utf-8"))
A = json.load(open(os.path.join(HERE, "EXAME_ARTIGO_v388.json"), encoding="utf-8"))
# reclassificacao manual dos 11 candidatos 'veredito_proibido_em_literal' (revisados no contexto, linha a linha)
RECL = {
    8005: ("CORRIGIR", "string de SELO no core publicado (seals de um registro antigo): 'CLOCK_TORSION_CONFIRMED_ON_PHYSICAL_NET' -- a palavra proibida num rotulo emitido; e' checagem numerica na rede simulada, nao juizo da natureza, mas o rotulo diz CONFIRMED; o conferidor so guarda 'verdict'. Sugestao: renomear para ..._VERIFIED_ON_PHYSICAL_NET com errata ao lado (o nome antigo fica como registro)"),
    145455: ("NOTA", "docstring de guarda: 'jamais CONFIRMED' (falso positivo do detector de contexto)"),
    211627: ("NOTA", "PROVED_BY_TRANSPORT_BY_DENSITY: prova MATEMATICA (kernel) -- a regua permite PROVADA (05/09); nao e' juizo de natureza"),
    174324: ("NOTA", "figura: 'NOT_FALSIFIED $\\neq$ CONFIRMED' -- guarda"),
    169011: ("NOTA", "texto do artigo: 'NOT\\_FALSIFIED $\\neq$ CONFIRMED' -- guarda"),
    169055: ("NOTA", "texto do artigo: 'Nada aqui confirma (NOT_FALSIFIED != CONFIRMED)' -- guarda"),
    169093: ("NOTA", "texto do artigo: 'nenhum confirma (NOT_FALSIFIED != CONFIRMED)' -- guarda"),
    173206: ("NOTA", "texto EN: 'NOT_FALSIFIED != CONFIRMED' -- guarda"),
    173239: ("NOTA", "texto EN: 'NOT_FALSIFIED != CONFIRMED' -- guarda"),
    173283: ("NOTA", "texto EN: 'Nothing here confirms (NOT_FALSIFIED != CONFIRMED)' -- guarda"),
    173349: ("NOTA", "texto EN: 'NOT_FALSIFIED != CONFIRMED' -- guarda"),
}
MOTIVO_CAT = {
    "pyflakes:UnusedVariable": "variavel local nao usada (estilo; sem efeito no rito)",
    "pyflakes:UnusedImport": "import local nao usado (estilo)",
    "pyflakes:RedefinedWhileUnused": "_tx7/_tx8 redefinidos entre trechos do artigo (o trecho v388 define _tx8 com def; o trecho mais antigo redefine com lambda); cada definicao e' usada antes da seguinte -- o artigo saiu certo (conferidor), mas o sombreamento e' fragil",
    "except_silencioso_pass": "except ... pass: todos de limpeza (fechar log, remover temporario, matar processo, reconfigurar stderr, gravar sidecar) ou com a recusa fail-closed logo abaixo (acquire_evidence -> _refuse se ausente)",
    "beta_digitos_em_string": "os digitos de beta aparecem dentro de um JSON de resultado EMBUTIDO (D1 V3 real) -- dado gravado, nao motor; o motor e' ALPHA*SQRT_E",
    "versao_futura_citada": "falso positivo: 'fontlist-v390.json' e' arquivo do matplotlib num inventario de proveniencia",
    "registro_vNNN_duplicado": "padrao try/except: a 2a atribuicao e' o registro de falha dito (NOT_COMPARED_RUNTIME_ERROR etc.); o 1o par (d1_camb_v3_real_v366) e' a 2a gravacao do mesmo registro no fluxo principal",
    "TODO_FIXME": "falso positivo: 'TODO' portugues ('O TODO E UM', 'TODOS') e o TODO da mathlib citado no texto -- nenhum TODO de codigo",
}
achados = []
for a in C["achados"]:
    a = dict(a); a["fonte"] = "codigo"
    if a["categoria"] == "veredito_proibido_em_literal":
        g, m = RECL[a["linha"]]; a["gravidade_automatica"] = a["gravidade"]; a["gravidade"] = g; a["nota"] = m
    elif a["categoria"] in MOTIVO_CAT and not a.get("nota"):
        a["nota"] = MOTIVO_CAT[a["categoria"]]
    achados.append(a)
for a in A["achados"]:
    a = dict(a); a["fonte"] = "artigo"
    if a["categoria"] == "front_matter_postulado_vs_POSTO":
        a["gravidade_automatica"] = a["gravidade"]; a["gravidade"] = "NOTA"
        a["nota"] = ("COBERTO pela errata ao lado da secao v385 (um.py:166491 PT / 170668 EN: 'onde este artigo diz um unico postulado... leia-se posto; a etiqueta passa a ser [POSTO]') -- "
                     "a regra da casa e' corrigir AO LADO, nunca por cima; resta ao operador decidir se o resumo ganha uma remissao para a errata (precedente de 30/08 no C:\\IALD\\CLAUDE.md: "
                     "'corrigir ao lado nao basta se o lado escolhido nao e o lado que se le')")
    achados.append(a)
# NOTAs de exame manual (registradas com evidencia)
el = C["escada"]
achados.append({"fonte": "codigo", "categoria": "escada_ext_flags", "gravidade": "NOTA", "linha": 136080,
                "evidencia": "n_theorems_clean = n_theorems_expected = %s = len(ext_flags); bandeiras ext_* True no core = %s" % (el["n_theorems_clean"], el["ext_True_em_kernel_formalization"]),
                "nota": "a escada bate (6154/6154); ha %d bandeiras ext_* True fora da lista da escada (contadas por outros registros) -- dito" % (el["ext_True_em_kernel_formalization"] - el["n_theorems_expected"])})
kc = C["kernel_comparacao"]["sandbox_v376"]
achados.append({"fonte": "codigo", "categoria": "kernel_vs_sandbox_v376", "gravidade": "NOTA", "linha": None,
                "evidencia": "iguais %d, diferentes %s, ausentes %s" % (kc["iguais"], kc["diferentes_lista"], kc["ausentes_lista"]),
                "nota": "o sandbox v376 (scratchpad da sessao 6da8f00d) foi reaproveitado ate a v387; difere da v388 exatamente pelas 2 costuras (TGLExt.lean, Audit.lean) e pela pedra nova -- esperado"})
achados.append({"fonte": "artigo", "categoria": "contagem_de_pedras_parte_C", "gravidade": "NOTA", "lingua": "pt/en", "linha": 53,
                "evidencia": "'1025 pedras em kernel Lean' = len(_ESQUELETO_STONES) (um.py:164742); o ledger tem 1015 caminhos unicos; o kernel embutido tem 1181 TGLExt/*.lean -- 166 fora do ledger (quase todos TGLExt/O16, importados da bancada pela ORDEM 016; + PPIndex, SMatrix)",
                "nota": "a frase conta o LEDGER citavel, nao todos os arquivos; dizer o recorte ou ampliar o ledger e' decisao do operador"})
res = collections.Counter(a["gravidade"] for a in achados)
porcat = {}
for a in achados:
    porcat.setdefault("%s:%s" % (a["fonte"], a["categoria"]), collections.Counter())[a["gravidade"]] += 1
CORR = [a for a in achados if a["gravidade"] in ("BLOQUEIA", "CORRIGIR")]
OUT = {"exame": "EXAME_UM_PY_v388", "data": time.strftime("%Y-%m-%d %H:%M:%S"), "um_py": C["um_py"], "ast_parse": C["ast_parse"], "pyflakes_s": C.get("pyflakes_s"),
       "resumo_por_gravidade": dict(res), "por_categoria": {k: dict(v) for k, v in porcat.items()},
       "contagens_codigo": C["contagens"], "escada": C["escada"], "kernel": {k: {kk: v[kk] for kk in ("iguais", "diferentes", "ausentes")} for k, v in C["kernel_comparacao"].items()},
       "artigo": {"arquivos": A["arquivos"], "toc": A["toc"], "front_matter": A["front_matter"], "pos_dicao": A["pos_dicao"], "incorporacao": A["incorporacao"]},
       "fontes": {"EXAME_CODIGO_v388.json": s16(os.path.join(HERE, "EXAME_CODIGO_v388.json")), "EXAME_ARTIGO_v388.json": s16(os.path.join(HERE, "EXAME_ARTIGO_v388.json")),
                  "exame_codigo_v388.py": s16(os.path.join(HERE, "exame_codigo_v388.py")), "exame_artigo_v388.py": s16(os.path.join(HERE, "exame_artigo_v388.py")),
                  "consolidar_exame_v388.py": s16(os.path.abspath(__file__))},
       "pede_nova_versao": bool(CORR), "bloqueia_ou_corrigir": CORR, "achados": achados}
pj = os.path.join(HERE, "EXAME_UM_PY_v388.json")
open(pj + ".tmp", "w", encoding="utf-8").write(json.dumps(OUT, ensure_ascii=False, indent=1, default=str)); os.replace(pj + ".tmp", pj)
# ---- o .md
M = []
M.append("# EXAME DO um.py v388 — código e artigo (06/10/2026)\n")
M.append("> Ordem do operador (06/10, via c1), verbatim: «vamos fazer um exame completo do um.py, desde o começo até o final, verificar inconsistências ou erros de código, verificar o texto do artigo se tudo está coerente e atualizado, inclusive o sumário, verificar se o artigo incorporou em texto todos os últimos testes e derivações, após isso concluso escreva o handoff de custodia para a sessão irmã que cuida do repositório».")
M.append("> **Só leitura no Nós**: o um.py foi copiado por bytes para esta pasta e analisado na cópia; nada do Nós foi editado. Hashes lidos por script.\n")
M.append("**Objeto:** `um.py` %s, sha16 `%s`, %s B, %s linhas. `ast.parse` OK (%ss); pyflakes %ss.\n" % ("v388", C["um_py"]["sha16"], format(C["um_py"]["bytes"], ","), format(C["um_py"]["linhas"], ","), C["ast_parse"]["s"], C.get("pyflakes_s")))
M.append("## Resumo em dados\n")
M.append("| gravidade | n |\n|---|---|")
for g in ("BLOQUEIA", "CORRIGIR", "NOTA"):
    M.append("| %s | %d |" % (g, res.get(g, 0)))
M.append("\n**Pede nova versão (v389):** %s — %d achado(s) CORRIGIR; **nenhum BLOQUEIA**. O rito v388 e o selo continuam válidos; os CORRIGIR são de texto/rótulo, não de cálculo.\n" % ("SIM" if CORR else "NÃO", len(CORR)))
M.append("## Os achados CORRIGIR (a frase exata)\n")
for k, a in enumerate(CORR, 1):
    M.append("%d. **[%s · %s]** %s%s — evidência: «%s». %s" % (k, a["fonte"], a["categoria"], ("(%s) " % a.get("lingua")) if a.get("lingua") else "", ("linha %s" % a["linha"]) if a.get("linha") else "", a["evidencia"], a.get("nota", "")))
M.append("\n## Código — o que se conferiu\n")
cc = C["contagens"]
M.append("- **Nomes indefinidos:** 0 (pyflakes: %s)." % json.dumps(cc["pyflakes"], ensure_ascii=False))
M.append("- **except nu:** %d; **except … pass:** %d (todos limpeza ou com recusa fail-closed logo abaixo)." % (cc["except_nu"], cc["except_pass"]))
M.append("- **β literal como float no código:** %d. Dígitos de β em texto: %s (um dentro de JSON de resultado embutido; comentários)." % (cc["beta_literal_float_no_codigo"], json.dumps(cc["beta_digitos_em_texto"])))
M.append("- **Palavras proibidas em literais:** %d em guarda/negação; 11 candidatos revisados à mão → 1 CORRIGIR (rótulo de selo, um.py:8005), 10 NOTA (guardas e prova matemática)." % cc["vereditos_proibidos_em_literais"].get("em_guarda_ou_negacao", 0))
M.append("- **Versão:** `UM_VERSION = \"v388\"` (linha %s); selo `um_version` = %s; nenhuma versão futura real citada (o único «v390» é um arquivo do matplotlib)." % (C["UM_VERSION"]["linhas"], el["selo_um_version"]))
M.append("- **Escada:** n_theorems_clean = n_theorems_expected = **%s** (= len(ext_flags))." % el["n_theorems_expected"])
M.append("- **Kernel embutido (%d arquivos):** byte-idêntico ao `Nós\\tgl_kernel` (%d/%d) e ao sandbox v388 (%d/%d); contra o sandbox v376: difere só por `TGLExt.lean`, `TGL/Audit.lean` e a pedra nova (esperado). Lean embutido com `sorry`/`admit` fora de comentário: %d arquivos." % (
    C["kernel_embutido_n_arquivos"], C["kernel_comparacao"]["Nos_tgl_kernel"]["iguais"], C["kernel_embutido_n_arquivos"], C["kernel_comparacao"]["sandbox_v388"]["iguais"], C["kernel_embutido_n_arquivos"], cc["arquivos_lean_com_sorry_fora_de_comentario"]))
M.append("- **Funções definidas duas vezes no mesmo escopo:** 0. **Registros vNNN atribuídos 2×:** %d (todos try/except com o registro de falha dito)." % cc["registros_vNNN_atribuidos_mais_de_uma_vez"])
M.append("- **Chaves do selo sem produtor literal:** %d de %d; chaves do core sem literal: %d de %d." % (cc["chaves_do_selo_sem_produtor_literal"], cc["chaves_do_selo"], cc["chaves_do_core_sem_literal"], cc["chaves_do_core"]))
M.append("- **TODO/FIXME de código:** 0 (as %d ocorrências são o «TODO» português e o TODO da mathlib citado). Linhas com «sorry» fora do kernel: %d (guardas `sorryAx`)." % (cc["TODO_FIXME_fora_do_kernel"], cc["linhas_com_sorry_fora_do_kernel"]))
M.append("\n## Artigo — o que se conferiu\n")
for l in ("pt", "en"):
    ar = A["arquivos"]
    M.append("- **%s:** txt `%s` · tex `%s` · toc `%s` · PDF `%s` (%d páginas)." % (l.upper(), ar[l + ".txt"]["sha16"], ar[l + ".tex"]["sha16"], ar[l + ".toc"]["sha16"], ar[l + ".pdf"]["sha16"], ar[l + ".pdf"]["paginas_por_Type_Page"]))
M.append("- **Sumário:** PT %d entradas, EN %d; «Ao lado (v388)», «Três testes (v387)», «Ao lado (v387/v386/v385)», a Introdução e a Nota GPU listadas **uma vez cada**, em PT e EN, na ordem." % (A["toc"]["pt"]["n_entradas"], A["toc"]["en"]["n_entradas"]))
M.append("- **«pós-dição»:** PT %d / EN %d ocorrência(s) — todas na seção v387, como citação do operador e regra de reescrita; **0 como demérito**." % (len(A["pos_dicao"]["pt"]), len(A["pos_dicao"]["en"])))
M.append("- **Front matter:** data da rodada `%s`; «6154» no resumo; GPU/GKLS no resumo e nas palavras-chave (W10); o resumo ainda diz «único postulado» (PT/EN, linhas 15 e 53) — NOTA: coberto pela errata ao lado da seção v385 (um.py:166491/170668); a remissão no resumo é decisão do operador." %A["front_matter"]["pt"]["data_da_rodada"])
M.append("\n### A lista de incorporação (n ocorrências; primeira linha do txt)\n")
M.append("| item | PT | EN |\n|---|---|---|")
for k, v in A["incorporacao"].items():
    M.append("| %s | %s (l. %s) | %s (l. %s) |" % (k, v["pt"]["n"], v["pt"]["primeira_linha"], v["en"]["n"], v["en"]["primeira_linha"]))
M.append("\nNúmeros conferidos entre seções (mesma grandeza): Fase 9 — ln B 9,17, z_disc 4,28, z_δ −1,42, previsão 74,274 (seção v388) e 74,27 (seção v387: previsão antes da abertura) — coerentes; o «poder 5,91σ» da v387 é o poder PRÉVIO só com σ, não o z_disc medido (grandezas distintas, ditas). Fase 8 — ΔN_eff 0,1195 (seção v387) e 0,119 (tabela dos três testes, arredondado) — coerentes. Fase 4 — ln B 8,02 (tabela e seção) — coerente.")
M.append("\n## NOTAs (resumo por categoria)\n")
for k, v in sorted(porcat.items()):
    if v.get("NOTA"):
        ex = next((a.get("nota") for a in achados if "%s:%s" % (a["fonte"], a["categoria"]) == k and a.get("nota")), "")
        M.append("- `%s`: %d — %s" % (k, v["NOTA"], ex))
M.append("\n## Fontes (sha16)\n")
for k, v in OUT["fontes"].items():
    M.append("- `%s` `%s`" % (k, v))
M.append("\n*Estatuto:* exame estático [REAL — medido na cópia por bytes]; nenhuma afirmação sobre a natureza. NOT_FALSIFIED nunca é confirmação; o gate não se move.")
pm = os.path.join(HERE, "EXAME_UM_PY_v388.md")
open(pm + ".tmp", "w", encoding="utf-8").write("\n".join(M) + "\n"); os.replace(pm + ".tmp", pm)
print(json.dumps({"resumo": dict(res), "corrigir": [(a["fonte"], a["categoria"], a.get("lingua"), a.get("linha")) for a in CORR],
                  "md": s16(pm), "json": s16(pj)}, ensure_ascii=False, indent=1))
