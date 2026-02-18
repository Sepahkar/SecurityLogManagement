import requests
from Utility import configs
from shared_lib import core as slcore


def ver1(doc_id: int) -> dict:
    """
    Returns comment page URL and comment count from Portal.

    Args:
        doc_id (int): Document ID

    Returns:
        dict:
        {
            'url': 'http://portal/Cartable/comments/page/?document_id=...',
            'comment_count': int
        }
    """

    # 🔹 Base Portal address (replace with config if available)
    base_url = "http://eit-app:23000"

    # 🔹 Comment count API endpoint
    count_url = f"{base_url}/Cartable/api/comments/count/?document_id={doc_id}"

    try:
        response = requests.get(
            count_url,
            # params={"document_id": doc_id},
            headers = {
                "Service-Authorization": slcore.generate_token("v.bagheri"),
                "Content-Type": "application/json",
            },
            timeout=5
        )

        response.raise_for_status()
        data = response.json()

        comment_count = data.get("comment_count", 0)

    except Exception:
        # Fail safe → do not break SecurityLogManagement
        comment_count = 0

    # 🔹 Comment page URL
    page_url = f"{base_url}/Cartable/comments/page/?document_id={doc_id}"

    return {
        "url": page_url,
        "comment_count": comment_count
    }





# def ver1(doc_id:int)->dict:
#         """
#         این تابع آدرس فرم یادداشت و تعداد یادداشت های ثبت شده را بازگشت می دهد

#         Args:
#             doc_id (str): شناسه مدرک

#         Returns:
#             dict: یک چیزی شبیه به این است:
#                 {'url':f'http://127.0.0.1/{int}', 'comment_count':comment_count}
#         """
        
#         import random
#         comment_count = random.randint(0, 3)
        
#         return {'url':f'http://127.0.0.1/{doc_id}', 'comment_count':comment_count}