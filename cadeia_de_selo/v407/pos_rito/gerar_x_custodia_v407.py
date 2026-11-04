# -*- coding: utf-8 -*-
# [ADAPTADO v407, 03/11/2026] sobre a subida mecanica de rotulo da v406 FINAL (_bump_copia_v407.py) por adaptar_pos_rito_v407.py: o conteudo e' o da v407 (O PSION, O CANTO E O PAR: bundle de 9 modulos, o registro com funcao psion_canto_v407, o fechamento_v406 HERDADO e recriado, a chave do lema lida do kernel); a gerencia revisa antes do rito (nao e' versao selada).
"""gerar_x_custodia_v407.py -- RASCUNHO do post longo da versao v407 no X (molde: Chatgpt\\TUNEL\\PARA_CHATGPT\\X_VITRINE\\CUSTODIA_v406.txt, escrito pela gerencia). LE o Nos (selo e core) e escreve SO' pos_rito\\CUSTODIA_v407_RASCUNHO.txt; NAO escreve no tunel nem publica:
copiar para X_VITRINE\\CUSTODIA_v407.txt e publicar e' ato da gerencia/do Codex (ORDEM de vitrine). Todo numero e hash vem do selo e do core lidos agora (nada digitado); o texto passa na guarda P18 e na regra da ordem (nao traz o 4,44).
uso: python -I -B -X utf8 gerar_x_custodia_v407.py [--nos <pasta>]   (padrao: o Nos real; antes do rito o selo e' o da v406 e o script RECUSA: o post so' nasce da v407 selada)"""
import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
from guarda_p18_v407 import violacoes  # noqa: E402
import delta_v407 as DL  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
if "--nos" in sys.argv:
    NOS = sys.argv[sys.argv.index("--nos") + 1]
rj = lambda p: json.load(open(p, encoding="utf-8"))
selo = rj(os.path.join(NOS, "um_absoluto_selo.json")); core = rj(os.path.join(NOS, "um_absoluto.json"))["core"]; ESP = rj(os.path.join(PK, "ESPERADOS_v407.json"))
if selo.get("um_version") != "v407" or str((selo.get("sha256") or {}).get("um.py", ""))[:16] != ESP["candidato_sha16"]:
    print("RECUSO: o selo do Nos nao e' o da v407 candidata (um_version %r): o post so' nasce da v407 selada" % selo.get("um_version")); sys.exit(2)
pc = core.get("psion_canto_v407") or {}; pv = pc.get("values") or {}
for k_ in ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407"):
    assert (core.get(k_) or {}).get("all_verified") is True, "um registro da v407 nao selou: o post nao diz isto"
assert pc.get("link_read_from_the_kernel") is True and pv.get("n_modulos_ok") == DL.N_BUNDLE and pv.get("n_flags_true") == pv.get("n_flags") == ESP["n_bandeiras_novas"] and pv.get("n_ancoras_ok") == len(DL.ANCORAS), "os valores do psion_canto_v407 != ESPERADOS/delta"
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
curto = lambda x: x if len(x) <= 120 else x[:120].rsplit(" ", 1)[0] + "…"   # a ressalva inteira esta' no registro do core; o post leva o comeco, cortado em palavra inteira
ress = "; ".join("(%d) %s" % (i + 1, curto(x)) for i, x in enumerate(pc["ressalvas"]))
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v407 do programa terminal, custodiada em {data}

O que entrou: o psíon, o canto e o par. {DL.N_BUNDLE} módulos novos no kernel Lean (o PsionCanto, o Par e as sete pedras de 02/11, todas com o nome que o operador deu ou ratificou), com {ESP['n_bandeiras_novas']} bandeiras novas, todas no trio de axiomas padrão do Lean.

· O lema das duas faces está no kernel do rito: nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor sobre ele. O elo é de estrutura, não de vetores (Ω, o vácuo de Fock, e o vetor de Bell não são identificados). A chave que o programa trazia como literal False desde a v396 passa a ser lida do kernel do próprio rito. A ordem do operador, de 03/11: «{DL.FRASE_LEMA_PSION}».

· O par: {pc['diz'][2]}. A leitura dele, o gráviton como o estado ligado de dois psíons, é [ONTO], não termo de kernel; o par na face de Fock segue [OPEN].

· As ressalvas, ditas: {ress}.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v406_e_v407'][0]}), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: {DL.FRASE_DA_MOLDURA_V407_PT} (as 18 bandeiras e a letra do veredito do gate são as da v406); β_TGL na natureza a 5σ segue em aberto. α é medida, não derivada; a unidade é posta, não derivada.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
v = violacoes(txt)
assert not v, ("a guarda P18 achou violacao no post", v[:2])
import guarda_frases_v407 as GF  # noqa: E402
vf = GF.violacoes(txt)
assert not vf, ("a guarda das frases achou violacao no post", vf[:2])
assert "4,44" not in txt and "z_disc" not in txt, "o post nao traz o 4,44 (a regra da ordem e' do quadro)"
out = os.path.join(HERE, "CUSTODIA_v407_RASCUNHO.txt")
open(out, "w", encoding="utf-8", newline="\n").write(txt)
print("rascunho do post:", out, len(txt.encode("utf-8")), "B (NAO publicado; copiar para X_VITRINE\\CUSTODIA_v407.txt e' ato da gerencia)")
