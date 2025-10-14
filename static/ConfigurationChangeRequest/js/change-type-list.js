$(document).ready(
        function()
        {

                const message_manager_obj = new message_manager();
                $('.btn-delete').click(
                    function() {
                        const id = $(this).data('id')
                        const itemName = $(this).data('title')
                        const url = '/ConfigurationChangeRequest/change-type/d/' + id + '/'

                        // راه‌حل سریع (تا رفع مشکل در کلاس پایه): اینجا یک تابع wrapper بدهیم که دقیقا تابع را با پارامتر درست بخواند
                        message_manager_obj.confirmDeleteMessage(
                            itemName,
                            url,
                            id,
                            function(data) 
                            {
                                // انتظار می‌رود که data.success وجود داشته باشد
                                if (data && (data.success === true || data.result === true))
                                {
                                    //در صورت موفقیت آمیز بودن عملیات حذف، رکورد مورد نظر را حذف می کنیم
                                    $('#change-type-list tbody tr[data-id="'+id+'"]').remove()
                                } else 
                                {
                                    // اگر حذف موفق نبود، پیام خطا نمایش داده شود
                                    if (data && data.message)
                                        message_manager_obj.showErrorMessage(data.message);
                                    else
                                        message_manager_obj.showErrorMessage('خطا در حذف رکورد');
                                }
                            }
                        );
                    }
                );

                // توضیح: اگر همچنان تابع on_success در confirmDeleteMessage صدا زده نمی‌شود،
                // لازم است بدنه confirmDeleteMessage در کلاس message_manager یا فایل request.js
                // اصلاح شود تا جای:
                //     if (on_success == 'function')
                // باشد:
                //     if (typeof on_success === 'function')

                // مشکل فعلی: در فایل request.js:
                //     if (on_success == 'function')
                // که این هیچ‌وقت درست نیست و on_success هرگز صدا زده نمی‌شود.
                // رفع نهایی باید در آنجا انجام شود.
        })
