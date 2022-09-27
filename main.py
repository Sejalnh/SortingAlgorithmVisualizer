import pygame
import random
import math
pygame.init()


class DrawInformation:
    BLACK = 0, 0, 0         # Class attributes accessible to all class instances
    WHITE = 255, 255, 255
    PURP = 238, 174, 238
    BLUE = 176, 224, 230
    BACKGROUND_COLOR = WHITE

    GRADIENT = [
        (224, 255, 255),
        (209, 238, 238),
        (180, 205, 205)
    ]

    FONT = pygame.font.SysFont('Times', 20)     # Font and size
    LARGE_FONT = pygame.font.SysFont('Times', 30)

    SIDE_PAD = 100      # Padding of 100 px from the left and right-hand side of window
    TOP_PAD = 150       # Padding of 150 px from the top of window

    def __init__(self, width, height, lst):     # Defining an initialization that takes in width, height and a list
                                                # That will be sorted
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))      # Creating a Pygame window
        pygame.display.set_caption("Sorting Algorithm Visualizer")  # Program Title
        self.set_list(lst)                                          # Call to set_list method

    def set_list(self, lst):
        self.lst = lst      # Stores list internally
        self.min_val = min(lst)     # Min value in list
        self.max_val = max(lst)     # Max value in list

        # Takes the total window width minus the side padding to give the workable window space
        # and divides it by the amount of elements in the list to give the width of one bar
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))

        # Represents the height of one unit of a block
        # The max value - min value gives the number of values in the range and distributes that in the workable area
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        # This is where the first bar is located on the X axis
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)   # Fills window with the background color

    # Draws menus bar options on screen
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.PURP)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    # Draws menu bar options on screen with a sharpness of 1 and color of black
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending ", 1, draw_info.BLACK)
    # Draws controls in the top center of screen
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    # Draws more menu bar options on screen
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()


#
def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    # Clears only the part of the screen where the bar chart is drawn, so the controls at the top isn't re drawn at every frame
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):   # Gives the index and value for every element in the list
        # This tells the program where to draw the bar so if i = 0 (first bar) we start at the first x position
        x = draw_info.start_x + i * draw_info.block_width
        # Takes the height of the bar and subtract it from the screen height to get the starting coordinate to
        # draw the bar downward from that point
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        # Gives each bar a different gradient in groups of three so no two bars next to each other are the same color
        color = draw_info.GRADIENT[i % 3]

        if i in color_positions:    # Uses dictionary where the index maps to a color
            color = color_positions[i]      # Manually override color we set above

        # Draws rectangles/bars in the Pygame window
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


# Randomly generated starting list
def generate_starting_list(n, min_val, max_val):
        lst = []

        for _ in range(n):
            val = random.randint(min_val, max_val)
            lst.append(val)
        return lst


#
def bubble_sort(draw_info, ascending=True):

    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
                num1 = lst[j]
                num2 = lst[j + 1]

                # Checks if we are sorting in ascending or descending and swaps the value to match
                if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]     # Swaps values in the array without a temp variable
                    draw_list(draw_info, {j: draw_info.PURP, j + 1: draw_info.BLUE}, True)     # Redraws list
                    yield True      # Yield command lets you pause the execution of the func and resume from the position where the function was yielded
    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        # While we are either sorting in ascending or descending swap values to match
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] > current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.PURP, i: draw_info.BLUE}, True)
            yield True  # everytime you do a swap yield = true

    return lst


def main():
    run = True
    clock = pygame.time.Clock()     # Regulates how quickly the loop runs

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)   # Generates list with a min and max and number of elements
    draw_info = DrawInformation(800, 600, lst)      # Instantiates DrawInfo Class to create PyGame window
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(120)      # Max number of times this loop can run per second

        if sorting:     # If we are sorting call the sorting_algorithm_generator method until the sorting is done
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        #   Returns a list of events that have occurred since the last time it was called
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # Quits program
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:     # Resets list and draws a new set of bars when 'r' is pressed
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:  # Press space triggers the program to start sorting
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:   # Press 'a' to sort in ascending order (once program is not sorting)
                ascending = True
            elif event.key == pygame.K_d and not sorting:   # Press 'd' to sort in descending order (once program is not sorting)
                ascending = False
            elif event.key == pygame.K_i and not sorting:   # Press 'i' to use insertion sort
                sorting_algorithm = insertion_sort          # Selects insertion sort
                sorting_algo_name = "Insertion Sort"        # Changes title to insertion sort
            elif event.key == pygame.K_b and not sorting:   # Press 'b' to use bubble sort
                sorting_algorithm = bubble_sort             # Selects bubble sort
                sorting_algo_name = "Bubble Sort"           # Changes title to bubble sort

    pygame.quit()   # Ends Pygame program after exiting loop


if __name__ == "__main__":      # Runs the module by clicking the run button before we call the main function
    main()
