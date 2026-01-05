"""
Pydantic 模型单元测试。
"""

import pytest
from pydantic import ValidationError

from yescaptcha.models import (
    ImageToTextTask,
    NoCaptchaTaskProxyless,
    RecaptchaV3TaskProxyless,
    HCaptchaClassification,
    TurnstileTaskProxyless,
    CloudFlareTask,
    Solution,
    CreateTaskResponse,
    TaskResultResponse,
    BalanceResponse,
)


class TestImageToTextTask:
    """ImageToTextTask 模型的测试。"""

    def test_basic_creation(self):
        """测试基本任务创建。"""
        task = ImageToTextTask(body="base64content==")
        assert task.type == "ImageToTextTaskMuggle"
        assert task.body == "base64content=="
        assert task.project_name is None

    def test_with_project_name(self):
        """测试带自定义模型名称的任务。"""
        task = ImageToTextTask(
            type="ImageToTextTaskMuggle",
            body="base64content==",
            project_name="dawn-validator-extension-241113",
        )
        assert task.project_name == "dawn-validator-extension-241113"

    def test_m1_type(self):
        """测试 M1 异步任务类型。"""
        task = ImageToTextTask(
            type="ImageToTextTaskM1",
            body="base64content==",
        )
        assert task.type == "ImageToTextTaskM1"

    def test_missing_body_raises(self):
        """测试缺少 body 抛出验证错误。"""
        with pytest.raises(ValidationError):
            ImageToTextTask()


class TestNoCaptchaTaskProxyless:
    """NoCaptchaTaskProxyless (reCaptcha V2) 模型的测试。"""

    def test_basic_creation(self):
        """测试基本任务创建。"""
        task = NoCaptchaTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="6Le-wvkS...",
        )
        assert task.type == "NoCaptchaTaskProxyless"
        assert task.websiteURL == "https://example.com"
        assert task.websiteKey == "6Le-wvkS..."
        assert task.isInvisible is False

    def test_invisible_recaptcha(self):
        """测试隐形 reCaptcha 配置。"""
        task = NoCaptchaTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="6Le-wvkS...",
            isInvisible=True,
        )
        assert task.isInvisible is True

    def test_alternate_type(self):
        """测试备选类型名称。"""
        task = NoCaptchaTaskProxyless(
            type="RecaptchaV2TaskProxyless",
            websiteURL="https://example.com",
            websiteKey="6Le-wvkS...",
        )
        assert task.type == "RecaptchaV2TaskProxyless"

    def test_serialization(self):
        """测试模型序列化用于 API 请求。"""
        task = NoCaptchaTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="6Le-wvkS...",
        )
        data = task.model_dump(exclude_none=True)
        assert data == {
            "type": "NoCaptchaTaskProxyless",
            "websiteURL": "https://example.com",
            "websiteKey": "6Le-wvkS...",
            "isInvisible": False,
        }


class TestRecaptchaV3TaskProxyless:
    """RecaptchaV3TaskProxyless 模型的测试。"""

    def test_basic_creation(self):
        """测试带必填 pageAction 的基本任务创建。"""
        task = RecaptchaV3TaskProxyless(
            websiteURL="https://example.com",
            websiteKey="6Le-wvkS...",
            pageAction="homepage",
        )
        assert task.type == "RecaptchaV3TaskProxyless"
        assert task.pageAction == "homepage"

    def test_missing_page_action_raises(self):
        """测试缺少 pageAction 抛出验证错误。"""
        with pytest.raises(ValidationError):
            RecaptchaV3TaskProxyless(
                websiteURL="https://example.com",
                websiteKey="6Le-wvkS...",
            )


class TestHCaptchaClassification:
    """HCaptchaClassification 模型的测试。"""

    def test_basic_creation(self):
        """测试基本任务创建。"""
        task = HCaptchaClassification(
            queries=["base64img1==", "base64img2=="],
            question="0x1234",
        )
        assert task.type == "HCaptchaClassification"
        assert len(task.queries) == 2
        assert task.question == "0x1234"

    def test_with_anchors(self):
        """测试带辅助图片的任务。"""
        task = HCaptchaClassification(
            queries=["base64img1=="],
            anchors=["anchor1==", "anchor2=="],
        )
        assert task.anchors == ["anchor1==", "anchor2=="]

    def test_empty_queries_raises(self):
        """测试空 queries 验证，列表为必填。"""
        with pytest.raises(ValidationError):
            HCaptchaClassification()


class TestTurnstileTaskProxyless:
    """TurnstileTaskProxyless 模型的测试。"""

    def test_basic_creation(self):
        """测试基本任务创建。"""
        task = TurnstileTaskProxyless(
            websiteURL="https://example.com",
            websiteKey="0x4AAAAAAAB...",
        )
        assert task.type == "TurnstileTaskProxyless"

    def test_m1_type(self):
        """测试 M1 备选类型。"""
        task = TurnstileTaskProxyless(
            type="TurnstileTaskProxylessM1",
            websiteURL="https://example.com",
            websiteKey="0x4AAAAAAAB...",
        )
        assert task.type == "TurnstileTaskProxylessM1"


class TestCloudFlareTask:
    """CloudFlareTask 模型的测试。"""

    def test_basic_creation(self):
        """测试基本任务创建。"""
        task = CloudFlareTask(
            websiteURL="https://example.com",
            proxy="http://user:pass@ip:port",
        )
        assert task.type == "CloudFlareTaskS3"
        assert task.waitLoad is False
        assert task.blockImage is False

    def test_with_options(self):
        """测试带各种选项的任务。"""
        task = CloudFlareTask(
            type="CloudFlareTaskS2",
            websiteURL="https://example.com",
            proxy="socks5://ip:port",
            waitLoad=True,
            requiredCookies=["cf_clearance", "session"],
            blockImage=True,
        )
        assert task.type == "CloudFlareTaskS2"
        assert task.waitLoad is True
        assert task.requiredCookies == ["cf_clearance", "session"]


class TestSolution:
    """Solution 模型的测试。"""

    def test_recaptcha_solution(self):
        """测试 reCaptcha 结果解析。"""
        solution = Solution(gRecaptchaResponse="03AGdBq25...")
        assert solution.gRecaptchaResponse == "03AGdBq25..."

    def test_turnstile_solution(self):
        """测试 Turnstile 结果解析。"""
        solution = Solution(token="0.ufq5RgSVZd11...")
        assert solution.token == "0.ufq5RgSVZd11..."

    def test_image_to_text_solution(self):
        """测试 ImageToText 结果解析。"""
        solution = Solution(text="ABC123")
        assert solution.text == "ABC123"

    def test_hcaptcha_classification_solution(self):
        """测试 HCaptcha 分类结果。"""
        solution = Solution(objects=[0, 2, 5])
        assert solution.objects == [0, 2, 5]

    def test_cloudflare_solution(self):
        """测试 CloudFlare 带 cookies 的结果。"""
        solution = Solution(
            cookies={"cf_clearance": "abc123"},
            userAgent="Mozilla/5.0...",
            content="<html>...</html>",
        )
        assert solution.cookies == {"cf_clearance": "abc123"}
        assert solution.userAgent == "Mozilla/5.0..."

    def test_extra_fields_allowed(self):
        """测试额外字段被保留。"""
        solution = Solution.model_validate(
            {"token": "xyz", "customField": "customValue"}
        )
        assert solution.token == "xyz"
        # 额外字段通过 model_extra 访问
        assert solution.model_extra.get("customField") == "customValue"


class TestResponseModels:
    """响应模型的测试。"""

    def test_create_task_response_success(self):
        """测试成功的 createTask 响应。"""
        response = CreateTaskResponse(
            errorId=0,
            taskId="abc123",
        )
        assert response.errorId == 0
        assert response.taskId == "abc123"

    def test_create_task_response_error(self):
        """测试错误的 createTask 响应。"""
        response = CreateTaskResponse(
            errorId=1,
            errorCode="ERROR_ZERO_BALANCE",
            errorDescription="Insufficient balance",
        )
        assert response.errorId == 1
        assert response.errorCode == "ERROR_ZERO_BALANCE"

    def test_task_result_response_ready(self):
        """测试已完成的任务结果响应。"""
        response = TaskResultResponse(
            errorId=0,
            status="ready",
            solution=Solution(token="xyz"),
        )
        assert response.status == "ready"
        assert response.solution.token == "xyz"

    def test_task_result_response_processing(self):
        """测试处理中的任务结果响应。"""
        response = TaskResultResponse(
            errorId=0,
            status="processing",
        )
        assert response.status == "processing"
        assert response.solution is None

    def test_balance_response(self):
        """测试余额响应解析。"""
        response = BalanceResponse(
            errorId=0,
            balance=10000.5,
            softBalance=100.0,
            inviteBalance=50.0,
            inviteBy="12345",
        )
        assert response.balance == 10000.5
        assert response.softBalance == 100.0
