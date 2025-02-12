
import time
from typing import List
from input_control import A, X, PressKey, ReleaseKey
from utils import get_all_handles, get_exe_from_process_id, get_process_id_from_handle
import pywintypes
import win32.win32gui as gui
import win32com.client as the_client

def find_my_handles(name: str) -> List[int]:
    length = len(name)
    handles_list = get_all_handles()
    return_list = []    
    for handle in handles_list:
        proc_id = get_process_id_from_handle(handle)
        exe_name = get_exe_from_process_id(proc_id)
        if exe_name[-length:] == name:
            return_list.append(handle)
    return return_list

shell = the_client.Dispatch("WScript.Shell")

def send_input_to_window(key: str, window_handle:int) -> None:
    # get foregroundwindow to switch back to later
    current_handle = gui.GetForegroundWindow()
    # bring targetwindow to foreground
    if window_handle != current_handle:
        shell.SendKeys("%")
        
        try:
            gui.SetForegroundWindow(window_handle)
        except pywintypes.error as e:
            print(e)
            if e.winerror == 1400:
                print("Window Gone")
    # send input
    time.sleep(1)
    for _ in range(5):
        PressKey(key)
        time.sleep(0.5)
        # release
        ReleaseKey(key)
    # bring cached window to foreground
    # if window_handle != current_handle:
    #     shell.SendKeys("%")
    #     try:
    #         gui.SetForegroundWindow(current_handle)    
    #     except pywintypes.error as e:
    #         print(e)
    #         if e.winerror == 1400:
    #             print("Window Gone")

if __name__ ==  "__main__":
    my_handle_list = find_my_handles("ufo50.exe")
    HANDLE = 1117284
    # my_handle_list = find_my_handles("scummvm.exe")
    # my_handle_list = find_my_handles("Notepad.exe")
    # try:
    #     gui.SetForegroundWindow(HANDLE)
    # except pywintypes.error as e:
    #     print(e)
    #     if e.winerror == 1400:
    #         print("Window Gone")
    # key = X
    # for _ in range(5):
    #     PressKey(key)
    #     time.sleep(0.5)
    #     # release
    #     ReleaseKey(key)
    for handle in my_handle_list:
        send_input_to_window(X, handle)
        print(handle)