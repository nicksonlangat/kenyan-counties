try:
    from django.db import models
except ImportError:
    class models:
        class Model:
            pass
        class CharField:
            def __init__(self, *args, **kwargs): pass
        class IntegerField:
            def __init__(self, *args, **kwargs): pass
        class ForeignKey:
            def __init__(self, *args, **kwargs): pass
        CASCADE = None

class County(models.Model):
    code = models.IntegerField(unique=True, primary_key=True, help_text="Unique county code (1-47)")
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "counties"
        ordering = ["code"]

    def __str__(self):
        return f"{self.name} ({self.code})"

class Constituency(models.Model):
    county = models.ForeignKey(County, related_name="constituencies", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "constituencies"
        ordering = ["name"]
        unique_together = [("county", "name")]

    def __str__(self):
        return f"{self.name} - {self.county.name}"

class Ward(models.Model):
    constituency = models.ForeignKey(Constituency, related_name="wards", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        unique_together = [("constituency", "name")]

    def __str__(self):
        return f"{self.name} - {self.constituency.name}"
