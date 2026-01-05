"""
YesCaptcha Python SDK

YesCaptcha 验证码识别服务的 Python SDK。

示例:

    >>> import asyncio
    >>> from yescaptcha import YesCaptchaClient
    >>>
    >>> async def main():
    ...     client = YesCaptchaClient(client_key="your-key")
    ...     balance = await client.get_balance()
    ...     print(f"余额: {balance.balance}")
    ...
    >>> asyncio.run(main())
"""

from yescaptcha.client import YesCaptchaClient, YesCaptchaClientSync
from yescaptcha.exceptions import (
    YesCaptchaError,
    TaskTimeoutError,
    InsufficientBalanceError,
    InvalidKeyError,
    TaskUnsolvableError,
    IPBlockedError,
    NoSlotAvailableError,
    TaskNotSupportedError,
)
from yescaptcha.models import (
    # 任务类型
    ImageToTextTask,
    NoCaptchaTaskProxyless,
    RecaptchaV3TaskProxyless,
    RecaptchaV2EnterpriseTaskProxyless,
    RecaptchaV3EnterpriseTask,
    HCaptchaTaskProxyless,
    HCaptchaClassification,
    TurnstileTaskProxyless,
    FunCaptchaClassification,
    CloudFlareTask,
    # 响应类型
    BalanceResponse,
    CreateTaskResponse,
    TaskResultResponse,
    Solution,
)

__version__ = "0.1.0"
__all__ = [
    # 客户端
    "YesCaptchaClient",
    "YesCaptchaClientSync",
    # 异常
    "YesCaptchaError",
    "TaskTimeoutError",
    "InsufficientBalanceError",
    "InvalidKeyError",
    "TaskUnsolvableError",
    "IPBlockedError",
    "NoSlotAvailableError",
    "TaskNotSupportedError",
    # 任务类型
    "ImageToTextTask",
    "NoCaptchaTaskProxyless",
    "RecaptchaV3TaskProxyless",
    "RecaptchaV2EnterpriseTaskProxyless",
    "RecaptchaV3EnterpriseTask",
    "HCaptchaTaskProxyless",
    "HCaptchaClassification",
    "TurnstileTaskProxyless",
    "FunCaptchaClassification",
    "CloudFlareTask",
    # 响应类型
    "BalanceResponse",
    "CreateTaskResponse",
    "TaskResultResponse",
    "Solution",
]
