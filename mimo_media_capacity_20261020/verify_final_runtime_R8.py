"""Preserve the first effective manifest; add the display-only overlay lineage."""
from pathlib import Path
W=Path(__file__).resolve().parent
text=(W/'verify_final_runtime.py').read_text(encoding='utf-8')
old="W/'host_followup/availability_deploy_R1/install_plan.json']"
new="W/'host_followup/availability_deploy_R1/install_plan.json',W/'client_stage/media_label_R8/install_plan.json']"
assert text.count(old)==1
text=text.replace(old,new).replace("W/'FINAL_RUNTIME_PINS.json'","W/'FINAL_RUNTIME_PINS_R8.json'")
exec(compile(text,str(W/'verify_final_runtime.py'),'exec'),{'__file__':__file__})
