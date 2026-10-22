#!/bin/sh
# pos-selo: a v393 ja esta no Nos; a arvore so-fontes do recibo e refeita a partir do Nos (sem lake build: logs e sha do recibo ja gravados). Confere por script contra KERNEL_RECIBO_v393.json.
cd "$(dirname "$0")" && python -I -B -X utf8 refazer_arvore_v393_pos_selo.py
