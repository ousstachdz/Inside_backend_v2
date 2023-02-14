from django.db import models


class Conversation(models.Model):
    owner = models.ForeignKey(
        "user.UserApp", on_delete=models.CASCADE, related_name='+', null=True)
    with_user = models.ForeignKey("user.UserApp", on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Of {self.owner} and {self.with_user}'


class Message(models.Model):
    owner = models.ForeignKey("user.UserApp", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Sent by {self.owner}'
