def v1() -> list[dict]:
    """Returns all Roles. *Using the HR API v1*.
    returns a list of dictionary that contains:

    {
        "RoleId": 45,
        "RoleName": "ادمين ديتابيس",
        "HasLevel": True,
        "HasSuperior": False
    }

    """
    return [
    {
        "RoleId": 45,
        "RoleName": "ادمين ديتابيس",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 48,
        "RoleName": "مدير تحقيق و توسعه",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 51,
        "RoleName": "کارشناس نسخه",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 52,
        "RoleName": "کارشناس کنترل پروژه",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 55,
        "RoleName": "تحليل گر تست",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 56,
        "RoleName": "تحليل گر سيستم",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 57,
        "RoleName": "تحليل گر کسب و کار",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 58,
        "RoleName": "مدير محصول",
        "HasLevel": False,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 61,
        "RoleName": "مدير پروژه",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 63,
        "RoleName": "برنامه نويس",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 68,
        "RoleName": "گزارش ساز",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 69,
        "RoleName": "پشتيبان",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 72,
        "RoleName": "تستر",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 77,
        "RoleName": "کارشناس حسابداري",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 78,
        "RoleName": "کارشناس  جذب",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 79,
        "RoleName": "کارشناس امور مشتريان",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 80,
        "RoleName": "مدير مالي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 81,
        "RoleName": "کارشناس مستندسازي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 82,
        "RoleName": "مدير عامل",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 83,
        "RoleName": "مدير امور اداري",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 84,
        "RoleName": "مدير فناوري اطلاعات",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 85,
        "RoleName": "کارشناس منابع انساني",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 86,
        "RoleName": "کارشناس حقوق و دستمزد",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 87,
        "RoleName": "خدمات",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 88,
        "RoleName": "سرپرست واحد جذب و آموزش",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 90,
        "RoleName": "کارشناس IT",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 91,
        "RoleName": "قائم مقام مدير عامل",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 92,
        "RoleName": "نگهبان",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 95,
        "RoleName": "کارشناس سيستم ارزيابي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 96,
        "RoleName": "منشي",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 97,
        "RoleName": "کمک مدرس آموزش",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 98,
        "RoleName": "کارشناس اداري",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 99,
        "RoleName": "سرپرست تدارکات و تأسيسات",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 100,
        "RoleName": "کارشناس آموزش",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 101,
        "RoleName": "طراح گرافيک",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 102,
        "RoleName": "کارشناس امور قراردادها",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 103,
        "RoleName": "مدير فروش و امور قراردادها",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 104,
        "RoleName": "مدير تحقيقات و برنامه ريزي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 105,
        "RoleName": "مدير ارتباطات و برندينگ",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 106,
        "RoleName": "مدير تيم تست",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 107,
        "RoleName": "مدير نسخه",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 108,
        "RoleName": "معاون فني",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 109,
        "RoleName": "معاون عمليات",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 110,
        "RoleName": "معاون اداري ومالي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 111,
        "RoleName": "معاون محصول",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 113,
        "RoleName": "معاون پروژه",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 115,
        "RoleName": "مدير تيم پشتيباني",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 116,
        "RoleName": "مديرادمين",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 117,
        "RoleName": "پرسنل آموزشي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 118,
        "RoleName": "کارشناس ارتباطات و برندينگ",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 119,
        "RoleName": "کارشناس فرآيند",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 120,
        "RoleName": "معاون توسعه ارتباط با مشتريان",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 121,
        "RoleName": "مديرتيم ارزيابي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 122,
        "RoleName": "مديرتيم مستندسازي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 123,
        "RoleName": "کارشناس مهندسي فروش",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 124,
        "RoleName": "Scrum Master",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 125,
        "RoleName": "کارشناس تحقيقات بازار  ",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 126,
        "RoleName": "کارشناس توليد محتوا",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 127,
        "RoleName": "NoneTechnicalRole",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 131,
        "RoleName": "مدير امور مشتريان",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 132,
        "RoleName": "مدير سامانه هاي ستادي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 133,
        "RoleName": "کمک حسابدار",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 134,
        "RoleName": "طراح UI/UX ",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 135,
        "RoleName": "مستندساز ",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 136,
        "RoleName": "مسئول اجرايي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 137,
        "RoleName": "کارآموز کنترل پروژه",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 138,
        "RoleName": "مشاور",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 139,
        "RoleName": "مجازي",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 140,
        "RoleName": "راهبر تيم توسعه",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 141,
        "RoleName": "معاون پشتيباني",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 142,
        "RoleName": "برنامه نويس UI",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 143,
        "RoleName": "کارپرداز",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 144,
        "RoleName": "تحليل گر داده",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 145,
        "RoleName": "رئيس حسابداري",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 146,
        "RoleName": "پيمانکار برق",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 147,
        "RoleName": "مسئول دفتر مديرعامل",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 148,
        "RoleName": "Data Scientist",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 149,
        "RoleName": "Data Engineer",
        "HasLevel": True,
        "HasSuperior": True,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 150,
        "RoleName": "سرپست امنيت و شبکه",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 151,
        "RoleName": "ادمين جيرا",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 152,
        "RoleName": "کارشناس power BI ",
        "HasLevel": True,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    },
    {
        "RoleId": 153,
        "RoleName": "کارآموز",
        "HasLevel": False,
        "HasSuperior": False,
        "Comment": None,
        "NewRoleRequest": None
    }
]

