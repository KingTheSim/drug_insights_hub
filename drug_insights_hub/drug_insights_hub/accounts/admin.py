from django.contrib import admin
from drug_insights_hub.accounts.models import Affiliation, UserProfile

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'description', 'website')
    list_filter = ('name', 'location', 'description', 'website')
    search_fields = ('name', 'location', 'description', 'website')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('bio', 'interests','specialization', 'user')
    list_filter = ('bio', 'interests','specialization', 'user')
    search_fields = ('bio', 'interests','specialization', 'user')