import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

def replace_at_index(string, index, letter):
    return string[:index] + letter + string[index + 1:]

COLORS = {
    "ybo": "ybowww",
    "yog": "yogwww",
    "yrb": "yrbwww",
    "ygr": "ygrwww",
    "wob": "wobyyy",
    "wgo": "wgoyyy",
    "wbr": "wbryyy",
    "wrg": "wrgyyy",
    "byr": "byrggg",
    "brw": "brwggg",
    "bwo": "bwoggg",
    "boy": "boyggg",
    "gry": "grybbb",
    "gwr": "gwrbbb",
    "gow": "gowbbb",
    "gyo": "gyobbb",
    "owg": "owgrrr",
    "ogy": "ogyrrr",
    "oyb": "oybrrr",
    "obw": "obwrrr",
    "rgw": "rgwooo",
    "ryg": "rygooo",
    "rby": "rbyooo",
    "rwb": "rwbooo",
}

UD_COLORS = {
    "y": "ybowww",
    "w": "wobyyy",
    "b": "byrggg",
    "g": "grybbb",
    "o": "owgrrr",
    "r": "rgwooo",
}

COLORS_U_LETTERS = {
    "ybo": "A",
    "yog": "B",
    "yrb": "C",
    "ygr": "D",
    "wob": "U",
    "wgo": "V",
    "wbr": "W",
    "wrg": "X",
    "byr": "F",
    "brw": "H",
    "bwo": "G",
    "boy": "E",
    "gry": "M",
    "gwr": "O",
    "gow": "P",
    "gyo": "N",
    "owg": "T",
    "ogy": "R",
    "oyb": "Q",
    "obw": "S",
    "rgw": "L",
    "ryg": "J",
    "rby": "I",
    "rwb": "K",
}

COLORS_D_LETTERS = {
    "ybo": "U",
    "yog": "V",
    "yrb": "W",
    "ygr": "X",
    "wob": "A",
    "wgo": "B",
    "wbr": "C",
    "wrg": "D",
    "byr": "M",
    "brw": "O",
    "bwo": "P",
    "boy": "N",
    "gry": "F",
    "gwr": "H",
    "gow": "G",
    "gyo": "E",
    "owg": "L",
    "ogy": "J",
    "oyb": "I",
    "obw": "K",
    "rgw": "T",
    "ryg": "R",
    "rby": "Q",
    "rwb": "S",
}

# https://cube.rider.biz/visualcube.php?fmt=png&pzl=1&size=200&fc=rlsybb&bg=t&r=y45x34
URL = "https://cube.rider.biz/visualcube.php?fmt=png&pzl=1&size=200&bg=t"

def save_images(dir_path, is_down, grey_idxs, colors):
    dir_path = f"images/{dir_path}"
    os.makedirs(dir_path, exist_ok=True)
    angle_param = "&r=y45x25" if is_down else ""

    for k, v in colors.items():
        url =  f"{URL}{angle_param}&fc="

        for i in grey_idxs:
            v = replace_at_index(v, i, 'l')
        
        url += v
        
        res = urllib.request.urlopen(url)
        filename = f"{dir_path}/{k}.png"
        f = open(filename, "wb")
        f.write(res.read())
        f.close()

def save_letter_images(is_down, colors):
    for k, v in colors.items():
        letter = v
        face = "D" if is_down else "U"

        try:
            image = Image.open(f"images/lr_{face}/{k[0]}.png")
        except FileNotFoundError:
            print(f"Error: The file was not found.")
            return

        draw = ImageDraw.Draw(image)

        center_position = (100, 152) if is_down else (100, 55)

        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except IOError:
            print("Using default font")
            font = ImageFont.load_default()

        bbox = font.getbbox(letter)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        top_left_position = (center_position[0] - text_width // 2, center_position[1] - text_height + 3) # // 2

        fill = "black"
        if face == "U" and k[0] in ["r", "b"]:
            fill = "white"
        if face == "D" and k[0] in ["o", "g"]:
            fill = "white"

        draw.text(top_left_position, letter, font=font, fill=fill)

        os.makedirs(f"images/letter_{face}", exist_ok=True)

        output_path = f"images/letter_{face}/{k}.png"
        image.save(output_path)
        # print(f"Image saved as '{output_path}'.")




# save_images("answer_D", True, [], COLORS)
# save_images("answer_U", False, [], COLORS)

# save_images("left_U", False, [2], COLORS)
# save_images("right_U", False, [1], COLORS)
# save_images("top_U", False, [0], COLORS)

# save_images("left_D", True, [2], COLORS)
# save_images("right_D", True, [1], COLORS)
# save_images("bottom_D", True, [3], COLORS)

# save_images("lr_U", False, [1, 2], UD_COLORS)
# save_images("lr_D", True, [1, 2], UD_COLORS)

save_letter_images(True, COLORS_D_LETTERS)
save_letter_images(False, COLORS_U_LETTERS)
