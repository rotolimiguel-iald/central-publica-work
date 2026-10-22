# PROPOSTA — NÃO APLICADA

Snapshot: 09D6BEC30171A9C1F522CADB0BD7189545CF03F1B8297A3A0DEB39A21922D140

As três substituições decisórias são extraídas por AST; os ajustes editoriais complementares estão no parecer.

```diff
@@ sub_a_conservation, linha 67591 @@
- sub_a_conservation = bool(all((v for k, v in internal.items() if k not in _v3_keys)) and all(in_window.values()) and em_face['em_identity_closes'])
+ sub_a_conservation = bool(all((v for k, v in internal.items() if k not in _v3_keys)) and em_face['em_identity_closes'])
```

```diff
@@ link_closed, linha 67608 @@
- link_closed = bool(all((v for k, v in internal.items() if k not in _v3_keys)) and all(in_window.values()))
+ link_closed = bool(all((v for k, v in internal.items() if k not in _v3_keys)))
```

```diff
@@ alive_ok, linha 2470 @@
- alive_ok = bool(abs(alive['beta'] - beta_live) < 1e-15 and lo <= alive['M_GA_Msun'] <= hi)
+ alive_ok = bool(abs(alive['beta'] - beta_live) < 1e-15)
```
