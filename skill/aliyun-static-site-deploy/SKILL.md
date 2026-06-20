---
name: aliyun-static-site-deploy
description: Prepare and guide frontend static website deployment to Aliyun for a no-custom-domain preview. Use when Codex needs to inspect a local HTML/CSS/JS or built frontend project, prepare GitHub/GitHub Actions deployment assets, guide a novice through Aliyun EMAS or OSS setup, handle Aliyun login/payment/AccessKey/GitHub Secrets hand-off with screenshots, push or trigger deployment when credentials are ready, and verify that the public URL opens as a web page instead of downloading or showing XML errors.
---

# Aliyun Static Site Deploy

## Core Rules

- Treat **EMAS Serverless static hosting** as the default novice no-domain preview route. It gives the user an Aliyun default URL and avoids the common OSS default-domain download problem.
- Treat **OSS + GitHub Actions** as the repeatable automation route only when the user explicitly wants GitHub-to-Aliyun automation, already has or can create an OSS bucket, and understands that the final URL must be verified to open inline as HTML.
- Do not pretend Aliyun login, real-name verification, paid service activation, AccessKey creation, GitHub 2FA, or billing confirmation can be automated. Pause and ask the user to complete those steps.
- Never ask the user to paste `ALIYUN_ACCESS_KEY_SECRET`, GitHub tokens, passwords, or payment screenshots into chat. Ask them to type secrets directly into GitHub Secrets or the Aliyun/GitHub UI.

## First Decision

Before writing deployment code, decide the route and say it explicitly:

| Route | Use When | Automation Level | Risk |
| --- | --- | --- | --- |
| EMAS static hosting | No custom domain, novice preview, user can operate Aliyun console | Agent prepares files and guides console steps; user handles login/payment/upload if needed | Console UI may change and may require manual upload |
| OSS workflow | User wants Codex X GitHub X Aliyun automation; OSS bucket and AccessKey can be prepared | Agent can generate workflow, push code, trigger CI, and verify URL | OSS default domains can download HTML unless metadata/static hosting is correct |

If the user only says "没有域名先给客户看", use EMAS guidance first. If the user says "自动上线", "XgitX阿里云", "GitHub 自动部署", or "以后反复更新", use the OSS workflow scripts but explain the browser-download verification risk before proceeding.

## Workflow

1. Inspect the project:
   ```bash
   python3 /Users/likai/.codex/skills/aliyun-static-site-deploy/scripts/check_readiness.py --project .
   ```
2. Explain the deployment route in one sentence:
   - OSS: "用 GitHub Actions 上传到阿里云 OSS，并验证浏览器不是下载文件。"
   - EMAS: "先用阿里云 EMAS 静态托管拿到无域名预览地址。"
3. If the user has not prepared Aliyun access, read `references/secrets-hand-off.md` and ask them to complete Aliyun login/payment/AccessKey/GitHub Secrets. Use bundled screenshots when explaining where to click.
4. For OSS automation only, generate the GitHub Actions workflow:
   ```bash
   python3 /Users/likai/.codex/skills/aliyun-static-site-deploy/scripts/prepare_oss_workflow.py --project . --force
   ```
5. Verify the generated workflow and local project again:
   ```bash
   python3 /Users/likai/.codex/skills/aliyun-static-site-deploy/scripts/check_readiness.py --project . --strict
   ```
6. Commit/push the project to GitHub if the user asked for that and credentials are available. If Git LFS is installed incorrectly, use the script output to explain the fix instead of retrying blindly.
7. After deployment finishes, verify the public URL:
   ```bash
   python3 /Users/likai/.codex/skills/aliyun-static-site-deploy/scripts/verify_deployed_url.py "$ALIYUN_SITE_URL"
   ```

## Required GitHub Secrets

For the included OSS workflow, ask the user to create these repository secrets in GitHub:

- `ALIYUN_ACCESS_KEY_ID`
- `ALIYUN_ACCESS_KEY_SECRET`
- `ALIYUN_OSS_BUCKET`
- `ALIYUN_OSS_ENDPOINT`

Optional:

- `ALIYUN_SITE_URL` for deployment-time verification. Example: `https://your-bucket.oss-cn-hangzhou.aliyuncs.com/index.html`

For EMAS, use the exact secret names required by the EMAS deployment script in that project. If no EMAS script exists, do not invent fake secret names; guide the user through manual EMAS static hosting upload or create a project-specific script after confirming the official API/SDK path.

## Human Boundary

Stop and call the user when any of these are missing:

- Aliyun account is not logged in, not real-name verified, or asks for payment.
- EMAS service space, OSS bucket, or static hosting has not been created.
- AccessKey is not created.
- GitHub Secrets are not filled.
- GitHub asks for username/token or two-factor confirmation.

Show the user exact fields to fill, but do not receive secrets in chat.

## Deployment Success Criteria

Treat the deployment as incomplete until all checks pass:

- GitHub repository has a committed website source and deployment instructions.
- For OSS automation, GitHub repository has the generated workflow under `.github/workflows/deploy-aliyun-static-site.yml` and the Actions run succeeds on `main` or `workflow_dispatch`.
- For EMAS manual/static-hosting upload, the Aliyun console shows uploaded homepage files and a public default URL.
- The public URL returns HTTP 200 or 3xx followed by 200.
- The response is HTML, not XML error text or forced download metadata.
- The page contains `<html` and a non-empty title or visible body text.
- Key assets referenced by the homepage are public or remote URLs.

## References

- Read `references/secrets-hand-off.md` when the user needs step-by-step Aliyun/GitHub Secrets help.
- Read `references/troubleshooting.md` when deployment or URL verification fails.
