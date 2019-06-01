import cx_Freeze

executables = [cx_Freeze.Executable("kolko_krzyzyk.py")]

cx_Freeze.setup(name="Kółko krzyżyk - PyGame",
                options={'build_exe': ["pygame"], 'include_files': []},
                executables=[cx_Freeze.Executable("kolko_krzyzyk.py")])
