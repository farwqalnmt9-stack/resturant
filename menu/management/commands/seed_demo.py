from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from menu.models import Category, Extra, Product

DATA={
 'وجبات رئيسية':[('فتة دجاج','دجاج مشوي، خبز مقرمش وصلصة لبن غنية',28000),('مقلوبة باذنجان','أرز بسمتي وخضار موسمية ولحم طري',34000),('كبة لبنية','كبة محشوة مطهوة بلبن ريفي',26000)],
 'بيتزا':[('بيتزا خضار مشوية','خضار طازجة، موزاريلا وصلصة طماطم',23000),('بيتزا بيبروني','شرائح بيبروني وموزاريلا ذائبة',27000)],
 'برغر':[('برغر سُفرة','لحم مشوي، جبن مدخن وصوص الدار',30000),('برغر دجاج كرسبي','دجاج مقرمش، كولسلو وصوص حار',26000)],
 'شاورما':[('شاورما دجاج عربي','خبز عربي، ثوم وبطاطا مقلية',22000),('شاورما لحم','لحم متبّل، طحينة وخضار مقرمشة',25000)],
 'مشاوي':[('مشاوي مشكلة','كباب، شيش طاووق وريش على الفحم',42000),('شيش طاووق','قطع دجاج متبلة ومشوية على الفحم',30000),('كباب حلبي','لحم مفروم وتتبيلة حلبية أصلية',32000)],
 'مقبلات':[('حمص باللحمة','حمص ناعم ولحم مشوي وصنوبر',16000),('متبل باذنجان','باذنجان مدخن وطحينة وزيت زيتون',14000)],
 'سلطات':[('فتوش','خضار مقطعة وخبز محمص ودبس رمان',12000),('تبولة','بقدونس طازج وبرغل ناعم',11000)],
 'حلويات':[('كنافة نابلسية','كنافة ساخنة وقطر خفيف',15000),('مهلبية فستق','حليب وفستق حلبي',10000)],
 'مشروبات':[('ليمون بالنعناع','ليمون طازج ونعناع أخضر',8000),('عصير رمان','عصير رمان طبيعي بارد',12000)],
}

class Command(BaseCommand):
    help='Creates restaurant demo categories and 20+ products.'
    def handle(self,*args,**kwargs):
        extras=[]
        for name,price in [('جبنة إضافية',3000),('صوص إضافي',2000),('بدون بصل',0),('حار',0)]: extras.append(Extra.objects.get_or_create(name=name,defaults={'price':price})[0])
        count=0
        for category_name, products in DATA.items():
            category,_=Category.objects.get_or_create(name=category_name,defaults={'slug':slugify(category_name,allow_unicode=True)})
            for index,(name,description,price) in enumerate(products):
                product,_=Product.objects.get_or_create(name=name,defaults={'slug':slugify(name,allow_unicode=True),'description':description,'price':Decimal(price),'category':category,'featured':count<6})
                product.extras.set(extras); count+=1
        self.stdout.write(self.style.SUCCESS(f'Created or kept {count} demo meals.'))
