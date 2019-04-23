## SimpleHTTPserver
SimpleHTTPserver.py is a simple HTTP service on Raspberry pi platform.
At the same time, it used VS Code remote edition.

SimpleHTTPserver.py 是一個簡單的HTTP網頁服務範例, 它是在Raspberry pi3上驗證的
同時本範例是使用VS Code遠程編輯.
###Start VSCode

Under command line of VSCode

* SSH pi@192.168.0.12    # need your password of the pi account

* rmate –p 52698 simple_webserver.py  # get the program (souce code) to VSCode

* Ctrl+S  # save the soucer code to remote raspberry pi after on your editor

* python3 ./simple_webserver.py   # Run http server


###Start Edge on your PC or mobile phone

* 192.168.0.12:8000

### Or download from github
git clone git@github.com:louisopen/SimpleHTTPServer.git
git clone git@github.com:louisopen/SimpleHTTPServer/simple_webserver.py
