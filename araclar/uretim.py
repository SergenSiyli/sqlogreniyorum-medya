"""Günlük üretim yardımcıları: Reels'i render et, müzik ekle, ses kalitesini ölç, kapak çıkar.

Kullanım (başka bir betikten):
    from uretim import reel, news_scenes
    reel("reel_konu", scenes, out_dir, seed=5)
"""
import os
import subprocess
import wave

import numpy as np

import reels as R
from brand import *

HERE = os.path.dirname(os.path.abspath(__file__))


def audio_qc(wav_path):
    w = wave.open(wav_path)
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels())[:, 0] / 32768
    jumps = int((np.abs(np.diff(a)) > 0.2).sum())
    hp = a - np.convolve(a, np.ones(8) / 8, "same")
    hf = float(np.sqrt((hp ** 2).mean()))
    return jumps, hf


def reel(name, scenes, out_dir, seed=7):
    """Sessiz videoyu üretir, müzik ekler, kalite ölçer. Döner: (mp4, kapak, süre, qc)"""
    os.makedirs(out_dir, exist_ok=True)
    R.OUT = out_dir
    silent, total = R.render(name + "_sessiz", scenes)
    wav = os.path.join(out_dir, name + "_muzik.wav")
    subprocess.run(["python3", os.path.join(HERE, "music.py"), wav, f"{total + 0.1:.2f}", str(seed)],
                   check=True, capture_output=True)
    jumps, hf = audio_qc(wav)
    mp4 = os.path.join(out_dir, name + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-af", "volume=0.8,loudnorm=I=-18:TP=-1.5", mp4], check=True)
    vol = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp4, "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    maxv = float(vol.split("max_volume:")[1].split("dB")[0])
    os.rename(os.path.join(out_dir, name + "_sessiz_kapak.png"), os.path.join(out_dir, name + "_kapak.png"))
    os.remove(silent)
    os.remove(wav)
    qc = {"sicrama": jumps, "hf_rms": round(hf, 4), "max_db": maxv,
          "ok": jumps == 0 and hf < 0.005 and maxv < -1.0}
    return mp4, os.path.join(out_dir, name + "_kapak.png"), total, qc


# ---------------------------------------------------------------- haber Reels şablonu
def news_scenes(tag, hook_lines, points, takeaway, question, source_label):
    """Teknoloji/yapay zekâ haberi için sahneler.
    hook_lines: [(metin, renk)], points: kısa maddeler (4-5), takeaway: 'neden önemli' cümlesi."""

    def s_hook(d, t):
        pill(d, (70, 420), tag, fill=TEAL, size=38)
        R.big_title(d, t, hook_lines, y=560, size=100, step=0.3)

    def s_points(d, t):
        R.caption(d, t, "Ne oldu?", 360, size=64, weight="Black")
        y = 500
        for i, p in enumerate(points):
            st = 0.3 + i * 1.1
            if R.visible(t, st):
                yy = y + R.rise(t, st, 40)
                d.rounded_rectangle([50, yy, 1030, yy + 170], radius=26, fill=CARD, outline=LINE, width=2)
                d.text((86, yy + 46), str(i + 1), font=font("Black", 64), fill=YELLOW)
                text_block(d, (170, yy + 40), p, font("Bold", 42), max_w=820)
            y += 190

    def s_takeaway(d, t):
        R.caption(d, t, "Neden önemli?", 420, size=64, weight="Black", col=TEAL)
        R.caption(d, t, takeaway, 560, start=0.3, size=56, weight="Bold")
        R.caption(d, t, "Kaynak: " + source_label, 1380, start=0.8, size=34, col=MUTED, weight="SemiBold")

    def s_question(d, t):
        R.big_title(d, t, [("Sen ne", TEXT), ("düşünüyorsun?", YELLOW)], y=560, size=110)
        R.caption(d, t, question, 880, start=0.5, size=52, weight="SemiBold")
        R.caption(d, t, "Yorumlara yaz.", 1150, start=1.0, size=52, col=PINK)

    def s_cta(d, t):
        R.big_title(d, t, [("Takip et,", TEXT), ("her gün yeni", YELLOW), ("teknoloji ve SQL", YELLOW)], y=600, size=96)
        if R.visible(t, 0.8):
            pill(d, (70, 1050 + R.rise(t, 0.8)), HANDLE, fill=PINK, size=44)

    n = len(points)
    return [(3.0, s_hook), (1.0 + n * 1.1 + 2.6, s_points), (5.0, s_takeaway), (4.0, s_question), (3.0, s_cta)]


# ---------------------------------------------------------------- story şablonları (1080x1920, güvenli alan y=250-1580)
def story_poll(path, tag, question, options, note="Cevabını DM'den yaz, akşam sonucu paylaşıyoruz."):
    img, d = canvas(1080, 1920)
    d.text((70, 250), HANDLE, font=font("Bold", 34), fill=MUTED)
    pill(d, (70, 330), tag, fill=PINK, size=36)
    y = text_block(d, (70, 450), question, font("Black", 84), max_w=940, spacing=1.1)
    y += 50
    cols = [YELLOW, TEAL, PINK, BLUE]
    for i, opt in enumerate(options):
        h = 150
        d.rounded_rectangle([60, y, 1020, y + h], radius=28, fill=CARD, outline=cols[i], width=4)
        d.text((100, y + 40), "ABCD"[i], font=font("Black", 60), fill=cols[i])
        text_block(d, (190, y + 46), opt, font("Bold", 46), max_w=800)
        y += h + 26
    text_block(d, (70, y + 30), note, font("SemiBold", 40), fill=MUTED, max_w=940)
    assert y + 120 <= 1580, ("story taşıyor", y)
    img.save(path)
    return path


def story_card(path, tag, title, lines, footer=None, tag_col=GREEN):
    img, d = canvas(1080, 1920)
    d.text((70, 250), HANDLE, font=font("Bold", 34), fill=MUTED)
    pill(d, (70, 330), tag, fill=tag_col, size=36)
    y = text_block(d, (70, 450), title, font("Black", 80), max_w=940, spacing=1.1, highlight=YELLOW)
    y += 40
    for ln in lines:
        lines_wrapped = wrap(d, ln, font("Bold", 44), 860)
        h = len(lines_wrapped) * 54 + 60
        d.rounded_rectangle([60, y, 1020, y + h], radius=26, fill=CARD, outline=LINE, width=2)
        text_block(d, (100, y + 30), ln, font("Bold", 44), max_w=860)
        y += h + 22
    if footer:
        y = text_block(d, (70, y + 30), footer, font("SemiBold", 38), fill=MUTED, max_w=940)
    assert y <= 1580, ("story taşıyor", y)
    img.save(path)
    return path
