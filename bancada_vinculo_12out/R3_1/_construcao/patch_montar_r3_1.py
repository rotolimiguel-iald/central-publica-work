# -*- coding: utf-8 -*-
"""patch_montar_r3_1.py (R3.1, 13/10/2026) -- aplica ao montar_sandbox.py da R3 (518cd2af4f67093b, copiado para R3_1) as fixtures do
contrato KERNEL_RECIBO_R3_1 (toolchain em lista, pedras com declaracoes, formal_files_antes, criterios so com o medido), o CRITERIOS
sintetico pinavel (contrato CRITERIOS_R3_1) e a AMOSTRA REAL do aviso de sorry do Lean 4.31 (lida, so leitura, de um log do
Nos/bancada_corpus; vai ao manifesto do sandbox com caminho, sha256 do arquivo, numero da linha e os bytes da linha em hex).
Substituicoes exatas e unicas; grava por temporario -> confere -> os.replace."""
import sys
sys.dont_write_bytecode = True
import hashlib, os
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
ALVO = AQUI / "montar_sandbox.py"
txt = ALVO.read_bytes().decode("utf-8")
assert hashlib.sha256(txt.encode("utf-8")).hexdigest().startswith("518cd2af4f67093b"), "a copia nao e a R3 pinada"
TROCAS = []


def troca(velho, novo):
    TROCAS.append((velho, novo))


troca('''"""montar_sandbox.py (R3, 13/10/2026) -- monta o sandbox''', '''"""montar_sandbox.py (R3.1, 13/10/2026) -- R3.1: o recibo do kernel sintetico no contrato KERNEL_RECIBO_R3_1 (toolchain em lista,
pedras com declaracoes, formal_files_antes, criterios so com o medido); fx/CRITERIOS_v392_SINTETICO.json (contrato CRITERIOS_R3_1,
os ESPERADOS pinaveis por --criterios-sha256); a AMOSTRA REAL do aviso de sorry do Lean 4.31 (crases), lida de um log do
Nos/bancada_corpus (so leitura) e guardada em hex no SANDBOX_MANIFEST_R3_1.json. O resto como na R3:
monta o sandbox''')
troca('KERNEL_CONTRATO = "KERNEL_RECIBO_R3"\n', '''KERNEL_CONTRATO = "KERNEL_RECIBO_R3_1"
CRITERIOS_CONTRATO = "CRITERIOS_R3_1"
# A1 (R3.1): a amostra REAL do aviso de sorry do Lean 4.31 -- um log do Nos/bancada_corpus (so leitura), a primeira linha com o aviso
AMOSTRA_SORRY = NOS / "bancada_corpus" / "ChainSiteOperators.20260905_150729.falha_lean.log"
''')
troca('''rec = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3 (13/10/2026)",''',
      '''rec = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.1 (13/10/2026)",''')
troca('''            toolchain=dict(lean_version=kman["lean_version"][0], lake_version=kman["lake_version"][0]),''',
      '''            toolchain=dict(lean_version=list(kman["lean_version"]), lake_version=list(kman["lake_version"])),   # N1m: lista, como no manifesto''')
troca('''            pedras=[dict(path="TGLExt/PedraSinteticaA.lean", sha256=ks_sha["TGLExt/PedraSinteticaA.lean"]),
                    dict(path="TGLExt/PedraSinteticaB.lean", sha256=ks_sha["TGLExt/PedraSinteticaB.lean"])],''',
      '''            pedras=[dict(path="TGLExt/PedraSinteticaA.lean", sha256=ks_sha["TGLExt/PedraSinteticaA.lean"], declaracoes=["TGLExt.PedraSinteticaA.um"]),
                    dict(path="TGLExt/PedraSinteticaB.lean", sha256=ks_sha["TGLExt/PedraSinteticaB.lean"], declaracoes=["TGLExt.PedraSinteticaB.dois"])],''')
troca('''            criterios=dict(j1_declaracoes=dict(esperado=2, medido=2), j1_teoremas=dict(esperado=2, medido=2), j1_fora_do_trio=dict(esperado=0, medido=0),
                           audit_entradas_antigas_identicas=dict(esperado=0, medido=0), tokens_proibidos=dict(esperado=0, medido=0),
                           r1_ausente=dict(esperado=True, medido=True), declaracoes_novas_no_trio=dict(esperado=True, medido=True)),''',
      '''            criterios=dict(j1_declaracoes=dict(medido=2), j1_teoremas=dict(medido=2), j1_fora_do_trio=dict(medido=0),
                           audit_entradas_antigas_identicas=dict(medido=0), tokens_proibidos=dict(medido=0),
                           r1_ausente=dict(medido=True), declaracoes_novas_no_trio=dict(medido=True)),   # A3: so o MEDIDO; o esperado vem do CRITERIOS pinado
            formal_files_antes=dict(ff_v391),   # N1l: o mapa do kernel ANTES (a impressao dele == nos_kernel_impressao.antes)''')
troca('''            nota="FIXTURE SINTETICA do recibo do build do kernel (etapa 2 da cadeia), contrato KERNEL_RECIBO_R3: nenhum kernel construido aqui; "
                 "os criterios J1/8523 do plano v392 viram 2/2/0/0 nesta arvore de duas pedras")''',
      '''            nota="FIXTURE SINTETICA do recibo do build do kernel (etapa 2 da cadeia), contrato KERNEL_RECIBO_R3_1: nenhum kernel construido aqui; "
                 "os criterios J1/8523 do plano v392 viram 2/2/0/0 nesta arvore de duas pedras (medidos aqui; os esperados no CRITERIOS sintetico)")''')
troca('''rec["fx"]["kernel_v391"] = dict(''', '''# A3 (R3.1): o CRITERIOS sintetico (os ESPERADOS), pinavel pela flag --criterios-sha256; o modelo da gerencia e R3_1/CRITERIOS_V392.json
crit = dict(contrato=CRITERIOS_CONTRATO, versao=VERSAO_SINTETICA, preenchido=True, x19="nao",
            esperados=dict(j1_declaracoes=2, j1_teoremas=2, j1_fora_do_trio=0, audit_entradas_antigas_identicas=0, tokens_proibidos=0,
                           r1_ausente=True, declaracoes_novas_no_trio=True),
            SINTETICO_SANDBOX="NAO SAO OS CRITERIOS DA v392: fixture do ensaio (R3.1, 13/10/2026) para a arvore sintetica de duas pedras; x19='nao' so preenche o campo")
rec["fx"]["CRITERIOS_v392_SINTETICO.json"] = gravar_novo(RAIZ / "fx" / "CRITERIOS_v392_SINTETICO.json", json.dumps(crit, ensure_ascii=False, indent=1).encode("utf-8"))
# A1 (R3.1): a amostra REAL do aviso de sorry (so leitura do Nos/bancada_corpus)
_am = AMOSTRA_SORRY.read_bytes()
_linhas = _am.split(b"\\n")
_n = next(i for i, l in enumerate(_linhas, 1) if b"declaration uses" in l)
rec["fx"]["amostra_sorry_lean431"] = dict(path=str(AMOSTRA_SORRY), sha256=sha(_am), bytes=len(_am), linha_n=_n, linha_hex=_linhas[_n - 1].hex(),
                                          n_avisos_crase_no_arquivo=_am.count(b"declaration uses `sorry`"), n_avisos_aspas_no_arquivo=_am.count(b"declaration uses 'sorry'"),
                                          nota="a linha verbatim (com o CR do CRLF) que os controles A1 acrescentam ao log sintetico")
rec["fx"]["kernel_v391"] = dict(''')
troca('''p = RAIZ / "SANDBOX_MANIFEST_R3.json"''', '''p = RAIZ / "SANDBOX_MANIFEST_R3_1.json"''')

for velho, novo in TROCAS:
    n = txt.count(velho)
    assert n == 1, "troca nao unica (%d): %r" % (n, velho[:120])
    txt = txt.replace(velho, novo, 1)
dados = txt.encode("utf-8")
compile(dados, str(ALVO), "exec")
tmp = ALVO.with_name(ALVO.name + ".tmp_patch")
with open(tmp, "xb") as f:
    f.write(dados)
assert tmp.read_bytes() == dados
os.replace(tmp, ALVO)
assert ALVO.read_bytes() == dados
print("ok", len(TROCAS), "trocas;", hashlib.sha256(dados).hexdigest()[:16], len(dados), "bytes")
