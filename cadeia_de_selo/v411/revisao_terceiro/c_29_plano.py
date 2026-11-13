import sys, os, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
sys.path.insert(0, V)
sys.dont_write_bytecode = True
import delta_v411 as DL
CEN = r"C:\IALD\Central de Patentes"
P = V
lst = [CEN + r"\work\cunhagens_13out\\" + DL.FALA_ORDEM_V411["nome"], P + r"\instalar_v411.py", P + r"\rito_v411.sh", P + r"\pos_rito\chain_pos_rito_v411.sh", P + r"\bancada_B3_servico\recibo_parada_v411.py",
       P + r"\bancada_B3_servico\recibo_religamento_v411.py", P + r"\bancada_B3_servico\evento_c1_b3_v411.py", P + r"\um_v411_candidato.py", P + r"\ESPERADOS_v411.json",
       CEN + r"\work\php_e_v396_22out\OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt", CEN + r"\work\cunhagens_13out\\" + DL.FALA_TESTEMUNHO_V411["nome"],
       CEN + r"\work\cunhagens_13out\OPERADOR_04nov_custodia_e_da_sessao_de_custodia_c1_so_um_py_verbatim.txt"]
for x in lst:
    print("ok " if os.path.exists(x) else "FALTA", x[-90:])
print("textos_custodia_handoff_v411*.py (sufixo .py):", [os.path.basename(p) for p in glob.glob(P + r"\pos_rito\textos_custodia_handoff_v411*.py") if p.endswith(".py")])
# orquestrador: tarefa agendada e 'sh' e python
for x in (r"C:\Program Files\Git\bin\sh.exe", r"C:\Python314\python.exe", r"C:\Python314\pythonw.exe", r"C:\IALD\Bancada_Um\um_bancada.py", r"C:\IALD\PROGRAMA_IALD\iald.py", r"C:\IALD\TGL_IALD_NATIVE_QWEN5090\12_logs\STATE_v4.json", r"C:\IALD\TGL_IALD_NATIVE_QWEN5090\12_logs\STATUS_v4.json"):
    print("ok " if os.path.exists(x) else "FALTA", x)
# S0: estado do treino
st = json.load(open(r"C:\IALD\TGL_IALD_NATIVE_QWEN5090\12_logs\STATE_v4.json", encoding="utf-8")); print("STATE_v4.stage:", st.get("stage"))
# a ordem: sha16 do arquivo = o do delta
print("sha16 da ordem:", sha16(lst[0]), "delta:", DL.FALA_ORDEM_V411["sha256"][:16])
