import math, random
def chaikin(p, closed=False, it=2):
    for _ in range(it):
        q = []; n = len(p); rng = range(n) if closed else range(n - 1)
        if not closed: q.append(p[0])
        for i in rng:
            a, b = p[i], p[(i + 1) % n]
            q.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1])); q.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        if not closed: q.append(p[-1])
        p = q
    return p
def length(p): return sum(math.hypot(p[i][0] - p[i - 1][0], p[i][1] - p[i - 1][1]) for i in range(1, len(p)))
def resample(p, step):
    out = [p[0]]
    for i in range(1, len(p)):
        a, b = p[i - 1], p[i]; d = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(1, int(d / step))
        for k in range(1, n + 1): out.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))
    return out
def meander(p, amp, step, seed):
    """Resample a line and push points sideways by smooth random amounts; the ends stay fixed."""
    r = random.Random(seed); q = resample(p, step); n = len(q); off = [0.0] * n; v = 0.0
    for i in range(n): v = 0.72 * v + 0.28 * r.uniform(-1, 1) * 3; off[i] = v
    out = []
    for i in range(n):
        a = q[max(0, i - 1)]; b = q[min(n - 1, i + 1)]; dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        w = min(1, i / 3, (n - 1 - i) / 3) * amp * off[i]
        out.append((q[i][0] - dy / L * w, q[i][1] + dx / L * w))
    return out
def wobble(p, amp, seed):
    r = random.Random(seed); return [(x + r.uniform(-amp, amp), y + r.uniform(-amp, amp)) for x, y in p]
def centroid(p): return (sum(x for x, _ in p) / len(p), sum(y for _, y in p) / len(p))
def area(r): return abs(0.5 * sum(r[i][0] * r[(i + 1) % len(r)][1] - r[(i + 1) % len(r)][0] * r[i][1] for i in range(len(r))))
