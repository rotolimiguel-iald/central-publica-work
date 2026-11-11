# -*- coding: utf-8 -*-
"""_r4ag_05_h0dn_v410.py -- agente de adaptacao da R1 (ADENDO 3, D96, E34): o texto e o contrato do registro h0dn_bg1_v410 (registros_h0dn_v410.py: SO' contrato e texto, o_que_falta e ressalvas) e os snippets do artigo PT/EN.
A frase do poder certificado, PT e EN, ao lado da frase obrigatoria («pré-registrado; nenhum dado observado lido») e da parede de montagem, que ficam; a ORDEM KIMI H0DN-02 como pino citado no contrato. runtime_h0dn_v410.py (e a funcao veredito_h0dn) NAO mudam."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

H = []
H.append(('"frase_parede_pt": DL.FRASE_H0DN_PAREDE_PT, "frase_parede_en": DL.FRASE_H0DN_PAREDE_EN,\n',
          '"frase_parede_pt": DL.FRASE_H0DN_PAREDE_PT, "frase_parede_en": DL.FRASE_H0DN_PAREDE_EN, "frase_poder_pt": DL.FRASE_H0DN_PODER_PT, "frase_poder_en": DL.FRASE_H0DN_PODER_EN,\n'
          '            "ordem_kimi_02": dict(DL.H0DN_ORDEM02, citado_nao_embutido=True, em_rito_nada_e_lido=True),   # (D96: a ORDEM KIMI H0DN-02 e\' PINO CITADO: nome, sha256 e bytes lidos do arquivo no build e conferidos contra o ADENDO 3)\n', 1))
H.append(('"a abertura e\' de versao futura. H0DN x BG1: " + Q + ".",\n',
          '"a abertura e\' de versao futura. [OPEN, D96] o certificado de poder: " + DL.FRASE_H0DN_PODER_PT + ". H0DN x BG1: " + Q + ".",\n', 1))
H.append(('"A RESSALVA DA NOVIDADE DE USO: o agregado publico do H0DN e\' conhecido desde out/2025;',
          '"O PODER CERTIFICADO (D96, ordem do operador de 10/11): " + DL.FRASE_H0DN_PODER_PT + "; a ORDEM KIMI H0DN-02 (pino citado por sha256, nao embutida) manda fechar a covariancia fisica e entregar o certificado de poder as cegas, sem o vetor observado; a funcao de veredito congelada nao muda. "\n                  "A RESSALVA DA NOVIDADE DE USO: o agregado publico do H0DN e\' conhecido desde out/2025;', 1))
H.append(('"G1/G2: o operador de agregacao das curvas de luz (47 IDs com multiplas curvas), 8 IDs sem correspondencia exata, 2 aliases candidatos [OPEN]"],\n',
          '"G1/G2: o operador de agregacao das curvas de luz (47 IDs com multiplas curvas), 8 IDs sem correspondencia exata, 2 aliases candidatos [OPEN]",\n'
          '                        "o certificado de poder, as cegas, sob a covariancia fisica (D96): " + DL.FRASE_H0DN_PODER_PT + " [OPEN; ORDEM KIMI H0DN-02, pino citado: sha256 " + DL.H0DN_ORDEM02["sha256"] + ", " + str(DL.H0DN_ORDEM02["bytes"]) + " bytes; o teste segue " + Q + "]"],\n', 1))
H.append(('"ressalvas": [DL.FRASE_H0DN_PAREDE_PT + " (o teste segue " + Q + ")", "o poder e\' PROSPECTIVO e SINTETICO, condicional ao modelo de covariancia publicado (bloco-diagonal; a independencia local/fundo e\' assumida, nao medida); nao e\' desvio observado",\n',
          '"ressalvas": [DL.FRASE_H0DN_PAREDE_PT + " (o teste segue " + Q + ")", Q + ": " + DL.FRASE_H0DN_PODER_PT + " (D96, ordem do operador de 10/11; E34)",\n'
          '                      "o poder e\' PROSPECTIVO e SINTETICO, da covariancia publicada (que nao aceita o vetor real), condicional ao modelo de covariancia publicado (bloco-diagonal; a independencia local/fundo e\' assumida, nao medida); nao e\' desvio observado nem poder certificado",\n', 1))
H.append(('"[OPEN] a covariancia fisica conjunta (G3/G4), o vetor observado e os IDs: ate\' la\', a funcao de veredito so\' pode devolver inconclusivo por sistematica", ',
          '"[OPEN] a covariancia fisica conjunta (G3/G4), o vetor observado e os IDs: ate\' la\', a funcao de veredito so\' pode devolver inconclusivo por sistematica", "[OPEN, D96] o poder preditivo discriminante certificado, as cegas, sob a covariancia fisica: " + DL.FRASE_H0DN_PODER_PT + "; o limiar de poder e\' do operador e nao esta\' decidido", ', 1))
H.append(('"que o poder prospectivo seja medida da natureza: e\' condicional ao modelo de covariancia publicado", ',
          '"que o poder prospectivo seja medida da natureza, ou poder certificado: e\' da covariancia publicada, que nao aceita o vetor real, e condicional ao modelo de covariancia publicado; o certificado, as cegas, sob a covariancia fisica, nao existe hoje (D96)", ', 1))
H.append(('"decisoes": {k_: DL.DECISOES[k_] for k_ in ("D72", "D73", "D76")}, "erratas": [DL.ERRATA_E30],',
          '"decisoes": {k_: DL.DECISOES[k_] for k_ in ("D72", "D73", "D76", "D96")}, "erratas": [DL.ERRATA_E30, DL.ERRATA_E34], "poder_pt": DL.FRASE_H0DN_PODER_PT, "poder_en": DL.FRASE_H0DN_PODER_EN, "ordem_kimi_02": dict(DL.H0DN_ORDEM02, citado_nao_embutido=True, em_rito_nada_e_lido=True),', 1))
H.append(('for k_ in ("as_decisoes_de_09nov", "a_leitura_do_5sigma", "o_selo_diz_beta_tgl_provado")}',
          'for k_ in ("as_decisoes_de_09nov", "a_leitura_do_5sigma", "o_selo_diz_beta_tgl_provado", "o_teste_sem_poder_preditivo_nao_se_roda")}', 1))
H.append(('"decisoes": {k_: DL.DECISOES[k_] for k_ in ("D72", "D73", "D76")}, "erratas": [DL.ERRATA_E30]}', '"decisoes": {k_: DL.DECISOES[k_] for k_ in ("D72", "D73", "D76", "D96")}, "erratas": [DL.ERRATA_E30, DL.ERRATA_E34]}', 1))
aplicar("registros_h0dn_v410.py", H)

# ---------------------------------------------------------------- a frase de moldura do H0DN (delta) leva a ressalva do poder da covariancia publicada
D = []
D.append(('FRASE_DA_MOLDURA_H0DN_PT = "pré-registrado nesta versão selada; poder prospectivo sintético de 96,6 % e 62,5 %; nenhum vetor observado lido; a abertura é de versão futura, com a covariância física fechada"',
          'FRASE_DA_MOLDURA_H0DN_PT = "pré-registrado nesta versão selada; poder prospectivo sintético de 96,6 % e 62,5 %, da covariância publicada (não é poder certificado); nenhum vetor observado lido; a abertura é de versão futura, com a covariância física fechada e o poder certificado"', 1))
D.append(('FRASE_DA_MOLDURA_H0DN_EN = "pre-registered in this sealed version; synthetic prospective power 96.6% and 62.5%; no observed vector read; the opening belongs to a future version, with the physical covariance closed"',
          'FRASE_DA_MOLDURA_H0DN_EN = "pre-registered in this sealed version; synthetic prospective power 96.6% and 62.5%, of the published covariance (not a certified power); no observed vector read; the opening belongs to a future version, with the physical covariance closed and the power certified"', 1))
aplicar("delta_v410.py", D)

# ---------------------------------------------------------------- snippets do artigo PT/EN do H0DN
P = []
P.append(('+ _th410(_V410_H0DN_CONTRACT["frase_parede_pt"]) + r". "\n',
          '+ _th410(_V410_H0DN_CONTRACT["frase_parede_pt"]) + r". "\n'
          '             r"\\textbf{O poder certificado (D96, ordem do operador de 10/11).} \\textsf{[INPUT]} «se ele não tiver poder preditivo não vamos roda-lo»; «um teste com poder preditivo discriminante real». \\textsf{[REAL]} " + _th410(_V410_H0DN_CONTRACT["frase_poder_pt"]) + r". A ordem está pinada por sha256 (\\texttt{" + _th410(_V410_H0DN_CONTRACT["ordem_kimi_02"]["sha256"][:16]) + r"}), não embutida, e em rito nada dela é lido. "\n', 1))
P.append(('o poder é prospectivo e sintético; provado na natureza', 'o poder é prospectivo e sintético, da covariância publicada (que não aceita o vetor real), e não é poder certificado; provado na natureza', 1))
aplicar("artigo_pt_h0dn_v410.pysnip", P, parse=False)
E = []
E.append(('+ _th410(_V410_H0DN_CONTRACT["frase_parede_en"]) + r". "\n',
          '+ _th410(_V410_H0DN_CONTRACT["frase_parede_en"]) + r". "\n'
          '             r"\\textbf{The certified power (D96, the operator\'s order of 10/11).} \\textsf{[INPUT]} The operator (our translation): if it has no predictive power we will not run it; a test with real discriminating predictive power. \\textsf{[REAL]} " + _th410(_V410_H0DN_CONTRACT["frase_poder_en"]) + r". The order is pinned by sha256 (\\texttt{" + _th410(_V410_H0DN_CONTRACT["ordem_kimi_02"]["sha256"][:16]) + r"}), not embedded, and in the rite nothing of it is read. "\n', 1))
E.append(('the power is prospective and synthetic; proved in nature', 'the power is prospective and synthetic, of the published covariance (which does not admit the real vector), and is not a certified power; proved in nature', 1))
aplicar("artigo_en_h0dn_v410.pysnip", E, parse=False)
