import pygame
import arabic_reshaper
from bidi.algorithm import get_display

pygame.init()

# ==================================================
# إعداد الشاشة
# ==================================================

info = pygame.display.Info()

WIDTH = info.current_w
HEIGHT = info.current_h

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.FULLSCREEN
)

pygame.display.set_caption("الهروب من الغرفة")

clock = pygame.time.Clock()

# ==================================================
# مساحة تصميم اللعبة
# ==================================================

GAME_W = 900
GAME_H = 600

game_surface = pygame.Surface(
    (GAME_W, GAME_H)
)

# ==================================================
# الألوان
# ==================================================

BLACK = (15, 15, 20)
BG = (20, 22, 30)

WALL = (55, 48, 62)
FLOOR = (35, 30, 38)

WHITE = (245, 245, 245)
GRAY = (170, 170, 180)

BLUE = (45, 120, 220)
BLUE_HOVER = (70, 150, 245)

BROWN = (105, 65, 38)
GOLD = (225, 180, 60)

RED = (190, 60, 60)
GREEN = (55, 170, 90)

# ==================================================
# الخط العربي
# ==================================================

FONT_PATH = "/system/fonts/NotoNaskhArabic-Regular.ttf"

title_font = pygame.font.Font(
    FONT_PATH,
    58
)

normal_font = pygame.font.Font(
    FONT_PATH,
    38
)

small_font = pygame.font.Font(
    FONT_PATH,
    28
)

tiny_font = pygame.font.Font(
    FONT_PATH,
    24
)

# ==================================================
# رسم العربي
# ==================================================

def draw_arabic(surface, text, font, color, center):

    reshaped = arabic_reshaper.reshape(text)

    bidi_text = get_display(reshaped)

    image = font.render(
        bidi_text,
        True,
        color
    )

    rect = image.get_rect(
        center=center
    )

    surface.blit(
        image,
        rect
    )


# ==================================================
# حجم اللعبة على الهاتف
# ==================================================

def get_game_rect():

    scale = min(
        WIDTH / GAME_W,
        HEIGHT / GAME_H
    )

    new_width = int(
        GAME_W * scale
    )

    new_height = int(
        GAME_H * scale
    )

    x = (WIDTH - new_width) // 2
    y = (HEIGHT - new_height) // 2

    return pygame.Rect(
        x,
        y,
        new_width,
        new_height
    )


# ==================================================
# تحويل إحداثيات الشاشة
# ==================================================

def screen_to_game(pos):

    game_rect = get_game_rect()

    x, y = pos

    if not game_rect.collidepoint(
        x,
        y
    ):
        return None

    gx = (
        x - game_rect.x
    ) * GAME_W / game_rect.width

    gy = (
        y - game_rect.y
    ) * GAME_H / game_rect.height

    return int(gx), int(gy)


# ==================================================
# عرض اللعبة
# ==================================================

def show_game():

    game_rect = get_game_rect()

    resized = pygame.transform.smoothscale(
        game_surface,
        (
            game_rect.width,
            game_rect.height
        )
    )

    screen.fill(
        BLACK
    )

    screen.blit(
        resized,
        game_rect
    )

    pygame.display.flip()


# ==================================================
# زر
# ==================================================

def draw_button(
    surface,
    rect,
    text,
    color=BLUE
):

    mouse = pygame.mouse.get_pos()

    game_mouse = screen_to_game(
        mouse
    )

    if (
        game_mouse is not None
        and rect.collidepoint(game_mouse)
    ):

        draw_color = BLUE_HOVER

    else:

        draw_color = color

    pygame.draw.rect(
        surface,
        draw_color,
        rect,
        border_radius=16
    )

    pygame.draw.rect(
        surface,
        (130, 190, 255),
        rect,
        2,
        border_radius=16
    )

    draw_arabic(
        surface,
        text,
        normal_font,
        WHITE,
        rect.center
    )


# ==================================================
# شاشة البداية
# ==================================================

def menu():

    start_button = pygame.Rect(
        300,
        330,
        300,
        75
    )

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return False

            if event.type == pygame.MOUSEBUTTONDOWN:

                game_pos = screen_to_game(
                    event.pos
                )

                if game_pos is not None:

                    if start_button.collidepoint(
                        game_pos
                    ):

                        return True

        game_surface.fill(
            BG
        )

        draw_arabic(
            game_surface,
            "الهروب من الغرفة",
            title_font,
            WHITE,
            (450, 150)
        )

        draw_arabic(
            game_surface,
            "لغز واحد يفصلك عن الحرية",
            normal_font,
            GRAY,
            (450, 220)
        )

        draw_button(
            game_surface,
            start_button,
            "ابدأ اللعبة"
        )

        draw_arabic(
            game_surface,
            "اكتشف الأدلة وحل الألغاز واخرج من الغرفة",
            small_font,
            GRAY,
            (450, 480)
        )

        show_game()

        clock.tick(60)


# ==================================================
# شاشة الفوز
# ==================================================

def win_screen():

    again_button = pygame.Rect(
        300,
        400,
        300,
        70
    )

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return False

            if event.type == pygame.MOUSEBUTTONDOWN:

                game_pos = screen_to_game(
                    event.pos
                )

                if game_pos is not None:

                    if again_button.collidepoint(
                        game_pos
                    ):

                        return True

        game_surface.fill(
            (18, 35, 25)
        )

        draw_arabic(
            game_surface,
            "نجحت!",
            title_font,
            GOLD,
            (450, 150)
        )

        draw_arabic(
            game_surface,
            "لقد خرجت من الغرفة!",
            title_font,
            WHITE,
            (450, 230)
        )

        draw_arabic(
            game_surface,
            "أحسنت! لقد حللت جميع الألغاز.",
            normal_font,
            WHITE,
            (450, 310)
        )

        draw_button(
            game_surface,
            again_button,
            "العب مرة أخرى"
        )

        show_game()

        clock.tick(60)


# ==================================================
# اللعبة
# ==================================================

def game():

    # ==================================================
    # الأشياء
    # ==================================================

    door = pygame.Rect(
        100,
        170,
        145,
        280
    )

    board = pygame.Rect(
        360,
        120,
        210,
        130
    )

    box = pygame.Rect(
        650,
        345,
        140,
        105
    )

    # ==================================================
    # مكان اللوحة بعد الزحزحة
    # ==================================================

    moved_board = pygame.Rect(
        500,
        120,
        210,
        130
    )

    # ==================================================
    # مكان المفتاح الثاني
    # ==================================================

    hidden_key = pygame.Rect(
        370,
        180,
        80,
        70
    )

    # ==================================================
    # حالات اللعبة
    # ==================================================

    puzzle_open = False

    puzzle_solved = False

    has_first_key = False

    box_open = False

    has_note = False

    board_moved = False

    has_second_key = False

    # ==================================================
    # الرسائل
    # ==================================================

    message = ""

    message_timer = 0

    # ==================================================
    # أزرار اللغز
    # ==================================================

    answer_buttons = [

        (
            pygame.Rect(
                180,
                340,
                120,
                65
            ),
            "7"
        ),

        (
            pygame.Rect(
                330,
                340,
                120,
                65
            ),
            "8"
        ),

        (
            pygame.Rect(
                480,
                340,
                120,
                65
            ),
            "9"
        ),

        (
            pygame.Rect(
                630,
                340,
                120,
                65
            ),
            "10"
        )
    ]

    # ==================================================
    # حلقة اللعبة
    # ==================================================

    running = True

    while running:

        # ==================================================
        # الأحداث
        # ==================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return False

            if event.type != pygame.MOUSEBUTTONDOWN:

                continue

            game_pos = screen_to_game(
                event.pos
            )

            if game_pos is None:

                continue

            # ==================================================
            # نافذة اللغز
            # ==================================================

            if puzzle_open:

                for answer_rect, answer in answer_buttons:

                    if answer_rect.collidepoint(
                        game_pos
                    ):

                        if answer == "8":

                            puzzle_solved = True

                            has_first_key = True

                            puzzle_open = False

                            message = (
                                "صحيح! حصلت على المفتاح الأول."
                            )

                            message_timer = 180

                        else:

                            message = (
                                "إجابة خاطئة... حاول مرة أخرى."
                            )

                            message_timer = 150

                continue

            # ==================================================
            # نافذة الورقة
            # ==================================================

            if box_open:

                close_note = pygame.Rect(
                    330,
                    410,
                    240,
                    65
                )

                if close_note.collidepoint(
                    game_pos
                ):

                    box_open = False

                    message = (
                        "مكتوب على الورقة: دور تحت الرموز."
                    )

                    message_timer = 180

                continue

            # ==================================================
            # المفتاح الثاني
            #
            # مهم:
            # نفحصه قبل اللوحة حتى لا تعتبر اللعبة
            # الضغط عليه ضغطًا على اللوحة.
            # ==================================================

            if board_moved and not has_second_key:

                if hidden_key.collidepoint(
                    game_pos
                ):

                    has_second_key = True

                    message = (
                        "وجدت المفتاح الثاني!"
                    )

                    message_timer = 180

                    continue

            # ==================================================
            # اللوحة
            # ==================================================

            if board.collidepoint(
                game_pos
            ):

                # ------------------------------------------
                # قبل حل اللغز
                # ------------------------------------------

                if not puzzle_solved:

                    puzzle_open = True

                # ------------------------------------------
                # بعد قراءة الورقة
                # ------------------------------------------

                elif has_note and not board_moved:

                    board_moved = True

                    message = (
                        "زحزحت اللوحة... انظر خلفها!"
                    )

                    message_timer = 180

                continue

            # ==================================================
            # الصندوق
            # ==================================================

            if box.collidepoint(
                game_pos
            ):

                if has_first_key:

                    box_open = True

                    has_note = True

                else:

                    message = (
                        "الصندوق مقفول... تحتاج إلى المفتاح الأول."
                    )

                    message_timer = 180

                continue

            # ==================================================
            # الباب
            # ==================================================

            if door.collidepoint(
                game_pos
            ):

                if has_second_key:

                    return "WIN"

                else:

                    message = (
                        "الباب مقفول... تحتاج إلى المفتاح الثاني."
                    )

                    message_timer = 180

        # ==================================================
        # الرسم الأساسي
        # ==================================================

        game_surface.fill(
            BLACK
        )

        # ==================================================
        # الحائط
        # ==================================================

        pygame.draw.rect(
            game_surface,
            WALL,
            (40, 40, 820, 410)
        )

        # ==================================================
        # الأرض
        # ==================================================

        pygame.draw.rect(
            game_surface,
            FLOOR,
            (40, 450, 820, 110)
        )

        # ==================================================
        # الباب
        # ==================================================

        pygame.draw.rect(
            game_surface,
            BROWN,
            door,
            border_radius=8
        )

        pygame.draw.rect(
            game_surface,
            (65, 40, 25),
            door,
            6,
            border_radius=8
        )

        pygame.draw.circle(
            game_surface,
            GOLD,
            (215, 315),
            9
        )

        # ==================================================
        # اللوحة
        # ==================================================

        if not board_moved:

            pygame.draw.rect(
                game_surface,
                BLACK,
                board,
                border_radius=10
            )

            pygame.draw.rect(
                game_surface,
                GOLD,
                board,
                4,
                border_radius=10
            )

            draw_arabic(
                game_surface,
                "2   4   6   ؟",
                normal_font,
                GOLD,
                board.center
            )

        else:

            # ----------------------------------------------
            # رسم اللوحة بعد زحزحتها
            # ----------------------------------------------

            pygame.draw.rect(
                game_surface,
                BLACK,
                moved_board,
                border_radius=10
            )

            pygame.draw.rect(
                game_surface,
                GOLD,
                moved_board,
                4,
                border_radius=10
            )

            draw_arabic(
                game_surface,
                "الرموز",
                normal_font,
                GOLD,
                moved_board.center
            )

            # ----------------------------------------------
            # المكان خلف اللوحة
            # ----------------------------------------------

            if not has_second_key:

                pygame.draw.rect(
                    game_surface,
                    (25, 25, 28),
                    hidden_key,
                    border_radius=8
                )

                draw_arabic(
                    game_surface,
                    "مفتاح",
                    tiny_font,
                    GOLD,
                    hidden_key.center
                )

            else:

                draw_arabic(
                    game_surface,
                    "تم أخذ المفتاح",
                    tiny_font,
                    GRAY,
                    hidden_key.center
                )

        # ==================================================
        # الصندوق
        # ==================================================

        pygame.draw.rect(
            game_surface,
            BROWN,
            box,
            border_radius=8
        )

        pygame.draw.rect(
            game_surface,
            GOLD,
            box,
            4,
            border_radius=8
        )

        if not has_first_key:

            pygame.draw.rect(
                game_surface,
                GOLD,
                (710, 380, 20, 35),
                border_radius=4
            )

        else:

            draw_arabic(
                game_surface,
                "صندوق",
                tiny_font,
                WHITE,
                box.center
            )

        # ==================================================
        # عنوان المرحلة
        # ==================================================

        draw_arabic(
            game_surface,
            "الغرفة الأولى",
            normal_font,
            WHITE,
            (450, 75)
        )

        # ==================================================
        # الرسالة
        # ==================================================

        if message_timer > 0:

            message_timer -= 1

            message_box = pygame.Rect(
                100,
                455,
                700,
                65
            )

            pygame.draw.rect(
                game_surface,
                (30, 30, 40),
                message_box,
                border_radius=12
            )

            pygame.draw.rect(
                game_surface,
                GOLD,
                message_box,
                2,
                border_radius=12
            )

            draw_arabic(
                game_surface,
                message,
                small_font,
                WHITE,
                message_box.center
            )

        # ==================================================
        # نافذة اللغز
        # ==================================================

        if puzzle_open:

            overlay = pygame.Surface(
                (GAME_W, GAME_H),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 185)
            )

            game_surface.blit(
                overlay,
                (0, 0)
            )

            panel = pygame.Rect(
                100,
                70,
                700,
                450
            )

            pygame.draw.rect(
                game_surface,
                (35, 35, 45),
                panel,
                border_radius=20
            )

            pygame.draw.rect(
                game_surface,
                GOLD,
                panel,
                4,
                border_radius=20
            )

            draw_arabic(
                game_surface,
                "اللغز الأول",
                title_font,
                WHITE,
                (450, 135)
            )

            draw_arabic(
                game_surface,
                "أكمل الرقم الناقص",
                normal_font,
                WHITE,
                (450, 205)
            )

            draw_arabic(
                game_surface,
                "2   ،   4   ،   6   ،   ؟",
                normal_font,
                GOLD,
                (450, 270)
            )

            for answer_rect, answer in answer_buttons:

                pygame.draw.rect(
                    game_surface,
                    BLUE,
                    answer_rect,
                    border_radius=12
                )

                pygame.draw.rect(
                    game_surface,
                    (130, 190, 255),
                    answer_rect,
                    2,
                    border_radius=12
                )

                draw_arabic(
                    game_surface,
                    answer,
                    normal_font,
                    WHITE,
                    answer_rect.center
                )

            draw_arabic(
                game_surface,
                "اختر الإجابة الصحيحة",
                tiny_font,
                GRAY,
                (450, 480)
            )

        # ==================================================
        # نافذة الورقة
        # ==================================================

        if box_open:

            overlay = pygame.Surface(
                (GAME_W, GAME_H),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 190)
            )

            game_surface.blit(
                overlay,
                (0, 0)
            )

            paper = pygame.Rect(
                150,
                70,
                600,
                430
            )

            pygame.draw.rect(
                game_surface,
                (235, 225, 190),
                paper,
                border_radius=12
            )

            pygame.draw.rect(
                game_surface,
                GOLD,
                paper,
                5,
                border_radius=12
            )

            draw_arabic(
                game_surface,
                "الورقة",
                title_font,
                (45, 40, 35),
                (450, 150)
            )

            pygame.draw.line(
                game_surface,
                (100, 90, 70),
                (220, 190),
                (680, 190),
                2
            )

            draw_arabic(
                game_surface,
                "دور تحت الرموز",
                title_font,
                (35, 35, 35),
                (450, 270)
            )

            draw_arabic(
                game_surface,
                "هناك شيء مخبأ خلف اللوحة.",
                small_font,
                (80, 75, 65),
                (450, 330)
            )

            close_note = pygame.Rect(
                330,
                410,
                240,
                65
            )

            pygame.draw.rect(
                game_surface,
                RED,
                close_note,
                border_radius=14
            )

            pygame.draw.rect(
                game_surface,
                WHITE,
                close_note,
                2,
                border_radius=14
            )

            draw_arabic(
                game_surface,
                "إغلاق الورقة",
                normal_font,
                WHITE,
                close_note.center
            )

        # ==================================================
        # التعليمات
        # ==================================================

        if not puzzle_open and not box_open:

            draw_arabic(
                game_surface,
                "اضغط على الأشياء للبحث عن الأدلة",
                small_font,
                WHITE,
                (450, 535)
            )

        # ==================================================
        # عرض اللعبة
        # ==================================================

        show_game()

        clock.tick(60)


# ==================================================
# تشغيل
# ==================================================

try:

    while True:

        result = menu()

        if not result:
            break

        result = game()

        if result == "WIN":

            again = win_screen()

            if not again:
                break

        else:

            break

finally:

    pygame.quit()