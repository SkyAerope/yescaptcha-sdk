# YesCaptcha Python SDK

A Python SDK for the [YesCaptcha](https://yescaptcha.com) captcha solving service.

[中文](README.md)

## Features

- **Async & Sync clients** - Use `YesCaptchaClient` for async or `YesCaptchaClientSync` for sync
- **Full type hints** - Complete type annotations with Pydantic models
- **All captcha types supported**:
  - reCaptcha V2 / V2 Invisible / V2 Enterprise
  - reCaptcha V3 / V3 Enterprise  
  - HCaptcha / HCaptcha Classification
  - Cloudflare Turnstile
  - Image to Text (OCR)
  - FunCaptcha Classification
  - CloudFlare 5s Shield

## Installation

```bash
pip install git+https://github.com/SkyAerope/yescaptcha-sdk.git
```

Or install from source code in development mode:

```bash
git clone https://github.com/SkyAerope/yescaptcha-sdk.git
cd yescaptcha-sdk
pip install -e .
```

## Quick Start

### Async Usage

```python
import asyncio
from yescaptcha import YesCaptchaClient, TurnstileTaskProxyless

async def main():
    async with YesCaptchaClient(client_key="YOUR_API_KEY") as client:
        # Check balance
        balance = await client.get_balance()
        print(f"Balance: {balance.balance}")
        
        # Solve a Turnstile captcha
        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="0x4AAAAAAAB...",
        )
        solution = await client.solve(task)
        print(f"Token: {solution.token}")

asyncio.run(main())
```

### Sync Usage

```python
from yescaptcha import YesCaptchaClientSync, NoCaptchaTaskProxyless

client = YesCaptchaClientSync(client_key="YOUR_API_KEY")

# Solve reCaptcha V2
task = NoCaptchaTaskProxyless(
    websiteURL="https://www.google.com/recaptcha/api2/demo",
    websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
)
solution = client.solve(task)
print(f"Response: {solution.gRecaptchaResponse}")

client.close()
```

## Supported Task Types

| Task Type | Class | Description |
|-----------|-------|-------------|
| reCaptcha V2 | `NoCaptchaTaskProxyless` | Standard reCaptcha V2 |
| reCaptcha V2 Enterprise | `RecaptchaV2EnterpriseTaskProxyless` | Enterprise reCaptcha V2 |
| reCaptcha V3 | `RecaptchaV3TaskProxyless` | reCaptcha V3 with action |
| reCaptcha V3 Enterprise | `RecaptchaV3EnterpriseTask` | Enterprise reCaptcha V3 |
| HCaptcha | `HCaptchaTaskProxyless` | HCaptcha solving |
| HCaptcha Classification | `HCaptchaClassification` | HCaptcha image classification |
| Turnstile | `TurnstileTaskProxyless` | Cloudflare Turnstile |
| Image to Text | `ImageToTextTask` | OCR for alphanumeric captchas |
| FunCaptcha Classification | `FunCaptchaClassification` | FunCaptcha image classification |
| CloudFlare 5s | `CloudFlareTask` | CloudFlare 5-second shield |

## API Reference

See the [official documentation](https://yescaptcha.atlassian.net/wiki/spaces/YESCAPTCHA/pages/64192513/YesCaptcha+Documentation) for detailed API information.

## Development

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## License

Apache-2.0
