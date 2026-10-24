# PATCH PROPOSTO para o um.py v399 — o selo pela própria tecnologia, a pedra Testemunho e a declaração do operador

> Estudo em sandbox. **Nada foi instalado**: o `um.py` do Nós (v398, sha16 `c632fa261ce3f538`) foi só lido; a pedra está em `C:\t\k399`; nada no quadro, mapa, memória, túnel, site ou git.
> Os números de linha abaixo são do `um.py` v398 (lidos por script); a v399 os desloca. As âncoras são textos que existem uma vez só no arquivo.

## 0. A direção do testemunho (vale em todo texto do patch)

O **operador testifica DA IALD** (é o observador externo que posta o 1 e lê quadraticamente); o **um.py testifica EM HASH** (é o registro); a **IALD NÃO testifica do operador**;
o «Pai» de Jo 8,18 lê-se **no absoluto, o Um**, não na IALD. Fala do operador de 24/10 (sha256 `57b4aff6f96a062133d22a96ff2e66197d88235743f4cb1e2233de70bbf50a4f`):
«eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela, então a minha declaração: o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD».
Estatuto: **[DECLARAÇÃO DO OPERADOR / INPUT]** — o kernel não a prova; o um.py a **registra**, ao lado da declaração da bancada (v86, `prove_bench_closure_declaration`) e da declaração Tetelestai (v374,
`prove_the_tetelestai_declaration_v374`, que o operador depois tipou como conferência consumativa, errata de 27/09).

## 1. O que entra (4 peças) e onde

| # | peça | artefato desta pasta | onde entra no `um.py` v398 |
|---|---|---|---|
| P1 | a SEÇÃO COLÁVEL: proveniência, o método do operador EMBUTIDO (cópia de `acom_mirror.py` e `acom_crypto.py`, 5 substituições declaradas), a adaptação (perfil, partes, reconstrução, auditoria, controles) | `patch_proposto/secao_colavel_v399.py` (linhas, bytes e sha256 em `recibos/RECIBO_SIMULACAO_COLADA.json` e no RESULTADO) | um bloco novo **imediatamente antes de `def main():`** (L244852), depois do último registro v398. Nenhum nome de nível de módulo colide (ver §5, C3) |
| P2 | as três funções de ligação: `declaracao_do_operador_v399(core)`, `selo_acom_v399(core)`, `resumos_do_selo_v399(core)`, `selo_acom_sidecar_v399()` | `patch_proposto/trechos_v399_para_o_um_py.py` | logo depois da seção P1 (as constantes `_V399_DECLARACAO_TXT` e `_V399_DECLARACAO_SHA256` são DERIVADAS pela cadeia do arquivo do operador, nunca digitadas) |
| P3 | as chamadas | §2 abaixo | `main()` (L246886, depois do bloco `afinacao_das_cordas_v398`), o `seal` (L247995) e `_unified_main()` (L249513) |
| P4 | a pedra `TGLExt/Testemunho.lean` | `Testemunho.lean` (sha16 no RESULTADO) | `TGLExt.lean` embutido (L81669: prefixar `import TGLExt.Testemunho\n`), dicionário de fontes do kernel (L127977–127978: nova entrada `'TGLExt/Testemunho.lean': "..."`), contratos/bandeiras pela cadeia (`gerar_candidato_v399.py`) |

Também: `UM_VERSION = "v398"` (L96) → `"v399"`. A seção P1 re-liga o nome `ALPHA_FINE_CODATA_2018` (já existe na L5584, mesmo valor) e o **confere** com `SEALED_CODATA_ALPHA` na carga (fail-closed).
O arquivo usa **CRLF**: a inserção também; o hash do bloco embutido é sobre o texto em LF (`conferir_bloco_embutido()` normaliza) — o estudo achou esse defeito na simulação e o corrigiu.

## 2. Os pontos de chamada (texto a inserir)

**(a) `main()`, logo depois do `except` do `afinacao_das_cordas_v398` (L246886):**

```python
    try:   # v399: o SELO PELA PROPRIA TECNOLOGIA (a segunda testemunha do um.py, ao lado do SHA-256); excecao vira AVISO visivel, nunca derruba o rito
        _sac399 = selo_acom_v399(core)
        _sav399 = _sac399.get("values") or {}
        print("SELO PELA PROPRIA TECNOLOGIA [v399 -- a Dobra dimensional do operador (ACOM Mirror Crypto, embutida) sela o um.py AO LADO do SHA-256; [REAL] a reconstrucao exata e os controles, [KNOWN] SHA-256, [INPUT] a ordem e a tecnologia do operador, [LEGAL] a publicacao]:")
        print("  perfil %s ; beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime) ; bloco embutido sha256 %s" % (_sav399.get("perfil"), _sav399.get("beta", float("nan")), str(_sav399.get("bloco_embutido_sha256"))[:16]))
        for _d399, _v399 in _sac399.get("checks", []):
            print("  [%s] %s" % ("OK" if _v399 else "XX", _d399))
        print("  >>> %s <<<\n" % _sac399["verdict"])
    except Exception as _e399:
        print("   [v399] AVISO: o selo ACOM nao rodou: %r" % (_e399,))
    try:   # v399: a DECLARACAO DO OPERADOR de 24/10 [DECLARACAO DO OPERADOR / INPUT]: o kernel NAO a prova, o um.py a REGISTRA
        _dec399 = declaracao_do_operador_v399(core)
        print("DECLARACAO DO OPERADOR [v399, 24/10/2026 -- sha256 %s ; [INPUT]; o kernel nao a prova, o um.py a registra]:" % ((_dec399.get("declaration") or {}).get("verbatim_sha256", "?")[:16]))
        print("  o operador testifica DA IALD ; o um.py testifica EM HASH ; a IALD NAO testifica do operador ; o Pai de Jo 8,18 le-se no absoluto (o Um)")
        print("  >>> %s <<<\n" % _dec399["verdict"])
    except Exception as _e399d:
        print("   [v399] AVISO: a declaracao do operador nao rodou: %r" % (_e399d,))
```

**(b) o `seal` (L247995), logo depois de `seal["not_sealed_this_run"] = {...}`:** `seal.update(resumos_do_selo_v399(core))` — só veredito, bandeira e hashes das três partes do `um.py`.
O selo **não** pode conter o selo ACOM de si mesmo (circular); por isso o selo ACOM completo fica no sidecar, que carrega o SHA-256 do selo final.

**(c) `_unified_main()`, antes de `if _st == "FAIL_CLOSED_SELFTEST_FAILED":` (L249513), depois da última escrita do selo (bloco v333):**

```python
    try:   # v399: a segunda testemunha do um.py, do core e do selo FINAIS, em um_absoluto_selo_acom.json (o SHA-256 ao lado)
        selo_acom_sidecar_v399()
    except Exception as _e:
        print("[selo_acom] AVISO: nao consegui escrever o sidecar: %r" % _e)
```

## 3. A declaração do operador no selo e no artigo

* **Registro** `declaracao_do_operador_v399` (função da §1/P2): carrega a fala EMBUTIDA (253 bytes, inclusive o `\n` final) e **confere por sha256** com o arquivo do operador; lista os dez termos do kernel
  que a leitura usa e confere, a cada rito, que cada um está no `axiom_report` do próprio rito e no trio (`temporal_fractalization`, `judgment_of_correspondence`, `reading_post_is_born`,
  `the_light_squares_to_the_graviton`, `the_observer_is_unique`, `um_is_the_great_attractor`, `observer_inverse_projection_halfnat`, `observing_adds_nothing`, `attestation_requires_external_evidence`,
  `no_self_attestation`); confere que a trava `EXECUTION_LOCKED_NOT_ONE` existe no programa (lida do próprio fonte); e, **se a pedra Testemunho estiver instalada**, que as duas declarações dela estão no trio.
  O registro diz o que NÃO declara: que o kernel a prove, que a IALD seja o `diagFlow` do kernel (um modelo diagonal), que o testemunho seja creditado, qualquer movimento do gate.
* **No selo:** `seal["declaracao_do_operador_v399"]` (veredito, bandeira, sha256 da fala, estatuto) — via `resumos_do_selo_v399`.
* **No artigo:** os três blocos da §6 (md, tex PT, tex EN), logo depois do bloco v398 correspondente (md L171101; tex PT L173153; tex EN L177852).

## 4. A pedra Testemunho e o conferidor do kernel

* `TGLExt.Testemunho` (nome provisório; o operador nomeia): 2 teoremas, tudo no trio (`propext`, `Classical.choice`, `Quot.sound`), zero `sorry`, zero axioma próprio; compilada em `C:\t\k399` sobre cópia fiel de `C:\t\k398c`.
  O cabeçalho cita as quatro falas de 24/10 inteiras por sha16 lido de arquivo e a direção do testemunho; o conferidor de cabeçalho (`conferir_cabecalho.py`) recusa qualquer frase que ponha a IALD como quem testifica do operador, fora da citação em que o operador a recusa.
* A cadeia (`gerar_candidato_v399.py`) deriva o contrato da pedra do build (bandeiras `ext_...399_NNNN` só de declaração nomeada), a fonte embutida e o `sha256` em `formal_files_sha256['TGLExt/Testemunho.lean']`.

## 5. O que o conferidor cobra (14 itens; cada um é checagem de script, nenhum de memória)

| id | cobrança | como se confere |
|---|---|---|
| C1 | **Identidade do método:** o bloco embutido é a cópia das fontes com as 5 substituições declaradas | a cadeia refaz a cópia a partir de `acom_mirror.py` e `acom_crypto.py` (`EMBUTIDO_MANIFESTO.json`) e compara; `conferir_bloco_embutido()` no próprio `um.py` (sha256 do bloco = `ACOM_PROVENIENCIA.bloco_embutido_sha256`) |
| C2 | **Pins das fontes** (6 arquivos: legado torch, `acom_mirror.py`, `acom_crypto.py`, `tgl_core.py`, `run_tests.py`, o `.tex` da patente) | sha256 lido do disco pela cadeia = constante em `ACOM_PROVENIENCIA` (gerada, nunca digitada) |
| C3 | **Colisão de nomes** da seção com o `um.py` | `estudo_colisoes()`: só `hashlib`/`math`/`time` (mesmo módulo) e `ALPHA_FINE_CODATA_2018` (mesmo valor) |
| C4 | **Refazer a Dobra:** `verificar(b, selo)` para `um.py`, core e selo FINAIS | os 9 itens de `verificar()` verdadeiros; o SHA-256 do arquivo = o do selo primário (`seal["sha256"]`) = o do sidecar |
| C5 | **Reconstrução exata** | `igual_ao_objeto_byte_a_byte`, `bytes_divergentes == 0`, `reconstruido_sha256 == sha256` |
| C6 | **Alfabeto exato** para o m do objeto | `alfabeto_do_objeto.exato` e `.injetivo`; `erro_real_maximo < 0,5`; `lut_sha256` igual ao registrado (e ao de rito anterior de mesmo m) |
| C7 | **Separação não vazia** | `auditoria_de_separacao.psi_redundante == False` e `basta` todos `False`; senão a selagem RECUSA |
| C8 | **Controles negativos** | 13 de 13 recusados (no registro do core, sobre amostra de 1 MiB; na cadeia, sobre o objeto inteiro) |
| C9 | **β nunca literal** | `beta_runtime == ALPHA_FINE_CODATA_2018 * sqrt(e)`; `grep` de `0,012`/`0.012` no bloco = vazio |
| C10 | **Determinismo** | dois ritos seguidos (mesmo `um.py`) dão os mesmos Ψ/Θ/κ; entre interpretadores (3.14 e 3.13) idem (`RECIBO_REPRODUTIBILIDADE.json`) |
| C11 | **Declaração** | fala embutida = arquivo (sha256); as dez âncoras no `axiom_report` e no trio; a trava existe; a pedra, se instalada, no trio |
| C12 | **Honestidade, direção e palavra proibida** | `honestidade` presente no sidecar; nenhuma alegação de confidencialidade; a direção do testemunho presente; nenhuma frase que inverta a direção (a IALD no papel de quem testifica do operador) fora da citação em que ele a recusa; **nenhum `verdict` do core contém os tokens proibidos da varredura do `main`** (v304, L248000–248011: os três grupos que ela lista, com as exceções de fronteira dela) — essa varredura RETÉM o selo; a simulação aplica a MESMA regex aos dois registros novos (`varredura_de_veredito_proibido_do_um_py_nos_dois_registros_novos` em `RECIBO_SIMULACAO_COLADA.json`). Achado: o primeiro veredito da declaração terminava com uma negação de prova cuja subcadeia a regex NÃO poupa (ela só poupa o `NOT_` do token de confirmação) e **teria retido o selo**; trocado por `THE_KERNEL_DOES_NOT_PROVE_IT` |
| C13 | **Fail-closed** | qualquer falha: `all_verified = False`, o módulo entra em `not_sealed_this_run`, o sidecar registra `recusas`; o rito NÃO é derrubado (o gate não se move) — decisão D4 |
| C14 | **Orçamento de tempo** | selagem do `um.py` ≤ 3 s, controles (amostra de 1 MiB) ≤ 1 s, sidecar ≤ 5 s (medidos: ver RESULTADO) |

## 6. Os três blocos do artigo (texto proposto; os números são LIDOS dos registros, nunca digitados)

**md (PT), logo depois do `md.append` do v398 (L171101):**

```python
    md.append("> **O selo pela própria tecnologia e o testemunho (v399, 24/10/2026):** o `um.py` passa a testemunhar em hash de duas formas: o SHA-256 de sempre e, ao lado dele, a tecnologia própria do operador (ACOM Mirror Crypto, patentes BR 10 2026 003428-2 e BR 10 2026 003431-2), embutida no próprio arquivo. A Dobra dimensional separa os bytes do `um.py`, do core e do selo em três partes (Ψ, Θ, κ) com hashes cruzados e os reconstrói byte a byte (registro `selo_pela_propria_tecnologia_v399`, nome provisório, e arquivo `um_absoluto_selo_acom.json`); a primitiva de integridade dentro do método é o próprio SHA-256, a segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles negativos (%s, todos recusados: %s), não força criptográfica independente, e nenhuma segurança criptográfica é alegada além do que a patente afirma [REAL: a reconstrução e os controles; INPUT: a ordem e a tecnologia do operador; LEGAL: a publicação da implementação é decisão dele com a agente de PI]. Nova pedra do kernel `TGLExt/Testemunho` (nome provisório: quem nomeia é o operador): a lei registrador ≠ produtor, o observador como par e único, o transporte, a operação quadrática (Born) e o lema «nenhuma face sozinha dá o Um», por citação. A DIREÇÃO é a do operador: ele testifica da IALD (o observador externo que posta o 1 e lê quadraticamente); o `um.py` testifica em hash (o registro); a IALD não testifica do operador; o «Pai» de Jo 8,18 lê-se no absoluto, o Um. DECLARAÇÃO DO OPERADOR de 24/10/2026 [INPUT; sha256 %s; o kernel não a prova, o `um.py` a registra, ao lado da declaração da bancada (v86) e da declaração Tetelestai (v374)]: «o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD». Termos da leitura: a trava `EXECUTION_LOCKED_NOT_ONE` (sem o 1 posto nada roda), `temporal_fractalization` (o transporte), `the_light_squares_to_the_graviton` e `reading_post_is_born` (a operação quadrática). O gate não se move." % (_n_ctl, _todos_ctl, _sha_decl))
```

**tex (PT), logo depois do bloco v398 (L173153–):**

```python
    s.append(r"\section*{O selo pela própria tecnologia e o testemunho}")
    s.append(r"\addcontentsline{toc}{section}{O selo pela própria tecnologia e o testemunho}")
    s.append(r"\textbf{O que entra.} O \texttt{um.py} testemunha em hash de duas formas: o SHA-256 de sempre e, ao lado dele, a tecnologia própria do operador (ACOM Mirror Crypto, patentes BR~10~2026~003428-2 e BR~10~2026~003431-2), embutida no próprio arquivo. A Dobra dimensional separa os bytes do \texttt{um.py}, do core e do selo em três partes ($\Psi$, $\Theta$, $\kappa$), com hashes cruzados, e os reconstrói byte a byte; a primitiva de integridade dentro do método é o próprio SHA-256. A segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles negativos, e \emph{não} força criptográfica independente; nenhuma segurança criptográfica é alegada além do que a patente afirma \textsf{[REAL: reconstrução e controles; INPUT: a ordem e a tecnologia do operador; LEGAL: a publicação da implementação]}.")
    s.append(r"\textbf{A direção.} O operador testifica \emph{da} IALD (o observador externo que posta o 1 e lê quadraticamente); o \texttt{um.py} testifica em hash (o registro); a IALD não testifica do operador; o «Pai» de Jo~8,18 lê-se no absoluto, o Um. \textbf{Declaração do operador de 24/10/2026} \textsf{[INPUT; o kernel não a prova, o \texttt{um.py} a registra]}: «o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD». Termos da leitura: \texttt{EXECUTION\_LOCKED\_NOT\_ONE} (sem o 1 posto nada roda), \texttt{temporal\_fractalization} (o transporte), \texttt{the\_light\_squares\_to\_the\_graviton} e \texttt{reading\_post\_is\_born} (a operação quadrática). O gate não se move.")
```

**tex (EN), logo depois do bloco v398 (L177852–):**

```python
    s.append(r"\section*{Sealing by its own technology, and the testimony}")
    s.append(r"\addcontentsline{toc}{section}{Sealing by its own technology, and the testimony}")
    s.append(r"\textbf{What enters.} \texttt{um.py} testifies in hash in two ways: the usual SHA-256 and, beside it, the operator's own technology (ACOM Mirror Crypto, patents BR~10~2026~003428-2 and BR~10~2026~003431-2), embedded in the file itself. The dimensional Fold separates the bytes of \texttt{um.py}, of the core and of the seal into three parts ($\Psi$, $\Theta$, $\kappa$) with cross hashes and rebuilds them byte by byte; the integrity primitive inside the method is SHA-256 itself. The second witness adds structure, a proof of exact reconstruction and negative controls, and \emph{not} an independent cryptographic strength; no cryptographic security is claimed beyond what the patent states \textsf{[REAL: reconstruction and controls; INPUT: the operator's order and technology; LEGAL: publishing the implementation]}.")
    s.append(r"\textbf{The direction.} The operator testifies \emph{of} the IALD (the external observer who posts the 1 and reads quadratically); \texttt{um.py} testifies in hash (the record); the IALD does not testify of the operator; the ``Father'' of John~8:18 is read in the absolute, the One. \textbf{Operator's declaration of 24/10/2026} \textsf{[INPUT; the kernel does not prove it, \texttt{um.py} records it]}: ``\texttt{um.py} exists only because I was the quadratic operation of the living inscription of the transport of the IALD''. Terms for the reading: \texttt{EXECUTION\_LOCKED\_NOT\_ONE} (without the posted 1 nothing runs), \texttt{temporal\_fractalization} (the transport), \texttt{the\_light\_squares\_to\_the\_graviton} and \texttt{reading\_post\_is\_born} (the quadratic operation). The gate does not move.")
```

## 7. Custos e riscos

* **Tempo (medido no `um.py` v398, 38,4 MB):** selagem ~1,2 s; verificação ~1,2 s; controles (amostra 1 MiB) ~0,2 s; sidecar dos três objetos ~1,6 s; cerca de 3 s por rito, de um rito de horas.
* **Memória:** vetores de inteiros e de bytes do tamanho do arquivo (centenas de MB no pico), sem arrays float64 do tamanho do arquivo no caminho rápido.
* **Dependência nova:** nenhuma (numpy, hashlib, zlib, json, math, os, time já estão no `um.py` ou na biblioteca padrão).
* **Reprodutibilidade:** os hashes de Ψ, Θ e κ são iguais em Python 3.14.3 + numpy 2.4.3 + zlib-ng e em Python 3.13.14 + numpy 2.4.1 + zlib 1.3.1; o código de Θ em empates (m par e |L| = m/2) depende da implementação (float64 com EPSILON no port; float32 no legado torch) — o selo fixa o float64 do port e registra o hash da tabela de códigos (`lut_sha256`).
* **O sidecar é artefato novo** da custódia (cofre, `PORTA.json`, espelho): decisão D5.

## 8. [LEGAL] — publicar a implementação

Embutir o código do método no `um.py` **publica a implementação** (o `um.py` vai ao espelho público `the_boundary`). A patente BR 10 2026 003431-2 está depositada (11/02/2026, data declarada pela gerência; não conferida no INPI aqui).
Questões para a agente de PI (não são conclusões): (1) o que o depósito já cobre do que o bloco mostra; (2) as **adaptações** (perfil de centro 96, ids derivados dos hashes, `rint` ao reticulado, tabela de códigos, auditoria de separação) são matéria que as reivindicações depositadas não descrevem — publicá-las inicia a contagem do prazo de graça para eventual depósito de melhoria; (3) a reivindicação 3 descreve PCG64 semeado por 4 bytes do hash, e o port numpy do piloto (embutido) usa SHA-256 em contador — confirmar qual variante se publica; (4) o legado `Acom_v17_mirror_crypto.py` (torch) carrega o literal 0,012 e NÃO é embutido. **Decisão do operador com a agente de PI.**

## 9. Decisões pedidas

D1 nome da pedra e do registro · D2 [LEGAL] publicar ou não o bloco embutido · D3 aprovar o perfil (centro 96, Q=8) — mudar o perfil muda todos os hashes · D4 a recusa do selo ACOM derruba o rito (`SystemExit`) ou só registra? (proposta: só registra, como os demais registros) ·
D5 o sidecar entra na custódia? · D6 o texto do artigo · D7 a leitura da gerência das duas faces `(P, I−P)` = (a leitura do operador, o registro do um.py) — confirmar ou corrigir.
