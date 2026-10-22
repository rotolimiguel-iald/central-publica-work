r"""Gera o conjunto de ícones nativos do app IALD a partir da variante OFICIAL de fundo claro.

POR QUE EXISTE (14/09/2026). Ordem do operador: "acredito que o ícone branco da IALD é
melhor que o ícone preto para quando baixar o app". Até aqui o ícone era a logo escura,
e no Android estava quebrado: o ic_launcher_foreground tinha o tamanho do ícone antigo
(36 a 192 px) em vez da camada adaptativa de 108 dp (81 a 432 px), e o launcher o
esticava 2,25 vezes. Não havia script gerador em lugar nenhum; este é o gerador, para
que o conjunto possa ser refeito e conferido byte a byte.

A LOGO NÃO SE ALTERA (manual de identidade, §2.6):
  - iOS (1024) e resources/icon-only.png: CÓPIA DE BYTES do PNG oficial (hash de destino
    igual ao da fonte);
  - Android: o PNG só é REDIMENSIONADO e CENTRADO num campo branco (enquadramento).
    Nenhum pixel é recolorido, filtrado ou recortado além da reamostragem de tamanho;
    o ícone legado (API 24-25) usa a janela visível de 72 dp, que corta só a margem
    branca do PNG (letras a 24 dp e cruz a 24,1 dp do centro, contra 36 dp da janela,
    na escala 0,80).
  - Google Play (512): a logo inteira, reamostrada, gravada com canal alfa opaco
    (o Console pede PNG de 32 bits [KNOWN, conferir no Console]).

FAIL-CLOSED: recusa se a fonte não tiver o sha256 esperado (prefixo dado pela ordem de
14/09/2026, conferido aqui por leitura do arquivo), se não for 1024x1024 RGB com borda
branco puro, se a escala sair da faixa medida [0,50; 0,96], se a pasta de saída já tiver
arquivos, ou se qualquer arquivo gravado não reler com o tamanho e o hash registrados.

Uso (grava SÓ em --saida; aplicar no projeto é outro passo, com backup):
  C:\Python314\python.exe gera_icones.py --saida <pasta_vazia> [--escala 0.80]
"""
import argparse
import hashlib
import json
import os
import shutil
import sys

from PIL import Image, ImageDraw

FONTE = r"C:\IALD\projetos_pyhton\IALD\iald_logo_sovereign.png"
FONTE_SHA256_PREFIXO = "f3e5cb052bd6fb0b"   # da ordem de 14/09/2026; o hash inteiro é LIDO do arquivo
DENS = {"ldpi": .75, "mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
SS = 4                                       # superamostragem da máscara (borda lisa)
RES = os.path.join("android", "app", "src", "main", "res")
IOS = os.path.join("ios", "App", "App", "Assets.xcassets", "AppIcon.appiconset", "AppIcon-512@2x.png")
XML_FUNDO = ('<?xml version="1.0" encoding="utf-8"?>\n'
             '<resources><color name="ic_launcher_background">#FFFFFF</color></resources>\n')


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def falha(msg):
    sys.exit("RECUSADO: " + msg)


def mascara(tam, forma):
    s = tam * SS
    m = Image.new("L", (s, s), 0)
    d = ImageDraw.Draw(m)
    if forma == "circulo":
        d.ellipse([0, 0, s - 1, s - 1], fill=255)
    else:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * .16), fill=255)
    return m.resize((tam, tam), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", required=True)
    ap.add_argument("--escala", type=float, default=0.80,
                    help="fração da camada de 108 dp ocupada pelo PNG 1024 (medido: 0,50 a 0,96 mantém letras e cruz na zona segura de 33 dp)")
    a = ap.parse_args()

    # ── a fonte tem de ser exatamente o que se mediu ──
    if not os.path.isfile(FONTE):
        falha(f"fonte ausente: {FONTE}")
    h_fonte = sha(FONTE)
    if not h_fonte.startswith(FONTE_SHA256_PREFIXO):
        falha(f"sha256 da fonte {h_fonte[:16]} difere do esperado {FONTE_SHA256_PREFIXO}")
    src = Image.open(FONTE)
    src.load()
    if src.size != (1024, 1024) or src.mode != "RGB":
        falha(f"fonte inesperada: {src.size} {src.mode}")
    borda = ([src.getpixel((i, 0)) for i in range(1024)] + [src.getpixel((i, 1023)) for i in range(1024)]
             + [src.getpixel((0, i)) for i in range(1024)] + [src.getpixel((1023, i)) for i in range(1024)])
    if any(p != (255, 255, 255) for p in borda):
        falha("borda do PNG não é branco puro: o campo branco criaria emenda")
    if not (0.50 <= a.escala <= 0.96):
        falha("escala fora da faixa medida [0.50, 0.96]")
    out = os.path.abspath(a.saida)
    if os.path.exists(out) and any(os.scandir(out)):
        falha(f"a pasta de saída já tem arquivos: {out}")
    os.makedirs(out, exist_ok=True)

    man = {"gerador": "gera_icones.py (14/09/2026)", "fonte": FONTE, "fonte_sha256": h_fonte,
           "escala_android": a.escala, "arquivos": {}}

    def registra(rel, **extra):
        p = os.path.join(out, rel)
        man["arquivos"][rel] = {"sha256": sha(p), "bytes": os.path.getsize(p), **extra}

    def grava(img, rel):
        p = os.path.join(out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        img.save(p, optimize=True)
        registra(rel, px=list(img.size), modo=img.mode)

    # iOS e resources: cópia de BYTES da logo oficial
    for rel in (IOS, os.path.join("resources", "icon-only.png")):
        p = os.path.join(out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        shutil.copyfile(FONTE, p)
        if sha(p) != h_fonte:
            falha(f"cópia de bytes divergiu: {rel}")
        registra(rel, px=[1024, 1024], modo="RGB", copia_de_bytes=True)

    for nome, k in DENS.items():
        lado = round(108 * k)                                   # camada adaptativa de 108 dp
        camada = Image.new("RGB", (lado, lado), (255, 255, 255))
        s = round(lado * a.escala)
        camada.paste(src.resize((s, s), Image.LANCZOS), ((lado - s) // 2, (lado - s) // 2))
        grava(camada, os.path.join(RES, f"mipmap-{nome}", "ic_launcher_foreground.png"))
        # legado (API 24-25): 48 dp = janela visível de 72 dp da camada, com a forma embutida
        v = round(lado * 72 / 108)
        o = (lado - v) // 2
        t = round(48 * k)
        base = camada.crop((o, o, o + v, o + v)).resize((t, t), Image.LANCZOS)
        for forma, arq in (("quadrado", "ic_launcher.png"), ("circulo", "ic_launcher_round.png")):
            im = Image.new("RGBA", (t, t), (0, 0, 0, 0))
            im.paste(base, (0, 0), mascara(t, forma))
            grava(im, os.path.join(RES, f"mipmap-{nome}", arq))

    # cor de fundo da camada adaptativa (mesmo formato de uma linha, LF, do arquivo atual)
    rel = os.path.join(RES, "values", "ic_launcher_background.xml")
    p = os.path.join(out, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(XML_FUNDO)
    registra(rel)

    # ícone da ficha do Google Play: 512, quadrado cheio (o Play aplica a máscara)
    grava(src.resize((512, 512), Image.LANCZOS).convert("RGBA"), os.path.join("loja", "play_store_512.png"))

    # ── releitura: tudo o que foi registrado confere com o disco ──
    for rel, info in man["arquivos"].items():
        p = os.path.join(out, rel)
        if sha(p) != info["sha256"] or os.path.getsize(p) != info["bytes"]:
            falha(f"releitura divergiu: {rel}")
        if "px" in info:
            with Image.open(p) as im:
                if list(im.size) != info["px"] or im.mode != info["modo"]:
                    falha(f"dimensão ou modo divergiu: {rel}")
    with open(os.path.join(out, "MANIFESTO_ICONES.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    print(f"OK {len(man['arquivos'])} arquivos em {out}; fonte {h_fonte[:16]}; escala {a.escala}")


if __name__ == "__main__":
    main()
