from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Item, ItemImage, Bid, Transaction, Notification, Feedback, Report, PaymentMethod, Category, User


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1  # Number of empty forms to display for adding new item images inline

class BidInline(admin.TabularInline):
    model = Bid
    extra = 1  # Number of empty forms to display for adding new bids inline

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1  # Number of empty forms to display for adding new transactions inline

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'read_status')
    list_filter = ('read_status',)
    search_fields = ('user__username', 'message')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_user', 'item', 'timestamp')
    search_fields = ('reporter__username', 'reported_user__username', 'item__title')
    list_filter = ('timestamp',)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'current_bid', 'status')
    search_fields = ('title', 'seller__username')
    list_filter = ('status', 'category')
    prepopulated_fields = {'slug':('title',)}
    inlines = [ItemImageInline, BidInline, TransactionInline]

class UserAdmin(BaseUserAdmin):
    #add_form = CustomUserCreationForm
    #form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email', 'phone_number', 'date_joined', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('address', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'address', 'phone_number', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

# Registering the models with the customized admin classes
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage)
admin.site.register(Bid)
admin.site.register(Transaction)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Feedback)
admin.site.register(Report, ReportAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Category)
admin.site.register(User, UserAdmin)
