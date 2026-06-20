#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


WORKFLOW = r'''name: Deploy static site to Aliyun OSS

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      OSSUTIL_VERSION: "1.7.18"

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Validate required secrets
        shell: bash
        run: |
          set -euo pipefail
          missing=0
          check_secret() {
            if [ -z "$2" ]; then
              echo "::error::Missing GitHub Secret: $1"
              missing=1
            fi
          }
          check_secret "ALIYUN_ACCESS_KEY_ID" "${{ secrets.ALIYUN_ACCESS_KEY_ID }}"
          check_secret "ALIYUN_ACCESS_KEY_SECRET" "${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}"
          check_secret "ALIYUN_OSS_BUCKET" "${{ secrets.ALIYUN_OSS_BUCKET }}"
          check_secret "ALIYUN_OSS_ENDPOINT" "${{ secrets.ALIYUN_OSS_ENDPOINT }}"
          exit "$missing"

      - name: Build or collect static files
        shell: bash
        run: |
          set -euo pipefail
          rm -rf site
          mkdir -p site

          if [ -f package.json ]; then
            if node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts.build ? 0 : 1)" >/dev/null 2>&1; then
              npm ci || npm install
              npm run build
            fi
          fi

          if [ -d dist ] && [ -f dist/index.html ]; then
            SOURCE_DIR="dist"
          elif [ -d build ] && [ -f build/index.html ]; then
            SOURCE_DIR="build"
          else
            SOURCE_DIR="."
          fi

          rsync -a "$SOURCE_DIR"/ site/ \
            --exclude='.git/' \
            --exclude='.github/' \
            --exclude='node_modules/' \
            --exclude='.DS_Store' \
            --exclude='output/' \
            --exclude='outputs/' \
            --exclude='site/' \
            --exclude='*.psd' \
            --exclude='*.ai' \
            --exclude='*.sketch'

          if [ ! -f site/index.html ]; then
            first_html="$(find site -maxdepth 2 -type f -name '*.html' | head -n 1 || true)"
            if [ -n "$first_html" ]; then
              cp "$first_html" site/index.html
            fi
          fi

          test -f site/index.html
          find site -maxdepth 3 -type f | sort | sed -n '1,120p'

      - name: Download ossutil
        shell: bash
        run: |
          set -euo pipefail
          wget "https://gosspublic.alicdn.com/ossutil/${OSSUTIL_VERSION}/ossutil64"
          chmod +x ossutil64

      - name: Configure ossutil
        shell: bash
        run: |
          set -euo pipefail
          ./ossutil64 config \
            -i "${{ secrets.ALIYUN_ACCESS_KEY_ID }}" \
            -k "${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}" \
            -e "${{ secrets.ALIYUN_OSS_ENDPOINT }}" \
            -c .ossutilconfig

      - name: Enable static website hosting
        shell: bash
        run: |
          set -euo pipefail
          cat > website.xml <<'EOF'
          <?xml version="1.0" encoding="UTF-8"?>
          <WebsiteConfiguration>
            <IndexDocument>
              <Suffix>index.html</Suffix>
            </IndexDocument>
            <ErrorDocument>
              <Key>index.html</Key>
            </ErrorDocument>
          </WebsiteConfiguration>
          EOF
          ./ossutil64 website --method put "oss://${{ secrets.ALIYUN_OSS_BUCKET }}" website.xml -c .ossutilconfig

      - name: Upload files
        shell: bash
        run: |
          set -euo pipefail
          ./ossutil64 cp -r -f site/ "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" -c .ossutilconfig

      - name: Set browser-friendly metadata
        shell: bash
        run: |
          set -euo pipefail
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:text/html#Content-Disposition:inline" --include "*.html" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:text/css#Content-Disposition:inline" --include "*.css" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:application/javascript#Content-Disposition:inline" --include "*.js" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:application/json#Content-Disposition:inline" --include "*.json" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:image/svg+xml#Content-Disposition:inline" --include "*.svg" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:image/png#Content-Disposition:inline" --include "*.png" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:image/jpeg#Content-Disposition:inline" --include "*.jpg" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:image/jpeg#Content-Disposition:inline" --include "*.jpeg" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:video/mp4#Content-Disposition:inline" --include "*.mp4" -r --update -c .ossutilconfig || true
          ./ossutil64 set-meta "oss://${{ secrets.ALIYUN_OSS_BUCKET }}/" "Content-Type:video/quicktime#Content-Disposition:inline" --include "*.mov" -r --update -c .ossutilconfig || true

      - name: Verify public URL when provided
        shell: bash
        run: |
          set -euo pipefail
          site_url="${{ secrets.ALIYUN_SITE_URL }}"
          if [ -z "$site_url" ]; then
            echo "ALIYUN_SITE_URL is optional and not set. Suggested object URL:"
            echo "https://${{ secrets.ALIYUN_OSS_BUCKET }}.${{ secrets.ALIYUN_OSS_ENDPOINT }}/index.html"
            exit 0
          fi
          curl -L --fail --max-time 30 -I "$site_url"
          curl -L --fail --max-time 30 "$site_url" | head -c 500 | grep -i "<html"
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a GitHub Actions workflow that deploys a static frontend to Aliyun OSS.")
    parser.add_argument("--project", default=".", help="Project root.")
    parser.add_argument("--workflow-name", default="deploy-aliyun-static-site.yml", help="Workflow file name.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing workflow file.")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    workflow_dir = root / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    target = workflow_dir / args.workflow_name

    if target.exists() and not args.force:
        print(f"EXISTS: {target}")
        print("Use --force to overwrite.")
        return 2

    target.write_text(WORKFLOW, encoding="utf-8")
    print(f"WROTE: {target}")
    print("Required GitHub Secrets: ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET, ALIYUN_OSS_BUCKET, ALIYUN_OSS_ENDPOINT")
    print("Optional GitHub Secret: ALIYUN_SITE_URL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
