from cx_Freeze import setup, Executable

build_exe_options = {
    "packages":["pyautogui","cv2","pygame","asyncio","requests"],
    "include_files":[("a\\")]}

setup(

       name="CoSCounter",

       version="0.1.1",

       description="Helper program for Creatures of Sonaria",
       options = {"build_exe": build_exe_options},
       executables=[Executable("main.pyw")],

)