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