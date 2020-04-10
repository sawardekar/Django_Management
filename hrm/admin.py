from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from hrm.models import Employee, EmployeeType, Product
# Register your models here.


# Admin Action Functions to update all employee gender as Male
def update_gender_all(modeladmin, request, queryset):
    queryset.update(gender='Male')


# Action description
update_gender_all.short_description = "Mark Selected Gender update as Male"


class EmployeeAdmin(admin.ModelAdmin):
    exclude = ('created_at',)   # exclude list of fields those not display in admin form
    # fields = ('name', 'address', 'gender','age')  # list of fields display in admin form
    # readonly_fields = ('age',)  # list of fields as readonly [NonEditable fields]
    sortable_by = 'id'  # field 'id' sorted by descending order
    date_hierarchy = 'created_at'  # field 'created_at' as date field display as descending order
    search_fields = ['name', 'address', 'gender']  # list of fields search in admin table
    list_display = ('image_tag', 'name', 'address','email','gender','age','mobile','type','get_products','display_age') # list of fields display in admin table
    list_display_links = ('name', 'address')  # list of fields display in table show as link
    list_select_related = ('type',)  # select_related in added only foreign key fields for query performance
    list_filter = ('name',)  # list of fields filter in admin table
    list_editable = ('age',)  # list of fields editable in admin table
    filter_vertical = ('product',)  # filter vertical in added only manytomany fields for filter will displayed
    actions = [update_gender_all]  # admin action function called
    # group wise fields display in admin form
    # fieldsets = [
    #     ('Body', {'classes': ('full-width',), 'fields': ('address',)})
    # ]
    change_list_template = 'admin/admin_filter_list.html'  # admin template called

    # manytomany fields display in admin table and multiple value separate by comma
    def get_products(self, obj):
        return ", ".join([p.name for p in obj.product.all()])

    # custom url created in admin table and added in django url
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('age/<int:age_count>/', self.update_age)
        ]
        return custom_urls + urls

    # all employee age updated
    def update_age(self, request, age_count):
        self.model.objects.all().update(age=age_count)
        self.message_user(request, 'All Employee Age changes Successfully')
        return HttpResponseRedirect("../")

    # custom admin function employee age wise font size increase
    def display_age(self, obj):
        display_size = obj.age if obj.age <= 60 else 60
        return format_html(
            f'<span style="font-size : {display_size}px;">{obj.age}</span>'
        )

# unregister app
admin.site.unregister(Group)

# register app
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeType)
admin.site.register(Product)

# admin header and title modification
admin.site.site_header = "Admin DashBoard"
admin.site.site_title = "Ecommerce"
admin.site.index_title = ''


# install django suit using below command
# pip install https://github.com/darklow/django-suit/tarball/v2