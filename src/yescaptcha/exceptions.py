"""
YesCaptcha SDK 自定义异常。

将 API 错误码映射到具体的异常类，便于错误处理。
"""

from typing import Optional


class YesCaptchaError(Exception):
    """YesCaptcha SDK 所有错误的基类。"""

    def __init__(
        self,
        error_id: int,
        error_code: Optional[str] = None,
        error_description: Optional[str] = None,
    ):
        self.error_id = error_id
        self.error_code = error_code
        self.error_description = error_description
        message = f"[{error_code}] {error_description}" if error_code else error_description
        super().__init__(message)


class TaskTimeoutError(YesCaptchaError):
    """任务识别超时时抛出 (ERROR_TASK_TIMEOUT)。"""

    pass


class InsufficientBalanceError(YesCaptchaError):
    """账户余额不足时抛出 (ERROR_ZERO_BALANCE)。"""

    pass


class InvalidKeyError(YesCaptchaError):
    """客户端密钥无效时抛出 (ERROR_KEY_DOES_NOT_EXIST)。"""

    pass


class TaskUnsolvableError(YesCaptchaError):
    """验证码无法识别时抛出 (ERROR_CAPTCHA_UNSOLVABLE)。不会扣费。"""

    pass


class IPBlockedError(YesCaptchaError):
    """IP 因过多错误请求被屏蔽时抛出 (ERROR_IP_BLOCKED_5MIN, ERROR_IP_BANNED)。"""

    pass


class NoSlotAvailableError(YesCaptchaError):
    """服务器资源不足时抛出 (ERROR_NO_SLOT_AVAILABLE)。请稍后重试。"""

    pass


class TaskNotSupportedError(YesCaptchaError):
    """任务类型不支持时抛出 (ERROR_TASK_NOT_SUPPORTED)。"""

    pass


class InvalidTaskIdError(YesCaptchaError):
    """任务 ID 无效或已过期时抛出 (ERROR_TASKID_INVALID)。"""

    pass


class BadRequestError(YesCaptchaError):
    """请求格式错误时抛出 (ERROR_BAD_REQUEST)。"""

    pass


class ServiceUnavailableError(YesCaptchaError):
    """服务暂时不可用时抛出 (ERROR_SERVICE_UNAVALIABLE)。"""

    pass


# API 错误码到异常类的映射
ERROR_CODE_MAP: dict[str, type[YesCaptchaError]] = {
    "ERROR_TASK_TIMEOUT": TaskTimeoutError,
    "ERROR_ZERO_BALANCE": InsufficientBalanceError,
    "ERROR_KEY_DOES_NOT_EXIST": InvalidKeyError,
    "ERROR_CAPTCHA_UNSOLVABLE": TaskUnsolvableError,
    "ERROR_IP_BLOCKED_5MIN": IPBlockedError,
    "ERROR_IP_BANNED": IPBlockedError,
    "ERROR_NO_SLOT_AVAILABLE": NoSlotAvailableError,
    "ERROR_NO_SLOT_AVAILABLE_BLOCK": NoSlotAvailableError,
    "ERROR_TASK_NOT_SUPPORTED": TaskNotSupportedError,
    "ERROR_TASKID_INVALID": InvalidTaskIdError,
    "ERROR_NO_SUCH_CAPCHA_ID": InvalidTaskIdError,
    "ERROR_BAD_REQUEST": BadRequestError,
    "ERROR_SERVICE_UNAVALIABLE": ServiceUnavailableError,
}


def raise_for_error(error_id: int, error_code: Optional[str], error_description: Optional[str]) -> None:
    """
    根据错误响应抛出相应的异常。

    参数:
        error_id: API 响应中的错误 ID（0 = 无错误，1 = 有错误）。
        error_code: API 响应中的错误码字符串。
        error_description: API 响应中的错误描述。

    异常:
        YesCaptchaError: 根据错误码抛出相应的异常子类。
    """
    if error_id == 0:
        return

    exception_class = ERROR_CODE_MAP.get(error_code or "", YesCaptchaError)
    raise exception_class(
        error_id=error_id,
        error_code=error_code,
        error_description=error_description,
    )
