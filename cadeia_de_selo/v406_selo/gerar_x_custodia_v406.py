# -*- coding: utf-8 -*-
"""gerar_x_custodia_v406.py -- RASCUNHO do post longo da versao v406 no X (molde: Chatgpt\\TUNEL\\PARA_CHATGPT\\X_VITRINE\\CUSTODIA_v405.txt, escrito pela gerencia). LE o Nos (selo e core) e escreve SO' pos_rito\\CUSTODIA_v406_RASCUNHO.txt; NAO escreve no tunel nem publica:
copiar para X_VITRINE\\CUSTODIA_v406.txt e publicar e' ato da gerencia/do Codex (ORDEM de vitrine). Todo numero e hash vem do selo e do core lidos agora (nada digitado); o texto passa na guarda P18 e na regra da ordem (nao traz o 4,44).
uso: python -I -B -X utf8 gerar_x_custodia_v406.py [--nos <pasta>]   (padrao: o Nos real; antes do rito o selo e' o da v405 e o script RECUSA: o post so' nasce da v406 selada)"""
import datetime, json, os, sys
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
