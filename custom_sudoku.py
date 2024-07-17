import pygame # 2.6.0
import pygame_gui # 0.6.8
from collections import defaultdict
import sys
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox

def resource_path(relative_path):
    try:
        # PyInstaller가 패키징한 경우, 실행 파일 위치 기준 경로
        base_path = sys._MEIPASS
    except Exception:
        # PyInstaller가 패키징하지 않은 경우, 스크립트 위치 기준 경로
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 화면 크기 설정
DEFAULT_SIZE = width, height = 800, 600

# 색상 정의
black = (0, 0, 0)
gray = (177, 177, 177)
white = (255, 255, 255)
HL_SELECTED = (100, 100, 100, 128)
HL_INVALID = (100, 0, 0, 128)

full_txt = {'0':'０', '1':'１', '2':'２', '3':'３', '4':'４',
            '5':'５', '6':'６', '7':'７', '8':'８', '9':'９',
            'L':'Ｌ', 'M':'Ｍ', 'H':'Ｈ'}

ex_color = defaultdict(lambda: (40, 40, 40))
ex_color.update({'CT':(255, 255, 40),
                })

ex_size = defaultdict(lambda: 0.6)
ex_size.update({'CT':0.3,
                })

ex_offset = defaultdict(lambda: (0, 0))
ex_offset.update({'CT':(0, -0.35),
                  })


def draw_custom_cursor(surface, pos):
    # 삼각형 커서 (폴리곤)
    cursor_color = (150, 150, 150)
    cursor_points = [
        (pos[0], pos[1]),
        (pos[0] + 20, pos[1] + 20),
        (pos[0] + 8, pos[1] + 19.2),
        (pos[0], pos[1] + 28)
    ]
    pygame.draw.polygon(surface, cursor_color, cursor_points)

def draw_fixed_text(screen, grid, gametype):
    n = len(grid)
    m = len(grid[0])

    width, height = screen.get_size()
    cell_size = min(width / m, height / (n + 3))
    font_size = int(cell_size * 0.8)  # 셀 크기에 비례한 폰트 크기
    font = pygame.font.SysFont('Arial', font_size, bold=True)
    
    lefttop = pygame.Rect(cell_size * 0.35, 0, cell_size * 2, cell_size * 1.5)
    text_gametype = font.render(' '.join(gametype), True, white)
    rect_gametype = text_gametype.get_rect(midleft=lefttop.midleft)
    screen.blit(text_gametype, rect_gametype)

    righttop = pygame.Rect(width - cell_size * 2.35, 0, cell_size * 2, cell_size * 1.5)
    text_timer = font.render('00:00', True, white)
    rect_timer = text_timer.get_rect(midright=righttop.midright)
    screen.blit(text_timer, rect_timer)

    return rect_gametype

def init_grid(screen, grid, ex_row, ex_col):
    n, m = len(grid), len(grid[0])
    ex_n = max(len(each) for each in ex_col)
    ex_m = max(len(each) for each in ex_row)
    
    width, height = screen.get_size()
    cell_size = min(width / (m + ex_m / 2 + 1), height / (n + ex_n / 2 + 4))  # 셀 크기를 화면 크기에 맞춰 조정
    grid_width = (m + ex_m / 2) * cell_size
    grid_height = (n + ex_n / 2) * cell_size

    # 그리드를 가운데에 정렬하기 위한 시작 위치 계산
    x = (width - grid_width) / 2
    y = (height - grid_height) / 2

    grid_rect = [[pygame.Rect(x + col * cell_size, y + row * cell_size, 1.05 * cell_size, 1.05 * cell_size) for col in range(9)] for row in range(9)]

    for row in range(9):
        for col in range(len(ex_row[row])):
            grid_rect[row].append(pygame.Rect(x + (9.05 + col / 2) * cell_size, y + row * cell_size, 1.02 * cell_size / 2, 1.02 * cell_size))

    grid_rect.extend([[pygame.Rect(x + col * cell_size, y + (9.05 + row / 2) * cell_size, 1.02 * cell_size, 1.02 * cell_size / 2) for col in range(9)] for row in range(ex_n)])

    return grid_rect

    
def draw_grid(screen, grid_rect, grid, ex_grid, ex_row, ex_col, highlight):
    n, m = len(grid), len(grid[0])
    ex_n = max(len(each) for each in ex_col)
    ex_m = max(len(each) for each in ex_row)
    
    width, height = screen.get_size()
    cell_size = min(width / (m + ex_m / 2 + 1), height / (n + ex_n / 2 + 4))  # 셀 크기를 화면 크기에 맞춰 조정
    grid_width = (m + ex_m / 2) * cell_size
    grid_height = (n + ex_n / 2) * cell_size

    font = pygame.font.Font(resource_path('Fonts/NanumGothic.ttf'), int(cell_size * 0.6))
    bold_font = pygame.font.Font(resource_path('Fonts/NanumGothicExtraBold.ttf'), int(cell_size * 0.6))
    extra_font = pygame.font.SysFont('Arial', int(cell_size * 0.4), bold=False)

    # 그리드를 가운데에 정렬하기 위한 시작 위치 계산
    x = (width - grid_width) / 2
    y = (height - grid_height) / 2

    # 하이라이트 표시
    for name, (cells, color) in highlight.items():
        for row, col in cells:
            surface = pygame.Surface(grid_rect[row][col].size, pygame.SRCALPHA)
            surface.fill(color)
            screen.blit(surface, grid_rect[row][col].topleft)

    # 그리드 그리기
    for row in range(9):
        for col in range(9):
            # 특수 규칙
            for each_type, each_ex_grid in ex_grid.items():
                if each_ex_grid[row][col]:
                    ex_font = pygame.font.Font(resource_path('Fonts/NanumGothicExtraBold.ttf'), int(cell_size * ex_size[each_type]))
                    ex_text = ex_font.render(each_ex_grid[row][col], True, ex_color[each_type])
                    ex_pos = tuple(a + b * cell_size for a, b in zip(grid_rect[row][col].center, ex_offset[each_type]))
                    ex_text_rect = ex_text.get_rect(center=ex_pos)
                    screen.blit(ex_text, ex_text_rect)
            
            num_color = (150, 150, 150)
            num_font = font
            # 숫자 그리기
            if grid[row][col] in full_txt.values():
                num_color = white 
                num_font = bold_font
            text = num_font.render(grid[row][col], True, num_color)
            text_rect = text.get_rect(center=grid_rect[row][col].center)
            screen.blit(text, text_rect)


    # 그리드 선 그리기
    for row in range(n + 1):
        if row % 3 == 0:
            pygame.draw.line(screen, white, (x, y + row * cell_size), (x + grid_width, y + row * cell_size), 2)
        else:
            pygame.draw.line(screen, gray, (x, y + row * cell_size), (x + grid_width, y + row * cell_size), 1)

    for col in range(m + 1):
        if col % 3 == 0:
            pygame.draw.line(screen, white, (x + col * cell_size, y), (x + col * cell_size, y + grid_height), 2)
        else:
            pygame.draw.line(screen, gray, (x + col * cell_size, y), (x + col * cell_size, y + grid_height), 1)

    for row in range(9):
        for col, each in enumerate(ex_row[row], 9):
            text = extra_font.render(each, True, white)
            text_rect = text.get_rect(center=grid_rect[row][col].center)
            screen.blit(text, text_rect)
        
    for col in range(9):
        for row, each in enumerate(ex_col[col], 9):
            text = extra_font.render(each, True, white)
            text_rect = text.get_rect(center=grid_rect[row][col].center)
            screen.blit(text, text_rect)
        

default_board = {
    'normal':'''+ ― ― ― + ― ― ― + ― ― ― +
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― +
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― +
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― +''',
    'extra_row':'''+ ― ― ― + ― ― ― + ― ― ― + ― ―
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― + ― ―
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― + ― ―
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― + ― ―''',
    'extra_col':'''+ ― ― ― + ― ― ― + ― ― ― +
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― +
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― +
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― +
|       |       |       |
|       |       |       |''',
    'extra':'''+ ― ― ― + ― ― ― + ― ― ― + ― ―
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― + ― ―
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― + ― ―
| • • • | • • • | • • • |
| • • • | • • • | • • • |
| • • • | • • • | • • • |
+ ― ― ― + ― ― ― + ― ― ― + ― ―
|       |       |       |
|       |       |       |''',
}

description = {
    'DT':'''[ DT ] 디스턴트 - 같은 종류의 두 숫자는 대각선으로 인접하지 않습니다.
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ • • • ｜ ３ • • ｜
｜ • • ３ ｜ • • • ｜   ▶  Ｘ
｜ • • • ｜ • • • ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋''',
    'TP':'''[ TP ] 트리플렛 - 연속하는 세 숫자는 가로, 세로, 대각선으로 나타나지 않습니다.
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ • • • ｜ • • • ｜
｜ • • ３ ｜ ２ １ ７ ｜
｜ • • • ｜ • • ６ ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋   ▶  Ｘ
｜ • • • ｜ ８ • ５ ｜
｜ • • ７ ｜ • • • ｜
｜ • ６ • ｜ • • • ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋''',
    'CR':'''[ CR ] 크로스 - 게임판을 가로지르는 두 대각선에서도 각각 1부터 9까지의 숫자가 중복 없이 하나씩 들어가야 합니다.''',
    'RO':'''[ RO ] 러프 - 몇몇 처음에 주어지는 숫자들은 문자 L, M, H 중 하나로 대체됩니다.
각 문자가 정확히 무슨 숫자가 변한 것인지는 알 수 없지만,
L은 1-3, M은 4-6, H는 7-9가 대체된 것입니다.''',
    'SD':'''[ SD ] 사이드 - 보드판 바깥의 숫자는 그 행/열에서 1과 9 사이에 있는 숫자의 개수를 나타냅니다.
(보드판 바깥의 숫자는 스도쿠 규칙과 무관합니다)
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ
｜ １ • • ｜ • • • ｜ ９ • • ｜ ５
｜ • • • ｜ • ９ １ ｜ • • • ｜ ０
｜ • １ • ｜ • • • ｜ • • ９ ｜ ６
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ''',
    'FX':'''[ FX ] 픽스드 - 보드판 바깥의 숫자의 순서는 그 행/열에서 등장하는 숫자의 순서와 일치해야 합니다.
(보드판 바깥의 숫자는 스도쿠 규칙과 무관합니다)
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ
｜ １ • • ｜ • ２ • ｜ ３ • • ｜ １２３
｜ • • ５ ｜ • • • ｜ • • ８ ｜ ５８
｜ • ９ ８ ｜ • • ７ ｜ • ６ ５ ｜ ９８７６５
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ''',
    'AS':'''[ AS ] 어센드 - 각 행과 열에서 1과 9, 그리고 그 사이에 있는 수들로 이루어진 순열은 항상 증가하거나 감소해야 합니다.
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ １ • ４ ｜ • ６ • ｜ ９ • • ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ • • • ｜ １ ５ ６ ｜ • • ９ ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ • ９ ８ ｜ • • ３ ｜ ２ １ • ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋''',
    'QT':'''[ QT ] 퀀텀 - 보드판 바깥에 있는 두 숫자 X, Y는 다음 두 가지 중 단 하나만을 나타냅니다.
"그 줄의 X번째 칸의 숫자는 Y이다" or "그 줄의 Y번째 칸의 숫자는 X이다"
(줄에서 첫 번째 칸은 가장 위, 또는 왼쪽 칸이며, 보드판 바깥의 숫자는 스도쿠 규칙과 무관합니다)
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ
｜ ６ • • ｜ １ • • ｜ • • • ｜ １４
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ
｜ • • • ｜ • • • ｜ • ９ ２ ｜ ８９
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ
｜ • • ７ ｜ • • • ｜ ３ • • ｜ ３７ (Ｘ)
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ''',
    'LI':'''[ LI ] 라이어 - 처음에 주어지는 숫자는 각각 실제 그 칸에 적힐 숫자보다 정확히 1 낮거나 1 높습니다.
1 --> 2
2 --> 1 or 3
3 --> 2 or 4
...
9 --> 8''',
    'RM':'''[ RM ] 리모트 - 상하좌우로 인접한 수끼리는 최소한 2 이상의 수 차이가 나야 합니다.
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ ４ ３ • ｜ ２ １ • ｜ • ７ ８ ｜   ▶  Ｘ
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋''',
    'QD':'''[ QD ] 쿼드 - 어떤 2×2 영역을 골라도 합이 16 이상 25 미만이어야 합니다.
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ • ８ ２ ｜ • • • ｜
｜ • ７ ３ ｜ • ９ ８ ｜
｜ • • • ｜ • ２ ３ ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ • • ６ ｜ ８ • • ｜
｜ ７ ３ １ ｜ ４ • • ｜
｜ ６ ５ • ｜ • • • ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋''',
    'CT':'''[ CT ] 센터 - 캐럿(^) 표시된 칸에 적힌 숫자는 상하좌우로 인접한 칸에 적힌 숫자보다 항상 커야 합니다.
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋
｜ • ２ • ｜ ４ 8^３ ｜
｜ １ 7^５ ｜ • ６ • ｜
｜ • ４ • ｜ • • • ｜
＋ ㅡ ㅡ ㅡ ＋ ㅡ ㅡ ㅡ ＋''',
}

title = '''[ Custom Sudoku v1.2 ]

Official : <a href="https://github.com/I-Cubic-I/Custom-Sudoku">github.com/I-Cubic-I/Custom-Sudoku</a>

이 게임에서 사용된 모든 스도쿠 변형 규칙은 <a href="https://discord.com/invite/aJPwNY7g6g">pillowprism</a>에게 권한이 있으며,
허가를 받아 사용되었습니다. 
'''

update_description = '''What's new:
 - 단일 모드 DT, CR, SD, FX, LI, RM, CT에 대한 세부 규칙 판정 추가
 - FX는 구현이 완룓되었으나 버그 또는 사용자 경험 향상을 위해 수정 가능성 있음
 - 특수 복합 모드 'RO + SD', 'RO + CT'에 대한 세부 규칙 판정 추가
 - 게임 내에서 일시정지와 메뉴로 나가는 기능 추가

Future update:
 1. 세부 규칙 판정 (11/12 완료)
 1. 메모 기능 구현
 2. 드래그로 다중 선택 구현
 2. 세부 규칙 툴팁 구현
 3. 타이머 구현
 3. 결과를 텍스트/이미지로 공유
 4. 세이브 구현
 4. Undo Redo 구현
 5. 마우스 위치를 바탕으로하는 힌트 표시
 5. 체크포인트 구현
'''
    
menu_format = {
    'start':{
        'class':pygame_gui.elements.UIButton,
        'pos':(59/72, 53/60),
        'size':(1/5, 1/10),
        'kwargs':{'text':'start'},
    },
    'inputfield':{
        'class':pygame_gui.elements.UITextEntryBox,
        'pos':(1/3, 2/3),
        'size':(5/9, 8/15),
        'kwargs':{'initial_text':default_board['normal']},
    },
    'selection':{
        'class':pygame_gui.elements.UISelectionList,
        'pos':(59/72, 3/5),
        'size':(1/4, 2/5),
        'kwargs':{'item_list':['DT', 'TP', 'CR', 'RO', 'SD', 'FX', 'AS', 'QT', 'LI', 'RM', 'QD', 'CT'],
                  'allow_multi_select':True,
        },
    },
    'textbox':{
        'class':pygame_gui.elements.UITextBox,
        'pos':(1/2, 1/5),
        'size':(8/9, 7/24),
        'kwargs':{'html_text':title},
    },
}
paused_format = {
    'exit':{
        'class':pygame_gui.elements.UIButton,
        'pos':(1/2, 2/3),
        'size':(1/5, 1/10),
        'kwargs':{'text':'exit'},
    },
    'text':{
        'class':pygame_gui.elements.UILabel,
        'pos':(1/2, 1/2),
        'size':(1, 1),
        'kwargs':{'text':'Paused'},
    },
}

def init_UI(root, ui_format, manager):
    UI = dict()
    
    for item, formats in ui_format.items():
        formats['kwargs']['relative_rect'] = pygame.Rect(get_rect(root, formats['pos'], formats['size']))
        formats['kwargs']['manager'] = manager

        UI[item] = formats['class'](**formats['kwargs'])
        UI[item].rebuild_from_changed_theme_data()

        if 'subUI' in formats:
            for subitem, subformats in formats['subUI'].items():
                subformats['kwargs']['container'] = UI[item]
            subUI = init_UI(UI[item], formats['subUI'], manager)
            UI[item] = (UI[item], subUI)

    return UI


def clear_UI(UI):
    for element in UI.values():
        if isinstance(element, tuple):
            element[0].kill()
        else:
            element.kill()
    UI.clear()


def get_rect(root, pos, size):
    if hasattr(root, 'get_size'):
        width, height = root.get_size()
        suit_size = min(width, height)
        
        ratio_x, ratio_y = pos
        ratio_w, ratio_h = size

        w, h = suit_size * ratio_w, suit_size * ratio_h
        x, y = (width - suit_size) / 2 + suit_size * ratio_x - w / 2, (height - suit_size) / 2 + suit_size * ratio_y - h / 2

    else:
        width, height = root.relative_rect.size
        
        ratio_x, ratio_y = pos
        ratio_w, ratio_h = size

        w, h = width * ratio_w, height * ratio_h
        x, y = width * ratio_x - w / 2, height * ratio_y - h / 2

    return x, y, w, h
    
     
def resize_UI(root, UI, ui_format):
    for item, formats in ui_format.items():
        x, y, w, h = get_rect(root, formats['pos'], formats['size'])

        try: target, sub = UI[item]
        except: target = UI[item]

        target.set_relative_position((x, y))
        target.set_dimensions((w, h))

        if 'subUI' in formats:
            resize_UI(target, sub, formats['subUI'])

def check_board_valid(grid, ex_grid, ex_row, ex_col, gametype):
    invalid = set()
    for row in range(9):
        for col in range(9):
            num = grid[row][col]
            if not num:
                continue

            row_count = sum(bool(grid[row][i]) and int(grid[row][i]) == int(num) for i in range(9))
            col_count = sum(bool(grid[i][col]) and int(grid[i][col]) == int(num) for i in range(9))
            box_count = sum(bool(grid[row // 3 * 3 + i][col // 3 * 3 + j]) and int(grid[row // 3 * 3 + i][col // 3 * 3 + j]) == int(num) for i in range(3) for j in range(3))
            if row_count > 1 or col_count > 1 or box_count > 1:
                invalid.add((row, col))

    if 'DT' in gametype:
        for row in range(8):
            for col in range(8):
                if not grid[row][col] or not grid[row + 1][col + 1]:
                    continue

                if int(grid[row][col]) == int(grid[row + 1][col + 1]):
                    invalid.update({(row, col), (row + 1, col + 1)})

        for row in range(1, 9):
            for col in range(8):
                if not grid[row][col] or not grid[row - 1][col + 1]:
                    continue

                if int(grid[row][col]) == int(grid[row - 1][col + 1]):
                    invalid.update({(row, col), (row - 1, col + 1)})

    if 'TP' in gametype:
        for row in range(9):
            for col in range(7):
                unit = [grid[row][col + i] for i in range(3)]
                if None in unit:
                    continue
                unit = list(map(int, unit))

                if unit[0] + 1 == unit[1] == unit[2] - 1 or unit[0] - 1 == unit[1] == unit[2] + 1:
                    invalid.update({(row, col + i) for i in range(3)})
                
        for col in range(9):
            for row in range(7):
                unit = [grid[row + i][col] for i in range(3)]
                if None in unit:
                    continue
                unit = list(map(int, unit))

                if unit[0] + 1 == unit[1] == unit[2] - 1 or unit[0] - 1 == unit[1] == unit[2] + 1:
                    invalid.update({(row + i, col) for i in range(3)})

        for row in range(7):
            for col in range(7):
                unit = [grid[row + i][col + i] for i in range(3)]
                if None in unit:
                    continue
                unit = list(map(int, unit))

                if unit[0] + 1 == unit[1] == unit[2] - 1 or unit[0] - 1 == unit[1] == unit[2] + 1:
                    invalid.update({(row + i, col + i) for i in range(3)})
                
        for row in range(2, 9):
            for col in range(7):
                unit = [grid[row - i][col + i] for i in range(3)]
                if None in unit:
                    continue
                unit = list(map(int, unit))

                if unit[0] + 1 == unit[1] == unit[2] - 1 or unit[0] - 1 == unit[1] == unit[2] + 1:
                    invalid.update({(row - i, col + i) for i in range(3)})

    if 'CR' in gametype:
        for i in range(9):
            num = grid[i][i]
            if not num:
                continue

            if sum(bool(grid[j][j]) and int(grid[j][j]) == int(num) for j in range(9)) > 1:
                invalid.add((i, i))

        for i in range(9):
            num = grid[8 - i][i]
            if not num:
                continue

            if sum(bool(grid[8 - j][j]) and int(grid[8 - j][j]) == int(num) for j in range(9)) > 1:
                invalid.add((8 - i, i))

    if 'RO' in gametype:
        # 해당 RO 칸을 채울 수 있는 숫자가 없는 경우에도 invalid 되게 끔 추가할 것??
        for row in range(9):
            for col in range(9):
                if not grid[row][col] or not ex_grid['RO'][row][col] or (row, col) in invalid:
                    continue

                if ex_grid['RO'][row][col] == 'L' and int(grid[row][col]) not in range(1, 4):
                    invalid.add((row, col))
                elif ex_grid['RO'][row][col] == 'M' and int(grid[row][col]) not in range(4, 7):
                    invalid.add((row, col))
                elif ex_grid['RO'][row][col] == 'H' and int(grid[row][col]) not in range(7, 10):
                    invalid.add((row, col))

    if 'AS' in gametype:
        for row in range(9):
            pass

    if 'LI' in gametype:
        for row in range(9):
            for col in range(9):
                if not ex_grid['LI'][row][col] or not grid[row][col]:
                    continue

                if abs(int(grid[row][col]) - int(ex_grid['LI'][row][col])) != 1:
                    invalid.add((row, col))

    if 'RM' in gametype:
        for row in range(9):
            for col in range(8):
                if not grid[row][col] or not grid[row][col + 1]:
                    continue

                if abs(int(grid[row][col]) - int(grid[row][col + 1])) == 1:
                    invalid.update({(row, col), (row, col + 1)})

        for col in range(9):
            for row in range(8):
                if not grid[row][col] or not grid[row + 1][col]:
                    continue

                if abs(int(grid[row][col]) - int(grid[row + 1][col])) == 1:
                    invalid.update({(row, col), (row + 1, col)})

    if 'QD' in gametype:
        square = [(0, 0), (1, 0), (0, 1), (1, 1)]
        for row in range(8):
            for col in range(8):
                total = 0
                for x, y in square:
                    if not grid[row + x][col + y]:
                        break
                    total += int(grid[row + x][col + y])
                else:
                    if total not in range(16, 25):
                        for x, y in square:
                            invalid.add((row + x, col + y))

    if 'CT' in gametype:
        for row in range(9):
            for col in range(9):
                if not ex_grid['CT'][row][col] or not grid[row][col]:
                    continue

                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    if 0 <= row + dx < 9 and 0 <= col + dy < 9 and grid[row + dx][col + dy]:
                        if int(grid[row][col]) < int(grid[row + dx][col + dy]):
                            invalid.update({(row, col), (row + dx, col + dy)})

    # ex_row/col 규칙
    if 'SD' in gametype:
        for row in range(9):
            if not ex_row[row]:
                continue

            unit = [int(grid[row][col]) if grid[row][col] else 0 for col in range(9)]
            if 1 not in unit or 9 not in unit:
                continue

            num = ex_row[row][0]
            dist = abs(unit.index(1) - unit.index(9)) - 1
            pos = {(row, unit.index(1)), (row, unit.index(9)), (row, 9)}

            if 'RO' in gametype:
                if num == 'L' and dist not in range(1, 4):
                    invalid.update(pos)
                elif num == 'M' and dist not in range(4, 7):
                    invalid.update(pos)
                elif num == 'H' and dist not in range(7, 10):
                    invalid.update(pos)
            else:
                if int(num) != dist:
                    invalid.update(pos)

        for col in range(9):
            if not ex_col[col]:
                continue

            unit = [int(grid[row][col]) if grid[row][col] else 0 for row in range(9)]
            if 1 not in unit or 9 not in unit:
                continue

            num = ex_col[col][0]
            dist = abs(unit.index(1) - unit.index(9)) - 1
            pos = {(unit.index(1), col), (unit.index(9), col), (9, col)}

            if 'RO' in gametype:
                if num == 'L' and dist not in range(1, 4):
                    invalid.update(pos)
                elif num == 'M' and dist not in range(4, 7):
                    invalid.update(pos)
                elif num == 'H' and dist not in range(7, 10):
                    invalid.update(pos)
            else:
                if int(num) != dist:
                    invalid.update(pos)

    elif 'FX' in gametype:
        for row in range(9):
            if not ex_row[row]:
                continue

            unit = [int(grid[row][col]) if grid[row][col] else 0 for col in range(9)]
            for i in range(len(ex_row[row])):
                x = int(ex_row[row][i])
                if x not in unit:
                    continue

                first = unit.index(x)
                left = sum(grid[row][col] == None or int(grid[row][col]) in map(int, ex_row[row][:i]) for col in range(first))
                right = sum(grid[row][col] == None or int(grid[row][col]) in map(int, ex_row[row][i + 1:]) for col in range(first + 1, 9))

                if i > left:
                    #invalid.add((row, first))
                    invalid.update({(row, 9 + col) for col in range(i) if int(ex_row[row][col]) not in unit[:first]})
                
                if len(ex_row[row]) - i - 1 > right:
                    #invalid.add((row, first))
                    invalid.update({(row, 9 + col) for col in range(i + 1, len(ex_row[row])) if int(ex_row[row][col]) not in unit[:first + 1]})
                
                for j in range(i + 1, len(ex_row[row])):
                    y = int(ex_row[row][j])
                    if y not in unit:
                        continue

                    second = unit.index(y)
                    
                    if first > second:
                        invalid.update({(row, first), (row, second), (row, (9 + i)), (row, (9 + j))})

                    else:
                        between = j - i - 1
                        idx_dist = second - first - 1
                        if idx_dist < between:
                            #invalid.update({(row, col) for col in range(first + 1, second)})
                            invalid.update({(row, 9 + col) for col in range(i + 1, j) if int(ex_row[row][col]) not in unit[first + 1:second]})
        
        for col in range(9):
            if not ex_col[col]:
                continue

            unit = [int(grid[row][col]) if grid[row][col] else 0 for row in range(9)]
            for i in range(len(ex_col[col])):
                x = int(ex_col[col][i])
                if x not in unit:
                    continue

                first = unit.index(x)
                left = sum(grid[row][col] == None or int(grid[row][col]) in map(int, ex_col[col][:i]) for row in range(first))
                right = sum(grid[row][col] == None or int(grid[row][col]) in map(int, ex_col[col][i + 1:]) for row in range(first + 1, 9))

                if i > left:
                    invalid.add((first, col))
                    invalid.update({(9 + row, col) for row in range(i) if int(ex_col[col][row]) not in unit[:first]})
                
                if len(ex_col[col]) - i - 1 > right:
                    invalid.add((first, col))
                    invalid.update({(9 + row, col) for row in range(i + 1, len(ex_col[col])) if int(ex_col[col][row]) not in unit[first + 1:]})
                
                for j in range(i + 1, len(ex_col[col])):
                    y = int(ex_col[col][j])
                    if y not in unit:
                        continue

                    second = unit.index(y)
                    
                    if first > second:
                        invalid.update({(first, col), (second, col), ((9 + i), col), ((9 + j), col)})

                    else:
                        between = j - i - 1
                        idx_dist = second - first - 1
                        if idx_dist < between:
                            #invalid.update({(row, col) for row in range(first + 1, second)})
                            invalid.update({(9 + row, col) for row in range(i + 1, j) if int(ex_col[col][row]) not in unit[first + 1:second]})
        
        
        
    elif 'QT' in gametype:
        for row in range(9):
            if not ex_row[row]:
                continue

            x, y = map(int, ex_row[row])
            unit = [int(grid[row][col]) if grid[row][col] else 0 for col in range(9)]
            if x in unit and y in unit:
                if (unit.index(x) == y - 1) == (unit.index(y) == x - 1):
                    invalid.update({(row, unit.index(x)), (row, unit.index(y)), (row, 9), (row, 10)})
                    continue
            
            if not grid[row][x - 1] or not grid[row][y - 1]:
                continue

            if (int(grid[row][x - 1]) == y) == (int(grid[row][y - 1]) == x):
                invalid.update({(row, x - 1), (row, y - 1), (row, 9), (row, 10)})

        for col in range(9):
            if not ex_col[col]:
                continue

            x, y = map(int, ex_col[col])
            unit = [int(grid[row][col]) if grid[row][col] else 0 for row in range(9)]
            if x in unit and y in unit:
                if (unit.index(x) == y - 1) == (unit.index(y) == x - 1):
                    invalid.update({(unit.index(x), col), (unit.index(y), col), (9, col), (10, col)})
                    continue

            if not grid[x - 1][col] or not grid[y - 1][col]:
                continue

            if (int(grid[x - 1][col]) == y) == (int(grid[y - 1][col]) == x):
                invalid.update({(x - 1, col), (y - 1, col), (9, col), (10, col)})

            
    return list(invalid)

def check_board_format(board, gametype):
    board = board.replace('  ', ' •')
    board = board.replace('+', '')
    board = board.replace('―', '')
    board = board.replace('|', '')
    board = board.replace(' ', '')
    board = board.replace('\n\n', '\n')

    grid = [[None] * 9 for _ in range(9)]
    ex_grid = {}
    ex_row = [[] for _ in range(9)]
    ex_col = [[] for _ in range(9)]

    ex_grid_type = ['LI', 'RO', 'CT']
    for each_type in ex_grid_type:
        if each_type in gametype:
            ex_grid[each_type] = [[None] * 9 for _ in range(9)]

    for i, row in enumerate(board.split()):
        if 'CT' in gametype:
            temp_row = ''
            for item in row:
                if item == '^' and i < 9 and len(temp_row) - 1 < 9:
                    ex_grid['CT'][i][len(temp_row) - 1] = 'ㅅ'
                else:
                    temp_row += item
            row = temp_row
        
        for j, item in enumerate(row):
            if item in ['o', 'x', '-', '•']:
                continue

            if i < 9 and j < 9:
                if 'LI' in gametype and item.isdigit():
                    ex_grid['LI'][i][j] = item
                elif 'RO' in gametype and item.isalpha():
                    ex_grid['RO'][i][j] = item
                else:
                    if item == '0':
                        continue
                    if item in full_txt.keys():
                        grid[i][j] = full_txt[item]
            elif i >= 9 and j < 9:
                ex_col[j].append(item)
            elif j >= 9 and i < 9:
                ex_row[i].append(item)

    for col in range(9):
        if set(ex_col[col]) == {'•'}:
            ex_col[col] = []

    min_ex_row, max_ex_row = min(len(each) for each in ex_row), max(len(each) for each in ex_row)
    min_ex_col, max_ex_col = min(len(each) for each in ex_col), max(len(each) for each in ex_col)

    ex_type = ['SD','FX', 'QT']
    if sum(ex in gametype for ex in ex_type) > 1:
        return '동시에 적용할 수 없는 모드가 존재합니다.'

    if set(gametype).isdisjoint(set(ex_type)) and (max_ex_row > 0 or max_ex_col > 0):
        return '불필요한 행 또는 열이 존재합니다.'
            
    if 'RO' not in gametype and sum(item in ['Ｌ', 'Ｍ', 'Ｈ'] for each in (grid, *ex_grid.values(), ex_row, ex_col) for row in each for item in row if item is not None) > 0:
        return '숫자 외의 알 수 없는 문자가 존재합니다.'
    
    if 'QT' in gametype:
        if sum(len(each) not in (0, 2) for each in ex_row) > 0 or sum(len(each) not in (0, 2) for each in ex_col):
            return 'QT 모드는 2개의 힌트가 요구됩니다.'

        elif sum(each[0] == each[1] for each in ex_row if each) > 0 or sum(each[0] == each[1] for each in ex_col if each):
            return 'QT 모드에 같은 두 숫자가 사용될 수 없습니다.'
            
    return grid, ex_grid, ex_row, ex_col

def check_hover_on_items(event_pos, selection):
    item_height = selection.list_item_height
    for index, item in enumerate(selection.item_list):
        item_rect = pygame.Rect(selection.rect.left, selection.rect.top + index * item_height, selection.rect.width, item_height)
        if item_rect.collidepoint(event_pos):
            return item
    return None

def change_text(textbox, text):
    if textbox.html_text != text:
        textbox.set_text(text)

def valid_update(UI):
    gametype = UI['selection'].get_multi_selection()
    board = check_board_format(UI['inputfield'].get_text(), gametype)
    if isinstance(board, str):
        UI['start'].disable()
        change_text(UI['textbox'], board)

    else:
        grid, ex_grid, ex_row, ex_col = board
        invalid = check_board_valid(grid, ex_grid, ex_row, ex_col, gametype)
        if invalid:
            UI['start'].disable()
            change_text(UI['textbox'], "규칙에 위배되는 불가능한 보드입니다.\n올바르지 않은 셀: " + ', '.join(map(str, invalid)))
        else:
            UI['start'].enable()
            change_text(UI['textbox'], title)


def main():
    # 초기화
    pygame.init()

    screen = pygame.display.set_mode(DEFAULT_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption('Custom Sudoku')
    pygame.mouse.set_visible(False)

    icon = pygame.image.load(resource_path('Images/custom_sudoku.png'))
    pygame.display.set_icon(icon)

    # GUI 매니저 설정
    manager = pygame_gui.UIManager((width, height), resource_path('Themes/theme.json'))


    page = 'Menu'

    UI = init_UI(screen, menu_format, manager)
    gametype = []
    grid = ex_grid = ex_row = ex_col = None
    grid_rect = None

    highlight = dict()

    # 게임 루프
    prev_cursor = 0
    last_key = None
    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(144) / 1000.0

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

                manager.set_window_resolution(event.size)
                if page == 'Menu':
                    resize_UI(screen, UI, menu_format)
                elif page == 'Game':
                    grid_rect = init_grid(screen, grid, ex_row, ex_col)
                elif page == 'Paused':
                    resize_UI(screen, UI, paused_format)


            # pygame_gui 이벤트
            manager.process_events(event)

            if page == 'Menu':
                # 시작 버튼 클릭
                if event.type == pygame_gui.UI_BUTTON_PRESSED and (target:=event.ui_element) == UI['start']:
                    gametype = UI['selection'].get_multi_selection()
                    board = check_board_format(UI['inputfield'].get_text(), gametype)

                    clear_UI(UI)
                        
                    page = 'Game'
                    grid, ex_grid, ex_row, ex_col = board
                    grid_rect = init_grid(screen, grid, ex_row, ex_col)

                    UI = dict()

                elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                    webbrowser.open(event.link_target)

                elif event.type == pygame.KEYDOWN and event.key != pygame.K_BACKSPACE and UI['inputfield'].is_focused:
                    prev_cursor += 1
                    
                elif event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and (target:=event.ui_element) == UI['inputfield']:
                    start, end = UI['inputfield'].select_range

                    if start == end == 0:
                        target.set_text(target.get_text())
                        UI['inputfield'].edit_position = prev_cursor
                        UI['inputfield'].select_range = [prev_cursor, prev_cursor]

                    valid_update(UI)

                elif event.type == pygame.MOUSEMOTION:
                    hovered = check_hover_on_items(event.pos, UI['selection'])
                    if hovered is not None:
                        change_text(UI['textbox'], description[hovered['text']])
                    else:
                        if UI['start'].is_enabled:
                            change_text(UI['textbox'], title)
                        else:
                            valid_update(UI)

                elif event.type in (pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION, pygame_gui.UI_SELECTION_LIST_NEW_SELECTION) and (target:=event.ui_element) == UI['selection']:
                    gametype = UI['selection'].get_multi_selection()
                    board = check_board_format(UI['inputfield'].get_text(), gametype)
                    if isinstance(board, str):
                        UI['start'].disable()
                    else:
                        grid, ex_grid, ex_row, ex_col = board
                        if check_board_valid(grid, ex_grid, ex_row, ex_col, gametype):
                            UI['start'].disable()
                        else:
                            UI['start'].enable()
                        
            elif page == 'Game':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    new_select = None
                    for row in range(9):
                        for col in range(9):
                            if grid_rect[row][col].collidepoint(event.pos):
                                new_select = (row, col)
                                break
                        else: continue
                        break

                    multi = pygame.key.get_mods() & pygame.KMOD_SHIFT or pygame.key.get_mods() & pygame.KMOD_CTRL

                    if new_select:
                        if 'selected' not in highlight or not multi:
                            highlight['selected'] = ([], HL_SELECTED)

                        try:
                            highlight['selected'][0].remove(new_select)
                        except:
                            highlight['selected'][0].append(new_select)

                    else:
                        if 'selected' in highlight and not multi:
                            del highlight['selected']

                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit() and event.unicode != '0':
                        if 'selected' in highlight:
                            for row, col in highlight['selected'][0]:
                                if grid[row][col] not in full_txt.values():
                                    grid[row][col] = event.unicode

                            invalid = check_board_valid(grid, ex_grid, ex_row, ex_col, gametype)
                            highlight['invalid'] = (invalid, HL_INVALID)

                    elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                        if 'selected' in highlight:
                            for row, col in highlight['selected'][0]:
                                if grid[row][col] not in full_txt.values():
                                    grid[row][col] = None
                            invalid = check_board_valid(grid, ex_grid, ex_row, ex_col, gametype)
                            highlight['invalid'] = (invalid, HL_INVALID)

                    elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        highlight['selected'] = ([(row, col) for row in range(9) for col in range(9)], HL_SELECTED)
                        
                    elif pygame.K_RIGHT <= event.key <= pygame.K_UP or event.key in (ord(c) for c in "wasd"):
                        if 'selected' not in highlight:
                            highlight['selected'] = ([(0, 0)], HL_SELECTED)
                        else:
                            row, col = highlight['selected'][0][-1]
                            if event.key in (pygame.K_UP, pygame.K_w):
                                new_select = ((row + 8) % 9, col)
                            elif event.key in (pygame.K_DOWN, pygame.K_s):
                                new_select = ((row + 1) % 9, col)
                            elif event.key in (pygame.K_LEFT, pygame.K_a):
                                new_select = (row, (col + 8) % 9)
                            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                                new_select = (row, (col + 1) % 9)

                            if pygame.key.get_mods() & pygame.KMOD_SHIFT or pygame.key.get_mods() & pygame.KMOD_CTRL:
                                try:
                                    highlight['selected'][0].remove(new_select)
                                except: pass
                                highlight['selected'][0].append(new_select)
                            else:
                                highlight['selected'] = ([new_select], HL_SELECTED)
                    elif event.key == pygame.K_ESCAPE:
                        page = 'Paused'
                        clear_UI(UI)
                        UI = init_UI(screen, paused_format, manager)
            elif page == 'Paused':
                if event.type == pygame_gui.UI_BUTTON_PRESSED and (target:=event.ui_element) == UI['exit']:
                    if target.text == 'exit':
                        target.set_text("really?")
                    elif target.text == 'really?':
                        page = 'Menu'
                        clear_UI(UI)
                        UI = init_UI(screen, menu_format, manager)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        page = 'Game'
                        clear_UI(UI)
                        grid_rect = init_grid(screen, grid, ex_row, ex_col)
                    

        if page == 'Menu':
            manager.update(time_delta)
            screen.fill(black)
            manager.draw_ui(screen)

            start, end = UI['inputfield'].select_range
            if start != end:
                prev_cursor = min(UI['inputfield'].select_range)

        elif page == 'Game':
            screen.fill(black)

            draw_grid(screen, grid_rect, grid, ex_grid, ex_row, ex_col, highlight)

            # 마우스 호버링 셀 표시
            for row in range(9):
                for col in range(9):
                    if grid_rect[row][col].collidepoint(mouse_pos):
                        pygame.draw.rect(screen, (100, 100, 200), grid_rect[row][col], 3)
                        break
                else: continue
                break
                    
            draw_fixed_text(screen, grid, gametype)
        elif page == 'Paused':
            manager.update(time_delta)
            screen.fill(black)
            manager.draw_ui(screen)
            raise NameError()

        draw_custom_cursor(screen, mouse_pos)

        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pygame.quit()

        root = tk.Tk()
        root.withdraw()
        
        messagebox.showerror("예기치 못한 오류가 발생했습니다.", f"Github의 Issue를 통해 해당 오류를 제보해주세요.\n발생 에러:\n{e}")

        sys.exit()
