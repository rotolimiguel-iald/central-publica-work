# -*- coding: utf-8 -*-
"""Máscara VISÍVEL de dados pessoais e credenciais (regra do operador, 22/10/2026: «segredo são dados pessoais, somente»). Troca CPF, RG,
telefone, e-mail pessoal e credenciais por «[dado pessoal removido]» e devolve a contagem por categoria. Usada no retrato do cockpit e nos
repositórios públicos. E-mails institucionais (OMPI, INPI, gov.br, domínios da casa, noreply) ficam."""
import re

MASK = "[dado pessoal removido]"
# institucionais e acadêmicos ficam: os e-mails de autores em cabeçalhos de licença de software científico de terceiros (LIGO, MPG,
# universidades) são parte da atribuição que a própria licença exige (22/10/2026); os pessoais (hotmail, gmail, icloud…) e os do
# Escritório (rmiguel.adv.br) são mascarados
INSTITUCIONAL = re.compile(r"@(?:[\w-]+\.)*(?:wipo\.int|inpi\.gov\.br|gov\.br|example\.(?:com|org)|anthropic\.com|openai\.com|github\.com|"
                           r"users\.noreply\.github\.com|noreply\.[\w.]+|arxiv\.org|zenodo\.org|iald\.ia\.br|python\.org|localhost|"
                           r"teoriadagravitacaoluminodinamica\.com|edu|ac\.[a-z]{2}|ligo\.org|mpg\.de|iap\.fr|cern\.ch|nasa\.gov|esa\.int|"
                           r"cnrs\.fr|inaf\.it|stsci\.edu|caltech\.edu|apache\.org|numpy\.org|scipy\.org|lean-lang\.org|mathlib\.org)\b", re.I)
PII = [("cpf", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
       ("cpf_rotulado", re.compile(r"(?i)(\bCPF\b[^\n\d]{0,12})\d{11}\b")),
       # 22/10/2026: «identidade» sozinha NÃO é rótulo de documento — na TGL é termo central (ω(I) = 1; «o mapeamento exato da
       # identidade», seguido de datas, fez a guarda barrar os um.py do cofre). Só rótulos de documento: RG, R.G., registro geral,
       # carteira/cédula/documento de identidade, identidade nº/número
       # (22/10/2026, 2º achado: na TGL «RG» é Relatividade Geral — «banda RG ✓, bate §88.27.14» virou máscara.) O RG de verdade se
       # escreve com o rótulo e só separadores curtos antes do número, no formato 1.234.567 / 12.345.678-9 / 1234567
       ("rg_rotulado", re.compile(r"(?i)((?:\bRG\b|\bR\.G\.|\bregistro geral\b|\b(?:carteira|c[ée]dula|documento) de identidade\b|"
                                  r"\bidentidade\s*(?:n\.?\s?[º°]|n[úu]m(?:ero|\.)))[\s:.\-nº°]{0,6})"
                                  r"\d{1,2}(?:\.\d{3}\.\d{3}|\d{5,6})(?:-[\dXx])?(?![\d.])")),
       # o rótulo do telefone com FRONTEIRA de palavra («hotel», «Intel», «célula» não são rótulo)
       ("telefone", re.compile(r"(?i)(\b(?:tel|fone|cel|whats|whatsapp|telefone|celular)\b[^\n\d]{0,12})(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}")),
       # 22/10/2026 (varredura de texto livre): telefone SEM rótulo só nas formas inequívocas — com (DDD), com +55 ou com hífen e o 9
       # do celular — para não ler colunas de números de uma tabela como telefone; CEP com rótulo; data de nascimento com rótulo; endereço
       # com quadra e lote
       ("telefone_br", re.compile(r"(?:\+55\s?\(?\d{2}\)?\s?(?:9\d{4}-?\d{4}|\d{4}-?\d{4})|\(\d{2}\)\s?(?:9\d{4}-?\d{4}|\d{4}-\d{4})|"
                                  r"(?<![\w.\-/])\d{2}\s9\d{4}-\d{4}\b|"
                                  # (22/10/2026, achado no cartão CNPJ) o DDD com o zero e a operadora: «[dado pessoal removido]», «[dado pessoal removido]»
                                  # (só com o ZERO na frente: «(1995) 2345-2350» é citação, não telefone)
                                  r"\(0\d{2,3}\)\s?\d{4,5}-\d{4}\b)")),
       # o CEP com ponto e o rótulo na linha de cima («CEP\n[dado pessoal removido]»), como no cartão CNPJ (22/10/2026)
       ("cep_rotulado", re.compile(r"(?i)(\bCEP\b[^\d]{0,6})\d{2}\.?\d{3}-?\d{3}\b")),
       # («nascimento» sozinho é também sobrenome e evento — «o nascimento da teoria»: só os rótulos de documento, 22/10/2026)
       ("nascimento", re.compile(r"(?i)((?:data de nascimento|nascid[oa] em|dt\.? nasc\.?)\s*[:\-]?\s*)\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}")),
       ("endereco", re.compile(r"(?i)\b(?:Rua|Avenida|Av\.|Alameda|Travessa|Rodovia)\s[^\n]{2,60}?\b(?:Qd|Quadra)\.?\s*\d+[^\n]{0,30}?"
                               r"\b(?:Lt|Lote)\.?\s*\d+[^\n,;]{0,60}")),
       ("credencial", re.compile(r"(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|gh[osu]_[A-Za-z0-9]{30,}|sk-ant-[A-Za-z0-9_-]{20,}|"
                                 r"sk-proj-[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"))]
# e-mail de verdade: rótulos de domínio com 2+ caracteres e terminação real — sem isso, o «@» de multiplicação de matrizes do
# Python (Q@K.T, x@W.dt) seria lido como e-mail e a máscara corromperia o código publicado (achado de 22/10/2026)
# (22/10/2026, cronometrado: a forma X*[A-Za-z]X*@ retrocede em quadrático em texto base64 — 34× mais lenta; a letra obrigatória vai num
# lookahead preguiçoso e a parte local é possessiva: o mesmo casamento, sem retrocesso)
EMAIL = re.compile(r"(?<![\w.])(?=[A-Za-z0-9._%+-]*?[A-Za-z])[A-Za-z0-9._%+-]++@(?:[A-Za-z0-9-]{2,}\.)+"
                   r"(?:com|br|org|net|edu|gov|io|ai|dev|info|me|co|uk|de|fr|it|es|pt|ch|int|us|ca|au|jp|cn|ru|nl|se|no|fi|be|at|pl|ar|mx|cl)\b", re.I)


def mascarar(t: str) -> tuple[str, dict]:
    cont = {}
    for nome, rx in PII:
        def rep(m, nome=nome):
            cont[nome] = cont.get(nome, 0) + 1
            return (m.group(1) if (m.lastindex and nome != "credencial") else "") + MASK
        t = rx.sub(rep, t)

    def rep_e(m):
        if INSTITUCIONAL.search(m.group(0)):
            return m.group(0)
        cont["email_pessoal"] = cont.get("email_pessoal", 0) + 1
        return MASK
    return EMAIL.sub(rep_e, t), cont
