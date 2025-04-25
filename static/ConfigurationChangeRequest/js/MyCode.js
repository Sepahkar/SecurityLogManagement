

function RunAjax(url, method, data,onsuccess)
{
    debugger
    $.ajax(
        {
        url : url, // the endpoint
        type : method, // http method
        data : data, // data sent with the get request

        // handle a successful response
        success : function(json) {
            debugger
            // j = $.parseJSON(json)
            //     $("#PersonId").val(j.PersonId)
            if (json.success)
            {
                console.log(json)
                console.log("success"); // another sanity check
                if (typeof onsuccess == 'function')
                {
                    onsuccess()
                }
                // $.alert({
                //     title: 'موفقیت آمیز',
                //     content: "اطلاعات به روزرسانی شد",
                //     type: 'green',
                //     typeAnimated: true,
                //     buttons: {
                //         close: {
                //             text: 'بستن',
                //             btnClass: 'btn-success',
                //         },
                //     }
                // });
            }
            else
            {
                let message = "به روزرساني اطلاعات با خطا مواجه شد"
                if (json.message)
                    message = json.message
                $.alert({
                    title: 'خطا',
                    content: message,
                    type: 'red',
                    typeAnimated: true,
                    buttons: {
                        close: {
                            text: 'بستن',
                            btnClass: 'btn-success',
                        },
                    }
                });
            }

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            //debugger
            //alert(xhr.status + ' ' + xhr.responseText)
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //extract error info
            let rt =  xhr.responseText
            let ErrorText = ""
            let ErrorPlace = ""
            $(rt).find('tr th').each(
                function(index, item)
                {
                    if ($(item).text()=='Exception Value:')
                        ErrorText = $(item).next().text()
                    if ($(item).text()=='Exception Location:')
                        ErrorPlace = $(item).next().text()
                }
            )
            let msg = ""
            msg = "متاسفانه عملیات با خطا مواجه شد"
            msg += "<br/>" +ErrorText+"<br/>"+ErrorPlace
            $.alert({
                title: 'خطا',
                content: msg,
                type: 'red',
                typeAnimated: true,
                buttons: {
                    close: {
                        text: 'بستن',
                        btnClass: 'btn-red',
                    },
                }
            });
        }
    });
}
function ChangeImage(icon, old_name, new_name)
{
    src = $(icon).attr('src');
    //to find part of src before name, we must find length of src
    l = src.length
    //get file extention
    e = src.substring(l-4)
    //and length of current name
    n = old_name.length  + 4 //for file extention
    //now set new name
    src = src.substring(0, l-n) + new_name + e
    //change image
    $(icon).attr('src', src)
}
function active_feature(corp_code, feature_code, year_number)
{
    let data={}
    let url = "/TeamFeature/active/"+feature_code+"/"+corp_code+"/"+year_number+"/"
    RunAjax(url, "POST", data)
}
function inactive_feature(corp_code, feature_code)
{
    let data={}
    let url = "/TeamFeature/deactivate/"+feature_code+"/"+corp_code+"/"
    RunAjax(url, "POST", data)
}
function delete_feature(feature_code)
{
    let data={}
    let url = "/TeamFeature/delete/"+feature_code+"/"
    RunAjax(url, "POST", data)
}
function update_feature(feature_code, feature_text)
{
    debugger
    let data={"feature_text":feature_text}
    let url = "/TeamFeature/update/"+feature_code+"/"
    RunAjax(url, "POST", data,
        function ()
        {
            $("span[data-key='"+feature_code+"']").text(feature_text)
        })
}

$(".icon.all").click(
    function ()
    {
       //get infomration of this image
        corp = $(this).attr('data-corp')
        //find corp name
        corp_name = $('.corp[data-key="'+corp+'"]').attr('title')
        feature = $(this).attr('data-feature')
        year_number = $('.year-no[data-corp="'+corp+'"][data-feature="'+feature+'"]').val()
        message = ''
        if (corp === 'ALL')
            message = 'آیا این قابلیت از سال  ' + year_number + ' برای تمامی شرکت های بیمه فعال شود؟'
        else
            message = 'آیا کلیه قابلیت ها برای شرکت بیمه ' + corp_name + ' در سال ' + year_number + ' فعال شود؟'

        $.confirm({
            title: 'فعال سازی گروهی',
            content: message,
            type: 'red',
            typeAnimated: true,
            autoClose: 'cancel|5000',
                buttons: {
                    confirm: {
                        text:"تایید",
                        btnClass:'btn-blue',
                        keys: ['enter'],
                        action:function () {
                            debugger
                            if (corp == 'ALL') {
                                $('.year-no.inactive[data-feature="' + feature + '"]').each(
                                    function (index, item)
                                    {
                                        $(item).val(year_number)
                                    })

                                $('.icon.inactive[data-feature="' + feature + '"]').not("[data-corp='ALL']").click()
                            } else {
                                $('.year-no.inactive[data-corp="' + corp + '"]').each(
                                    function (index, item)
                                    {
                                        $(item).val(year_number)
                                    })
                                $('.icon.inactive[data-corp="' + corp + '"]').not("[data-feature='ALL']").click()
                            }
                        }
                    },

                    cancel: {
                        text:"انصراف",
                        btnClass:'btn-red',
                        action:function () {

                        }
                    }},
            });
    }
)
$("tbody td .icon").not('.all').click(
    function ()
    {
       //get infomration of this image
        corp = $(this).attr('data-corp')
        feature = $(this).attr('data-feature')
        year_number = $('.year-no[data-corp="'+corp+'"][data-feature="'+feature+'"]').val()

        //if this icon is inactive, we must active it
        if ($(this).hasClass("inactive"))
        {
            //change image
            ChangeImage(this, 'inactive', 'active')
            //update data
            active_feature(corp, feature, year_number)
            //change class
            $(this).removeClass('inactive')
            $(this).addClass('active')
        }
        else
        {
            //change image
            ChangeImage(this, 'active', 'inactive')
            //update data
            inactive_feature(corp, feature)
            //change class
            $(this).removeClass('active')
            $(this).addClass('inactive')
        }
    }
)


$(".team_feature_page").on('change',function ()
{
    // $("#SubmitForm").click()
    // let url = window.location.href
    // Form = $("form[name='frmTeamInfo']")
    // data = Form.serializeArray()

    // RunAjax(url, "POST", data)
})

$(".feature-icon.delete").click(
    function ()
    {
        let feature_code = $(this).attr('data-key')
        $.confirm({
            title: 'حذف',
            icon:"fa-square-exclamation fa-beat-fade",
            closeIcon: true,
            closeIconClass: 'fa fa-close',
            content: 'آیا از حذف این قابلیت اطمینان دارید؟',
            type: 'red',
            typeAnimated: true,
            rtl: true,
            theme: 'light',
            animation: 'scale',
            closeAnimation: 'scale',
            animationSpeed: 400,
            animationBounce: 1,
            backgroundDismissAnimation: 'shake',
            autoClose: 'cancel|5000',
                buttons: {
                    confirm: {
                        text:"تایید",
                        btnClass:'btn-blue',
                        keys: ['enter'],
                        action:function () {
                            delete_feature(feature_code)
                            debugger
                            $('tr[data-key="'+feature_code+'"]').remove()
                            $.alert(
                                {
                                    title:"حذف",
                                    content:"قابلیت مذکور با موفقیت حذف شد",
                                    theme: "bootstrap",
                                    animation:"zoom",
                                    rtl:true,
                                    autoClose:'ok|2000',
                                    buttons:
                                        {
                                            ok:
                                                {
                                                    text:"بستن",
                                                    btnClass:"btn-success"

                                                }
                                        }
                                }
                            )
                        }

                    },

                    cancel: {
                        text:"انصراف",
                        btnClass:'btn-red',
                        action:function () {

                        }
                    }},
            });

})
function feature_edit_icon_show(feature_code)
{
    //hide this feature normal mode
    $(".feature-icon.edit[data-key='"+feature_code+"']").addClass("hidden")
    $(".feature-icon.delete[data-key='"+feature_code+"']").addClass("hidden")
    $(".feature-text span[data-key='"+feature_code+"']").addClass("hidden")

    //hide feature edit
    $(".feature-icon.save[data-key='"+feature_code+"']").removeClass("hidden")
    $(".feature-icon.cancel[data-key='"+feature_code+"']").removeClass("hidden")
    $(".feature-text-edit[name='"+feature_code+"']").removeClass("hidden")
}
function feature_edit_icon_hide(feature_code)
{
    //hide feature edit
    $(".feature-icon.save[data-key='"+feature_code+"']").addClass("hidden")
    $(".feature-icon.cancel[data-key='"+feature_code+"']").addClass("hidden")
    $(".feature-text-edit[name='"+feature_code+"']").addClass("hidden")

    //show this feature normal mode
    $(".feature-icon.edit[data-key='"+feature_code+"']").removeClass("hidden")
    $(".feature-icon.delete[data-key='"+feature_code+"']").removeClass("hidden")
    $(".feature-text span[data-key='"+feature_code+"']").removeClass("hidden")

}
function future_edit_icon_hide_all()
{
    //close all  feature edit
    $(".feature-icon.save").addClass("hidden")
    $(".feature-icon.cancel").addClass("hidden")
    $(".feature-text-edit").addClass("hidden")

    //show all  feature in edit mode
    $(".feature-icon.edit").removeClass("hidden")
    $(".feature-icon.delete").removeClass("hidden")
    $(".feature-text span").removeClass("hidden")
}
$(".feature-icon.edit").click(
    function ()
    {
        //get code of this feature
        let feature_code = $(this).attr("data-key")

        future_edit_icon_hide_all()

        //and finally show this one edit mode
        feature_edit_icon_show(feature_code)


    })
$(".feature-icon.save").click(
    function ()
    {
        debugger
        let feature_code = $(this).attr("data-key")
        let feature_text = $('.feature-text-edit[name="'+feature_code+'"]').val()
        update_feature(feature_code, feature_text)
        future_edit_icon_hide_all()

    })

$(".feature-icon.cancel").click(
    function ()
    {

        future_edit_icon_hide_all()

    })

function active_star(star, active_inactive)
{
    if (active_inactive == 'A')
    {
        $(star).addClass('active')
        $(star).removeClass('inactive')
        ChangeImage(star, 'star-inactive', 'star-active')

    }
    else
    {
        $(star).addClass('inactive')
        $(star).removeClass('active')
        ChangeImage(star, 'star-active', 'star-inactive')
    }
}

$('.feature-text .star').click(function()
{
    //debugger
    let feature_code = $(this).attr('data-key')
    let star_level = $(this).attr('data-val')
    let star2 = '.star[data-key="'+feature_code+'"][data-val="2"]'
    let star3 = '.star[data-key="'+feature_code+'"][data-val="3"]'

    //if this feature is active, we must inactivate it
    if ($(this).hasClass('active'))
    {
        //we can not inactivate level 1
        if (star_level == 1)
            return
        // now inactive this item
        active_star(this, 'I')
        // if we inactivate star 2, star 3 must inactivate too
        if (star_level == 2 && $(star3).hasClass('active'))
            active_star(star3, 'I')

        //now update value in database
        star_level -= 1
    }
    else
    {
        // now active this item
        active_star(this, 'A')
        // if we inactivate star 3, star 2 must inactivate too
        if (star_level == 3 && !$(star2).hasClass('active'))
            active_star(star2, 'A')
    }
    let data = {}
    let url = '/TeamFeature/importance/' + feature_code + '/' + star_level + '/'
    RunAjax(url, 'POST', data)
})

$("#team_selected").change(
    function ()
    {
        $("form[name='frm_user_team']").find('button[type="submit"]').click()
    }
)

$('.feature-add-icon').click(
    function ()
    {
        $(".feature-add-icon").addClass('hidden')
        $(".feature-add-form").removeClass('hidden')
    }
)
$(".feature-add-form .cancel").click(
    function ()
    {

        $(".feature-add-icon").removeClass('hidden')
        $(".feature-add-form").addClass('hidden')
    }
)

$(".feature-add .icon.save").click(
    function()
    {
        let Form = $("form[name='frm-feature-add']")
        let data = Form.serializeArray();
        let url = '/TeamFeature/insert/'
        // debugger;
        RunAjax(url, 'POST', data,
            function()
            {
                location.reload()
            })

    }
)

$('.feature-filter').keyup(
    function()
    {
        let feature_text = $(this).val()
        //at first, we must show all record
        $('tbody tr').show()
        if (feature_text.length >= 3)
        {
            $('tbody tr').hide()
            $('tbody tr .feature-text span:contains('+feature_text+')').parents('tr').show()
        }
    }
)