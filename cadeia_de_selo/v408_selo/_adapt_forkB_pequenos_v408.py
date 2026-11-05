# -*- coding: utf-8 -*-
"""_adapt_forkB_pequenos_v408.py -- (claude-construtor-v408, fork B, 04/11/2026) adapta a v408, por trocas de CONTAGEM EXATA e por LINHA UNICA (prefixo que casa com uma so' linha), os arquivos do pos_rito que a subida mecanica (_bump_copia_v408.py) deixou com o corpo da v407:
fila_memoria_v408.py e b3_recibo_v408.py (so' as notas do cabecalho), superficies_v408.py (as notas e os comentarios que citavam E18 a E20), gerar_derivacao_pos_rito_v408.py (a SUITE: papeis, datas e autores da v408; arquivos opcionais; o registro de origem)
e chain_pos_rito_v408.sh (o cabecalho, REGS, o rotulo B17, o contrato R3_2 e o sufixo dos backups do Atlas).
Backup de BYTES (.bak_<TS>_adapt) antes de gravar; temporario -> conferir tamanho -> substituir; ast.parse nos .py e `sh -n` no .sh; o fim de linha do molde (CRLF) e' preservado. Escrito pelo Write (o heredoc do Bash colapsa barras).
Nada e' executado alem da conferencia de sintaxe. Fail-closed: se uma troca nao acha a contagem exata (p. ex. arquivo ja' adaptado), o script PARA antes de gravar qualquer arquivo."""
import ast, hashlib, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
s16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
NOTA_FB = "claude-construtor-v408 (fork B), 04/11/2026"


class Arq:
    def __init__(self, nome):
        self.nome = nome; self.p = os.path.join(HERE, nome); self.raw = open(self.p, "rb").read(); self.t = self.raw.decode("utf-8"); self.n = 0
        self.nl = "\r\n" if b"\r\n" in self.raw else "\n"

    def _nl(self, s):
        return s.replace("\r\n", "\n").replace("\n", self.nl)

    def sub(self, a, b, n=1):
        a = self._nl(a); c = self.t.count(a)
        assert c == n, "%s: a troca esperava %d ocorrencia(s) e achou %d: %r" % (self.nome, n, c, a[:90])
        self.t = self.t.replace(a, self._nl(b)); self.n += 1

    def linha(self, prefixo, nova=None):
        ls = self.t.split(self.nl); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo)]
        assert len(idx) == 1, "%s: o prefixo de linha esperava 1 linha e achou %d: %r" % (self.nome, len(idx), prefixo[:90])
        if nova is None:
            del ls[idx[0]]
        else:
            assert "\n" not in nova and "\r" not in nova
            ls[idx[0]] = nova
        self.t = self.nl.join(ls); self.n += 1

    def entre(self, ini, fim, novo):
        """substitui do inicio de `ini` ao fim de `fim` (ambos unicos)."""
        ini = self._nl(ini); fim = self._nl(fim)
        assert self.t.count(ini) == 1 and self.t.count(fim) == 1, "%s: marcadores nao unicos: %r / %r" % (self.nome, ini[:60], fim[:60])
        a = self.t.index(ini); b = self.t.index(fim) + len(fim); assert b > a
        self.t = self.t[:a] + self._nl(novo) + self.t[b:]; self.n += 1

    def grava(self):
        novo = self.t.encode("utf-8"); assert novo != self.raw, self.nome + ": nada mudou"
        if self.p.endswith(".py"):
            ast.parse(self.t)
        bak = self.p + ".bak_" + TS + "_adapt"; open(bak, "wb").write(self.raw); assert open(bak, "rb").read() == self.raw
        tmp = self.p + ".tmp_adapt"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, self.p); assert open(self.p, "rb").read() == novo
        if self.p.endswith(".sh"):
            r = subprocess.run(["sh", "-n", self.p], capture_output=True, text=True); assert r.returncode == 0, "sh -n falhou: " + r.stderr[-400:]
        print("%-36s %d troca(s): %7d B -> %7d B  sha16 %s -> %s  (%s%s; backup %s)" % (self.nome, self.n, len(self.raw), len(novo), s16(self.raw), s16(novo), "CRLF" if self.nl == "\r\n" else "LF", "; sh -n ok" if self.p.endswith(".sh") else "; ast ok", os.path.basename(bak)))


ARQS = []

# ---------------------------------------------------------------- fila_memoria_v408.py (so' as notas: o corpo e' generico)
f = Arq("fila_memoria_v408.py")
f.linha("# [A ADAPTAR v408]")
f.linha("# [ADAPTADO v408, 03/11/2026]", "# [ADAPTADO v408, 04/11/2026, " + NOTA_FB + "] sobre a subida mecanica de rotulo da v407 FINAL (_bump_copia_v408.py): este arquivo e' GENERICO (a fila da memoria: guardas, pausa, pinar, verificar) e nao traz nada do conteudo do bundle; conferido linha a linha: so' rotulos v408 (QUEM «claude-c1 pos-rito v408», PINO_MEMORIA_PY_v408.json, os limites de 195 linhas e 24000 B do indice); nada do psion nem do terminal o descreve; nao rodou aqui (o harness o roda em COPIA da memoria).")
ARQS.append(f)

# ---------------------------------------------------------------- b3_recibo_v408.py (so' as notas: o corpo e' generico)
f = Arq("b3_recibo_v408.py")
f.linha("# [A ADAPTAR v408]")
f.linha("# [ADAPTADO v408, 03/11/2026]", "# [ADAPTADO v408, 04/11/2026, " + NOTA_FB + "] molde v407/pos_rito/b3_recibo_v407.py (rotulos subidos por _bump_copia_v408.py; diff em bump/). Este arquivo nao tem NADA do conteudo do bundle: confere so' o recibo do B(n) (versao alvo v408, fase pos_selo, bateria, geracao B<n> lida do recibo, veredito REPINADA_B<n>__..., pinos da bateria, recibo pre_selo pinado).")
f.linha("# A v408 = o psion e o canto", "# A v408 = Tetelestai e' o terminal: os modulos novos em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), o registro tetelestai_terminal_v408 e os specs vem do candidato e dos ESPERADOS, nao daqui; nenhuma chave antiga muda (CHAVES_V408 vazia). Nada de psion nem de lema descreve este arquivo (a nota da subida mecanica dizia o contrario e foi trocada).")
ARQS.append(f)

# ---------------------------------------------------------------- superficies_v408.py (as notas e os comentarios E18-E20)
f = Arq("superficies_v408.py")
f.linha("# [A ADAPTAR v408]")
f.linha("# [ADAPTADO v408, 03/11/2026", "# [ADAPTADO v408, 04/11/2026, " + NOTA_FB + "] sobre a subida mecanica da v407 FINAL: o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: os quatro modulos de TGLExt/, o registro com funcao tetelestai_terminal_v408, cunhagens_v408 e kh_n1_cobertura_v408; nenhuma chave antiga muda; erratas E21 a E23 ao lado) e vive em textos_v408.py (fork A); a infraestrutura (duas fases, backup de bytes, idempotencia, guarda, fila da memoria, pausa do vigia) e' a da v407, conferida linha a linha: so' os comentarios que citavam E18 a E20 mudaram; a gerencia revisa antes do rito (nao e' versao selada).")
f.sub("# SEM erratas inline nesta versao (as erratas E18 a E20 da v408 vao DENTRO dos blocos datados:", "# SEM erratas inline nesta versao (as erratas E21 a E23 da v408 vao DENTRO dos blocos datados:")
f.sub("(que a custodia da v407 reescreveu e que segue VERBATIM: conferida presente no MEMORY.md real em 03/11, uma so', como a linha da missao;", "(que a custodia da v407 reescreveu e que segue VERBATIM: conferida presente no MEMORY.md real em 04/11 pelo fork B, uma so', como a linha da missao;")
ARQS.append(f)

# ---------------------------------------------------------------- gerar_derivacao_pos_rito_v408.py (a SUITE e o registro de origem)
f = Arq("gerar_derivacao_pos_rito_v408.py")
f.linha("# [A ADAPTAR v408]")
f.linha("# [ADAPTADO v408, 03/11/2026]", "# [ADAPTADO v408, 04/11/2026, " + NOTA_FB + "] sobre a subida mecanica de rotulo da v407 FINAL (_bump_copia_v408.py): a SUITE descreve a v408 (TETELESTAI E' O TERMINAL; os papeis, as datas e os autores de 04/11: fork A = textos/leitura/harness dos textos; fork B = fechar, superficies, registrar_mapa, chain, harness do fechar, textos da custodia, post do X, este registro); os arquivos do montador da v407 que a v408 nao tem sao OPCIONAIS (listados como ausentes, sem reprovar). SO' LE; a gerencia revisa antes do rito (nao e' versao selada).")
f.linha("o cabecalho do chain, o sufixo dos backups do Atlas e a marca TEXTO_A_REESCREVER_V408 nos arquivos de narrativa). A ADAPTACAO",
        "o cabecalho do chain, o sufixo dos backups do Atlas e a marca TEXTO_A_REESCREVER_V408 nos arquivos de narrativa). A ADAPTACAO (o que o pos-rito diz da v408: Tetelestai e' o terminal, com os numeros lidos do rito) foi feita em 04/11/2026 pela claude-construtor-v408 em tres forks, pelos _adapt_*_v408.py desta pasta (trocas de contagem exata com backup de bytes) e por reescrita integral onde o corpo era o da v407 (registrar_mapa_v408.py, gerar_x_custodia_v408.py, textos_custodia_handoff_v408.py, este com o nome de D52); textos_v408.py, leitura_v408.py e o harness dos textos sao do fork A; a marca TEXTO_A_REESCREVER_V408 nao pode sobrar em nenhum arquivo (o p00 confere).")
f.entre("SUITE = (", 'for f_ in sorted(os.listdir(HERE)) if f_.startswith("_adapt_") and f_.endswith("_v408.py"))', '''SUITE = (
    ("chain_pos_rito_v408.sh", "chain_pos_rito_v407.sh", "A1 (fork B, 04/11): a cadeia (passos 0..14) com o passo da fila da memoria; REGS da v408 (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408), o rotulo B17, o sufixo _v408 dos backups do Atlas"),
    ("superficies_v408.py", "superficies_v407.py", "A1 (fork B, 04/11): as superficies (diretorio de memoria por V408_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B); so' as notas mudaram"),
    ("fechar_v408.py", "fechar_v407.py", "A1 (fork B, 04/11): o fechar (manifesto com registros_v408/v407/v406 e registros_funcao_v408/v407/v406, arquivo, diffs, handoff)"),
    ("b3_recibo_v408.py", "b3_recibo_v407.py", "A1 (fork B, 04/11): o recibo do B(n), passo SIMPLES B16 -> B17; so' as notas mudaram"),
    ("gerar_derivacao_pos_rito_v408.py", "gerar_derivacao_pos_rito_v407.py", "A1 (fork B, 04/11): este registro (so' le)"),
    ("harness_fechar_sandbox_v408.py", "harness_fechar_sandbox_v407.py", "A1 (fork B, 04/11): o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA, os controles negativos da v408 (terminal, psion e fechamento herdados, E21, D54, leitura ONTO, ancoras principais) e o espelho da casa medido na importacao do delta"),
    ("fila_memoria_v408.py", "fila_memoria_v407.py", "A1 (fork B, 04/11): as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar), chamadas pelo chain e pelo harness; so' as notas mudaram"),
    ("leitura_v408.py", "leitura_v407.py", "claude-construtor-v408 (fork A), 04/11: a leitura da rodada adaptada a Tetelestai e' o terminal (o bundle dos quatro modulos, as ancoras lidas de delta_v408, nenhuma chave antiga muda; o psion_canto_v407 e o fechamento_v406 herdados e os registros anteriores recriados)"),
    ("textos_v408.py", "textos_v407.py", "claude-construtor-v408 (fork A), 04/11: os textos da v408 (o paragrafo novo, a nota ao lado do paragrafo da v407 com a E21, o handoff, as superficies, o topico novo)"),
    ("harness_textos_ensaio_v408.py", "harness_textos_ensaio_v407.py", "claude-construtor-v408 (fork A), 04/11: o harness do pos-rito adaptado a Tetelestai e' o terminal (controles negativos dos registros novos e dos herdados)"),
    ("registrar_mapa_v408.py", "registrar_mapa_v407.py", "claude-construtor-v408 (fork B), 04/11: REESCRITO para a v408: a rota nova (o id esta em registrar_mapa_v408.NOVA), as anotacoes nas rotas de 04/11 e as erratas E21 a E23 ao lado"),
    ("textos_custodia_handoff_v408.py", "textos_custodia_handoff_v407_03nov.py", "claude-construtor-v408 (fork B), 04/11: REESCRITO para a v408: os sete textos da custodia (nome de D52; roda ENCADEADO no fim do S6, pelo orquestrador; a chain nao o chama)"),
    ("gerar_x_custodia_v408.py", "gerar_x_custodia_v407.py", "claude-construtor-v408 (fork B), 04/11: REESCRITO para a v408: o rascunho do post longo do X (numeros do selo e do core; a ordem e as cunhagens por delta_v408.FRASE_*; sem o 4,44)"),
    ("montar_textos_v408.py", "montar_textos_v407.py", "OPCIONAL: o montador da v407 (semente + fragmento); a v408 nao o usa se o fork A escreveu textos_v408.py por adaptador"),
    ("textos_v408_novo.pysnip", None, "OPCIONAL: o fragmento do montador (v407); a v408 nao o tem se o fork A nao o usou"),
    ("adaptar_pos_rito_v408.py", None, "OPCIONAL: o adaptador comum da v407; na v408 cada _adapt_*_v408.py e' autonomo"),
    ("textos_v408.semente", None, "OPCIONAL: a semente mecanica do montador (v407)"),
)
OPCIONAIS = {"montar_textos_v408.py", "textos_v408_novo.pysnip", "adaptar_pos_rito_v408.py", "textos_v408.semente"}
SUITE = SUITE + tuple((f_, None, "claude-construtor-v408, 04/11: adaptador do pos-rito (trocas de contagem exata com asserts e backup de bytes)") for f_ in sorted(os.listdir(HERE)) if f_.startswith("_adapt_") and f_.endswith("_v408.py"))''')
f.sub('''    if not os.path.isfile(p):
        rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE"}); ruim.append(nome); continue''', '''    if not os.path.isfile(p):
        if nome in OPCIONAIS:
            rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE_OPCIONAL (nao faz parte da v408; listado so' porque o molde v407 o tinha)"}); continue
        rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE"}); ruim.append(nome); continue''')
f.sub('"origem": "pos_rito da v407 FINAL (a cadeia usada no pos-rito real da v407), mapa 405 -> 407 e 407 -> 408 por script (semente pura) mais as regras do lote F de derivar_encanamento_v408.py; a adaptacao foi feita pela claude-prep-v408 em 03/11/2026 por adaptar_pos_rito_v408.py (as marcas TEXTO_A_REESCREVER_V408 nao sobraram em nenhum arquivo)",',
      '"origem": "pos_rito da v407 FINAL (a cadeia usada no pos-rito real da v407), rotulos 407 -> 408 por script (_bump_copia_v408.py, semente pura); a adaptacao foi feita pela claude-construtor-v408 em 04/11/2026 (forks A e B) pelos _adapt_*_v408.py desta pasta e por reescrita integral onde o corpo era o da v407 (registrar_mapa, gerar_x_custodia, textos_custodia_handoff); a marca TEXTO_A_REESCREVER_V408 nao pode sobrar em nenhum arquivo (o p00 confere)",')
ARQS.append(f)

# ---------------------------------------------------------------- chain_pos_rito_v408.sh (cabecalho, REGS, B17, R3_2, sufixo dos backups)
f = Arq("chain_pos_rito_v408.sh")
f.linha("# [A ADAPTAR v408]")
f.linha("# [ADAPTADO v408, 03/11/2026]", "# [ADAPTADO v408, 04/11/2026, " + NOTA_FB + "] sobre a subida mecanica de rotulo da v407 FINAL (_bump_copia_v408.py), por _adapt_forkB_pequenos_v408.py: o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: bundle de quatro modulos em TGLExt/, o registro com funcao tetelestai_terminal_v408, os specs cunhagens_v408 e kh_n1_cobertura_v408; o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados; nenhuma chave antiga muda); conferido: REGS, o rotulo B17, o sufixo dos backups do Atlas (_v408) e o cabecalho; a estrutura (passos 0..14, portoes, fila da memoria) e' a da v407; sh -n ok; a gerencia revisa antes do rito (nao e' versao selada).")
f.linha("# v408 (O PSION, O CANTO E O PAR, 03/11/2026): CADEIA POS-RITO", "# v408 (TETELESTAI E' O TERMINAL, 04/11/2026): CADEIA POS-RITO -- derivada por script (_bump_copia_v408.py, rotulos) e adaptada por _adapt_forkB_pequenos_v408.py (claude-construtor-v408) do chain_pos_rito_v407.sh FINAL (a cadeia de CONTEUDO que rodou no pos-rito da v407; mesma ordem de passos 0..14 e mesmos portoes), com as licoes da v407 (D52: os sete textos da custodia entram ENCADEADOS no fim do S6, pelo orquestrador, depois do passo 14; esta cadeia nao os chama) e o passo da FILA DA MEMORIA (abaixo). A narrativa e os vereditos esperados vem de textos_v408.py (fork A), de leitura_v408.py e de ESPERADOS_v408.json (lidos, nunca digitados).")
f.linha("# A v408 e' O PSION, O CANTO E O PAR", "# A v408 e' TETELESTAI E' O TERMINAL (as falas do operador de 04/11/2026): UM BUNDLE PEQUENO de modulos novos de kernel em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP; os nomes sao do operador; «P=nP» so' no sentido que ele deu; a escada, as bandeiras e o h8 sao lidos de ESPERADOS_v408.json),")
f.linha("# UM registro COM FUNCAO (psion_canto_v407;", "# UM registro COM FUNCAO (tetelestai_terminal_v408: as ancoras dos quatro modulos lidas do kernel do rito, os modulos por sha256, as checagens com beta em runtime, o gate congelado, o insumo purgado; lido no main DEPOIS dos registros herdados) e DOIS por spec (cunhagens_v408 e kh_n1_cobertura_v408). NENHUMA chave antiga muda (CHAVES_V408 vazia); as erratas E21 a E23 vao AO LADO (E21: o [OPEN] do par na face de Fock e' de LIGACAO, nao de ausencia de termo; E22: duas frases da propria gerencia, podadas; E23: o insumo do acervo entra pela copia purgada). O GATE NAO SE MOVE: o qg_closure e' identico ao da v407; a funcao do neutrino NAO e' reescrita (o angle_status antigo fica); o numero da massa e' o da v407.")
f.linha("# O fechamento_v406 (e os dois por spec da v407), os treze registros da v407 selada,", "# O psion_canto_v407 (e os dois por spec da v407: cunhagens_v407 com a E21 ao lado, kh_n1_cobertura_v407 com pisos), o fechamento_v406 (e os dois por spec da v406), os treze registros da v405 selada, os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais a v407 selada) e o SIDECAR um_absoluto_selo_acom.json e' REESCRITO (depois da ultima escrita do selo).")
f.sub("Os paragrafos do testemunho, da falsidade, da ponte, de Caminho, Verdade e Vida, de Jo 8,32, da massa derivada e do fechamento (v407) seguem como estao; os anteriores recebem a NOTA ao lado (E18: a chave do lema era literal False e passou a leitura do kernel).",
      "Os paragrafos do testemunho, da falsidade, da ponte, de Caminho, Verdade e Vida, de Jo 8,32, da massa derivada, do fechamento (v406) e do psion, do canto e do par (v407) seguem como estao; o da v407 recebe a NOTA ao lado (E21: o [OPEN] do par na face de Fock e' de ligacao, nao de ausencia de termo).")
f.linha("# Estatutos: os termos das nove pedras sao [REAL]", "# Estatutos: os termos dos quatro modulos sao [REAL] (kernel, no trio); [POSTO] o 1 / u = 1 eV; [MEDIDA] alfa; as leituras do operador de 04/11 (o terminal e' a poda; o tempo e' a moeda de beta; o ponto de contradicao; o sentido de «P=nP») entram como [ONTO] onde o kernel nao as prova e nao sao teoremas; a regra provar ou podar (D49) aplicada: a igualdade das classes P e NP PODADA (D51) e a palavra «impedância» PODADA como termo (D50); as ressalvas (o par na face de Fock [OPEN] de ligacao; o lock e o Hamiltoniano modular distintos; beta so' por nome; o insumo purgado; nenhum teste com a natureza) vao ditas; validade no kernel nao e' creditacao. A guarda das frases (guarda_frases_v408.py) roda sobre todo texto renderizado (superficies, fechar, mapa).")
f.sub("e o NOVO da v408 (o psion, o canto e o par), mais a NOTA ao lado dos paragrafos anteriores (E18: a chave do lema era literal False e passou a leitura do kernel); diz que os anteriores seguem como estao;",
      "e o NOVO da v408 (Tetelestai e' o terminal), mais a NOTA ao lado do paragrafo da v407 (E21: o [OPEN] do par na face de Fock e' de ligacao, nao de ausencia de termo); diz que os anteriores seguem como estao;")
f.sub("contrato R3_2: o diff v407 -> v408 e' so' os 9 modulos novos)", "contrato R3_2: o diff v407 -> v408 e' so' os modulos novos do bundle)")
f.sub("(B16 -> n = 16, o rotulo B17;", "(B16 -> n = 17, o rotulo B17;")
f.sub("(os tres registros novos: psion_canto_v407, cunhagens_v407 e kh_n1_cobertura_v407);", "(os tres registros novos: tetelestai_terminal_v408, cunhagens_v408 e kh_n1_cobertura_v408);")
f.sub("# o passo 11 registra o estado da fila no manifesto e diz que os paragrafos do testemunho, da falsidade e da v407 seguem como estao).", "# o passo 11 registra o estado da fila no manifesto e diz que os paragrafos do testemunho, da falsidade, do fechamento (v406) e do psion (v407) seguem como estao).")
f.sub('REGS="psion_canto_v407 cunhagens_v407 kh_n1_cobertura_v407"', 'REGS="tetelestai_terminal_v408 cunhagens_v408 kh_n1_cobertura_v408"')
f.sub("contrato R3_2: os 9 modulos novos tem declaracoes nomeadas, logo nao ha", "contrato R3_2: os modulos novos do bundle tem declaracoes nomeadas, logo nao ha")
f.sub('B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v407"', 'B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v408"')
ARQS.append(f)

for a in ARQS:
    assert "# [A ADAPTAR v408]" not in a.t and "[ADAPTADO v408, 03/11/2026" not in a.t, a.nome + ": sobrou marca da subida mecanica"
for a in ARQS:
    a.grava()
print("OK: %d arquivos adaptados (fork B, pequenos)" % len(ARQS))
