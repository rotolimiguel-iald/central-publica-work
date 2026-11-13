#!/bin/sh
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] pos-selo: chama refazer_arvore_v411_pos_selo.py (NAO executado na preparacao); a v411 nao tem modulo novo (o recibo nao lista pedra)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] pos-selo: chama refazer_arvore_v410_pos_selo.py (NAO executado na preparacao); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# pos-selo: a v411 ja esta no Nos; a arvore so-fontes do recibo (C:/t/k411c/arvore) e refeita a partir do Nos (sem lake build: logs e sha do recibo ja gravados). Confere por script contra kernel/KERNEL_RECIBO_v411.json (raiz, Audit, os modulos novos em TGLExt/ -- nenhum na v411 -- e as contagens de .lean). SO' DEPOIS do selo/instalacao; apaga e refaz a arvore.
cd "$(dirname "$0")" && python -I -B -X utf8 refazer_arvore_v411_pos_selo.py
