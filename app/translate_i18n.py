

import argparse
import json
import os
import sys
import time
from typing import Dict, Any, Callable, Optional

try:

    from deep_translator import GoogleTranslator, DeeplTranslator
except Exception as e:
    print("Missing dependency: deep-translator\n  pip install deep-translator", file=sys.stderr)
    raise

DEEPL_MAP = {
    "en": "EN", "es": "ES", "fr": "FR", "de": "DE", "pt": "PT", "it": "IT", "nl": "NL",
    "pl": "PL", "tr": "TR", "ru": "RU", "uk": "UK", "ar": "AR", "he": "HE", "fa": "FA",
    "hi": "HI", "bn": "BN", "id": "ID", "ms": "MS", "vi": "VI", "th": "TH",
    "ja": "JA", "ko": "KO", "zh": "ZH", "zh_TW": "ZH-TW",
}
GOOGLE_MAP = {
    "en": "en", "es": "es", "fr": "fr", "de": "de", "pt": "pt", "it": "it", "nl": "nl",
    "pl": "pl", "tr": "tr", "ru": "ru", "uk": "uk", "ar": "ar", "he": "iw", "fa": "fa",
    "hi": "hi", "bn": "bn", "id": "id", "ms": "ms", "vi": "vi", "th": "th",
    "ja": "ja", "ko": "ko", "zh": "zh-CN", "zh_TW": "zh-TW",
}

ALL_CODES = [
    "ar","bn","de","es","fa","fr","he","hi","id","it","ja","ko","ms","nl","pl","pt",
    "ru","th","tr","uk","vi","zh","zh_TW"
]

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f) or {}

def save_json(path: str, data: Dict[str, Any], backup: bool=True) -> None:
    if backup and os.path.exists(path):
        try:
            os.replace(path, path + ".bak")
        except Exception:
            pass
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def detect_placeholders(s: str) -> set:

    import re
    curly = set(re.findall(r"\{[^{}]+\}", s))        # {name}, {count}
    pct    = set(re.findall(r"%\w", s))             # %s, %d (rare in your UI)
    fmt    = set(re.findall(r"\{\d+\}", s))         # {0}, {1}
    return curly | pct | fmt

def restore_placeholders(src: str, translated: str) -> str:

    ph = list(detect_placeholders(src))
    out = translated
    for p in ph:
        if p not in out:
            if not out.endswith(" "):
                out += " "
            out += p
    return out

def mk_translator(provider: str, api_key: Optional[str], source: str, target: str) -> Callable[[str], str]:
    provider = provider.lower()
    if provider == "deepl":
        if not api_key:
            print("DeepL selected but no API key given. Use --deepl-key or DEEPL_API_KEY env var.", file=sys.stderr)
            sys.exit(1)

        def _fn(text: str) -> str:
            return DeeplTranslator(api_key=api_key).translate_text(text, source_lang=source.upper(), target_lang=target)
        return _fn
    elif provider == "google":

        def _fn(text: str) -> str:
            return GoogleTranslator(source=source.lower(), target=target.lower()).translate(text)
        return _fn
    else:
        print("Unknown provider. Use --provider deepl|google", file=sys.stderr)
        sys.exit(1)

def translate_file(path: str,
                   provider: str,
                   deepl_key: Optional[str],
                   src_code: str,
                   tgt_code: str,
                   skip_english: bool,
                   sleep_s: float,
                   dry_run: bool) -> None:

    if provider.lower() == "deepl":
        src = DEEPL_MAP.get(src_code, src_code.upper())
        tgt = DEEPL_MAP.get(tgt_code, tgt_code.upper())
    else:
        src = GOOGLE_MAP.get(src_code, src_code.lower())
        tgt = GOOGLE_MAP.get(tgt_code, tgt_code.lower())

    translate = mk_translator(provider, deepl_key, src, tgt)

    data = load_json(path)
    changed = False
    for k, v in list(data.items()):
        if not isinstance(v, str):
            continue
        if skip_english and v.strip() and v.strip() != v.encode("ascii", "ignore").decode("ascii"):

            continue
        try:
            t = translate(v)
            t = restore_placeholders(v, t)
            if t and t != v:
                data[k] = t
                changed = True

                print(f"[{tgt_code}] {k}: {v[:40]!r} -> {t[:40]!r}")
            if sleep_s > 0:
                time.sleep(sleep_s)
        except Exception as e:
            print(f"[WARN] translate failed for key={k} in {os.path.basename(path)}: {e}", file=sys.stderr)

    if changed and not dry_run:
        save_json(path, data, backup=True)

def main():
    ap = argparse.ArgumentParser(description="Translate JSON language packs (values only), preserving keys.")
    ap.add_argument("--dir", required=True, help="Directory containing <code>.json packs (e.g., user_settings/i18n)")
    ap.add_argument("--provider", choices=["deepl","google"], default="google", help="Translation backend")
    ap.add_argument("--deepl-key", default=os.environ.get("DEEPL_API_KEY"), help="DeepL API key (for provider=deepl)")
    ap.add_argument("--source", default="en", help="Source language code (default: en)")
    ap.add_argument("--targets", default="all", help="Comma-separated targets (e.g., fr,de,ja) or 'all'")
    ap.add_argument("--skip-english", action="store_true", help="Heuristic: skip values that already look non-English")
    ap.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between calls (avoid rate limits)")
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing files")
    args = ap.parse_args()

    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}", file=sys.stderr)
        sys.exit(1)

    if args.targets.lower() == "all":
        targets = [c for c in ALL_CODES if c != args.source]
    else:
        targets = [c.strip() for c in args.targets.split(",") if c.strip()]

    src_path = os.path.join(args.dir, f"{args.source}.json")
    if not os.path.isfile(src_path):
        print(f"Source file missing: {src_path}", file=sys.stderr)
        sys.exit(1)

    src_data = load_json(src_path)

    for code in targets:
        path = os.path.join(args.dir, f"{code}.json")
        if not os.path.isfile(path):

            print(f"[INFO] Creating seed file for {code} from {args.source}")
            save_json(path, dict(src_data), backup=False)

    for code in targets:
        path = os.path.join(args.dir, f"{code}.json")
        print(f"\n=== Translating {os.path.basename(path)} ===")
        translate_file(
            path=path,
            provider=args.provider,
            deepl_key=args.deepl_key,
            src_code=args.source,
            tgt_code=code,
            skip_english=args.skip_english,
            sleep_s=args.sleep,
            dry_run=args.dry_run,
        )

    print("\nDone.")

if __name__ == "__main__":
    main()
