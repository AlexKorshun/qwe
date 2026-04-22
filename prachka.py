import os
import sys
import arcade
import random
import all_maps
import hero_class
import explodableBlock
import solidBlock
import oneTimeBlock
from all_maps import maps
import finishClass
from constants import *
import arcade.gui as gui

records = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


def readingRecords():
    global records
    with open("resources/records.txt", encoding="utf-8") as file:
        records.clear()
        for i in file:
            records.append(i)


def draw_texture_center(texture, center_x, center_y, width, height):
    arcade.draw_texture_rect(
        texture,
        arcade.LBWH(center_x - width / 2, center_y - height / 2, width, height),
    )


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class Game(arcade.Window):
    def _reset_level_cycle(self):
        self.level_cycle_modes = []
        self.level_cycle_index = 0

    def _next_level_mode(self):
        if self.level_cycle_index >= len(self.level_cycle_modes):
            self.level_cycle_modes = ["normal", "alpha", "beta", "gamma"]
            random.shuffle(self.level_cycle_modes)
            self.level_cycle_index = 0
        mode = self.level_cycle_modes[self.level_cycle_index]
        self.level_cycle_index += 1
        return mode

    def generate_level_map(self):
        # Every 4 levels: one normal + alpha + beta + gamma in random order.
        self.current_level_mode = self._next_level_mode()
        self.force_one_time_each_level = self.current_level_mode != "normal"

        if self.current_level_mode == "normal":
            self.engine = all_maps.Engine()
            self.engine.generateTheWay()
            all_maps.maps[0] = self.engine.map
            return

        all_maps.ACTIVE_ONE_TIME_TEMPLATE = self.current_level_mode
        while True:
            self.engine = all_maps.Engine()
            self.engine.generateTheWay()
            special_map = all_maps.generate_one_time_map(self.engine.map)
            if special_map is not None:
                all_maps.maps[0] = special_map
                return

    def __init__(self, width, height, title):
        self.inputer = False
        self.name_input = ""
        self.quit_button_rect = arcade.LBWH(SCREEN_WIDTH / 2 - 180, SCREEN_HEIGHT / 2 - 165, 160, 50)
        self.save_button_rect = arcade.LBWH(SCREEN_WIDTH / 2 + 20, SCREEN_HEIGHT / 2 - 165, 160, 50)
        self.start_button_rect = arcade.LBWH(SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 20, 240, 60)
        self.menu_exit_button_rect = arcade.LBWH(SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 100, 240, 60)
        super().__init__(width, height, title, fullscreen=False, center_window=True)
        arcade.play_sound(arcade.load_sound('resources/videoplayback.m4a'), volume=0.1, loop=True)
        self.coinSound = arcade.load_sound('resources/smw_coin.wav')
        self.blockSound = arcade.load_sound('resources/smw_jump.wav')
        self.deadSound = arcade.load_sound('resources/smw_blargg.wav')
        self.finishSound = arcade.load_sound('resources/smw_cape_rise.wav')
        self.background_texture = arcade.load_texture("resources/background.png")
        self.win_texture = arcade.load_texture("resources/win/win.png")
        self.lose_texture = arcade.load_texture("resources/win/lose.png")
        self.heart_texture = arcade.load_texture("resources/heart.png")
        self.manager = gui.UIManager()
        self.hp = START_HEARTS
        self.name = "Player"
        self.real_game = True
        self.score = 0
        self.current_score = 0
        self.level_time_left = LEVEL_TIME_SECONDS
        self.meteorites_destroyed = 0
        self.meteorites_this_level = 0
        self.scale_of_map = 1
        self.column_count = COLUMN_COUNT
        self.row_count = ROW_COUNT
        self.indent = 0
        self.solid_blocks = arcade.SpriteList()
        self.explodable_blocks = arcade.SpriteList()
        self.hero = hero_class.Hero(PLAYER_SPEED, self)
        self.game = True
        self.delay_moment = 0
        self.timer = 0
        self.end_game = False
        self.pending_one_time_block = None
        self.pending_one_time_hit_direction = None
        self.level_cycle_modes = []
        self.level_cycle_index = 0
        self.current_level_mode = "normal"
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        self.current_map = 0
        self.level_number = 1
        self._reset_level_cycle()
        self.generate_level_map()
        for i in all_maps.maps[0]:
            print(i)
        self.setup()
        self.in_menu = True

    def start_from_menu(self):
        self.in_menu = False

    def on_meteorite_destroyed(self):
        self.meteorites_this_level += 1

    def confirm_meteorites_for_cleared_level(self):
        """Подтверждённые при прохождении уровня метеориты — в общий счёт и бонусные сердца."""
        old = self.meteorites_destroyed
        self.meteorites_destroyed += self.meteorites_this_level
        self.meteorites_this_level = 0
        crossed = (self.meteorites_destroyed // METEORITES_PER_HEART) - (old // METEORITES_PER_HEART)
        if crossed > 0:
            self.hp = min(self.hp + crossed, MAX_HEARTS)

    @staticmethod
    def _format_level_time(seconds: float) -> str:
        s = max(0, int(seconds + 0.5))
        m, sec = s // 60, s % 60
        return f"{m:01d}:{sec:02d}"

    def setup(self, preserve_level_timer=False):
        if self.game and self.real_game:
            self.finishPlay = True
            self.current_score = 0
            if not preserve_level_timer:
                self.level_time_left = LEVEL_TIME_SECONDS
            self.pending_one_time_block = None
            self.pending_one_time_hit_direction = None
            self.hero.won = False
            user_x = 0
            user_y = 0
            self.scale_of_map = 13.36 / (len(all_maps.maps[self.current_map][0]))
            self.row_count = len(all_maps.maps[self.current_map])
            self.column_count = len(all_maps.maps[self.current_map][0])
            self.cell_width = CELL_WIDTH * self.scale_of_map
            self.cell_height = CELL_HEIGHT * self.scale_of_map
            self.hero.change_scale(self.scale_of_map)
            for y in range(self.row_count):
                for x in range(self.column_count):
                    if maps[self.current_map][self.row_count - y - 1][x] == 6:
                        user_x = x
                        user_y = y
                    elif maps[self.current_map][self.row_count - y - 1][x] == 7:
                        self.finishSprite = finishClass.FnishBlock(self.scale_of_map)
                        self.finishSprite.center_x = justify_x(
                            difference(x, self.cell_width), self.cell_width, self.column_count
                        )
                        self.finishSprite.center_y = justify_y(
                            difference(y, self.cell_height), self.cell_height, self.row_count
                        )
                    elif maps[self.current_map][self.row_count - y - 1][x] == 1:
                        wall_block = solidBlock.SolidBlock(self.scale_of_map)
                        wall_block.center_x = difference(x, self.cell_width)
                        wall_block.center_y = difference(y, self.cell_height)
                        self.solid_blocks.append(wall_block)
                    elif maps[self.current_map][self.row_count - y - 1][x] == 8:
                        wall_block = oneTimeBlock.OneTimeBlock(self.scale_of_map)
                        wall_block.center_x = difference(x, self.cell_width)
                        wall_block.center_y = difference(y, self.cell_height)
                        self.solid_blocks.append(wall_block)
                    elif random.randint(1, 3) == 1:
                        exp_block = explodableBlock.ExplodableBlock(self.scale_of_map)
                        exp_block.center_x = difference(x, self.cell_width)
                        exp_block.center_y = difference(y, self.cell_height)
                        self.explodable_blocks.append(exp_block)
            x = justify_x(difference(user_x, self.cell_width), self.cell_width, self.column_count)
            y = justify_y(difference(user_y, self.cell_height), self.cell_height, self.row_count)
            self.hero.center_x = x
            self.hero.center_y = y

    def on_draw(self):
        self.clear()
        if self.in_menu:
            draw_texture_center(self.background_texture, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            arcade.draw_rect_filled(
                arcade.LBWH(SCREEN_WIDTH / 2 - 220, SCREEN_HEIGHT / 2 - 170, 440, 260),
                arcade.color.DARK_BLUE_GRAY
            )
            arcade.draw_text(
                "AstroSlide",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 + 105,
                arcade.color.WHITE,
                font_size=44,
                anchor_x="center",
            )
            arcade.draw_rect_filled(self.start_button_rect, arcade.color.DARK_MIDNIGHT_BLUE)
            arcade.draw_rect_outline(self.start_button_rect, arcade.color.WHITE, 2)
            arcade.draw_text(
                "Старт",
                SCREEN_WIDTH / 2,
                self.start_button_rect.bottom + 18,
                arcade.color.WHITE,
                font_size=28,
                anchor_x="center",
            )
            arcade.draw_rect_filled(self.menu_exit_button_rect, arcade.color.DARK_MIDNIGHT_BLUE)
            arcade.draw_rect_outline(self.menu_exit_button_rect, arcade.color.WHITE, 2)
            arcade.draw_text(
                "Выход",
                SCREEN_WIDTH / 2,
                self.menu_exit_button_rect.bottom + 18,
                arcade.color.WHITE,
                font_size=28,
                anchor_x="center",
            )
            return
        if self.game:
            draw_texture_center(self.background_texture, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.solid_blocks.draw()
            self.explodable_blocks.draw()
            arcade.draw_sprite(self.hero)
            arcade.draw_sprite(self.finishSprite)
        else:
            if self.hero.won:
                if self.timer <= 0:
                    self.game = True
                    self.timer = 0
                    self.explodable_blocks.clear()
                    self.solid_blocks.clear()
                    self.level_number += 1
                    self.generate_level_map()
                    self.score += self.current_score
                    self.confirm_meteorites_for_cleared_level()
                    self.setup(preserve_level_timer=True)
                    self.hero.to_stop()
                else:
                    self.timer -= 0.1
                    if self.finishPlay:
                        arcade.play_sound(self.finishSound, volume=0.4)
                        self.finishPlay = False
                    draw_texture_center(self.win_texture, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
            else:
                if self.real_game:
                    draw_texture_center(self.lose_texture, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
                    arcade.play_sound(self.deadSound, volume=0.2)
                else:
                    draw_texture_center(self.lose_texture, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
                    arcade.draw_rect_filled(
                        arcade.LBWH(SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 225, 500, 450),
                        arcade.color.DARK_BLUE_GRAY
                    )
                    arcade.draw_text(
                        "Enter your name",
                        SCREEN_WIDTH / 2 - 170,
                        SCREEN_HEIGHT / 2 + 120,
                        arcade.color.DARK_RED,
                        font_size=30
                    )
                    arcade.draw_rect_filled(
                        arcade.LBWH(SCREEN_WIDTH / 2 - 190, SCREEN_HEIGHT / 2 - 20, 380, 50),
                        arcade.color.DARK_MIDNIGHT_BLUE
                    )
                    arcade.draw_text(
                        self.name_input if self.name_input else "_",
                        SCREEN_WIDTH / 2 - 175,
                        SCREEN_HEIGHT / 2 - 5,
                        arcade.color.WHITE,
                        font_size=24
                    )
                    arcade.draw_rect_filled(self.quit_button_rect, arcade.color.DARK_BLUE_GRAY)
                    arcade.draw_rect_outline(self.quit_button_rect, arcade.color.WHITE, 2)
                    arcade.draw_rect_filled(self.save_button_rect, arcade.color.DARK_BLUE_GRAY)
                    arcade.draw_rect_outline(self.save_button_rect, arcade.color.WHITE, 2)
                    arcade.draw_text("Quit", self.quit_button_rect.left + 50, self.quit_button_rect.bottom + 14,
                                     arcade.color.WHITE, 20)
                    arcade.draw_text("Save", self.save_button_rect.left + 50, self.save_button_rect.bottom + 14,
                                     arcade.color.WHITE, 20)
                readingRecords()
                for i in range(1, 11):
                    arcade.draw_text(records[10 - i], SCREEN_WIDTH * 9 / 11, SCREEN_HEIGHT / 3 + i * 20,
                                     color=(255, 255, 255))
            if self.end_game:
                draw_texture_center(self.win_texture, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        if self.game:
            arcade.draw_text(
                self._format_level_time(self.level_time_left),
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT - 8,
                arcade.color.WHITE,
                font_size=26,
                anchor_x="center",
                anchor_y="top",
            )
        fs = 24 - int(self.score // 100 != 0) * 8
        arcade.draw_text(str(self.score), 30, SCREEN_HEIGHT - 52, color=arcade.color.RED_ORANGE, font_size=fs)
        arcade.draw_text(
            "(+" + str(self.current_score) + ")",
            70,
            SCREEN_HEIGHT - 52,
            color=arcade.color.BLUE_GREEN,
            font_size=fs,
        )
        heart_w = min(44, max(28, (SCREEN_WIDTH - 220) // max(self.hp, 1)))
        margin_r = 20
        for i in range(self.hp):
            cx = SCREEN_WIDTH - margin_r - heart_w / 2 - i * (heart_w + 4)
            draw_texture_center(self.heart_texture, cx, SCREEN_HEIGHT - 46, heart_w, heart_w)
        self.manager.draw()

    def on_update(self, delta_time):
        if self.in_menu:
            return
        if self.game:
            self.level_time_left -= delta_time
            if self.level_time_left <= 0:
                self.level_time_left = LEVEL_TIME_SECONDS
                self.hp = max(0, self.hp - 1)
            self.hero.update_animation(delta_time)
            self.hero.update()
        elif not self.hero.won:
            if self.timer <= 0:
                self.game = True
                self.timer = 0
                self.hp = max(0, self.hp - 1)
                self.meteorites_this_level = 0
                self.explodable_blocks.clear()
                self.solid_blocks.clear()
                self.setup()
                self.hero.to_stop()
            else:
                self.timer -= 0.1
        if self.hp <= 0:
            self.real_game = False
            self.game = False
            if not self.inputer:
                self.name_input = ""
                self.inputer = True

    def update_text(self):
        clean_name = self.name_input.strip()
        if clean_name:
            self.name = clean_name

    def on_click(self, event):
        print(f"click-event caught: {event}")
        self.update_text()
        with open('resources/records.txt', 'w'):
            pass
        with open('resources/records.txt', 'a', encoding='utf-8') as file:
            k = 0
            change = False
            lastString = ''
            for i in records:
                fullString = ''
                k += 1
                if change and k <= 10:
                    fullString = lastString
                    lastString = i
                else:
                    j = 0
                    while (i[j] != ':'):
                        fullString += i[j]
                        j += 1
                    j += 1
                    fullString += ':'
                    bufer = ''
                    while (k <= 10 and j != len(i) - 1):
                        bufer += i[j]
                        j += 1
                    fullString += bufer + '\n'
                    bufer = int(bufer)
                    if bufer < self.score:
                        change = True
                        fullString = self.name + ":" + str(int(self.score)) + '\n'
                        lastString = i
                file.write(fullString)
            self.restart()

    def restart(self):
        self.inputer = False
        self.name_input = ""
        self.manager = gui.UIManager()
        self.hp = START_HEARTS
        self.name = "Player"
        self.real_game = True
        self.score = 0
        self.current_score = 0
        self.level_time_left = LEVEL_TIME_SECONDS
        self.meteorites_destroyed = 0
        self.meteorites_this_level = 0
        self.scale_of_map = 1
        self.column_count = COLUMN_COUNT
        self.row_count = ROW_COUNT
        self.indent = 0
        self.solid_blocks = arcade.SpriteList()
        self.explodable_blocks = arcade.SpriteList()
        self.hero = hero_class.Hero(PLAYER_SPEED, self)
        self.game = True
        self.delay_moment = 0
        self.timer = 0
        self.end_game = False
        self.pending_one_time_block = None
        self.pending_one_time_hit_direction = None
        self.level_cycle_modes = []
        self.level_cycle_index = 0
        self.current_level_mode = "normal"
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        self.current_map = 0
        self.level_number = 1
        self._reset_level_cycle()
        self.generate_level_map()
        for i in all_maps.maps[0]:
            print(i)
        self.setup()

    def on_key_press(self, key, modifiers):
        if self.in_menu:
            if key in (arcade.key.ENTER, arcade.key.SPACE):
                self.start_from_menu()
                return
            if key == arcade.key.ESCAPE:
                arcade.close_window()
                return
        if self.inputer:
            if key == arcade.key.BACKSPACE:
                self.name_input = self.name_input[:-1]
                return
            if key in (arcade.key.ENTER, arcade.key.NUM_ENTER):
                self.on_click(None)
                return
        if key == arcade.key.H:
            self.restart()
        if self.game:
            if key == arcade.key.R:
                self.meteorites_this_level = 0
                self.setup()
            if key == arcade.key.LEFT:
                self.hero.to_left()
            elif key == arcade.key.RIGHT:
                self.hero.to_right()
            elif key == arcade.key.UP:
                self.hero.to_up()
            elif key == arcade.key.DOWN:
                self.hero.to_down()
            self.hero.costume_change()
        if key == arcade.key.ESCAPE or key == arcade.key.F11:
            arcade.close_window()

    def on_text(self, text):
        if self.inputer and text and text.isprintable():
            self.name_input += text
            return
        return super().on_text(text)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.in_menu:
            if self.start_button_rect.left <= x <= self.start_button_rect.right and \
                    self.start_button_rect.bottom <= y <= self.start_button_rect.top:
                self.start_from_menu()
                return
            if self.menu_exit_button_rect.left <= x <= self.menu_exit_button_rect.right and \
                    self.menu_exit_button_rect.bottom <= y <= self.menu_exit_button_rect.top:
                arcade.close_window()
                return
            return super().on_mouse_press(x, y, button, modifiers)
        if not self.inputer:
            return super().on_mouse_press(x, y, button, modifiers)
        if self.save_button_rect.left <= x <= self.save_button_rect.right and \
                self.save_button_rect.bottom <= y <= self.save_button_rect.top:
            self.on_click(None)
            return
        if self.quit_button_rect.left <= x <= self.quit_button_rect.right and \
                self.quit_button_rect.bottom <= y <= self.quit_button_rect.top:
            arcade.close_window()
            return
        return super().on_mouse_press(x, y, button, modifiers)


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
