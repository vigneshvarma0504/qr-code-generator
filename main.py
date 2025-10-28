import argparse
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

import qrcode
from dotenv import load_dotenv

# --- env + paths ---
load_dotenv()  # loads .env if present

DEFAULT_URL = os.getenv("DEFAULT_URL", "http://github.com/kaw393939")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "qr_codes")
LOG_DIR = os.getenv("LOG_DIR", "logs")

# Ensure folders exist (works both on host and in container)
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# --- logging ---
log_file = Path(LOG_DIR) / "app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)]
)

def generate_qr(url: str, outdir: str = OUTPUT_DIR) -> Path:
    """Generate a QR PNG for the given URL."""
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL must start with http:// or https://")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = url.replace("://", "_").replace("/", "_")
    out_path = Path(outdir) / f"qr_{safe}_{ts}.png"

    img = qrcode.make(url)
    img.save(out_path)

    logging.info("Generated QR for %s -> %s", url, out_path)
    return out_path

def parse_args():
    parser = argparse.ArgumentParser(description="QR Code Generator")
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"URL to encode (default from env DEFAULT_URL or {DEFAULT_URL})"
    )
    parser.add_argument(
        "--outdir",
        default=OUTPUT_DIR,
        help=f"Directory to write PNGs (default from env OUTPUT_DIR or {OUTPUT_DIR})"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        path = generate_qr(args.url, args.outdir)
        print(f"OK: {path}")
    except Exception as e:
        logging.exception("Failed to generate QR")
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
