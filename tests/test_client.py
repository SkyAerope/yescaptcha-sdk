"""
YesCaptcha 客户端单元测试。

使用 respx mock HTTP 请求，无需真实 API 调用即可测试。
"""

import pytest
import respx
from httpx import Response

from yescaptcha import (
    YesCaptchaClient,
    YesCaptchaError,
    InvalidKeyError,
    InsufficientBalanceError,
    TaskTimeoutError,
    TurnstileTaskProxyless,
    NoCaptchaTaskProxyless,
    ImageToTextTask,
)


@pytest.fixture
def client():
    """创建测试客户端。"""
    return YesCaptchaClient(client_key="test-key-12345")


@pytest.fixture
def base_url():
    """API 基础地址，用于 mock。"""
    return "https://api.yescaptcha.com"


class TestGetBalance:
    """get_balance 方法的测试。"""

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_balance_success(self, client, base_url):
        """测试成功获取余额。"""
        respx.post(f"{base_url}/getBalance").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 0,
                    "balance": 10000,
                    "softBalance": 100.5,
                    "inviteBalance": 50.0,
                    "inviteBy": "12345",
                },
            )
        )

        balance = await client.get_balance()

        assert balance.errorId == 0
        assert balance.balance == 10000
        assert balance.softBalance == 100.5
        assert balance.inviteBalance == 50.0

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_balance_invalid_key(self, client, base_url):
        """测试无效密钥的余额请求。"""
        respx.post(f"{base_url}/getBalance").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 1,
                    "errorCode": "ERROR_KEY_DOES_NOT_EXIST",
                    "errorDescription": "Account key does not exist",
                },
            )
        )

        with pytest.raises(InvalidKeyError) as exc_info:
            await client.get_balance()

        assert exc_info.value.error_code == "ERROR_KEY_DOES_NOT_EXIST"


class TestCreateTask:
    """create_task 方法的测试。"""

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_turnstile_task_success(self, client, base_url):
        """测试成功创建 Turnstile 任务。"""
        respx.post(f"{base_url}/createTask").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 0,
                    "taskId": "abc123-task-id",
                },
            )
        )

        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="0x4AAAAAAAB...",
        )
        response = await client.create_task(task)

        assert response.errorId == 0
        assert response.taskId == "abc123-task-id"

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_recaptcha_v2_task(self, client, base_url):
        """测试创建 reCaptcha V2 任务。"""
        respx.post(f"{base_url}/createTask").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 0,
                    "taskId": "recaptcha-task-123",
                },
            )
        )

        task = NoCaptchaTaskProxyless(
            websiteURL="https://www.google.com/recaptcha/api2/demo",
            websiteKey="6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
        )
        response = await client.create_task(task)

        assert response.taskId == "recaptcha-task-123"

    @respx.mock
    @pytest.mark.asyncio
    async def test_create_task_insufficient_balance(self, client, base_url):
        """测试余额不足时创建任务。"""
        respx.post(f"{base_url}/createTask").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 1,
                    "errorCode": "ERROR_ZERO_BALANCE",
                    "errorDescription": "Account balance is insufficient",
                },
            )
        )

        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="0x4AAAAAAAB...",
        )

        with pytest.raises(InsufficientBalanceError):
            await client.create_task(task)


class TestGetTaskResult:
    """get_task_result 方法的测试。"""

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_task_result_ready(self, client, base_url):
        """测试获取已完成的任务结果。"""
        respx.post(f"{base_url}/getTaskResult").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 0,
                    "status": "ready",
                    "solution": {
                        "token": "0.ufq5RgSVZd11DPSX1brdrxnEs28KcVlKj..."
                    },
                },
            )
        )

        result = await client.get_task_result("task-123")

        assert result.status == "ready"
        assert result.solution is not None
        assert result.solution.token == "0.ufq5RgSVZd11DPSX1brdrxnEs28KcVlKj..."

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_task_result_processing(self, client, base_url):
        """测试获取处理中的任务结果。"""
        respx.post(f"{base_url}/getTaskResult").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 0,
                    "status": "processing",
                },
            )
        )

        result = await client.get_task_result("task-123")

        assert result.status == "processing"
        assert result.solution is None


class TestSolve:
    """高级 solve 方法的测试。"""

    @respx.mock
    @pytest.mark.asyncio
    async def test_solve_turnstile_immediate_success(self, client, base_url):
        """测试立即完成的 Turnstile 验证码识别。"""
        # Mock createTask
        respx.post(f"{base_url}/createTask").mock(
            return_value=Response(
                200,
                json={"errorId": 0, "taskId": "solve-task-123"},
            )
        )

        # Mock getTaskResult - 立即返回结果
        respx.post(f"{base_url}/getTaskResult").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 0,
                    "status": "ready",
                    "solution": {"token": "solved-token-xyz"},
                },
            )
        )

        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="0x4AAAAAAAB...",
        )
        solution = await client.solve(task, poll_interval=0.1, timeout=5.0)

        assert solution.token == "solved-token-xyz"

    @respx.mock
    @pytest.mark.asyncio
    async def test_solve_with_polling(self, client, base_url):
        """测试需要多次轮询的验证码识别。"""
        # Mock createTask
        respx.post(f"{base_url}/createTask").mock(
            return_value=Response(
                200,
                json={"errorId": 0, "taskId": "poll-task-123"},
            )
        )

        # Mock getTaskResult - 先返回 processing，后返回 ready
        call_count = 0

        def get_result_side_effect(request):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                return Response(
                    200,
                    json={"errorId": 0, "status": "processing"},
                )
            return Response(
                200,
                json={
                    "errorId": 0,
                    "status": "ready",
                    "solution": {"gRecaptchaResponse": "polled-response"},
                },
            )

        respx.post(f"{base_url}/getTaskResult").mock(side_effect=get_result_side_effect)

        task = NoCaptchaTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="6Le-wvkS...",
        )
        solution = await client.solve(task, poll_interval=0.1, timeout=5.0)

        assert solution.gRecaptchaResponse == "polled-response"
        assert call_count == 3

    @respx.mock
    @pytest.mark.asyncio
    async def test_solve_timeout(self, client, base_url):
        """测试 solve 方法超时。"""
        respx.post(f"{base_url}/createTask").mock(
            return_value=Response(
                200,
                json={"errorId": 0, "taskId": "timeout-task"},
            )
        )

        # 始终返回 processing
        respx.post(f"{base_url}/getTaskResult").mock(
            return_value=Response(
                200,
                json={"errorId": 0, "status": "processing"},
            )
        )

        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="0x4AAAAAAAB...",
        )

        with pytest.raises(TaskTimeoutError):
            await client.solve(task, poll_interval=0.1, timeout=0.3)


class TestImageToText:
    """ImageToText 任务的测试。"""

    @respx.mock
    @pytest.mark.asyncio
    async def test_image_to_text_task(self, client, base_url):
        """测试 ImageToText 任务创建和结果。"""
        respx.post(f"{base_url}/createTask").mock(
            return_value=Response(
                200,
                json={
                    "errorId": 0,
                    "status": "ready",
                    "taskId": "ocr-task-123",
                    "solution": {"text": "ABC123"},
                },
            )
        )

        task = ImageToTextTask(
            type="ImageToTextTaskMuggle",
            body="base64encodedimage==",
        )
        response = await client.create_task(task)

        assert response.taskId == "ocr-task-123"


class TestContextManager:
    """上下文管理器使用的测试。"""

    @respx.mock
    @pytest.mark.asyncio
    async def test_async_context_manager(self, base_url):
        """测试客户端作为异步上下文管理器使用。"""
        respx.post(f"{base_url}/getBalance").mock(
            return_value=Response(
                200,
                json={"errorId": 0, "balance": 5000},
            )
        )

        async with YesCaptchaClient(client_key="ctx-test-key") as client:
            balance = await client.get_balance()
            assert balance.balance == 5000
