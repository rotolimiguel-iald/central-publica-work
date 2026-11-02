| cenario | CPU-h por PE | wall de 1 PE (24 workers) | F4.1 (2 PE sinteticas) | D10 PE cega (10 PE) | C2 minima (10 PE) | C2 media (20 PE) | C2 ampla (50 PE) |
|---|---|---|---|---|---|---|---|
| otimista (3e6 chamadas) | 51-52 | 3.3-3.8 h | 102-103 CPU-h; 3.3-3.8 h | 511-517 CPU-h; 16.6-19.0 h | 511-517 CPU-h; 16.6-19.0 h | 1023-1034 CPU-h; 33.1-38.1 h | 2556-2586 CPU-h; 82.8-95.2 h |
| central (1e7 chamadas) | 170-172 | 11.0-12.7 h | 341-345 CPU-h; 11.0-12.7 h | 1704-1724 CPU-h; 55.2-63.5 h | 1704-1724 CPU-h; 55.2-63.5 h | 3408-3448 CPU-h; 110.4-126.9 h | 8521-8619 CPU-h; 276.0-317.4 h |
| pessimista (3e7 chamadas) | 511-517 | 33.1-38.1 h | 1023-1034 CPU-h; 33.1-38.1 h | 5113-5171 CPU-h; 165.6-190.4 h | 5113-5171 CPU-h; 165.6-190.4 h | 10225-10343 CPU-h; 331.2-380.8 h | 25563-25856 CPU-h; 828.0-952.1 h |

Totais:

| cenario | F4.1 + D10 + C2 minima (22 PE) | F4.1 + D10 + C2 media (32 PE) | F4.1 + D10 + C2 ampla (62 PE) |
|---|---|---|---|
| otimista (3e6 chamadas) | 1125-1138 CPU-h; 36-42 h (1.5-1.7 dias) | 1636-1655 CPU-h; 53-61 h (2.2-2.5 dias) | 3170-3206 CPU-h; 103-118 h (4.3-4.9 dias) |
| central (1e7 chamadas) | 3749-3792 CPU-h; 121-140 h (5.1-5.8 dias) | 5453-5516 CPU-h; 177-203 h (7.4-8.5 dias) | 10566-10687 CPU-h; 342-394 h (14.3-16.4 dias) |
| pessimista (3e7 chamadas) | 11248-11377 CPU-h; 364-419 h (15.2-17.5 dias) | 16360-16548 CPU-h; 530-609 h (22.1-25.4 dias) | 31698-32062 CPU-h; 1027-1181 h (42.8-49.2 dias) |
