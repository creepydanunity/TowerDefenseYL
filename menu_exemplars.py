from Menu import *

BUTTON_BACKGROUND_COLOR = "#737373"
LABEL_BACKGROUND_COLOR = '#a6a6a6'
TEXT_COLOR = "#1a1a1a"
LAYOUT_BACKGROUND_COLOR = "#cccccc"
TEXT_SIZE = 15
LABEL_INDENT = 5
LAYOUT_INDENT = (5, 5)


def print_1():
    lbl1.set_text("Изменено")


def print_2():
    print(2)


def print_3():
    print(3)


def print_4():
    print(4)


btn1 = MenuButton(0, 0, 0, 0, func=print_1, color=BUTTON_BACKGROUND_COLOR, text="Начать", text_color=TEXT_COLOR,
                  text_size=TEXT_SIZE)
btn2 = MenuButton(0, 0, 0, 0, func=print_2, color=BUTTON_BACKGROUND_COLOR, text="Заново", text_color=TEXT_COLOR,
                  text_size=TEXT_SIZE)
btn3 = MenuButton(0, 0, 0, 0, func=print_3, color=BUTTON_BACKGROUND_COLOR, text="Настройки", text_color=TEXT_COLOR,
                  text_size=TEXT_SIZE)
btn4 = MenuButton(0, 0, 0, 0, func=print_4, color=BUTTON_BACKGROUND_COLOR, text="Выйти", text_color=TEXT_COLOR,
                  text_size=TEXT_SIZE)
btn5 = f'MenuButton(0, 0, 0, 0, func=print_4, color=BUTTON_BACKGROUND_COLOR, text="*кнопка*",' + \
       f' text_color=TEXT_COLOR, text_size={TEXT_SIZE})'

lbl1 = MenuLabel(0, 0, 0, 0, color=LABEL_BACKGROUND_COLOR, text="какой-то\nтекст\nна пи сан", text_color='#1a1a1a',
                 text_size=TEXT_SIZE,
                 indent=LABEL_INDENT)

lb = []
for x in range(1, 5):
    eval(f'lb.append(btn{x})')
for x in range(4):
    lb.append(eval(btn5))
btn = MenuButtonList(lb)

ll = [lbl1]
lbl = MenuLabelList(ll)

place = ['l']
for x in range(len(lb)):
    place.append("b")

layout = MenuLayOut(btn, lbl, place, 0, 0, 60, 600, LAYOUT_INDENT, LAYOUT_BACKGROUND_COLOR, 'v')
