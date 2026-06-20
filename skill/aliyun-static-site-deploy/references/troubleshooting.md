# Troubleshooting

## First Identify the Route

Before fixing anything, say which route is failing:

- EMAS no-domain preview: Aliyun console/static hosting/default URL issue.
- OSS GitHub Actions: GitHub Secrets/workflow/OSS bucket/metadata issue.
- GitHub push: local Git/token/network issue.

Do not mix EMAS and OSS fixes in the same explanation.

## Git Push Fails

- `git-lfs: command not found`: install Git LFS or bypass filters for inspection only. Do not claim the repo is clean until `git status` works or the LFS issue is fixed.
- `Invalid username or token`: username is the GitHub account name, password is a GitHub token. Do not paste tokens into the final answer.

## GitHub Actions Fails

- Missing secret: ask the user to add the exact missing GitHub Secret.
- `AccessDenied`: RAM user lacks OSS permissions or the bucket name/endpoint is wrong.
- `NoSuchBucket`: `ALIYUN_OSS_BUCKET` is wrong or in another account.
- `Connection refused` or timeout: retry once, then verify endpoint and region.

## URL Opens XML Error

- `NoSuchKey`: `index.html` was not uploaded to the root.
- `AccessDenied`: bucket/object is not publicly readable or static website access is not enabled.
- `UserDisable`: Aliyun account/resource is disabled or unpaid; ask the user to handle billing in Aliyun.

## Browser Downloads HTML

If this happens on an OSS default domain, tell the user clearly that OSS is serving the object like a file. Rerun the workflow once because it sets `Content-Type:text/html` and `Content-Disposition:inline`. If it still downloads, use EMAS static hosting or a custom domain/static website endpoint instead of repeatedly changing page code.

If this happens on EMAS, verify the uploaded file is actually an HTML file and not a zip, missing `index.html`, or wrong entry path.

## Videos Do Not Play

Prefer externally hosted video URLs for large media. If local videos are included, confirm GitHub file size limits, LFS availability, and OSS public access.

## Novice Explanation Pattern

Use this structure when reporting an error to a non-technical user:

1. `现在卡在：` one plain-language sentence.
2. `不是页面内容问题，而是：` account/permission/network/upload/URL.
3. `你要做：` the one action the user must take, if any.
4. `我继续做：` the next action Codex will perform after the user confirms.
