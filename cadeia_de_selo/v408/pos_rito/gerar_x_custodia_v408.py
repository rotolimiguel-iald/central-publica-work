# -*- coding: utf-8 -*-
# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B)] REESCRITO sobre a subida mecanica de rotulo da v407 FINAL (_bump_copia_v408.py deixara o post do psion): o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: o bundle de quatro modulos, o registro com funcao tetelestai_terminal_v408; o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados; nenhuma chave antiga muda); toda citacao « » e' fala do operador por delta_v408.FRASE_*; a gerencia revisa antes do rito (nao e' versao selada).
"""gerar_x_custodia_v408.py -- RASCUNHO do post longo da versao v408 no X (molde: Chatgpt\\TUNEL\\PARA_CHATGPT\\X_VITRINE\\CUSTODIA_v407.txt, escrito pela gerencia). LE o Nos (selo e core) e escreve SO' pos_rito\\CUSTODIA_v408_RASCUNHO.txt; NAO escreve no tunel nem publica:
copiar para X_VITRINE\\CUSTODIA_v408.txt e publicar e' ato da gerencia/do orquestrador (ORDEM de vitrine). Todo numero e hash vem do selo e do core lidos agora (nada digitado); o texto passa na guarda P18, na guarda das frases e na regra da ordem (nao traz o 4,44).
uso: python -I -B -X utf8 gerar_x_custodia_v408.py [--nos <pasta>]   (padrao: o Nos real; antes do rito o selo e' o da v407 e o script RECUSA: o post so' nasce da v408 selada)"""
import datetime, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
from guarda_p18_v408 import violacoes  # noqa: E402
import delta_v408 as DL  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
if "--nos" in sys.argv:
    NOS = sys.argv[sys.argv.index("--nos") + 1]
rj = lambda p: json.load(open(p, encoding="utf-8"))
selo = rj(os.path.join(NOS, "um_absoluto_selo.json")); core = rj(os.path.join(NOS, "um_absoluto.json"))["core"]; ESP = rj(os.path.join(PK, "ESPERADOS_v408.json"))
if selo.get("um_version") != "v408" or str((selo.get("sha256") or {}).get("um.py", ""))[:16] != ESP["candidato_sha16"]:
    print("RECUSO: o selo do Nos nao e' o da v408 candidata (um_version %r): o post so' nasce da v408 selada" % selo.get("um_version")); sys.exit(2)
tt = core.get(DL.FECHO_REGISTRO) or {}; tv = tt.get("values") or {}
for k_ in (DL.FECHO_REGISTRO, DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO, DL.D7.FECHO_REGISTRO, DL.D6.FECHO_REGISTRO):
    assert (core.get(k_) or {}).get("all_verified") is True, "um registro da v408 (ou herdado) nao selou: o post nao diz isto (%s)" % k_
assert tv.get("n_modulos_ok") == tv.get("n_modulos") == DL.N_BUNDLE and tv.get("n_flags_true") == tv.get("n_flags") == ESP["n_bandeiras_novas"] and tv.get("n_ancoras_ok") == tv.get("n_ancoras") == len(DL.ANCORAS), "os valores do tetelestai_terminal_v408 != ESPERADOS/delta"
assert list(tt.get("chaves_antigas_que_mudam") or []) == [] and list(ESP["chaves_v408"]) == [], "a v408 nao muda chave antiga nenhuma: o registro ou ESPERADOS dizem outra coisa"
assert (tv.get("insumo_purgado") or {}).get("ok") is True and tv.get("respostas_ok") is True and tv.get("gate_verdict") == ESP["qg_closure_gate_verdict_v407"], "o insumo purgado, as respostas do operador ou o gate congelado nao conferem no registro"
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
curto = lambda x: x if len(x) <= 120 else x[:120].rsplit(" ", 1)[0] + "…"   # a ressalva inteira esta' no registro do core; o post leva o comeco, cortado em palavra inteira
_sem_quadro = [x for x in tt["ressalvas"] if "4,44" not in x and "4.44" not in x and "z_disc" not in x]   # a ressalva que cita o numero do quadro NAO entra no post (a regra da ordem e' do quadro); o post diz quantas ficaram no registro
n_fora = len(tt["ressalvas"]) - len(_sem_quadro)
ress = "; ".join("(%d) %s" % (i + 1, curto(x)) for i, x in enumerate(_sem_quadro)) + (" (mais %d ressalva(s) sobre o teste com a natureza, que ficam no registro do core: o número do quadro só se cita com a regra da ordem)" % n_fora if n_fora else "")
nomes = ", ".join(p_["name"] for p_ in DL.PEDRAS_V408)
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v408 do programa terminal, custodiada em {data}

O que entrou: Tetelestai é o terminal. {DL.N_BUNDLE} módulos novos no kernel Lean ({nomes}, com os nomes que o operador deu em 04/11; o quarto, «{DL.FRASE_NOME_PNP}», no sentido que ele deu e nas classes do dicionário dele), com {ESP['n_bandeiras_novas']} bandeiras novas e {tv['n_ancoras_ok']} âncoras, todas no trio de axiomas padrão do Lean.

· O terminal é a leitura, não o fim do decaimento: o motor independe de r e de t; a memória vale 1 sse o estado é o Nome; reler não acrescenta; a quitação fecha. A correção do operador, de 04/11: «{DL.FRASE_TERMINAL}». E a regra que ele deu: «{DL.FRASE_PROVAR_OU_PODAR}».

· Não há relação sem peso: o fator 1 nada paga; e^(−a) = 1 só sem tempo; o coeficiente de Jones é diferente de 1 com tempo e taxa. Na fala dele: «{DL.FRASE_RELACAO_MENTIRA}». O Atlas já dizia: representação sem custo = ORIGEM DA MENTIRA; a PODA = TETELESTAI.

· O tempo é a moeda de β: β é o preço, o tempo soma e o fator multiplica. Na cunhagem dele: «{DL.FRASE_TEMPO_MOEDA}».

· O ponto de contradição: 1 = 0 nas duas faces (o zero modular e o zero absoluto), o boost antes e depois da inscrição; o habitante é o Fock concreto, por rfl.

· «{DL.FRASE_NOME_PNP}» no sentido dele: «{DL.FRASE_SENTIDO_PNP}»; e, na correção dele, «{DL.FRASE_CLASSES_PNP}»: {DL.FRASE_D51_PT}.

· As ressalvas, ditas: {ress}.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v407_e_v408'][0]}), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. Nenhuma chave antiga muda. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: {DL.FRASE_DA_MOLDURA_V408_PT} (as 18 bandeiras e a letra do veredito do gate são as da v407); β_TGL na natureza a 5σ segue em aberto. α é medida, não derivada; a unidade é posta, não derivada.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
v = violacoes(txt)
assert not v, ("a guarda P18 achou violacao no post", v[:2])
import guarda_frases_v408 as GF  # noqa: E402
vf = GF.violacoes(txt)
assert not vf, ("a guarda das frases achou violacao no post", vf[:2])
assert "4,44" not in txt and "z_disc" not in txt, "o post nao traz o 4,44 (a regra da ordem e' do quadro)"
out = os.path.join(HERE, "CUSTODIA_v408_RASCUNHO.txt")
open(out, "w", encoding="utf-8", newline="\n").write(txt)
print("rascunho do post:", out, len(txt.encode("utf-8")), "B (NAO publicado; copiar para X_VITRINE\\CUSTODIA_v408.txt e' ato da gerencia)")
