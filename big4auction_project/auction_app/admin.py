from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(Bid)
admin.site.register(Transaction)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(Report)
admin.site.register(PaymentMethod)
admin.site.register(Category)
