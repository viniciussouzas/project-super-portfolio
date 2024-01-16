from django.contrib import admin
from .models import Profile, Project, CertifyingInstitution, Certificate


class CertificateInline(admin.StackedInline):
    model = Certificate


class CertifiyingInstitutionAdmin(admin.ModelAdmin):
    inlines = [CertificateInline]


admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(CertifyingInstitution, CertifiyingInstitutionAdmin)