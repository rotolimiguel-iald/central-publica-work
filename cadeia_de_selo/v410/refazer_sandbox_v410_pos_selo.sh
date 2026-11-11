#!/bin/sh
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] pos-selo: chama refazer_arvore_v410_pos_selo.py (NAO executado na preparacao); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# pos-selo: a v410 ja esta no Nos; a arvore so-fontes do recibo (C:/t/k410c/arvore) e refeita a partir do Nos (sem lake build: logs e sha do recibo ja gravados). Confere por script contra kernel/KERNEL_RECIBO_v410.json (raiz, Audit, o modulo novo em TGLExt/ e as contagens de .lean). SO' DEPOIS do selo/instalacao; apaga e refaz a arvore.
cd "$(dirname "$0")" && python -I -B -X utf8 refazer_arvore_v410_pos_selo.py
