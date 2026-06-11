To build .exe, run: 
pyinstaller imageconverter.py --windowed --specpath build_files --workpath build_files/build --distpath release

with --onefile option it will only be one file but slower at startup.