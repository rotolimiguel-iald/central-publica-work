[REAL — registro autoral de falhas e correções]

Primeiro Lake build: rc=1. Os 44 fornecedores recompilaram; o módulo novo falhou em eom_at por associação do produto após simplificação, e em eom_rejects_changed_generator porque smul_right_injective requer primeiro o tipo do módulo. Correções locais: mul_assoc e argumento (X → Complex). Sem mudança das hipóteses ou dos enunciados. A tentativa integral e os snapshots estão em attempts/20260915_151902_028090.

Depois de salvar stdout/stderr/run.json, o wrapper Python tentou imprimir caracteres Unicode em console cp1252 e falhou com UnicodeEncodeError. O recibo do processo Lean já estava salvo e marca rc=1, não sucesso. Wrapper ajustado para stdout UTF-8. Nenhum log anterior foi apagado.

O Lake avisou sobre mudanças locais no cache aesop: git status da cópia mostra exclusão de lean_packages/std; o caminho ausente foi herdado da origem, a conferir no recibo. O cache é copiado, não checkout limpo reconstruído. Avisos de linter em fornecedores preexistentes ficaram preservados; sem saneamento de fontes fora deste escopo.

ERRATA AO LADO: a checagem encontrou lean_packages/std como DIRETORIO VAZIO existente na origem e ausente na copia. Portanto a frase anterior de ausencia herdada estava errada. O script havia copiado todos os arquivos, mas nao pastas vazias. A pasta vazia foi reproduzida exclusivamente na nova raiz e o recibo RESSALVA_CACHE_AESOP.json foi corrigido com backup. Isso nao altera fontes ou objetos da origem.

Segunda tentativa: fonte principal e controles compilados; auditor falhou porque pp.width nao e opcao reconhecida nesta toolchain. Opcao de apresentacao removida. As consultas aos axiomas foram reexecutadas em build com rc=0 antes de qualquer aceite autoral. O leitor Python normaliza sufixos de universo tambem nos nomes dos axiomas (os logs brutos os preservam).

Terceira tentativa concluida: Lake rc=0 em attempts/20260915_152955_280967/run.json. Principal, controles e auditor completos. A lista de axiomas sera validada pelo leitor, incluindo presenca de todos os nomes e normalizacao dos sufixos de universo. O aviso aesop nao se repetiu apos reproduzir o diretorio vazio.

Resultado efetivamente medido: o auditor Python terminou rc=0; 27 nomes presentes, axiomas normalizados subconjunto do trio; nove controles negativos rc=1 por Type mismatch e todas as paredes correspondentes presentes na auditoria. A conferencia das nove revisoes Git dos pacotes tambem passou.
