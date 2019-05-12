## Simple HTTP server
SimpleHTTPserver.py is a simple HTTP service to control GPIO status on Raspberry pi platform.
At the same time, it used VS Code remote edition.

SimpleHTTPserver.py 是一個簡單的HTTP網頁服務範例,它是演示驗證在Raspberry pi3上的網頁直接控制IO pin的狀態,同時演示使用VS Code遠程編輯.

### Start VSCode
Under command line of VSCode

* SSH pi@192.168.0.12    # need your password of the pi account

* rmate –p 52698 simple_webserver.py  # get the program (souce code) to VSCode

* Ctrl+S  # save the soucer code to remote raspberry pi after on your editor

* python3 ./simple_webserver.py   # Run http server

### Or download example from github
git clone git@github.com:louisopen/SimpleHTTPServer.git

git clone git@github.com:louisopen/SimpleHTTPServer/simple_webserver.py

### Start Edge on your PC or mobile phone

* 192.168.0.12:8000
