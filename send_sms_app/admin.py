from django.contrib import admin
from django.contrib import messages
from .models import Mutualist, Sms
from . import tasks
from dotenv import load_dotenv
import os

load_dotenv()


class MutualistInline(admin.TabularInline):
    model = Sms.mutualists.through



@admin.register(Mutualist)
class Mutualistdmin(admin.ModelAdmin):
    
    list_display = ["full_name", "phone"]
    list_filter = ["full_name",]
    search_fields = ["full_name", "phone"]
    ordering = ("full_name",)



@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    
    list_display = ["content"]
    actions = ["send_sms"]


    @admin.action(description="envoyer un sms aux mutualistes")
    def send_sms(self, request, queryset):

        access_token = tasks.get_token.delay(os.getenv("TOKEN_URL")).get()
        content_list = " ".join([c.content for c in queryset])
        phone_list = []
        for sms in queryset:
            mutualist_list = sms.mutualists.all()
            for m in mutualist_list:
                phone_list.append(m.phone)
 

        # phone_list = (m for m in Mutualist.objects.values_list("phone", flat=True))
        tasks.send_mass_sms_task(phone_list, content_list, access_token)
        self.message_user(
            request, "Message(s) envoyé(s) à tous les mutualistes", messages.SUCCESS,
        )