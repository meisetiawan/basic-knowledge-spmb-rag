import re
from pathlib import Path

INPUT_FILE = "spmb_2026.md"
OUTPUT_FILE = "spmb_2026_clean.md"

text = Path(INPUT_FILE).read_text(encoding="utf-8")

# =========================================================
# 1. HAPUS OCR ARTIFACT
# =========================================================

ocr_replacements = {
    "￾": "-",
    "–": "-",
    "\u00a0": " ",
}

for old, new in ocr_replacements.items():
    text = text.replace(old, new)

# =========================================================
# 2. HAPUS FOOTER BERULANG
# =========================================================

footer_patterns = [
    r"Petunjuk Operasional SPMB SMAN & SMKN Provinsi Jawa Tengah T\.A\. 2026/2027\s+\d+",
    r"Dinas Pendidikan Provinsi Jawa Tengah Tahun 2026",
]

for pattern in footer_patterns:
    text = re.sub(pattern, "", text, flags=re.IGNORECASE)

# =========================================================
# 3. HAPUS WATERMARK / TANDA TANGAN ELEKTRONIK
# =========================================================

text = re.sub(
    r"Dokumen ini telah ditandatangani.*?BSSN\.\s*",
    "",
    text,
    flags=re.IGNORECASE | re.DOTALL
)

# =========================================================
# 4. HAPUS NOMOR HALAMAN STANDALONE
# =========================================================

text = re.sub(
    r"\n\s*[ivxlcdm\d]+\s*\n",
    "\n",
    text,
    flags=re.IGNORECASE
)

# =========================================================
# 5. HAPUS TOC / DAFTAR ISI NOISE
# =========================================================

text = re.sub(
    r"\*\*BAB III.*?LAMPIRAN II\s+\d+",
    "",
    text,
    flags=re.DOTALL
)

# =========================================================
# 6. HAPUS GAMBAR MARKDOWN
# =========================================================

text = re.sub(
    r"!\[.*?\]\(.*?\)",
    "",
    text
)

# =========================================================
# 7. RAPIIKAN HEADING BAB
# =========================================================

# Gabungkan:
# # BAB IV
# # NILAI AKHIR
# menjadi:
# # BAB IV - NILAI AKHIR

text = re.sub(
    r"#\s*(BAB\s+[IVXLC]+)\s*\n#\s*(.+)",
    r"# \1 - \2",
    text
)

# =========================================================
# 8. NORMALISASI HEADING HURUF BESAR
# =========================================================

def normalize_heading(match):
    level = match.group(1)
    title = match.group(2).strip()

    # jangan ubah singkatan penting
    protected = ["SPMB", "SMA", "SMK", "SLB", "TKA", "KKO"]

    words = []
    for word in title.split():
        if word.upper() in protected:
            words.append(word.upper())
        else:
            words.append(word.capitalize())

    return f"{level} {' '.join(words)}"

text = re.sub(
    r"^(#{1,6})\s+(.+)$",
    normalize_heading,
    text,
    flags=re.MULTILINE
)

# =========================================================
# 9. HAPUS SPASI / NEWLINE BERLEBIHAN
# =========================================================

text = re.sub(r"\n{3,}", "\n\n", text)

# =========================================================
# 10. BERSIHKAN TABLE HTML KOSONG
# =========================================================

text = re.sub(
    r"<table>.*?</table>",
    "",
    text,
    flags=re.DOTALL
)

# =========================================================
# 11. HAPUS TAG HTML SISA
# =========================================================

text = re.sub(r"<[^>]+>", "", text)

# =========================================================
# 12. RAPIIKAN LIST
# =========================================================

text = re.sub(r"\n\s*•", "\n-", text)

# =========================================================
# 13. SIMPAN HASIL
# =========================================================

Path(OUTPUT_FILE).write_text(text, encoding="utf-8")

print(f"Cleaning selesai: {OUTPUT_FILE}")
