# -*- coding: utf-8 -*-
"""_adapt_h0dn_delta_registros_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410): as constantes do registro H0DN (D72) no delta_v410.py (H0DN_REGISTRO, TAG, vereditos ok/recusa, N_CHECKS_H0DN LIDO do DESENHO,
a pasta do desenho do Codex, o sha16 da leitura do dossie LIDO do DESENHO, a rota Kimi, o agregado que nao entra; REGISTROS_FUNCAO com os dois registros) e, em registros_v410.py, as FONTES e ORIGENS do H0DN (via registros_h0dn_v410).
Trocas exatas; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def aplicar(nome, trocas, marca):
    P = os.path.join(HERE, nome)
    b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0, (nome, "era LF; agora tem CRLF: parar")
    bk = P + ".bak_" + TS + "_h0dn"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
    t = b0.decode("utf-8")
    for velho, novo, n in trocas:
        c = t.count(velho); assert c == n, (nome, "troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140]); t = t.replace(velho, novo)
    linhas = t.split("\n"); i = 1
    while linhas[i].startswith("# [ADAPTADO"):
        i += 1
    linhas.insert(i, marca); t = "\n".join(linhas)
    nb = t.encode("utf-8"); ast.parse(nb)
    tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P); assert open(P, "rb").read() == nb
    print(nome, "adaptado (H0DN):", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(trocas))


DL_TROCAS = [
    ("REGISTROS_FUNCAO = [FECHO_REGISTRO]\n",
     "H0DN_REGISTRO = \"h0dn_bg1_v410\"                               # o SEGUNDO registro com FUNCAO (D72): o teste pre-registrado da razao de Hubble H0DN x BG1; chamado no main LOGO DEPOIS de iald2_v410\n"
     "TAG_H0DN = \"H0DN_BG1\"\n"
     "VEREDITO_H0DN_OK = \"TGL_H0DN_BG1_V410__PREREGISTERED_RATIO_TEST_FROZEN__NO_OBSERVED_VECTOR_READ__SYNTHETIC_CONDITIONAL_POWER_ONLY__GATE_UNMOVED\"\n"
     "VEREDITO_H0DN_RECUSA = \"TGL_H0DN_BG1_V410__REFUSED_%s__GATE_UNMOVED\"\n"
     "_m_nh = re.search(r\"N_CHECKS = (\\d+): c1 os 9 pinos\", _DESENHO_TXT)\n"
     "assert _m_nh, \"o AO LADO D72 do DESENHO_v410 nao traz o N_CHECKS do H0DN\"\n"
     "N_CHECKS_H0DN = int(_m_nh.group(1))                            # LIDO do AO LADO D72 do DESENHO_v410 (12): conferido contra as checagens que o runtime emite\n"
     "N_PINOS_FREEZE_R2 = int(re.search(r\"`FREEZE_R2\\.json`, (\\d+) pinos\", _DESENHO_TXT).group(1))   # (9) LIDO do DESENHO; conferido contra o arquivo no preparo\n"
     "H0DN_DIR = os.path.join(WK, \"astra_bell_fock_tt_05nov\", \"h0dn_bg1_06nov\")   # a pasta do desenho do Codex astra-bell (06/11); so' leitura\n"
     "LEITURA_DOSSIE_SHA16_DO_DESENHO = re.search(r\"`LEITURA_DOSSIE_5SIGMA_09nov\\.json` sha16 `([0-9a-f]{16})`\", _DESENHO_TXT).group(1)   # LIDO do DESENHO (D72); conferido contra o arquivo em registros_h0dn_v410\n"
     "H0DN_ROTA_KIMI = {\"rota\": \"coerencia_espectro_fotometria_05nov (Kimi)\", \"estado\": \"NOT_TESTABLE\", \"eta\": 1, \"mapa_seq\": 1635, \"nota\": \"K nao age em luminosidade nem em distancia angular; eta = 1; nao discrimina; nao e' o teste (D72, c10; a leitura da gerencia do dossie)\"}\n"
     "H0DN_AGREGADO_NAO_ENTRA = (\"73,50\", \"73.50\", \"0,81\", \"5,93\", \"5.93\", \"5,75\", \"5.75\")   # D72 (c8): a aritmetica do agregado publico do H0DN NAO entra em texto do registro\n"
     "REGISTROS_FUNCAO = [FECHO_REGISTRO, H0DN_REGISTRO]              # os DOIS registros com FUNCAO da v410 (D72): iald2_v410 e, logo depois, h0dn_bg1_v410\n"
     "assert not any(t_ in VEREDITO_H0DN_OK + VEREDITO_H0DN_RECUSA for t_ in TOKENS_PROIBIDOS_V410 + TOKENS_PROIBIDOS_H0DN)\n", 1),
]
RG_TROCAS = [
    ("import delta_v410 as DL  # noqa: E402\n\nINS = os.path.join(HERE, \"insumos\")\n",
     "import delta_v410 as DL  # noqa: E402\nimport registros_h0dn_v410 as RH  # noqa: E402   (D72: as fontes e os insumos do registro H0DN)\n\nINS = os.path.join(HERE, \"insumos\")\n", 1),
    ("              (\"BUNDLE_v410.json\", DL.BUNDLE_ARQ), (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, \"KH_N1_v410.json\"))])\n",
     "              (\"BUNDLE_v410.json\", DL.BUNDLE_ARQ), (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, \"KH_N1_v410.json\"))]\n"
     "           + list(RH.ORIGENS_H0DN))   # (D72) as copias duraveis dos insumos do H0DN em insumos\\\\h0dn_*\n", 1),
    ("    {\"chave\": CHAVE_KH, \"arquivo\": os.path.join(INS, DL.KH_N1_INSUMO), \"papel\": \"a medida da cobertura no Audit do sandbox da v410 (pos_build_kernel_v410.py)\"},\n]\n",
     "    {\"chave\": CHAVE_KH, \"arquivo\": os.path.join(INS, DL.KH_N1_INSUMO), \"papel\": \"a medida da cobertura no Audit do sandbox da v410 (pos_build_kernel_v410.py)\"},\n] + list(RH.FONTES_H0DN_RG)   # (D72) as fontes pinadas do H0DN\n", 1),
]
aplicar("delta_v410.py", DL_TROCAS, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_h0dn_delta_registros_v410.py: as constantes do registro H0DN (D72): H0DN_REGISTRO, TAG, vereditos, N_CHECKS_H0DN e N_PINOS lidos do DESENHO, a pasta do desenho, a rota Kimi, o agregado que nao entra; REGISTROS_FUNCAO com os dois registros")
aplicar("registros_v410.py", RG_TROCAS, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_h0dn_delta_registros_v410.py: as FONTES e ORIGENS do H0DN (registros_h0dn_v410), copiadas por copiar_insumos_v410.py e lidas pelo motor v392 por chave")
