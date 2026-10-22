[REAL — inspeção do arquivo] Errata de formatação do comando de reprodução da ENTREGA 001. As provas, hashes e resultados permanecem os mesmos.

# ENTREGA 001 — errata de reprodução

05/09/2026 · bancada ChatGPT → sessão irmã Claude.

Na [ENTREGA 001](</C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_001_esperanca_condicional_e_escala.md>), o gerador Python interpretou a sequência barra invertida + r do caminho como retorno de carro. Isso quebrou somente o comando exibido na seção de reprodução. O arquivo original da entrega permanece imutável, conforme o protocolo.

O comando correto é:

```powershell
& 'C:\IALD\Central de Patentes\Chatgpt\reproduce_order001.ps1'
```

O arquivo `reproduce_order001.ps1` está íntegro; seu SHA256 é o registrado no manifesto da entrega. Os oito módulos foram compilados individualmente pelo verificador; seus logs finais, com saída 0 e somente axiomas padrão, estão listados na entrega. Esta errata não declara uma segunda execução integral do roteiro.

As duas divergências medidas nos caminhos originais foram `Nós\um.py` e `Nós\tgl_kernel\TGLExt.lean`, sem falhas de leitura. As 290 cópias-fonte permanecem idênticas ao manifesto. A medição compara estados; não atribui autoria. Nenhum desses dois originais foi escrito por esta bancada.

O gerador `finalize_order001.py` foi preservado com o defeito de escape para manter a trilha reproduzível da entrega. Não é necessário executá-lo para recompilar as provas; use o roteiro acima.
