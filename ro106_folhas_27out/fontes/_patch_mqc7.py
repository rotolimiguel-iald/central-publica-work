import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\mqc_folhas.py')
s = p.read_text(encoding='utf-8')
# legenda
old = """    best = None
    for fx_ in np.linspace(0.08, 0.92, 22):
        for fy_ in np.linspace(0.08, 0.92, 22):
            lg.set_bbox_to_anchor((fx_, fy_), transform=ax.transAxes)
            R = lg.get_window_extent(r)
            if R.x0 < axb.x0 + 4 or R.x1 > axb.x1 - 4 or R.y0 < axb.y0 + 4 or R.y1 > axb.y1 - 4:
                continue
            if _hit(R, ob) or any(R.overlaps(Bbox.from_extents(a.x0 - 6, a.y0 - 6, a.x1 + 6, a.y1 + 6)) for a in avoid):
                continue
            dist = (fx_ - prefer[0]) ** 2 + (fy_ - prefer[1]) ** 2
            if best is None or dist < best[0]:
                best = (dist, fx_, fy_)
    if best is None:"""
new = """    best = None
    for npos in (22, 61, 121):
        for fx_ in np.linspace(0.05, 0.95, npos):
            for fy_ in np.linspace(0.05, 0.95, npos):
                lg.set_bbox_to_anchor((fx_, fy_), transform=ax.transAxes)
                R = lg.get_window_extent(r)
                if R.x0 < axb.x0 + 4 or R.x1 > axb.x1 - 4 or R.y0 < axb.y0 + 4 or R.y1 > axb.y1 - 4:
                    continue
                if _hit(R, ob) or any(R.overlaps(Bbox.from_extents(a.x0 - 6, a.y0 - 6, a.x1 + 6, a.y1 + 6)) for a in avoid):
                    continue
                dist = (fx_ - prefer[0]) ** 2 + (fy_ - prefer[1]) ** 2
                if best is None or dist < best[0]:
                    best = (dist, fx_, fy_)
        if best is not None:
            break
    if best is None:"""
assert s.count(old) == 1
s = s.replace(old, new)
old2 = """    best = None
    for fx_ in np.linspace(0.08, 0.92, 22):
        for fy_ in np.linspace(0.08, 0.92, 22):
            t.set_position((fx_, fy_))
            R0 = t.get_window_extent(r)
            R = Bbox.from_extents(R0.x0 - 8, R0.y0 - 8, R0.x1 + 8, R0.y1 + 8)
            if R.x0 < axb.x0 + 3 or R.x1 > axb.x1 - 3 or R.y0 < axb.y0 + 3 or R.y1 > axb.y1 - 3:
                continue
            if _hit(R, ob) or any(R.overlaps(Bbox.from_extents(a.x0 - 6, a.y0 - 6, a.x1 + 6, a.y1 + 6)) for a in avoid):
                continue
            dist = (fx_ - prefer[0]) ** 2 + (fy_ - prefer[1]) ** 2
            if best is None or dist < best[0]:
                best = (dist, fx_, fy_)
    if best is None:"""
new2 = """    best = None
    for npos in (22, 61, 121):
        for fx_ in np.linspace(0.05, 0.95, npos):
            for fy_ in np.linspace(0.05, 0.95, npos):
                t.set_position((fx_, fy_))
                R0 = t.get_window_extent(r)
                R = Bbox.from_extents(R0.x0 - 8, R0.y0 - 8, R0.x1 + 8, R0.y1 + 8)
                if R.x0 < axb.x0 + 3 or R.x1 > axb.x1 - 3 or R.y0 < axb.y0 + 3 or R.y1 > axb.y1 - 3:
                    continue
                if _hit(R, ob) or any(R.overlaps(Bbox.from_extents(a.x0 - 6, a.y0 - 6, a.x1 + 6, a.y1 + 6)) for a in avoid):
                    continue
                dist = (fx_ - prefer[0]) ** 2 + (fy_ - prefer[1]) ** 2
                if best is None or dist < best[0]:
                    best = (dist, fx_, fy_)
        if best is not None:
            break
    if best is None:"""
assert s.count(old2) == 1
s = s.replace(old2, new2)
p.write_text(s, encoding='utf-8')
print('ok')
