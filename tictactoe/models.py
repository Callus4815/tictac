from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.urlresolvers import reverse

from django.db import models

# Create your models here.
GAME_STATUS_CHOICES = (
    ('A', 'Active'),
    ('F', 'First Player Wins'),
    ('S', 'Second Player Wins'),
    ('D', 'Draw')
)

FIRST_PLAYER_MOVE = 'X'
SECOND_PLAYER_MOVE = 'O'
BOARD_SIZE = 3


class GamesManager(models.Manager):

    def games_for_user(self, user):
        return super(GamesManager, self).get_queryset().filter(
            Q(first_player_id=user.id) | Q(second_player_id=user.id))

    def new_game(self, invitation):
        game = Game(first_player=invitation.to_user,
                    second_player=invitation.from_user,
                    next_to_move=invitation.to_user)
        return game


class Game(models.Model):
    first_player = models.ForeignKey(User, related_name='games_first_player')
    second_player = models.ForeignKey(User, related_name='games_second_player')
    next_to_move = models.ForeignKey(User, related_name='games_to_move')
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, default='A',
                            choices=GAME_STATUS_CHOICES)

    objects = GamesManager()

    def as_board(self):
        board = [['' for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for move in self.move_set.all():
            board[move.y][move.x] = FIRST_PLAYER_MOVE if move.by_first_player else SECOND_PLAYER_MOVE
        return board

    def last_move(self):
        return self.move_set.latest()

    def get_absolute_url(self):
        return reverse('tictactoe_game_detail', args=[self.id])

    def __str__(self):
        return "{} vs {}".format(self.first_player, self.second_player)


class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=255)
    game = models.ForeignKey(Game)
    by_first_player = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'

    def player(self):
        return self.game.first_player if self.by_first_player else self.game.second_player

class Invitation(models.Model):
    from_user = models.ForeignKey(User, related_name="invitations_sent")
    to_user = models.ForeignKey(User, related_name="invitations_received",
                                verbose_name="User to Invite")
    message = models.CharField("Optional Message", max_length=300, blank=True,
                                help_text="Add a message if you would like...")
    timestamp = models.DateTimeField(auto_now_add=True)
