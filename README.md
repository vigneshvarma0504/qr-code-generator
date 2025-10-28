# QR Code Generator (Dockerized)

## What this does
Generates QR PNG files from a URL. Defaults can come from env vars or CLI flags.

## Quick start (Docker)
```bash
docker build -t qr-code-generator-app .
# PowerShell: map host folder to container output folder
mkdir qr_codes
docker run --rm --name qr-generator `
  -v ${PWD}\qr_codes:/app/qr_codes `
  qr-code-generator-app --url https://www.njit.edu
