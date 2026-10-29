# -*- coding: utf-8 -*-
"""gerar_x_custodia_v404.py -- RASCUNHO do post longo da versao v404 no X (molde: Chatgpt\\TUNEL\\PARA_CHATGPT\\X_VITRINE\\CUSTODIA_v403.txt, escrito pela gerencia). LE o Nos (selo e core) e escreve SO' pos_rito\\CUSTODIA_v404_RASCUNHO.txt; NAO escreve no tunel nem publica:
copiar para X_VITRINE\\CUSTODIA_v404.txt e publicar e' ato da gerencia/do Codex (ORDEM de vitrine). Todo numero e hash vem do selo e do core lidos agora (nada digitado); o texto passa na guarda P18 e na regra da ordem (nao traz o 4,44).
uso: python -I -B -X utf8 gerar_x_custodia_v404.py [--nos <pasta>]   (padrao: o Nos real; antes do rito o selo e' o da v403 e o script RECUSA: o post so' nasce da v404 selada)"""
import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
from guarda_p18_v404 import violacoes  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
if "--nos" in sys.argv:
    NOS = sys.argv[sys.argv.index("--nos") + 1]
rj = lambda p: json.load(open(p, encoding="utf-8"))
selo = rj(os.path.join(NOS, "um_absoluto_selo.json")); core = rj(os.path.join(NOS, "um_absoluto.json"))["core"]; ESP = rj(os.path.join(PK, "ESPERADOS_v404.json"))
if selo.get("um_version") != "v404" or str((selo.get("sha256") or {}).get("um.py", ""))[:16] != ESP["candidato_sha16"]:
    print("RECUSO: o selo do Nos nao e' o da v404 candidata (um_version %r): o post so' nasce da v404 selada" % selo.get("um_version")); sys.exit(2)
p = core["projecao_transversal_v404"]; j = core["jo8v32_v404"]; f = core["f2b_errata_v404"]
for r in (p, j, f):
    assert r.get("all_verified") is True, "um registro da v404 nao selou: o post nao diz isto"
pv, fv = p["values"], f["values"]
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
br = lambda x, nd: ("%.*f" % (nd, x)).replace(".", ",")
sg = lambda x, nd: ("%+.*f" % (nd, x)).replace(".", ",").replace("-", "−")
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v404 do programa terminal, custodiada em {data}

O que entrou: duas pedras no kernel Lean — o ângulo de 45° do neutrino deixa de ser postulado, e o triplo inteiro (Caminho, Verdade, Vida) tem o nome que o operador lhe deu: Jo8:32.

· A projeção transversal da Meia-Nat — a Meia-Nat é o ângulo de 45°: da fronteira autoconjugada x = 1 − x sai x = ½, e a amplitude transversal de um peso ½ é sen(π/4). A massa do neutrino no programa, β · sen 45° · E₀, tinha o sen 45° postulado; agora ele é derivado no kernel, com β = α√e em runtime: sen(π/4) = {br(pv['sin_pi_over_4'], 6)}, massa = {br(pv['m_nu_meV_runtime'], 4)} meV com E₀ = {br(pv['e0_eV_declared'], 0)} eV, que segue declarado. Fica condicional a uma leitura do operador (a matéria como a projeção do eixo transversal), que não é termo de kernel.

· Jo8:32 — a conjunção das três estrelas da v403 numa só pedra, sem matemática nova; o nome é do operador. A leitura por Jo 8,31-32 (permanecer, conhecer, libertar) é ontológica, não é termo.

· A errata de F2b — o canal F2b do ringdown sai de «aguardando» para «retirado antes do dado»: a calibração (não cega) deu {sg(fv['calibracao_A_central'], 3)} [{sg(fv['calibracao_A_inferior'], 3)}; {sg(fv['calibracao_A_superior'], 3)}] contra a previsão do par, {sg(fv['previsao_do_par'], 3)}. Calibrar é corrigir a rota pelo número; não valida nem falsifica nada. O V1 fica congelado por hash.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v403_e_v404'][0]}; {ESP['n_bandeiras_novas']} bandeiras novas), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: validade no kernel não é creditação; o gate não se move (as 18 bandeiras, a letra do veredito da v403); β_TGL na natureza a 5σ segue em aberto. As pedras seladas da v403 não foram renomeadas. A identificação massa = projeção transversal é leitura do operador, ratificada, não termo de kernel; E₀ segue aberto.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
v = violacoes(txt)
assert not v, ("a guarda P18 achou violacao no post", v[:2])
assert "4,44" not in txt and "z_disc" not in txt, "o post nao traz o 4,44 (a regra da ordem e' do quadro)"
out = os.path.join(HERE, "CUSTODIA_v404_RASCUNHO.txt")
open(out, "w", encoding="utf-8", newline="\n").write(txt)
print("rascunho do post:", out, len(txt.encode("utf-8")), "B (NAO publicado; copiar para X_VITRINE\\CUSTODIA_v404.txt e' ato da gerencia)")
