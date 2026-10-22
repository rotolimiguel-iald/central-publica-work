# Remove só a pasta parcial do cofre v394 criada pela 1ª execução (falhou por caminho longo). Prefixo \\?\ para caminhos longos.
import os, shutil
V = r"C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v394"
KV = r"C:\IALD\Central de Patentes\vault\originals_copy\tgl_kernel_v394"
assert not os.path.exists(KV), "o kernel v394 já existe: não era parcial"
assert not os.path.exists(os.path.join(V, "CUSTODY_MANIFEST.json")), "o manifesto existe: não era parcial"
shutil.rmtree("\\\\?\\" + V)
print("parcial removida:", not os.path.exists(V))
