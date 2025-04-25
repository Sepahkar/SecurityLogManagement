from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ConfigurationChangeRequest
from .serializers import ConfigurationChangeRequestSerializer
from Utility.APIManager.Portal.register_document import v1 as RegisterDocument
from Utility.APIManager.Portal.send_document import ver1 as send_document
from Utility.APIManager.Portal.update_document import v1 as update_document


@api_view(['GET'])
def configuration_change_request_list(request):
    """
    لیست تمام درخواست‌های تغییر را برمی‌گرداند.
    """
    requests = ConfigurationChangeRequest.objects.all()
    serializer = ConfigurationChangeRequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def configuration_change_request_create(request):
    """
    یک درخواست تغییر جدید ایجاد می‌کند.
    """
    serializer = ConfigurationChangeRequestSerializer(data=request.data)
    if serializer.is_valid():
        request_instance = serializer.save()  # ذخیره رکورد و دریافت نمونه آن

        # صدا زدن تابع RegisterDocument
        # فرض بر این است که پارامترهای لازم را از request_instance می‌گیریم
        doc_response = RegisterDocument(
            app_doc_id=request_instance.id,  # شناسه درخواست تغییر
            priority="عادی",  # اولویت سند
            doc_state="New",  #وضعیت سند
            document_title= 'درخواست تغییرات ' + request_instance.change_title,  # عنوان سند
            app_code="CCR",  # کد برنامه
            owner=request_instance.requestor_nationalcode  #  مالک سند فرد درخواست دهنده است
        )

        if doc_response.get("msg") == "success":  # اگر ثبت موفقیت‌آمیز بود
            doc_id = doc_response["data"]["id"]  # دریافت شناسه سند
            request_instance.DocId = doc_id  # ذخیره شناسه در فیلد DocId
            request_instance.save()  # ذخیره تغییرات در پایگاه داده

            manger_nationalcode = '1234567890'  # دریافت کد ملی مدیر
            # صدا زدن تابع send_document
            send_response = send_document(
                doc_id=doc_id,  # شناسه سند
                sender=request_instance.requestor_nationalcode,  # فرستنده در اولین مرحله ایجاد کننده است
                inbox_owners=[manger_nationalcode]  # لیست دریافت‌کنندگان
            )
            
            if send_response.get("msg") == "success":  # اگر ارسال موفقیت‌آمیز بود
                request_instance.state_code = 'MANAGE'  # تغییر وضعیت سند به "MANAGER"
                request_instance.save()  # ذخیره تغییرات در پایگاه داده
                doc_state = request_instance.get_state_display()  # مقدار متنی را دریافت می‌کنیم
                update_document(doc_id=doc_id, doc_state=doc_state)  # تغییر وضعیت سند به متناظر            return Response({'id': request_instance.id}, status=status.HTTP_201_CREATED)  # بازگشت شناسه رکورد جدید
                
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def configuration_change_request_detail(request, pk):
    """
    جزئیات یک درخواست تغییر خاص را برمی‌گرداند.
    """
    try:
        request_instance = ConfigurationChangeRequest.objects.get(pk=pk)
    except ConfigurationChangeRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ConfigurationChangeRequestSerializer(request_instance)
    return Response(serializer.data)

@api_view(['PUT'])
def configuration_change_request_update(request, pk):
    """
    یک درخواست تغییر خاص را به‌روز می‌کند.
    """
    try:
        request_instance = ConfigurationChangeRequest.objects.get(pk=pk)
    except ConfigurationChangeRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ConfigurationChangeRequestSerializer(request_instance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def configuration_change_request_partial_update(request, pk):
    """
    یک درخواست تغییر خاص را به‌صورت جزئی به‌روز می‌کند.
    """
    try:
        request_instance = ConfigurationChangeRequest.objects.get(pk=pk)
    except ConfigurationChangeRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ConfigurationChangeRequestSerializer(request_instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def configuration_change_request_delete(request, pk):
    """
    یک درخواست تغییر خاص را حذف می‌کند.
    """
    try:
        request_instance = ConfigurationChangeRequest.objects.get(pk=pk)
    except ConfigurationChangeRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)