# Aliyun Static Site Deploy Skill

这是一个 Codex Skill，用于把前端静态网页通过 GitHub Actions 自动上线到阿里云无域名访问地址。

## 仓库内容

- `skill/aliyun-static-site-deploy/`：Skill 源文件，可复制到 `~/.codex/skills/` 使用。
- `release/aliyun-static-site-deploy-skill.zip`：Skill 压缩包，已同步插入飞书教程文档。
- `docs/codex-git-aliyun-tutorial.md`：飞书教程文档 Markdown 导出。
- `docs/codex-git-aliyun-tutorial.xml`：飞书教程文档 XML 导出，保留飞书结构块。
- `docs/feishu-doc-url.txt`：飞书文档链接。

## 使用方式

1. 解压 `release/aliyun-static-site-deploy-skill.zip`。
2. 将 `aliyun-static-site-deploy` 文件夹放到 `~/.codex/skills/`。
3. 在 Codex 中说：`使用 $aliyun-static-site-deploy 帮我把这个前端网页自动上线到阿里云无域名地址`。

## 人工边界

Skill 不会自动处理阿里云登录、实名认证、付费、AccessKey 创建或 GitHub Secrets 填写。遇到这些步骤时，代理会停下来，并用截图引导使用者自己完成。

## 教程文档

飞书教程：

https://rcnoc1fzg33a.feishu.cn/docx/UPsHdVbQcoZ3rlxBuWXcMGcun1e
