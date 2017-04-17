from django.contrib import admin
import register_activate.models


class User_infoAdmin(admin.ModelAdmin):
    list_display = ['surname',
                    'name',
                    'middlename',
                    'country',
                    'city',
                    'phone',
                    'birthday',
                    'gender',
                    'time_zone',
                    'time_congratulations']


admin.site.register(register_activate.models.User_info, User_infoAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['country',
                    'description',
                    'data',
                    'name']


admin.site.register(register_activate.models.Type, TypeAdmin)


class CongratulationsAdmin(admin.ModelAdmin):
    list_display = ['type_id',
                    'user_id',
                    'status',
                    'category_cmc',
                    'text',
                    'data_created']
    actions = ['status2', 'status']
    list_filter = ('status',)

    def status2(self, request, queryset):
        queryset.update(status='2')

    status2.short_description = "Принять поздравления"

    def status(self, request, queryset):
        queryset.update(status='0')

    status.short_description = "Отклонить поздравления"


admin.site.register(register_activate.models.Congratulations, CongratulationsAdmin)


class LettersAdmin(admin.ModelAdmin):
    list_display = ['user_letters',
                    'text_letters',
                    'date_create',
                    'date_send',
                    'email_create',
                    'email_send',
                    'status']
    actions = ['status2', 'status']
    list_filter = ('status',)

    def status2(self, request, queryset):
        queryset.update(status='2')

    status2.short_description = "Одобрить письмо"

    def status(self, request, queryset):
        queryset.update(status='0')

    status.short_description = "Отклонить письмо"


admin.site.register(register_activate.models.Letters, LettersAdmin)
