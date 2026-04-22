import arcade


class OneTimeBlock(arcade.Sprite):
    def __init__(self, scale):
        super().__init__('resources/Blocks/SolidBlock.png', scale)
        self.explodable = False
        self.one_time = True
        # Light warm tint to visually separate from regular walls.
        self.color = (255, 210, 120)
