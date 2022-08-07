from django.db import models
from django.utils.translation import gettext_lazy as _


class Images(models.Model):
    original_url = models.URLField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_("URL"),
        help_text=_("URL of the Image"),
    )
    media = models.ImageField(
        upload_to="images/",
        verbose_name=_("File"),
        help_text=_("Image File"),
    )
    width = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Width"),
        help_text=_("Width of the image"),
    )
    height = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Height"),
        help_text=_("Height of the image"),
    )
    size = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Size"),
        help_text=_("Size of the document in KB"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, using=None, keep_parents=False):
        """
        Override delete method
        to delete the file if the document is deleted
        """
        self.media.delete(save=False)
        super().delete(using, keep_parents)

    def save(self, *args, **kwargs):
        """
        Override save method
        to delete old file if new file is uploaded
        """
        if self.pk:
            old_file = Images.objects.get(pk=self.pk).media
            if old_file != self.media:
                old_file.delete(save=False)
        super().save(*args, **kwargs)

