// 

function reject()
{
    //شناسه درخواست را به دست می آوریم
    var requestId = $('input[name="request_id"]').val();
    
    //به سراغ مرحله بعدی می رویم
    var url = '/ConfigurationChangeRequest/request/next_step/' + requestId + '/REJ/';

    // جمع‌آوری داده‌های فرم


    $.confirm({
        title: 'دلیل رد',
        content: '' +
        '<form action="" class="formName">' +
        '<div class="form-group">' +
        '<label>دلیل رد مدرک را وارد کنید:</label>' +
        '<input type="text" placeholder="دلیل رد مدرک" class="reject-reason form-control" required />' +
        '</div>' +
        '</form>',
        buttons: {
            formSubmit: {
                text: 'رد مدرک',
                btnClass: 'btn-blue',
                action: function () {
                    var reject_reason = this.$content.find('.reject-reason').val();
                    if(!reject_reason){
                        $.alert('لطفا دلیل رد را وارد کنید');
                        return false;
                    }
                    var formData = {'reject_reason':reject_reason, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()}
                    // ارسال درخواست AJAX
                    $.ajax({
                        url: url,
                        method: 'POST',
                        data: formData,
                        success: function(response) 
                        {
                            if (response.success) 
                            {
                                if (response.message)
                                    msg = response.message
                                else
                                    msg = 'فرآیند مختومه شد'
                                
                                $.alert({
                                    title: 'خاتمه فرآیند',
                                    content: msg,
                                    buttons: {
                                        confirm: {
                                            text: 'بستن',
                                            btnClass: 'btn-blue',
                                            action: function() {
                                                window.location.href = '/ConfigurationChangeRequest/request/view/'+response.request_id+'/';
                                            }
                                        }
                                    }});                                
                            } 
                            else 
                            {
                                // در صورت بروز خطا، پیام‌های خطا را نمایش دهید
                                var errorMessage = response.message;
                                $.alert({
                                    title: 'خطا',
                                    content: errorMessage,
                                });
                                on_failure()
                            }
                        },
                        error: function(xhr) 
                        {
                            // در صورت بروز خطا، پیام خطا را نمایش می‌دهیم
                            // ایجاد یک عنصر موقتی
                            var tempDiv = $('<div>').html(xhr.responseText);
                
                            // استخراج متن از div با شناسه summary
                            var errorMessage = tempDiv.find('#summary').text().trim(); // استفاده از #summary
                            $.alert({
                                title: 'خطا',
                                content: errorMessage,
                            });
                            on_failure()
                        }
                        });
                }
            },
            cancel: {
                text:'انصراف',
                function () {
                    //close
                },
    
            }
        },
        onContentReady: function () {
            // bind to events
            var jc = this;
            this.$content.find('form').on('submit', function (e) {
                // if the user submits the form by pressing enter in the field.
                e.preventDefault();
                jc.$$formSubmit.trigger('click'); // reference the button and click it
            });
        }
    });    

    

}
