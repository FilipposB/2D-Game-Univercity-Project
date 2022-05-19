class Level:

    def __init__(self, level_id=-1, level_name="None", images_to_load=list(), background="Ground",
                 color_data_file="DEFAULT"):
        self.level_id = level_id
        self.level_name = level_name
        self.images_to_load = images_to_load
        self.background = background
        self.color_data_file = color_data_file

        #


def load_level_file():
    level_data_file = open("data/Level_Data.txt", "r")
    level_list = list()
    if level_data_file.mode == "r":
        content = level_data_file.read()
        level_data_file.close()
        for line in content.split("\n"):
            if len(line) < 1:
                continue

            # If a sentence starts with # it is treated like a comment
            if line[0] == '#':
                continue

            # Here we expect a level to be described
            tmp_lvl = Level()
            count_values = 0
            for value in line.split("&"):
                print(value)
                if count_values == 0:
                    tmp_lvl.level_id = int(value)
                elif count_values == 1:
                    tmp_lvl.level_name = value
                elif count_values == 2:
                    for img_files in value.split("%"):
                        tmp_lvl.images_to_load.append(img_files)
                elif count_values == 3:
                    tmp_lvl.background = value
                elif count_values == 4:
                    if tmp_lvl.color_data_file != value:
                        tmp_lvl.color_data_file = value
                else:
                    break
                count_values += 1
            level_list.append(tmp_lvl)
        level_data_file.close()
        return level_list
    level_data_file.close()
