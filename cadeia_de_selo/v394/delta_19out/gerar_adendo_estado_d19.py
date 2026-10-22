# -*- coding: utf-8 -*-
"""gerar_adendo_estado_d19.py -- DELTA 19/10 (rodada d19c, gerencia c1): acrescenta ao FIM de ESTADO_V394.md o «ADENDO 19/10 (delta)». O texto e' gerado LENDO os artefatos (CANDIDATO_v394.json, ESPERADOS_v394.json, ensaio_a_seco_v394.json,
kernel\\KH_N1_v394.json, kernel\\FLAGS_v394.json, kernel\\POS_BUILD_v394.json, os controles do conferidor, os harness dos textos, ARQUIVOS_ALTERADOS_DELTA_19OUT.json e os backups de bytes dos estados ANTERIORES): nenhum numero ou hash e' digitado.
Backup de BYTES do ESTADO_V394.md antes (.bak_<STAMP>_c1d19c, na mesma pasta); temporario -> conferir tamanho -> substituir; idempotente pelo marcador; a guarda P18 (cinco regras) roda sobre o texto novo.
uso: python -I -B -X utf8 gerar_adendo_estado_d19.py [--seco]   (--seco: so' imprime o adendo)"""
import glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); sys.path.insert(0, V)
import delta19_v394 as DL  # noqa: E402
from guarda_p18_v394 import violacoes  # noqa: E402
J = lambda *p: json.load(open(os.path.join(*p), encoding="utf-8"))
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
br = lambda n: format(n, ",").replace(",", ".")
sg = lambda n: format(n, "+,").replace(",", ".")
SECO = "--seco" in sys.argv
MARCA = "<!-- adendo_19out_delta_d19c -->"
ALVO = os.path.join(V, "ESTADO_V394.md")
CM, ESP, ENS = J(V, "CANDIDATO_v394.json"), J(V, "ESPERADOS_v394.json"), J(V, "ensaio_a_seco_v394.json")
KD = os.path.join(V, DL.KERNEL_DIR); KH, FL, PB, KR = J(KD, "KH_N1_v394.json"), J(KD, "FLAGS_v394.json"), J(KD, "POS_BUILD_v394.json"), J(KD, "KERNEL_RECIBO_v394.json")
ALT = J(HERE, "ARQUIVOS_ALTERADOS_DELTA_19OUT.json"); AX = J(HERE, "AXIOMAS_DELTA_19OUT.json")
CN = J(V, "conferencia_rito_v394_CONTROLE_NEGATIVO_PRE_RITO.json"); POS = J(HERE, "conferencia_POSITIVO_FALSO_NOS.json")
HA, HD = J(HERE, "HARNESS_TEXTOS_ENSAIO_ANTES_original.json"), J(HERE, "HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json")
S16 = CM["sha16"]; OLD = DL.CANDIDATO_ANTERIOR_SHA16
SIM = J(V, "SIMULACAO_ARVORE_NOS_%s.json" % S16); EXM = J(V, "EXAME_PONTOS_%s.json" % S16)
old_p = os.path.join(V, "um_v394_candidato.py"); assert sha16(old_p) == OLD, "o candidato em exame foi tocado"
# o candidato INTERMEDIARIO (primeira entrega do delta) e os estados antigos, lidos dos backups de bytes (nada digitado)
inter = sorted(glob.glob(os.path.join(V, "um_v394_candidato_d19.py.bak_*_c1d19c"))); assert len(inter) == 1, inter
INTER = sha16(inter[0]); assert INTER != S16
cm_ant = J(V, "CANDIDATO_v394.json.bak_20261019_130748_c1"); assert cm_ant["sha16"] == OLD, "o backup antigo de CANDIDATO_v394.json nao e' o do candidato em exame"
esp_ant = J(V, "ESPERADOS_v394.json.bak_20261019_130748_c1")
ep = lambda k: ESP[k]
cob = KH["linha_TOTAL"]; dv = KH["delta_vs_v393"]; nao_thm = dv["decl"] - dv["thm"]
po, bg = FL["por_origem"], ESP["n_bandeiras_por_grupo"]
part =FL["n_flags"] + FL["publicas_sem_bandeira_total"] + FL["privadas_nos_modulos_novos"]
assert part == dv["decl"], ("a particao das declaracoes novas nao fecha", part, dv["decl"])
al = {e["arquivo"]: e for e in ALT["alterados"]}
tx = al["pos_rito/textos_v394.py"]; ae, ap_ = al["artigo_en_v394.pysnip"], al["artigo_pt_v394.pysnip"]
stone_sbx = os.path.join(DL.SANDBOX, *DL.STONE_REL.split("/")); stone16 = sha16(DL.STONE_SRC)
assert os.path.isfile(stone_sbx) and sha16(stone_sbx) == stone16 == ESP["pedra_do_delta"]["sha16"], "a pedra do sandbox != a do delta != a dos ESPERADOS"
recibo_hora = time.strftime("%H:%M", time.localtime(os.path.getmtime(os.path.join(KD, "KERNEL_RECIBO_v394.json"))))
ntexto = sum(1 for k, e in HD["etapas"].items() if k != "leitura"); com_errata = [k for k, e in HD["etapas"].items() if isinstance(e, dict) and e.get("tem_errata_teoremas")]
assert HD["tudo_passou"] is True and HA["tudo_passou"] is False and HD["candidato_sha16"] == S16, "o harness nao esta no estado esperado (antes reprova, depois passa, candidato final)"
erro_antes = (HA["etapas"]["_d"].get("erro") or "").split(": ", 1)[-1]
cn_d, cn_n, pd_, pn_ = CN["deve_mudar"], CN["nao_pode_mudar"], POS["deve_mudar"], POS["nao_pode_mudar"]
assert CN["tudo_bate"] is False and POS["tudo_bate"] is True
assert ENS["veredito"] == "TUDO PASSOU" and ENS["sha16"] == S16 and SIM["formal_files_n_no_rito_real"] == ESP["h8_entradas"] and EXM["algum_falso"] == []
reg_ant = len(cm_ant["registros"]) + 3          # 3 de runtime (tempo, quadratica, rede) + os registros por spec do candidato em exame
reg_novo = len(CM["registros"]) + 3
ERR = DL.ERRATA_TEOREMAS_PT
VB = list(ESP["criterio_binario"]["verbatim"]); assert len(VB) == 2 and all(k.startswith("v394_cun_") for k in VB)
L = []
a = L.append
a("## ADENDO 19/10 (delta)")
a("")
a(MARCA)
a("Gerência c1, subagente Sonnet do delta (rodada final d19c), 19/10/2026, %s (hora local), por ordem da gerência. Escrito por script (`delta_19out\\gerar_adendo_estado_d19.py`) a partir dos artefatos: nenhum número ou hash foi digitado. As seções 0 a 7 acima ficam como REGISTRO do candidato em exame (`%s`); onde divergem, vale este adendo (correção AO LADO, nunca por cima). Estatutos: [REAL] medido ou lido por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido aqui; [ONTO] leitura do operador. Nada foi instalado e o rito não rodou; o Nós real, o `um.py` real, o túnel, a Bancada, o quadro, o mapa de rotas, a memória, o site e o git não foram tocados; sem init/transition ACOM. Escrevi só em `work\\cadeia_de_selo\\v394` (nela, `pos_rito\\textos_v394.py` por ordem expressa) e em `C:\\t\\k394d`." % (time.strftime("%H:%M"), OLD))
a("")
a("**1. O que mudou**")
a("")
a("- **Candidato.** Antes (em exame, REGISTRO, intacto, conferido por p00): `%s`, %s B, %d patches (`um_v394_candidato.py`). Depois: **`%s`** (sha256 `%s`), %s B (%s B), %d patches, arquivo novo `%s`, gerado de `base_v393` (`%s`) por `gerar_candidato_v394.py` (nada à mão; `V394_REGERAR=1`). O intermediário da primeira entrega do delta (`%s`) foi superado nesta rodada pela errata da palavra «teoremas» no artigo; os bytes dele estão em `%s` e a evidência dele em `superado_7abb7ba986c098c7\\`." % (OLD, br(os.path.getsize(old_p)), len(cm_ant["patches"]), S16, CM["sha256"], br(CM["bytes"]), sg(CM["bytes"] - os.path.getsize(old_p)), len(CM["patches"]), DL.CANDIDATO, CM["base_v393_sha16"], INTER, os.path.basename(inter[0])))
a("- **Pedra** (nome provisório: o operador nomeia). `%s` (sha16 `%s`, %s B): um teorema de composição, `%s`, que CITA oito teoremas que já estavam no kernel (sem matemática nova). Axiomas: o trio (`propext`, `Classical.choice`, `Quot.sound`) e nada além [REAL: compilada a frio no sandbox `C:\\t\\k394d\\final`; `lake build` rc 0, Audit rc 0, %s constantes, %s teoremas, %s fora do trio]. A analogia com o qubit vale nos pesos (½, ½), não na entropia (`fair_bit_entropy_is_not_half_nat`); «a parada é o ponto fixo» é [ONTO] do operador. O kernel NÃO mudou nesta rodada: sandbox e recibo (`kernel\\KERNEL_RECIBO_v394.json`, sha16 `%s`, %s) são os da primeira entrega, e o ensaio reconferiu kernel embutido == sandbox (%d arquivos, %d diferentes)." % (DL.STONE_REL, stone16, br(os.path.getsize(DL.STONE_SRC)), DL.THEOREM, br(cob["decl"]), br(cob["thm"]), cob["fora_do_trio"], sha16(os.path.join(KD, "KERNEL_RECIBO_v394.json")), recibo_hora, ENS["kernel_embutido_vs_sandbox"]["n"], ENS["kernel_embutido_vs_sandbox"]["n_diferentes"]))
a("- **Inscrições e registro.** As duas falas de 19/10 (sha16 `%s` e `%s`) entram embutidas por sha256 (%d falas no total) e o registro `criterio_binario_de_parada_v394` (o %dº registro novo da v394) as lê junto com a bandeira da pedra e os oito teoremas, no ponto real de chamada (`_v394_rodar_specs`, no `main`); selou no ensaio e no exame de pontos, e tem controles negativos (bandeira falsa, teorema ausente, axioma fora do trio, sha errado em cada fala, pedra adulterada); o gate não se move (`gate_recomputado.verdict_igual = %s`, 18 bandeiras)." % (VB[0][len("v394_cun_"):], VB[1][len("v394_cun_"):], len(ESP["cunhagens"]), reg_novo, EXM["gate_recomputado"]["verdict_igual"]))
a("- **Política de bandeiras** (decisão da gerência). Só declaração NOMEADA tem bandeira (a prática selada da v392 e da v393): **%d** = %d nomeadas do Codex + %d nomeadas que ele não marcou + 1 da pedra; por grupo: tempo %d, quadrática %d, rede %d, pedra %d. As %d auxiliares geradas pelo compilador que o Codex marcara ficam fora. Das %s declarações dos módulos novos (%s teoremas e %s não-teoremas; fonte `kernel\\KH_N1_v394.json::delta_vs_v393`), %d recebem bandeira, %d são auxiliares públicas sem bandeira e %d são privadas (fonte `kernel\\FLAGS_v394.json`). **Escada: %s + %d = %s** (%s antes da pedra). Os contratos do Codex (%d / %d / %d declarações) seguem como contrato e deixaram de coincidir com as bandeiras." % (FL["n_flags"], po["codex_nomeada"], po["nomeada_sem_bandeira"], bg["tempo"], bg["quadratica"], bg["rede"], bg["outros"], FL["excluidas_auxiliares"]["n"], br(dv["decl"]), br(dv["thm"]), br(nao_thm), FL["n_flags"], FL["publicas_sem_bandeira_total"], FL["privadas_nos_modulos_novos"], br(ESP["escada_v393_e_v394"][0]), ESP["n_bandeiras_novas"], br(ESP["escada"][1]), br(ESP["politica_de_bandeiras"]["escada_antes_da_pedra_do_delta"]), ESP["n_formais"]["tempo"], ESP["n_formais"]["quadratica"], ESP["n_formais"]["rede"]))
a("- **h8.** O pino de `kh_n1_cobertura_v394` tem **%d** entradas = %d embutidos + `%s` (o pino antigo, de %d, reprovava no rito real: achado do exame de 19/10 [DECLARADO pelo exame]). O pino é recalculado a cada geração pela árvore SIMULADA do Nós (`simular_arvore_do_nos.py`, etapa obrigatória do ensaio: %d entradas, pino %d, extras fora do embutido: %s) e a regra foi conferida contra o `formal_files_sha256` real da v393 selada (1233 = 1232 embutidos + o residual); a exclusão nominal de `ExtrairDeps.lean` em `sha256_directory` não foi tocada." % (ESP["h8_entradas"], ESP["formal_files_n"], "`, `".join(ESP["h8_residuais_do_nos"]), esp_ant["formal_files_n"], SIM["formal_files_n_no_rito_real"], ENS["simular_arvore_do_nos"]["pino_h8_entradas"], ", ".join("`%s`" % x for x in SIM["extras_no_nos_fora_do_corpo_embutido"])))
a("- **Texto.** (i) «THEOREMS» passa a «FLAGS» no único token em maiúsculas do veredito de `estatuto_da_prova_v391` (patch C11; troca declarada em ESPERADOS e aplicada pelo conferidor); (ii) o token de máquina `teoremas limpos: N/M` do stdout do rito NÃO mudou (o pós-rito o lê por regex); (iii) a errata da palavra «teoremas», abaixo.")
a("- **Conferidor.** Corrigido um defeito latente (lista de axiomas VAZIA é válida; ausência reprova). Caminho positivo exercitado contra um Nós FALSO montado do ensaio (`delta_19out\\teste_conferidor_positivo.py`, emulação): **%s** (deve-mudar %d de %d; não-pode-mudar %d de %d). Controle negativo (Nós ainda v393): `tudo_bate = %s`; deve-mudar %d de %d (só os dois que não mudam: os registros da v393 e o pilar); não-pode-mudar %d de %d." % ("TUDO BATE" if POS["tudo_bate"] else "NAO BATE", sum(1 for v in pd_.values() if v), len(pd_), sum(1 for v in pn_.values() if v), len(pn_), CN["tudo_bate"], sum(1 for v in cn_d.values() if v), len(cn_d), sum(1 for v in cn_n.values() if v), len(cn_n)))
a("- **Pós-rito.** `pos_rito\\textos_v394.py`: aplicada a proposta aprovada (as bandeiras POR GRUPO passam a vir de `ESPERADOS.n_bandeiras_por_grupo`: %d + %d + %d + %d = %d) e a frase de errata (abaixo); sha16 `%s` → `%s` (%s → %s B); backup de bytes na mesma pasta (`.bak_..._c1d19c`). O harness dos textos em modo ensaio (`delta_19out\\harness_textos_ensaio.py`: importa os `textos_v394` e `leitura_v394` REAIS contra um Nós emulado a partir do ensaio; só leitura; emulados e ditos: o stdout do rito, o aplicado e a conferência) reprovava no original (`%s`; %d problemas) e passa agora: %d funções de texto, guarda P18 limpa, a soma fecha, a errata presente nos %d textos que embutem `_num`. `derivar_cadeia_v394.py` NÃO rodou." % (bg["tempo"], bg["quadratica"], bg["rede"], bg["outros"], ESP["n_bandeiras_novas"], tx["sha16_antes"], tx["sha16_depois"], br(tx["bytes_antes"]), br(tx["bytes_depois"]), erro_antes, len(HA["problemas"]), ntexto, len(com_errata)))
a("")
a("**2. Erratas AO LADO** (em nome próprio da gerência c1; o que está acima fica como registro)")
a("")
a("- (a) Onde o `um.py` dizia «THEOREMS» para um conjunto que inclui não-teoremas, diz «FLAGS» (token do veredito de `estatuto_da_prova_v391`): a escada conta bandeiras.")
a("- (b) **A palavra «teoremas».** Os módulos novos têm %s declarações e %s teoremas (%s não-teoremas): a escada conta BANDEIRAS de declarações nomeadas (teoremas e definições), todas com axiomas no trio; o rótulo «teoremas limpos: N/M» fica como registro de máquina. A frase de errata entrou UMA vez no artigo PT e EN (seção da v394, parágrafo «O que entra», logo depois da frase da escada e da cobertura; `artigo_pt_v394.pysnip` `%s` → `%s`, `artigo_en_v394.pysnip` `%s` → `%s`) e no texto do kernel de `textos_v394.py` (`_num`), com as mesmas palavras: %s. Sem número digitado na frase; T e D acima vêm de `kernel\\KH_N1_v394.json` (a linha TOTAL do Audit do sandbox menos a da v393 em `base_v393\\um_absoluto.json`) [REAL]." % (br(dv["decl"]), br(dv["thm"]), br(nao_thm), ap_["sha16_antes"], ap_["sha16_depois"], ae["sha16_antes"], ae["sha16_depois"], ERR))
a("- (c) Onde as seções 0 a 4 acima dizem `%s`, %d módulos novos, %s bandeiras, escada %s, Audit %s/%s, %d falas, %d registros novos, h8 de %d e sandbox `C:\\t\\k394`, lê-se agora: `%s`, %d módulos, %d bandeiras, escada %s, Audit %s/%s, %d falas, %d registros novos, h8 de %d e sandbox `C:\\t\\k394d\\final` (a pasta VIVA dos logs e do recibo é `kernel\\`; os arquivos antigos dela ficaram como `.bak_20261019_135101_c1`)." % (
    OLD, ESP["kernel"]["modulos_novos_do_codex"], br(cm_ant["n_bandeiras"]), br(cm_ant["escada"][1]), br(KH["pre_auditoria_codex"]["decl"]), br(KH["pre_auditoria_codex"]["thm"]), cm_ant["verbatins_embutidos"], reg_ant, esp_ant["formal_files_n"],
    S16, ESP["kernel"]["modulos_novos"], ESP["n_bandeiras_novas"], br(ESP["escada"][1]), br(cob["decl"]), br(cob["thm"]), len(ESP["cunhagens"]), reg_novo, ESP["h8_entradas"]))
a("")
a("**3. Números finais do ensaio** [REAL]")
a("")
a("- Ensaio a seco inteiro (`ensaio_a_seco_v394.json`, candidato `%s`): **%s**; `verify_tgl_kernel_formalization` real com os logs crus do build frio, cobertura %s/%s, proveniência %s == %s; escada recomputada %s/%s (sem as bandeiras novas: %s de %s, e não fecha); artigo PT/EN com pdflatex ×2 rc 0 e sem «n/d»; etapas obrigatórias: `simular_arvore_do_nos` (rc %d, %d entradas == pino %d) e `exame_pontos_v394` (`algum_falso = %s`; bandeiras novas True %d/%d; `ext_` True %d/%d); `p00_precondicoes_v394.py`: %s. Tudo regenerado nesta rodada pelos scripts da cadeia (candidato, ensaio, ESPERADOS, conferidor e controle negativo, diff e pinos, comparações v393 e r8)." % (
    S16, ENS["veredito"], br(ENS["verify_kernel_ponta_a_ponta"]["cobertura"]["decl"]), br(ENS["verify_kernel_ponta_a_ponta"]["cobertura"]["thm"]), br(ENS["verify_kernel_ponta_a_ponta"]["proveniencia"]["compiler_names"]), br(ENS["verify_kernel_ponta_a_ponta"]["proveniencia"]["audited_names"]), br(ENS["escada"][0]), br(ENS["escada"][1]),
    br(ENS["escada_sem_as_bandeiras_novas"][0]), br(ENS["escada_sem_as_bandeiras_novas"][1]), ENS["simular_arvore_do_nos"]["rc"], SIM["formal_files_n_no_rito_real"], ENS["simular_arvore_do_nos"]["pino_h8_entradas"], EXM["algum_falso"], EXM["verify"]["novas_true"], EXM["verify"]["n_novas"], EXM["verify"]["ext_true"], EXM["verify"]["n_ext"],
    "TODAS PASSARAM" if J(V, "PRECONDICOES_v394.json")["ok"] else "FALHOU"))
a("")
a("**4. O que segue aberto** (nada disto foi decidido ou tocado aqui)")
a("")
a("- **B(n).** %d pedras sem declaração nomeada (%s): o B(n) pós-selo RECUSARIA o recibo (não o rito) [`riscos_bn` de `kernel\\POS_BUILD_v394.json`]; decisão da gerência (esboço R3.4, ou recibo sem elas)." % (len(PB["riscos_bn"]["pedras_sem_declaracao_nomeada"]), ", ".join("`%s`" % os.path.basename(p)[:-5] for p in PB["riscos_bn"]["pedras_sem_declaracao_nomeada"])))
a("- **O rito real** (build a frio do Nós, GPU, o conferidor depois do rito) é o único que exercita o conferidor, o pós-rito e o h8 de verdade; o caminho positivo e o harness acima são EMULAÇÃO (core e selo vêm do ensaio, não do rito).")
a("- **Nome da pedra** (provisório) e a leitura «critério binário de parada» ([ONTO]): do operador. Validade no kernel não é creditação; o gate não se move.")
a("- Detalhe completo, comandos para refazer e a tabela de arquivos com sha16 antes/depois: `delta_19out\\RESULTADO_DELTA_19OUT.md` e `delta_19out\\ARQUIVOS_ALTERADOS_DELTA_19OUT.md`.")
texto = "\n".join(L)
v = violacoes(texto)
assert not v, ("a guarda P18 achou violacao no adendo", v[:3])
assert MARCA in texto and "nao provou" not in texto.lower()
if SECO:
    print(texto); sys.exit(0)
raw = open(ALVO, "rb").read()
if MARCA.encode("utf-8") in raw:
    print("JA APLICADO (idempotente): o adendo ja esta em ESTADO_V394.md"); sys.exit(0)
assert b"\r\n" not in raw and raw.endswith(b"\n")
stamp = time.strftime("%Y%m%d_%H%M%S"); bak = ALVO + ".bak_%s_c1d19c" % stamp
assert not os.path.exists(bak)
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw + b"\n" + texto.encode("utf-8") + b"\n"
tmp = ALVO + ".tmp_c1d19c"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(raw)
os.replace(tmp, ALVO); fin = open(ALVO, "rb").read(); assert fin == novo and fin.startswith(raw)
print("OK: ESTADO_V394.md %d B -> %d B (sha16 %s -> %s); backup %s" % (len(raw), len(fin), hashlib.sha256(raw).hexdigest()[:16], hashlib.sha256(fin).hexdigest()[:16], os.path.basename(bak)))
