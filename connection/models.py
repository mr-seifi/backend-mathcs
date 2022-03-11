from django.db import models
from account.models import User, Group


class JoinRequest(models.Model):
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='join_request')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             related_name='join_request')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date', )


class ConnectionRequest(models.Model):

    source_group = models.ForeignKey(Group,
                                     on_delete=models.CASCADE,
                                     related_name='sent_request')
    dest_group = models.ForeignKey(Group,
                                   on_delete=models.CASCADE,
                                   related_name='received_request')
    sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-sent', )
