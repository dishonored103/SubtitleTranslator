import re
import sys
import time
import glob
from pathlib import Path

try:
    from tqdm import tqdm
except Exception:
    def tqdm(x, **kw):
        return x

from deep_translator import GoogleTranslator

BATCH_BLOCKS = 20
SLEEP_BETWEEN_BATCHES = 0.2
SOURCE_LANG = "auto"
TARGET_LANG = "fa"

translator = GoogleTranslator(source=SOURCE_LANG, target=TARGET_LANG)

def is_number(s: str) -> bool:
    return s.strip().isdigit()

def read_srt(path: Path):
    raw = path.read_text(encoding="utf-8", errors="ignore").strip()
    blocks = re.split(r"\n\s*\n", raw)
    parsed = [b.splitlines() for b in blocks]
    return parsed

def write_srt_blocks(blocks_lines, out_path: Path):
    blocks_text = ["\n".join(lines) for lines in blocks_lines]
    out_path.write_text("\n\n".join(blocks_text), encoding="utf-8")
    return out_path

def extract_block_text_lines(block_lines):
    if len(block_lines) >= 3 and is_number(block_lines[0]):
        return block_lines[2:]
    return []

def replace_block_text_lines(block_lines, new_text_lines):
    if len(block_lines) >= 3 and is_number(block_lines[0]):
        return [block_lines[0], block_lines[1]] + new_text_lines
    return block_lines

def batch_translate_blocks(blocks, batch_blocks=BATCH_BLOCKS):
    total = len(blocks)
    out_blocks = []
    bar = tqdm(range(0, total, batch_blocks), desc="Batches", ncols=80)
    for start in bar:
        end = min(start + batch_blocks, total)
        batch = blocks[start:end]
        block_texts = []
        block_line_counts = []
        for block in batch:
            text_lines = extract_block_text_lines(block)
            block_line_counts.append(len(text_lines))
            block_texts.append("\n".join(text_lines) if text_lines else "")
        translated_texts = ["" for _ in block_texts]
        nonempty = [(i, t) for i, t in enumerate(block_texts) if t.strip()]
        if nonempty:
            inputs = [t for _, t in nonempty]
            try:
                translated_batch = translator.translate_batch(inputs)
                if isinstance(translated_batch, str):
                    translated_batch = [translator.translate(t) for t in inputs]
            except Exception:
                translated_batch = []
                for t in inputs:
                    try:
                        translated_batch.append(translator.translate(t))
                        time.sleep(0.05)
                    except Exception:
                        translated_batch.append(t)
            for (idx, _), translated in zip(nonempty, translated_batch):
                translated_texts[idx] = translated or ""
        for bi, block in enumerate(batch):
            orig_count = block_line_counts[bi]
            translated_blob = translated_texts[bi].strip()
            if orig_count == 0:
                out_blocks.append(block)
                continue
            cand_lines = [l for l in translated_blob.splitlines() if l.strip() != ""]
            if len(cand_lines) == orig_count:
                new_text_lines = cand_lines
            else:
                if "|||" in translated_blob:
                    parts = [p.strip() for p in translated_blob.split("|||")]
                    new_text_lines = parts if len(parts) == orig_count else [" ".join(cand_lines)] if cand_lines else [translated_blob]
                elif len(cand_lines) >= orig_count and orig_count > 1:
                    new_text_lines = cand_lines[:orig_count]
                else:
                    new_text_lines = [" ".join(cand_lines)] if cand_lines else [""]
            out_blocks.append(replace_block_text_lines(block, new_text_lines))
        time.sleep(SLEEP_BETWEEN_BATCHES)
    return out_blocks

def translate_file(input_path: Path):
    print(f"\n📂 Reading: {input_path}")
    blocks = read_srt(input_path)
    print(f"🔢 Blocks: {len(blocks)}")
    translated = batch_translate_blocks(blocks, batch_blocks=BATCH_BLOCKS)
    out_path = input_path.with_name(input_path.stem + "_fa.srt")
    write_srt_blocks(translated, out_path)
    print(f"✅ Done: {out_path}")
    return out_path

def expand_inputs(args):
    files = []
    seen = set()
    if not args:
        p = input("📂 Enter SRT path(s) or pattern(s) (e.g., *.srt): ").strip()
        args = [p] if p else []
    for arg in args:
        matches = glob.glob(arg) or [arg]
        for m in matches:
            p = Path(m)
            if p.is_dir():
                for s in sorted(p.glob("*.srt")):
                    if s.resolve() not in seen:
                        files.append(s)
                        seen.add(s.resolve())
            else:
                if p.suffix.lower() == ".srt" and p.exists():
                    if p.resolve() not in seen:
                        files.append(p)
                        seen.add(p.resolve())
    return files

def main():
    args = sys.argv[1:]
    inputs = expand_inputs(args)
    if not inputs:
        print("❌ No valid .srt files found.")
        return
    print(f"\n🗂️ Files to process: {len(inputs)}")
    for i, f in enumerate(inputs, 1):
        print(f"  {i}. {f}")
    for f in inputs:
        try:
            translate_file(f)
        except Exception as e:
            print(f"❌ Failed on {f}: {e}")

if __name__ == "__main__":
    main()
