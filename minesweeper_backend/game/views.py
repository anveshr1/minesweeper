# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Game
# from .serializers import GameSerializer

# class GameViewSet(viewsets.ModelViewSet):
#     queryset = Game.objects.all()
#     serializer_class = GameSerializer

#     def create(self, request, *args, **kwargs):
#         user = request.data.get('user')
#         grid_size = int(request.data.get('grid_size'))
#         num_mines = int(request.data.get('num_mines'))
        
#         game = Game(user=user, grid_size=grid_size, num_mines=num_mines)
#         game.initialize_game()
        
#         serializer = self.get_serializer(game)
#         return Response(serializer.data)

#     @action(detail=True, methods=['post'])
#     def reveal_cell(self, request, pk=None):
#         game = self.get_object()
#         x = int(request.data.get('x'))
#         y = int(request.data.get('y'))
        
#         # Add logic to reveal the cell at (x, y)
#         # For example:
#         if game.grid_state[x][y]["value"] == 'M':
#             game.game_state = 'lost'
#         else:
#             game.grid_state[x][y]["revealed"] = True
        
#         game.save()
#         serializer = self.get_serializer(game)
#         return Response(serializer.data)

#     @action(detail=True, methods=['post'])
#     def flag_cell(self, request, pk=None):
#         game = self.get_object()
#         x = int(request.data.get('x'))
#         y = int(request.data.get('y'))
        
#         # Flag or unflag the cell at (x, y)
#         game.grid_state[x][y]["flagged"] = not game.grid_state[x][y]["flagged"]
        
#         game.save()
#         serializer = self.get_serializer(game)
#         return Response(serializer.data)