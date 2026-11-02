# -*- coding: utf-8 -*-
"""gerar_x_custodia_v405.py -- RASCUNHO do post longo da versao v405 no X (molde: Chatgpt\\TUNEL\\PARA_CHATGPT\\X_VITRINE\\CUSTODIA_v404.txt, escrito pela gerencia). LE o Nos (selo e core) e escreve SO' pos_rito\\CUSTODIA_v405_RASCUNHO.txt; NAO escreve no tunel nem publica:
copiar para X_VITRINE\\CUSTODIA_v405.txt e publicar e' ato da gerencia/do Codex (ORDEM de vitrine). Todo numero e hash vem do selo e do core lidos agora (nada digitado); o texto passa na guarda P18 e na regra da ordem (nao traz o 4,44).
uso: python -I -B -X utf8 gerar_x_custodia_v405.py [--nos <pasta>]   (padrao: o Nos real; antes do rito o selo e' o da v404 e o script RECUSA: o post so' nasce da v405 selada)"""
import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
from guarda_p18_v405 import violacoes  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
if "--nos" in sys.argv:
    NOS = sys.argv[sys.argv.index("--nos") + 1]
rj = lambda p: json.load(open(p, encoding="utf-8"))
selo = rj(os.path.join(NOS, "um_absoluto_selo.json")); core = rj(os.path.join(NOS, "um_absoluto.json"))["core"]; ESP = rj(os.path.join(PK, "ESPERADOS_v405.json"))
if selo.get("um_version") != "v405" or str((selo.get("sha256") or {}).get("um.py", ""))[:16] != ESP["candidato_sha16"]:
    print("RECUSO: o selo do Nos nao e' o da v405 candidata (um_version %r): o post so' nasce da v405 selada" % selo.get("um_version")); sys.exit(2)
for k_ in ("ponte_da_massa_v405", "lei_do_diminuto_v405", "ponto_zero_do_psion_v405", "identidade_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405"):
    assert core[k_].get("all_verified") is True, "um registro da v405 nao selou: o post nao diz isto"
pv = core["ponte_da_massa_v405"]["values"]; dv = core["lei_do_diminuto_v405"]["values"]; zv = core["ponto_zero_do_psion_v405"]["values"]; gv = core["ga_reclassificacao_v405"]["values"]
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
br = lambda x, nd: ("%.*f" % (nd, x)).replace(".", ",")
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v405 do programa terminal, custodiada em {data}

O que entrou: oito pedras no kernel Lean, com os nomes do operador: Ponte da Massa, Massa = tensão pura, Identidade, Observador = terminal, Lei do diminuto, Tônica do Hamiltoniano, Disco de Euler e Ponto Zero do Psíon.

· A moldura: os campos das estruturas fecharam; as leituras do operador passaram do campo para a definição; a leitura física não virou teorema. Um Um posto, uma α medida e as leituras do operador; dadas essas entradas, a FORMA é teorema.

· A massa: m₂ = β · sen 45° · u, com β = α√e em runtime e u = 1 eV posto pelo operador: {br(pv['m_derivada_meV'], 4)} meV, o número da v404. O meio-tom {br(dv['meio_tom'], 6)} desfaz o √e; E₀ = u é identidade algébrica, que não fixa u: o no-go não cai, localiza-se no Um posto. Sob a leitura R = β · u², ½ħω dá a mesma forma, com ħω = {br(zv['hbar_omega_meV'], 4)} meV; a coincidência é a aritmética ½ · √2 = sen 45°.

· A identidade: a pedra prova um fato sobre projeções no estado traço; que isso seja a identidade é leitura do operador, tipada como modelo. O ensaio «A identidade» é dele e entra no artigo verbatim.

· O Grande Atrator: a classe do teste muda, ao lado; a forma fica condicional; a janela mantém o veto; não é evidência e não discrimina da RG. Só a definição do raio move a previsão em {br(gv['piso_de_definicao'] * 100.0, 1)}%.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v404_e_v405'][0]}; {ESP['n_bandeiras_novas']} bandeiras novas), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: validade no kernel não é creditação; o gate não se move (as 18 bandeiras, a letra do veredito da v404); β_TGL na natureza a 5σ segue em aberto. As pedras seladas da v404 não foram renomeadas. α é medida, não derivada; a unidade é posta, não derivada.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
v = violacoes(txt)
assert not v, ("a guarda P18 achou violacao no post", v[:2])
import guarda_frases_v405 as GF  # noqa: E402
vf = GF.violacoes(txt)
assert not vf, ("a guarda das frases achou violacao no post", vf[:2])
assert "4,44" not in txt and "z_disc" not in txt, "o post nao traz o 4,44 (a regra da ordem e' do quadro)"
out = os.path.join(HERE, "CUSTODIA_v405_RASCUNHO.txt")
open(out, "w", encoding="utf-8", newline="\n").write(txt)
print("rascunho do post:", out, len(txt.encode("utf-8")), "B (NAO publicado; copiar para X_VITRINE\\CUSTODIA_v405.txt e' ato da gerencia)")
