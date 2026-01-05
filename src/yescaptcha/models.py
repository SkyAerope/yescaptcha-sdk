"""
YesCaptcha API 请求和响应的 Pydantic 模型。

本模块定义 SDK 使用的所有任务类型和响应模型。
"""

from typing import Literal, Optional, Union, Any
from pydantic import BaseModel, Field


# =============================================================================
# 任务类型
# =============================================================================


class ImageToTextTask(BaseModel):
    """
    图片转文字验证码任务（OCR 识别英文数字验证码）。

    属性:
        type: 任务类型标识符。
              - ImageToTextTaskMuggle: 2 点/次，同步返回结果
              - ImageToTextTaskM1: 15 点/次，异步任务需要轮询
        body: Base64 编码的图片内容（不含 data:image/xxx;base64, 前缀）。
        project_name: 可选的自定义模型名称，用于特定验证码识别。
    """

    type: Literal["ImageToTextTask", "ImageToTextTaskMuggle", "ImageToTextTaskM1"] = "ImageToTextTaskMuggle"
    body: str = Field(..., description="Base64 编码的图片内容")
    project_name: Optional[str] = Field(None, alias="project_name")

    model_config = {"populate_by_name": True}


class NoCaptchaTaskProxyless(BaseModel):
    """
    reCaptcha V2 无代理任务。

    属性:
        type: 任务类型标识符。
              - NoCaptchaTaskProxyless: 15 点/次
              - RecaptchaV2TaskProxyless: 20 点/次（备选架构）
        websiteURL: 包含 reCaptcha 的页面 URL。
        websiteKey: reCaptcha 网站密钥。
        isInvisible: 是否为隐形 reCaptcha 类型。
    """

    type: Literal["NoCaptchaTaskProxyless", "RecaptchaV2TaskProxyless"] = "NoCaptchaTaskProxyless"
    websiteURL: str
    websiteKey: str
    isInvisible: bool = False


class RecaptchaV2EnterpriseTaskProxyless(BaseModel):
    """
    reCaptcha V2 企业版无代理任务。

    属性:
        type: 任务类型标识符。
        websiteURL: 包含 reCaptcha 的页面 URL。
        websiteKey: reCaptcha 网站密钥。
        enterprisePayload: 可选的企业版特定载荷。
    """

    type: Literal["RecaptchaV2EnterpriseTaskProxyless"] = "RecaptchaV2EnterpriseTaskProxyless"
    websiteURL: str
    websiteKey: str
    enterprisePayload: Optional[dict[str, Any]] = None


class RecaptchaV3TaskProxyless(BaseModel):
    """
    reCaptcha V3 无代理任务。

    属性:
        type: 任务类型标识符。
              - RecaptchaV3TaskProxyless: 20 点/次
              - RecaptchaV3TaskProxylessM1: 25 点/次（备选架构）
        websiteURL: 包含 reCaptcha 的页面 URL。
        websiteKey: reCaptcha 网站密钥。
        pageAction: reCaptcha V3 的 action 值，必须正确否则结果无效。
    """

    type: Literal["RecaptchaV3TaskProxyless", "RecaptchaV3TaskProxylessM1"] = "RecaptchaV3TaskProxyless"
    websiteURL: str
    websiteKey: str
    pageAction: str


class RecaptchaV3EnterpriseTask(BaseModel):
    """
    reCaptcha V3 企业版任务。

    属性:
        type: 任务类型标识符。
        websiteURL: 包含 reCaptcha 的页面 URL。
        websiteKey: reCaptcha 网站密钥。
        pageAction: reCaptcha V3 的 action 值。
        enterprisePayload: 可选的企业版特定载荷。
    """

    type: Literal["RecaptchaV3EnterpriseTask", "RecaptchaV3EnterpriseTaskProxyless"] = "RecaptchaV3EnterpriseTask"
    websiteURL: str
    websiteKey: str
    pageAction: str
    enterprisePayload: Optional[dict[str, Any]] = None


class HCaptchaTaskProxyless(BaseModel):
    """
    HCaptcha 无代理任务。

    属性:
        type: 任务类型标识符。
        websiteURL: 包含 HCaptcha 的页面 URL。
        websiteKey: HCaptcha 网站密钥。
    """

    type: Literal["HCaptchaTaskProxyless"] = "HCaptchaTaskProxyless"
    websiteURL: str
    websiteKey: str


class HCaptchaClassification(BaseModel):
    """
    HCaptcha 图像分类任务（九宫格识别）。

    属性:
        type: 任务类型标识符。8 点/次。
        queries: Base64 编码的图片列表（九张小图）。
        question: 可选的问题 ID。
        anchors: 可选的辅助小图（九宫格右上角的参考图）。
    """

    type: Literal["HCaptchaClassification"] = "HCaptchaClassification"
    queries: list[str] = Field(..., description="Base64 编码的图片列表")
    question: Optional[str] = None
    anchors: Optional[list[str]] = None


class ReCaptchaV2Classification(BaseModel):
    """
    reCaptcha V2 图像分类任务。

    属性:
        type: 任务类型标识符。
        image: Base64 编码的图片内容。
        question: 分类问题 ID。
    """

    type: Literal["ReCaptchaV2Classification"] = "ReCaptchaV2Classification"
    image: str = Field(..., description="Base64 编码的图片内容")
    question: str


class FunCaptchaClassification(BaseModel):
    """
    FunCaptcha 图像分类任务。

    属性:
        type: 任务类型标识符。
        images: Base64 编码的图片列表。
        question: 分类问题。
    """

    type: Literal["FunCaptchaClassification"] = "FunCaptchaClassification"
    images: list[str] = Field(..., description="Base64 编码的图片列表")
    question: str


class TurnstileTaskProxyless(BaseModel):
    """
    Cloudflare Turnstile 无代理任务。

    属性:
        type: 任务类型标识符。
              - TurnstileTaskProxyless: 25 点/次
              - TurnstileTaskProxylessM1: 30 点/次（备选架构）
        websiteURL: 包含 Turnstile 的页面 URL。
        websiteKey: Turnstile 网站密钥。
    """

    type: Literal["TurnstileTaskProxyless", "TurnstileTaskProxylessM1"] = "TurnstileTaskProxyless"
    websiteURL: str
    websiteKey: str


class CloudFlareTask(BaseModel):
    """
    CloudFlare 5秒盾任务（不推荐使用，质量较差）。

    属性:
        type: 任务类型标识符。
              - CloudFlareTaskS2: 25 点/次
              - CloudFlareTaskS3: 20 点/次
        websiteURL: 需要识别的页面 URL。
        proxy: 代理地址，格式：http://user:pass@ip:port 或 socks5://ip:port。
        userAgent: 可选的自定义 UA（仅 CloudFlareTaskS2 支持）。
        waitLoad: 是否等待页面完全加载。
        requiredCookies: 需要获取的 cookie 名称列表。
        blockImage: 是否阻止图片加载以节省流量。
        postData: 可选的 POST 数据。
    """

    type: Literal["CloudFlareTaskS2", "CloudFlareTaskS3"] = "CloudFlareTaskS3"
    websiteURL: str
    proxy: str
    userAgent: Optional[str] = None
    waitLoad: bool = False
    requiredCookies: Optional[list[str]] = None
    blockImage: bool = False
    postData: Optional[dict[str, Any]] = None


# 所有支持的任务类型联合
Task = Union[
    ImageToTextTask,
    NoCaptchaTaskProxyless,
    RecaptchaV2EnterpriseTaskProxyless,
    RecaptchaV3TaskProxyless,
    RecaptchaV3EnterpriseTask,
    HCaptchaTaskProxyless,
    HCaptchaClassification,
    ReCaptchaV2Classification,
    FunCaptchaClassification,
    TurnstileTaskProxyless,
    CloudFlareTask,
]


# =============================================================================
# 响应模型
# =============================================================================


class Solution(BaseModel):
    """
    包含验证码识别结果的对象。

    不同任务类型返回不同的字段。
    """

    # reCaptcha / HCaptcha 响应令牌
    gRecaptchaResponse: Optional[str] = None

    # Turnstile 令牌
    token: Optional[str] = None

    # 图片转文字结果
    text: Optional[str] = None

    # HCaptcha 分类结果（选中图片的索引列表）
    objects: Optional[list[int]] = None

    # CloudFlare 任务结果
    cookies: Optional[dict[str, str]] = None
    userAgent: Optional[str] = None
    content: Optional[str] = None

    # 允许额外字段以保持扩展性
    model_config = {"extra": "allow"}


class CreateTaskResponse(BaseModel):
    """
    createTask API 的响应。

    属性:
        errorId: 0 表示成功，1 表示错误。
        errorCode: 错误码字符串（errorId 为 1 时存在）。
        errorDescription: 人类可读的错误描述。
        taskId: 创建的任务 ID（仅成功时存在）。
    """

    errorId: int
    errorCode: Optional[str] = None
    errorDescription: Optional[str] = None
    taskId: Optional[str] = None


class TaskResultResponse(BaseModel):
    """
    getTaskResult API 的响应。

    属性:
        errorId: 0 表示成功，1 表示错误。
        errorCode: 错误码字符串（errorId 为 1 时存在）。
        errorDescription: 人类可读的错误描述。
        status: "processing" 表示识别中，"ready" 表示完成。
        solution: 识别结果对象（仅 status 为 "ready" 时存在）。
    """

    errorId: int
    errorCode: Optional[str] = None
    errorDescription: Optional[str] = None
    status: Optional[Literal["processing", "ready"]] = None
    solution: Optional[Solution] = None


class BalanceResponse(BaseModel):
    """
    getBalance API 的响应。

    属性:
        errorId: 0 表示成功，1 表示错误。
        errorCode: 错误码字符串（errorId 为 1 时存在）。
        errorDescription: 人类可读的错误描述。
        balance: 账户余额（点数，1元=1000点）。
        softBalance: 开发者分成余额。
        inviteBalance: 邀请分成余额。
        inviteBy: 邀请人账户 ID。
    """

    errorId: int
    errorCode: Optional[str] = None
    errorDescription: Optional[str] = None
    balance: Optional[float] = None
    softBalance: Optional[float] = None
    inviteBalance: Optional[float] = None
    inviteBy: Optional[str] = None
