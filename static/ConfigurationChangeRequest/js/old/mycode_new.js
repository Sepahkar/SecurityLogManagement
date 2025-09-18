function RunAjax(url, method, data, onsuccess) {
    debugger
    $.ajax(
        {
            url: url, // the endpoint
            type: method, // http method
            data: data, // data sent with the get request

            // handle a successful response
            success: function (json) {
                debugger
                // j = $.parseJSON(json)
                //     $("#PersonId").val(j.PersonId)
                if (json.success) {
                    console.log(json)
                    console.log("success"); // another sanity check
                    if (typeof onsuccess == 'function') {
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
                } else {
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
            error: function (xhr, errmsg, err) {
                //debugger
                //alert(xhr.status + ' ' + xhr.responseText)
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                //extract error info
                let rt = xhr.responseText
                let ErrorText = ""
                let ErrorPlace = ""
                $(rt).find('tr th').each(
                    function (index, item) {
                        if ($(item).text() == 'Exception Value:')
                            ErrorText = $(item).next().text()
                        if ($(item).text() == 'Exception Location:')
                            ErrorPlace = $(item).next().text()
                    }
                )
                let msg = ""
                msg = "متاسفانه عملیات با خطا مواجه شد"
                msg += "<br/>" + ErrorText + "<br/>" + ErrorPlace
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

function active_feature(corp_code, feature_code, year_number) {
    let data = {}
    let url = "/TeamFeature/active/" + feature_code + "/" + corp_code + "/" + year_number + "/"
    RunAjax(url, "POST", data)
}

function inactive_feature(corp_code, feature_code) {
    let data = {}
    let url = "/TeamFeature/deactivate/" + feature_code + "/" + corp_code + "/"
    RunAjax(url, "POST", data)
}

function delete_feature(feature_code) {
    let data = {}
    let url = "/TeamFeature/delete/" + feature_code + "/"
    RunAjax(url, "POST", data)
}

function update_feature(feature_code, feature_text) {
    debugger
    let data = {"feature_text": feature_text}
    let url = "/TeamFeature/update/" + feature_code + "/"
    RunAjax(url, "POST", data,
        function () {
            $("span[data-key='" + feature_code + "']").text(feature_text)
        })
}


/****************************** general code start *********************************/
$('.panel-body table tr .select').change(
    function () {
        debugger
        if (this.checked) {
            $(this).parents('tr').addClass('selected-row')
        } else {
            $(this).parents('tr').removeClass('selected-row')
        }
    })
// with click on  each row add selected-row class in it for change color of row and make true check box of row
$('.panel-body table tr td').not('td:nth-child(1)').click(
    function () {
        let panel = $(this).parents('.panel')
        let situation_box = $(this).parents('.situation-box')
        let tr = $(this).parent()

        if (tr.find('.select').is(':checked')) {
            tr.find('.select').prop('checked', false)
            tr.removeClass('selected-row')
        } else {


            tr.find('.select').prop('checked', true)
            tr.addClass('selected-row')
        }
    }
)


// for Specify the direction of the arrow in operation class (make active or not)
// if check box is true in active panel ,in inactive panel checkbox can not be ture and similarly, the opposite of this case
$('.panel').click(
    function () {

        let panel = $(this)
        let situation_box = $(this).parents('.situation-box')
        let tr = $(this).parent()


        if (panel.hasClass('active')) {
            situation_box.find('.operation img').attr('src', '/static/TeamFeature/images/icon/arrow.png')
            situation_box.find('.operation p').html('غیرفعال سازی')
            situation_box.find(".operation").addClass('inactive')
            situation_box.find(".operation").removeClass('active')
            situation_box.find('.inactive table tr .select').prop('checked', false)
            situation_box.find('.inactive table tr').removeClass('selected-row')


        } else {
            situation_box.find('.operation img').attr('src', '/static/TeamFeature/images/icon/arrowf.png')
            situation_box.find('.operation p').html('فعال سازی')
            situation_box.find(".operation").addClass('active')
            situation_box.find(".operation").removeClass('inactive')
            situation_box.find('.active table tr .select').prop('checked', false)
            situation_box.find('.active table tr').removeClass('selected-row')
        }


    }
)


// press select all button all tr of table selected
$(".panel-search .btn-all").click(
    // if press button change it color to red (class:select-all) and add selected-row class for change color of rows and make true check box of rows
    function () {
        //debugger

        if ($(this).hasClass('select-all')) {
            $(this).removeClass('select-all')
            $(this).parents('.panel').find('table tr').removeClass('selected-row')
            $(this).parents('.panel').find('.select').prop('checked', false)
        } else {
            $(this).addClass('select-all')
            $(this).parents('.panel').find('table tr').addClass('selected-row')
            $(this).parents('.panel').find('.select').prop('checked', true)


        }

    });


function move_item(row) {
    debugger
    let other_panel = null
    let corp_code = ''
    let feature_code = ''
    let year_number = ''
    let row_count = row.length // test mahsa


    row.fadeOut(1500, function () { //row is one or more tr of a table


        if ($('.main-content').hasClass('feature-view')) {
            corp_code = $(this).attr('data-key')
            year_number = $(this).parents(".feature").find(".title .select-year .title-year").val()
            feature_code = $(this).parents(".feature").attr('data-key')
        } else {
            feature_code = $(this).attr('data-key')
            corp_code = $(this).parents(".corp").attr('data-key')
            year_number = $(this).find('.feature-title').attr('data-year-number')
        }

        if ($(this).parents('.panel').hasClass('active')) {
            other_panel = $(this).parents('.main-row').find('.panel.inactive')
            $(this).find('td').last().remove()
            inactive_feature(corp_code, feature_code)

        } else {
            other_panel = $(this).parents('.main-row').find('.panel.active')

            $(this).append('<td><input class="active-year"  type="number" value="" name="active_year" data-key="' + corp_code + '"></td>')
            $(this).find('.active-year').val(year_number)
            active_feature(corp_code, feature_code, year_number)
        }
        // this part is for update number of panel-title
        let current_panel_number = $(this).parents('.panel').find('.panel-title .case-count').attr('data-key')
        let other_panel_number = other_panel.find('.panel-title .case-count').attr('data-key')
        let current_panel_new_number = parseInt(current_panel_number) - 1
        let other_panel_new_number = parseInt(other_panel_number) + 1
        other_panel.find('.panel-title .case-count').text(other_panel_new_number + "مورد")
        other_panel.find('.panel-title .case-count ').attr('data-key', other_panel_new_number)
        $(this).parents('.panel').find('.panel-title .case-count').text(current_panel_new_number + "مورد")
        $(this).parents('.panel').find('.panel-title .case-count').attr('data-key', current_panel_new_number)

        $(this).find('.select').prop('checked', false)// To uncheck the checkbox after moving
        $(this).removeClass('selected-row') // remove selected class after moving
        other_panel.find('table').append($(this))
        // for update case count of title in corp-view
        if ($(this).parents('.main-content').hasClass('corp-view')) {
            let corp_active_counter = $(this).parents('.corp').find(' .situation-box .active .panel-title .case-count').attr('data-key')
            let corp_inactive_counter = $(this).parents('.corp').find(' .situation-box .inactive .panel-title .case-count').attr('data-key')
            $(this).parents('.corp').find('.title .item-count .active-item-count').text(+corp_active_counter + 'مورد فعال')
            $(this).parents('.corp').find('.title .item-count .inactive-item-count').text(corp_inactive_counter + "مورد غیر فعال")
        }

        $(this).fadeIn(2000)
    })
}

// when you
$('.operation').click(
    function () {
        debugger
        let row = $(".selected-row")
        move_item(row)
        $('.panel-search .btn-all').removeClass('select-all')
    }
)

$('.panel-body table tr').dblclick(
    function () {
        debugger
        let row = $(this)
        move_item(row)


    }
)

/****************************** general code end ***********************************/
/****************************** feature view code start *********************************/

//we want to slide up and down by click on feature title
$(".feature .title .star-title").click(
    function () {
        // debugger
        //get feature code
        let feature_code = $(this).parents(".feature").attr('data-key')
        // let up = $(".feature[data-key='" + feature_code + "'] ").find('.title .little-arrow .up')
        // let down = $(".feature[data-key='" + feature_code + "'] ").find('.title .little-arrow .down')
        let page = $(".feature[data-key='" + feature_code + "'] .situation-box")//find situation box of that feature and toggle slide
        //at first slide up all other panel except this panel
        $(".feature .situation-box").not(".feature[data-key='" + feature_code + "'] .situation-box").slideUp("fast")
        page.slideToggle()
        // up.toggleClass("hide")
        // down.toggleClass("hide")
    }
)

$(".feature .title .little-arrow").click(
    function () {
        // debugger
        //get feature code
        let feature_code = $(this).parents(".feature").attr('data-key')
        // let up = $(".feature[data-key='" + feature_code + "'] ").find('.title .little-arrow .up')
        // let down = $(".feature[data-key='" + feature_code + "'] ").find('.title .little-arrow .down')
        let page = $(".feature[data-key='" + feature_code + "'] .situation-box")//find situation box of that feature and toggle slide
        //at first slide up all other panel except this panel
        $(".feature .situation-box").not(".feature[data-key='" + feature_code + "'] .situation-box").slideUp("fast")
        page.slideToggle()
        // up.toggleClass("hide")
        // down.toggleClass("hide")
    }
)


$(".feature .title .star-title").click(function () {
    $(this).parents('.title').find(".rotate").toggleClass("down");
})
/******** Duplicate code3 arrow*****/
$(".feature .title .little-arrow").click(function () {
    $(this).parents('.title').find(".rotate").toggleClass("down");
})

/**************** you should manage this Duplicate codes by function *****/
function ChangeImage(icon, old_name, new_name) {
    src = $(icon).attr('src');
    //to find part of src before name, we must find length of src
    l = src.length
    //get file extention
    e = src.substring(l - 4)
    //and length of current name
    n = old_name.length + 4 //for file extention
    //now set new name
    src = src.substring(0, l - n) + new_name + e
    //change image
    $(icon).attr('src', src)
}

function active_star(star, active_inactive) {

    if (active_inactive == 'A') {
        $(star).addClass('active')
        $(star).removeClass('inactive')
        ChangeImage(star, 'star-inactive', 'star-active')

    } else {
        $(star).addClass('inactive')
        $(star).removeClass('active')
        ChangeImage(star, 'star-active', 'star-inactive')
    }
}

$('.feature .title .star').click(function () {

    let feature_code = $(this).attr('data-key')
    let star_level = $(this).attr('data-val')
    let star2 = '.star[data-key="' + feature_code + '"][data-val="2"]'
    let star3 = '.star[data-key="' + feature_code + '"][data-val="3"]'

    //if this feature is active, we must inactivate it
    if ($(this).hasClass('active')) {
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
    } else {
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

// searching for panel-title
$('.situation-box .panel-search .search-input').on('keyup',
    function () {
        let corp_title = $(this).val()
        let tr = $(this).parents('.panel').find('.panel-body table tr')
        if (corp_title.length > 0) {
            tr.hide()
            tr.parent().find('[data-corp-title*="' + corp_title + '"]').show() // show tr that is like value of input
        } else {
            tr.show()
        }
    }
)
// delete a feature

// $('.feature .title .trash').click(
//
//     function (){
//         debugger
//         let feature_code = $(this).parents('.feature').attr('data-key')
//         $(this).parents('.feature').remove() // delete this feature by jquery
//         delete_feature(feature_code) // delete from data base
//
//     }
// )
//  general search for feature-view
$('.feature-view .general-search-box .search-input').on('keyup',
    function () {
        let input_val = $(this).val()
        let feature_title = $(this).parents('.feature-view').find('.feature .title')
        if (input_val.length > 0) {
            feature_title.hide()
            feature_title.parent().find('[data-feature-title*="' + input_val + '"]').show()
        } else {
            feature_title.show()
        }
    }
)

// mange the part of edit a feature

function feature_edit_icon_show(feature_code) {
    //hide this feature normal mode
    $(".feature-icon.edit[data-key='" + feature_code + "']").addClass("hide")
    $(".feature-icon.trash[data-key='" + feature_code + "']").addClass("hide")
    $(".feature-text-place span[data-key='" + feature_code + "']").addClass("hide")

    //hide feature edit
    $(".feature-icon.save-edit[data-key='" + feature_code + "']").removeClass("hide")
    $(".feature-icon.cancel-edit[data-key='" + feature_code + "']").removeClass("hide")
    $(".feature-text-edit[name='" + feature_code + "']").removeClass("hide")
}

function feature_edit_icon_hide(feature_code) {
    //hide feature edit
    $(".feature-icon.save-edit[data-key='" + feature_code + "']").addClass("hide")
    $(".feature-icon.cancel-edit[data-key='" + feature_code + "']").addClass("hide")
    $(".feature-text-edit[name='" + feature_code + "']").addClass("hide")

    //show this feature normal mode
    $(".feature-icon.edit[data-key='" + feature_code + "']").removeClass("hide")
    $(".feature-icon.trash[data-key='" + feature_code + "']").removeClass("hide")
    $(".feature-text-place span[data-key='" + feature_code + "']").removeClass("hide")

}

function future_edit_icon_hide_all() {
    //close all  feature edit
    $(".feature-icon.save-edit").addClass("hide")
    $(".feature-icon.cancel-edit").addClass("hide")
    $(".feature-text-edit").addClass("hide")

    //show all  feature in edit mode
    $(".feature-icon.edit").removeClass("hide")
    $(".feature-icon.trash").removeClass("hide")
    $(".feature-text-place span").removeClass("hide")
}

// press edit icon
$(".feature-icon.edit").click(
    function () {
        //get code of this feature
        let feature_code = $(this).attr("data-key")

        future_edit_icon_hide_all()

        //and finally show this one edit mode
        feature_edit_icon_show(feature_code)
    }
)
// change some edit and now want to save them
$(".feature-icon.save-edit").click(
    function () {
        debugger
        let feature_code = $(this).attr("data-key")
        let feature_text = $('.feature-text-edit[name="' + feature_code + '"]').val()
        update_feature(feature_code, feature_text)
        future_edit_icon_hide_all()

    }
)

//cancel edit
$(".feature-icon.cancel-edit").click(
    function () {

        future_edit_icon_hide_all()

    }
)

$(".feature-add-form .cancel").click(
    function () {

        $(".add-feature").removeClass('hide')
        $(".feature-add-form").addClass('hide')
    }
)
$(".feature-add-form form .action-icon .icon.save").click(
    function () {
        debugger
        let Form = $("form[name='frm-feature-add']")
        let data = Form.serializeArray();
        let url = '/TeamFeature/insert/'
        // debugger;
        RunAjax(url, 'POST', data,
            function () {
                location.reload()
            })

    }
)
$('.add-feature').click(
    function () {

        let modal = $('.modal')
        // modal.css("display", "block")
        $.dialog({
            title: 'ایجاد قابلیت جدید',
            content: $(".modal").html(),
            animation: 'rotateYR',
            closeAnimation: 'RotateXR',
            animationBounce: 1.5,
            animationSpeed: 200,
            backgroundDismissAnimation: 'random',
            theme: 'modern',
            boxWidth: '500px',
            useBootstrap: false,
            onContentReady: function () {
                //when dialog appear new button create, so we must bind new click event
                this.$content.find('.action-icon .save').click(function () {
                    debugger
                    let Form = $("form[name='frm-feature-add']")
                    let data = Form.serializeArray();
                    let url = '/TeamFeature/insert/'
                    // debugger;
                    RunAjax(url, 'POST', data,
                        function () {
                            location.reload()
                        })


                })
                this.$content.find(".star-add-feature .new-star").click(
                    function () {
                        debugger
                        // let feature_code = $(this).attr('data-key')
                        let star_level = $(this).attr('data-val')
                        let star2 = '.new-star[data-val="2"]'
                        let star3 = '.new-star[data-val="3"]'


                        //if this feature is active, we must inactivate it
                        if ($(this).hasClass('active')) {

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
                        } else {

                            // now active this item
                            active_star(this, 'A')
                            // if we inactivate star 3, star 2 must inactivate too
                            if (star_level == 3 && !$(star2).hasClass('active'))
                                active_star(star2, 'A')
                        }
                        $(this).parents('.star-add-feature').find('.star-count').val(star_level)

                    }
                )


            }
        })

    }
)


$('.feature .title .trash').click(
    function () {

        let feature_code = $(this).parents('.feature').attr('data-key')
        let feature = $(this).parents('.feature')// delete this feature by jquery

        $.confirm({
            title: 'Delete',
            content: 'آیا از حذف قابلیت مورد نظر مطمئن هستید؟',
            buttons: {
                delete: function () {
                    feature.remove() // delete this feature by jquery
                    delete_feature(feature_code) // delete from data base
                    $.alert('حذف شد!');
                },
                cancel: function () {
                    $.alert('Canceled!');
                },

            }
        });
    }
)

/****************************** feature view code end ***********************************/
/****************************** corp view code start **********************************/
$(".corp .title").click(
    function () {
        debugger
        //get corp code
        let corp_code = $(this).parents('.corp').attr('data-key')
        let up = $(".corp[data-key='" + corp_code + "']  ").find('.title .little-arrow .up')
        let down = $(".corp[data-key='" + corp_code + "']  ").find('.title .little-arrow .down')
        //at first slide up all other panel except this panel
        $(".corp .situation-box ").not(".corp[data-key='" + corp_code + "'] .situation-box").slideUp("fast")
        // //find situation box of that corp and toggle slide
        $(".corp[data-key='" + corp_code + "'] .situation-box").slideToggle()
        // for add background for corp icons
        //   $(".corp-img").removeClass('select')
        $(".corp-img[data-key='" + corp_code + "']").toggleClass('select')

        // up.toggleClass("hide")
        // down.toggleClass("hide")

    }
)

// this for down and up a  little arrow that is in title
$(".corp-view .title ").click(function () {
    $(this).find(".rotate").toggleClass("down");
})

$('.corp .situation-box .panel-search .search-input').on('keyup',
    function () {
        debugger
        let feature_title = $(this).val()
        let tr = $(this).parents('.panel').find('.panel-body table tr')
        if (feature_title.length > 0) {
            tr.hide()
            tr.parent().find('[data-feature-title*="' + feature_title + '"]').show()
        } else {
            tr.show()
        }

    }
)
$('.corp-view .general-search-box .search-input').on('keyup',
    function () {
        let input_val = $(this).val()
        let corp_name = $(this).parents('.corp-view').find('.corp .title-icon')
        if (input_val.length > 0) {
            corp_name.hide()
            corp_name.parent().find('[data-corp-name*="' + input_val + '"]').show()
        } else {
            corp_name.show()
        }
    }
)
/****************************** corp view code end ***********************************/




