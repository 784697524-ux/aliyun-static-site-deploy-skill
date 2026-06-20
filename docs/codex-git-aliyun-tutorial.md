<title>保姆级教程：Codex X Git X 阿里云开发官网</title>

<callout emoji="📌">
**这篇教程只讲一件事：**一个小白怎么从 0 做出官网，并把它上线到阿里云。你不用先学完前端、服务器和运维，只要照着这篇文档一步一步做。
阅读方式也很简单：每一步先看“大白话解释”，再看后台截图，最后照着“这一页你要填什么”去做。
</callout>

# 一、先看懂全流程：你到底在做什么

做官网上线，不是一下子完成的。它其实是 6 个动作串起来：

<whiteboard token="KTKxwjjCihiwXkbdcdRcxtsUn5f"></whiteboard>

| 工具 | 大白话解释 | 你用它做什么 |
|-|-|-|
| Codex | 帮你写代码的开发同事 | 生成官网、改页面、写部署脚本 |
| GitHub | 代码仓库 | 保存官网代码，让自动部署能拿到最新代码 |
| 阿里云 EMAS | 放官网文件的线上空间 | 无域名阶段也能先有一个可打开的地址 |
| GitHub Secrets | 密钥保险箱 | 保存阿里云密钥，不把密钥写进代码 |
| GitHub Actions | 自动跑部署任务的机器人 | 推代码后自动上传官网文件 |

---

# 二、开始前先准备 4 样东西

先把账号和文件准备好，后面就不会做到一半卡住。

| 准备项 | 你要确认什么 | 卡住时怎么办 |
|-|-|-|
| 1. Codex 可用 | 能让 Codex 读写本地官网文件 | 先用一句话让它改个文字测试 |
| 2. GitHub 账号 | 能创建仓库，能 push 代码 | 密码不能 push 时，用 GitHub Token |
| 3. 阿里云账号 | 已登录控制台，能打开 EMAS 和 RAM | 先完成实名认证和必要开通 |
| 4. 官网文件夹 | 里面有 index.html、官网 HTML、assets 等文件 | 让 Codex 先整理项目结构 |

<callout emoji="💡">
**安全底线：**AccessKey、GitHub Token、密码都不要放进文档正文、聊天记录和代码文件。密钥只放 GitHub Secrets。
</callout>

---

# 三、让 Codex 先做出官网初版

你不需要自己写代码。你要先把官网目标讲清楚，让 Codex 生成第一版页面。

```text
请帮我做一个官网页面，主题是“本地生活 AI 获客系统”。
要求：
1. 第一屏说清楚产品能帮客户解决什么问题。
2. 有功能模块、适合客户、价格方案、案例证明、视频演示、联系方式。
3. 页面可以本地打开，也可以部署到阿里云静态托管。
4. 不要写成营销空话，要像真实产品官网。
5. 做完后告诉我本地怎么预览。
```

| 你要看什么 | 合格标准 |
|-|-|
| 首屏 | 3 秒内知道你卖什么、帮谁解决什么问题 |
| 功能 | 每个功能都讲清楚应用场景，不只写名词 |
| 价格 | 基础价、试用价、托管价或定制价讲清楚 |
| 证据 | 有案例、截图、视频或媒体报道支撑 |

---

# 四、本地预览：先在自己电脑看满意

上线前先本地预览。不要一边上线一边改样式，小白很容易把问题搞混。

```bash
cd 你的官网文件夹
python3 -m http.server 8010
```

然后在浏览器打开：

```text
http://127.0.0.1:8010
```

- [ ] 我已经能在本地浏览器打开官网

- [ ] 首屏没有文字重叠

- [ ] 手机宽度下也能正常看

- [ ] 图片和视频能打开

---

# 五、把官网代码放到 GitHub

GitHub 是代码仓库。后面无论用 EMAS、OSS 还是其他静态托管，最好都从 GitHub 管代码。

```bash
cd 你的官网文件夹
git init
git add .
git commit -m "init website"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

<callout emoji="❗">
如果 GitHub 让你输入密码：用户名填 GitHub 用户名，密码位置填 GitHub Token，不要填 GitHub 登录密码。
</callout>

| 报错 | 原因 | 处理办法 |
|-|-|-|
| SSL_ERROR_SYSCALL | 连 GitHub 不稳定 | 开代理，或切 HTTP/1.1 重试 |
| Invalid username or token | 用户名或 Token 错 | 用户名填账号名，密码填 Token |
| HTTP2 framing layer | 连接中途断开 | 加代理，或重新 push |

---

# 六、阿里云 EMAS：先准备能放官网的空间

没有域名时，先用阿里云 EMAS 的静态网站托管做预览。后面有域名了，再绑定自定义域名。

## 6.1 进入 EMAS 产品页

打开阿里云控制台，搜索或进入“移动研发平台 EMAS”。如果你还没建应用，点“立即添加应用”；如果已经有空间，点 Serverless 或右上角“接入”。

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YWE1ZmExNGE0YTE4M2M5M2MzOWY2NTU0Mzc1OTEzODJfZTRlY2NiMjljNDY1Yzk2MDVjMDg4Y2E2YzA2NmE4OTVfSUQ6NzY1MzQ3NDcxMzIxNzQ2OTY1OV8xNzgxOTY4NjM3OjE3ODE5NzIyMzdfVjM)

| 这一页你要做什么 | 说明 |
|-|-|
| 新项目 | 点“立即添加应用” |
| 已有空间 | 点 Serverless 或右上角“接入” |
| 目标 | 进入 EMAS Serverless 服务空间 |

## 6.2 服务空间概览页

服务空间就是官网在线运行的房间。先确认空间状态是“服务中”，再复制空间 ID。

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=M2IwYzVmZGM3MTYwODVhMGRmMDI3NDI4ZjJkYWU0YzlfNWJjYzc2NzFkMzMwNTFjNjI5OGJlNTRiMDUwZDU2YmVfSUQ6NzY1MzQ3NDcxNTYyMDgwNTg0MV8xNzgxOTY4NjM3OjE3ODE5NzIyMzdfVjM)

| 这一页你要看什么 | 合格标准 |
|-|-|
| 空间状态 | 必须是“服务中” |
| 空间 ID | 复制保存，后续脚本可能用到 |
| 下一步 | 左侧点“静态网站托管” |

## 6.3 静态网站托管页

这里就是放官网文件的地方。手动上线时点“上传文件”；自动上线时，GitHub Actions 会替你上传。

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NmU1MDMwM2I1NjU0MDJiZjI0ODk4Yjk0NDEwNWNmNGNfOTZiM2U5YjM1MTcxZDNlMjk0MDBiNDJiMzE1OTdkY2JfSUQ6NzY1MzQ3NDcxNTUzNjg3MDU5NF8xNzgxOTY4NjM3OjE3ODE5NzIyMzdfVjM)

| 你要知道的入口 | 用途 |
|-|-|
| 文件 | 看已上传的 HTML、图片、JS 文件 |
| 上传文件 | 手动上传官网文件 |
| 设置 | 看访问地址、默认首页、域名配置 |

<callout emoji="✅">
小白先跑通手动上传也可以。等页面能打开了，再做 GitHub Actions 自动部署。
</callout>

---

# 七、阿里云密钥：创建 RAM 用户和 AccessKey

GitHub Actions 要把文件上传到阿里云，必须有一把钥匙。不要优先用主账号钥匙，建议创建部署专用 RAM 用户。

## 7.1 创建或选择 RAM 用户

进入 RAM 访问控制，左侧点“身份管理 > 用户”。新手建议创建一个“只用于官网部署”的用户。

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDAyNTdjNmNmNDYxYTdjNTMwNmI0YjI3MGE2MTRkYzFfYmIwZWZlMzU2OWQzY2Y0NzRkNDdjMTgyM2I0MjM3MDFfSUQ6NzY1MzQ3NDcxODQzMDk0MDM0MV8xNzgxOTY4NjM3OjE3ODE5NzIyMzdfVjM)

| 这一页怎么点 | 说明 |
|-|-|
| 创建用户 | 没有部署用户时先创建 |
| 点用户名称 | 进入用户详情，后面创建 AccessKey |
| 新增授权 | 给这个用户上传官网文件所需权限 |

## 7.2 创建 AccessKey

AccessKey ID 和 AccessKey Secret 就像账号和密码。Secret 通常只完整显示一次，复制后马上保存到 GitHub Secrets。

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OWQ1MTE5NWEzYjMzNDJjZmMyZmNkYTgxYjAxNzBlZmJfMGQxN2YzMzIzY2FlNzQzNDY3ZWMxNDJkNGM1OTkyYjRfSUQ6NzY1MzQ3NDcxNjgzMjk0MzMwMl8xNzgxOTY4NjM3OjE3ODE5NzIyMzdfVjM)

| 看到什么 | 该怎么做 |
|-|-|
| 提示不建议主账号 AK | 优先点“使用 RAM 用户 AccessKey” |
| 确实要用主账号 | 才勾选风险确认继续 |
| 创建成功 | 复制 AccessKey ID 和 Secret |

<callout emoji="💡">
不要把 Secret 截图发给别人。不要写进代码。不要放进飞书正文。只放 GitHub Secrets。
</callout>

---

# 八、把阿里云密钥填进 GitHub Secrets

GitHub Secrets 是密钥保险箱。代码里只写变量名，真实密钥藏在 GitHub 后台。

## 8.1 找到 Secrets 页面

打开你的 GitHub 仓库，点 Settings，再从左侧进入 Actions 的 Secrets 页面。

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZDExMDBlOGIxYjM1MmJlMjg1NDU1YzJiNDA5M2Y1MDVfNjc1NWRhYzNkODBiYzE5ZGY2YzgxYWM2YzMxYjkxZjNfSUQ6NzY1MzQ3NDcxNzQyODc4MDI3NV8xNzgxOTY4NjM3OjE3ODE5NzIyMzdfVjM)

| 路径 | 说明 |
|-|-|
| 仓库顶部 Settings | 进入仓库设置 |
| 左侧 Secrets and variables | 如果没看到，先展开 Actions |
| Actions > Secrets | 这里保存自动部署密钥 |

## 8.2 新增 Secret：Name 和 Secret 不要填反

这里最容易错。Name 填固定变量名，Secret 填真实值。

![](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=N2RiMmZhNDRhYWFjZTFlOTQwZmZjZDM2NmUxY2ZkZDFfZjkzN2JmZTFhNDc5Y2UxODgxOTFkZTIyZDY0NDcwOTBfSUQ6NzY1MzQ3NDcxOTI1MzA1NjY5OF8xNzgxOTY4NjM3OjE3ODE5NzIyMzdfVjM)

| 第几次添加 | Name 填什么 | Secret 填什么 |
|-|-|-|
| 第 1 个 | ALIYUN_ACCESS_KEY_ID | 阿里云 AccessKey ID |
| 第 2 个 | ALIYUN_ACCESS_KEY_SECRET | 阿里云 AccessKey Secret |
| 第 3 个 | ALIYUN_OSS_BUCKET | 你的 OSS Bucket 名，例如 chengkegaunwang |
| 第 4 个 | ALIYUN_OSS_ENDPOINT | 地域 endpoint，例如 oss-cn-hangzhou.aliyuncs.com |

<callout emoji="📌">
你的当前仓库里已有部署到 OSS 的 workflow，所以需要上面 4 个 Secret。如果后面改成 EMAS 专用脚本，变量名要以 workflow 文件里的 `secrets.xxx` 为准，名字必须一字不差。
</callout>

---

# 九、写自动部署配置

自动部署配置就是 GitHub Actions 的 workflow 文件。它会在你 push 代码后自动执行。

你现在仓库里的 workflow 路径是：

```text
.github/workflows/deploy-site.yml
```

```yaml
ALIYUN_ACCESS_KEY_ID: ${{ secrets.ALIYUN_ACCESS_KEY_ID }}
ALIYUN_ACCESS_KEY_SECRET: ${{ secrets.ALIYUN_ACCESS_KEY_SECRET }}
ALIYUN_OSS_BUCKET: ${{ secrets.ALIYUN_OSS_BUCKET }}
ALIYUN_OSS_ENDPOINT: ${{ secrets.ALIYUN_OSS_ENDPOINT }}
```

<callout emoji="❗">
如果 Actions 报 `secret not found`，先检查 GitHub Secrets 里的 Name 是否和 workflow 完全一样。大小写、下划线、拼写都不能错。
</callout>

---

# 十、推送代码，等待自动上线

改完官网以后，提交并推送到 main 分支。推送成功后，GitHub Actions 会自动开始部署。

```bash
git add .
git commit -m "update website"
git push
```

| 看到什么 | 说明 |
|-|-|
| Actions 绿色对勾 | 部署任务成功 |
| 红色叉号 | 点进去看失败日志 |
| 一直排队 | 等一会儿刷新，或检查 GitHub Actions 是否启用 |

---

# 十一、上线后怎么验收

不要只看电脑浏览器。至少做下面几项。

- [ ] 电脑浏览器能打开首页

- [ ] 手机 4G/5G 能打开首页

- [ ] 刷新页面不会 404

- [ ] 图片和视频能加载

- [ ] 联系方式、二维码、按钮能看到

- [ ] 价格、案例、媒体报道没有断链

<bookmark name="示例：已上线的阿里云官网地址" href="https://static-mp-e64ce04f-c34d-4ee6-9bb4-6a395b780ae1.next.bspapp.com/%E6%9C%AC%E5%9C%B0%E7%94%9F%E6%B4%BBAI%E8%8E%B7%E5%AE%A2%E7%B3%BB%E7%BB%9F%E5%AE%98%E7%BD%91.html"></bookmark>

---

# 十二、常见问题：先按这个表排查

| 问题 | 最可能原因 | 怎么排查 |
|-|-|-|
| Actions 提示 secret not found | Secret 名字填错或少填 | 回 GitHub Secrets 核对大小写和下划线 |
| 阿里云上传失败 | AccessKey 权限不够 | 检查 RAM 用户授权 |
| 页面打开变下载 HTML | OSS 默认域名策略或响应头问题 | 无域名阶段优先用 EMAS 静态托管地址 |
| 页面能开但图片视频不显示 | 资源路径或权限问题 | 单独打开图片/视频 URL，看是否能访问 |
| GitHub push 失败 | 网络或 Token 问题 | 开代理，用户名填账号，密码填 Token |

---

# 十三、小白照抄版完整检查清单

- [ ] 我已经让 Codex 做出官网初版

- [ ] 我已经本地预览并改到满意

- [ ] 我已经把官网代码推到 GitHub

- [ ] 我已经进入阿里云 EMAS Serverless

- [ ] 我已经确认服务空间是“服务中”

- [ ] 我已经进入静态网站托管并知道上传入口

- [ ] 我已经创建或选择 RAM 用户

- [ ] 我已经创建 AccessKey，并没有把 Secret 发给别人

- [ ] 我已经在 GitHub Secrets 配好 4 个变量

- [ ] 我已经推送 main 分支并看到 Actions 成功

- [ ] 我已经用电脑和手机打开最终网址

---

# 十四、官方参考链接

后台界面以后可能改版。界面变了就看官方文档，但逻辑不变：先准备托管空间，再准备受控密钥，最后把密钥放进 GitHub Secrets。

<bookmark name="阿里云：创建 AccessKey" href="https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair"></bookmark>

<bookmark name="阿里云：开通 EMAS 静态网站托管" href="https://help.aliyun.com/zh/document_detail/435874.html"></bookmark>

<bookmark name="阿里云：上传静态网站文件" href="https://help.aliyun.com/zh/document_detail/435877.html"></bookmark>

<bookmark name="GitHub：在 Actions 中使用 Secrets" href="https://docs.github.com/actions/security-guides/using-secrets-in-github-actions"></bookmark>

---

# 十五、自动上线 Skill 文件

<callout emoji="✅">
**已补充可复用 Skill：**这个 Skill 会把“前端网页 → GitHub → 阿里云 OSS 无域名上线 → URL 验收”的流程固化下来。小白使用时，代理会自动生成部署配置、检查项目、引导填写 GitHub Secrets，并在上线后验证页面是否真的能打开。
</callout>

| 交付物 | 用途 |
|-|-|
| aliyun-static-site-deploy-skill.zip | Codex Skill 压缩包，包含 SKILL.md、脚本、参考文档和密钥填写截图。 |
| GitHub 同步仓库 | 保存教程导出文件、Skill 源文件和 Skill 压缩包，便于后续版本管理。 |

<bookmark name="GitHub 仓库：aliyun-static-site-deploy-skill" href="https://github.com/784697524-ux/aliyun-static-site-deploy-skill"></bookmark>

下方附件就是本次生成的 Skill 压缩包。

<figure view-type="Card"><source href="https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MTI5MWQwYmIwNGJlOTFkZTY0MTllZjZkM2Y2MjA2MGFfMDg2ZDc2YjJkZjM2YWFkYTg3MDEzYzQyNGZkYmFiMWNfSUQ6NzY1MzQ5NzEyNzAyODY5MDEyOV8xNzgxOTY4NzAxOjE3ODE5NzIzMDFfVjM" mime="application/zip" token="G2RjbiA8Vo1Gu7xJXAGc5kVCnlg"/></figure>