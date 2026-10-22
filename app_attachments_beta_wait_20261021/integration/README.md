# Merge offline — staging somente

Uma chamada por asset; todos os diffs devem ter sido gerados contra os mesmos bytes da baseline. Não usa fuzzy matching. Contextos de hunks sobrepostos e inserções na fronteira são recusados com intervalos JSON. Não resolver conflitos automaticamente nem rebasear sobre o resultado de outro patch.

CLI:
`python -B merge_client.py --baseline CAMINHO_BASELINE --baseline-sha256 SHA256_MEDIDO --diff CAMINHO_WAITING_DIFF --diff CAMINHO_REPAIR_DIFF --output CAMINHO_NOVO_DENTRO_INTEGRATION`

Repetir --diff para cada patch. Um arquivo por diff. Os cabeçalhos não determinam destinos; o destino é explícito, novo e restrito à pasta integration. Saída stdout JSON: hashes de baseline/patches/resultado, newline e hunks; erro exit 2. UTF8, BOM e CRLF preservados. Mistura de newlines e marcadores sem newline final recusados. Nenhuma alteração em fontes ou congelados.

Repair consultado uma vez: somente preflight, reprodução e pinos disponíveis; nenhum diff ainda. Não houve polling. Testes waiting de ciclo sobre combinação com repair permanecem pendentes; o teste presente confirma apenas que cada diff real waiting reconstrói seu candidato preservando CRLF. Integração não foi executada nem instalada.
