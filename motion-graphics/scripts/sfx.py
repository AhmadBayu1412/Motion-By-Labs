"""sfx.py: procedural sound design for motion graphics (Python stdlib only, no samples, no licensed music).

Use it from a per-video sound script (copy the example at the bottom):

    import sys; sys.path.insert(0, "<skill>/scripts"); import sfx
    m = sfx.Mix(20.0)                                      # duration in seconds
    m.drone(0, 20, [110.0, 164.81, 220.0], .01)            # thin bed
    m.put(1.5, sfx.kick(120, 45, .5, 1.6), .22)            # hit at a camera punch
    m.put(1.5, sfx.whoosh(.5, 300, 6000, .6), .1, pan=.3)  # whoosh on a morph
    m.typing(2.0, 30, cps=34)                              # keyboard foley for typed text
    m.write(sys.argv[1])                                   # reverb, master to −0.9 dBFS peak, 48 kHz stereo WAV

Every generator returns a list of mono float samples at SR. Mix.put(t, samples, gain, pan, send) places them.
`send` is the reverb amount: 0 is dry, .3 is roomy, .7 is a bell tail.
"""
import math
import random
import struct
import wave

SR = 48000
TAU = 2 * math.pi
rng = random.Random(7)
PENT = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.66, 1318.51, 1567.98, 1760.0]   # C-major pentatonic blips


# ------------------------------------------------------------------ generators
def env(n, a, d):
    na = max(1, int(a * SR))
    return [(k / na if k < na else math.exp(-(k - na) / (d * SR))) for k in range(n)]


def tone(freq, dur, a=0.002, d=0.2, kind="sine"):
    """kind: sine | bell (inharmonic partials) | pluck (bright attack)"""
    n = int(dur * SR); e = env(n, a, d); out, ph = [], 0.0
    for k in range(n):
        ph += TAU * freq / SR; s = math.sin(ph)
        if kind == "bell":
            s = 0.6 * s + 0.25 * math.sin(ph * 2.76) + 0.15 * math.sin(ph * 5.4)
        elif kind == "pluck":
            s = 0.7 * s + 0.2 * math.sin(ph * 2) * math.exp(-k / (0.05 * SR)) + 0.1 * math.sin(ph * 3)
        out.append(s * e[k])
    return out


def noise(dur, lp, a, d, hp=0.0):
    """filtered noise burst: lp/hp in Hz"""
    n = int(dur * SR); e = env(n, a, d); out, y, yh = [], 0.0, 0.0
    al = 1 - math.exp(-TAU * lp / SR); ah = 1 - math.exp(-TAU * hp / SR) if hp else 0
    for k in range(n):
        y += al * ((rng.random() * 2 - 1) - y); s = y
        if hp:
            yh += ah * (y - yh); s = y - yh
        out.append(s * e[k] * 2.2)
    return out


def whoosh(dur=0.5, lo=300, hi=5000, peak=0.6):
    """noise swept lo→hi with its loudest point at `peak` (0..1). Swap lo/hi for a falling whoosh."""
    n = int(dur * SR); out, y = [], 0.0
    for k in range(n):
        p = k / n; shape = (p / peak) ** 2 if p < peak else ((1 - p) / (1 - peak)) ** 1.5
        c = lo + (hi - lo) * shape; al = 1 - math.exp(-TAU * c / SR)
        y += al * ((rng.random() * 2 - 1) - y); out.append(y * shape * 2.6)
    return out


def kick(f0=150, f1=42, dur=0.5, drive=1.5):
    """pitched-down sine thump. Low f1 and long dur give a sub drop (f0=55, f1=26, dur=1.6, drive=2.6)."""
    n = int(dur * SR); out, ph = [], 0.0
    for k in range(n):
        t = k / SR; ph += TAU * (f1 + (f0 - f1) * math.exp(-t * 28)) / SR
        out.append(math.tanh(math.sin(ph) * math.exp(-t * 8) * drive))
    return out


def thud(weight=1.0):
    b = kick(110 * (1.2 - .3 * weight), 38, 0.7, 1.8); n = noise(0.18, 1800, 0.001, 0.05, 80)
    return [x + (n[i] * 0.35 if i < len(n) else 0) for i, x in enumerate(b)]


def knock(f=700):
    """UI click / key press"""
    return [a * 0.8 + b * 0.35 for a, b in zip(tone(f, 0.12, 0.0008, 0.03), noise(0.12, 4000, 0.0005, 0.012, 600))]


def pop(f=520):
    return kick(f, f / 2, 0.12, 1.2)


def zip_(dur=0.35, up=True):
    return whoosh(dur, 900 if up else 6000, 7000 if up else 900, 0.85 if up else 0.15)


def riser(dur, f0, f1, harm=0.3):
    n = int(dur * SR); out, ph = [], 0.0
    for k in range(n):
        p = k / n; ph += TAU * f0 * (f1 / f0) ** (p * p) / SR
        out.append((math.sin(ph) + harm * math.sin(ph * 2.01) + 0.15 * math.sin(ph * 3.02)) * p ** 1.6 * 0.6)
    return out


def glide(dur, f0, f1):
    """smooth pitch slide (an object travelling along a curve)"""
    n = int(dur * SR); out, ph = [], 0.0
    for k in range(n):
        p = k / n; ph += TAU * f0 * (f1 / f0) ** p / SR; out.append(math.sin(ph) * math.sin(math.pi * p) ** .6 * .7)
    return out


def boing(dur=.45, f0=700, f1=180):
    """comedic falling spring (absurd / error moments)"""
    n = int(dur * SR); out, ph = [], 0.0
    for k in range(n):
        p = k / n; ph += TAU * (f0 * (f1 / f0) ** p) * (1 + .08 * math.sin(TAU * 18 * p)) / SR; out.append(math.sin(ph) * (1 - p) ** 1.4)
    return out


def buzz(dur=.35, f=55):
    """square-wave error buzz (segfault, denied)"""
    n = int(dur * SR); return [math.copysign(1, math.sin(TAU * f * k / SR)) * .5 * (1 - k / n) for k in range(n)]


# ------------------------------------------------------------------ mixer
class Mix:
    def __init__(self, dur, seed=7):
        global rng
        rng = random.Random(seed)
        self.dur = dur; self.n = int(SR * dur)
        self.L = [0.0] * self.n; self.R = [0.0] * self.n; self.SL = [0.0] * self.n; self.SR_ = [0.0] * self.n

    def put(self, t0, samples, gain=1.0, pan=0.0, send=0.25):
        i0 = int(t0 * SR); gl, gr = gain * math.cos((pan + 1) * math.pi / 4), gain * math.sin((pan + 1) * math.pi / 4)
        L, R, SL, SRr = self.L, self.R, self.SL, self.SR_
        for k, s in enumerate(samples):
            i = i0 + k
            if 0 <= i < self.n:
                L[i] += s * gl; R[i] += s * gr; SL[i] += s * gl * send; SRr[i] += s * gr * send

    # --- beds
    def drone(self, t0, t1, notes, gain=.01, send=.6):
        """sustained chord with slow tremolo (pads, sensor hum). Fades .8 s in and .6 s out."""
        phs = [rng.random() * TAU for _ in notes]
        for i in range(int(t0 * SR), int(min(self.dur, t1 + .6) * SR)):
            tt = i / SR; a = min(1, (tt - t0) / .8) * (1 if tt < t1 else max(0, 1 - (tt - t1) / .6))
            v = sum(math.sin(phs[j] + TAU * f * (tt - t0)) * (1 + .3 * math.sin(TAU * .21 * tt + j)) for j, f in enumerate(notes)) * a * gain
            self.L[i] += v; self.R[i] += v; self.SL[i] += v * send; self.SR_[i] += v * send

    def beat(self, t0, t1, bpm=120, gain=.14, hats=True):
        """four-on-the-floor kick (+ off-beat hats). Use for upbeat promos; skip it for SFX-led films."""
        b = 60 / bpm; t = t0
        while t < t1:
            self.put(t, kick(125, 44, .32, 1.6), gain, 0, .04)
            if hats: self.put(t + b / 2, noise(.045, 10000, .001, .012, 6000), gain * .25, .35, .1)
            t += b

    # --- foley helpers
    def blip(self, t, k, g=.04, pan=0.0, d=.05):
        self.put(t, tone(PENT[k % 10] * (2 if k >= 10 else 1), d, .0008, d * .35), g, pan, .3)

    def tick(self, t, g=.025, pan=0.0):
        self.put(t, noise(.018, 9000, .0003, .005, 3500), g, pan, .08)

    def typing(self, t0, chars, cps=34, g=.05, pan=-.2):
        """one key press per visible character of a typed line"""
        for i in range(chars):
            tt = t0 + i / cps
            self.put(tt, knock(1300 + rng.random() * 900), g * (.6 + rng.random() * .5), pan + rng.uniform(-.15, .15), .05)

    def lock(self, t, g=.08, pan=0.0):
        """tracker / bracket locking on"""
        self.put(t, knock(2200), g, pan, .15); self.put(t + .03, tone(1760, .09, .001, .03), g * .6, pan, .2)

    def glitch(self, t, dur, g=.07):
        for i in range(int(dur / .03)):
            self.put(t + i * .03, tone(200 + rng.random() * 3200, .025, .0004, .01, "bell" if i % 3 == 0 else "sine"), g * (.4 + rng.random() * .6), rng.uniform(-.7, .7), .1)
            self.put(t + i * .03, noise(.028, 8000, .0004, .009, 900), g * .5, rng.uniform(-.7, .7), .05)

    def bell_chord(self, t, notes, g=.055, dur=2.2):
        for j, f in enumerate(notes):
            self.put(t + j * .03, tone(f, dur, .004, dur / 2, "bell"), g, -.5 + j / max(1, len(notes) - 1), .8)

    def footage(self, wav_path, time_map=None, gain=.28, t_end=None):
        """mix original footage audio. time_map(t_out) → t_footage applies speed ramps (slow-mo drops pitch, like tape)."""
        with wave.open(wav_path) as w:
            sr, nch, raw = w.getframerate(), w.getnchannels(), w.readframes(w.getnframes())
        ns = len(raw) // (2 * nch); src = struct.unpack("<%dh" % (ns * nch), raw); end = t_end or self.dur
        for i in range(int(min(end, self.dur) * SR)):
            tt = i / SR; fv = time_map(tt) if time_map else tt; p = fv * sr; q = int(p)
            if q + 1 >= ns: break
            u = p - q; l = (src[q * nch] * (1 - u) + src[(q + 1) * nch] * u) / 32768; r = (src[q * nch + nch - 1] * (1 - u) + src[(q + 1) * nch + nch - 1] * u) / 32768
            g = gain * min(1, tt / .4) * min(1, (end - tt) / .25); self.L[i] += l * g; self.R[i] += r * g

    # --- output
    def _reverb(self, x, combs, aps):
        out = [0.0] * self.n
        for d, fb in combs:
            buf = [0.0] * d; lp = 0.0; j = 0
            for i in range(self.n):
                y = buf[j]; lp = y * 0.7 + lp * 0.3; buf[j] = x[i] + lp * fb; out[i] += y; j += 1
                if j == d: j = 0
        for d, g in aps:
            buf = [0.0] * d; j = 0
            for i in range(self.n):
                b = buf[j]; y = -out[i] * g + b; buf[j] = out[i] + b * g; out[i] = y; j += 1
                if j == d: j = 0
        return out

    def write(self, path, reverb=.16, fade_out=.9):
        wl = self._reverb(self.SL, [(1557, .83), (1617, .83), (1491, .82), (1422, .82)], [(225, .5), (556, .5)])
        wr = self._reverb(self.SR_, [(1580, .83), (1640, .83), (1514, .82), (1445, .82)], [(248, .5), (579, .5)])
        L = [a + b * reverb for a, b in zip(self.L, wl)]; R = [a + b * reverb for a, b in zip(self.R, wr)]
        peak = max(max(abs(x) for x in L), max(abs(x) for x in R)) or 1.0; g = min(3.0, 0.92 / peak)
        with wave.open(path, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); fr = bytearray()
            for k in range(self.n):
                fi = min(1.0, k / (0.05 * SR)); fo = min(1.0, (self.n - k) / (fade_out * SR))
                fr += struct.pack("<hh", int(math.tanh(L[k] * g) * fi * fo * 32767), int(math.tanh(R[k] * g) * fi * fo * 32767))
            w.writeframes(bytes(fr))
        print("wrote", path)


if __name__ == "__main__":
    # demo: python3 sfx.py out/demo.wav
    import sys
    m = Mix(6.0)
    m.drone(0, 6, [110.0, 164.81, 220.0], .01)
    m.put(.2, riser(.6, 120, 900, .4), .1)
    m.put(.8, kick(120, 45, .5, 1.6), .22)
    for i in range(8):
        m.blip(.85 + i * .03, i, .03)
    m.typing(1.5, 20, 34)
    m.put(2.6, whoosh(.5, 300, 6000, .6), .1, .3)
    m.glitch(3.4, .4)
    m.put(3.85, kick(55, 26, 1.6, 2.6), .4, 0, .6)
    m.bell_chord(3.9, [440.0, 554.37, 659.25, 880.0])
    m.write(sys.argv[1] if len(sys.argv) > 1 else "demo.wav")
