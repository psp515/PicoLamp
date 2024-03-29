from models.color import Color

DEFAULT_COLOR = Color(255, 255, 255, "white")
OFF_COLOR = Color(0, 0, 0, "none")
DEVICE_COLORS = []
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

DEFAULT_SPIN = [
    [64, 64, 64],
    [164, 164, 164],
    [255, 255, 255],
    [164, 164, 164],
    [64, 64, 64]
]

DEFAULT_TORCH = [
    (160, 148, 31),
    (235, 226, 46),
    (184, 176, 10),
    (182, 146, 36),
    (182, 163, 36),
    (212, 203, 42),
    (201, 185, 40),
    (180, 178, 35),
    (212, 200, 42),
    (189, 174, 37),
    (228, 214, 45),
    (229, 222, 15),
    (197, 172, 35),
    (177, 160, 33),
    (206, 200, 41),
    (254, 239, 50),
    (145, 130, 30),
    (159, 145, 15),
    (217, 208, 43),
    (195, 180, 38),
    (222, 210, 44),
    (127, 110, 35),
    (166, 146, 33),
    (175, 168, 34),
    (210, 201, 15),
    (159, 150, 31),
    (240, 221, 47),
    (161, 143, 32),
    (196, 191, 5),
    (239, 222, 47),
]