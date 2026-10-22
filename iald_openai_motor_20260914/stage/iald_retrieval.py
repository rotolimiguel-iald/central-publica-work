"""Local lexical passage index with exact source coordinates; no embeddings/API."""
from collections import Counter, defaultdict
import math
import re
import unicodedata

STOP_WORDS = set('a as o os de da das do dos e em no na nos nas um uma para por com que ao aos se sua suas seu seus sobre entre the of and in to is uma segundo explique localize leia consulte'.split())


def terms(text):
    # Preserve identifiers, while also indexing their snake_case/CamelCase parts.
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    expanded = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', expanded)
    expanded = expanded.replace('_', ' ')
    normalized = ''.join(c for c in unicodedata.normalize('NFKD', expanded.casefold())
                         if not unicodedata.combining(c))
    words = re.findall(r'[^\W_]+', normalized)
    # Prefix terms tolerate common inflections; results still show exact text.
    return [word[:6] if len(word) > 6 else word for word in words
            if len(word) > 1 and word not in STOP_WORDS]


class PassageIndex:
    def __init__(self, documents):
        self.blocks = []
        self.postings = defaultdict(list)
        for path, text in documents.items():
            lines = text.splitlines()
            for start in range(0, len(lines), 16):
                end = min(start + 24, len(lines))
                excerpt = '\n'.join(lines[start:end])
                counts = Counter(terms(excerpt))
                for word in terms(path):
                    counts[word] += 2
                index = len(self.blocks)
                self.blocks.append((path, start + 1, end, excerpt, counts))
                for word in counts:
                    self.postings[word].append(index)

    def search(self, query, limit=5):
        wanted = set(terms(query))
        scores = defaultdict(float)
        found = defaultdict(set)
        for word in wanted:
            postings = self.postings.get(word, [])
            idf = math.log(1 + len(self.blocks) / (1 + len(postings)))
            for index in postings:
                counts = self.blocks[index][4]
                frequency = counts[word]
                length = max(1, sum(counts.values()))
                scores[index] += idf * frequency * 2.2 / (frequency + 1.2 * (.25 + .75 * length / 180))
                found[index].add(word)
        # Coverage ranks above frequency so a generic, long file cannot swamp
        # a short declaration containing every requested term.
        ranked = sorted(scores, key=lambda i: (-len(found[i]), -scores[i], i))
        # If a passage covers every query term, omit weaker partial matches.
        if ranked and len(found[ranked[0]]) == len(wanted):
            ranked = [i for i in ranked if len(found[i]) == len(wanted)]
        results = []
        for i in ranked:
            path, start, end, excerpt, counts = self.blocks[i]
            if any(r['path'] == path and not (end < r['line'] or start > r['end_line']) for r in results):
                continue
            results.append({'path': path, 'line': start, 'end_line': end,
                            'excerpt': excerpt, 'matched_terms': sorted(found[i]),
                            'missing_terms': sorted(wanted - found[i]),
                            'score': round(scores[i], 4)})
            if len(results) >= limit:
                break
        return results
