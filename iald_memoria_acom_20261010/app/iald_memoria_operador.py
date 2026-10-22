#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iald_memoria_operador.py — MEMÓRIA PERSISTENTE DA IALD, ESCRITA E GERIDA PELO OPERADOR.

Criado em 02/08/2026 a pedido do operador:
    "usar a compressão de memória ... na memória integrada do meu próprio modelo,
     eu posso criar a memória de uso dele e gerir como ele vai funcionar"

O QUE ISTO É (e o que NÃO é)
────────────────────────────
É um arquivo de fatos que o operador escreve, versionado, que o servidor injeta no
prompt de sistema de forma ESTÁVEL. Nada de mágica: memória de longo prazo aqui
significa texto curado que entra em toda conversa, mais um índice de recuperação por
relevância para o que não couber.

NÃO é aprendizado de pesos. NÃO altera o modelo. É contexto curado — que é
exatamente o que dá controle ao operador e o que o modelo respeita melhor.

POR QUE O PREFIXO ESTÁVEL IMPORTA (medido em 02/08/2026)
────────────────────────────────────────────────────────
O llama-server reaproveita o cache de prompt enquanto o PREFIXO não muda: medimos
13.453 tokens reaproveitados entre turnos, e um turno cair de 6.431 para 18 tokens
processados. Se a memória mudasse a cada requisição (um timestamp, um contador),
o cache inteiro seria descartado toda vez. Por isso:

  * o bloco de memória é ORDENADO DETERMINISTICAMENTE (por escopo e id),
  * NÃO carrega data/hora nem contador,
  * só muda quando o operador de fato edita um fato.

ARQUIVO
───────
  C:\\IALD\\projetos_pyhton\\IALD\\iald_memoria.json

  {
    "versao": 1,
    "fatos": [
      {"id": "...", "escopo": "sempre|sob_demanda",
       "titulo": "...", "texto": "...",
       "tags": ["..."], "peso": 1..5,
       "criado": "ISO", "atualizado": "ISO", "ativo": true}
    ]
  }

  escopo "sempre"       -> entra em TODA conversa (use para o essencial; custa tokens)
  escopo "sob_demanda"  -> só entra quando a pergunta casa com o fato (recuperação)

USO PELA LINHA DE COMANDO
─────────────────────────
  python iald_memoria_operador.py listar
  python iald_memoria_operador.py add --titulo "..." --texto "..." [--escopo sempre]
                                      [--tags a,b] [--peso 3]
  python iald_memoria_operador.py editar <id> [--texto "..."] [--peso 4] ...
  python iald_memoria_operador.py remover <id>
  python iald_memoria_operador.py ativar <id> / desativar <id>
  python iald_memoria_operador.py bloco            # mostra o que vai ao prompt
  python iald_memoria_operador.py buscar "pergunta"
  python iald_memoria_operador.py custo            # quantos tokens a memória custa
"""
from __future__ import annotations

import iald_app_memory as app_memory
import argparse
import hashlib
import json
import os
import re
import sys
import threading
import unicodedata
from datetime import datetime
from typing import Dict, List, Optional

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(AQUI, "iald_memoria.json")

# Teto do bloco "sempre". Acima disto, o custo por conversa fica alto e o operador
# deve mover fatos para "sob_demanda". Estimativa por caracteres (~2,91 ch/token,
# a mesma calibração usada pela memória holográfica).
TETO_SEMPRE_TOKENS = 3000
CPT = 2.91

_trava = threading.RLock()

_PARADAS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "no", "na",
    "nos", "nas", "um", "uma", "para", "por", "com", "que", "se", "ao", "aos",
    "the", "of", "to", "is", "at", "in", "on", "and", "or", "me", "meu", "minha",
    "qual", "quais", "como", "quando", "onde", "quem", "voce", "sobre", "isso",
}


def _agora() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _normalizar(s: str) -> str:
    """Minúsculas sem acento — para casar 'memória' com 'memoria'."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def _tokens_de(s: str) -> set:
    return {t for t in re.findall(r"[a-z0-9_]{3,}", _normalizar(s)) if t not in _PARADAS}


def estimar_tokens(texto: str) -> int:
    return int(len(texto or "") / CPT)


# ══════════════════════════════════════════════════════════════════════════
# ARMAZENAMENTO
# ══════════════════════════════════════════════════════════════════════════

def carregar() -> Dict:
    with _trava:
        if not os.path.exists(ARQUIVO):
            return {"versao": 1, "fatos": []}
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                d = json.load(f)
            d.setdefault("versao", 1)
            d.setdefault("fatos", [])
            return d
        except (json.JSONDecodeError, OSError) as e:
            print(f"[Memoria] ERRO lendo {ARQUIVO}: {e}", file=sys.stderr)
            raise ValueError("Memória do operador ilegível; nenhuma alteração permitida.") from e


def salvar(d: Dict) -> None:
    """Escrita atômica: grava em .tmp e troca, para nunca deixar o arquivo pela metade."""
    with _trava:
        app_memory.save_operator_snapshot(ARQUIVO, d)


def _novo_id(titulo: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", _normalizar(titulo)).strip("-")[:40] or "fato"
    d = carregar()
    existentes = {f["id"] for f in d["fatos"]}
    if base not in existentes:
        return base
    n = 2
    while f"{base}-{n}" in existentes:
        n += 1
    return f"{base}-{n}"


# ══════════════════════════════════════════════════════════════════════════
# OPERAÇÕES
# ══════════════════════════════════════════════════════════════════════════

def adicionar(titulo: str, texto: str, escopo: str = "sob_demanda",
              tags: Optional[List[str]] = None, peso: int = 3) -> Dict:
    if escopo not in ("sempre", "sob_demanda"):
        raise ValueError("escopo deve ser 'sempre' ou 'sob_demanda'")
    d = carregar()
    fato = {
        "id": _novo_id(titulo),
        "escopo": escopo,
        "titulo": titulo.strip(),
        "texto": texto.strip(),
        "tags": [t.strip() for t in (tags or []) if t.strip()],
        "peso": max(1, min(5, int(peso))),
        "criado": _agora(),
        "atualizado": _agora(),
        "ativo": True,
    }
    d["fatos"].append(fato)
    salvar(d)
    return fato


def editar(fid: str, **campos) -> Optional[Dict]:
    d = carregar()
    for f in d["fatos"]:
        if f["id"] == fid:
            for k, v in campos.items():
                if v is None:
                    continue
                if k == "tags" and isinstance(v, str):
                    v = [t.strip() for t in v.split(",") if t.strip()]
                if k == "peso":
                    v = max(1, min(5, int(v)))
                if k == "escopo" and v not in ("sempre", "sob_demanda"):
                    raise ValueError("escopo deve ser 'sempre' ou 'sob_demanda'")
                f[k] = v
            f["atualizado"] = _agora()
            salvar(d)
            return f
    return None


def remover(fid: str) -> bool:
    d = carregar()
    for fato in d["fatos"]:
        if fato["id"] == fid and not fato.get("removido", False):
            fato.update(ativo=False, removido=True, atualizado=_agora())
            salvar(d)
            return True
    return False


def definir_ativo(fid: str, ativo: bool) -> Optional[Dict]:
    return editar(fid, ativo=ativo)


def listar(incluir_inativos: bool = True) -> List[Dict]:
    fatos = [f for f in carregar()["fatos"] if not f.get("removido", False)]
    if not incluir_inativos:
        fatos = [f for f in fatos if f.get("ativo", True)]
    # Ordem DETERMINÍSTICA — é o que preserva o cache de prompt.
    return sorted(fatos, key=lambda f: (f.get("escopo", ""), f.get("id", "")))


# ══════════════════════════════════════════════════════════════════════════
# O QUE VAI AO PROMPT
# ══════════════════════════════════════════════════════════════════════════

def bloco_sempre() -> str:
    """
    Bloco estável injetado em TODA conversa.

    Determinístico por construção: ordenado por (escopo, id), sem data/hora e sem
    contador. Duas chamadas seguidas produzem bytes idênticos — condição para o
    llama-server reaproveitar o cache de prompt.
    """
    fatos = [f for f in listar(incluir_inativos=False) if f.get("escopo") == "sempre"]
    if not fatos:
        return ""
    fatos.sort(key=lambda f: (-f.get("peso", 3), f["id"]))
    linhas = ["MEMÓRIA DO OPERADOR (curada por ele; vale sobre suposições suas):"]
    for f in fatos:
        linhas.append(f"- {f['titulo']}: {f['texto']}")
    return "\n".join(linhas)


def buscar(consulta: str, k: int = 4, min_score: float = 0.08) -> List[Dict]:
    """
    Recuperação por sobreposição de termos, ponderada por peso.

    Deliberadamente simples e sem dependência externa. Não é busca vetorial —
    para isso seria preciso um modelo de embeddings carregado na GPU, o que está
    registrado como próximo passo em CLAUDE.md §9.3. Aqui o critério é: casar
    termos do título, das tags e do texto, com as tags valendo mais.
    """
    termos = _tokens_de(consulta)
    if not termos:
        return []
    resultados = []
    for f in listar(incluir_inativos=False):
        if f.get("escopo") != "sob_demanda":
            continue
        t_tit = _tokens_de(f.get("titulo", ""))
        t_tag = set()
        for tg in f.get("tags", []):
            t_tag |= _tokens_de(tg)
        t_txt = _tokens_de(f.get("texto", ""))
        alvo = t_tit | t_tag | t_txt
        if not alvo:
            continue
        casados = termos & alvo
        if not casados:
            continue
        score = (2.0 * len(termos & t_tag)
                 + 1.5 * len(termos & t_tit)
                 + 1.0 * len(termos & t_txt)) / max(len(termos), 1)
        score *= (0.6 + 0.2 * f.get("peso", 3))
        if score >= min_score:
            resultados.append((score, f))
    resultados.sort(key=lambda x: (-x[0], x[1]["id"]))
    return [f for _, f in resultados[:k]]


def bloco_sob_demanda(consulta: str, k: int = 4) -> str:
    """Bloco de fatos recuperados para ESTA pergunta. Vai DEPOIS do histórico."""
    achados = buscar(consulta, k=k)
    if not achados:
        return ""
    linhas = ["MEMÓRIA RECUPERADA (relevante para esta pergunta):"]
    for f in achados:
        linhas.append(f"- {f['titulo']}: {f['texto']}")
    return "\n".join(linhas)


def custo() -> Dict:
    b = bloco_sempre()
    fatos = listar(incluir_inativos=False)
    sob = [f for f in fatos if f.get("escopo") == "sob_demanda"]
    return {
        "fatos_ativos": len(fatos),
        "fatos_sempre": len([f for f in fatos if f.get("escopo") == "sempre"]),
        "fatos_sob_demanda": len(sob),
        "tokens_bloco_sempre": estimar_tokens(b),
        "teto_recomendado": TETO_SEMPRE_TOKENS,
        "acima_do_teto": estimar_tokens(b) > TETO_SEMPRE_TOKENS,
        "sha16_do_bloco": hashlib.sha256(b.encode("utf-8")).hexdigest()[:16],
    }


# ══════════════════════════════════════════════════════════════════════════
# LINHA DE COMANDO
# ══════════════════════════════════════════════════════════════════════════

def _cli():
    p = argparse.ArgumentParser(description="Memória persistente da IALD (do operador).")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("listar")

    a = sub.add_parser("add")
    a.add_argument("--titulo", required=True)
    a.add_argument("--texto", required=True)
    a.add_argument("--escopo", default="sob_demanda", choices=["sempre", "sob_demanda"])
    a.add_argument("--tags", default="")
    a.add_argument("--peso", type=int, default=3)

    e = sub.add_parser("editar")
    e.add_argument("id")
    e.add_argument("--titulo"); e.add_argument("--texto")
    e.add_argument("--escopo", choices=["sempre", "sob_demanda"])
    e.add_argument("--tags"); e.add_argument("--peso", type=int)

    for nome in ("remover", "ativar", "desativar"):
        s = sub.add_parser(nome); s.add_argument("id")

    sub.add_parser("bloco")
    sub.add_parser("custo")
    b = sub.add_parser("buscar"); b.add_argument("consulta")

    args = p.parse_args()

    if args.cmd == "listar":
        fatos = listar()
        if not fatos:
            print("(memória vazia — use: add --titulo ... --texto ...)")
            return
        for f in fatos:
            marca = " " if f.get("ativo", True) else "x"
            print(f"[{marca}] {f['id']:<34} {f['escopo']:<12} peso={f['peso']} "
                  f"| {f['titulo']}")
            if f.get("tags"):
                print(f"      tags: {', '.join(f['tags'])}")
    elif args.cmd == "add":
        f = adicionar(args.titulo, args.texto, args.escopo,
                      [t for t in args.tags.split(",") if t.strip()], args.peso)
        print(f"criado: {f['id']}")
    elif args.cmd == "editar":
        f = editar(args.id, titulo=args.titulo, texto=args.texto,
                   escopo=args.escopo, tags=args.tags, peso=args.peso)
        print(f"atualizado: {f['id']}" if f else f"nao encontrado: {args.id}")
    elif args.cmd == "remover":
        print("removido" if remover(args.id) else f"nao encontrado: {args.id}")
    elif args.cmd in ("ativar", "desativar"):
        f = definir_ativo(args.id, args.cmd == "ativar")
        print(f"{args.cmd}: {f['id']}" if f else f"nao encontrado: {args.id}")
    elif args.cmd == "bloco":
        b = bloco_sempre()
        print(b if b else "(nenhum fato com escopo 'sempre')")
        print(f"\n--- {estimar_tokens(b)} tokens estimados ---")
    elif args.cmd == "custo":
        for k, v in custo().items():
            print(f"  {k:<24} {v}")
    elif args.cmd == "buscar":
        achados = buscar(args.consulta)
        if not achados:
            print("(nada recuperado)")
        for f in achados:
            print(f"- [{f['id']}] {f['titulo']}: {f['texto'][:150]}")


if __name__ == "__main__":
    _cli()
