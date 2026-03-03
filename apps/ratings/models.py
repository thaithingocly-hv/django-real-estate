"""
Mục đích: Một user đánh giá một agent (Profile) với số sao + comment.
Qui trình: User (rater)  →  Rating  →  Profile (agent)
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from realEstate.settings.base import AUTH_USER_MODEL
from apps.common.models import TimeStampedUUIDModel
from apps.profiles.models import Profile


class Rating(TimeStampedUUIDModel):
    class Range(models.IntegerChoices):
        RATING_1 = 1, _("Poor")
        RATING_2 = 2, _("Fair")
        RATING_3 = 3, _("Good")
        RATING_4 = 4, _("Very Good")
        RATING_5 = 5, _("Excellent")

    rater = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("User providing the rating"),
        related_name="ratings_given",
    )
    agent = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Agent being rated"),
        related_name="ratings_received",
    )
    rating = models.IntegerField(
        verbose_name=_("Rating"),
        choices=Range.choices,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
    )
    comment = models.TextField(verbose_name=_("Comment"), blank=True, null=True)

    class Meta:
        unique_together = [
            "rater",
            "agent",
        ]  # Ensure a user can only rate an agent once

    def __str__(self):
        return f"{self.agent} rated at {self.rating} by {self.rater}"
    
    def average_rating(self):
        return (
            self.ratings_received.aggregate(
                avg=models.Avg("rating")
            )["avg"]
            or 0
        )
