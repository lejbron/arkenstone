from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Match


@receiver(post_save, sender=Match)
def save_match(sender, instance, **kwargs):
    if instance.opp1_gp is not None and instance.opp2_gp is not None:
        instance.opp1.update_player_stats()
        instance.opp2.update_player_stats()
