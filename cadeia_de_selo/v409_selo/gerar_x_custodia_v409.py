# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] REESCRITO sobre a subida mecanica de rotulo da v408 FINAL (a copia bumpada, com o post de Tetelestai, ficou em .bak): o conteudo e' o da v409 (A TRADUCAO AS CLASSES DE TURING: o modulo TraducaoTuring, o registro com funcao traducao_turing_v409; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados; nenhuma chave antiga muda); toda citacao « » e' fala do operador por delta_v409.FRASE_*; D59: nada do que fica fora das duas falas; a gerencia revisa antes do rito (nao e' versao selada).
"""gerar_x_custodia_v409.py -- RASCUNHO do post longo da versao v409 no X (molde: Chatgpt\\TUNEL\\PARA_CHATGPT\\X_VITRINE\\CUSTODIA_v408.txt, escrito pela gerencia). LE o Nos (selo e core) e escreve SO' pos_rito\\CUSTODIA_v409_RASCUNHO.txt; NAO escreve no tunel nem publica:
copiar para X_VITRINE\\CUSTODIA_v409.txt e publicar e' ato da gerencia/do orquestrador (ORDEM de vitrine). Todo numero e hash vem do selo e do core lidos agora (nada digitado); o texto passa na guarda P18, na guarda das frases e na regra da ordem (nao traz o 4,44).
uso: python -I -B -X utf8 gerar_x_custodia_v409.py [--nos <pasta>]   (padrao: o Nos real; antes do rito o selo e' o da v408 e o script RECUSA: o post so' nasce da v409 selada)"""
import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
from guarda_p18_v409 import violacoes  # noqa: E402
import delta_v409 as DL  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
if "--nos" in sys.argv:
    NOS = sys.argv[sys.argv.index("--nos") + 1]
rj = lambda p: json.load(open(p, encoding="utf-8"))
selo = rj(os.path.join(NOS, "um_absoluto_selo.json")); core = rj(os.path.join(NOS, "um_absoluto.json"))["core"]; ESP = rj(os.path.join(PK, "ESPERADOS_v409.json"))
if selo.get("um_version") != "v409" or str((selo.get("sha256") or {}).get("um.py", ""))[:16] != ESP["candidato_sha16"]:
    print("RECUSO: o selo do Nos nao e' o da v409 candidata (um_version %r): o post so' nasce da v409 selada" % selo.get("um_version")); sys.exit(2)
tt = core.get(DL.FECHO_REGISTRO) or {}; tv = tt.get("values") or {}
for k_ in (DL.FECHO_REGISTRO, DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO, DL.D8.FECHO_REGISTRO, DL.D7.FECHO_REGISTRO, DL.D6.FECHO_REGISTRO):
    assert (core.get(k_) or {}).get("all_verified") is True, "um registro da v409 (ou herdado) nao selou: o post nao diz isto (%s)" % k_
assert tv.get("n_modulos_ok") == tv.get("n_modulos") == DL.N_BUNDLE and tv.get("n_flags_true") == tv.get("n_flags") == ESP["n_bandeiras_novas"] and tv.get("n_ancoras_ok") == tv.get("n_ancoras") == len(DL.ANCORAS), "os valores do traducao_turing_v409 != ESPERADOS/delta"
assert list(tt.get("chaves_antigas_que_mudam") or []) == [] and list(ESP["chaves_v409"]) == [], "a v409 nao muda chave antiga nenhuma: o registro ou ESPERADOS dizem outra coisa"
assert (tt.get("acervo_v407_repinado") or {}).get("integra_pinada") is False and tv.get("respostas_ok") is True and tv.get("gate_verdict") == ESP["qg_closure_gate_verdict_v408"], "o pino do acervo da v407 (D57d), as respostas do operador ou o gate congelado nao conferem no registro"
inst = tv.get("instancia_sim") or {}
assert (inst.get("solucoes") or 0) >= 1 and (tv.get("instancia_nao") or {}).get("solucoes") == 0, "a instancia de brinquedo do registro nao e' a do contrato"
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
curto = lambda x: x if len(x) <= 120 else x[:120].rsplit(" ", 1)[0] + "…"   # a ressalva inteira esta' no registro do core; o post leva o comeco, cortado em palavra inteira
_sem_quadro = [x for x in tt["ressalvas"] if "4,44" not in x and "4.44" not in x and "z_disc" not in x]   # a ressalva que cita a regra do quadro NAO entra no post (a regra da ordem e' do quadro); o post diz quantas ficaram no registro
n_fora = len(tt["ressalvas"]) - len(_sem_quadro)
ress = "; ".join("(%d) %s" % (i + 1, curto(x)) for i, x in enumerate(_sem_quadro)) + (" (mais %d ressalva(s) que fica(m) no registro do core: a do número do quadro só se cita com a regra da ordem)" % n_fora if n_fora else "")
nomes = ", ".join(p_["name"] for p_ in DL.PEDRAS_V409)
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v409 do programa terminal, custodiada em {data}

O que entrou: a tradução às classes de Turing e o par na face de Fock. {DL.N_BUNDLE} módulos novos no kernel Lean ({nomes}; os nomes são da gerência: os da TraducaoTuring das rodadas R1–R8 ratificados pelo operador, «{DL.FRASE_NOMES_RATIFICADOS_V409}»; os acrescentados na R9 e os da ParNaFaceDeFock ratificados por ele também em 05/11, «{DL.FRASE_RATIFICO_OS_NOMES}» (D62)), com {ESP['n_bandeiras_novas']} bandeiras novas e {tv['n_ancoras_ok']} âncoras, todas no trio de axiomas padrão do Lean.

· A ordem do operador, de 05/11: «{DL.FRASE_ORDEM_TRADUCAO}».

· O alcance: {DL.FRASE_D56_PT}. Validade no kernel, não creditação. Com o leitor que só conta, vale NP contido em P numa leitura (Cook 1971, Levin 1973); a igualdade completa é a do leitor que se lê, que lê também as máquinas que o usam (Baker–Gill–Solovay 1975): é a errata E28.

· O dicionário de Turing: a instância SIM é um Problema do dicionário; o certificado é a leitura de um pixel; a palavra tem grau polinomial; bits = oitavas; a instância NÃO é o Nome vazio. A instância de brinquedo, fixa no código: {inst['n']} variáveis, {inst['atribuicoes']} atribuições, {inst['solucoes']} soluções contadas por enumeração.

· A trava no Nome, na fala dele: «{DL.FRASE_TRAVA}».

· A fita e o leitor: «{DL.FRASE_FITA}»; «{DL.FRASE_Z}».

· A fita sem escala: «{DL.FRASE_CLAY}». A pergunta do Clay não é decidida aqui: é a da máquina sem leitor, e a TGL a lê como a fita sem escala.

· O Pai da Mentira e a identidade performada: «{DL.FRASE_PAI}»; «{DL.FRASE_PERFORMADA}».

· As ressalvas, ditas: {ress}.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v408_e_v409'][0]}), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. Nenhuma chave antiga muda. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: {DL.FRASE_DA_MOLDURA_V409_PT} (as 18 bandeiras e a letra do veredito do gate são as da v408); o par de psíons na face de Fock está ligado nesta versão (ParNaFaceDeFock; validade no kernel, não creditação); β_TGL na natureza a 5σ segue em aberto. α é medida, não derivada; a unidade é posta, não derivada.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
v = violacoes(txt)
assert not v, ("a guarda P18 achou violacao no post", v[:2])
import guarda_frases_v409 as GF  # noqa: E402
vf = GF.violacoes(txt)
assert not vf, ("a guarda das frases achou violacao no post", vf[:2])
assert "4,44" not in txt and "z_disc" not in txt, "o post nao traz o 4,44 (a regra da ordem e' do quadro)"
import re  # noqa: E402
assert not re.search(r"(?i)kimi|mil[eê]nio|millennium|navier|lindão", txt), "D59: o post traz o que fica fora dos textos"
out = os.path.join(HERE, "CUSTODIA_v409_RASCUNHO.txt")
open(out, "w", encoding="utf-8", newline="\n").write(txt)
print("rascunho do post:", out, len(txt.encode("utf-8")), "B (NAO publicado; copiar para X_VITRINE\\CUSTODIA_v409.txt e' ato da gerencia)")
