from rest_framework import serializers
from ..models.game import Game

class GameSerializer(serializers.ModelSerializer):
    num_flagged_cells = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'user', 'num_mines', 'grid_state', 'game_state', 'created_at', 'updated_at', 'num_flagged_cells']

    def get_num_flagged_cells(self, obj):
        num_flagged_cells = 0
        for row in obj.grid_state:
            for cell in row:
                if isinstance(cell, dict) and cell.get("flagged"):
                    num_flagged_cells += 1
        return num_flagged_cells
        # return sum(cell["flagged"] for row in obj.grid_state for cell in row)

    def get_revealed_cells(self, obj):
        return [
            {"x": x, "y": y, "value": cell["value"]}
            for x, row in enumerate(obj.grid_state)
            for y, cell in enumerate(row)
            if isinstance(cell, dict) and cell.get("revealed")
        ]