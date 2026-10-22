"""Apply independent reviewers' scope clarifications to our own reporter safely."""
from pathlib import Path
from datetime import datetime
import os

folder = Path(__file__).resolve().parent
path = folder / "finalize_reexamination.py"
assert folder.parent == Path(r"C:\IALD\Central de Patentes\Chatgpt")
before = path.read_bytes()
backup = path.with_name(path.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as stream:
    stream.write(before)
    stream.flush()
    os.fsync(stream.fileno())
assert backup.read_bytes() == before
text = before.decode("utf-8")
changes = [
    ("A testemunha de um vínculo prova que o cociclo não é identicamente 1;",
     "Para a escolha de um vínculo `singleBondData`, a testemunha prova que o cociclo não é identicamente 1;"),
    ("**A transformação finita de Einstein foi deduzida.** Para uma mudança suave invertível",
     "**A transformação finita de Einstein foi deduzida.** O resultado trata de métrica Lorentziana suave em dimensão quatro, com Levi-Civita sem torção. Para uma mudança suave invertível"),
    ("usando infinitas observações exatas; falta a correspondência operacional",
     "usando informação exata infinita, codificada por amostras densas e cortes racionais, em cada domínio/carta; falta a correspondência operacional"),
    ("O teorema de reconstrução do caráter já devolve os campos e a equação de Einstein quando as hipóteses de área, conservação e regularidade são satisfeitas.",
     "O teorema de reconstrução do caráter já devolve os campos e a equação de Einstein para parâmetro do caráter t ≠ 0, domínio aberto não vazio preconexo, registro admissível, telas e η ≠ 0, quando as hipóteses de área, conservação e regularidade são satisfeitas."),
    ("e lei de Einstein nas sobreposições métricas abertas.",
     "e lei de transformação de Einstein nas sobreposições métricas abertas."),
    ("O limite em número de sítios com potencial limitado não é, por si, uma construção do limite ultravioleta relativista.",
     "Os vínculos XX entre si comutam; a interação atestada envolve observáveis locais. O limite em número de sítios com potencial limitado não é, por si, uma construção do limite ultravioleta relativista."),
]
for old, new in changes:
    assert text.count(old) == 1, old
    text = text.replace(old, new)
after = text.encode("utf-8")
assert len(after) > len(before)
compile(text, str(path), "exec")
temp = path.with_name(path.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
with temp.open("xb") as stream:
    stream.write(after)
    stream.flush()
    os.fsync(stream.fileno())
assert temp.read_bytes() == after
assert path.read_bytes() == before
os.replace(temp, path)
assert path.read_bytes() == after
print("Independent review clarifications applied atomically; no report or um.py executed.")
