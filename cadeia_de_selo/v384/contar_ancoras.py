import sys
sys.stdout.reconfigure(encoding="utf-8")
T = open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py", encoding="utf-8", newline="").read()
anc = {
 "inscricao": '    print("Iniciando desconstrucao fractalizada: 1 -> 1/2 -> beta -> borda -> massa\n")\r\n',
 "kernel": "    materialize_embedded_kernel()   # v31: o kernel nasce DESTE arquivo\r\n",
 "regua_pt": '    s.append(r"\section*{Régua: o que cada coisa é}")\r\n',
 "ruler_en": '    s.append(r"\section*{Ruler: what each thing is}")\r\n',
 "v383_print": '    print("   [v383] o livro de cobrancas',
 "seal_v383": '            "the_ledger_of_charges_reading_v383": ',
 "um_version": 'UM_VERSION = "v383"',
 "rt383_first": open(r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v383\v383_runtime.py", encoding="utf-8").read().splitlines()[0],
 "pt383_first": open(r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v383\artigo_pt_v383.pysnip", encoding="utf-8").read().splitlines()[0],
}
for k, a in anc.items():
    print(k, T.count(a))
print("CRLF linhas:", T.count("\r\n"), "LF soltos:", T.count("\n") - T.count("\r\n"))
print("re importado:", "\nimport re" in T or "import re\r\n" in T or ", re," in T[:5000])
