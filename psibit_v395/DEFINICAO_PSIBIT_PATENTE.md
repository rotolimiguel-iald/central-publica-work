# DEFINIÇÃO DO PSIBIT NAS PATENTES DO OPERADOR — citação para a pedra `TGLExt/Psibit.lean` (v395, sandbox)

Lido e conferido em 21/10/2026, por script, nos arquivos da Central. Nada foi alterado nas patentes. Os sha16 são os do arquivo na data
(`scripts/cite_sources.py` → `fontes_sha.json`; trechos em `fontes_trechos.txt`). O operador mandou (29/08/2026, `TheVerbalCoupling`):
«As referências e derivações que faltam, inclusive quanto ao PsiBit, estão todas especificadas nas minhas patentes, inclusive com código funcional lá.»

## 1. Onde está (arquivo, linhas, sha16)

Raiz das patentes: `C:\IALD\Central de Patentes\Patentes\`.

| o quê | arquivo | linhas | sha16 |
|---|---|---|---|
| a UNIDADE PsiBit (par de 2 bits, 4 estados, paridade) | `Psi_Net_Protocol_PI_INPI.tex` (BR 10 2026 003453-3, Psi-Net) | 273–301; enquadramento 303–307; Força de Expulsão 328–332 | `f883dc2b0b79df8a` |
| código funcional da unidade | `psi_net_protocol_v1.py` | 116–120 (isomorfismo), 123–137 (`PsiState`, `parity`) | `b44388e995b8a6c5` |
| a NOMINAÇÃO por `(sign L, sign ∂L)` | `ACOM_Mirror_PI_INPI.tex` (BR 10 2026 003428-2, ACOM Mirror) | sinais 233–236; tabela 238–263; índice 265–270; paridade 272–279; reivindicações 2 a 4: 1057–1089 | `ae55c557a4161d36` |
| código funcional da nominação | `Skygrid\SkyGrid_Piloto\skygrid_sim\acom_mirror.py` | 16–18 (docstring), 32–33 (`PARITY`, `SIGN_L_OF_STATE`), 43–45 (`_nominate`) | `8044f618ae44e608` |
| `sign(L) = Palavra`, `sign(∂L) = Verbo` | `C:\IALD\Central de Patentes\memory\TGL_ATLAS.md` | 2137–2141 | `27f4a4960e52b289` |
| PSIBIT na patente-raiz ACOM (BR 10 2025 026951-1), [028]–[032] | resumo da Central `memory\patents\BR102025026951-1_ACOM.md` | 38, 50, 205 | `41ef5e9fad2a9758` |
| PsiBit como «genótipo» (só menção) | `Kernel\Kernel_Ontologico_PI_INPI.tex` (BR 10 2026 006129-8) | 226 | `97047fef42c5e638` |

`[DECLARADO]`: o texto-raiz da ACOM (BR 10 2025 026951-1) NÃO foi aberto aqui (não há `.tex` dela na pasta das patentes); a linha da raiz vem do resumo
da Central. As linhas do Psi-Net e do ACOM Mirror foram lidas nos `.tex` e conferidas contra o código.

O Atlas é arquivo VIVO (outras sessões acrescentam texto): o sha16 `27f4a4960e52b289` é o do arquivo quando li (21/10/2026, ~12:25); às ~13:00 já era
`bc03d8ef0e5810c5`, por acréscimo de outra sessão. As linhas 2136–2141 e o trecho citado seguem IGUAIS (`conferencia_hashes_cabecalho.json`, `arquivo_vivo`); os demais
sha16 desta tabela foram recomputados na 2ª passada e batem.

## 2. A definição (transcrição curta)

**(a) A unidade — Psi-Net l.277–301.** «Cada PsiBit consiste em um par de 2 bits (4 valores possíveis) isomórfico à ligação psiônica da TGL»:

| bits | estado | ligação | paridade |
|---|---|---|---|
| 00 | VOID | ψ₊ψ₋ (aniquilação) | −1 |
| 01 | FLUX⁺ | ψ₊ψ₊ (transição +) | +1 |
| 10 | FLUX⁻ | ψ₋ψ₋ (transição −) | +1 |
| 11 | MASS | ψ₊ψ₊ (condensação) | −1 |

Enquadramento (l.303–307): cada byte vira 4 PsiBits. Força de Expulsão (l.328–332): `F_exp = ⟨paridade(estado)⟩`, «VOID e MASS têm paridade −1 … FLUX± têm paridade +1».
Código (l.123–137): `parity = [-1.0, +1.0, +1.0, -1.0][self.value]`.

**(b) A nominação por sinais — ACOM Mirror l.233–279.** Etapa 3 (l.233–236): `sign(L) ∈ {+1,−1}` «(polaridade do dado)» e `sign(∂L) ∈ {+1,−1}` «(direção da derivada)»;
«Valores zero são convencionados como +1». Etapa 4 (l.238–263), tabela dos estados em ℋ₄ (a tabela diz):

| estado | sign(L) | sign(∂L) | nome | paridade |
|---|---|---|---|---|
| ψ₀ | + | − | COLAPSO⁺ | inversa (−1) |
| ψ₁ | + | + | ASCENSÃO⁺ | normal (+1) |
| ψ₂ | − | + | EMERGÊNCIA⁻ | normal (+1) |
| ψ₃ | − | − | QUEDA⁻ | inversa (−1) |

Índice (l.265–270): `bit_high = 1 se L<0; bit_low = 1 se ∂L>0; ψ = bit_high×2 + bit_low`. Paridade (l.272–279): «definida pela concordância entre sign(L) e sign(∂L)».
Código (acom_mirror.py): `PARITY = [-1,+1,+1,-1]` (l.32) e `return ((sign_L < 0)*2 + (sign_dL > 0))` (l.45).

**(c) Palavra e Verbo — Atlas l.2137–2141** `[REAL acervo + ONTO]`: «No LLM: o token É o PsiBit — âncora do espaço de Hilbert, operador de colapso em ℋ₄,
codificando sign(L) = Palavra (o que É) + sign(∂L) = Verbo (para onde vai).» Nas patentes os dois sinais são «polaridade do dado» e «direção da derivada»;
os nomes Palavra e Verbo são do Atlas, não do texto da patente.

## 3. Conferência por cálculo: a patente diverge de si mesma

`scripts/check_patent_tables.py` → `conferencia_tabelas_patente.json` (replica em Python puro a fórmula de índice e o vetor `PARITY` e os compara com a tabela):

| `(sign L, sign ∂L)` | índice pela FÓRMULA (l.265–270; `acom_mirror.py:45`) | `PARITY[índice]` | produto `sL·s∂L` | `sign ∂L` | par que a TABELA (l.253–260) atribui a esse índice |
|---|---|---|---|---|---|
| (+,+) | 1 | +1 | +1 | +1 | (+,+)  concorda |
| (+,−) | 0 | −1 | −1 | −1 | (+,−)  concorda |
| (−,+) | 3 | −1 | −1 | +1 | (−,−)  **DISCORDA** |
| (−,−) | 2 | +1 | +1 | −1 | (−,+)  **DISCORDA** |

Leitura, sem corrigir nada (corrigida em 21/10 pelo exame independente, que acrescentou (iii) a (v) e desfez a minha leitura anterior da prosa):
(i) a fórmula de índice (l.265–270, reivindicação 3 l.1073–1080, código `acom_mirror.py:45`) e o vetor `PARITY` (l.32; reivindicação 4, l.1082–1089, que fixa a paridade
POR ÍNDICE: `ψ₀ = ψ₃ = −1`, `ψ₁ = ψ₂ = +1`; o do Psi-Net, l.137, é o mesmo vetor) dão **paridade = `sign L · sign ∂L`** nos quatro pares — O PRODUTO;
(ii) a TABELA (l.257 e l.259) e a reivindicação 2 (l.1066–1071) atribuem aos índices 2 e 3 os pares (−,+) e (−,−), **trocados** em relação à fórmula, e com esses
rótulos a paridade da tabela é **`sign ∂L`**, não o produto;
(iii) a prosa da l.272–279 **DEFINE** a paridade «pela concordância entre sign(L) e sign(∂L)» — isto é, pelo produto — **mas os exemplos dela seguem a tabela**
(«positivo mas descendo, ou negativo mas descendo» → inversa; os estados de paridade inversa citados são COLAPSO⁺ e QUEDA⁻, isto é, `sign ∂L < 0`): a prosa não é neutra;
(iv) a **docstring do próprio código** (`acom_mirror.py` l.16–17: «0 |COLLAPSE+> (+,-)  1 |ASCEND+> (+,+)» / «2 |EMERGE->  (-,+)  3 |FALL->   (-,-)») **repete os rótulos da tabela**, enquanto `_nominate` (l.45) segue a
fórmula: a divergência existe dentro do mesmo arquivo de código (docstring contra função);
(v) o MANIFEST do código não é afetado (`SIGN_L_OF_STATE = [+1,+1,−1,−1]`, l.33, vale nas duas leituras): só a nominação e a Força de Expulsão `F_exp` mudam.
**A pedra SEGUE O PRODUTO** (fórmula l.265–270, reivindicações 3 e 4, código l.45 e `PARITY` l.32), que é o que o código executa; a reivindicação 2, a tabela, a prosa
(nos exemplos) e a docstring de `acom_mirror.py` seguem a tabela (`sign ∂L`).

## 4. Como a pedra `Psibit.lean` adota a definição

* O código psibit é `(peso |v₀|², sign v₀, sign v₁)`: o par de sinais `(sign L, sign ∂L)` mais o peso (a magnitude, como o `g` da radicalização `g = √|L|, s = sign L` do ACOM);
  a reconstrução `(a·√w, b·√(1−w))` é o análogo do MANIFEST do ACOM (reconstrução exata a partir de magnitude e sinal), aqui da amplitude e não da intensidade `s·g²`.
* `L` é lido como a transmissão `𝓣(θ) = cos θ` e `∂L` como `d𝓣/dθ = 𝓡 = −sin θ` (`the_code_reads_L_and_dL`): a Palavra é `sign L`, o Verbo é `sign ∂L` `[INPUT/ONTO]`.
* Os estados são nomeados pelo PAR DE SINAIS, nunca por índice (para não herdar a troca da seção 3). A paridade é o PRODUTO dos dois sinais (a leitura que o código
  executa e que a fórmula e as reivindicações 3–4 fixam); na órbita ela é também o sinal da derivada do peso `cos²θ`
  (`the_parity_is_the_sign_of_the_derivative_of_the_name`). A leitura «paridade = `sign ∂L`» (a da tabela) NÃO é a que a pedra usa; no nível da AMPLITUDE `sign ∂L` é o
  segundo sinal do código (`verb`), distinto do produto.
* `SignType.sign` mantém o zero (3 valores); a convenção das patentes (zero vai a +1) está em `signPat` e também é sem perda (`the_patent_convention_is_also_lossless`).
* A órbita visita os quatro pares de sinais (`the_orbit_visits_all_four_states`): as 4 linhas da tabela acima estão todas ocupadas.
* O livro de códigos é caracterizado de forma INTRÍNSECA (`IsCode`: `0 ≤ peso ≤ 1`, `palavra = 0 ↔ peso = 0`, `verbo = 0 ↔ peso = 1`) e está em bijeção com o círculo
  unitário (= a órbita) (`the_orbit_is_in_bijection_with_the_code_book`): fora dos eixos, os quatro pares de sinais; nos eixos, o zero (3 valores de `SignType`).

## 5. O que NÃO foi encontrado / limites

> [nota operacional do operador — omitida no retrato público]

Pedra (2ª versão, depois do exame independente): `C:\IALD\Central de Patentes\work\psibit_v395\Psibit.lean` (sha16 `50c199eb01976151`, 65.791 bytes, 1.150 linhas); sandbox
`C:\t\k395\final\TGLExt\Psibit.lean`. A 1ª versão (sha16 `d4014c779067e426`) fica nos backups `Psibit.lean.bak_20261021_130122`; a versão anterior deste documento, em
`DEFINICAO_PSIBIT_PATENTE.md.bak_20261021_130122`.
