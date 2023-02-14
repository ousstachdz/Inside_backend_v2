from django.db import models


class RequestFriendShip(models.Model):
    from_user = models.ForeignKey(
        "user.UserApp", on_delete=models.CASCADE, related_name='+')
    to_user = models.ForeignKey("user.UserApp", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'From {self.from_user} to {self.to_user}'
