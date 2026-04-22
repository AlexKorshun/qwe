SCREEN_TITLE = "Prachka"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
CELL_WIDTH = 60
CELL_HEIGHT = 60
ROW_COUNT = 11
COLUMN_COUNT = 11
PLAYER_SPEED = 20

LEVEL_TIME_SECONDS = 60.0
MAX_HEARTS = 10
METEORITES_PER_HEART = 50
START_HEARTS = 3


def justify_x(position_x, cell_width, column_count):
    for x in range(column_count):
        cell_center_x = difference(x, cell_width)
        if position_x - cell_center_x <= cell_width / 2:
            return cell_center_x


def justify_y(position_y, cell_height, row_count):
    for y in range(row_count):
        cell_center_y = difference(y, cell_height)
        if position_y - cell_center_y <= cell_height / 2:
            return cell_center_y


def difference(coordinate, distance):
    return coordinate * distance + distance / 2
