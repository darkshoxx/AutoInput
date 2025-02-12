# Section taken from  
# https://gist.github.com/Aniruddha-Tapas/1627257344780e5429b10bc92eb2f52a
from ctypes import POINTER, WinError, byref, c_int, get_last_error, sizeof, wintypes, Structure, WinDLL, Union
import time

user32 = WinDLL('user32', use_last_error=True)

INPUT_KEYBOARD = 1

KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_KEYUP       = 0x0002
MAPVK_VK_TO_VSC = 0

# List of all codes for keys:
# # msdn.microsoft.com/en-us/library/dd375731
UP = 0x26
DOWN = 0x28
A = 0x41
X = 0x58

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class HARDWAREINPUT(Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class KEYBDINPUT(Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))
    
    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.       
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)

class INPUT(Structure):
    class _INPUT(Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise WinError(get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             c_int)

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    print(user32.SendInput(1, byref(x), sizeof(x)))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=-KEYEVENTF_KEYUP))
    user32.SendInput(1, byref(x), sizeof(x))

if __name__ == "__main__":
    key = X
    time.sleep(2)
    while True:
        PressKey(key)
        time.sleep(0.5)
        ReleaseKey(key)
        time.sleep(0.5)
        print(f"pressed {str(key)}")