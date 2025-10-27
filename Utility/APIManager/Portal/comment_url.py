def ver1(doc_id:int)->dict:
        """
        این تابع آدرس فرم یادداشت و تعداد یادداشت های ثبت شده را بازگشت می دهد

        Args:
            doc_id (str): شناسه مدرک

        Returns:
            dict: یک چیزی شبیه به این است:
                {'url':f'http://127.0.0.1/{int}', 'comment_count':comment_count}
        """
        
        import random
        comment_count = random.randint(0, 3)
        
        return {'url':f'http://127.0.0.1/{doc_id}', 'comment_count':comment_count}