from constants import SHAPES, SHAPE_COLORS, GRID_WIDTH


class Tetromino:
    def __init__(self, x, y, shape_idx):
        self.x = x
        self.y = y
        self.shape_idx = shape_idx
        self.rotation = 0
        self.color = SHAPE_COLORS[shape_idx]
        self.shape = SHAPES[shape_idx][self.rotation]

    def rotate(self):
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % 4
        self.shape = SHAPES[self.shape_idx][self.rotation]

        if self.x + len(self.shape[0]) > GRID_WIDTH:
            self.x = GRID_WIDTH - len(self.shape[0])

        return old_rotation