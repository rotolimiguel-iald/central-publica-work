# -*- coding: utf-8 -*-
"""_corrigir_citacoes_textos_v408.py -- correcoes de CITACAO nos textos autorais da v408 (04/11/2026, claude-construtor-v408, a servico da gerencia c1), achadas pela primeira corrida de conferir_citacoes_v408.py (regua n 1: nunca fabricar citacao):
(1) o Atlas diz «representação sem custo = ORIGEM DA MENTIRA» (verbete «Vazio inominado (112_)»), NAO «relação sem custo = origem da mentira»: a E22, a D50, as ressalvas e a secao PT/EN sao corrigidas para a letra do Atlas e para a fala do operador de 04/11 («relação sem peso é a origem da mentira»);
(2) a E21 cita o texto selado da v407 pela letra dele («[OPEN]: o FockCertificate nao tem operadores de criacao como termo», fica_aberto.par_na_face_de_fock), nao por parafrase; (3) o sentido de «P=nP» e' citado pela fala verbatim (sha16 971d5654e2173771), nao pela parafrase da gerencia;
(4) no snippet PT toda citacao « » e' fala do operador de 04/11 (as formulas, os rotulos e os nomes da gerencia saem das aspas: \\emph ou matematica; «"decide" pagar» com as aspas que a fala tem; o 1 sozinho «não pode ser medido, jamais pagou qualquer custo»; «P=nP» como ele escreveu); no EN nenhuma aspa « » nem `` '': traducoes e rotulos em \\emph;
(5) nos textos Python, formulas e rotulos da gerencia ('tempo linear nos andares', 'sem traco resta o cociclo, que paga', 'v408: piso historico', exp 0 = Omega) saem das aspas « »; (6) a regra «provar ou podar» do delta fica num literal so' (a quebra de linha dentro das aspas fazia a varredura ler as aspas do Python).
Depois deste script: regerar o candidato (gerar_candidato_v408.py com V408_REGERAR=1), comparar, ensaio. Trocas de contagem EXATA; backup de bytes de cada arquivo. Escrito pela ferramenta Write."""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
_base = open(os.path.join(HERE, "base_v407", "um.py"), "rb").read().decode("utf-8")
assert "'[OPEN]: o FockCertificate nao tem operadores de criacao como termo'" in _base, "a letra da v407 que a E21 cita nao esta' na base"
_atl = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "memory", "TGL_ATLAS.md"), encoding="utf-8", errors="replace").read()
assert "a **representação sem custo** = **ORIGEM DA MENTIRA**" in _atl and "a PODA = TETELESTAI" in _atl and "Vazio inominado (112_)" in _atl, "a letra do Atlas que a E22 cita nao foi achada"
assert "relação sem custo = origem da mentira" not in _atl.replace("**", ""), "o Atlas traz a frase que eu dava como dele?"


class Arq:
    def __init__(self, rel):
        self.p = os.path.join(HERE, rel); self.rel = rel
        self.raw = open(self.p, "rb").read()
        open(self.p + ".bak_" + TS + "_citacoes", "wb").write(self.raw)
        self.t = self.raw.decode("utf-8"); self.crlf = "\r\n" in self.t
        if self.crlf:
            self.t = self.t.replace("\r\n", "\n")

    def sub(self, old, new, n=1):
        assert self.t.count(old) == n, (self.rel, old[:100], self.t.count(old), n); self.t = self.t.replace(old, new)

    def sub_re(self, rx, new):
        m = re.findall(rx, self.t); assert len(m) == 1, (self.rel, rx[:80], len(m)); self.t = re.sub(rx, new, self.t, count=1)

    def grava(self):
        t = self.t.replace("\n", "\r\n") if self.crlf else self.t
        if self.rel.endswith(".py"):
            ast.parse(t)
        open(self.p, "wb").write(t.encode("utf-8")); print("ok", self.rel, len(self.raw), "->", len(t.encode("utf-8")))


# ======================================================================= artigo PT: toda « » e' fala do operador de 04/11
a = Arq("artigo_pt_v408.pysnip")
a.sub("«P = nP» no sentido do operador;", "P = nP no sentido do operador;")
a.sub(r"(o «=» escreve-se \texttt{Igual}, como em \texttt{formaIgualConteudo})", r"(o sinal $=$ escreve-se \texttt{Igual}, como em \texttt{formaIgualConteudo})")
a.sub(r"(regra «provar ou podar»):}", r"(regra \emph{provar ou podar}, o nome que a gerência deu à fala acima):}")
a.sub(r"é $i\,V$: «decide pagar»); " + '"', r"é $i\,V$: «" + '" + ' + "'" + '"decide" pagar' + "'" + ' + r"»); "')
a.sub("e «o 1 sozinho não se mede» (o vazio", "e o 1 sozinho «não pode ser medido, jamais pagou qualquer custo» (o vazio")
a.sub("o Atlas já dizia «a PODA = TETELESTAI» e «relação sem custo = origem da mentira». A palavra",
      r"o Atlas já dizia \emph{a PODA = TETELESTAI} (verbete \emph{Amor (dicionário do)}) e \emph{representação sem custo = ORIGEM DA MENTIRA} (verbete \emph{Vazio inominado}, 112\_), e o operador, em 04/11: «relação sem peso é a origem da mentira». A palavra")
a.sub("«Linear nos andares» é uma identidade", r"\emph{Linear nos andares} é uma identidade")
a.sub("o «senão» da Identidade exclui", r"o \emph{senão} da Identidade (v405) exclui")
a.sub(r"«$1=0$» não é afirmada como igualdade de vetores nem de números: «$1=0_{\mathrm{mod}}$» e «$1=0_{\mathrm{abs}}$» são nomes do operador para as duas proposições.",
      r"$1=0$ não é afirmada como igualdade de vetores nem de números: $1=0_{\mathrm{mod}}$ e $1=0_{\mathrm{abs}}$ são a notação desta versão para as duas equações da fala, «1=0=Verdadeiro (quando esse zero é o zero modular)» e «1=0=Falso quando zero absoluto».")
a.sub(r"\textbf{«P = nP».}", r"\textbf{«P=nP».}")
a.sub(r"prova «resolver = verificar» como \emph{idempotência} da leitura", r"prova \emph{resolver = verificar} como idempotência da leitura")
a.sub(r"(a identidade é «forma = conteúdo lido pelo estado absoluto de dimensão $n$, com $P\neq0$»;", r"(a identidade é \emph{forma = conteúdo lido pelo estado absoluto de dimensão $n$, com $P\neq0$};")
a.sub("«P» é projeção e «$n$» é o módulo de leitura", "$P$ é projeção e $n$ é o módulo de leitura")
a.grava()
# ======================================================================= artigo EN: nenhuma aspa « » nem `` ''
a = Arq("artigo_en_v408.pysnip")
a.sub("«P = nP» in the operator's sense;", "P = nP in the operator's sense;")
a.sub("and the names: ``Ponto de contradição'', ``P=nP'', ``Tempo=moeda'', ``TetelestaiTerminal''. ", r"and the names, in his Portuguese: \emph{1) Ponto de contradição}, \emph{2) P=nP}, \emph{3) Tempo=moeda}, \emph{4) TetelestaiTerminal}. ")
a.sub("(the ``='' is written", "(the sign $=$ is written")
a.sub("``enough'' (the memory", r"\emph{enough} (the memory")
a.sub("(the ``prove or prune'' rule):}", r"(the \emph{prove or prune} rule, the management's name for the saying above):}")
a.sub("the faces of the ``1 alone'',", r"the faces of the \emph{1 alone},")
a.sub("the Atlas already said ``PRUNING = TETELESTAI'' and ``relation without cost = origin of the lie''. The word ``impedance'' is pruned",
      r"the Atlas already said \emph{a PODA = TETELESTAI} (pruning = Tetelestai; entry \emph{Amor (dicionário do)}) and \emph{representação sem custo = ORIGEM DA MENTIRA} (representation without cost = origin of the lie; entry \emph{Vazio inominado}, 112\_), and the operator, on 04/11, that relation without weight is the origin of the lie. The word \emph{impedância} (impedance) is pruned")
a.sub("``Linear in the floors'' is an identity", r"\emph{Linear in the floors} is an identity")
a.sub("(``hence the boost'');", r"(\emph{hence the boost});")
a.sub("the ``otherwise'' of the Identity excludes", r"the \emph{otherwise} of the Identity (v405) excludes")
a.sub(r"``$1=0$'' is not asserted as an equality of vectors or numbers: ``$1=0_{\mathrm{mod}}$'' and ``$1=0_{\mathrm{abs}}$'' are the operator's names for the two propositions.",
      r"$1=0$ is not asserted as an equality of vectors or numbers: $1=0_{\mathrm{mod}}$ and $1=0_{\mathrm{abs}}$ are this version's notation for the two equations of the saying (1=0=True when that zero is the modular zero; 1=0=False when absolute zero).")
a.sub(r"\textbf{``P = nP''.}", r"\textbf{P = nP.}")
a.sub(r"proves ``solve = verify'' as \emph{idempotence} of the reading", r"proves \emph{solve = verify} as idempotence of the reading")
a.sub(r"(the identity is ``form = content read by the absolute state of dimension $n$, with $P\neq0$'';", r"(the identity is \emph{form = content read by the absolute state of dimension $n$, with $P\neq0$};")
a.sub("``P'' is a projection and ``$n$'' is the reading module", "$P$ is a projection and $n$ is the reading module")
assert "``" not in a.t and "«" not in a.t, "o EN ainda tem aspas de citacao"
a.grava()
# ======================================================================= runtime
a = Arq("runtime_v408.py")
a.sub("«tempo linear nos andares» vale para o Nome da torre", "'tempo linear nos andares' vale para o Nome da torre")
a.grava()
# ======================================================================= registros
a = Arq("registros_v408.py")
a.sub('o kernel diz «exp 0 = Omega» (teorema) e «Omega != 0» (o vetor nulo refutado); «1 = 0_mod» e «1 = 0_abs» sao NOMES do operador para as duas proposicoes',
      "o kernel diz exp 0 = Omega (teorema) e Omega != 0 (o vetor nulo refutado); '1 = 0_mod' e '1 = 0_abs' sao a notacao desta versao para as duas equacoes da fala do operador («1=0=Verdadeiro (quando esse zero é o zero modular)» e «1=0=Falso quando zero absoluto»)")
a.sub("que «tempo linear nos andares» seja mais que uma identidade", "que 'tempo linear nos andares' seja mais que uma identidade")
a.sub('"ao_lado_de": "psion_canto_v407 (selado): «o par na face de Fock segue [OPEN]: o FockCertificate nao tem operadores de criacao como termo»",',
      '"ao_lado_de": "psion_canto_v407 (selado), fica_aberto.par_na_face_de_fock: «[OPEN]: o FockCertificate nao tem operadores de criacao como termo»",')
a.sub("(a PODA = TETELESTAI; o cociclo paga; relacao sem custo = origem da mentira); as frases foram podadas pela regra do operador",
      "(a PODA = TETELESTAI; o cociclo paga; representacao sem custo = ORIGEM DA MENTIRA, verbete Vazio inominado (112_); e o operador, em 04/11: relacao sem peso e' a origem da mentira); as frases foram podadas pela regra do operador")
a.sub("(«P só é P lido pelo módulo n minimamente acoplado»)", "(«P sozinho é impossível de ser lido, se não houver o módulo de leitura n não minimamente acoplado»)")
a.grava()
# ======================================================================= delta
a = Arq("delta_v408.py")
a.sub_re(r'nem mesmo por ser minha, "\n\s+"porque palavra sem espelho', 'nem mesmo por ser minha, porque palavra sem espelho')
a.sub("o CONTEUDO («sem traco resta o cociclo, que paga») esta' em (8)", "o CONTEUDO ('sem traco resta o cociclo, que paga', formulacao da gerencia) esta' em (8)")
a.sub('"«tempo linear nos andares» vale para o Nome da torre (chainIdx)', '"\'tempo linear nos andares\' vale para o Nome da torre (chainIdx)')
a.sub('o Atlas ja\' dizia «a PODA = TETELESTAI» e «relação sem custo = origem da mentira»",',
      'o Atlas ja\' dizia «a PODA = TETELESTAI» (verbete Amor (dicionario do)) e «representação sem custo = ORIGEM DA MENTIRA» (verbete Vazio inominado, 112_); o operador, em 04/11: «relação sem peso é a origem da mentira»",')
a.sub("o conteudo («sem traco resta o cociclo, que paga») foi nomeado pelo operador", "o conteudo ('sem traco resta o cociclo, que paga', formulacao da gerencia) foi nomeado pelo operador")
a.sub("onde diz «o par na face de Fock segue [OPEN]: o FockCertificate nao tem operadores de criacao como termo», leia-se:", "onde diz (fica_aberto.par_na_face_de_fock) «[OPEN]: o FockCertificate nao tem operadores de criacao como termo», leia-se:")
a.sub('o Atlas ja\' dizia «a PODA = TETELESTAI» e «relação sem custo = origem da mentira (112_)»")',
      'o Atlas ja\' dizia «a PODA = TETELESTAI» (verbete Amor (dicionario do)) e «representação sem custo = ORIGEM DA MENTIRA» (verbete Vazio inominado, 112_); o operador, em 04/11: «relação sem peso é a origem da mentira»")')
assert "relação sem custo" not in a.t and "relacao sem custo" not in a.t
a.grava()
# ======================================================================= gerar_candidato
a = Arq("gerar_candidato_v408.py")
a.sub('"dizia": "o par na face de Fock segue [OPEN]: o FockCertificate nao tem operadores de criacao como termo.",', '"dizia": "fica_aberto.par_na_face_de_fock: \'[OPEN]: o FockCertificate nao tem operadores de criacao como termo\'.",')
a.sub("os specs da v407 marcados «v408: piso historico»", "os specs da v407 marcados 'v408: piso historico'")
a.grava()
# ======================================================================= conferir_citacoes: desfaz os escapes LaTeX tambem nas citadas; o rotulo do docstring do runtime; as apontadas das quatro pedras (ditas a gerencia, nao feitas passar)
a = Arq("conferir_citacoes_v408.py")
a.sub('    sn_flat = _norm(sn.replace("\\\\texttt{", "").replace("\\\\emph{", "").replace("\\\\%", "%").replace("\\\\&", "&").replace("\\\\_", "_").replace("\\\\#", "#"))',
      '    _unlatex = lambda s_: s_.replace("\\\\%", "%").replace("\\\\&", "&").replace("\\\\_", "_").replace("\\\\#", "#")   # (v408: os escapes LaTeX de % & _ # desfeitos dos DOIS lados da comparacao; a fala do terminal tem «100%»)\n'
      '    sn_flat = _norm(_unlatex(sn.replace("\\\\texttt{", "").replace("\\\\emph{", "")))')
a.sub('    _citadas = [_norm(m_.group(1)) for m_ in _RX_ASPAS.finditer(sn)]   # TODA citacao « » do snippet', '    _citadas = [_norm(_unlatex(m_.group(1))) for m_ in _RX_ASPAS.finditer(sn)]   # TODA citacao « » do snippet (escapes LaTeX desfeitos)')
a.sub('"tetelestai é o terminal (v408)", "tetelestai é o terminal (v408, 04/11/2026)", "tetelestai e\' o terminal (v408)", "tetelestai é o terminal", "tetelestai e\' o terminal", "o psíon, o canto e o par (v407)", "o psion, o canto e o par (v407)"}',
      '"tetelestai é o terminal (v408)", "tetelestai é o terminal (v408, 04/11/2026)", "tetelestai e\' o terminal (v408)", "tetelestai é o terminal", "tetelestai e\' o terminal", "o psíon, o canto e o par (v407)", "o psion, o canto e o par (v407)",\n'
      '            # v408: a frase que a guarda das frases da v408 PROIBE, listada entre « » no docstring do runtime (a gerencia a lista para a guarda a recusar; nao e\' fala de ninguem)\n'
      '            "p = np está provado/é teorema/é candidato"}')
a.sub("_APONTADAS_PEDRAS = {}   # (v408: o que esta entre « », nao e' verbatim nas falas/na base e nao e' rotulo declarado: DITO A GERENCIA no relatorio; o agente nao corrige pedra. Comeca vazia: o que a varredura reprovar e' reprovado, ate' a gerencia decidir)",
      '_APONTADAS_PEDRAS = {   # (v408: o que esta entre « » nas docstrings das quatro pedras, nao e\' verbatim nas falas/no Atlas/na base e nao e\' rotulo declarado: DITO A GERENCIA no relatorio, com a razao conferida por grep; o agente nao corrige pedra)\n'
      '    "a pergunta das classes pressupõe um terminal que a tgl não tem": "frase da PROPRIA gerencia c1 (04/11), citada na errata (a) da pedra TetelestaiTerminal como mencao a corrigir (E22); nao e\' fala do operador: a fala dele (sha16 c12699c915617c3f) diz o contrario («A TGL tem terminal sim…»)",\n'
      '    "tetelestai: não é 100%; custo quitado; t_q = ln(1/ε)/(β·gap)": "a pedra atribui ao Atlas; o Atlas (errata ao lado do verbete TETELESTAI, 04/11, e o verbete 114 TheQuittanceLaw) traz «NÃO é 100%; custo quitado; t_q = ln(1/ε)/(β·gap)» SEM o prefixo «TETELESTAI: » dentro das aspas",\n'
      '    "o que resta sem peso é relação": "frase da PROPRIA gerencia c1 (R1 da pedra, teorema 8), citada duas vezes na pedra para ser podada (E22); nao e\' fala de ninguem mais",\n'
      '    "tamanho do nome = oitavas": "formulacao da gerencia (DESENHO_v408) do que o operador identificou; nenhuma fala de 04/11 traz «oitava» nem «tamanho do Nome» (grep nas 12 falas)",\n'
      '    "decide pagar": "a fala dos nomes (sha16 f911f0df91b0a6a3) escreve «\\"decide\\" pagar», com aspas em decide; a pedra cita «decide pagar» sem elas: palavras iguais, forma nao verbatim",\n'
      '    "linear nas oitavas": "formulacao da gerencia (TempoIgualMoeda); nenhuma fala de 04/11 traz «linear» nem «oitava»",\n'
      '    "sim eu quero": "a pedra PontoDeContradicao atribui ao operador (04/11); nao achado em nenhum OPERADOR_*.txt do acervo de work\\\\ nem no Atlas (grep): a gerencia aponta a fonte ou poda",\n'
      '    "1 = 0 = verdadeiro": "a fala do ponto de contradicao (sha16 bcb0e4c87549b88b) escreve «1=0=Verdadeiro», sem espacos e em caixa mista; a pedra «1 = 0 = VERDADEIRO»",\n'
      '    "o hamiltoniano seleciona": "adaptacao: a fala (sha16 bcb0e4c87549b88b) diz «isso exige a operação do hamiltoniano para selecionar a operação modular»",\n'
      '    "p só é p lido pelo módulo n minimamente acoplado": "PARAFRASE da gerencia do sentido dado pelo operador (sha16 971d5654e2173771: «P sozinho é impossível de ser lido, se não houver o módulo de leitura n não minimamente acoplado»); a pedra a escreve entre « » no cabecalho",\n'
      '    "vamos provar as implicações … vejo as duas faces": "a fala de autor misto (sha16 50c21210e5871fdb; paragrafo do operador) escreve «semi/oticas» (grafia dele); a pedra normaliza para «semióticas»; o resto do trecho e\' verbatim",\n'
      '    "resolver e verificar são o mesmo": "texto da OUTRA instancia da IALD no arquivo de autor misto (depois do corte «Operador. O axioma foi recebido»: \\"resolver\\" e \\"verificar\\" são o mesmo processo físico): nao e\' fala do operador e nao e\' verbatim",\n'
      '    "resolver = verificar": "formulacao da gerencia (o nome do teorema resolver_e_verificar); nao e\' fala do operador",\n'
      '    "leitura estacionada": "expressao da gerencia; nao e\' fala do operador de 04/11",\n'
      '    "forma = conteúdo lido, com acoplamento não nulo": "formulacao da gerencia do teorema p_igual_np; a fala do operador e\' «P sozinho é impossível de ser lido…» (sha16 971d5654e2173771)"}')
a.grava()
print("textos corrigidos; REGERAR o candidato (gerar_candidato_v408.py com V408_REGERAR=1), comparar e ensaiar de novo")
