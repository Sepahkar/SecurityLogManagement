def ver1(doc_id:int)-> str:
        """
        این تابع شناسه یک شناسه سند را می گیرد و آدرس صفحه گردش کار را بازگشت می دهد

        Args:
            doc_id (int): شناسه مدرکی که باید گردش آن نمایش داده شود

        Returns:
            str: آدرس صفحه نمایش گردش مدرک
        """
        return f'http://eit-app:23000/Cartable/WorkFlowTable/?doc_pk={doc_id}' 
        # return f'http://127.0.0.1:10000/flow/{doc_id}'  

