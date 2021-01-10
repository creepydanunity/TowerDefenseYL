from Menu import *
from settings import get_resolution

BUTTON_BACKGROUND_COLOR = "#737373"
BUTTON_TOWERS_BACKGROUND_COLOR = "#8c8c8c"
LABEL_BACKGROUND_COLOR = '#a6a6a6'
TEXT_COLOR = "#1a1a1a"
LAYOUT_BACKGROUND_COLOR = "#cccccc"
TEXT_SIZE = 15
LABEL_INDENT = 5
LAYOUT_INDENT = (5, 5)


def print_1():
    pass


def print_2():
    pass


def print_3():
    print(3)


def print_4():
    print(4)


btn1 = MenuButton(0, 0, 0, 0, func=print_1, color=BUTTON_BACKGROUND_COLOR, text="Начать", text_color=TEXT_COLOR,
                  text_size=TEXT_SIZE)
btn2 = MenuButton(0, 0, 0, 0, func=print_2, color=BUTTON_BACKGROUND_COLOR, text="Пауза", text_color=TEXT_COLOR,
                  text_size=TEXT_SIZE)
btn3 = MenuButton(0, 0, 0, 0, func=print_3, color=BUTTON_BACKGROUND_COLOR, text="Настройки", text_color=TEXT_COLOR,
                  text_size=TEXT_SIZE)
btn4 = MenuButton(0, 0, 0, 0, func=print_4, color=BUTTON_BACKGROUND_COLOR, text="Выйти", text_color=TEXT_COLOR,
                  text_size=TEXT_SIZE)
btn5 = MenuButton(0, 0, 0, 0, color=BUTTON_BACKGROUND_COLOR, text="Купить", text_color=TEXT_COLOR, text_size=TEXT_SIZE)
lbl1 = MenuLabel(0, 0, 0, 0, color=LABEL_BACKGROUND_COLOR, text="Валюта:\nx $", text_color=TEXT_COLOR,
                 text_size=TEXT_SIZE,
                 indent=LABEL_INDENT)
lbl2 = MenuLabel(0, 0, 0, 0, color=LABEL_BACKGROUND_COLOR, text="Волна:\nx / 25", text_color=TEXT_COLOR,
                 text_size=TEXT_SIZE,
                 indent=LABEL_INDENT)
lbl3 = MenuLabel(0, 0, 0, 0, color=LABEL_BACKGROUND_COLOR, text="Враги на\nсл волне:\n0", text_color=TEXT_COLOR,
                 text_size=TEXT_SIZE,
                 indent=LABEL_INDENT)
lbl4 = MenuLabel(0, 0, 0, 0, color=LABEL_BACKGROUND_COLOR, text="ХП:\n50 %", text_color=TEXT_COLOR, text_size=TEXT_SIZE,
                 indent=LABEL_INDENT)
lb = []
for x in range(1, 4):
    eval(f'lb.append(btn{x})')
btn = MenuButtonList(lb)

ll = []
for x in range(1, 5):
    eval(f'll.append(lbl{x})')
lbl = MenuLabelList(ll)

place = []
for _ in range(len(ll)):
    place.append('l')
for x in range(len(lb)):
    place.append("b")

place2 = ['b' for _ in range(9)]
lb2 = []
for x in range(1, 10):
    if x == 1:
        lb2.append(btn5)
    elif x == 2:
        lb2.append(
            MenuButton(0, 0, 0, 0, color=BUTTON_BACKGROUND_COLOR, text="<", text_color=TEXT_COLOR, text_size=50)
        )
    elif x == 9:
        lb2.append(
            MenuButton(0, 0, 0, 0, color=BUTTON_BACKGROUND_COLOR, text=">", text_color=TEXT_COLOR, text_size=50)
        )
    else:
        lb2.append(
            MenuButton(0, 0, 0, 0, color=BUTTON_TOWERS_BACKGROUND_COLOR, text_color=TEXT_COLOR,
                       text=f"Башня {x - 2} | {(x - 2) * 10 - 3} $", text_size=TEXT_SIZE))
btn2l = MenuButtonList(lb2)

w, h = get_resolution()
k = 5
w, h = w // 12 - k, h // 12 - k
layout = MenuLayOut(btn, lbl, place, 0, h, w, 600 - h, LAYOUT_INDENT, LAYOUT_BACKGROUND_COLOR, 'v')

layout2 = MenuLayOut(btn2l, MenuLabelList([]), place2, 0, 0, 800, h, LAYOUT_INDENT, LAYOUT_BACKGROUND_COLOR, 'h')
