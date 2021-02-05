from Menu import *
from settings import get_resolution, show_window
import main_game as mg

BUTTON_BACKGROUND_COLOR = "#737373"
BUTTON_TOWERS_BACKGROUND_COLOR = "#8c8c8c"
LABEL_BACKGROUND_COLOR = '#a6a6a6'
TEXT_COLOR = "#1a1a1a"
LAYOUT_BACKGROUND_COLOR = "#cccccc"
TEXT_SIZE = 15
LABEL_INDENT = 5
LAYOUT_INDENT = (5, 5)


def resume_button():
    mg.pause = False


def pause_button():
    mg.pause = True


def settings_button():
    show_window()


def buy_button():
    mg.buy_tower()


def tower_test(*args):
    arguments = args[0]
    if arguments[1]:
        mg.picked_Tower = arguments[0]


start_mb = MenuButton(0, 0, 0, 0,
                      func=resume_button,
                      color=BUTTON_BACKGROUND_COLOR,
                      text="Начать",
                      text_color=TEXT_COLOR,
                      text_size=TEXT_SIZE)

pause_mb = MenuButton(0, 0, 0, 0,
                      func=pause_button,
                      color=BUTTON_BACKGROUND_COLOR,
                      text="Пауза",
                      text_color=TEXT_COLOR,
                      text_size=TEXT_SIZE)

settings_mb = MenuButton(0, 0, 0, 0,
                         func=settings_button,
                         color=BUTTON_BACKGROUND_COLOR,
                         text="Настройки",
                         text_color=TEXT_COLOR,
                         text_size=TEXT_SIZE)

buy_mb = MenuButton(0, 0, 0, 0,
                    func=buy_button,
                    color=BUTTON_BACKGROUND_COLOR,
                    text="Купить",
                    text_color=TEXT_COLOR,
                    text_size=TEXT_SIZE)

money_ml = MenuLabel(0, 0, 0, 0,
                     color=LABEL_BACKGROUND_COLOR,
                     text="Валюта:\nx $",
                     text_color=TEXT_COLOR,
                     text_size=TEXT_SIZE,
                     indent=LABEL_INDENT)

wave_ml = MenuLabel(0, 0, 0, 0,
                    color=LABEL_BACKGROUND_COLOR,
                    text="Волна:\n1",
                    text_color=TEXT_COLOR,
                    text_size=TEXT_SIZE,
                    indent=LABEL_INDENT)

enemies_ml = MenuLabel(0, 0, 0, 0,
                       color=LABEL_BACKGROUND_COLOR,
                       text="Враги на\nсл волне:\n5",
                       text_color=TEXT_COLOR,
                       text_size=TEXT_SIZE,
                       indent=LABEL_INDENT)

health_ml = MenuLabel(0, 0, 0, 0,
                      color=LABEL_BACKGROUND_COLOR,
                      text="ХП:\n50",
                      text_color=TEXT_COLOR,
                      text_size=TEXT_SIZE,
                      indent=LABEL_INDENT)

lb = [start_mb, pause_mb, settings_mb]
btn = MenuButtonList(lb)

ll = [money_ml, wave_ml, enemies_ml, health_ml]
lbl = MenuLabelList(ll)

place = ['l'] * len(ll) + ['b'] * len(lb)
lb2 = []

for x in range(1, 10):
    if x == 1:
        lb2.append(buy_mb)
    else:
        temp = MenuButton(0, 0, 0, 0, func=tower_test, args=[x + 8, True], color=BUTTON_TOWERS_BACKGROUND_COLOR,
                          text_color=TEXT_COLOR,
                          text=f"Башня {x - 1} | {(x - 1) * 10 - 3} $", text_size=TEXT_SIZE)
        lb2.append(temp)
pause_mbl = MenuButtonList(lb2)

w1, h1 = w, h = get_resolution()
k = 5
w, h = w // 12 - k, h // 12 - k
layout = MenuLayout(btn, lbl, place, 0, h, w, h1 - h, LAYOUT_INDENT, LAYOUT_BACKGROUND_COLOR, 'v')

layout2 = MenuLayout(pause_mbl, MenuLabelList([]), ['b' for _ in range(9)], 0, 0, w1, h, LAYOUT_INDENT,
                     LAYOUT_BACKGROUND_COLOR, 'h')
