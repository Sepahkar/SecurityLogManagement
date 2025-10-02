import requests
from Utility import configs
from shared_lib import core as slcore

def v1(
    template_code: str,
    variable_value: dict[str, str],
    to: list[str],
    cc: list[str],
    bcc: list[str]
) -> dict:
    """
    فراخوانی سرویس اطلاع رسانی و بازگرداندن نتیجه با لیست ایمیل‌ها و متغیرهای نامعتبر و کد خطا
    """
    url = f"http://{configs.servers['MAIN_SERVER']}:{configs.Port.NOTIFICATION}/EmailService/api/v1/send-template-mail/"
    payload = {
        "template_code": template_code,
        "variable_value": variable_value,
        "to": to,
        "cc": cc,
        "bcc": bcc
    }
    headers = {
        "Service-Authorization": slcore.generate_token("v.bagheri"),
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
    except requests.exceptions.RequestException:
        # -10 : سرویس ایمیل در دسترس نیست
        return {
            "success": False,
            "message": "سرویس ایمیل در دسترس نیست",
            "error_code": -10,
            "invalid_email_address": [],
            "invalid_variablep": []
        }
    # Always return all fields
    return {
        "success": result.get("success", False),
        "message": result.get("message", ""),
        "error_code": result.get("error_code"),
        "invalid_email_address": result.get("invalid_email_address", []),
        "invalid_variablep": result.get("invalid_variablep", [])
    }
