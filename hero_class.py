import arcade
import animate
import explodableBlock
from constants import *


class Hero(animate.Animate):
    def _try_consume_one_time_block(self, next_direction):
        pending = self.window.pending_one_time_block
        if pending is None:
            return
        hit_direction = getattr(self.window, "pending_one_time_hit_direction", None)
        # One-time block disappears after changing direction away from hit direction.
        # If hit direction is unexpectedly missing, consume to avoid stuck pending state.
        if hit_direction is None or next_direction != hit_direction:
            pending.kill()
            self.window.pending_one_time_block = None
            self.window.pending_one_time_hit_direction = None

    def change_scale(self, scale):
        self.scale = scale * 0.5

    def __init__(self, speed, window):
        super().__init__("resources/Bomberman/Front/Bman_F_f00.png", 0.5 * window.scale_of_map)
        self.walk_down_frames = []
        self.walk_up_frames = []
        self.walk_right_frames = []
        self.walk_left_frames = []
        self.stand_down_frames = []
        self.stand_up_frames = []
        self.stand_right_frames = []
        self.stand_left_frames = []
        for i in range(8):
            self.walk_down_frames.append(arcade.load_texture(f"resources/Bomberman/Front/Bman_F_f0{i}.png"))
            self.walk_up_frames.append(arcade.load_texture(f"resources/Bomberman/Back/Bman_B_f0{i}.png"))
            side_texture = arcade.load_texture(f"resources/Bomberman/Side/Bman_S_f0{i}.png")
            self.walk_right_frames.append(side_texture)
            # Arcade 3 removed flipped_horizontally in load_texture, reuse side texture for left walk.
            self.walk_left_frames.append(side_texture)
            self.stand_down_frames.append(arcade.load_texture(f"resources/Bomberman/Front/Bman_F_f0{0}.png"))
        self.direction = 4
        self.motion = 0
        self.speed = speed
        self.window = window
        self.delay_direction = 0
        self.time_left = 0
        self.won = False

    def costume_change(self):
        if self.direction == 1:
            self.textures = self.walk_left_frames
        elif self.direction == 2:
            self.textures = self.walk_right_frames
        elif self.direction == 3:
            self.textures = self.walk_up_frames
        elif self.direction == 4:
            self.textures = self.walk_down_frames

    def update(self):
        if self.window.game:
            self.time_left -= 0.15
            if self.time_left < 0:
                self.time_left = 0
            if self.time_left > 0:
                self.costume_change()
                if self.delay_direction == 1:
                    self.to_left()
                elif self.delay_direction == 2:
                    self.to_right()
                elif self.delay_direction == 3:
                    self.to_up()
                elif self.delay_direction == 4:
                    self.to_down()
            self.center_x += self.change_x
            self.center_y += self.change_y
            if self.left < 0 and self.direction == 1 or self.right > SCREEN_WIDTH and self.direction == 2 or self.bottom < 0 and self.direction == 4 or self.top > SCREEN_HEIGHT and self.direction == 3:
                self.window.game = False
                self.window.timer = 1
            self.collisions(self.window.solid_blocks)
            self.collisions(self.window.explodable_blocks)
            if arcade.check_for_collision(self, self.window.finishSprite):
                self.window.timer = 2
                self.won = True
                self.window.game = False

    def to_up(self):
        if not self.motion:
            self._try_consume_one_time_block(3)
            self.motion = 1
            self.direction = 3
            self.change_y = self.speed
        elif self.time_left == 0:
            self.delay_direction = 3
            self.time_left = 1

    def to_down(self):
        if not self.motion:
            self._try_consume_one_time_block(4)
            self.motion = 1
            self.direction = 4
            self.change_y = -self.speed
        elif self.time_left == 0:
            self.delay_direction = 4
            self.time_left = 1

    def to_left(self):
        if not self.motion:
            self._try_consume_one_time_block(1)
            self.motion = 1
            self.direction = 1
            self.change_x = -self.speed
        elif self.time_left == 0:
            self.delay_direction = 1
            self.time_left = 1

    def to_right(self):
        if not self.motion:
            self._try_consume_one_time_block(2)
            self.motion = 1
            self.direction = 2
            self.change_x = self.speed
        elif self.time_left == 0:
            self.delay_direction = 2
            self.time_left = 1

    def to_stop(self):
        self.change_x = 0
        self.change_y = 0
        self.motion = 0
        self.textures = self.stand_down_frames

    def collisions(self, spritelist):
        block_hit = arcade.check_for_collision_with_list(self, spritelist)
        if len(block_hit) > 0:
            for block in block_hit:
                if block.explodable == False:
                    arcade.play_sound(self.window.blockSound, volume=0.1)
                    if self.direction == 3 and self.top > block.bottom:
                        self.top = block.bottom
                    elif self.direction == 4 and self.bottom < block.top:
                        self.bottom = block.top
                    elif self.direction == 2 and self.right > block.left:
                        self.right = block.left
                    elif self.direction == 1 and self.left < block.right:
                        self.left = block.right
                    self.to_stop()
                    self.center_y = justify_y(self.center_y, self.window.cell_height, self.window.row_count)
                    self.center_x = justify_x(self.center_x, self.window.cell_width, self.window.column_count)
                    if getattr(block, "one_time", False):
                        self.window.pending_one_time_block = block
                        self.window.pending_one_time_hit_direction = self.direction
                else:
                    block.kill()
                    self.window.current_score += 1
                    if isinstance(block, explodableBlock.ExplodableBlock):
                        self.window.on_meteorite_destroyed()
                    arcade.play_sound(self.window.coinSound, volume=0.1)
