set PORT=COM3
taskkill /FI "WindowTitle eq PythonMiniterm*" /T /F
ampy -p %PORT% -d 2.0 put main.py
ampy -p %PORT% -d 2.0 put ./lib