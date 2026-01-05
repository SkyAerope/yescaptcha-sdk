# YesCaptcha Python SDK

[YesCaptcha](https://yescaptcha.com) 验证码识别服务的 Python SDK。

[English](README_EN.md)

## 特性

- **异步 & 同步客户端** - 使用 `YesCaptchaClient` 异步或 `YesCaptchaClientSync` 同步
- **完整类型提示** - 使用 Pydantic 模型的完整类型注解
- **支持所有验证码类型**:
  - reCaptcha V2 / V2 隐形 / V2 企业版
  - reCaptcha V3 / V3 企业版
  - HCaptcha / HCaptcha 图像识别
  - Cloudflare Turnstile
  - 图片转文字 (OCR)
  - FunCaptcha 图像识别
  - CloudFlare 5秒盾

## 安装

```bash
pip install git+https://github.com/SkyAerope/yescaptcha-sdk.git
```

或先克隆仓库再以开发模式安装：

```bash
git clone https://github.com/SkyAerope/yescaptcha-sdk.git
cd yescaptcha-sdk
pip install -e .
```

## 快速开始

### 异步使用

```python
import asyncio
from yescaptcha import YesCaptchaClient, TurnstileTaskProxyless

async def main():
    # 使用国内节点
    async with YesCaptchaClient(
        client_key="YOUR_API_KEY",
        base_url="https://cn.yescaptcha.com"
    ) as client:
        # 查询余额
        balance = await client.get_balance()
        print(f"余额: {balance.balance}")
        
        # 识别 Turnstile 验证码
        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="0x4AAAAAAAB...",
        )
        solution = await client.solve(task)
        print(f"Token: {solution.token}")

asyncio.run(main())
```

### 同步使用

```python
from yescaptcha import YesCaptchaClientSync, NoCaptchaTaskProxyless

# 使用国内节点
client = YesCaptchaClientSync(
    client_key="YOUR_API_KEY",
    base_url="https://cn.yescaptcha.com"
)

# 识别 reCaptcha V2
task = NoCaptchaTaskProxyless(
    websiteURL="https://www.google.com/recaptcha/api2/demo",
    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
)
solution = client.solve(task)
print(f"Response: {solution.gRecaptchaResponse}")

client.close()
```

## 支持的任务类型

| 任务类型 | 类名 | 说明 |
|----------|------|------|
| reCaptcha V2 | `NoCaptchaTaskProxyless` | 标准 reCaptcha V2 |
| reCaptcha V2 企业版 | `RecaptchaV2EnterpriseTaskProxyless` | 企业版 reCaptcha V2 |
| reCaptcha V3 | `RecaptchaV3TaskProxyless` | 带 action 的 reCaptcha V3 |
| reCaptcha V3 企业版 | `RecaptchaV3EnterpriseTask` | 企业版 reCaptcha V3 |
| HCaptcha | `HCaptchaTaskProxyless` | HCaptcha 识别 |
| HCaptcha 图像识别 | `HCaptchaClassification` | HCaptcha 九宫格分类 |
| Turnstile | `TurnstileTaskProxyless` | Cloudflare Turnstile |
| 图片转文字 | `ImageToTextTask` | OCR 英文数字验证码 |
| FunCaptcha 图像识别 | `FunCaptchaClassification` | FunCaptcha 图像分类 |
| CloudFlare 5秒盾 | `CloudFlareTask` | CloudFlare 5秒盾 |

## API 文档

查看 [官方文档](https://yescaptcha.atlassian.net/wiki/spaces/YESCAPTCHA/pages/63897603/YesCaptcha+API) 获取详细的 API 信息。

## 开发

```bash
# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v
```

## License

Apache-2.0
