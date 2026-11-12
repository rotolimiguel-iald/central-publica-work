# ORDEM KIMI H0DN-05 (11/11/2026) — conferir o pacote da emenda, pinar as linhas de estresse antigas, dar o recibo do vetor e objetar ao rascunho do pré-registro

**De:** gerência c1. **Para:** Kimi K3 Pro. **Túnel:** o operador entrega o caminho deste arquivo. **Nenhum vetor observado é avaliado nesta ordem.**

## §0 O que mudou desde a ordem 04

1. O achado da gerência (`ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md`, sha256 `0ad5b0286fe56dce1c76a0e3febab96f91cc38146e90a3dc6e4e26a15d86808b`; mensagem 007, sha256 `ba27cff3c971c7404c11fbc2d21287ff46664a5334f5653eb657d9bcfda6fdbe`): o vetor de 09/11 já é a variante `raw_MAS`; a colaboração resolve por pseudoinversa; a trava era da casa.
2. O operador decidiu EMENDAR a regra (fala por bytes em `work\cunhagens_13out\OPERADOR_11nov_vamos_emendar_a_regra_o_numero_corrige_a_frase_o_dado_ja_esta_la_verbatim.txt`, sha256 `36a95f2e5c958f875224f085397a5720a14236d220b08b34c9f2ffd9d64ffa11`) e ratificou o plano e o portão com os quatro números publicados (`OPERADOR_11nov_ja_passei_a_ordem_ao_kimi_concordo_com_tudo_verbatim.txt`, sha256 `132448426284a6843f1b53c75ab7e4b9b2033f09c5565cfabb217648e51f955d`).
3. **A Etapa 2 e os itens restantes da Etapa 1 da ordem 04 (sha256 `72ab3d8fd34f56368d43f6a3c59f2c2351bb3e5ceb98c9e1bed9c7d39fdbd5d0`) ficam SEM OBJETO e são ab-rogados**: a conferência das 72 identidades só poderia falhar, e a ponte aos fits, a prova do centro e a quantização deixaram de ser caminho para abrir.
4. O pacote da emenda está em `work\h0dn_bg1_v411_emenda_11nov\` (19 arquivos pinados em `artefatos\PINOS.json`, sha256 `cad7160ee22b18d6a05a714192fe88215d2903b076d1799bbf5c1786be424f18`). Foi construído por um agente, reexecutado pela gerência numa cópia isolada (matrizes iguais bit a bit) e revisto por revisor distinto; 18 testes, todos com vetores sintéticos.
5. O rascunho do pré-registro está em `work\h0dn_bg1_v411_emenda_11nov\EMENDA_E_PRE_REGISTRO_V411_rascunho.md` (sha256 `4c9146470f933007060c227122baa40c28d31d5adcdf920724988930e810e072`). Ainda não foi lido ao operador por inteiro nem pinado.

## §1 Proibições

- Não chamar `evaluate`, `abrir` nem o executor com vetor observado; não calcular estimativa, razão, Z ou H0 a partir do vetor.
- Não abrir `y_obs.npz`, salvo para o item 3 do §2, e ali só para somar hashes, sem imprimir valor nenhum.
- Não tocar o FREEZE_R2, a v410, nem o pacote da emenda (é só leitura; objeção vai por escrito).
- Escrever só em `work\h0dn_bg1_v410_09nov\kimi\ordem05\`.

## §2 O que entregar

1. **Conferência independente do pacote (só desenho).** Recalcular por código próprio os pesos do desenho de 242 linhas e dos três desenhos de âncora única e comparar com `artefatos\estimador_s0_v411.npz` (sha256 `6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617`): diferença máxima por matriz. Refazer as contas de `artefatos\ESPERADO_PELOS_AGREGADOS.json` (sha256 `47302eec3c17752dc3e54dca1f5a28c26abe1d7eb250c6fd33cd167fbc62b872`). Ler `codigo\abertura_v411.py` (sha256 `13f88cf8b8626b0ec5330aec5d0ddd3186aa73d5de271cb154fc26f0b5b5056b`) e `codigo\executar_abertura_v411.py` (sha256 `45869ac339ad9fc660b9362646a47c763684446f36dc6505e1e4af610de5736b`) contra as seções 3 a 7 do rascunho e apontar toda divergência entre texto e código.
2. **As linhas S1, S2 e S4 para o rito.** Para cada uma, ou (a) um estimador pinado no mesmo esquema das âncoras únicas do pacote (índices das linhas sobre a rede de 255, pesos 2×n, desvio do nulo, desvio da lei, D, e a covariância usada quando não for submatriz da publicada), com script e manifesto; ou (b) a declaração fundamentada de que a linha só existe como D de desenho. Sem vetor.
3. **Recibo do vetor, só com hashes.** Para o `y_obs.npz` de 09/11: o sha256 do arquivo; para a chave `y_uncentered`: tipo, forma e o sha256 de `tobytes()`; os sha256 dos arquivos de dados e do código da colaboração de que o vetor saiu; e a declaração de que o arquivo de configuração é o da análise de base. Nenhum valor impresso. A gerência fará uma segunda construção independente e comparará os hashes.
4. **Objeções ao rascunho do pré-registro.** Em especial: as tolerâncias do portão 1; a seção 5 (o que os agregados públicos deixam prever, dito antes); as três linhas de estresse novas; os diagnósticos de coerência; e a pergunta da mensagem 007 sobre a convenção da pseudoinversa no modelo primário.

## §3 Relato

Até 15 linhas, mais `ENTREGA_ORDEM05.json` com os pinos, o depósito na fila e o registro no Mapa. Perguntas ao operador nas quatro línguas dele, como de costume. Uma obstrução demonstrada também é resultado.
