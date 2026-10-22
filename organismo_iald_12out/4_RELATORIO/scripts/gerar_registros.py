"""Gera registro_rota_F1.MOTOR.json, registro_mapa_F1.MOTOR.json e medidas/HASHES_FONTES.json.
Formato de rotas.py modelo; artefatos como lista de caminhos (o sha256 e calculado pela ferramenta ao registrar).
NAO registra no mapa (rotas.py registrar e ato da gerencia). Hashes lidos dos bytes. Sem a palavra proibida."""
import hashlib, json, pathlib

W = pathlib.Path(r"C:\IALD\Central de Patentes\work")
O = W / "organismo_iald_12out"
R = O / "4_RELATORIO"
FONTES = [
    W / "cunhagens_12out" / "OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt",
    pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"),
    O / "0_LEVANTAMENTO_ORGANISMO" / "ORGANISMO_LEVANTAMENTO.md",
    O / "0_LEVANTAMENTO_PROVA" / "INVENTARIO_PROVA.md",
    O / "0_LEVANTAMENTO_PROVA" / "CANAIS.json",
    O / "1_DESENHO_PEDRA" / "ESPEC_PEDRA_IALD.md",
    O / "1_DESENHO_PEDRA" / "PREREGISTRO_PEDRA.json",
    O / "1_DESENHO_PEDRA" / "FREEZE.json",
    O / "1_ESTRATEGIA_A" / "ESTRATEGIA_A.md",
    O / "1_ESTRATEGIA_B" / "ESTRATEGIA_B.md",
    O / "1_JUIZ" / "PROGRAMA_PROVA_DISTINTIVA.md",
    O / "2_CONSTRUCAO" / "sandbox" / "TGLExt" / "IALD.lean",
    O / "2_CONSTRUCAO" / "RESULTADO_CONSTRUCAO.md",
    O / "2_CONSTRUCAO" / "RESULTADO_PEDRA.json",
    O / "2_CONSTRUCAO" / "FREEZE_CONSTRUCAO.json",
    O / "3_AUD_REPRO" / "RELATORIO_AUD_REPRO.md",
    O / "3_AUD_REPRO" / "MANIFESTO_AUD_REPRO.json",
    O / "3_AUD_REPRO" / "sandbox" / "SondasAuditor.lean",
    O / "3_AUD_REPRO" / "sandbox" / "SondaFundacaoSemPeso.lean",
    O / "3_AUD_REPRO" / "sandbox_atual" / "IALD_porte.lean",
    O / "3_AUD_REPRO" / "sandbox_atual" / "TGLExt" / "TheTimeIsNotAPost.lean",
    O / "3_AUD_ESTATUTO" / "AUDITORIA_ESTATUTO.md",
    W / "frequencia_defasa_12out" / "5_R3" / "sandbox" / "TGLExt" / "TheUnitIsTheRank.lean",
    R / "O_ORGANISMO_E_A_PROVA_DISTINTIVA.md",
    R / "medidas" / "beta_runtime.json",
]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

hashes = []
for p in FONTES:
    hashes.append({"path": str(p), "sha256": sha(p), "bytes": p.stat().st_size})
(R / "medidas" / "HASHES_FONTES.json").write_text(json.dumps(hashes, ensure_ascii=False, indent=1), encoding="utf-8")
H = {pathlib.Path(h["path"]).name: h["sha256"][:16] for h in hashes}
beta = json.loads((R / "medidas" / "beta_runtime.json").read_text(encoding="utf-8"))["beta_repr"]

artefatos = [str(R / "O_ORGANISMO_E_A_PROVA_DISTINTIVA.md"),
             str(O / "2_CONSTRUCAO" / "sandbox" / "TGLExt" / "IALD.lean"),
             str(O / "2_CONSTRUCAO" / "RESULTADO_PEDRA.json"),
             str(O / "1_DESENHO_PEDRA" / "PREREGISTRO_PEDRA.json"),
             str(O / "1_DESENHO_PEDRA" / "FREEZE.json"),
             str(O / "2_CONSTRUCAO" / "FREEZE_CONSTRUCAO.json"),
             str(O / "3_AUD_REPRO" / "RELATORIO_AUD_REPRO.md"),
             str(O / "3_AUD_REPRO" / "sandbox" / "SondasAuditor.lean"),
             str(O / "3_AUD_REPRO" / "sandbox" / "SondaFundacaoSemPeso.lean"),
             str(O / "3_AUD_ESTATUTO" / "AUDITORIA_ESTATUTO.md"),
             str(O / "1_JUIZ" / "PROGRAMA_PROVA_DISTINTIVA.md")]

rota = {
    "tipo": "ROTA",
    "rota_id": "formal.iald_o_motor_unico",
    "dominio": "FORMAL",
    "titulo": "TGLExt.IALD, o motor unico: inscricao (post a, posto 1) -> transporte U ancorado -> defasagem axiomFlow -> leitura post a -> memoria <psi, P psi>, num so termo, em sandbox contra o kernel v391",
    "pergunta": "O organismo (o rank que liga o Nome a identidade IALD; a lei da memoria M[rho] = Tr[rho Pi_N]; o atrator; Zenao; o tempo sem posto) compoe-se num unico termo de kernel, e o que esse termo prova e nao prova?",
    "dados": ["nenhum dado observado; so o kernel v391 do Nos (lido via .lake/build copiado e verificado) e as candidatas da v392 em sandbox"],
    "metodo": ("Desenho pre-registrado e congelado (FREEZE " + H["FREEZE.json"] + ", 03:53:13Z) antes da construcao (04:15:14Z); "
               "pedra IALD.lean " + H["IALD.lean"] + " com 51 declaracoes (34 pre-registradas + 17 novas: pontes B1-B11 a Palavra, ADENDO1, TheUnitIsTheRank r2, TheTimeHasNoRank; sondas S4-S6); "
               "lean v4.31.0 direto, LEAN_PATH so-leitura; #print axioms por declaracao; ensaio numerico 2x2 e nxn com beta de runtime; "
               "auditoria de reproducao (recompilacao independente, 9 sondas adversariais em Lean, porte as candidatas vigentes) e auditoria de estatuto e regua (leitura e grep)."),
    "resultado": ("EXIT 0; 0 sorry; 51/51 no trio {propext, Classical.choice, Quot.sound}; .olean 643d767a3d9a4cfd reproduzido bit a bit; ensaio 84/84; "
                  "tres nomes do Nome (ialdSelector, PFmic, post a) sao a mesma construcao (rfl); o e de Jones e a secao, nao o Nome (T12); "
                  "M[a]=1, M[psi]=1 <-> post psi = post a (T5'); motor idempotente sob ancora U a = a (T2); nunca chega e tende ao posto (T8, T8'''); relogio das metades paga zeno_partial_sum (T8''); o Verbo nao e posto (T9). "
                  "Sondas da auditoria: a ancora fraca post a (U a) = a basta e nao e necessaria no sentido forte (anchor_not_necessary); H-N decorativa em T2; T7' prova-se sem a Fundacao (Agape so nominal); "
                  "beta nao atua na saida do motor (T1; the_leak_is_any_rate); a pedra pina candidatas superadas (porte as vigentes compila, 1211e76b). beta runtime = " + beta + "."),
    "veredito": "PEDRA_REPRODUZ_51_DE_51_NO_TRIO__NAO_ENTRA_NA_V392_COMO_ESTA__OITO_CORRECOES_NOMEADAS__VALIDADE_NAO_PROVA_DISTINTIVA__GATE_INTOCADO",
    "estatuto": "REAL",
    "status": "EXAMINADA_COM_DEFEITO",
    "olhou_dados": False,
    "defeito": ("ALTA: homonimo 'defasagem' sem ponte (IALD.dephase x diagExpect x eJ x Ergodicity.dephase); 'Agape por termo' e 'Q15 resolvida' nominais; o nome anchor_is_necessary diz mais do que o termo; "
                "MEDIA: [ONTO] sem marca nas docstrings; 'Q16/Q17 resolvidas' exagera (o organismo segue lista: 0 referencias a QGSolutionComplete, the_whole_is_one, the_matrix_rule, TheLedgerOfCharges, agape); beta nao atua no motor e nao e dito; "
                "pina TheTimeHasNoRank a68539d8 e TheUnitIsTheRank r2 3195ef8f em vez de TheTimeIsNotAPost 4d8a8259 e r3 e95775d6."),
    "nao_refazer": ("Nao refazer a busca de lema entre os 'quatro nomes do Nome': tres sao a mesma definicao (rfl) e o quarto (Jones) e a secao. "
                    "Nao refazer a pergunta se o motor prova beta na natureza: T1 mostra que a saida nao depende da taxa; a pedra e validade. "
                    "Nao reabrir Zenao como pergunta: o operador ja respondeu (06/10, 07/10); a face finita esta em T8-T8'''."),
    "proximo_passo": ("Aplicar as correcoes C1-C8 do relatorio (renomear T2', ancora fraca, H-N, Fundacao, homonimo, [ONTO], beta sem acao, re-pino), recompilar e re-auditar em sandbox; "
                      "decisoes do operador: Pi_N := post a (pergunta 2), a ancora posta ou provada (3), DualScalingData do motor (4), nome e entrada na v392 (6)."),
    "onde": str(O / "2_CONSTRUCAO" / "sandbox" / "TGLExt" / "IALD.lean") + " (TGLExt.IALD, nao instalada)",
    "artefatos": artefatos,
    "refs": ["infra.memoria_acom.core_20261010"],
    "nota": ("Gerencia c1, redator, 13/10/2026. Ordem do operador por sha256 78ef70e6f9868281. NOT_FALSIFIED nunca e a palavra proibida; PROVADA = validade; a confirmacao recusada e creditacao; "
             "o unico elo pendente da QG e beta_TGL na natureza a 5 sigma; o gate nao se move. Registrar e ato da gerencia (rotas.py registrar), nao deste redator."),
}

resultado = {
    "tipo": "RESULTADO",
    "rota_id": "formal.iald_o_motor_unico",
    "dominio": "FORMAL",
    "titulo": "O ORGANISMO E A PROVA DISTINTIVA - 12/10: relatorio ao operador (pedra, duas auditorias, estado da QG, programa da prova distintiva, v392, residuo nas quatro linguas)",
    "pergunta": "O que o organismo e em matematica, o que ficou ONTO, o que 'resolver a QG de uma vez por todas' pode significar, qual e o programa da prova distintiva e o que so o operador decide?",
    "dados": ["nenhum dado observado aberto; numeros transcritos do core v391 e das folhas por hash"],
    "metodo": "Composicao das folhas L1, L2, desenho, estrategias A e B, juiz, construcao e das duas auditorias (reproducao e estatuto), com as correcoes das auditorias ao lado; hashes por script; beta em runtime.",
    "resultado": ("Pedra TGLExt.IALD " + H["IALD.lean"] + ": 51/51 no trio, reproduz bit a bit; nao entra na v392 como esta (as duas auditorias convergem; vale a de estatuto somada ao re-pino da de reproducao). "
                  "QG provada como fecho logico (v391); o unico elo pendente e beta na natureza a 5 sigma. Programa: decisivo = razao de Hubble em duas testemunhas sem juiz (z_disc +4,28; ln B 9,17; INCONCLUSIVE_SYSTEMATICS ate D-H; por decisao 4,14/4,81, nao 5; 5 sigma so com sigma_comb <= 0,7686 ou centro >= 73,56, ou poder da conjunta >= 5 pela d72); "
                  "forma = par K x DeltaN_eff, R = 1,4844, ao lado do contorno de 14/08 e como cobranca nova (2,17-2,65 sigma contra LCDM + 1 parametro com o SO); morte = m2 (7,06 sigma com o centro do JUNO; 7,84 com o centro NuFIT); falsificador da teoria = piso por kappa. "
                  "Correcoes ao lado: m2 2031 depende do centro, nao de convencao; 'Planck 0,70 sigma' e poder (distancia 1,02); o par nao compoe leis ja cobradas. 13 perguntas nas quatro linguas."),
    "veredito": "RELATORIO_ENTREGUE__NENHUM_VEREDITO_SOBRE_A_NATUREZA__GATE_INTOCADO",
    "estatuto": "DERIVED",
    "status": "EXAMINADA_COM_DEFEITO",
    "olhou_dados": False,
    "defeito": "Os defeitos da pedra listados na rota (C1-C8); o par K x DeltaN_eff tem quadratura so como teto (covariancia do fundo comum por fazer) e hubble_form sem #print axioms (F6).",
    "nao_refazer": "Nao refazer o inventario dos 24 canais nem as projecoes condicionais da razao de Hubble: estao reproduzidas a diferenca 0,0 (z_disc 4,2837) e auditadas.",
    "proximo_passo": "Respostas do operador as 13 perguntas; correcoes C1-C8 da pedra; erratas ao lado do m2 2031, do Planck 0,70 e dos literais de N_eff (l.4802-4807); desenho da B3 da Bancada (BANCADA_PORTA.json, manifesto de canais, T18) se autorizado.",
    "onde": str(R / "O_ORGANISMO_E_A_PROVA_DISTINTIVA.md"),
    "artefatos": [str(R / "O_ORGANISMO_E_A_PROVA_DISTINTIVA.md"), str(R / "medidas" / "HASHES_FONTES.json"),
                  str(O / "3_AUD_REPRO" / "RELATORIO_AUD_REPRO.md"), str(O / "3_AUD_ESTATUTO" / "AUDITORIA_ESTATUTO.md"),
                  str(O / "1_JUIZ" / "PROGRAMA_PROVA_DISTINTIVA.md")],
    "refs": ["formal.iald_o_motor_unico"],
    "nota": "Sintetico e condicional; nenhuma funcao congelada executada; o um.py nao foi executado. Registrar e ato da gerencia.",
}

for nome, obj in (("registro_rota_F1.MOTOR.json", rota), ("registro_mapa_F1.MOTOR.json", resultado)):
    txt = json.dumps(obj, ensure_ascii=False, indent=1)
    assert "CONFIRMED" not in txt
    (R / nome).write_text(txt, encoding="utf-8")
    print(nome, len(txt.encode("utf-8")), hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16])
print(json.dumps(H, indent=1))
