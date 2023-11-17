from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    cover_url = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, id: {self.id}'
    
class Review(models.Model):
    SCORE_CHOICES = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five')
    ]
    score = models.IntegerField(
        default=5, 
        choices=SCORE_CHOICES
        )
    review = models.TextField()
    date_submitted = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'review id: {self.id}'