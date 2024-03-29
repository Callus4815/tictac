from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from tictactoe.models import Game
# Create your views here.

@login_required
def home(request):
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.filter(status="A")
    finsihed_games = my_games.exclude(status="A")
    waiting_games = active_games.filter(next_to_move=request.user)
    other_games = active_games.exclude(next_to_move=request.user)
    invitations = request.user.invitations_received.all()
    context = {'other_games': other_games,
                'waiting_games': waiting_games,
                'finsihed_games': finsihed_games,
                'invitations': invitations}
    return render(request, "users/home.html", context)
