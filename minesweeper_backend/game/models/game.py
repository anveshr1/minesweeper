from collections import deque
import random
from django.db import models

class Game(models.Model):
    user = models.CharField(max_length=100)
    grid_size = models.IntegerField()
    num_mines = models.IntegerField()
    grid_state = models.JSONField()
    game_state = models.CharField(max_length=10, default='active')  # active, won, lost => make enum
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def initialize_game(self):
        self._initialize_grid()
        self._place_mines()
        self._calculate_adjacent_mines()
        self.game_state = 'active'
        self.save()

    def _initialize_grid(self):
        self.grid_state = [[{"value": 0, "revealed": False, "flagged": False, "adjacent_mines": 0} for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def _place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.grid_state[x][y]["value"] != 'M':
                self.grid_state[x][y]["value"] = 'M'
                mines_placed += 1

    def _calculate_adjacent_mines(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid_state[x][y]["value"] != 'M':
                    self.grid_state[x][y]["adjacent_mines"] = self._count_adjacent_mines(x, y)

    def _count_adjacent_mines(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                if self.grid_state[nx][ny]["value"] == 'M':
                    count += 1
        return count

    def reveal_cells(self, x, y):
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return
        if self.grid_state[x][y]["revealed"]:
            return

        queue = deque([(x, y)])
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        while queue:
            cx, cy = queue.popleft()
            if not (0 <= cx < self.grid_size and 0 <= cy < self.grid_size):
                continue
            if self.grid_state[cx][cy]["revealed"]:
                continue

            adjacent_mines = self.grid_state[cx][cy]["adjacent_mines"]
            self.grid_state[cx][cy]["revealed"] = True

            if adjacent_mines == 0:
                for dx, dy in directions:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and not self.grid_state[nx][ny]["revealed"]:
                        queue.append((nx, ny))

    def check_win_condition(self):
        for row in self.grid_state:
            for cell in row:
                if cell["value"] != 'M' and not cell["revealed"]:
                    return False
        return True