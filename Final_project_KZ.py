import turtle
import random
import time
from datetime import datetime

bg = turtle.Screen()

frame_pen = turtle.Turtle()
frame_pen.speed(0)

tile_boarder = turtle.Turtle()
tile_boarder.speed(0)
tile_boarder.ht()

stamp = turtle.Turtle()
stamp.speed(0)
stamp.ht()

icons = turtle.Turtle()
icons.speed(0)
icons.ht()

move_num = 0   #number of moves

THUMB_X = 295    #x coordinate of where thumbnail image is going to be placed
THUMB_Y = 320    #y coordinate of where thumbnail image is going to be placed

BOARDER_INI_X = -319 #x coord of where tile boarder is going to be drew
BOARDER_INI_Y = 289  #y coord of where tile boarder is going to be drew

TILE_INI_X = -270  #x coord of where tile is going to be placed
TILE_INI_Y = 240  #y coord of where tile is going to be placed


def draw_square(tool, x, y, length, width, color, size):
    '''
    Function: This function draws squares with turtle 'tool' at coordinate
              (x,y) with specified length and width. Color and size of pen
              can also be specified.
    Parameter: turtle name, x,y coordinate of where you want to start drawing
                the square, the length and width of the square, the color and
                size of pen
    Return: none
    '''
    tool.st()
    tool.color(color)
    tool.pensize(size)
    tool.penup()
    tool.goto(x,y)
    tool.down()
    for i in range(4):
        tool.forward(length)
        tool.right(90)
        tool.forward(width)
        tool.right(90)
        
    tool.ht()

def stamp_pic(tool, x, y, image):
    '''
    Function: This function helps stamp images on to turtle screen at
              coordinate x,y
    Parameter: turtle name, x,y coordinate, image name
    Return: none
    '''
    tool.st()
    tool.penup()
    tool.goto(x, y)
    tool.shape(image)
    tool.stamp()
    tool.ht()
    
def load_resources():
    '''
    Function: This function helps load images into background before stamping
    Parameter: none
    Return: none
    '''
    bg.addshape('Resources/quitbutton.gif')
    bg.addshape('Resources/loadbutton.gif')
    bg.addshape('Resources/resetbutton.gif')

    bg.addshape('Resources/Lose.gif')
    bg.addshape('Resources/credits.gif')
    bg.addshape('Resources/file_error.gif')
    bg.addshape('Resources/file_warning.gif')
    
    
    bg.addshape('Resources/leaderboard_error.gif')
    bg.addshape('Resources/quit.gif')
    bg.addshape('Resources/quitmsg.gif')
    bg.addshape('Resources/splash_screen.gif')
    bg.addshape('Resources/winner.gif')
    
def tile_num_calc(col, row, tpr):

    '''
    Function: This function helps to calculate the tile number given the
              column and row number, and tile per row number
    Parameter: column number, and row number of the tile, and number of
                tiles per row 
    Return: tile number
    '''
    tile_number = col + row * tpr
    return tile_number

###############################################################################
def board():
    '''
    Function: This function helps to initialize the game board
    Parameter: none
    Return: none
    '''
    bg.addshape('Resources/splash_screen.gif')
    frame_pen.shape('Resources/splash_screen.gif')
    time.sleep(2)
    frame_pen.shape('classic')

    name = turtle.textinput('name', 'What is your name?')
    num_step = turtle.numinput('steps',
                               'Enter the number of moves you want (5-200)',
                               minval = 5, maxval = 200)
    
    bg.bgcolor('yellow')
    bg.screensize(800, 800)
    bg.tracer(0)
    draw_square(frame_pen, -400, 400, 800, 800, 'black', 1)
    draw_square(frame_pen, -350, 350, 460, 520, 'black', 5)
    draw_square(frame_pen, -350, -230, 700, 120, 'black', 5)
    draw_square(frame_pen, 130, 350, 220, 520, 'blue', 5)
    load_resources()

    #append 3 buttons onto the board
    stamp_pic(icons, 290, -290, 'Resources/quitbutton.gif')
    stamp_pic(icons, 200, -290, 'Resources/loadbutton.gif')
    stamp_pic(icons, 110, -290, 'Resources/resetbutton.gif')
    
    game_select = 'mario'
    frame_pen.st()
    frame_pen.penup()
    frame_pen.goto(150, 270)
    frame_pen.pendown()
    style = ('Arial', 25)
    frame_pen.write('Leaders: ', font = style, align = 'left')
    frame_pen.ht()

    move_num_pen = turtle.Turtle()
    move_num_pen.speed(0)
    move_num_pen.ht()

    def leader():
        '''
        Function: This function helps to open leaderboard file, sort 
                 players by their number of steps and display the top 8
                 players to the leader section of the board.
                 If the leaderboard file does not exist, it will generate
                 an error message automatically
        Parameter: none
        Return: none
        '''
        try:
            with open('leaderboard.txt', mode = 'r') as infile:
                line = infile.readlines()
                leader_list = []
                
                for i in range(len(line)):
                    line[i] = line[i].strip('\n')
                    a,b = line[i].split(': ')
                    a = int(a)
                    leader_list.append([a,b])
                leader_list.sort(key = lambda x: x[0])
                
                if len(line) >= 8:
                    for i in range(8):
                        frame_pen.st()
                        frame_pen.penup()
                        frame_pen.goto(150, 270 - 30* (i+1))
                        frame_pen.pendown()
                        style2 = ('Arial', 20)
                        frame_pen.write(
                            f'{leader_list[i][0]}: {leader_list[i][1]}',
                            font = style2, align = 'left')
                        frame_pen.ht()

                else:
                    for i in range(len(line)):
                        frame_pen.st()
                        frame_pen.penup()
                        frame_pen.goto(150, 270 - 30* (i+1))
                        frame_pen.pendown()
                        style2 = ('Arial', 20)
                        frame_pen.write(
                            f'{leader_list[i][0]}: {leader_list[i][1]}',
                            font = style2, align = 'left')
                        frame_pen.ht()
  
        except OSError:
            stamp_pic(stamp, 0, 0, 'Resources/file_error.gif')
            bg.update()
            time.sleep(2)
            stamp.clearstamps(-1)
            
            error = 'Error: Could not open leaderboard.txt. Location: leader()'
            now = datetime.now()
            time_now = now.strftime("%m/%d/%Y %H:%M:%S")
            day = now.strftime('%a')

            with open('5001_puzzle.err', mode='a') as outfile:
                outfile.write(day + ' ' + time_now + ' ' + error +'\n')
            

    def tile(puz):
        '''
        Function: this function append randomized puzzle images to game board,
                 draws a boarder of each puzzle tile before attaching image
        Parameter: puzzle name
        Return: none
        '''
        info_list = []
        puz_tile_name_list = []

        tile_dict = {}
        tile_random_dict = {}

        with open(f'{puz}.puz',mode = 'r') as infile:
            info = infile.readlines()[:4]
            for i in range(len(info)):
                info[i] = info[i].strip('\n')
                m,n = info[i].split(': ')
                info_list.append(n)
            puz_name = info_list[0] #puzzle name
            puz_num = info_list[1] #number of tiles
            puz_size = info_list[2] #size of each tile
            puz_thumb_name = info_list[3] #thumbnail name
        
        with open(f'{puz}.puz',mode = 'r') as infile:
            line = infile.readlines()[4:]
            for i in range(len(line)):
                line[i] = line[i].strip('\n')
                m,n = line[i].split(': ')
                r,s,t = n.split('/')
                x,y = t.split('.')
                puz_tile_name_list.append(x)
                
        puz_num = int(puz_num)

        for i in range(puz_num):
            bg.addshape(f'Images/{puz}/{puz_tile_name_list[i]}.gif')
        bg.addshape(puz_thumb_name)

        #randomize puzzle tile name list
        random_puz_tile_name_list = random.sample(puz_tile_name_list,
                                                  len(puz_tile_name_list))

        # decide the number of tiles per row based on the puzzle tile number
        if puz_num == 16:
            tile_per_row = 4
        elif puz_num == 9:
            tile_per_row = 3
        elif puz_num == 4:
            tile_per_row = 2

        #generate dictionary of puzzle name in original order
        for i in range(len(puz_tile_name_list)):
            tile_dict[i] = puz_tile_name_list[i]
            
        #generate dictionary of puzzle name in random order
        for i in range(len(random_puz_tile_name_list)):
            tile_random_dict[i] = random_puz_tile_name_list[i]

        #start placing tiles to gameboard in random order
        for i,j in tile_random_dict.items():
            draw_square(tile_boarder,
                        (BOARDER_INI_X + 100 * (i % tile_per_row)),
                        (BOARDER_INI_Y - 100 * (i//tile_per_row)), 98, 98,
                        'black', 1)
            stamp_pic(stamp, (TILE_INI_X + 100 * (i % tile_per_row)),
                      (TILE_INI_Y - 100 * ( i // tile_per_row )),
                      f'Images/{puz}/{j}.gif')
        stamp_pic(stamp, THUMB_X, THUMB_Y, puz_thumb_name)
        
        def handle_click(x,y):
            '''
            Function: This function helps to recognize where users clicked on
                      gameboard and carry out the corresponding action.
                      Each time when user clicked on the screen, we determine
                      where the blank tile locate and decide which tiles around
                      it could be switchable.
                      If user click any switchable tiles, switch position of
                      blank with tile clicked. If user did not click on
                      switchable tiles, do nothing.
                      Everytime a switch was performed, check if puzzle has
                      been solved or not. If solved, show winner image and
                      close game.
                      Record the number of moves as player plays.
                      When users run out of number of moves, show the lose image
                      and close turtle.
                      When user click on reset, quit, load button, carry out
                      corresponding task.
            Parameter: x, y coordinate
            Return: none
            '''
            switchable_tile_num = [] # list of tile num that can is switchable
            global move_num 

            #if click within tile region
            if x >= BOARDER_INI_X and x <= BOARDER_INI_X + 100 * (tile_per_row)\
               and\
            y <= BOARDER_INI_Y and y >= BOARDER_INI_Y - 100 * (tile_per_row):

                #determine the row number and column num of tile clicked
                click_col_num = int((x - BOARDER_INI_X ) // 100)
                click_row_num = int((BOARDER_INI_Y - y) // 100)

                tile_clicked = tile_num_calc(click_col_num, click_row_num,
                                             tile_per_row)

                #determine column and row number of blank tile
                for i,j in tile_random_dict.items():          
                    if j == 'blank':
                        blank_num = i
                '''
            formula of col and row number of tile that are on the left,
            right, up, down to the blank tile
                '''
                blank_col_num = blank_num % tile_per_row
                blank_row_num = blank_num // tile_per_row

                blank_left_row_num = blank_row_num
                blank_left_col_num = blank_col_num - 1

                blank_right_row_num = blank_row_num
                blank_right_col_num = blank_col_num + 1

                blank_up_row_num = blank_row_num - 1
                blank_up_col_num = blank_col_num

                blank_down_row_num = blank_row_num + 1
                blank_down_col_num = blank_col_num


                '''
            applying the game rule:
            if blank tile is in any place of the board, which tiles could switch
            with the blank tile
            
                '''
                if blank_col_num == 0:
                    if blank_row_num == 0:
                        switchable_tile_num.append(
                            tile_num_calc(blank_right_col_num,
                                          blank_right_row_num, tile_per_row)) 
                        switchable_tile_num.append(
                            tile_num_calc(blank_down_col_num,
                                          blank_down_row_num, tile_per_row))
                    elif blank_row_num == tile_per_row - 1:
                        switchable_tile_num.append(
                            tile_num_calc(blank_right_col_num,
                                          blank_right_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_up_col_num, blank_up_row_num,
                                          tile_per_row))
                    else:
                        switchable_tile_num.append(
                            tile_num_calc(blank_right_col_num,
                                          blank_right_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_up_col_num, blank_up_row_num,
                                          tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_down_col_num,
                                          blank_down_row_num, tile_per_row))
                
                elif blank_col_num == tile_per_row - 1:
                    if blank_row_num == 0:
                        switchable_tile_num.append(
                            tile_num_calc(blank_left_col_num,
                                          blank_left_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_down_col_num,
                                          blank_down_row_num, tile_per_row))
                    elif blank_row_num == tile_per_row - 1:
                        switchable_tile_num.append(
                            tile_num_calc(blank_left_col_num,
                                          blank_left_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_up_col_num,
                                          blank_up_row_num, tile_per_row))
                    else:
                        switchable_tile_num.append(
                            tile_num_calc(blank_left_col_num,
                                          blank_left_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_up_col_num,
                                          blank_up_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_down_col_num,
                                          blank_down_row_num, tile_per_row))
                else:
                    if blank_row_num == 0:
                        switchable_tile_num.append(
                            tile_num_calc(blank_left_col_num,
                                          blank_left_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_right_col_num,
                                          blank_right_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_down_col_num,
                                          blank_down_row_num, tile_per_row))
                    elif blank_row_num == tile_per_row - 1:
                        switchable_tile_num.append(
                            tile_num_calc(blank_left_col_num,
                                          blank_left_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_right_col_num,
                                          blank_right_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_up_col_num, blank_up_row_num,
                                          tile_per_row))
                    else:
                        switchable_tile_num.append(
                            tile_num_calc(blank_left_col_num,
                                          blank_left_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_right_col_num,
                                          blank_right_row_num, tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_up_col_num, blank_up_row_num,
                                          tile_per_row))
                        switchable_tile_num.append(
                            tile_num_calc(blank_down_col_num,
                                          blank_down_row_num, tile_per_row))

                #if tile clicked is switchable, switch pos in random dict
                if tile_clicked in switchable_tile_num:
                    move_num +=  1
                    for i in switchable_tile_num:
                        if i == tile_clicked:
                            for x, y in tile_random_dict.items():
                                if x == tile_clicked:
                                    click = y
                                    temp = click
                                if x == blank_num:
                                    blank = y
                                
                            for x, y in tile_random_dict.items():
                                if x == tile_clicked:
                                    tile_random_dict[x] = blank
                                if x == blank_num:
                                    tile_random_dict[x] = temp
                                    
                    #display the number of moves in the lower panel              
                    frame_pen.st()
                    frame_pen.penup()
                    frame_pen.goto(-319,-300)
                    frame_pen.pendown()
                    frame_pen.color('black')

                    style = ('Arial', 30)
                    frame_pen.write('Player Moves:',
                                    font = style, align = 'left')
                    frame_pen.ht()
                    move_num_pen.clear()
                    move_num_pen.st()
                    move_num_pen.penup()
                    move_num_pen.goto(-100, -300)
                    move_num_pen.pendown()
                    move_num_pen.write(f'{move_num}', font = style,
                                       align = 'left')
                    move_num_pen.ht()
                            
                    #restamping puzzle tiles after swithing
                    for i, j in tile_random_dict.items():
                        stamp_pic(stamp,
                                  (TILE_INI_X + 100 * (i % tile_per_row)),
                        (TILE_INI_Y - 100 * ( i // tile_per_row )),
                        f'Images/{puz}/{j}.gif')
                        
                    tile_random_list = list(tile_random_dict.values())
                    tile_original_list = list(tile_dict.values())

                    #check if new tile list matches with original one
                    if tile_random_list == tile_original_list:
                        with open('leaderboard.txt', mode = 'a') as outfile:
                            outfile.write(f'{move_num}: {name}\n')
                            
                        stamp_pic(stamp, 0, 0, 'Resources/winner.gif')
                        bg.update()
                        time.sleep(2)
                        stamp.clearstamps(-1)
                        bg.bye()
                    #if run out of steps, but fail, close game
                    if move_num == num_step:
                        stamp_pic(stamp, 0, 0, 'Resources/Lose.gif')
                        bg.update()
                        time.sleep(2)

                        stamp_pic(stamp, 0, 0, 'Resources/credits.gif')
                        bg.update()
                        time.sleep(3)
                        bg.bye()

            #if click on load button, display a menu of all puzzles        
            if x <= 240 and x >= 160 and y >= -328 and y <= -252:
                print('Load is clicked')
                move_num_pen.clear()
                move_num = 0
                #if select available puzzle, load it
                while True:
                    load_puzzle = turtle.textinput('Load puzzle',
                                                   'Enter the name of the ' \
                                                    'puzzle '\
'you wish to load. Choices are:\n''luigi\nsmiley\nfifteen\nyoshi\nmario')
                
                    
                    if load_puzzle == 'luigi' or load_puzzle == 'smiley'\
                    or load_puzzle == 'fifteen' \
                    or load_puzzle == 'yoshi' or load_puzzle == 'mario':
                        tile_boarder.clear()
                        stamp.clearstamps()
                        bg.update()
                        stamp.ht()
                        tile(load_puzzle)   
                        break
                    #if select not available puzzle, show error image 
                    else:
                        print('Invalid puzzle game')
                        stamp_pic(stamp,0,0,'Resources/file_error.gif')
                        bg.update()
                        time.sleep(2)
                        stamp.clearstamps(-1)
                        stamp.ht()
                        
                        error = 'Error: Could not open leaderboard.txt. '\
                        + 'Location: handle_click(), load'
                        now = datetime.now()
                        time_now = now.strftime("%m/%d/%Y %H:%M:%S")
                        day = now.strftime('%a')

                        with open('5001_puzzle.err', mode='a') as outfile:
                            outfile.write(day + ' ' + time_now + ' ' + error +
                                          '\n')

            #if click on reset button, restamp tiles in original order           
            if x <= 150 and x>= 70 and y >= -330 and y <= -250:
                print('reset is clicked')
                stamp.clearstamps(-1 - puz_num)              
                for i in tile_random_dict:
                    tile_random_dict[i] = tile_dict[i]
                    
                
                for i, j in tile_random_dict.items():
                        stamp_pic(stamp,
                                  (TILE_INI_X + 100 * (i % tile_per_row)),
                        (TILE_INI_Y - 100 * ( i // tile_per_row )),
                        f'Images/{puz}/{j}.gif')
                stamp_pic(stamp, THUMB_X, THUMB_Y, puz_thumb_name)

            #if click on quit button, close the game    
            if x <= 330 and x >= 250 and y >= -316.5 and y <= -263.5:
                print('Quit is clicked')
                stamp_pic(stamp, 0, 0, 'Resources/quitmsg.gif')
                bg.update()
                time.sleep(2)
                stamp.clearstamps(-1)
                bg.bye()
   
        bg.onclick(handle_click)

    leader()
    tile(game_select)

def main():
    board()

if __name__ == "__main__":
    main()
    
    
