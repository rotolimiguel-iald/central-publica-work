# -*- coding: utf-8 -*-
"""_adapt_pequenos_v408.py -- adapta a v408 (04/11/2026, claude-construtor-v408, a servico da gerencia c1) os arquivos PEQUENOS da cadeia que a subida mecanica de rotulo (v407->v408) deixou com a marca `# [A ADAPTAR v408]`:
guarda_p18_v408.py e acom_conferencias_v408.py (corpo identico ao molde: so' a marca sai e a nota diz por que), diff_e_pinos_v408.py, teste_conferidor_positivo_v408.py, refazer_candidato_v408.sh, regerar_v408.sh, fim_de_cadeia_v408.sh,
e COPIA carimbar_stdout_v407.py -> carimbar_stdout_v408.py (o carimbador do stdout do rito, que o rito_v408.sh chama e a subida nao copiou: so' o rotulo da versao sobe no texto).
Trocas de contagem EXATA (assert); backup de bytes de cada arquivo tocado; a marca so' sai do arquivo adaptado; numeros de tempo LIDOS de kernel/construir_marcas.txt. Escrito pela ferramenta Write (o heredoc do Bash colapsa barras)."""
import ast, datetime, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
N_BUNDLE = 4   # o DESENHO_v408 (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP); conferido abaixo contra kernel_modulos_novos_v408.json
import json
_nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v408.json"), encoding="utf-8"))["novos"]
assert len(_nov) == N_BUNDLE == 4 and [x.split("/")[-1][:-5] for x in _nov] == ["TetelestaiTerminal", "TempoIgualMoeda", "PontoDeContradicao", "PIgualNP"], _nov
_mk = open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read()
_mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", _mk, re.M)}
BUILD_S = _mm["epoch_build_fim"] - _mm["epoch_inicio"]; AUDIT_S = _mm["epoch_audit_fim"] - _mm["epoch_build_fim"]
assert BUILD_S > 0 and AUDIT_S > 0, (BUILD_S, AUDIT_S)
MARCA_RX = re.compile(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n")


class Arq:
    def __init__(self, rel):
        self.p = os.path.join(HERE, rel); self.rel = rel
        self.raw = open(self.p, "rb").read()
        open(self.p + ".bak_" + TS + "_adapt", "wb").write(self.raw)
        self.t = self.raw.decode("utf-8"); self.crlf = "\r\n" in self.t
        if self.crlf:
            self.t = self.t.replace("\r\n", "\n")

    def sub(self, old, new, n=1):
        assert self.t.count(old) == n, (self.rel, old[:100], self.t.count(old), n); self.t = self.t.replace(old, new)

    def tira_marca(self, nota=None):
        assert len(MARCA_RX.findall(self.t)) == 1, (self.rel, "marca")
        self.t = MARCA_RX.sub((nota + "\n") if nota else "", self.t, count=1)

    def grava(self):
        assert "[A ADAPTAR" not in self.t, self.rel
        t = self.t.replace("\n", "\r\n") if self.crlf else self.t
        if self.rel.endswith(".py"):
            ast.parse(t)
        open(self.p, "wb").write(t.encode("utf-8"))
        if self.rel.endswith(".sh"):
            r = subprocess.run(["sh", "-n", self.p], capture_output=True, text=True); assert r.returncode == 0, (self.rel, r.stderr[:300])
        print("ok", self.rel, len(self.raw), "->", len(t.encode("utf-8")))


# ---- guarda_p18_v408.py: o corpo e' a guarda P18 da v392, identico de versao a versao (so' o rotulo do arquivo sobe); conferido: o diff do bump e' so' a marca
a = Arq("guarda_p18_v408.py")
a.tira_marca("# copia da guarda P18 (v392) na cadeia v408 (04/11/2026, claude-construtor-v408): o corpo NAO muda de versao a versao (o diff do bump e' so' a marca); so' o rotulo do arquivo sobe. Importada por runtime/registros da v408 como nas versoes anteriores.")
a.grava()
# ---- acom_conferencias_v408.py: reexporta por caminho as conferencias da v407 (que reaproveitam as da v399): a secao do selo ACOM nao muda na v408; conferido: o diff do bump e' a marca + o rotulo
a = Arq("acom_conferencias_v408.py")
a.tira_marca("# adaptado a v408 (04/11/2026, claude-construtor-v408): a v408 NAO muda a secao do selo pela propria tecnologia; este modulo segue reexportando, por caminho, as conferencias da v407 (o diff do bump e' so' o rotulo e a marca).")
a.grava()
# ---- diff_e_pinos_v408.py
a = Arq("diff_e_pinos_v408.py")
a.tira_marca()
a.sub("(1) DIFF_KERNEL_v408.txt: arquivos novos (os 9 modulos do bundle, em TGLExt/: o numero e' o de CANDIDATO_v408.json)", "(1) DIFF_KERNEL_v408.txt: arquivos novos (os modulos do bundle da v408, em TGLExt/: 4 pelo DESENHO; o numero e' o de CANDIDATO_v408.json)")
a.sub("Molde: diff_e_pinos_v407.py (adaptado em 03/11/2026 ao bundle de 9 modulos).", "Molde: diff_e_pinos_v407.py (adaptado em 04/11/2026 ao bundle de 4 modulos: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; os 9 da v407 e os 301 da v406 ficam no kernel como registro).")
a.sub('("o diff do kernel nao e\' so\' os modulos do bundle (9, em TGLExt/) + a raiz (o Audit nao muda na v408)", len(novos), removidos, mudados)',
      '("o diff do kernel nao e\' so\' os modulos do bundle (%d, em TGLExt/) + a raiz (o Audit nao muda na v408)" % DL.N_BUNDLE, len(novos), removidos, mudados)')
a.grava()
# ---- teste_conferidor_positivo_v408.py
a = Arq("teste_conferidor_positivo_v408.py")
a.tira_marca()
a.sub("o round trip do um.py e, na v408, o registro psion_canto_v407, o fechamento_v406 herdado,\na chave linked_to_the_corner_by_a_lemma lida do kernel, as 76 ancoras e os 9 modulos do bundle) concordam",
      "o round trip do um.py e, na v408, o registro tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados,\nas 41 ancoras e os 4 modulos do bundle; nenhuma chave antiga muda) concordam")
a.sub("Molde: teste_conferidor_positivo_v407.py (cadeia v407), adaptado em 03/11/2026 a v408.", "Molde: teste_conferidor_positivo_v407.py (cadeia v407), adaptado em 04/11/2026 a v408 (claude-construtor-v408).")
a.grava()
# ---- refazer_candidato_v408.sh
a = Arq("refazer_candidato_v408.sh")
a.tira_marca()
a.sub("preparar_bundle_v408_03nov.py", "preparar_bundle_v408_04nov.py")
a.sub("# [v408, adaptado em 03/11/2026] o candidato e' o do BUNDLE PEQUENO de 9 modulos em TGLExt/ (registro psion_canto_v407; nao o bundle de 301 modulos do fecho da v407, que a v408 herda).",
      "# [v408, adaptado em 04/11/2026, claude-construtor-v408] o candidato e' o do BUNDLE PEQUENO de 4 modulos em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP; registro com funcao tetelestai_terminal_v408 + specs cunhagens_v408/kh_n1_cobertura_v408); os 9 modulos do psion (v407) e os 301 do fecho (v406) ficam no kernel como registro; nenhuma chave antiga muda.")
a.grava()
# ---- regerar_v408.sh
a = Arq("regerar_v408.sh")
a.tira_marca()
a.sub("# regerar_v408.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO de 9 modulos (adaptado em 03/11/2026 da v407: la' eram os 301 modulos do fecho em TGLExt/F1Fecho394; aqui o kernel novo sao 9 modulos em TGLExt/: PsionCanto e Par, da gerencia c1, e as sete pedras de 02/11, todas de nome ratificado, normalizados por preparar_bundle_v408_03nov.py):",
      "# regerar_v408.sh -- refaz, NA ORDEM, tudo o que depende do BUNDLE PEQUENO de 4 modulos (adaptado em 04/11/2026 da v407: la' eram os 9 modulos do psion e do canto; aqui o kernel novo sao 4 modulos em TGLExt/: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao e PIgualNP, com os nomes dados pelo operador em 04/11, normalizados por preparar_bundle_v408_04nov.py):")
a.sub("e recebe o bundle UMA VEZ por `preparar_bundle_v408_03nov.py` (ele ABORTA se o sandbox ja' tem o modulo e difere);", "e recebe o bundle UMA VEZ por `preparar_bundle_v408_04nov.py` (ele ABORTA se o sandbox ja' tem o modulo e difere);")
a.sub("# O build leva ~6 min e o Audit ~4 min no sandbox (medido em 03/11/2026: kernel/construir_marcas.txt, 379 s e 245 s: incremental sobre a v407 compilada, so' os 9 modulos a frio).",
      "# O build leva ~%d min e o Audit ~%d min no sandbox (medido em 04/11/2026: kernel/construir_marcas.txt, %d s e %d s: incremental sobre a v407 compilada, so' os 4 modulos a frio)." % (round(BUILD_S / 60), round(AUDIT_S / 60), BUILD_S, AUDIT_S))
a.grava()
# ---- fim_de_cadeia_v408.sh
a = Arq("fim_de_cadeia_v408.sh")
a.tira_marca()
a.sub("# fim_de_cadeia_v408.sh -- (adaptado em 03/11/2026; nenhum nome do bundle entra aqui:", "# fim_de_cadeia_v408.sh -- (adaptado em 04/11/2026, claude-construtor-v408; nenhum nome do bundle entra aqui:")
a.grava()
# ---- carimbar_stdout_v408.py: copia do carimbador da v407 (o rito_v408.sh o chama; a subida nao o copiou), com o rotulo da versao subido no texto
src7 = os.path.join(os.path.dirname(HERE), "v407", "carimbar_stdout_v407.py"); dst8 = os.path.join(HERE, "carimbar_stdout_v408.py")
b7 = open(src7, "rb").read(); t7 = b7.decode("utf-8")
assert not os.path.exists(dst8), "carimbar_stdout_v408.py ja existe: nao sobrescrevo"
t8 = t7.replace("v407", "v408")
assert t8.count("v408") >= 4 and "v407" not in t8, "a copia do carimbador nao subiu o rotulo"
assert t8.count('"""carimbar_stdout_v408.py -- ') == 1
t8 = t8.replace('"""carimbar_stdout_v408.py -- ', '"""carimbar_stdout_v408.py -- [copia na cadeia v408, 04/11/2026, claude-construtor-v408: o corpo e\' o do carimbador da v407 (sha16 %s); so\' o rotulo da versao sobe no texto] ' % __import__("hashlib").sha256(b7).hexdigest()[:16], 1)
ast.parse(t8); open(dst8, "wb").write(t8.encode("utf-8")); print("ok carimbar_stdout_v408.py copiado de", src7, len(b7), "->", len(t8.encode("utf-8")))
print("tempos lidos de construir_marcas.txt: build", BUILD_S, "s; audit", AUDIT_S, "s")
