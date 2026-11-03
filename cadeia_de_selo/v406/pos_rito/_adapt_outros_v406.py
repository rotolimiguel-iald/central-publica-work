# -*- coding: utf-8 -*-
"""_adapt_outros_v406.py -- as edicoes de b3_recibo_v406.py, gerar_derivacao_pos_rito_v406.py, gerar_x_custodia_v406.py e (fora de pos_rito) bateria_pre_selo\\conferir_recibo_pre_selo_v406.py (chamado por adaptar_pos_rito_v406.py)."""
import os

DERIV_DOC_B = """A ADAPTACAO (o que o pos-rito diz da v406: o fechamento, com os numeros lidos do rito) foi feita em 02/11/2026 por adaptar_pos_rito_v406.py (+ os _adapt_<arquivo>_v406.py) e textos_v406_novo.pysnip: textos_v406.py sai do montador (montar_textos_v406.py) sobre textos_v406.semente (copia de bytes da semente mecanica) e textos_v406_novo.pysnip; leitura_v406.py, fechar_v406.py, registrar_mapa_v406.py, superficies_v406.py, o harness e o cabecalho do chain foram adaptados e a marca TEXTO_A_REESCREVER_V406 nao sobrou em nenhum arquivo (o p00 confere).
"""

X_BODY = r'''import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
from guarda_p18_v406 import violacoes  # noqa: E402
import delta_v406 as DL  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
if "--nos" in sys.argv:
    NOS = sys.argv[sys.argv.index("--nos") + 1]
rj = lambda p: json.load(open(p, encoding="utf-8"))
selo = rj(os.path.join(NOS, "um_absoluto_selo.json")); core = rj(os.path.join(NOS, "um_absoluto.json"))["core"]; ESP = rj(os.path.join(PK, "ESPERADOS_v406.json"))
if selo.get("um_version") != "v406" or str((selo.get("sha256") or {}).get("um.py", ""))[:16] != ESP["candidato_sha16"]:
    print("RECUSO: o selo do Nos nao e' o da v406 candidata (um_version %r): o post so' nasce da v406 selada" % selo.get("um_version")); sys.exit(2)
fe = core.get("fechamento_v406") or {}; fv = fe.get("values") or {}
for k_ in ("fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406"):
    assert (core.get(k_) or {}).get("all_verified") is True, "um registro da v406 nao selou: o post nao diz isto"
assert fe.get("certificate_inhabited") is True and fv.get("n_modulos_ok") == DL.N_BUNDLE and fv.get("n_flags_true") == fv.get("n_flags") == ESP["n_bandeiras_novas"], "os valores do fechamento_v406 != ESPERADOS/delta"
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
ress = "; ".join("(%d) %s" % (i + 1, (x.split(":")[0] if ":" in x else x)) for i, x in enumerate(fe["ressalvas"]))
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v406 do programa terminal, custodiada em {data}

O que entrou: o fechamento. {DL.N_BUNDLE} módulos novos no kernel Lean (os 300 da bancada do ChatGPT, recompilados do fonte, e uma candidata da gerência, de nome provisório: os nomes das pedras são do operador), com {ESP['n_bandeiras_novas']} bandeiras novas, todas no trio de axiomas padrão do Lean.

· O certificado de Fock está habitado por construção no kernel do rito, e a passagem para o contínuo é termo para todo CanonicalNetInput. O operador ordenou: «{DL.FRASE_CONSTRUIR}»; a prioridade: «{DL.FRASE_PASSAGEM}». Virou validade no kernel; a creditação segue recusada.

· As quatro chaves de testemunha que o programa trazia como literal False passam a ser lidas do kernel do próprio rito. {fe['diz'][2]}.

· As ressalvas, ditas: {ress}.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v405_e_v406'][0]}), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: {DL.FRASE_DA_MOLDURA_V406_PT}; o gate não se move (as 18 bandeiras, a letra do veredito da v405); β_TGL na natureza a 5σ segue em aberto. α é medida, não derivada; a unidade é posta, não derivada.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
v = violacoes(txt)
assert not v, ("a guarda P18 achou violacao no post", v[:2])
import guarda_frases_v406 as GF  # noqa: E402
vf = GF.violacoes(txt)
assert not vf, ("a guarda das frases achou violacao no post", vf[:2])
assert "4,44" not in txt and "z_disc" not in txt, "o post nao traz o 4,44 (a regra da ordem e' do quadro)"
out = os.path.join(HERE, "CUSTODIA_v406_RASCUNHO.txt")
open(out, "w", encoding="utf-8", newline="\n").write(txt)
print("rascunho do post:", out, len(txt.encode("utf-8")), "B (NAO publicado; copiar para X_VITRINE\\CUSTODIA_v406.txt e' ato da gerencia)")
'''


def rodar(A):
    # ---- b3_recibo_v406.py: so' o cabecalho (o corpo e' a subida pura de rotulo e ja' esta' certo: B14 -> B15, v405 -> v406)
    nome = "b3_recibo_v406.py"
    txt, crlf, raw = A.le(nome)
    if not A.pula(nome, txt):
        t = A.tira_cabecalho(txt)
        A.grava(nome, t, crlf, raw)
    # ---- gerar_derivacao_pos_rito_v406.py
    nome = "gerar_derivacao_pos_rito_v406.py"
    txt, crlf, raw = A.le(nome)
    if not A.pula(nome, txt):
        t = A.tira_cabecalho(txt)
        t = A.entre(t, "A ADAPTACAO (o que o pos-rito diz da v406", "Este script apenas recalcula", DERIV_DOC_B)
        t = A.sub(t, "o recibo do B(n), passo SIMPLES B13 -> B14", "o recibo do B(n), passo SIMPLES B14 -> B15")
        t = A.sub(t, '"claude-prep-v406, 01/11: a leitura da rodada adaptada a v406"', '"gerencia c1, 02/11: a leitura da rodada adaptada ao fechamento (leitura_v406; o bundle, as oito ancoras, as quatro chaves; os treze registros da v405 recriados)"')
        t = A.sub(t, '"claude-prep-v406, 01/11: montado de textos_v406.semente + textos_v406_novo.pysnip (a massa derivada e a identidade definida)"', '"gerencia c1, 02/11: montado de textos_v406.semente + textos_v406_novo.pysnip (o fechamento; sem prosa nova de conteudo)"')
        t = A.sub(t, '"claude-prep-v406, 01/11: o harness do pos-rito adaptado a v406"', '"gerencia c1, 02/11: o harness do pos-rito adaptado ao fechamento"')
        t = A.sub(t, '"claude-prep-v406, 01/11: o registro da rota umpy.v406.selada_massa_derivada_e_identidade_01nov"', '"gerencia c1, 02/11: o registro da rota umpy.v406.selada_o_fechamento_02nov"')
        t = A.sub(t, '"claude-prep-v406, 01/11: o montador (semente + fragmento)"', '"gerencia c1, 02/11: o montador (semente + fragmento; DELETAR as funcoes das oito pedras da v405)"')
        t = A.sub(t, '"claude-prep-v406, 01/11: o fragmento escrito a mao para a v406"', '"gerencia c1, 02/11: o fragmento escrito para a v406 (sem prosa nova de conteudo)"')
        t = A.sub(t, '    ("textos_v406.semente", None,', '    ("adaptar_pos_rito_v406.py", None, "gerencia c1, 02/11: o adaptador do pos-rito (as edicoes exatas por arquivo, com asserts; os blocos novos moram nos _adapt_*_v406.py)"),\n    ("textos_v406.semente", None,')
        t = A.sub(t, "a adaptacao a mao foi feita pela gerencia c1 em 28/10/2026 (as marcas TEXTO_A_REESCREVER_V406 sairam depois de cada arquivo testado)", "a adaptacao foi feita pela gerencia c1 em 02/11/2026 por adaptar_pos_rito_v406.py (as marcas TEXTO_A_REESCREVER_V406 nao sobraram em nenhum arquivo)")
        A.grava(nome, t, crlf, raw)
    # ---- gerar_x_custodia_v406.py (o corpo e' reescrito: o post diz o fechamento, com os numeros lidos do selo e do core)
    nome = "gerar_x_custodia_v406.py"
    txt, crlf, raw = A.le(nome)
    if "fechamento_v406" not in txt:
        t = A.entre(txt, "import datetime, json, os, sys", "\x00FIM", X_BODY) if False else txt[:txt.index("import datetime, json, os, sys")] + X_BODY
        A.grava(nome, t, crlf, raw)
    else:
        print("  JA ADAPTADO:", nome)
    # ---- bateria_pre_selo\conferir_recibo_pre_selo_v406.py: o selo da versao ANTES da anterior e' o da v404 (a pasta v405\base_v404), nao a v403 (v405\base_v403 nao existe)
    bdir = os.path.join(os.path.dirname(A.HERE), "bateria_pre_selo")
    p = os.path.join(bdir, "conferir_recibo_pre_selo_v406.py")
    raw = open(p, "rb").read(); crlf = b"\r\n" in raw; t = raw.decode("utf-8").replace("\r\n", "\n")
    if "SELO_V403" in t:
        t = A.sub(t, 'SELO_V403 = os.path.join(V14, "base_v403", "um_absoluto_selo.json")', 'SELO_V404 = os.path.join(V14, "base_v404", "um_absoluto_selo.json")')
        t = A.sub(t, 'KM_V403 = os.path.join(V14, "base_v403", "tgl_kernel_proof_manifest.json")', 'KM_V404 = os.path.join(V14, "base_v404", "tgl_kernel_proof_manifest.json")')
        t = A.sub(t, "conferir(RP, RSHA, SELO_V403, KM_V403)", "conferir(RP, RSHA, SELO_V404, KM_V404)")
        t = A.sub(t, "selo_anterior_e_o_da_v403_nao_o_pinado", "selo_anterior_e_o_da_v404_nao_o_pinado")
        import ast
        ast.parse(t)
        open(p + ".bak_" + A.STAMP + "_adapt", "wb").write(raw)
        out = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
        tmp = p + ".tmp"; open(tmp, "wb").write(out); os.replace(tmp, p)
        print("  gravado bateria_pre_selo/conferir_recibo_pre_selo_v406.py: %d B -> %d B" % (len(raw), len(out)))
    else:
        print("  JA ADAPTADO: bateria_pre_selo/conferir_recibo_pre_selo_v406.py")
