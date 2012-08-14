from django.db import models


class Announcement(models.Model):
    """
    Create a new announcement message.
    """
    created_on = models.DateTimeField(auto_now_add=True)

    # Hero Unit block
    hero_unit_title = models.CharField(
        help_text="Enter the title used in Hero Unit block.",
        max_length=128
    )
    hero_unit_desc = models.TextField(
        help_text="Enter the description used in Hero Unit block.",
        max_length=255
    )
    show_hero_unit = models.BooleanField(
        verbose_name="Show the Hero Unit block",
        default=True
    )

    # Announce block
    title = models.CharField(
        help_text="Enter the title for this announcement.",
        max_length=128
    )
    content = models.TextField(
        help_text="Enter the body of the announcement. " \
                  "Use <a href=\"http://daringfireball.net/projects/markdown/syntax\">Markdown</a> syntax."
    )
    is_enabled = models.BooleanField(
        verbose_name="Enabled",
        help_text="Enable this announcement.<br><strong>Note:</strong> it will replace the currently enabled one !"
    )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        announces_enabled = Announcement.objects.filter(is_enabled=True)
        announces_enabled.update(is_enabled=False)

        super(Announcement, self).save(*args, **kwargs)
