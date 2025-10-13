$(document).ready(
        function()
        {

                const message_manager_obj = new message_manager();
                $('.btn-delete').click(
                        function()
                        {
                                const id = $(this).data('id')
                                const itemName = $(this).data('title')
                                const url = '/ConfigurationChangeRequest/change-type/d/' + id + '/'
                                message_manager_obj.confirmDeleteMessage(itemName,url, id,
                                        function on_success (data)
                                        {
                                                //در صورت موفقیت آمیز بودن عملیات حذف، رکورد مورد نظر را حذف می کنیم
                                                $('#change-type-list tbody tr[data-id="'+id+'"]').remove()
                                        }
                                )
                        }
                )
        }
)