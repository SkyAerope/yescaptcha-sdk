"""
YesCaptcha API 客户端实现。

提供异步和同步两种客户端用于与 YesCaptcha 服务交互。
"""

import asyncio
from typing import Optional, Union

import httpx

from yescaptcha.exceptions import raise_for_error, TaskTimeoutError, YesCaptchaError
from yescaptcha.models import (
    Task,
    BalanceResponse,
    CreateTaskResponse,
    TaskResultResponse,
    Solution,
)

SOFT_ID = "21471"

class YesCaptchaClient:
    """
    YesCaptcha API 异步客户端。

    示例:

        >>> async with YesCaptchaClient(client_key="your-key") as client:
        ...     balance = await client.get_balance()
        ...     print(f"余额: {balance.balance}")

    参数:
        client_key: YesCaptcha API 密钥（从用户中心获取）。
        base_url: API 基础地址。国内用户使用 "https://cn.yescaptcha.com"。
        timeout: HTTP 请求超时时间（秒）。
    """

    INTERNATIONAL_API = "https://api.yescaptcha.com"
    CHINA_API = "https://cn.yescaptcha.com"

    def __init__(
        self,
        client_key: str,
        base_url: str = INTERNATIONAL_API,
        timeout: float = 120.0,
    ):
        self.client_key = client_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "YesCaptchaClient":
        self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """获取 HTTP 客户端，如果不存在则创建。"""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        """关闭 HTTP 客户端。"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _request(self, endpoint: str, payload: dict) -> dict:
        """
        发送 POST 请求到 API。

        参数:
            endpoint: API 端点（如 "/createTask"）。
            payload: 请求载荷字典。

        返回:
            响应 JSON 字典。
        """
        url = f"{self.base_url}{endpoint}"
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    async def get_balance(self) -> BalanceResponse:
        """
        查询账户余额。

        返回:
            BalanceResponse 包含账户余额信息。

        异常:
            YesCaptchaError: API 返回错误时抛出。
        """
        payload = {"clientKey": self.client_key}
        data = await self._request("/getBalance", payload)
        response = BalanceResponse.model_validate(data)
        raise_for_error(response.errorId, response.errorCode, response.errorDescription)
        return response

    async def create_task(self, task: Task) -> CreateTaskResponse:
        """
        创建验证码识别任务。

        参数:
            task: 任务对象（如 NoCaptchaTaskProxyless, TurnstileTaskProxyless）。

        返回:
            CreateTaskResponse 包含任务 ID。

        异常:
            YesCaptchaError: API 返回错误时抛出。
        """
        payload: dict = {
            "clientKey": self.client_key,
            "task": task.model_dump(exclude_none=True),
            "softId": SOFT_ID,
        }

        data = await self._request("/createTask", payload)
        response = CreateTaskResponse.model_validate(data)
        raise_for_error(response.errorId, response.errorCode, response.errorDescription)
        return response

    async def get_task_result(self, task_id: str) -> TaskResultResponse:
        """
        获取验证码识别任务的结果。

        参数:
            task_id: createTask 返回的任务 ID。

        返回:
            TaskResultResponse 包含状态和识别结果（如果已完成）。

        异常:
            YesCaptchaError: API 返回错误时抛出。
        """
        payload = {
            "clientKey": self.client_key,
            "taskId": task_id,
        }
        data = await self._request("/getTaskResult", payload)
        response = TaskResultResponse.model_validate(data)
        raise_for_error(response.errorId, response.errorCode, response.errorDescription)
        return response

    async def solve(
        self,
        task: Task,
        poll_interval: float = 3.0,
        timeout: Optional[float] = None,
    ) -> Solution:
        """
        高级方法：识别验证码。

        创建任务并轮询结果直到完成或超时。

        参数:
            task: 要识别的任务对象。
            poll_interval: 轮询请求的间隔时间（秒），默认 3.0。
            timeout: 等待结果的最大时间（秒），默认使用 self.timeout。

        返回:
            Solution 对象包含验证码识别结果。

        异常:
            TaskTimeoutError: 任务超时时抛出。
            YesCaptchaError: API 返回错误时抛出。

        示例:

            >>> from yescaptcha import YesCaptchaClient, TurnstileTaskProxyless
            >>> async with YesCaptchaClient(client_key="your-key") as client:
            ...     task = TurnstileTaskProxyless(
            ...         websiteURL="https://example.com",
            ...         websiteKey="0x4AAAAAAAB..."
            ...     )
            ...     solution = await client.solve(task)
            ...     print(solution.token)
        """
        if timeout is None:
            timeout = self.timeout

        # 创建任务
        create_response = await self.create_task(task)
        task_id = create_response.taskId

        if not task_id:
            raise YesCaptchaError(
                error_id=1,
                error_code="ERROR_NO_TASK_ID",
                error_description="createTask 未返回任务 ID",
            )

        # 轮询结果
        elapsed = 0.0
        while elapsed < timeout:
            result = await self.get_task_result(task_id)

            if result.status == "ready" and result.solution:
                return result.solution

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise TaskTimeoutError(
            error_id=1,
            error_code="ERROR_TASK_TIMEOUT",
            error_description=f"任务 {task_id} 在 {timeout} 秒后超时",
        )


class YesCaptchaClientSync:
    """
    YesCaptchaClient 的同步包装器。

    提供与 YesCaptchaClient 相同的接口，但使用同步方法。

    示例:

        >>> from yescaptcha import YesCaptchaClientSync
        >>> client = YesCaptchaClientSync(client_key="your-key")
        >>> balance = client.get_balance()
        >>> print(f"余额: {balance.balance}")
        >>> client.close()
    """

    def __init__(
        self,
        client_key: str,
        base_url: str = YesCaptchaClient.INTERNATIONAL_API,
        timeout: float = 120.0,
    ):
        self._async_client = YesCaptchaClient(
            client_key=client_key,
            base_url=base_url,
            timeout=timeout,
        )
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        """获取或创建事件循环。"""
        if self._loop is None or self._loop.is_closed():
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop

    def _run(self, coro):
        """同步运行协程。"""
        loop = self._get_loop()
        return loop.run_until_complete(coro)

    def close(self) -> None:
        """关闭 HTTP 客户端。"""
        self._run(self._async_client.close())

    def get_balance(self) -> BalanceResponse:
        """查询账户余额。详见 YesCaptchaClient.get_balance。"""
        return self._run(self._async_client.get_balance())

    def create_task(self, task: Task) -> CreateTaskResponse:
        """创建验证码识别任务。详见 YesCaptchaClient.create_task。"""
        return self._run(self._async_client.create_task(task))

    def get_task_result(self, task_id: str) -> TaskResultResponse:
        """获取任务结果。详见 YesCaptchaClient.get_task_result。"""
        return self._run(self._async_client.get_task_result(task_id))

    def solve(
        self,
        task: Task,
        poll_interval: float = 3.0,
        timeout: Optional[float] = None,
    ) -> Solution:
        """识别验证码。详见 YesCaptchaClient.solve。"""
        return self._run(self._async_client.solve(task, poll_interval, timeout))
