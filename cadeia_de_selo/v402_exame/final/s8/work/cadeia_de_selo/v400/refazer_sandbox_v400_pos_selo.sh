#!/bin/sh
# pos-selo: a v400 ja esta no Nos; a arvore so-fontes do recibo e refeita a partir do Nos (sem lake build: logs e sha do recibo ja gravados). Confere por script contra kernel/KERNEL_RECIBO_v400.json.
cd "$(dirname "$0")" && python -I -B -X utf8 refazer_arvore_v400_pos_selo.py
