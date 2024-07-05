import turtle
import time
import random
import os
from PIL import Image
import copy


class puzzle_game_view:
    def __init__(self):
        self.width, self.height = 650, 650
        self.image_folder = os.path.join(
            "puzzle_resource", "Images", "your_name"
        )  # "./puzzle_resource/Images/mario"
        self.ui_folder = os.path.join(
            "puzzle_resource", "Resources"
        )  # "./puzzle_resource/Resources"
        self.thumb_gif_path = os.path.join(self.image_folder, "your_name_thumbnail.gif")
        self.splash_path = os.path.join(
            self.ui_folder, "splash_screen.gif"
        )  # "./puzzle_resource/Resources/splash_screen.gif"
        self.screen = turtle.Screen()
        self.splash = turtle.Turtle()  # create 'splash' Turtle instance
        self.ui = turtle.Turtle()  # create 'ui' Turtle instance
        self.name = "Hi there"
        self.moves = 0
        self.new_puzzle = ""

    def draw_rectangle(
        self, x: float, y: float, width: float, height: float, pen_color: str
    ):
        t = turtle.Turtle()
        t.pencolor(pen_color)
        t.speed(9)
        t.pensize(3)
        t.penup()
        t.goto(x, y)  # move to the left bottom vertex of the rectangle
        t.pendown()

        for _ in range(2):
            t.forward(width)
            t.left(90)
            t.forward(height)
            t.left(90)
        t.hideturtle()

    def draw_filled_rectangle(self, x: float, y: float, width: float, height: float):
        t = turtle.Turtle()
        t.pencolor("pale green")
        t.speed(9)
        bg_color = "pale green"

        # 绘制背景矩形
        t.penup()
        t.goto(x, y)  # upper left corner
        t.pendown()
        t.fillcolor(bg_color)
        t.begin_fill()
        for _ in range(2):
            t.forward(width)  # 文本框的宽度
            t.right(90)
            t.forward(height)  # 文本框的高度
            t.right(90)
        t.end_fill()

    def show_pic(
        self, pic_path: str, x: float, y: float
    ):  # x, y are the central of this pic

        t = turtle.Turtle()
        turtle.addshape(pic_path)  # add gif from outside
        stretch_wid, stretch_len, _ = (
            t.shapesize()
        )  # get the streched wid andlen of gif

        # calculate actual pic size
        width = stretch_len * 20  # default factor=20
        height = stretch_wid * 20
        center_x = x - width / 2
        center_y = y - height / 2
        t.speed(8)
        t.penup()
        t.goto(center_x, center_y)
        t.pendown()
        t.shape(pic_path)  # show the gif

    def write_words_down(
        self, words: str, fontsize: float, x: float, y: float
    ):  # x, y are the left-bottom of this text
        t = turtle.Turtle()
        font = ("Times New Roman", fontsize, "normal")  # set font
        t.speed(8)
        t.penup()
        t.goto(x, y)  # set the upper_left vertex of the text
        t.pendown()
        t.write(words, align="left", font=font)
        t.hideturtle()

    def initialization(self):
        self.screen.setup(self.width, self.height)  # set screen size
        self.screen.bgcolor("pale green")  # set backgroound color

    def splash_screen(self):
        turtle.addshape(self.splash_path)
        self.splash.shape(self.splash_path)  # display splash
        time.sleep(3)  # show splash for 3 s
        self.splash.hideturtle()  # clear screen

    def get_name(self):  # get the name of the player
        popup_window = turtle.Screen()
        self.name = popup_window.textinput("CS5001 Puzzle Slide", "Your Name")

    def get_new_puzzle(self):  # get a new puzzle name for loading
        popup_window = turtle.Screen()
        prompt_text = (
            "Choose from the following puzzle\nfifteen\nluigi\nmario\nyour_name\nyoshi"
        )
        self.new_puzzle = popup_window.textinput("CS5001 Puzzle Slide", prompt_text)

    def get_moves(self):
        popup_window = turtle.Screen()
        while self.moves < 5 or self.moves > 200:
            self.moves = int(
                popup_window.textinput(
                    "CS5001 Puzzle Slide", "Enter the number of moves (5-200)."
                )
            )

    def draw_UI(self):
        self.draw_rectangle(-260, -130, 325, 390, "black")  # draw main puzzle part
        self.draw_rectangle(-260, -260, 520, 65, "black")  # draw button and move part
        self.draw_rectangle(130, -130, 130, 390, "blue")  # draw player part

        self.show_pic(
            os.path.join(self.ui_folder, "resetbutton.gif"), 13, -227.5
        )  # reset button
        self.show_pic(
            os.path.join(self.ui_folder, "loadbutton.gif"), 104, -222.5
        )  # load button
        self.show_pic(
            os.path.join(self.ui_folder, "quitbutton.gif"), 195, -217.5
        )  # quit button
        self.show_pic(self.thumb_gif_path, 260, 260)  # origin thumb pic

        self.write_words_down("Player:", 20, 162.5, 170)  # 'Player' text
        self.write_words_down(self.name, 18, 162.5, 137.5)  # player's name
        self.write_words_down(
            "Players move: 0", 16, -227.5, -240
        )  # "Players move:" text

    def draw_16_rectangle(self, vertices: list):
        # draw 16 puzzles part
        begin_vertex = vertices
        for i in range(4):
            for j in range(4):
                self.draw_rectangle(
                    begin_vertex[i][j][0], begin_vertex[i][j][1], 65, 65, "black"
                )

    def draw_16_rectangle_filled(self, vertices: list):
        # draw 16 puzzles part
        begin_vertex = vertices
        for i in range(3):
            for j in range(4):
                self.draw_filled_rectangle(
                    begin_vertex[i][j][0], begin_vertex[i][j][1], 65, 65
                )

    def draw_split_puzzles(self, puzzle_sequence, pic_mid):
        for i in range(4):
            for j in range(4):
                if (puzzle_sequence[i][j]) == None:  # pass the None case
                    cur_img_path = os.path.join(self.image_folder, "blank.gif")
                    image = Image.open(cur_img_path)  # Open the image
                    resized_image = image.resize((52, 52))  # Resize the image
                    temp_path = "resized_temp_" + str(puzzle_sequence[i][j]) + ".gif"
                    resized_image.save(
                        temp_path
                    )  # Save the resized image to a temporary file
                    self.show_pic(temp_path, pic_mid[i][j][0], pic_mid[i][j][1])
                    continue

                cur_img_path = os.path.join(
                    self.image_folder, str(puzzle_sequence[i][j]) + ".gif"
                )
                image = Image.open(cur_img_path)  # Open the image
                resized_image = image.resize((52, 52))  # Resize the image
                temp_path = "resized_temp_" + str(puzzle_sequence[i][j]) + ".gif"
                resized_image.save(
                    temp_path
                )  # Save the resized image to a temporary file

                self.show_pic(temp_path, pic_mid[i][j][0], pic_mid[i][j][1])

    def draw_split_puzzles_9(self, puzzle_sequence: list, pic_mid: list):
        for i in range(3):
            for j in range(3):
                if (puzzle_sequence[i][j]) == None:  # pass the None case
                    temp_path = "resized_temp_None.gif"
                    self.show_pic(temp_path, pic_mid[i][j][0], pic_mid[i][j][1])
                    continue

                cur_img_path = os.path.join(
                    self.image_folder, str(puzzle_sequence[i][j]) + ".gif"
                )
                image = Image.open(cur_img_path)  # Open the image
                resized_image = image.resize((52, 52))  # Resize the image
                temp_path = "resized_temp_" + str(puzzle_sequence[i][j]) + ".gif"
                resized_image.save(
                    temp_path
                )  # Save the resized image to a temporary file

                self.show_pic(temp_path, pic_mid[i][j][0], pic_mid[i][j][1])

    def draw_split_puzzles_4(self, puzzle_sequence, pic_mid):
        for i in range(2):
            for j in range(2):
                if (puzzle_sequence[i][j]) == None:  # pass the None case
                    temp_path = "resized_temp_None.gif"
                    self.show_pic(temp_path, pic_mid[i][j][0], pic_mid[i][j][1])
                    continue

                cur_img_path = os.path.join(
                    self.image_folder, str(puzzle_sequence[i][j]) + ".gif"
                )
                image = Image.open(cur_img_path)  # Open the image
                resized_image = image.resize((52, 52))  # Resize the image
                temp_path = "resized_temp_" + str(puzzle_sequence[i][j]) + ".gif"
                resized_image.save(
                    temp_path
                )  # Save the resized image to a temporary file

                self.show_pic(temp_path, pic_mid[i][j][0], pic_mid[i][j][1])


class puzzle_game_controller:
    def __init__(self):
        self.view = puzzle_game_view()
        self.model = puzzle_game_model()

        self.vertices = self.model.get_16_puzzle_begin_vertex()
        self.puzzle_sequence = self.model.generate_solvable_puzzle()
        self.changed_num = self.model.find_missing_number(
            self.puzzle_sequence
        )  # changed num, i.e. 1 of the number of 1 to 16
        self.ordered_sequence, self.ordered_None_x, self.ordered_None_y = (
            self.model.get_ordered_sequence(self.changed_num)
        )
        [self.cur_blank_x, self.cur_blank_y] = self.model.find_None_loc(
            self.puzzle_sequence
        )  # current blank loc of the puzzle_sequence
        self.around_None_index, self.around_None_loc = (
            self.model.find_index_loc_around_None(self.cur_blank_x, self.cur_blank_y)
        )  # get current blank index and loc, i.e. [[3, 2], [2, 3]], [[10, 42.5], [-55, -22.5]]
        self.actual_move = 0

        self.view.initialization()
        self.view.splash_screen()
        self.view.get_name()
        self.view.get_moves()
        self.view.draw_UI()
        self.view.draw_16_rectangle(self.vertices)
        self.view.draw_split_puzzles(
            self.puzzle_sequence, self.model.get_16_puzzle_pic_mid()
        )
        self.view.screen.onclick(self.on_click)

    def on_click(self, x, y):
        # the block around the None
        a1 = [-185, 172.5]  # first mid of the puzzle starts here
        for index, loc in enumerate(self.around_None_loc):  # i.e. loc = [10, 42.5]
            # pixel of every split fig is 52 * 52
            if abs(x - loc[0]) <= 26 and abs(y - loc[1]) <= 26:
                none_path = os.path.join("resized_temp_None.gif")
                puzzle_sequence_index = self.around_None_index[index]  # i.e. [3, 2]
                switch_pic_num = self.puzzle_sequence[puzzle_sequence_index[0]][
                    puzzle_sequence_index[1]
                ]  # i.e. 7
                switch_pic_path = "resized_temp_" + str(switch_pic_num) + ".gif"
                self.view.show_pic(none_path, loc[0], loc[1])
                self.view.show_pic(
                    switch_pic_path,
                    a1[0] + 65 * self.cur_blank_y,
                    a1[1] - 65 * self.cur_blank_x,
                )

                self.actual_move += 1  # change the actual move

                # reset the current puzzle sequence == switch the click part num and None
                self.puzzle_sequence[puzzle_sequence_index[0]][
                    puzzle_sequence_index[1]
                ] = None  # None part
                self.puzzle_sequence[self.cur_blank_x][
                    self.cur_blank_y
                ] = switch_pic_num  # click part num

                [self.cur_blank_x, self.cur_blank_y] = (
                    puzzle_sequence_index  # change the blank loc
                )
                self.around_None_index, self.around_None_loc = (
                    self.model.find_index_loc_around_None(
                        self.cur_blank_x, self.cur_blank_y
                    )
                )  # relocate the around None index and loc

                # state the player's actual move
                self.view.draw_filled_rectangle(-245, -200, 190, 45)  # refill that part
                self.view.write_words_down(
                    "Players move: " + str(self.actual_move), 16, -227.5, -240
                )

                # check win status first
                if self.puzzle_sequence == self.ordered_sequence:
                    win_pic_path = os.path.join(self.view.ui_folder, "winner.gif")
                    self.view.show_pic(win_pic_path, 0, 0)
                    continue

                # check the lose status
                if self.actual_move > self.view.moves:
                    lose_pic_path = os.path.join(self.view.ui_folder, "Lose.gif")
                    self.view.show_pic(lose_pic_path, 0, 0)

        # (13, -227.5) reset button
        if abs(x - 13) <= 42 and abs(y + 227.5) <= 42:
            self.cur_blank_x, self.cur_blank_y = (
                self.ordered_None_x,
                self.ordered_None_y,
            )  # set the current blank index
            self.around_None_index, self.around_None_loc = (
                self.model.find_index_loc_around_None(
                    self.cur_blank_x, self.cur_blank_y
                )
            )  # relocate the around None index and loc
            self.puzzle_sequence = copy.deepcopy(
                self.ordered_sequence
            )  # reset the current puzzle sequence
            if len(self.puzzle_sequence) == 4:  # 4 * 4 puzzle
                self.view.draw_split_puzzles(
                    self.puzzle_sequence, self.model.get_16_puzzle_pic_mid()
                )
            elif len(self.puzzle_sequence) == 3:  # 3 *3 puzzle
                self.view.draw_split_puzzles_9(
                    self.ordered_sequence, self.model.get_9_puzzle_pic_mid()
                )
            elif len(self.puzzle_sequence) == 2:  # 2 * 2 puzzle
                self.view.draw_split_puzzles_4(
                    self.ordered_sequence, self.model.get_4_puzzle_pic_mid()
                )

        # (104, -222.5) load button
        if abs(x - 104) <= 42 and abs(y + 222.5) <= 40:
            self.actual_move = 0  # reset player's actual move
            # reset view of the player's actual move
            self.view.draw_filled_rectangle(-245, -200, 190, 45)  # refill that part
            self.view.write_words_down("Players move: 0", 16, -227.5, -240)

            # get a workable file name
            while True:
                try:
                    self.view.get_new_puzzle()  # get new puz name from player
                    # show the new thumb pic
                    self.view.image_folder = os.path.join(
                        "puzzle_resource", "Images", self.view.new_puzzle
                    )  # reset the image folder i.e. "./puzzle_resource/Images/mario"
                    thumb_gif_file = (
                        self.view.new_puzzle + "_thumbnail.gif"
                    )  # "mario_thumbnail.gif"
                    self.view.thumb_gif_path = os.path.join(
                        self.view.image_folder, thumb_gif_file
                    )  # reset the thumb pic path

                    _ = Image.open(self.view.thumb_gif_path)  # check file readability
                    break
                except Exception as e:
                    error_pic_path = os.path.join(self.view.ui_folder, "file_error.gif")
                    self.view.show_pic(error_pic_path, 0, 0)
                    time.sleep(3)

            self.view.show_pic(
                self.view.thumb_gif_path, 260, 260
            )  # show that thumb pic
            # draw all 16 blank
            self.view.draw_16_rectangle_filled(self.vertices)

            cur_file_num = self.model.count_files_in_folder(self.view.image_folder)
            if cur_file_num == 18 or cur_file_num == 34:  # puzzle size 4 * 4
                self.view.draw_split_puzzles(
                    self.puzzle_sequence, self.model.get_16_puzzle_pic_mid()
                )

            elif cur_file_num == 11 or cur_file_num == 20:  # puzzle size 3 * 3
                # self.view.draw_split_puzzles_None(self.model.get_16_puzzle_pic_mid())
                self.puzzle_sequence = self.model.generate_solvable_puzzle_9()
                self.changed_num = self.model.find_missing_number(
                    self.puzzle_sequence
                )  # changed num, i.e. 1 of the number of 1 to 9
                self.ordered_sequence, self.ordered_None_x, self.ordered_None_y = (
                    self.model.get_ordered_sequence_9(self.changed_num)
                )
                self.view.draw_split_puzzles_9(
                    self.puzzle_sequence, self.model.get_9_puzzle_pic_mid()
                )

                [self.cur_blank_x, self.cur_blank_y] = self.model.find_None_loc(
                    self.puzzle_sequence
                )  # current blank loc of the puzzle_sequence

                self.around_None_index, self.around_None_loc = (
                    self.model.find_index_loc_around_None(
                        self.cur_blank_x, self.cur_blank_y
                    )
                )  # get current blank index and loc, i.e. [[3, 2], [2, 3]], [[10, 42.5], [-55, -22.5]]

            elif cur_file_num == 6 or cur_file_num == 10:  # puzzle size 2 * 2
                # self.view.draw_split_puzzles_None(self.model.get_16_puzzle_pic_mid())
                self.puzzle_sequence = self.model.generate_solvable_puzzle_4()
                self.changed_num = self.model.find_missing_number(
                    self.puzzle_sequence
                )  # changed num, i.e. 1 of the number of 1 to 4
                self.ordered_sequence, self.ordered_None_x, self.ordered_None_y = (
                    self.model.get_ordered_sequence_4(self.changed_num)
                )
                self.view.draw_split_puzzles_4(
                    self.puzzle_sequence, self.model.get_4_puzzle_pic_mid()
                )

                [self.cur_blank_x, self.cur_blank_y] = self.model.find_None_loc(
                    self.puzzle_sequence
                )  # current blank loc of the puzzle_sequence

                self.around_None_index, self.around_None_loc = (
                    self.model.find_index_loc_around_None(
                        self.cur_blank_x, self.cur_blank_y
                    )
                )  # get current blank index and loc, i.e. [[3, 2], [2, 3]], [[10, 42.5], [-55, -22.5]]

        # (195, -217.5) quit button
        if abs(x - 195) <= 42 and abs(y + 217.5) <= 30:
            turtle.bye()


class puzzle_game_model:
    @staticmethod
    def generate_solvable_puzzle():
        # initialization, including 1 to 15 and a None
        puzzle = list(range(1, 16)) + [None]
        random.shuffle(puzzle)  # shuffle the puzzle

        # calculate the inversion of the puzzle
        inversions = sum(
            sum(
                (puzzle[j] > puzzle[i])
                for j in range(i + 1, 16)
                if puzzle[i] is not None and puzzle[j] is not None
            )
            for i in range(15)
        )

        # if the inversion is odd, switch the last two element to make it even
        if inversions % 2 != 0:
            puzzle[-1], puzzle[-2] = puzzle[-2], puzzle[-1]

        # wrap up the puzzle to
        puzzle_sequence = []
        for i in range(0, 16, 4):
            puzzle_sequence.append(puzzle[i : i + 4])

        for i in range(4):
            for j in range(4):
                if puzzle_sequence[i][j] == None:
                    try:
                        puzzle_sequence[i][j + 1] = None
                        puzzle_sequence[i][j] = 16
                        break
                    except Exception as e:
                        break

        return puzzle_sequence

    @staticmethod
    def generate_solvable_puzzle_9():
        # initialization, including 1 to 8 and a None
        puzzle = list(range(1, 9)) + [None]
        random.shuffle(puzzle)  # shuffle the puzzle

        # calculate the inversion of the puzzle
        inversions = sum(
            sum(
                (puzzle[j] > puzzle[i])
                for j in range(i + 1, 9)
                if puzzle[i] is not None and puzzle[j] is not None
            )
            for i in range(8)
        )

        # if the inversion is odd, switch the last two element to make it even
        if inversions % 2 != 0:
            puzzle[-1], puzzle[-2] = puzzle[-2], puzzle[-1]

        # wrap up the puzzle to
        puzzle_sequence = []
        for i in range(0, 9, 3):
            puzzle_sequence.append(puzzle[i : i + 3])

        for i in range(3):
            for j in range(3):
                if puzzle_sequence[i][j] == None:
                    try:
                        puzzle_sequence[i][j + 1] = None
                        puzzle_sequence[i][j] = 9
                        break
                    except Exception as e:
                        break

        return puzzle_sequence

    @staticmethod
    def generate_solvable_puzzle_4():
        # initialization, including 1 to 3 and a None
        puzzle = list(range(1, 4)) + [None]
        random.shuffle(puzzle)  # shuffle the puzzle

        # calculate the inversion of the puzzle
        inversions = sum(
            sum(
                (puzzle[j] > puzzle[i])
                for j in range(i + 1, 4)
                if puzzle[i] is not None and puzzle[j] is not None
            )
            for i in range(3)
        )

        # if the inversion is odd, switch the last two element to make it even
        if inversions % 2 != 0:
            puzzle[-1], puzzle[-2] = puzzle[-2], puzzle[-1]

        # wrap up the puzzle to
        puzzle_sequence = []
        for i in range(0, 4, 2):
            puzzle_sequence.append(puzzle[i : i + 2])

        for i in range(2):
            for j in range(2):
                if puzzle_sequence[i][j] == None:
                    try:
                        puzzle_sequence[i][j + 1] = None
                        puzzle_sequence[i][j] = 4
                        break
                    except Exception as e:
                        break

        return puzzle_sequence

    @staticmethod
    def get_16_puzzle_begin_vertex():
        a1 = [-227.5, 130]  # first vertex of the puzzle starts here
        res = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                cur_pos = a1.copy()
                cur_pos[0] = cur_pos[0] + 65 * j
                cur_pos[1] = cur_pos[1] - 65 * i
                res[i].append(cur_pos)
        return res

    @staticmethod
    def get_16_puzzle_pic_mid():
        a1 = [-185, 172.5]  # first mid of the puzzle starts here
        res = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                cur_pos = a1.copy()
                cur_pos[0] = cur_pos[0] + 65 * j
                cur_pos[1] = cur_pos[1] - 65 * i
                res[i].append(cur_pos)
        return res

    @staticmethod
    def get_9_puzzle_pic_mid():
        a1 = [-185, 172.5]  # first mid of the puzzle starts here
        res = [[], [], []]
        for i in range(3):
            for j in range(3):
                cur_pos = a1.copy()
                cur_pos[0] = cur_pos[0] + 65 * j
                cur_pos[1] = cur_pos[1] - 65 * i
                res[i].append(cur_pos)
        return res

    @staticmethod
    def get_4_puzzle_pic_mid():
        a1 = [-185, 172.5]  # first mid of the puzzle starts here
        res = [[], []]
        for i in range(2):
            for j in range(2):
                cur_pos = a1.copy()
                cur_pos[0] = cur_pos[0] + 65 * j
                cur_pos[1] = cur_pos[1] - 65 * i
                res[i].append(cur_pos)
        return res

    @staticmethod
    def find_missing_number(nested_list: list):
        full_set = set(range(1, 17))  # create a set from 1 to 16
        actual_numbers = set()

        # iterate the nested list
        for sublist in nested_list:
            for num in sublist:
                if num is not None:
                    actual_numbers.add(num)

        # use set minus to find the lost number
        missing_number = full_set - actual_numbers
        return missing_number.pop() if missing_number else None

    @staticmethod
    def find_None_loc(nested_list: list):
        for i, sublist in enumerate(nested_list):
            for j, num in enumerate(sublist):
                if num is None:
                    return [i, j]

    @staticmethod
    def find_index_loc_around_None(cur_blank_x: int, cur_blank_y: int):
        res_index, res_loc = [], []
        a1 = [-185, 172.5]  # first mid of the puzzle starts here

        if cur_blank_y >= 1:  # check upper_box
            upper_box = [cur_blank_x, cur_blank_y - 1]
            upper_box_loc = [a1[0] + 65 * upper_box[1], a1[1] - 65 * upper_box[0]]
            res_index.append(upper_box)
            res_loc.append(upper_box_loc)

        if cur_blank_y <= 2:  # check down_box
            down_box = [cur_blank_x, cur_blank_y + 1]
            down_box_loc = [a1[0] + 65 * down_box[1], a1[1] - 65 * down_box[0]]
            res_index.append(down_box)
            res_loc.append(down_box_loc)

        if cur_blank_x >= 1:  # check left_box
            left_box = [cur_blank_x - 1, cur_blank_y]
            left_box_loc = [a1[0] + 65 * left_box[1], a1[1] - 65 * left_box[0]]
            res_index.append(left_box)
            res_loc.append(left_box_loc)

        if cur_blank_x <= 2:  # check right_box
            right_box = [cur_blank_x + 1, cur_blank_y]
            right_box_loc = [a1[0] + 65 * right_box[1], a1[1] - 65 * right_box[0]]
            res_index.append(right_box)
            res_loc.append(right_box_loc)

        return res_index, res_loc

    @staticmethod
    def get_ordered_sequence(changed_num):
        ordered_sequence = [[], [], [], []]
        num = 1
        # get the ordered list from 1 to 16
        for i in range(4):
            for j in range(4):
                ordered_sequence[i].append(num)
                num += 1
        # self.changed_num is the changed to None number
        i = changed_num // 4
        j = changed_num % 4 - 1
        if j == -1:
            i -= 1
            j = 3
        ordered_sequence[i][j] = None  # set the chenged to None num to None
        return ordered_sequence, i, j

    @staticmethod
    def get_ordered_sequence_9(changed_num):
        ordered_sequence = [[], [], []]
        num = 1
        # get the ordered list from 1 to 9
        for i in range(3):
            for j in range(3):
                ordered_sequence[i].append(num)
                num += 1
        # self.changed_num is the changed to None number
        i = changed_num // 3
        j = changed_num % 3 - 1
        if j == -1:
            i -= 1
            j = 2
        ordered_sequence[i][j] = None  # set the chenged to None num to None
        return ordered_sequence, i, j

    @staticmethod
    def get_ordered_sequence_4(changed_num):
        ordered_sequence = [[], []]
        num = 1
        # get the ordered list from 1 to 4
        for i in range(2):
            for j in range(2):
                ordered_sequence[i].append(num)
                num += 1
        # self.changed_num is the changed to None number
        i = changed_num // 2
        j = changed_num % 2 - 1
        if j == -1:
            i -= 1
            j = 1
        ordered_sequence[i][j] = None  # set the chenged to None num to None
        return ordered_sequence, i, j

    @staticmethod
    def count_files_in_folder(folder_path):
        count = 0
        for _, _, files in os.walk(folder_path):
            count += len(files)
        return count


def main():
    puzzle = puzzle_game_controller()
    turtle.mainloop()


if __name__ == "__main__":
    main()
