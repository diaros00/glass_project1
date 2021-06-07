"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blogs import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.hello),
    path('createForm/', views.createForm),
    path('addForm', views.addUser),
    path('report', views.report, name='pie-chart'),
    path('',views.loginForm),
    path('login',views.login),
    path('addDefect', views.addDefect),
    path('addModel', views.addModel),
    path('logout',views.logout),
    path('collector',views.collector),
    path('choose_defect_on_glass',views.choose_defect_on_glass),
    path('add_no_defect',views.add_no_defect),
    path('add_have_defect',views.add_have_defect),
    path('filtering',views.filtering),
    path('add_defect1',views.add_defect1),
    path('add_defect2',views.add_defect2),
    path('add_defect3',views.add_defect3),
    path('add_defect4',views.add_defect4),
    path('add_defect5',views.add_defect5),
    path('add_defect6',views.add_defect6),
    path('add_defect7',views.add_defect7),
    path('add_defect8',views.add_defect8),
    path('add_defect9',views.add_defect9),
    path('add_defect10',views.add_defect10),
    path('add_defect11',views.add_defect11),
    path('add_defect12',views.add_defect12),
    path('add_defect13',views.add_defect13),
    path('add_defect14',views.add_defect14),
    path('add_defect15',views.add_defect15),
    path('add_defect16',views.add_defect16),
    path('add_defect17',views.add_defect17),
    path('add_defect18',views.add_defect18),
    path('add_defect19',views.add_defect19),
    path('add_defect20',views.add_defect20),
    path('add_defect21',views.add_defect21),
    path('add_defect22',views.add_defect22),
    path('add_defect23',views.add_defect23),
    path('add_defect24',views.add_defect24),
    path('add_defect25',views.add_defect25),
    path('add_defect26',views.add_defect26),
    path('add_defect27',views.add_defect27),
    path('add_defect28',views.add_defect28),
    path('add_defect29',views.add_defect29),
    path('add_defect30',views.add_defect30),
    path('add_defect31',views.add_defect31),
    path('add_defect32',views.add_defect32),
    path('add_defect33',views.add_defect33),
    path('add_defect34',views.add_defect34),
    path('add_defect35',views.add_defect35),
    path('add_defect36',views.add_defect36),
    path('add_defect37',views.add_defect37),
    path('add_defect38',views.add_defect38),
    path('add_defect39',views.add_defect39),
    path('add_defect40',views.add_defect40),
    path('add_defect41',views.add_defect41),
    path('add_defect42',views.add_defect42),
    path('add_defect43',views.add_defect43),
    path('add_defect44',views.add_defect44),
    path('add_defect45',views.add_defect45),
    path('add_defect46',views.add_defect46),
    path('add_defect47',views.add_defect47),
    path('add_defect48',views.add_defect48),
    path('add_defect49',views.add_defect49),
    path('add_defect50',views.add_defect50),
    path('add_defect51',views.add_defect51),
    path('add_defect52',views.add_defect52),
    path('add_defect53',views.add_defect53),
    path('add_defect54',views.add_defect54),
    path('add_defect55',views.add_defect55),
    path('add_defect56',views.add_defect56),
    path('add_defect57',views.add_defect57),
    path('add_defect58',views.add_defect58),
    path('add_defect59',views.add_defect59),
    path('add_defect60',views.add_defect60),
    path('add_defect61',views.add_defect61),
    path('add_defect62',views.add_defect62),
    path('add_defect63',views.add_defect63),
    path('add_defect64',views.add_defect64),
    path('add_defect65',views.add_defect65),
    path('add_defect66',views.add_defect66),
    path('add_defect67',views.add_defect67),
    path('add_defect68',views.add_defect68),
    path('add_defect69',views.add_defect69),
    path('add_defect70',views.add_defect70),
    path('add_defect71',views.add_defect71),
    path('add_defect72',views.add_defect72),
    path('add_defect73',views.add_defect73),
    path('add_defect74',views.add_defect74),
    path('add_defect75',views.add_defect75),
    path('add_defect76',views.add_defect76),
    path('add_defect77',views.add_defect77),
    path('add_defect78',views.add_defect78),
    path('add_defect79',views.add_defect79),
    path('add_defect80',views.add_defect80),
    path('add_defect81',views.add_defect81),
    path('add_defect82',views.add_defect82),
    path('add_defect83',views.add_defect83),
    path('add_defect84',views.add_defect84),
    path('add_defect85',views.add_defect85),
    path('add_defect86',views.add_defect86),
    path('add_defect87',views.add_defect87),
    path('add_defect88',views.add_defect88),
    path('add_defect89',views.add_defect89),
    path('add_defect90',views.add_defect90),
    path('add_defect91',views.add_defect91),
    path('add_defect92',views.add_defect92),
    path('add_defect93',views.add_defect93),
    path('add_defect94',views.add_defect94),
    path('add_defect95',views.add_defect95),
    path('add_defect96',views.add_defect96),
    path('add_defect97',views.add_defect97),
    path('add_defect98',views.add_defect98),
    path('add_defect99',views.add_defect99),
    path('add_defect100',views.add_defect100),
    path('add_defect101',views.add_defect101),
    path('add_defect102',views.add_defect102),
    path('add_defect103',views.add_defect103),
    path('add_defect104',views.add_defect104),
    path('add_defect105',views.add_defect105),
    path('add_defect106',views.add_defect106),
    path('add_defect107',views.add_defect107),
    path('add_defect108',views.add_defect108),
    path('add_defect109',views.add_defect109),
    path('add_defect110',views.add_defect110),
    path('add_defect111',views.add_defect111),
    path('add_defect112',views.add_defect112),
    path('add_defect113',views.add_defect113),
    path('add_defect114',views.add_defect114),
    path('add_defect115',views.add_defect115),
    path('add_defect116',views.add_defect116),
    path('add_defect117',views.add_defect117),
    path('add_defect118',views.add_defect118),
    path('add_defect119',views.add_defect119),
    path('add_defect120',views.add_defect120),
    path('add_defect121',views.add_defect121),
    path('add_defect122',views.add_defect122),
    path('add_defect123',views.add_defect123),
    path('add_defect124',views.add_defect124),
    path('add_defect125',views.add_defect125),
    path('add_defect126',views.add_defect126),
    path('add_defect127',views.add_defect127),
    path('add_defect128',views.add_defect128),
    path('add_defect129',views.add_defect129),
    path('add_defect130',views.add_defect130),
    path('add_defect131',views.add_defect131),
    path('add_defect132',views.add_defect132),
    path('add_defect133',views.add_defect133),
    path('add_defect134',views.add_defect134),
    path('add_defect135',views.add_defect135),
    path('add_defect136',views.add_defect136),
    path('add_defect137',views.add_defect137),
    path('add_defect138',views.add_defect138),
    path('add_defect139',views.add_defect139),
    path('add_defect140',views.add_defect140),
    path('add_defect141',views.add_defect141),
    path('add_defect142',views.add_defect142),
    path('add_defect143',views.add_defect143),
    path('add_defect144',views.add_defect144),
    path('add_defect145',views.add_defect145),
    path('add_defect146',views.add_defect146),
    path('add_defect147',views.add_defect147),
    path('add_defect148',views.add_defect148),
    path('add_defect149',views.add_defect149),
    path('add_defect150',views.add_defect150),
    path('add_defect151',views.add_defect151),
    path('add_defect152',views.add_defect152),
    path('add_defect153',views.add_defect153),
    path('add_defect154',views.add_defect154),
    path('add_defect155',views.add_defect155),
    path('add_defect156',views.add_defect156),
    path('add_defect157',views.add_defect157),
    path('add_defect158',views.add_defect158),
    path('add_defect159',views.add_defect159),
    path('add_defect160',views.add_defect160),
    path('add_defect161',views.add_defect161),
    path('add_defect162',views.add_defect162),
    path('add_defect163',views.add_defect163),
    path('add_defect164',views.add_defect164),
    path('add_defect165',views.add_defect165),
    path('add_defect166',views.add_defect166),
    path('add_defect167',views.add_defect167),
    path('add_defect168',views.add_defect168),
    path('add_defect169',views.add_defect169),
    path('add_defect170',views.add_defect170),
    path('add_defect171',views.add_defect171),
    path('add_defect172',views.add_defect172),
    path('add_defect173',views.add_defect173),
    path('add_defect174',views.add_defect174),
    path('add_defect175',views.add_defect175),

    
    
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)