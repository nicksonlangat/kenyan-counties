try:
    from django.contrib import admin
    from .models import County, Constituency, Ward

    @admin.register(County)
    class CountyAdmin(admin.ModelAdmin):
        list_display = ("code", "name")
        search_fields = ("name",)
        ordering = ("code",)

    @admin.register(Constituency)
    class ConstituencyAdmin(admin.ModelAdmin):
        list_display = ("name", "county")
        search_fields = ("name",)
        list_filter = ("county",)
        ordering = ("county", "name")

    @admin.register(Ward)
    class WardAdmin(admin.ModelAdmin):
        list_display = ("name", "constituency")
        search_fields = ("name",)
        list_filter = ("constituency__county",)
        ordering = ("constituency", "name")

except ImportError:
    pass
