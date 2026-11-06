#!/bin/sh
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] pos-selo: chama refazer_arvore_v409_pos_selo.py (NAO executado na preparacao)
# pos-selo: a v409 ja esta no Nos; a arvore so-fontes do recibo (C:/t/k409c/arvore) e refeita a partir do Nos (sem lake build: logs e sha do recibo ja gravados). Confere por script contra kernel/KERNEL_RECIBO_v409.json (raiz, Audit, o modulo novo em TGLExt/ e as contagens de .lean). SO' DEPOIS do selo/instalacao; apaga e refaz a arvore.
cd "$(dirname "$0")" && python -I -B -X utf8 refazer_arvore_v409_pos_selo.py
