from PIL import Image


# This function takes the name of the map and a list of colors
# And returns a 2D array containing the color codes
# Each color code represents a tile/object/character
def load_map_data(level_name):
    map_name = level_name + ".bmp"
    assets_name = level_name + ".txt"

    image = Image.open(map_name, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    image.close()

    decoded_map = [[0 for x in range(width)] for y in range(height)]

    # Checks every pixel in the image to find out it's number
    for y in range(0, height):
        for x in range(0, width):
            decoded_map[y][x] = check_color_code(pixel_values[width * y + x], color_data)

    return decoded_map


# This function takes a color and a list of colors and returns the correct color code
def check_color_code(color, color_data):
    # Color white is treated as the blank color
    counter = 0
    for col in color_data:
        if col == color:
            return counter
        counter += 1
    # If color isn't found 0 is returned
    return 0;


# This function returns a list of colors from the file
# This is called automatic but can be called manually
# To for example change the file where the data is being
# Gathered from
def get_color_codes(file_name):
    color_code_file = open(file_name, "r")
    if color_code_file.mode == "r":
        content = color_code_file.read()
        color_code_file.close()
        red = list()
        green = list()
        blue = list()
        color_count = 0
        for value in content.split():
            # If a word starts with # it is treated like a comment
            # WARNING -> #comment, #not a comment, #this_is_a_comment
            if value[0] == '#':
                continue
            if color_count == 0:
                red.append(int(value))
            elif color_count == 1:
                green.append(int(value))
            else:
                blue.append(int(value))
                color_count = 0
                continue
            color_count += 1
        color_data = list(zip(red, green, blue))
        return color_data
    color_code_file.close()


# Default file name
color_data = get_color_codes("data/Color_Code_Data.txt")
