# ANSI color codes
# ANSI color codes
class colors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    BRIGHT_YELLOW = '\033[93;1m'
    BRIGHT_GREEN = '\033[92;1m'
    BRIGHT_CYAN = '\033[96;1m'
    BRIGHT_BLUE = '\033[94;1m'
    BRIGHT_MAGENTA = '\033[95;1m'
    BRIGHT_RED = '\033[91;1m'
    BRIGHT_WHITE = '\033[97;1m'
    BRIGHT_BLACK = '\033[90;1m'
    BRIGHT_ORANGE = '\033[38;5;208m'
    BRIGHT_PURPLE = '\033[38;5;141m'

    END = '\033[0m'


def print_info(msg, color=colors.LIGHT_GREEN, info="INFO"):
    print(f"{color}[ {info} ]{colors.END}", color + msg + colors.END)


def print_error(msg, color=colors.LIGHT_RED, info="ERROR"):
    print(f"{color}[ {info} ]{colors.END}", color + msg + colors.END)


def print_debug(msg, color=colors.LIGHT_RED, info="DEBUG"):
    print(f"{colors}[ {info} ]{colors.END}", color + msg + colors.END)
