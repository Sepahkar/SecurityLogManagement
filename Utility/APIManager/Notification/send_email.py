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


def v2(
        template_code:str,
        variable_value:dict,
        to: list[str],
        cc: list[str],
        bcc: list[str]
) -> dict:
        """
        این تابع بر اساس کد الگوی اطلاع رسانی دریافتی، سرویس مربوط به اطلاع رسانی را فراخوانی می کند

        Args:
            template_code (str): کد الگوی اطلاع رسانی
            variable_value (dict): یک آرایه از متغییرهایی که باید در الگو جایگزین شوند و مقادیر آنها
            to (list[str]): لیستی از آدرس های ایمیلی که باید اطلاع رسانی به آنها انجام شود
            cc (list[str]): لیستی از آدرس های ایمیلی که باید اطلاع رسانی به آنها انجام شود
            bcc (list[str]): لیستی از آدرس های ایمیلی که باید اطلاع رسانی به آنها انجام شود

        Returns:
            dict: یک دیکشنری که شامل موارد زیر است:
                success : 
                        True: عملیات اطلاع رسانی با موفقیت انجام شده است
                        False : عملیات اطلاع رسانی ناموفق بوده است
                message: پیام مربوطه
                error_code:
                        -10 : سرویس دهنده ایمیل در دسترس نیست
                        -20 : سرویس ایمیل (در سرور جنگو) در دسترس نیست
                        -30 : حساب کاربری جهت ارسال ایمیل معتبر نیست
                        -40 : الگوی اطلاع رسانی پیدا نشد
                        -50 : خطای غیرمنتظره ای رخ داد
                        -60 : آدرس ایمیل نامعتبر است (لیست آنها در متغییر مربوطه آورده شده است)
                                -61 : خطا در آدرس ایمیل TO
                                -62 : خطا در آدرس ایمیل CC
                                -63 : خطا در آدرس ایمیل BCC
                        -70 : خطا در مقادیر متغییرها (لیست آنها در متغییر مربوطه آورده شده است)
                                -71 : برای متغییری که مورد نیاز است، مقدار ارسال نشده است
                                -72 : نوع مقدار متغییر نامعتبر است (مثلا برای متغییر عددی، متن ارسال شده است)
                        
                invalid_email_address[]: لیست ایمیل های نامعتبر
                invalid_variable[]: لیست متغییرهای نامعتبر
        """

        return {"success":True,"message":"اطلاع رسانی با موفقیت انجام شد","return_code":200}