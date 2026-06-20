# Secrets Hand-Off

Use this reference when the user has not completed Aliyun or GitHub secret setup.

## Explain the Boundary First

Tell the user:

```text
接下来有两类事情：
1. 我可以做：整理官网文件、写部署配置、推 GitHub、触发部署、验收 URL。
2. 你必须亲自做：阿里云登录/实名/付款、创建或确认 AccessKey、把 Secret 填进 GitHub。

请不要把 AccessKey Secret 或 GitHub Token 发到聊天里。只在阿里云、GitHub 页面输入。
```

## Route A: EMAS No-Domain Preview

Use this when the user has no custom domain and mainly wants a public preview URL.

1. Ask the user to log in to Aliyun.
2. Open EMAS Serverless and create or choose a service space.
3. Confirm the service space status is active.
4. Open Static Website Hosting.
5. Upload or deploy the built static files.
6. Copy the default Aliyun URL and verify it with `verify_deployed_url.py`.

If Aliyun asks for payment or service activation, pause until the user completes it.

## Route B: OSS GitHub Actions Automation

Use this when the project already has an OSS bucket or the user wants CI deployment from GitHub.

1. Ask the user to log in to Aliyun.
2. Create or choose a dedicated RAM user for deployment.
3. Create an AccessKey for that RAM user.
4. Confirm the OSS bucket name and endpoint.
5. Open GitHub repository Settings > Secrets and variables > Actions.
6. Add the required secrets.

## Screenshot Assets

Resolve these paths relative to this skill folder and show them to the user when helpful:

- `assets/screenshots/ram-user-auth.png` - RAM user list and authorization entry.
- `assets/screenshots/accesskey-warning.png` - AccessKey creation risk warning.
- `assets/screenshots/github-secrets-entry.png` - GitHub Actions Secrets entry.
- `assets/screenshots/github-new-secret.png` - GitHub New repository secret form.

## Exact User Prompt

For OSS workflow, use wording like this:

```text
现在需要你手动完成密钥录入。请不要把 Secret 发到聊天里。

在 GitHub 仓库里打开 Settings > Secrets and variables > Actions > New repository secret，逐个新增：
1. ALIYUN_ACCESS_KEY_ID：填阿里云 AccessKey ID
2. ALIYUN_ACCESS_KEY_SECRET：填阿里云 AccessKey Secret
3. ALIYUN_OSS_BUCKET：填 OSS Bucket 名称
4. ALIYUN_OSS_ENDPOINT：填 endpoint，例如 oss-cn-hangzhou.aliyuncs.com
5. ALIYUN_SITE_URL：可选，填最终访问地址，例如 https://bucket.oss-cn-hangzhou.aliyuncs.com/index.html

填完告诉我“已填好”，我再继续触发部署和验收。
```

For EMAS manual upload, use wording like this:

```text
现在需要你在阿里云里完成登录、实名/付款确认，并进入 EMAS Serverless 静态网站托管。
我可以继续帮你检查文件和上线结果，但登录、付款、AccessKey 创建这些步骤必须由你亲自确认。

进入静态网站托管后，把页面里的默认访问地址发给我，或者告诉我“已进入上传页”，我继续帮你做下一步。
```

## Minimum Aliyun Permission

For a novice flow, prefer an isolated deployment RAM user. Grant only the bucket/upload/static-hosting permissions the project needs. If the user cannot configure fine-grained permissions, ask them to confirm the risk before using broader OSS permissions.
