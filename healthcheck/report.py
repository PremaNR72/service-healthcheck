"""Summary table output."""
from typing import List

from .checker import Result


def render_table(results: List[Result]) -> str:
    headers = ["SERVICE", "STATUS", "CODE", "TIME(ms)", "TRIES", "ERROR"]
    rows = [[
        r.name,
        "UP" if r.ok else "DOWN",
        str(r.status) if r.status is not None else "-",
        f"{r.elapsed_ms:.0f}" if r.elapsed_ms is not None else "-",
        str(r.attempts),
        r.error or "",
    ] for r in results]
    widths = [max(len(str(x)) for x in col) for col in zip(headers, *rows)]
    line = "  ".join("-" * w for w in widths)
    fmt = lambda row: "  ".join(c.ljust(w) for c, w in zip(row, widths))
    out = [fmt(headers), line] + [fmt(r) for r in rows]
    down = sum(not r.ok for r in results)
    out.append(line)
    out.append(f"{len(results) - down}/{len(results)} services up")
    return "\n".join(out)
