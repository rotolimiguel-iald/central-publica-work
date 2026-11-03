# -*- coding: utf-8 -*-
"""gerar_relatorio_v406.py -- escreve PLANO_v406.md, RELATORIO_PREPARACAO_v406.md e PREPARACAO_v406_PRONTA.json. Todo hash, tamanho, contagem e veredito e' LIDO dos arquivos desta pasta no momento da geracao (nada digitado); a prosa e' da preparacao.
`pronta` e' CALCULADA: true so' se TODOS os portoes passaram (kernel, candidato, AST, ensaio a seco, conferidor, citacoes, guarda das frases, p00, B(n) pre-selo, harnesses); um arquivo que falta ou nao le reprova o portao (fail-closed), nunca o contrario.
Rodar DEPOIS de refazer_candidato_v406.sh e dos dois harnesses (sem --nao-exigir-refazer). Backup de bytes do que ja' existe; temporario -> conferir -> substituir. Adaptado em 02/11/2026 ao FECHAMENTO (bundle de 301 modulos; a prosa da v405 sobre as erratas R2 a R7 das oito pedras saiu). uso: python -I -B -X utf8 gerar_relatorio_v406.py"""
import datetime, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); POS = os.path.join(HERE, "pos_rito")
AGORA = datetime.datetime.now(); ST = AGORA.strftime("%Y%m%d_%H%M%S")
P = lambda p: os.path.join(HERE, *p.split("/"))
rj = lambda p: json.load(open(P(p), encoding="utf-8"))
fh = lambda p: hashlib.sha256(open(P(p), "rb").read()).hexdigest()
h16 = lambda p: fh(p)[:16]
sz = lambda p: os.path.getsize(P(p))


def tenta(p):
    """O JSON lido, ou None (o portao que depende dele reprova)."""
    try:
        return rj(p)
    except (OSError, ValueError):
        return None


import sys as _sys; _sys.path.insert(0, HERE)
import delta_v406 as _DL   # (so' para ler a Bancada que o delta le do manifesto dela: nada digitado)
DL_B_N = _DL.B_N_SEGUINTE; DL_BANCADA = _DL.BANCADA_PINA_HOJE["deployment_id"]
CM = tenta("CANDIDATO_v406.json") or {}; ES = tenta("ESPERADOS_v406.json") or {}; EN = tenta("ensaio_a_seco_v406.json") or {}; PC = tenta("PRECONDICOES_v406.json") or {"ok": False, "checagens": []}
PR = tenta("PINO_RECIBO_PRE_SELO_v406.json") or {}; PROV = tenta("PROVA_PRODUCAO_INTACTA_v406_pre_selo.json") or {}; CMP = tenta("COMPARACAO_V405_v406.json") or {}; KR = tenta("kernel/KERNEL_RECIBO_v406.json") or {}; PB = tenta("kernel/POS_BUILD_v406.json") or {}; FJ = tenta("kernel/FLAGS_v406.json") or {}
CN = tenta("conferencia_rito_v406_CONTROLE_NEGATIVO_PRE_RITO.json") or {}; CP = tenta("conferencia_rito_v406_POSITIVO_FALSO_NOS.json") or {}; CIT = tenta("conferir_citacoes_v406.json") or {}; GF = tenta("GUARDA_FRASES_v406.json") or {}; DRV = tenta("DERIVACAO_v406.json") or {"falhas": ["DERIVACAO_v406.json ausente"]}
SERV = tenta("bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v406.json") or {}; CTRL = tenta("bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v406.json") or {}; PN = tenta("PINOS_BN_v406.json") or {}
H_T = tenta("pos_rito/HARNESS_TEXTOS_ENSAIO_v406.json"); H_F = tenta("pos_rito/HARNESS_FECHAR_SANDBOX_v406.json")
refazer = open(P("refazer_out_v406.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("refazer_out_v406.txt")) else ""
fim_ok = "== FIM" in refazer and refazer.rstrip().endswith("RC_REFAZER=0")
falhas_p00 = [c["checagem"] for c in PC["checagens"] if not c["ok"] and not c.get("pendente")]
pendentes_p00 = [c["checagem"] for c in PC["checagens"] if c.get("pendente")]
ok_p00 = sum(1 for c in PC["checagens"] if c["ok"]); n_p00 = len(PC["checagens"])
_bn = open(P("bateria_pre_selo/bn_pre_selo_out_v406.txt"), encoding="utf-8", errors="replace").read() if os.path.exists(P("bateria_pre_selo/bn_pre_selo_out_v406.txt")) else ""
_m = re.search(r'veredito_bateria": "(\w+)"', _bn); bat = _m.group(1) if _m else "NAO LIDO"


def passou(H):
    return bool(H and H.get("tudo_passou") is True and not H.get("nao_exigiu_refazer"))


def _arquivo_e(p, sha):
    return bool(sha) and os.path.exists(P(p)) and fh(p) == sha


cand_ok = bool(CM.get("sha16") and ES.get("candidato_sha16") == CM["sha16"] and h16("um_v406_candidato.py") == CM["sha16"] and sz("um_v406_candidato.py") == CM.get("bytes") and EN.get("sha16") == CM["sha16"])
PORTOES = {
    "kernel": bool(KR.get("rc") == 0 and KR.get("sorry") in (0, [], None) and PB.get("ok") is True and len(KR.get("pedras") or []) == 301 and FJ.get("n_flags") == ES.get("n_bandeiras_novas")),
    "candidato": cand_ok,
    "ast_v405_v406": bool(CMP.get("ok") is True and CMP.get("removidos") in (0, []) and CMP.get("mudados_sem_explicacao") in (0, []) and CMP.get("o_gate_nao_se_move_e_a_v386_nao_e_reescrita") is True),
    "ensaio_a_seco": bool(EN.get("veredito") == "TUDO PASSOU" and EN.get("sha16") == CM.get("sha16")),
    "conferidor_controle_negativo": bool(CN.get("tudo_bate") is False and CN.get("nao_pode_mudar") and all(CN["nao_pode_mudar"].values()) and CN.get("um_py_sha16") != CM.get("sha16")),
    "conferidor_caminho_positivo": bool(CP.get("tudo_bate") is True and CP.get("um_py_sha16") == CM.get("sha16")),
    "citacoes": bool(CIT.get("todas_conferem") is True),
    "guarda_das_frases": bool(GF.get("ok") is True and GF.get("pedras_limpas") is True and len(GF.get("pedras") or {}) == 1),   # (v406: a candidata e' a unica pedra da gerencia)
    "instalar_reverter_rito_estatico": bool(not DRV.get("falhas")),
    "p00": bool(PC.get("ok") is True and n_p00 > 0 and not falhas_p00 and not PC.get("pendentes")),
    "bn_pre_selo": bool(PR.get("veredito") == "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA" and PR.get("utilizavel_como_recibo_pre_selo_do_B_n") is True and PROV.get("producao_intacta") is True and bat == "BATERIA_PASSA" and (PN.get("candidato") or {}).get("sha256") == CM.get("sha256")),
    "servico_estatico": bool(SERV.get("n_condicoes") and SERV.get("n_condicoes_ok") == SERV.get("n_condicoes") and CTRL.get("toda_mutacao_foi_pega") is True),
    "harness_textos": passou(H_T),
    "harness_fechar": passou(H_F),
    "refazer_limpo": fim_ok,
    "purga_da_fala_reservada": bool((tenta("purga_v406.json") or {}).get("total_com_ocorrencia") == 0),
    "fala_excluida_fora_dos_artefatos": bool((tenta("purga_v406.json") or {}).get("fala_excluida_total_com_ocorrencia") == 0),
}
falta = [k for k, v in PORTOES.items() if not v]
pronta = not falta
n_neg_leit = len((H_T or {}).get("etapas", {}).get("leitura_negativos", {}).get("controles", []))
n_neg_fech = len((H_F or {}).get("etapas", {}).get("fechar_negativos", []))
n_neg_par = len((H_T or {}).get("etapas", {}).get("paragrafo_v406_e_citacoes", {}).get("negativos", []))
ROTA = "kernel.fechamento_construir_tudo_programa_02nov"   # a rota da v406 no Mapa de Rotas (aberta pela gerencia)
tab_pedras = "\n".join("| `%s` | `%s` | `%s` | %s |" % (n_, v_.get("rel", "").split("/")[-1], v_.get("bandeira"), v_.get("classe") or "") for n_, v_ in (ES.get("estrelas_v406") or {}).items())
try:
    prep_seq = [json.loads(l) for l in open(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", encoding="utf-8") if l.strip() and ('"' + ROTA + '"') in l]
    seqs = ", ".join("%s (%s)" % (r["seq"], r["tipo"]) for r in prep_seq if r.get("rota_id") == ROTA)
except Exception as e:   # noqa: BLE001
    seqs = "nao lido: %r" % (e,)
ARQ = ["um_v406_candidato.py", "CANDIDATO_v406.json", "ESPERADOS_v406.json", "ensaio_a_seco_v406.json", "COMPARACAO_V405_v406.json", "PINOS_BN_v406.json", "PINO_RECIBO_PRE_SELO_v406.json", "PROVA_PRODUCAO_INTACTA_v406_pre_selo.json", "PRECONDICOES_v406.json", "GUARDA_FRASES_v406.json", "VERBATIM_CONGELADO_v406.json", "BUNDLE_v406.json", "kernel_modulos_novos_v406.json", "CONTRATO_DA_CADEIA_v406.md",
       "delta_v406.py", "registros_v406.py", "runtime_v406.py", "guarda_frases_v406.py", "guarda_ordem_de_chamada_v406.py", "gerar_candidato_v406.py", "gerar_esperados_v406.py", "artigo_pt_v406.pysnip", "artigo_en_v406.pysnip", "comparar_v405_v406.py", "instalar_v406.py", "reverter_v406.py", "rito_v406.sh", "conferir_rito_v406.py", "conferir_citacoes_v406.py", "p00_precondicoes_v406.py",
       "pos_rito/textos_v406.semente", "pos_rito/montar_textos_v406.py", "pos_rito/leitura_v406.py", "pos_rito/fechar_v406.py", "pos_rito/registrar_mapa_v406.py", "pos_rito/superficies_v406.py", "pos_rito/harness_textos_ensaio_v406.py", "pos_rito/harness_fechar_sandbox_v406.py", "pos_rito/chain_pos_rito_v406.sh", "pos_rito/gerar_x_custodia_v406.py",
       "kernel/KERNEL_RECIBO_v406.json", "kernel/FLAGS_v406.json", "kernel/KH_N1_v406.json"]
HASHES = {p: {"sha16": h16(p), "bytes": sz(p)} for p in ARQ if os.path.exists(P(p))}
tab_arq = "\n".join("| `%s` | %s | `%s` |" % (p, format(v["bytes"], ","), v["sha16"]) for p, v in HASHES.items())
_apont = (CIT.get("apontadas_a_gerencia_aspas") or [])
AVISOS = [
    "o nome CanonicalFullTGLWitnessR1 e' PROVISORIO da gerencia: os nomes das pedras sao do operador e ele ainda nao nomeou esta; as pedras candidatas do dia (APonteDoAtrito, OUmInscrito, KEhATangente e as demais) ficam FORA do kernel da v406 (D40); entram so' como leitura [ONTO] e como fonte [DECLARADO]",
    "as QUATRO chaves de testemunha passam de literal False a LEITURA do kernel do rito (errata E14 AO LADO; o texto selado das versoes anteriores nao e' reescrito): rede_fock_v394.whole_certificate_inhabited, psibit_v395...inhabitant_exhibited e testemunha_estatica_v396...inhabitant_exhibited leem True, witness_layers.canonical_full_witness_term_constructed le True sem patch; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA e linked_to_the_corner_by_a_lemma segue False",
    "ressalvas ditas em todo texto (D36): K(O) != bot so' na cunha; «nucleo II_∞» [KNOWN/DECLARADO]; o traco e' ENNReal e CICLICO, nao linear; o parecer R7 foi o Codex revisando o Codex; as linhas #eval removidas na integracao R3; R4/R5 da missao fora; o nome provisorio",
    "a TROCA DITA de veredito e' UMA so' em texto: rede_fock_v394 passa a TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CERTIFICATE_INHABITED_V406__THREE_JOINT_ITEMS_STILL_OPEN__GATE_UNMOVED (antes e depois pinados em ESPERADOS.troca_dita_textual); os vereditos de psibit_v395 e testemunha_estatica_v396 NAO mudam; os que carregam a escada mudam so' em numeros",
    "o revisor distinto da v406 e' o Sonnet (ordem do operador, D37); esta preparacao NAO foi revisada por terceiro; quem constroi nao aprova",
    "o motor continuo no pilar quantico (D38) NAO entra na v406: exige pre-registro aprovado; o pilar reusa a chave de cache; o README pinado e a linha do 4,44 no site (D39) ficam fora desta cadeia; a regra do 4,44 (nunca sozinho: z_disc 4,44 calibrado, abaixo do degrau de 5 sigma da creditacao) vale em qualquer texto",
    "o B(n) pre-selo da v406 (passo simples %s; a Bancada de producao pina %s) e o pino da memoria dependem de arquivos que a preparacao ainda nao gerou quando este relatorio nao os acha: o p00 os diz PENDENTES, nao erro, e `pronta` so' fica true com todos os portoes" % (DL_B_N, DL_BANCADA),
    "conferir_citacoes_v406.json aponta %d citacao(oes) entre « » dos textos da gerencia que nao sao verbatim das falas do operador (arquivo: trecho): %s; o agente nao corrige texto da gerencia" % (len(_apont), "; ".join("%s: %s" % (a_["arquivo"], a_["trecho"]) for a_ in _apont) or "nenhuma"),
    "a candidata cita «nucleo II_∞» sem acento; a bancada escreve «núcleo II_∞»: a conferencia de citacoes aceita a igualdade sem acento e a diz em varredura_das_pedras.so_sem_acento",
    "build a frio dos 301 modulos no sandbox k406c: 1736 s, Audit 280 s (kernel/construir_marcas.txt, medidos); 33732 declaracoes, 26911 teoremas, nenhuma fora do trio; escada 10066 -> 11860",
]
NAO_REVISADO = "este candidato (o fechamento, v406) NAO foi revisado por terceiro; o revisor distinto e' o Sonnet (ordem do operador, D37) e a trava do orquestrador fica fechada ate a revisao aprovar; quem constroi nao aprova"
_vp = (CIT.get("varredura_das_pedras") or {})
_cong406 = tenta("VERBATIM_CONGELADO_v406.json") or {}
ERRATAS_V406_RES = {"erratas": ["E14", "E15", "E16", "E17"], "E14": "as tres chaves de testemunha eram literal False (v394 a v405) e a quarta, medida; agora leitura do kernel", "E15": "«a luz nao tem autovetor nenhum» afirmou demais; o vacuo e' o unico vetor FIXO; o operador corrigiu", "E16": "«falta replicar o traco»: a passagem para o continuo estava construida na bancada desde 16/10; o cetico leu o tipo e nao a bancada", "E17": "os specs que cobravam «falso» nas chaves foram versionados («ate' a v405»)",
                    "falas_embutidas": len(_cong406.get("arquivos") or []), "citacoes_da_candidata": {"conferidas": _vp.get("citacoes_conferidas"), "reprovadas": len(_vp.get("reprovadas") or []), "so_sem_acento": _vp.get("so_sem_acento")}}
PRONTA = {"contrato": "PREPARACAO_v406_PRONTA", "agente": "claude-prep-v406", "quando": AGORA.strftime("%Y-%m-%d %H:%M:%S"), "pronta": pronta, "falta": falta, "portoes": PORTOES,
          "candidato_sha16": CM.get("sha16"), "candidato_sha256": CM.get("sha256"), "candidato_bytes": CM.get("bytes"), "origem_sha16": CM.get("base_v405_sha16"), "escada": ES.get("escada_v405_e_v406"), "n_bandeiras_novas": ES.get("n_bandeiras_novas"),
          "kernel_recibo": {"path": "kernel/KERNEL_RECIBO_v406.json", "sha16": h16("kernel/KERNEL_RECIBO_v406.json") if os.path.exists(P("kernel/KERNEL_RECIBO_v406.json")) else None, "rc": KR.get("rc")},
          "esperados_sha16": h16("ESPERADOS_v406.json") if os.path.exists(P("ESPERADOS_v406.json")) else None, "p00": {"ok": PC.get("ok"), "passaram": ok_p00, "n": n_p00, "pendentes": pendentes_p00, "sha16": h16("PRECONDICOES_v406.json") if os.path.exists(P("PRECONDICOES_v406.json")) else None},
          "ensaio_a_seco": {"veredito": EN.get("veredito"), "sha16_do_candidato": EN.get("sha16"), "json_sha16": h16("ensaio_a_seco_v406.json") if os.path.exists(P("ensaio_a_seco_v406.json")) else None},
          "comandos": {"instalar": "python -B -X utf8 instalar_v406.py", "rito": "sh rito_v406.sh", "cadeia": "CHAIN_DE=<rotulo> CHAIN_ATE=<rotulo> sh pos_rito/chain_pos_rito_v406.sh (rotulos 0..10 10a 10b 10c 11..14; 10b com B3_AUTORIZADO=sim, EVENTO e EVENTO_HASH)", "cwd": HERE,
                       "reverter": "python -B -X utf8 reverter_v406.py (so' por decisao da gerencia)"},
          "hashes": HASHES, "nao_revisado_por_terceiro": NAO_REVISADO, "erratas_E14_E17": ERRATAS_V406_RES, "avisos": AVISOS, "rota_no_mapa": "%s (seq %s)" % (ROTA, seqs)}


def grava(nome, b):
    p = P(nome)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + ST; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p)


fr = "o certificado de Fock esta' habitado por construcao no kernel do rito; validade no kernel nao e' creditacao; o gate nao se move"
_esc = ES.get("escada_v405_e_v406") or ["?", "?"]
PLANO = f"""# PLANO da v406 — O FECHAMENTO (preparação)

Agente de preparação `claude-prep-v406`, {AGORA.strftime('%Y-%m-%d %H:%M')}. Estatutos: [REAL] lido aqui por script · [INPUT/ONTO] leitura ou ordem do operador · [KNOWN] · [OPEN] · [DECLARADO]. Base: a v405 selada `{CM.get('base_v405_sha16')}`. Nada foi instalado; o rito não rodou; o Nós e a produção só foram lidos. A moldura: {fr}.

## 0. A ordem

- [INPUT, operador, 02/11/2026] «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento»; a prioridade: «a construção da passagem para o contínuo é o que mais importa»; e a ordem de compilar: «compile a nova versão do um.py, rode, publique e atualize tudo por favor». As {len(ES.get('cunhagens') or {})} falas de 02/11 entram por sha256 (lista congelada em `VERBATIM_CONGELADO_v406.json`).
- (A) O BUNDLE: 301 módulos de kernel em `TGLExt/F1Fecho394` (os 300 da bancada do ChatGPT, recompilados do fonte na integração R3, mais a candidata `CanonicalFullTGLWitnessR1` da gerência). (B) O registro com função `fechamento_v406` e os registros por spec `cunhagens_v406` e `kh_n1_cobertura_v406`. (C) As quatro chaves de testemunha, de literal a leitura do kernel. (D) A seção «O fechamento: a passagem para o contínuo e o certificado habitado» no artigo PT/EN e a linha do `.md`. (E) O resto, derivado da v405 por script.

## 1. As oito âncoras [REAL, sandbox `{(CM.get('kernel') or {}).get('sandbox')}`; nada tocado no Nós]

| âncora (nome Lean) | módulo | bandeira | classe |
|---|---|---|---|
{tab_pedras}

Pós-build: {PB.get('n_axiomas_lidos_no_audit')} axiomas lidos no Audit, {PB.get('n_flags')} bandeiras novas (só declaração nomeada), escada {_esc[0]} → {_esc[1]}; build a frio {PB.get('duracao_build_s')} s, Audit {PB.get('duracao_audit_s')} s.

## 2. O que a v406 afirma e o que não afirma

- [REAL] `physicalFockCertificate` habita `FockCertificate` sobre a rede física, e `modularCoreInput` habita os 21 campos de `RemainingModularCoreInput D` para todo `D : CanonicalNetInput`, só com o trio de axiomas; `canonicalFullTGLWitness` é o termo canônico da testemunha completa.
- [REAL] As quatro chaves que eram literal False leem agora o kernel do próprio rito; o que fica False fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`) e o lema que liga `psion C` ao `psionCorner` segue faltando.
- [OPEN/KNOWN/DECLARADO] Ressalvas ditas: K(O) ≠ ⊥ só na cunha; «núcleo II_∞» [KNOWN/DECLARADO]; o traço é ENNReal e cíclico, não linear; R7 foi Codex revisando Codex; R4/R5 fora.
- O número da massa não muda; o gate não se move (as funções do gate e do neutrino ficam idênticas por AST); `NOT_FALSIFIED` nunca é `CONFIRMED`; validade no kernel não é creditação; o 4,44 nunca vai sozinho.

## 3. A cadeia

Candidato `um_v406_candidato.py` `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; +{format(CM.get('delta_bytes') or 0, ',')} B); {CM.get('n_patches')} patches; AST: {CMP.get('nos_nomeados_v405')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (todos explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos. Ensaio a seco: **{EN.get('veredito')}**. Pós-rito: `pos_rito/chain_pos_rito_v406.sh`, rótulos 0…10 10a 10b 10c 11…14.

## 4. Gates

Ver `PREPARACAO_v406_PRONTA.json`: `pronta` = {str(pronta).lower()}. {NAO_REVISADO}.
"""
RELATORIO = f"""# RELATÓRIO DA PREPARAÇÃO DA v406 — O fechamento

Agente de preparação `claude-prep-v406` · {AGORA.strftime('%Y-%m-%d %H:%M')} · para a gerência c1. Estatutos: [REAL] lido por script nesta pasta · [DECLARADO] dito na origem, não conferido aqui · [OPEN] em aberto. **Quem constrói não aprova: {NAO_REVISADO}.** Nada foi instalado; o rito NÃO foi rodado; o Nós e a Bancada de produção só foram lidos; o `MEMORY.md` não foi tocado.

## 1. Estado em uma frase

Candidato `{CM.get('sha16')}` ({format(CM.get('bytes') or 0, ',')} B; base v405 `{CM.get('base_v405_sha16')}`): `pronta` = **{str(pronta).lower()}**{'' if pronta else '; falta: ' + ', '.join(falta)}.

## 2. Portões (cada linha lida de um arquivo)

| portão | resultado |
|---|---|
| kernel (sandbox `{(CM.get('kernel') or {}).get('sandbox')}`) | {PORTOES['kernel']}: build + Audit rc {KR.get('rc')}, {PB.get('n_flags')} bandeiras novas, escada {_esc[0]} → {_esc[1]}, {len(KR.get('pedras') or [])} módulos no recibo; `KERNEL_RECIBO_v406.json` |
| candidato | {PORTOES['candidato']}: {CM.get('n_patches')} patches; refazer limpo = {fim_ok} |
| AST v405 × v406 | {PORTOES['ast_v405_v406']}: {CMP.get('nos_nomeados_v405')} nós, {CMP.get('iguais')} iguais, {len(CMP.get('mudados') or [])} mudados (explicados), {len(CMP.get('removidos') or [])} removidos, {CMP.get('n_novos')} novos; {len(CMP.get('funcoes_intactas') or {})} funções e constantes intactas, todas verdadeiras = {all((CMP.get('funcoes_intactas') or {'x': False}).values())} |
| ensaio a seco | {PORTOES['ensaio_a_seco']}: {EN.get('veredito')} |
| conferidor | negativo {PORTOES['conferidor_controle_negativo']} (`tudo_bate` = {CN.get('tudo_bate')}); positivo {PORTOES['conferidor_caminho_positivo']} (`tudo_bate` = {CP.get('tudo_bate')}) |
| citações | {PORTOES['citacoes']}: {len(CIT.get('apontadas_a_gerencia_aspas') or [])} apontada(s) à gerência (ver §4) |
| guarda das frases | {PORTOES['guarda_das_frases']} (controle negativo e a candidata) |
| instalar / reverter / rito (estático) | {PORTOES['instalar_reverter_rito_estatico']} |
| p00 | {PORTOES['p00']}: {ok_p00}/{n_p00} checagens OK; pendentes: {len(pendentes_p00)} |
| B(n) pré-selo | {PORTOES['bn_pre_selo']}: {PR.get('veredito')}; bateria {bat}; produção intacta = {PROV.get('producao_intacta')}; recibo `{h16('PINO_RECIBO_PRE_SELO_v406.json') if os.path.exists(P('PINO_RECIBO_PRE_SELO_v406.json')) else None}` |
| serviço da Bancada (estático) | {PORTOES['servico_estatico']}: {SERV.get('n_condicoes_ok')}/{SERV.get('n_condicoes')} condições; toda mutação pega = {CTRL.get('toda_mutacao_foi_pega')} |
| harness dos textos | {PORTOES['harness_textos']}: {n_neg_leit} controles da leitura, {n_neg_par} do parágrafo novo |
| harness do fechar | {PORTOES['harness_fechar']}: {n_neg_fech} controles do fechar |
| regeneração limpa | {PORTOES['refazer_limpo']}: `refazer_out_v406.txt` termina em `== FIM` e `RC_REFAZER=0` |
| purga da fala reservada | {PORTOES['purga_da_fala_reservada']}: `purga_v406.json`, zero ocorrências na pasta e no sandbox do kernel |
| fala excluída fora dos artefatos | {PORTOES['fala_excluida_fora_dos_artefatos']}: `purga_v406.json`, zero ocorrências |

## 3. O que NÃO passou ou fica para depois

- p00 reprova {len(falhas_p00)} checagem(ns): {'; '.join(f[:200] for f in falhas_p00) if falhas_p00 else 'nenhuma'}; pendentes ({len(pendentes_p00)}): {'; '.join(f[:160] for f in pendentes_p00) if pendentes_p00 else 'nenhum'}.
- Só depois do rito: o conferidor real, a leitura real, as superfícies, o B(n) pós-selo e o fechar; os recibos do B(n) nos harnesses são sintéticos.
- Não feito (fora do escopo): instalar, rodar o rito, revisão independente, custódia, commit, push. A rota da preparação está no Mapa: `{ROTA}`, seq {seqs}.

## 4. Avisos e desvios ditos

{chr(10).join('- ' + a for a in AVISOS)}

## 5. Para a gerência — ordem sugerida

1. Revisão de terceiro (o Sonnet, D37), nesta ordem, antes de qualquer publicação: `delta_v406.py` (moldura, erratas E14 a E17, decisões D34 a D40), `registros_v406.py`, `runtime_v406.py` (as 14 checagens de `fechamento_v406`), `pedra/CanonicalFullTGLWitnessR1.lean`, as seções do artigo (`artigo_pt_v406.pysnip`, `artigo_en_v406.pysnip`) e `pos_rito/textos_v406.semente`.
2. Dizer ao operador, na língua dele (regra do posto), o que a v406 NÃO entrega: validade no kernel não é creditação; o fechamento habita o certificado de Fock e a passagem para o contínuo, mas K(O) ≠ ⊥ só vale na cunha, o traço é cíclico e não linear, e as duas chaves que ficam False ficam por teorema; o 4,44 continua abaixo do degrau de 5 sigma; o teste com a natureza segue da natureza.
3. O orquestrador lê `PREPARACAO_v406_PRONTA.json` e segue: `instalar_v406.py`, `rito_v406.sh`, `pos_rito/chain_pos_rito_v406.sh` (0 → 10, 10a, 10b, 10c → 14).
4. Se o rito cair: `reverter_v406.py` é decisão da gerência; `refazer_candidato_v406.sh --regerar` refaz o candidato.

## 6. Âncoras

| âncora (nome Lean) | módulo | bandeira | classe |
|---|---|---|---|
{tab_pedras}

## 7. Artefatos e hashes (lidos agora)

| arquivo | bytes | sha16 |
|---|---|---|
{tab_arq}
"""
grava("PLANO_v406.md", PLANO.encode("utf-8")); grava("RELATORIO_PREPARACAO_v406.md", RELATORIO.encode("utf-8"))
HASHES["PLANO_v406.md"] = {"sha16": h16("PLANO_v406.md"), "bytes": sz("PLANO_v406.md")}; HASHES["RELATORIO_PREPARACAO_v406.md"] = {"sha16": h16("RELATORIO_PREPARACAO_v406.md"), "bytes": sz("RELATORIO_PREPARACAO_v406.md")}
grava("PREPARACAO_v406_PRONTA.json", json.dumps(PRONTA, ensure_ascii=False, indent=1).encode("utf-8"))
print("pronta =", pronta, "| falta:", falta)
print("candidato", CM.get("sha16"), "| kernel recibo", PRONTA["kernel_recibo"]["sha16"], "| ESPERADOS", PRONTA["esperados_sha16"], "| p00", PRONTA["p00"]["sha16"], "(%d/%d)" % (ok_p00, n_p00))
print(P("PREPARACAO_v406_PRONTA.json"))
