# -*- coding: utf-8 -*-
"""02/11/2026: reparos de docstring nas três pedras candidatas, conforme a revisão Sonnet (REVISAO_PEDRAS_CANDIDATAS_02nov_SONNET.md),
conferida pela gerência no kernel. Nenhuma prova muda. Backup de bytes; substituições exatas com assert (falha visível)."""
import datetime, hashlib, os
from pathlib import Path
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

def patch(path: Path, reps):
    b = path.read_bytes(); t = b.decode("utf-8")
    bk = path.with_name(path.name + ".bak_" + TS); open(bk, "xb").write(b); assert bk.read_bytes() == b
    for old, new in reps:
        assert t.count(old) == 1, (path.name, old[:70], t.count(old))
        t = t.replace(old, new)
    tmp = path.with_name(path.name + ".tmp"); tmp.write_text(t, encoding="utf-8", newline="\n"); os.replace(tmp, path)
    print(path.name, s16(bk), "->", s16(path))

A = Path(r"C:\t\crivo02nov\KEhATangenteCandidata.lean")
patch(A, [
 ("* A massa lida no acorde (a derivada, `massaDerivada`) e a massa lida na projecao dividida por `K`; no posto\n  `K = 1` e as duas coincidem (`deriv_eq_projecao_at_half`).",
  "* A massa lida no acorde (a derivada, `massaDerivada`) e a massa lida na projecao dividida por `K`. Em TODA\n  `TransicaoParaAMassa` vale θ = π/4 (teorema `theta_eq_pi_div_four`, derivado do campo `autoconjugado`), logo K = 1\n  sempre: a divisao e por 1, e `no_posto_o_acorde_e_a_projecao` repete `massa_derivada_eq_projecao` (PonteDaMassa.lean:181)\n  na forma de K. O conteudo desta pedra e a FORMA `massa = projecao / K`, nao um fato novo (dito, revisao Sonnet 02/11)."),
 ("* `transicaoLida`: a transicao com o angulo LIDO pela regra da selecao a partir do peso da face absoluta\n  (`absolute_faces_half` via `peso_da_face_absoluta`), em vez de escrito; coincide com `transicaoDerivada`.\n  A hipotese nao some: muda do numero `π/4` para a regra de leitura `selectionAngle`, que ja era termo.",
  "* `transicaoLida`: a transicao com o angulo dado pela regra da selecao, `selectionAngle (1/2)`. O numero ½ SEGUE\n  ESCRITO na definicao; `o_angulo_e_lido_do_absoluto` mostra so que esse ½ coincide com o peso da face absoluta\n  (`peso_da_face_absoluta`, por `rw`): COINCIDENCIA DE VALOR, nao ponte, como o kernel ja avisa (PonteDaMassa.lean:245-246,\n  275-276). A hipotese nao some nem muda de lugar; a regra de leitura ja era termo. Coincide com `transicaoDerivada`."),
 ("Homonimos: este K (tangente do angulo lido) nao e o K de Hubble nem o K modular; a ponte e leitura.",
  "Homonimos: este K (tangente do angulo lido) nao e o K de Hubble, nem o K modular, nem `genK` (TheAngleIsTheProjection.lean:76,\no gerador 2×2); «posto» aqui e o angulo π/4 da selecao justa, nao o Um POSTO do `echo 1` nem o posto como cargo. Dito para nao\nencadear homonimos; a ponte e leitura."),
 ("/-- a massa lida no acorde (a derivada) e a massa lida na projecao dividida por `K`. -/",
  "/-- a massa lida no acorde (a derivada) e a massa lida na projecao dividida por `K`. Como θ = π/4 em toda transicao\n(`theta_eq_pi_div_four`), K = 1 e a divisao e por 1: a FORMA, nao um fato novo. -/"),
 ("/-- no posto `K = 1`: o acorde (a derivada) e a projecao sao a mesma massa. -/",
  "/-- no posto `K = 1`: o acorde (a derivada) e a projecao sao a mesma massa (repete `massa_derivada_eq_projecao`,\nPonteDaMassa.lean:181, na forma de K). -/"),
 ("/-- o angulo da transicao lida E o peso da face absoluta passado pela regra da selecao: nao e escrito. -/",
  "/-- o angulo da transicao lida, `selectionAngle (1/2)`, coincide com o peso da face absoluta passado pela mesma regra\n(`peso_da_face_absoluta`): o ½ esta escrito na definicao e a igualdade e um `rw`; coincidencia de valor, nao ponte. -/"),
])

B = Path(r"C:\t\ponte02nov\APonteDoAtritoCandidata.lean")
patch(B, [
 ("* ★ A PONTE (`o_atrito_lido_na_temperatura`): o que atravessa numa volta do relogio do boost e o PESO DE BOLTZMANN do\n  atrito a temperatura derivada, `e^{−tβg}` em `t = P` e `e^{−βg/T}`. As duas pontas que o kernel tinha separadas\n  (o atrito `βg` e a temperatura `κ/2π`) aparecem numa identidade so.",
  "* ★ A PONTE (`o_atrito_lido_na_temperatura`): o que atravessa numa volta do relogio do boost, `e^{−Pβg}`, e `e^{−βg/T}` com\n  `T = 1/P`. TRIVIAL POR DEFINICAO (algebra do expoente), dito: o nome e a leitura, o conteudo e a definicao. As duas pontas\n  que o kernel tinha separadas (o atrito `βg` e a temperatura `κ/2π`) aparecem numa identidade so. «Peso de Boltzmann» e\n  ROTULO [ONTO]: `βg` e uma taxa de decaimento, nao uma energia; a leitura «ħ = k_B = 1» e do operador."),
 ("* A PARCELA POR VOLTA e `1 − e^{−δS}` (`a_parcela_e_um_menos_o_peso`) e nunca excede `δS` (`a_parcela_nao_excede_a_entropia`,\n  que e `parcela_le_beta` em forma de temperatura): o balanco da volta fecha como balanco de Clausius.",
  "* A PARCELA POR VOLTA e `1 − e^{−δS}` (`a_parcela_e_um_menos_o_peso`) e nunca excede `δS` (`a_parcela_nao_excede_a_entropia`,\n  que e `parcela_le_beta` em forma de temperatura). Tem a FORMA de Clausius: `δS := δQ/T` e DEFINICAO desta pedra e `δQ := βg`\n  e leitura do operador [ONTO]; nenhum balanco termodinamico e provado aqui."),
 ("* O EQUILIBRIO DAS CONTAS (operador): atravessado + cobrado = 1 em toda volta (`o_balanco_fecha_a_cada_volta`).",
  "* O EQUILIBRIO DAS CONTAS (operador): atravessado + cobrado = 1 em toda volta (`o_balanco_fecha_a_cada_volta`), re-exportacao\n  de `the_charge_is_continuous_both_sides`, que o kernel marca TRIVIAL POR DEFINICAO (ThePsionAndTheViscosity.lean:87-88)."),
 ("* O ZERO ABSOLUTO: no periodo fiel `T = κ/2π > 0` (`o_zero_absoluto_nao_e_lido`); e no limite `T → 0⁺` a parcela\n  quitaria numa volta (`no_zero_absoluto_a_parcela_quitaria`), o que `parcela_nunca_quita` proibe para todo periodo fiel.",
  "* O ZERO ABSOLUTO: no periodo fiel `T = κ/2π > 0` (`o_zero_absoluto_nao_e_lido`); e no limite `T → 0⁺` a parcela\n  quitaria numa volta (`no_zero_absoluto_a_parcela_quitaria`), o que `parcela_nunca_quita` proibe para todo periodo fiel.\n  Esse limite e um CALCULO sobre a funcao generica `T ↦ 1 − e^{−q/T}`, `q > 0` arbitrario, nao sobre o modelo (nao usa `Emprestimo`)."),
 ("Homonimos: a temperatura aqui e a do relogio do boost (Unruh/BW, [KNOWN]), nao temperatura de laboratorio; o «calor da\nvolta» e a leitura do operador do coeficiente `βg`; o balanco de Clausius da tela otica (`boost_defect_with_derived_period`)\ne outro objeto, nao ligado aqui por termo.",
  "Homonimos e entradas: a temperatura aqui e `1/P = κ/2π` do periodo fiel (`reciprocal_temperature`); o kernel a chama\n«normalizacao herdada (sem Unruh/KMS)» (BoostHeatConstruction.lean:16), e que seja a temperatura de Unruh e [KNOWN] fora do\ntermo; nao e temperatura de laboratorio. `g` (o contraste) e `κ` sao dados livres de `Emprestimo` [INPUT]. O «calor da volta»\ne a leitura do operador do coeficiente `βg`. O balanco de Clausius da tela otica (`boost_defect_with_derived_period`) e outro\nobjeto, nao ligado aqui por termo. `ThePsionAndTheViscosity.transmitted` e citado pelo nome inteiro porque `TGLExt.transmitted`\n(TheDeathOfTheSignal.lean:60) e homonimo."),
 ("/-- a entropia da volta, Clausius: `δS = δQ / T`. -/", "/-- a entropia da volta: `δS := δQ / T`. DEFINICAO com a forma de Clausius, nao teorema termodinamico. -/"),
 ("/-- ★ A PONTE: o que atravessa numa volta e o peso de Boltzmann do atrito a temperatura derivada,\n`e^{−Pβg} = e^{−βg/T}`. -/",
  "/-- ★ A PONTE: o que atravessa numa volta, `e^{−Pβg}`, e `e^{−βg/T}` com `T = 1/P`. Trivial por definicao (algebra do\nexpoente), dito; «peso de Boltzmann» e rotulo [ONTO]. -/"),
 ("/-- a parcela por volta e `1 − e^{−δS}`: o balanco da volta fecha como Clausius. -/",
  "/-- a parcela por volta e `1 − e^{−δS}`: a FORMA de Clausius, por definicao de `entropiaDaVolta`. -/"),
 ("/-- o equilibrio das contas (operador): atravessado + cobrado = 1 em toda volta. -/",
  "/-- o equilibrio das contas (operador): atravessado + cobrado = 1 em toda volta. Re-exportacao de\n`the_charge_is_continuous_both_sides` (trivial por definicao no kernel; o nome e a leitura). -/"),
 ("/-- no limite do zero absoluto a parcela quitaria numa volta: `1 − e^{−q/T} → 1` quando `T → 0⁺`, para `q > 0`.\nO periodo fiel nao chega la (`o_zero_absoluto_nao_e_lido`, `parcela_nunca_quita`). -/",
  "/-- no limite do zero absoluto a parcela quitaria numa volta: `1 − e^{−q/T} → 1` quando `T → 0⁺`, para `q > 0`.\nCalculo sobre a funcao generica em `q`, nao sobre o modelo. O periodo fiel nao chega la (`o_zero_absoluto_nao_e_lido`,\n`parcela_nunca_quita`). -/"),
])

C = Path(r"C:\t\ponte02nov\OUmInscritoCandidata.lean")
patch(C, [
 ("* `gamma_no_fixed` alimentado por `B0_zero`, `B0_add`, `B0_continuous`, `B0_no_eigen`: so o vacuo resta fixo pelo boost da\n  luz — o Um e o UNICO autovetor;",
  "* `gamma_no_fixed` alimentado por `B0_zero`, `B0_add`, `B0_continuous`, `B0_no_eigen`: so o vacuo resta FIXO pelo boost da\n  luz — o Um e o UNICO vetor fixo (autovalor 1 do grupo). Autovetores com fase (`Γ(B0 s) ψ = c(s) • ψ`, `‖c‖ = 1`) nos\n  setores de n ≥ 1 particulas NAO sao excluidos por este termo;"),
 ("Corrige a frase da gerencia (02/11) «a luz nao tem autovetor nenhum»: valia so em uma particula. Leitura vigente:\no espectro pontual da luz e o Um e so ele; o resto e continuo.",
  "Corrige a frase da gerencia (02/11) «a luz nao tem autovetor nenhum»: valia so em uma particula. Leitura: o Um e o unico\nvetor FIXO da luz [REAL]; que nao haja outro autovetor com fase, e que «o resto seja continuo», e [KNOWN/OPEN como termo]\n(revisao Sonnet 02/11). No certificado o mesmo fato e `light_modular_fixed_iff_vacuum` (QGReaderUVLock.lean:149), condicional\na `C`; aqui vale no Fock concreto, sem hipotese. `Γ(B0(−2πt))` e o fluxo modular do vacuo no Fock concreto por\n`CanonicalFockBWR2.actualModularFlow_eq_gamma`; no certificado isso e o campo `bw_kms`."),
 ("/-- a luz fixa o Um: o vacuo e fixo por toda segunda quantizacao. -/", "/-- a luz fixa o Um: o vacuo e fixo por toda segunda quantizacao (re-exportacao de `gamma_vacuum`). -/"),
 ("/-- o Um e o UNICO fixo do boost da luz no Fock: todo vetor fixo por `Γ(B0 s)` esta na reta do vacuo. -/",
  "/-- o Um e o UNICO fixo do boost da luz no Fock: todo vetor fixo por `Γ(B0 s)` esta na reta do vacuo (a reta inclui 0;\nautovetor com fase nao e tratado aqui). -/"),
 ("/-- o Um inscrito e a exponencial do zero: exp(0) = 1. -/", "/-- o Um inscrito e a exponencial do zero: exp(0) = 1 (re-exportacao de `exponential_zero`). -/"),
 ("/-- em uma particula, sem par: o unico autovetor do boost e o zero, o abstrato inominado. -/",
  "/-- em uma particula, sem par: o unico autovetor do boost e o zero, o abstrato inominado (apelido de `B0_no_eigen`, PAGO\npela bancada). -/"),
 ("/-- ★ composto: a luz tem autovetor, a inscricao do Um, e so ela. -/", "/-- ★ composto: a luz tem um vetor fixo, a inscricao do Um, e so ele. -/"),
])
print("ok")
