from models.color import Color

DEFAULT_COLOR = Color(255, 255, 255, "white")
OFF_COLOR = Color(0, 0, 0, "none")
device_colors = []
MINIMUM_BLINK_SPAN = 300
LOADING_SPAN = 5


EXCELLENT_CONNECTION = (84, 245, 66)
GOOD_CONNECTION = (197, 245, 66)
POOR_CONNECTION = (245, 194, 66)
BAD_CONNECTION = (245, 90, 66)
UNRESOLVED_CONNECTION = (66, 69, 245)


TORCH_MAX = (255, 250, 50)

DEFAULT_FADE = [
    [255, 0, 0],
    [255, 255, 0],
    [0, 255, 0],
    [0, 255, 255],
    [0, 0, 255],
    [255, 0, 255]
]

DEFAULT_TORCH = [
    (160, 148, 31),
    (235, 226, 46),
    (184, 176, 36),
    (182, 176, 36),
    (182, 163, 36),
    (212, 203, 42),
    (201, 185, 40),
    (180, 168, 35),
    (212, 200, 42),
    (189, 174, 37),
    (228, 214, 45),
    (229, 222, 45),
    (177, 172, 35),
    (167, 160, 33),
    (206, 200, 41),
    (254, 239, 50),
    (155, 140, 30),
    (159, 145, 31),
    (217, 208, 43),
    (195, 180, 38),
    (222, 210, 44),
    (177, 170, 35),
    (166, 146, 33),
    (175, 168, 34),
    (210, 201, 41),
    (159, 150, 31),
    (240, 221, 47),
    (161, 143, 32),
    (196, 191, 39),
    (239, 222, 47),
]