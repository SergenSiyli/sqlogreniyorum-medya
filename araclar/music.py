"""Telifsiz, sözsüz lo-fi altyapı üretir (numpy ile sentez). Kullanım: music.py cikti.wav saniye [seed]"""
import sys
import wave
import numpy as np

SR = 44100
BPM = 78
BEAT = 60 / BPM
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 7)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a=0.01, d=1.2):
    t = np.arange(n) / SR
    e = np.minimum(t / a, 1.0) * np.exp(-t / d)
    return e


def epiano(freq, dur, vel=0.18):
    n = int(dur * SR)
    t = np.arange(n) / SR
    # Rhodes benzeri: temel + yumuşak harmonikler + hafif tremolo
    s = (np.sin(2 * np.pi * freq * t)
         + 0.35 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t / 0.4)
         + 0.12 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-t / 0.2))
    s *= 1 + 0.06 * np.sin(2 * np.pi * 4.5 * t)
    return vel * s * env(n, 0.008, 1.6)


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def kick(vel=0.5):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t / 0.04)
    return vel * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.12)


def hat(vel=0.05):
    n = int(0.05 * SR)
    noise = rng.standard_normal(n)
    noise = noise - lowpass(noise, 6000)
    return vel * noise * np.exp(-np.arange(n) / SR / 0.015)


def snare(vel=0.12):
    n = int(0.2 * SR)
    noise = lowpass(rng.standard_normal(n), 4000)
    return vel * noise * np.exp(-np.arange(n) / SR / 0.06)


def build(seconds):
    total = int(seconds * SR) + SR
    mix = np.zeros(total)

    def add(sig, start):
        i = int(start * SR)
        j = min(i + len(sig), total)
        if i < total:
            mix[i:j] += sig[: j - i]

    # Akor dizisi: Fmaj9 - Em7 - Dm9 - Cmaj7 (sakin, çalışma müziği havası)
    chords = [[53, 57, 60, 64, 67], [52, 55, 59, 62], [50, 53, 57, 60, 64], [48, 52, 55, 59]]
    bass = [41, 40, 38, 36]
    bar = 4 * BEAT
    t = 0.0
    k = 0
    while t < seconds + bar:
        ch = chords[k % 4]
        for j, note in enumerate(ch):
            add(epiano(midi(note), bar * 1.1, 0.10), t + j * 0.018)  # hafif arpej
        # ikinci vuruşta yumuşak tekrar
        for note in ch[1:4]:
            add(epiano(midi(note), bar * 0.6, 0.05), t + 2.5 * BEAT)
        add(epiano(midi(bass[k % 4]), bar, 0.22), t)
        for b in range(4):
            bt = t + b * BEAT
            if b in (0, 2):
                add(kick(0.45 if b == 0 else 0.32), bt + (0.0 if b == 0 else BEAT * 0.5))
            if b in (1, 3):
                add(snare(0.09), bt)
            for sub in (0, 0.5):
                add(hat(0.018 if sub else 0.026), bt + sub * BEAT + rng.uniform(0, 0.012))
        t += bar
        k += 1

    mix = lowpass(mix, 2800)  # sıcak, boğuk lo-fi tını
    # Not: plak cızırtısı ve arka plan hışırtısı bilerek YOK (hesap sahibi cızırtı istemedi).

    mix = mix[: int(seconds * SR)]
    # giriş/çıkış
    fi, fo = int(1.0 * SR), int(2.0 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)
    mix[-fo:] *= np.linspace(1, 0, fo)
    mix /= np.max(np.abs(mix)) + 1e-9
    return (mix * 0.7).astype(np.float32)


if __name__ == "__main__":
    out, secs = sys.argv[1], float(sys.argv[2])
    a = build(secs)
    st = np.stack([a, np.roll(a, int(0.012 * SR))], axis=1)  # hafif stereo genişlik
    pcm = (st * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(out, secs)
