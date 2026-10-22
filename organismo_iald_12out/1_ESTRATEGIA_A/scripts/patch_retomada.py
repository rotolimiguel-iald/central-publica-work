import pathlib
p = pathlib.Path(r"C:\IALD\Central de Patentes\work\organismo_iald_12out\1_ESTRATEGIA_A\ESTRATEGIA_A.md")
lines = p.read_text(encoding="utf-8").split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **Kernel:**")]
assert len(idx) == 1, idx
nova = ("- **Retomada (13/10, 00:22, mesma sessão `6da8f00d`, após interrupção):** o texto acima estava completo às 20:35 de 12/10; "
        "nesta retomada só se fechou a higiene prometida — `fp_kernel_depois.txt` medido às 00:22:25 (`132088 c8c3ef7987b12353…`, idêntico ao de antes), "
        "`scripts\hashes.py` → `medidas\HASHES_ESTRATEGIA_A.json`, a projeção da memória ACOM (`project_02_out.json`, revisão 0) e a transition única. "
        "Nenhum número da folha foi alterado; esta linha é a única inserção.")
if any("Retomada (13/10" in l for l in lines):
    print("ja patched")
else:
    lines.insert(idx[0] + 1, nova)
    p.write_text("\n".join(lines), encoding="utf-8")
    print("patched; bytes", p.stat().st_size)
