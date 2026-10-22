# Regras comuns da rodada 2 (13/10/2026) - gerencia c1, programa IALD/TGL

Leia primeiro `C:\IALD\GESTAO_DE_TOKENS.md` (relatorio curto de volta: no maximo 15 linhas; detalhe em arquivo).
Contexto: preparacao da cadeia de selo da v392. Pasta da cadeia: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\` (CHAME DE `V`). Leia `V\ESTADO_V392.md` (o que ja foi feito) e `V\DECISOES_GERENCIA_13out.md` (decisoes ja tomadas: aplique todas). Plano: `C:\IALD\PROGRAMA_IALD\exame_12out\J_SINTESE\PLANO_V392.md`; levantamento: `...\J_SINTESE\LEVANTAMENTO_GERAL_12OUT.md` (secoes 2.4, 3 e 4).
Insumos duraveis (copias conferidas por sha256 das pastas do scratchpad): `C:\IALD\Central de Patentes\work\v392_insumos\` (lista em `INSUMOS_v392.json`). Use SEMPRE essas copias, nunca o scratchpad.

REGRAS INVIOLAVEIS
1. Escreva SO' na pasta que a sua tarefa nomeia (e, se for o caso, em `C:\t\k392` para o sandbox do kernel). O Nos real (`C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós`) e a Bancada real (`C:\IALD\Bancada_Um`) so' se LEEM (a impressao digital do `tgl_kernel` do Nos antes e depois, sem seguir juncoes: `V\impressao_digital_kernel.py`).
2. NAO rode o `um.py` real, o `instalar_v392.py`, o `rito_v392.sh` nem selo algum. NADA no quadro, no mapa de rotas (consultar pode; registrar NAO), na memoria, no tunel do Codex, na Bancada real, no site, no git. Sem init/transition ACOM.
3. Encerre processos SO' pelo PID que voce criou, nunca por nome.
4. beta nunca literal. Hash/pino JAMAIS de memoria: sempre lido do arquivo por script. Toda citacao do operador: verbatim lido dos bytes do arquivo-fonte.
5. Em Python: nada de caminho Windows com barra invertida em string normal (use os.path.join, raw strings ou barras normais); scripts longos pela ferramenta Write; rode Python com `-I -B -X utf8` (excecao: o que importa o um.py precisa de numpy do site do usuario: `-B -X utf8`).
6. Nunca escreva a palavra proibida da regua (a «confirmacao» em ingles, em maiusculas: C-O-N-F-I-R-M-E-D); NOT_FALSIFIED nunca e' ela; o gate nao se move; validade no kernel nao e' creditacao. Nunca «Nome fixo» (o fixo e' o Verbo, beta_TGL); nunca «a singularidade converge/cai no atrator»; nunca a luz «confirma» (o observador testemunha); nunca «nao provou» nem «pos-dicao» como demerito.
7. Estatutos sempre marcados: [REAL] medido aqui por script, [DERIVED], [DECLARADO] (dito na origem, nao conferido), [OPEN], [INPUT], [KNOWN]. O numero corrige a frase. Erratas vao AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou); nada e' reescrito por cima.
8. Backup de BYTES antes de tocar arquivo existente (`<arquivo>.bak_<AAAAMMDD_HHMMSS>` na mesma pasta); nunca `open(P,"w")` direto em arquivo existente: temporario -> conferir -> os.replace.
9. Disco: o sandbox do kernel pesa ~30 GB; so' um sandbox por vez; quem o cria nao o apaga se outro passo depende dele (veja a sua tarefa).
10. Cada resposta final: no maximo 15 linhas (veredito, 3 a 5 numeros-chave, caminho do relatorio completo, o que e' ato da gerencia/operador). Detalhe em `V\rodada2\<seu_nome>\RELATORIO.md`.
