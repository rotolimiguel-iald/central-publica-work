# -*- coding: utf-8 -*-
"""Gera, a partir dos artefatos ja' calculados, as entregas: PEDIDO_DE_CONGELAMENTO.json, registro_mapa_fase9_v2_c1.json e RESULTADO.md.
Rodar por ultimo:  python -P -E -X utf8 ferramentas/build_entregas.py   (todo numero e' LIDO dos JSON; todo hash, calculado dos arquivos)."""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(ROOT, "runner"))
import f9v2_background as BG  # noqa: E402
import f9v2_freeze as FRZ  # noqa: E402
import f9v2_verdict as VER  # noqa: E402


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rd(rel):
    return open(os.path.join(ROOT, *rel.split("/")), "rb").read()


def js(rel):
    return json.loads(rd(rel).decode("utf-8"))


def f4(x):
    return "%.4g" % x


def pct(x):
    return "%.1f%%" % (100 * x)


def main():
    spec_w = js("spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json")
    spec = spec_w["spec"]
    cal = js("calibracao/CALIBRACAO_CAUDA_RECIBO.json")
    mc = js("calibracao/MC_VALIDACAO.json")
    pw = js("poder/PODER_ESPERADO_V2C1.json")
    tests = js("testes/RESULTADO_TESTES.json")
    qual = js("testes/QUALIFICACAO_FORNECEDOR_REAL.json")
    reg = js("spec/REGISTRO_DH_V2_C1.json")
    pins = FRZ.build_pins(ROOT, "REAL", bancada_pins=BG.bancada_pins())

    # ------------------------------------------------------------------ PEDIDO DE CONGELAMENTO
    mode = spec["calibracao_de_cauda"]["modo"]
    classes = pw["probabilidade_da_classe_do_veredito"]
    disp = pw["taxa_de_INCONCLUSIVE_pela_dispersao_sob_a_nula"]
    pedido = {
        "schema": "F9V2C1_PEDIDO_DE_CONGELAMENTO_V1", "para": "gerencia c1", "de": "subagente de preparacao (c1, 23/10/2026)",
        "estado": "PREPARADO_NAO_CONGELADO; nada aberto; nenhum centro observado entrou em calculo; nenhum recibo emitido",
        "o_recibo_pinara": pins,
        "autoria_dos_pinos": "calculados por script a partir dos arquivos desta pasta no instante da geracao deste pedido; o recibo recalcula tudo ao ser emitido",
        "conferir_antes_de_assinar": [
            {"id": "C01", "item": "spec: o texto do alcance, X13, D-H e D-J reflete as decisoes do operador de 23/10", "como": "ler spec/DIFF_R52_PARA_V2C1.md (cada mudanca atribuida) e spec.alcance", "criterio": "nenhuma mudanca sem atribuicao; logica e limiares da funcao identicos aos da R5.2"},
            {"id": "C02", "item": "funcao de veredito = texto da R5.2 com 3 trocas literais", "como": "ferramentas/build_funcao.py reproduz o arquivo; testes A4 (4000 entradas aleatorias) comparam com a R5.2", "criterio": "tokens iguais salvo a base"},
            {"id": "C03", "item": "registro D-H: 8 fontes por sha256, regra de extracao testada contra os bytes, L1b e L6 baixados", "como": "sha256sum de cada arquivo em fontes/; ferramentas/build_registro_dh.py; teste F1", "criterio": "extraido = declarado a 1e-9 nos 8 leitores"},
            {"id": "C04", "item": "fundo BG1 real reproduz o pino", "como": "testes/QUALIFICACAO_FORNECEDOR_REAL.json", "criterio": "|H0-68,531|<0,01 e |sigma-0,301|<0,005"},
            {"id": "C05", "item": "o runner recusa na ausencia de qualquer trava", "como": "testes/run_tests.py (%d casos); relato em testes/TESTES.log" % tests["n"], "criterio": "todos os controles negativos recusam com o codigo esperado e sem deixar saida"},
            {"id": "C06", "item": "ordem do modo observado: poder (so sigma) antes dos centros; centros so da fonte; nenhum ALVOS a mao", "como": "testes D1, D4, E08, E12", "criterio": "log ordem_de_acesso; cofre lacrado"},
            {"id": "C07", "item": "calibracao de cauda: modo escolhido, p calibrado, limiares brutos equivalentes", "como": "calibracao/CALIBRACAO_CAUDA_RECIBO.json e MC_VALIDACAO.json", "criterio": "MC concorda com o analitico; reducao exata verificada contra o pipeline completo"},
            {"id": "C08", "item": "auditoria c1 do runner (a R5.2 foi auditada ate X13/D-H; o runner do modo observado, nao)", "como": "auditoria independente dos modulos runner/*.py", "criterio": "sem achado ALTO/MEDIO aberto"},
            {"id": "C09", "item": "bytes da Bancada (fornecedor do fundo) inalterados desde a qualificacao", "como": "pinos 'bancada' do recibo x BG.bancada_pins()", "criterio": "iguais"},
        ],
        "decisoes_da_gerencia_reversiveis_antes_do_congelamento": [
            {"id": "G01", "assunto": "modo da calibracao de cauda", "padrao": mode,
             "alternativas": {"sup_caixa": "p com a pior covariancia da caixa (conservador)", "proprio": "p com a covariancia do ponto de analise", "bruto": "escore bruto (equivale a R5.2)"},
             "efeito_medido": {"limiar_bruto_equivalente_a_5sigma_z_delta": {m: cal["limiares_equivalentes_todos_os_modos"][m]["z_delta_bruto_para_5sigma_calibrado"] for m in ("proprio", "sup_caixa")},
                               "P(FALSIFIED | LCDM verdadeira) por modo e covariancia verdadeira": {k: {m: classes[k][m].get("FALSIFIED", 0.0) for m in ("bruto", "proprio", "sup_caixa")} for k in classes if k.startswith("LCDM")},
                               "P(TENSION | LCDM verdadeira)": {k: {m: classes[k][m].get("TENSION", 0.0) for m in ("bruto", "proprio", "sup_caixa")} for k in classes if k.startswith("LCDM")}},
             "como_mudar": "editar calibracao_de_cauda.modo em ferramentas/build_spec.py, refazer build_spec.py, calibracao/rodar_calibracao.py e os testes"},
            {"id": "G02", "assunto": "regra de dispersao herdada do V1 (chi2/(n-1) > 2 OU p < 0,01 em qualquer extremo => INCONCLUSIVE)", "padrao": "mantida como na R5.2 (nao alterei limiar)",
             "efeito_medido": {"taxa de INCONCLUSIVE pela dispersao quando tudo e' consistente (nula, 5 leitores)": disp},
             "nota": "so p < 0,01 daria ~2% em vez de ~9-20%; mudar e' decisao de limiar ANTES de congelar, nao depois"},
            {"id": "G03", "assunto": "BG2/BG3 (fundos diagnosticos) nao tem fonte pinada", "padrao": "ficam [KNOWN]/[DECLARADO], fora do veredito"},
            {"id": "G04", "assunto": "versao do L6", "padrao": "v1/v2 (76,6 +13,0/-9,5; declarado desde o V1); a v3 publicada diz 75,4 +12,8/-9,1 e fica ao lado, nao admitida", "nota": "L6 esta fora do composto; nao muda o veredito"},
            {"id": "G05", "assunto": "acrescimos da c1 nao pedidos pelo operador", "padrao": "E2 tambem confere sigma (|sigma-0,301|<0,005); beta_livre_no_limite vale se QUALQUER extremo estiver na borda; ln B decisorio = n 100 (conferencia n 200)"},
        ],
        "o_que_o_recibo_atesta_e_o_que_nao": {
            "atesta": "que os bytes de spec, funcao, registro D-H, fontes, runner, calibracao e Bancada sao os que estao pinados e que a gerencia auditou o runner",
            "nao_atesta": ["que o teste vai discriminar ou falsificar (isso e' do dado)", "autenticidade criptografica do emitente (a trava e' o ato da gerencia + conferencia dos bytes)", "que d72 (a testemunha conjunta) esteja qualificada"],
        },
        "comandos": {
            "ensaio_do_recibo_nada_e_gravado": "python -P -E -X utf8 ferramentas/emitir_recibo_de_congelamento.py --root . --emitido-por \"...\" --auditoria-ref \"...\" --confirmo-auditoria",
            "emitir_recibo_de_congelamento": "... --escrever",
            "emitir_recibo_de_abertura_ato_proprio": "python -P -E -X utf8 ferramentas/emitir_recibo_de_abertura.py --root . --quem \"...\" --texto \"...\" --escrever",
            "executar": "python -P -E -X utf8 runner/f9v2_runner.py --package-root . --mode observed",
            "preflight_sem_abrir": "python -P -E -X utf8 runner/f9v2_runner.py --package-root . --mode preflight",
        },
        "nao_executado_nesta_preparacao": ["emissao do recibo de congelamento", "emissao do recibo de abertura", "o runner em modo observado", "qualquer calculo do composto observado da V2", "escrita no tunel, no Nos, no um.py, no mapa, no quadro, na memoria, no site, no git"],
    }
    pb = json.dumps(pedido, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    open(os.path.join(ROOT, "PEDIDO_DE_CONGELAMENTO.json"), "wb").write(pb)

    # ------------------------------------------------------------------ REGISTRO DO MAPA
    arts = [os.path.join(ROOT, p) for p in (
        "RESULTADO.md", "spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json", "spec/veredito_fase9_v2_c1.py", "spec/REGISTRO_DH_V2_C1.json", "spec/DIFF_R52_PARA_V2C1.md",
        "runner/f9v2_runner.py", "runner/f9v2_stats.py", "runner/f9v2_calibration.py", "runner/f9v2_freeze.py", "runner/f9v2_background.py",
        "calibracao/CALIBRACAO_CAUDA_RECIBO.json", "poder/PODER_ESPERADO_V2C1.json", "testes/RESULTADO_TESTES.json", "PEDIDO_DE_CONGELAMENTO.json")]
    mapa = {
        "tipo": "ROTA", "rota_id": "d1.fase9.v2_c1_a_unica_palavra_23out",
        "dominio": "D1_FUNDO_COSMOLOGICO",
        "titulo": "Fase 9 V2-c1 «O Teste da Unica Palavra»: V2 R5.2 com as decisoes do operador de 23/10, runner do modo observado (E1-E5, S5, calibracao de cauda) e trava de congelamento — preparada, nao aberta",
        "pergunta": "A razao de Hubble K = E(z*)^(2 beta_TGL/3), voz unica de beta_TGL na expansao, resiste ou cai a 5 sigma calibrado contra o dado publico ja' existente?",
        "dados": ["fundo BG1: Planck 2018 comprimido (Chen+2019) + DESI DR2 BAO, recalculado na Bancada (so fundo; nenhum H0 local)", "8 leitores locais por sha256 (SH0ES R22, SH0ES R25, CCHP v3, SBF v2, masers Pesce Tab.2, TDCOSMO v4, sirenes LVK O4a v1) — NAO combinados nesta preparacao"],
        "metodo": "V2 R5.2-E1 + OP-a..d + C1-E1..E5/S5/CAL/TRAVA; funcao de veredito = texto R5.2 com 3 trocas literais; calibracao de cauda analitica (reducao exata) + simulacao sob as nulas; testes so sinteticos (45+ casos, controles negativos)",
        "resultado": "PREPARADA, NAO ABERTA. D esperado so-sigma BG1: min %.3f / max %.3f. Limiar bruto equivalente a 5 sigma calibrado: z_delta %.2f (sup_caixa) / %.2f (proprio); z_disc %.2f. Testes %d/%d." % (
            pw["D_so_sigma"]["P_primaria"]["maximum"]["D_BG1_formula_pinada"], pw["D_so_sigma"]["P_primaria"]["minimum"]["D_BG1_formula_pinada"],
            cal["limiares_equivalentes_todos_os_modos"]["sup_caixa"]["z_delta_bruto_para_5sigma_calibrado"], cal["limiares_equivalentes_todos_os_modos"]["proprio"]["z_delta_bruto_para_5sigma_calibrado"],
            cal["limiares_equivalentes_todos_os_modos"]["sup_caixa"]["z_disc_bruto_para_5sigma_calibrado"], tests["ok"], tests["n"]),
        "veredito": "PREPARADO_NAO_CONGELADO__NENHUM_VEREDITO_EMITIDO",
        "estatuto": "DERIVED", "status": "EM_CURSO", "olhou_dados": False,
        "defeito": "regra de dispersao herdada (chi2/(n-1)>2 OU p<0,01) da ~9-20%% de INCONCLUSIVE mesmo com tudo consistente; calibracao sup_caixa reduz a letalidade; BG2/BG3 sem fonte pinada; runner do modo observado ainda sem auditoria c1",
        "nao_refazer": "o D-H (8 fontes pinadas, 2 baixadas), a funcao (logica R5.2 intocada), o fundo BG1 real (reproduz 68,531), a reducao exata do z_delta e a calibracao de cauda, a trava e seus controles",
        "proximo_passo": "auditoria c1 do runner; decisao G01/G02 do PEDIDO; emitir RECIBO_DE_CONGELAMENTO; ato proprio de abertura; abrir UMA vez e preservar o resultado mesmo abaixo de 5 sigma",
        "onde": "C:\\IALD\\Central de Patentes\\work\\fase9_v2_c1_23out",
        "artefatos": arts,
        "refs": ["d1.fase9.auditoria_suficiencia_20261019", "d1.fase9.f3_1_reauditoria_v2r2_c1_08out", "d1.fase9.razao_de_hubble.lentes_05out"],
        "nota": ("Leitura do dado nesta preparacao: o fundo BG1 foi recalculado na Bancada (Planck comprimido + DESI DR2) para qualificar o fornecedor (E1/E2) e as 8 regras de extracao foram testadas contra os "
                 "bytes publicos (igual ao declarado, 1e-9); NENHUM composto local, NENHUMA estatistica sobre os centros publicados e NENHUM veredito foram calculados; os testes usam centros FABRICADOS. "
                 "L1b e L6 baixados em 23/10/2026 (arXiv 2509.01667; arXiv 2509.04348 v1/v2/v3). NOT_FALSIFIED nunca e' CONFIRMED."),
    }
    mb = json.dumps(mapa, ensure_ascii=False, indent=1).encode("utf-8")
    open(os.path.join(ROOT, "registro_mapa_fase9_v2_c1.json"), "wb").write(mb)

    # ------------------------------------------------------------------ RESULTADO.md
    th = cal["limiares_equivalentes_todos_os_modos"]
    an = cal["analitico"]
    P = pw["D_so_sigma"]["P_primaria"]
    N = pw["D_so_sigma"]["N_sem_cefeidas"]
    L = []
    A = L.append
    A("FASE 9 V2 — O TESTE DA ÚNICA PALAVRA — preparada, não aberta")
    A("")
    A("**Natureza:** preparação (gerência c1, 23/10/2026). Nada foi aberto: nenhum composto observado da V2, nenhum veredito, nenhum recibo de congelamento ou de abertura emitido, nada escrito no túnel, no Nós, no um.py, no mapa, no quadro, na memória, no site ou no git. Pasta: `C:\\IALD\\Central de Patentes\\work\\fase9_v2_c1_23out`. Estatutos: [REAL] medido aqui · [DERIVED] · [INPUT] decisão do operador · [DECLARADO] afirmado na origem. NOT_FALSIFIED nunca é CONFIRMED; o gate não se move.")
    A("")
    A("## 0. Resposta curta")
    A("")
    A("1. A V2 R5.2-E1 (`81a970926345832a`) ganhou as quatro decisões do operador de 23/10 e virou `%s` (spec canônico `%s`); **a lógica e os limiares da função de veredito são os da R5.2** (4000 entradas aleatórias dão a mesma classe e o mesmo sufixo). Token: `%s`." % (sha(rd("spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json"))[:16], spec_w["spec_sha256"][:16], VER.TOKEN_BASE))
    A("2. L1b (Riess+2025, arXiv:2509.01667: 73,49 ± 0,93) e L6 (LVK O4a, arXiv:2509.04348 v1/v2: 76,6 +13,0/−9,5) foram **baixados e pinados**; os 8 leitores têm regra de extração testada contra os bytes (igual ao declarado a 1e-9). `n_alvos_declarados` passa de 2 para **0**.")
    A("3. Runner do modo observado em cópia (E1–E5, S5, calibração de cauda) e **trava**: recusa sem recibo de congelamento e sem recibo de abertura. **%d/%d testes sintéticos e controles negativos passam.**" % (tests["ok"], tests["n"]))
    A("4. **Fundo BG1 real** (não mock) reproduz o pino: H0 = %.5f (Δ = %.1e), σ = %.5f." % (qual["reproducao_E2"]["H0"], qual["reproducao_E2"]["dH0"], qual["reproducao_E2"]["sigma"]))
    A("5. **Poder esperado só pelas incertezas** (BG1, 5 maseres): D = %.3f (extremo de maior σ) a %.3f (menor σ); sem Cefeidas %.3f a %.3f. Reproduz os pinos da R5.2 a 1e-9." % (
        P["maximum"]["D_BG1_formula_pinada"], P["minimum"]["D_BG1_formula_pinada"], N["maximum"]["D_BG1_formula_pinada"], N["minimum"]["D_BG1_formula_pinada"]))
    lc = [v for k, v in classes.items() if k.startswith("LCDM")]
    rng_ = lambda m, c: (pct(min(v[m].get(c, 0) for v in lc)), pct(max(v[m].get(c, 0) for v in lc)))
    A("6. **O que a calibração mostrou e a gerência precisa decidir (reversível até o congelamento):** o `|z_δ| ≥ 5` bruto equivale a z calibrado **%.2f** com a pior covariância da caixa (p = %s, não 5,7e-07) e a **%.2f** com a covariância do ponto; para um 5σ calibrado o bruto tem de ser **%.2f** (caixa) ou **%.2f** (ponto). Com o modo padrão `%s`, se a ΛCDM for a verdadeira a função devolve FALSIFIED em %s a %s dos casos (TENSION em %s a %s); com o escore bruto, %s a %s. E a regra de dispersão herdada do V1 dá INCONCLUSIVE em %s a %s mesmo com tudo consistente." % (
        an["z_delta_p_cal"]["5"]["z_cal_sup_caixa"], f4(an["z_delta_p_cal"]["5"]["sup_caixa"]), an["z_delta_p_cal"]["5"]["z_cal_proprio"],
        th["sup_caixa"]["z_delta_bruto_para_5sigma_calibrado"], th["proprio"]["z_delta_bruto_para_5sigma_calibrado"], mode,
        *rng_(mode, "FALSIFIED"), *rng_(mode, "TENSION"), *rng_("bruto", "FALSIFIED"),
        pct(min(v["qualquer_regra"] for v in disp.values())), pct(max(v["qualquer_regra"] for v in disp.values()))))
    A("")
    A("## 1. Entregas (sha256[:16], lidos dos arquivos)")
    A("")
    A("| arquivo | sha256[:16] | papel |")
    A("|---|---|---|")
    ents = [("spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json", "a spec V2-c1 (alcance, X13, D-H, D-J, S5, calibração, trava)"), ("spec/veredito_fase9_v2_c1.py", "a função de veredito pinada"),
            ("spec/REGISTRO_DH_V2_C1.json", "registro D-H: 8 fontes por sha256 + regras de extração"), ("spec/DIFF_R52_PARA_V2C1.md", "diff contra a R5.2, cada mudança atribuída"),
            ("spec/DIFF_R52_PARA_V2C1.patch", "o mesmo, linha a linha"), ("runner/f9v2_runner.py", "runner do modo observado"), ("runner/f9v2_stats.py", "estatística do executor (X13, S5, E3)"),
            ("runner/f9v2_calibration.py", "calibração de cauda"), ("runner/f9v2_freeze.py", "a trava (recibos)"), ("runner/f9v2_background.py", "E1/E2: fornecedor real do fundo"),
            ("runner/f9v2_extract.py", "extração dos centros das fontes (E5)"), ("runner/f9v2_text.py", "leitura de fonte como dado não confiável"), ("runner/f9v2_verdict.py", "carrega a função pinada em espaço restrito"),
            ("calibracao/CALIBRACAO_CAUDA_RECIBO.json", "recibo da calibração"), ("calibracao/MC_VALIDACAO.json", "MC × analítico"), ("poder/PODER_ESPERADO_V2C1.json", "poder esperado só por incertezas"),
            ("testes/RESULTADO_TESTES.json", "resultado dos testes"), ("testes/QUALIFICACAO_FORNECEDOR_REAL.json", "fundo BG1 real (sem H0 local)"), ("PEDIDO_DE_CONGELAMENTO.json", "o que a gerência confere e assina"),
            ("registro_mapa_fase9_v2_c1.json", "registro para o mapa (olhou_dados=false)")]
    for rel, papel in ents:
        p = os.path.join(ROOT, *rel.split("/"))
        if os.path.exists(p):
            A("| `%s` | `%s` | %s |" % (rel, sha(open(p, "rb").read())[:16], papel))
    A("")
    A("## 2. Fontes baixadas e pinadas (D-H)")
    A("")
    A("| leitor | H0 ± σ (extraído da fonte) | arquivo | sha256[:16] |")
    A("|---|---|---|---|")
    for rid, r in reg["leitores"].items():
        A("| %s | %.4g ± %.4g | `%s` | `%s` |" % (rid, r["extraido_no_build"]["H0"], r["extraido_no_build"]["sigma"], r["file"], r["sha256"][:16]))
    A("")
    A("Baixados em 23/10/2026 por `curl` (download autorizado à gerência), lidos como dado não confiável (`python -P -E`, caminho como argumento): L1b `abs_2509.01667.html`; L6 `abs_2509.04348v1.html` (admitido), v2, v3 e o PDF v3 (ao lado, **não admitidos**: a v3 publicada diz 75,4 +12,8/−9,1; L6 está fora do composto, a troca não muda o veredito). Os outros seis arquivos são cópias byte a byte do ORDEM_018 (hashes idênticos aos do levantamento). Limites: SBF §III.3 e TDCOSMO §VIII.2.1 seguem só como resumo; BG2/BG3 seguem [KNOWN]/[DECLARADO].")
    A("")
    A("## 3. O que mudou da R5.2 (resumo; `spec/DIFF_R52_PARA_V2C1.md` tem cada linha)")
    A("")
    A("- **OP-a ALCANCE:** `alcance` novo — FALSIFIED_AT_5SIGMA = β_TGL refutado na natureza, a lei K é a voz única, sem saída posterior; a validade do kernel não está em jogo; o pré-registro é o devido processo. `nao_decide` reescrito.")
    A("- **OP-b X13 SIM:** `estatisticas_do_executor` descreve o que o executor faz (fundo marginalizado; z_δ pelo perfil com log-det; ln B com n ≥ 100; ln B(TGL/β-livre) = 1,97).")
    A("- **OP-c D-H:** registro pinado; L1b e L6 entram com os papéis tipados que a V2 já dava; `n_alvos_declarados` 2 → 0.")
    A("- **OP-d D-J:** token `%s` + a ordem do sufixo (INCONCLUSIVE_SYSTEMATICS · FALSIFIED_AT_5SIGMA · TENSION_3_TO_5_SIGMA · NOT_FALSIFIED_UNDERPOWERED · DISCRIMINATES · NOT_FALSIFIED_POWERED)." % VER.TOKEN_BASE)
    A("- **C1 (ordem da gerência, reversível):** E1–E5, S5, calibração de cauda, trava. Acréscimos que o operador não pediu e a gerência pode recusar: σ do fundo também conferido (|σ−0,301|<0,005); `beta_livre_no_limite` vale se QUALQUER extremo estiver na borda; ln B decisório n = 100 com conferência n = 200.")
    A("")
    A("## 4. O runner — o que ele faz e o que recusa")
    A("")
    A("Ordem do modo observado: (0) recibos e pinos, bytes lidos **uma vez**; (1) β = α·√e em runtime com o α do um.py instalado, K recalculado = K congelado (1e-12); (2) **E1/E2** fundo BG1 real, |H0−68,531|<0,01 — diverge, interrompe, nunca calibra; (3) **PODER_FASE9_ANTES_DE_ABRIR.json** com só σ, gravado e hasheado, com os centros num cofre lacrado (acesso antecipado = KeyError/recusa); (4) **E4/E5** centros extraídos das fontes pelo registro D-H pinado; `ALVOS_FASE9_LIDOS.json` em qualquer lugar do pacote = recusa; (5) estatística do executor, **E3** (|ln Z₁₀₀ − ln Z₂₀₀| > 1e-6 ⇒ recusa sem veredito), **S5**, calibração; (6) função pinada executada do texto; resultado inteiro gravado, também abaixo de 5σ.")
    A("")
    A("**S5 fechada por propagação:** a variância da previsão muda %.1f%% e a média, por Ω_m do próprio fundo (0,3011 contra 0,3023 pré-registrado), %.4f km/s/Mpc — desprezíveis frente a σ_comb 0,80–0,95." % (
        100 * (spec["S5_propagacao"]["efeito_medido_no_fundo_real_de_qualificacao"]["razao"] - 1), spec["S5_propagacao"]["efeito_medido_no_fundo_real_de_qualificacao"]["delta_K_vezes_H0_km_s_Mpc"]))
    A("")
    A("**Sistemáticas do levantamento:** S5 propagada (acima); S1 (a covariância cruzada é uma caixa de tetos) entra na calibração como `sup_caixa`; velocidades peculiares e vazio local, covariâncias SN/Pantheon (L1–L2, L1–L5) e a origem do fator 0,031 do SBF seguem [OPEN]/declarados na spec — não os fechei.")
    A("")
    A("## 5. Calibração de cauda")
    A("")
    A("Redução exata (fundo marginalizado, f = 1): z_δ é função determinística de u = m − K·μ (m = média GLS); z_disc, de x = m − μ, em forma fechada. Verificado contra o pipeline completo: máx |Δz_δ| = %.1e, máx |Δz_disc| = %.1e (400 sorteios). O MC sob as nulas concorda com o analítico (`calibracao/MC_VALIDACAO.json`)." % (
        cal["reducao_exata_pipeline_completo_x_mapa"]["max_abs_diff_z_delta"], cal["reducao_exata_pipeline_completo_x_mapa"]["max_abs_diff_z_disc"]))
    A("")
    A("| z_δ bruto | p gaussiano (bilateral) | p_cal (ponto) | z_cal (ponto) | p_cal (caixa) | z_cal (caixa) |")
    A("|---|---|---|---|---|---|")
    for t in ("2", "3", "4", "5", "6"):
        r = an["z_delta_p_cal"][t]
        A("| %s | %s | %s | %.3f | %s | %.3f |" % (t, f4(r["gauss_bilateral"]), f4(r["proprio"]), r["z_cal_proprio"], f4(r["sup_caixa"]), r["z_cal_sup_caixa"]))
    A("")
    A("| z_disc bruto | p gaussiano (unilateral) | p_cal (ponto) | z_cal (ponto) | p_cal (caixa) | z_cal (caixa) |")
    A("|---|---|---|---|---|---|")
    for t in ("2", "3", "4", "5", "6"):
        r = an["z_disc_p_cal"][t]
        A("| %s | %s | %s | %.3f | %s | %.3f |" % (t, f4(r["gauss_unilateral"]), f4(r["proprio"]), r["z_cal_proprio"], f4(r["sup_caixa"]), r["z_cal_sup_caixa"]))
    A("")
    A("(z_disc é unilateral e assimétrico: sob ΛCDM, z_disc ≥ 2 é raríssimo porque o p é calculado sobre a região de Δχ² ≥ z², onde a previsão TGL, de variância maior, pode vencer só nas caudas; só o limiar de 5 decide.)")
    A("")
    A("Limiares brutos equivalentes: 3σ → z_δ %.2f (ponto) / %.2f (caixa), z_disc %.2f / %.2f; 5σ → z_δ %.2f / %.2f, z_disc %.2f / %.2f. O pior caso da caixa é λ_N = λ_T = 1 (τ_f %.3f contra %.3f do ponto). O z_disc já é quase calibrado a 5σ; o z_δ não, porque a covariância entre leitores é uma caixa, não uma medida." % (
        th["proprio"]["z_delta_bruto_para_3sigma_calibrado"], th["sup_caixa"]["z_delta_bruto_para_3sigma_calibrado"], th["proprio"]["z_disc_bruto_para_3sigma_calibrado"], th["sup_caixa"]["z_disc_bruto_para_3sigma_calibrado"],
        th["proprio"]["z_delta_bruto_para_5sigma_calibrado"], th["sup_caixa"]["z_delta_bruto_para_5sigma_calibrado"], th["proprio"]["z_disc_bruto_para_5sigma_calibrado"], th["sup_caixa"]["z_disc_bruto_para_5sigma_calibrado"],
        cal["taus"]["tau_f_sup"], cal["taus"]["tau_f_proprio"]))
    A("")
    A("## 6. Poder esperado (pipeline completo, função pinada, %d sorteios por cenário; centros sintéticos, nenhum observado)" % pw["n_por_cenario"])
    A("")
    for nul in ("TGL", "LCDM"):
        A("**%s verdadeira:**" % ("β_TGL (TGL)" if nul == "TGL" else "ΛCDM"))
        A("")
        A("| covariância verdadeira | modo | " + " | ".join(["FALSIFIED", "TENSION", "INCONCLUSIVE", "UNDERPOWERED", "DISCRIMINATES", "POWERED_NOT_DISCRIMINATED"]) + " |")
        A("|---|---|" + "---|" * 6)
        for k, v in classes.items():
            if not k.startswith(nul):
                continue
            for m in ("bruto", "proprio", "sup_caixa"):
                A("| %s | %s | " % (k.split("C_verdadeira=")[1], m) + " | ".join(pct(v[m].get(c, 0.0)) for c in ["FALSIFIED", "TENSION", "INCONCLUSIVE", "UNDERPOWERED", "DISCRIMINATES", "POWERED_NOT_DISCRIMINATED"]) + " |")
        A("")
    A("Taxa de INCONCLUSIVE pela dispersão quando tudo é consistente (sob a nula): " + "; ".join("%s: χ²/(n−1)>2 em algum extremo e/ou p<0,01 → %s (só p<0,01 → %s)" % (k.split("__")[0] + " / " + k.split("C_verdadeira=")[1], pct(v["qualquer_regra"]), pct(v["so_p_lt_001"])) for k, v in disp.items() if k.startswith("TGL")) + ".")
    A("")
    A("## 7. Testes e controles negativos (só sintéticos)")
    A("")
    A("`testes/run_tests.py`: **%d/%d**. Controles: congelamento ausente · abertura ausente · spec adulterada · **fonte adulterada** · .py a mais no runner · módulo do runner alterado · **fundo divergente** (H0 e σ) · **ALVOS manual** · pacote REAL com fornecedor não real · Bancada adulterada · α diferente · extração ≠ declarado · autohash corrompido · abertura de outro congelamento · token diferente · função diferente · tolerância de quadratura diferente · recibo de calibração diferente · poder ≠ pino · **quadratura instável** (estatística e runner) · CLI sobre este pacote (recusa sem ler nada) · NaN. Ponta a ponta: pacote fabricado (TGL-like, ΛCDM-like, borda do prior), ordem de acesso, cofre, 7 diagnósticos, **E2E com o fundo REAL e locais fabricados**." % (tests["ok"], tests["n"]))
    A("")
    A("## 8. O que a gerência decide e confere (detalhe em `PEDIDO_DE_CONGELAMENTO.json`)")
    A("")
    A("- **G01** modo da calibração (padrão `%s`; alternativas `proprio`, `bruto`) — muda a letalidade do teste (§0.6, §6). **G02** regra de dispersão (mantida como na R5.2; ~9–20%% de INCONCLUSIVE indevido). G03 BG2/BG3 sem fonte pinada. G04 versão do L6. G05 acréscimos da c1." % mode)
    A("- Antes do recibo: **auditoria c1 do runner** (a R5.2 foi auditada até X13/D-H; o runner do modo observado, não). Depois: recibo de congelamento (gerência) → recibo de abertura (ato próprio) → abrir UMA vez → relatar escore, p calibrado, ln B, diagnósticos e limitações separados → **preservar o resultado mesmo abaixo de 5σ**.")
    A("- d72 (testemunha conjunta ROOT90da) é outra testemunha; não soma, não empresta poder.")
    A("")
    A("## 9. Mapa consultado e o que examinei")
    A("")
    A("`rotas.py consultar` com \"fase9\" (23 rotas), \"razao de Hubble\" (1), \"F3.1\" (9) e \"F3.2\" (12): `d1.fase9.auditoria_suficiencia_20261019` (separação esperada condicional, V2 observada em aberto), `d1.fase9.f3_1_reauditoria_v2r2_c1_08out` (APROVA_COM_RESSALVAS), `d1.fase9.f3_1_semantica_v1x_leitores`, `d1.fase9.f3_2_r1_hash_gate` (harness sintético), `d1.fase9.razao_de_hubble.lentes_05out`. Nada do que o mapa manda não refazer foi refeito: gate/harness/pinos F3.2 foram lidos, não repetidos; a estatística do executor é a do F3.2 estendida (S5, calibração) e a reprodução do fundo é a do R2 do V1. Registro proposto: `registro_mapa_fase9_v2_c1.json` (`olhou_dados=false`).")
    A("")
    A("## 10. O que NÃO foi feito (e por quê)")
    A("")
    A("- Não calculei o composto observado da V2 nem abri o veredito; os centros publicados só foram usados para **verificar** as regras de extração contra o declarado (igualdade a 1e-9), e o fundo BG1 (Planck+DESI) foi recalculado para qualificar o fornecedor. Os testes usam centros fabricados.")
    A("- Não emiti recibo de congelamento nem de abertura; não rodei `emitir_recibo_*`; não toquei o serviço da Bancada (porta 18777): o fornecedor roda em processo, como o runner V1; o código do pacote não faz chamada de rede (teste F3).")
    A("- Não mudei nenhum limiar da função; os acréscimos da c1 estão listados (G05) e são reversíveis.")
    A("- Pendentes: auditoria c1 do runner; decisões G01/G02; pinar fontes de BG2/BG3 se a gerência quiser fundos diagnósticos [REAL]; texto integral do SBF §III.3 e do TDCOSMO §VIII.2.1.")
    A("")
    A("## 11. Como refazer (ordem; tudo com `python -P -E -X utf8`, a partir de qualquer cwd)")
    A("")
    A("1. `ferramentas/build_funcao.py` → `ferramentas/build_registro_dh.py` → `ferramentas/build_spec.py` (spec, função, registro, diff).")
    A("2. `testes/qualifica_fornecedor_real.py` (fundo BG1 real; só Planck+DESI) — se o fundo mudar, refazer o passo 3.")
    A("3. `calibracao/rodar_calibracao.py --n-por-cenario 100000 --workers 40` (recibo da calibração, MC, poder esperado).")
    A("4. `testes/run_tests.py` (%d casos). 5. `ferramentas/build_entregas.py` (pedido, registro do mapa, este RESULTADO)." % tests["n"])
    A("6. Só depois da auditoria c1: `ferramentas/emitir_recibo_de_congelamento.py ... --escrever`, depois `ferramentas/emitir_recibo_de_abertura.py ... --escrever`, depois `runner/f9v2_runner.py --package-root . --mode observed`.")
    A("7. `ferramentas/conferir_consistencia.py` (só leitura; sai com 1 se spec, função, registro, runner, recibo de calibração, testes e pedido divergirem).")
    open(os.path.join(ROOT, "RESULTADO.md"), "wb").write(("\n".join(L) + "\n").encode("utf-8"))
    print("entregas escritas")


if __name__ == "__main__":
    main()
