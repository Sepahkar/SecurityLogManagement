from django.test import TestCase
from .models import *
from .business import FormManager
import json


class FormManagerTestCase(TestCase):
    def setUp(self):
        """تنظیمات اولیه برای تست‌ها"""
        pass  # نیازی به ایجاد رکوردهای پیچیده نیست

    def test_get_record_json_request_success(self):
        """تست موفقیت‌آمیز دریافت JSON یک درخواست"""
        # تست با شناسه ناموجود
        result = FormManager.get_record_json('R', 99999)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'درخواست مورد نظر یافت نشد.')

    def test_get_record_json_changetype_success(self):
        """تست موفقیت‌آمیز دریافت JSON یک نوع تغییر"""
        # تست با شناسه ناموجود
        result = FormManager.get_record_json('C', 99999)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'نوع تغییر مورد نظر یافت نشد.')

    def test_get_record_json_changetype_new_record(self):
        """تست دریافت JSON برای رکورد جدید نوع تغییر"""
        result = FormManager.get_record_json('C', -1)
        
        # بررسی موفقیت‌آمیز بودن نتیجه
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'رکورد تازه فاقد اطلاعات است.')
        self.assertEqual(result['record_data'], {})

    def test_get_record_json_invalid_record_type(self):
        """تست با نوع رکورد نامعتبر"""
        result = FormManager.get_record_json('X', 1)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertIn('نوع رکورد ارسالی نامعتبر است', result['message'])

    def test_get_record_json_request_not_found(self):
        """تست با شناسه درخواست ناموجود"""
        result = FormManager.get_record_json('R', 99999)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'درخواست مورد نظر یافت نشد.')

    def test_get_record_json_changetype_not_found(self):
        """تست با شناسه نوع تغییر ناموجود"""
        result = FormManager.get_record_json('C', 99999)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'نوع تغییر مورد نظر یافت نشد.')

    def test_get_record_json_unicode_handling(self):
        """تست صحت پردازش کاراکترهای فارسی و Unicode"""
        # تست با رکورد جدید نوع تغییر (id = -1)
        result = FormManager.get_record_json('C', -1)
        
        # بررسی موفقیت‌آمیز بودن نتیجه
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'رکورد تازه فاقد اطلاعات است.')
        self.assertEqual(result['record_data'], {})
        
        # تست با نوع رکورد نامعتبر
        result = FormManager.get_record_json('X', 1)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertIn('نوع رکورد ارسالی نامعتبر است', result['message'])
        
        # تست با شناسه ناموجود
        result = FormManager.get_record_json('R', 99999)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'درخواست مورد نظر یافت نشد.')
        
        # تست با شناسه نوع تغییر ناموجود
        result = FormManager.get_record_json('C', 99999)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'نوع تغییر مورد نظر یافت نشد.')
        
        # تست با شناسه تسک ناموجود
        result = FormManager.get_record_json('T', 99999)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'تسک مورد نظر یافت نشد.')

    def test_get_record_json_task_record(self):
        """تست دریافت JSON برای یک تسک"""
        # تست با شناسه ناموجود
        result = FormManager.get_record_json('T', 99999)
        
        # بررسی عدم موفقیت
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'تسک مورد نظر یافت نشد.')
