from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.game import Game
from ..serializers.game import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        grid_size = int(request.data.get('grid_size'))
        num_mines = int(request.data.get('num_mines'))
        if grid_size < 1:
            return Response({"error": "Grid size must be at least 1"}, status=400)
        if num_mines < 1:
            return Response({"error": "Place atleast one mine"}, status=400)
        if num_mines >= grid_size * grid_size:
            return Response({"error": "Number of mines cannot be greater than or equal to the number of cells"}, status=400)
        game = Game(user=user, grid_size=grid_size, num_mines=num_mines)
        game.initialize_game()
        
        serializer = self.get_serializer(game)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reveal_cell(self, request, pk=None):
        game = self.get_object()
        if game.game_state != 'active':
            return Response({"error": "Game is not active"}, status=400)

        x = int(request.data.get('x'))
        y = int(request.data.get('y'))
        
        if not (0 <= x < game.grid_size and 0 <= y < game.grid_size):
            return Response({"error": "Invalid coordinates"}, status=400)

        if game.grid_state[x][y]["value"] == 'M':
            game.game_state = 'lost'
            for row in game.grid_state:
                for cell in row:
                    if cell["value"] == 'M':
                        cell["revealed"] = True
        else:
            game.reveal_cells(x, y)
            if game.check_win_condition():
                game.game_state = 'won'
        
        game.save()
        serializer = self.get_serializer(game)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def flag_cell(self, request, pk=None):
        game = self.get_object()
        if game.game_state != 'active':
            return Response({"error": "Game is not active"}, status=400)

        x = int(request.data.get('x'))
        y = int(request.data.get('y'))
        
        if not (0 <= x < game.grid_size and 0 <= y < game.grid_size):
            return Response({"error": "Invalid coordinates"}, status=400)
    
        game.grid_state[x][y]["flagged"] = not game.grid_state[x][y]["flagged"]
        
        flagged_cells = sum(cell["flagged"] for row in game.grid_state for cell in row)
        if flagged_cells == game.num_mines:
            all_mines_flagged = all(
                cell["flagged"] == (cell["value"] == 'M')
                for row in game.grid_state
                for cell in row
            )
            if all_mines_flagged:
                game.game_state = 'won'
            else:
                game.game_state = 'lost'
                for row in game.grid_state:
                    for cell in row:
                        if cell["value"] == 'M':
                            cell["revealed"] = True

        game.save()
        serializer = self.get_serializer(game)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reset_game(self, request, pk=None):
        game = self.get_object()
        game.initialize_game()
        game.save()
        serializer = self.get_serializer(game)
        return Response(serializer.data)