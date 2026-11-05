#!/bin/sh
# pos-selo: a v408 ja esta no Nos; a arvore so-fontes do recibo (C:/t/k408c/arvore) e refeita a partir do Nos (sem lake build: logs e sha do recibo ja gravados). Confere por script contra kernel/KERNEL_RECIBO_v408.json (raiz, Audit, os 4 modulos novos em TGLExt/ e as contagens de .lean). SO' DEPOIS do selo/instalacao; apaga e refaz a arvore.
cd "$(dirname "$0")" && python -I -B -X utf8 refazer_arvore_v408_pos_selo.py
