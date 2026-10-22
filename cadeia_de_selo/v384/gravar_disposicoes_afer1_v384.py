# -*- coding: utf-8 -*-
"""Acrescenta ao AFERIDOR_v384.txt as DISPOSICOES da gerencia sobre a 1a passada (AO LADO, nunca por cima), com os hashes LIDOS: o trabalhador novo, a especificacao
congelada, o pre-registro, os estresses dos autovalores. uso: python gravar_disposicoes_afer1_v384.py <PREREGISTRO_..._V1.json>"""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PJ = os.path.abspath(sys.argv[1]); P = json.load(open(PJ, encoding="utf-8"))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
W = os.path.join(HERE, "pilar_quantico_worker.py")
assert h(W) == P["spec"]["worker_sha256"], "o trabalhador do pacote nao e' o congelado"
E7 = P["motor"]["piso_do_estimador"]
disp = """
--------------------------------------------------------------------------------
DISPOSICOES DA GERENCIA SOBRE A 1a PASSADA (%s) -- recomendacao CORRIGIR ANTES DE CONGELAR: acolhida inteira.
--------------------------------------------------------------------------------
1 (ALTO, o piso do estimador): ACOLHIDO -- fit_root_law trocado pela REGRESSAO LOG-LINEAR sobre y_i = e_i - e_nucleo (= k_i^p/|v|); E7 novo no motor:
  6 000 matrizes exatas de posto um (d de 8 a 64; p = 1/2 e 1; 1 200 com k quase iguais): pior erro relativo de beta %.1e e de p %.1e (limites %.0e e %.0e).
  O N3 alinhado: o texto e o codigo pedem a lei injetada recuperada (p e beta) E a lei-raiz rejeitada.
2 (hash do trabalhador): ACOLHIDO -- worker_sha256 DENTRO da especificacao congelada; o trabalhador recusa (WORKER_HASH_MISMATCH) se o proprio hash for outro;
  --spec-sha256, --beta-hex e --run-id obrigatorios no modo run; o um.py materializa byte a byte (bytes, nao texto).
3 (tokens): ACOLHIDO -- a linha do estatuto reescrita sem os tokens; o gerador recusa congelar se a guarda das tres palavras achar alguma no texto.
4 (o desvio do plano B): ACOLHIDO -- declarado no pre-registro (campo desvio_do_plano_B, com a razao medida e os limites por regra de tres) e LEVADO AO OPERADOR
  para ratificar; T2 em d = 64 restaurado a 96 pontos; T1 reestruturado (ruido so num subconjunto) para d = 32: 200 e d = 64: 20.
5 (N2): ACOLHIDO -- N2 vira IDENTIDADE (residuo de S vec(I/d) relativo <= 1e-12); status e gap da parte unital relatados como informacao.
6 (o token do T1): ACOLHIDO -- T1_INSTRUMENT_RECOVERS_INJECTED_LAW_BLIND / T1_INSTRUMENT_DOES_NOT_RECOVER_INJECTED_LAW.
7 (arquivos velhos): ACOLHIDO -- marca unica (run_id) passada pelo um.py e conferida em result/progress/cpuref; pasta nova por rodada (o trabalhador recusa pasta
  com saidas de outra rodada, sem escrever nada); o filho da CPU grava so cpuref*.json; o pai confere o codigo de saida do filho e a marca.
8 (o reaproveitamento): ACOLHIDO -- ambiente com scipy e Python; o motor (E1..E7) roda de novo ao reaproveitar; so resultado COMPLETO vai ao cache; o conferidor
  da versao final e a custodia recusam selo com o pilar reaproveitado.
9 (orcamento e prazo): ACOLHIDO -- prazo CONGELADO na especificacao (execution.um_py_timeout_s = 4 h); excecao contida POR INSTANCIA (contada; >0 anula como
  INSTANCE_ERRORS); a margem x1,25 declarada como estimativa nao medida sob a carga do rito.
10 (o ramo do log): ACOLHIDO -- o gerador inteiro L^ e' reconstruido; ramo = tau*||(L^-L^dag)/2i|| < pi - 0,1 E Choi projetada de L^ >= -1e-9.
11 (identidades nao conferidas): ACOLHIDO -- as conferencias sao contadas por identidade; o veredito diz em quantas instancias do T4 TODAS foram conferidas.
12 (janelas e grade): ACOLHIDO -- janelas so com atrator UNICO; «ON_THE_GRID» no veredito e «na grade» no texto.
13 (D128): ACOLHIDO -- estados distintos (RAN; NOT_RUN_DEADLINE; NOT_RUN_ERROR_<tipo>; STARTED no parcial -> INTERRUPTED); RK4 com h = 0,002 e 5 000 passos,
  Spohn do D128 so como informacao.
14 (proveniencia): ACOLHIDO -- fontes por caminho e sha256 no pre-registro; a familia v5.0 excluida; os rotulos trocados ditos; o CCI por Tr(Pi rho) dito;
  o L_diss alternativo nao escolhido dito.
15 (o kernel no N1): ACOLHIDO -- IALDRhoStar.tgl_fix_iff (IALDRhoStar.lean:255) e ModularDephasingBridge.spectral_preserves_every_diagonal (:18), conferidos por grep.
16 (o sentido da janela das dobras): ACOLHIDO -- dito: n(c1) <= 3 sempre; a janela e' quase-pureza (PR <= d^(1/6)).
17 (pequenos): ACOLHIDO -- a CPU compara n(c1) e n(c2), nao n(c3); escrita atomica com novas tentativas; o parcial dentro do try; a VRAM registrada; o formato
  da especificacao materializada dito (o objeto SPEC em JSON canonico); o gerador confere o hash do trabalhador na sonda e no autoteste; PSD e residuo na lista.
ACHADO NOVO DA GERENCIA (depois da afericao, ao refazer a sonda): o cuSOLVER padrao do PyTorch 2.11 derruba o processo (violacao de acesso, 0xC0000005) em
  autovalores nao Hermitianos n = 64 (eig e eigvals); o MAGMA nao. A especificacao congela a escolha por tamanho (linalg.nonhermitian_eig_backend); os
  estresses estao no pre-registro por sha256.
Trabalhador congelado: %s; especificacao: %s; pre-registro JSON: %s.
""" % (time.strftime("%%d/%%m/%%Y %%H:%%M"), E7["max_beta_rel_err"], E7["max_abs_p_err"], E7["limit_beta"], E7["limit_p"], P["spec"]["worker_sha256"], P["spec_sha256"], h(PJ))
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
if b"DISPOSICOES DA GERENCIA SOBRE A 1a PASSADA" in raw:
    print("ja gravado"); sys.exit(0)
bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw + disp.encode("utf-8"); open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p)
assert open(p, "rb").read()[:len(raw)] == raw
print("AFERIDOR_v384.txt:", len(raw), "->", len(novo), "B; sha16", hashlib.sha256(novo).hexdigest()[:16])
