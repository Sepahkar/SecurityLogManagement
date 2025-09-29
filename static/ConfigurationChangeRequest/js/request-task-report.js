// document.addEventListener('DOMContentLoaded', function() {
//     // init datepicker روی همه inputهای با کلاس persian-date
//     window.pwtDatepicker.createInputFields('.persian-date', {
//         initialValue: false,  // اگه مقدار اولیه داری، true کن
//         minDate: new Date(),  // فقط از امروز به بعد (optional)
//         maxDate: false,       // یا محدودیت بالا
//         format: 'YYYY/MM/DD', // فرمت شمسی
//         autoClose: true,      // بعد از انتخاب ببنده
//         defaultText: {        // متن‌های فارسی
//             selectYear: 'انتخاب سال',
//             selectMonth: 'انتخاب ماه',
//             selectDay: 'انتخاب روز',
//             day: 'روز',
//             month: 'ماه'
//         },
//         onSelect: function(unix) {  // callback بعد از انتخاب
//             console.log('تاریخ انتخاب شد:', unix);  // unix timestamp
//         }
//     });
// });

// $(document).ready(function() {
//     $(".persian-date").pDatepicker();
//   });

//   window.pwtDatepicker.createInputFields('.persian-date', {
//     initialValue: false,
//     format: 'YYYY/MM/DD', // چیزی که کاربر می‌بینه
//     altField: '#hidden-date', // یک input مخفی برای مقدار واقعی
//     altFormat: 'YYYY/MM/DD', // فرمت دقیق برای ذخیره‌سازی
//     autoClose: true,
//     timePicker: {
//         enabled: false
//     }
// });

//     document.addEventListener('DOMContentLoaded', function() {
//         // ابتدایی‌سازی timepicker
//         const doneTimeInput = document.querySelector('input[name="done_time"]');
//         if (doneTimeInput) {
//             const timepicker = new TimepickerUI(doneTimeInput, {
//                 format: 'HH:mm', // فرمت 24 ساعته
//                 theme: 'light', // تم روشن
//                 mobile: true, // موبایل‌فرندلی
//                 hour12: false, // 24 ساعته (نه 12 ساعته)
//                 stepHour: 1, // گام ساعت
//                 stepMinute: 5, // گام دقیقه
//                 // گزینه‌های دیگه: onChange: function(time) { console.log(time); }
//             });
//             timepicker.create(); // ایجاد timepicker
//         }
//     });    

$(function(){ // document.ready
    // helper: تبدیل unix -> تاریخ میلادی به شکل YYYY/MM/DD (اعداد لاتین)
    function unixToGregorianString(unixMillis) {
      if (!unixMillis) return '';
      // persianDate از کتابخانه‌ی persian-date
      var pd = new persianDate(unixMillis); // unix به میلی‌ثانیه
      // تبدیل به تقویم میلادی و خروجی با اعداد لاتین
      return pd.toCalendar('gregorian').toLocale('en').format('YYYY/MM/DD');
      // توابع بالا مطابق مستندات persianDate/pwt.datepicker قابل استفاده‌اند. :contentReference[oaicite:2]{index=2}
    }
  
    // راه‌اندازی datepicker
    var picker = $('#persianDateInput').pDatepicker({
    format: 'dddd DD MMMM YYYY',         // فرمت نمایش در input (شما می‌تونید 'YYYY/MM/DD' بذارید)
      initialValue: !!$('#persianDateInput').data('date'), // اگه data-date داری مقدار اولیه بذار
      initialValueType: 'gregorian', // اگه data-date میلادیه بگو این مقدار از نوع میلادیه
      observer: true,              // اجازه‌ی ویرایش دستی (اختیاری)
      autoClose: true,
      timePicker: {
        enabled: false            // ⬅️ این خط ساعت را غیرفعال می‌کند (فقط تاریخ نشان داده می‌شود). :contentReference[oaicite:3]{index=3}
      },
      onSelect: function(unix) {   // وقتی کاربر تاریخ انتخاب کرد
        var g = unixToGregorianString(unix);
        $('#done_date').val(g);
      },
      onSet: function(unix) {      // وقتی مقدار با API یا set تغییر کرد (طبق مستندات)
        var g = unixToGregorianString(unix);
        $('#done_date').val(g);
      }
    });
  
    // اگر هنگام بارگذاری ویجت مقدار اولیه انتخاب شده باشد، مقدار hidden را هم ست کن
    try {
      var state = picker.getState && picker.getState(); // getState() موجود است و selected.unixDate می‌دهد. :contentReference[oaicite:4]{index=4}
      if (state && state.selected && state.selected.unixDate) {
        $('#done_date').val( unixToGregorianString(state.selected.unixDate) );
      } else {
        // یا اگر data-date به عنوان مقدار میلادی گذاشته شده بود، می‌توانیم مستقیماً آن را قرار دهیم:
        var dd = $('#persianDateInput').data('date');
        if (dd) { $('#done_date').val(dd); }
      }
    } catch(e){
      // ignore
    }
  
    // اختیاری: اگر می‌خوایم هنگام تغییر دستی کاربر هم همگام‌سازی کنیم
    $('#persianDateInput').on('change', function(){
      // تلاش می‌کنیم مقدار فعلی ویجت را بخوانیم از state (اگر موجود باشد)
      try {
        var st = picker.getState();
        if (st && st.selected && st.selected.unixDate) {
          $('#done_date').val( unixToGregorianString(st.selected.unixDate) );
        }
      } catch(e){}
    });

    const input = document.getElementById('timepicker');
    const TimepickerUI = window.TimepickerUI.TimepickerUI;
  
    const time_picker = new TimepickerUI(input, {
      clockType: '24h',
      enableSwitchIcon: true, // آیکون تعویض AM/PM (در حالت 12h)
      showSeconds: false,     // ثانیه‌ها رو مخفی کن
      autoClose: true         // بعد از انتخاب بسته بشه
      // inline: { enabled: true } // ❌ این رو نذار، چون همون باعث میشه از اول باز باشه
    });
  
    time_picker.create();
  
    // وقتی ساعت انتخاب شد، بریز تو hidden
    $(input).on("accept.tui.timepicker", function (event) {
      const value = $(this).val();
      $("#done_time").val(value);
      console.log("ساعت انتخاب شد:", value);
    });

  
  });