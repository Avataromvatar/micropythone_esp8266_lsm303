## ESP8266 with micropython

[firmware](https://micropython.org/download/ESP8266_GENERIC/)  
[info](https://docs.micropython.org/en/latest/esp8266/quickref.html)  
[net info](https://www.programmersought.com/article/89385397335/)  
  -------  
[habr](https://habr.com/ru/articles/345912/)   
[some_info](https://pythonforundergradengineers.com/upload-py-files-to-esp8266-running-micropython.html)   

### install micropython
in venv   
```pip3 install esptool```
```pip3 install adafruit-ampy```

### env
on venv  
```source ~/.python_venv/bin/activate```   
```deactivate```  

### upload firmware
```esptool.py --port /dev/ttyUSB0 erase_flash```   
```esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin```  

## ampy
read file sys  
```ampy --port /dev/ttyUSB0 --baud 115200 ls```   
get boot script  
```ampy --port /dev/ttyUSB0 --baud 115200 get boot.py boot.py```  
put boot script   
```ampy --port /dev/ttyUSB0 --baud 115200 put boot.py```   
run script  
```ampy --port /dev/ttyUSB0 --baud 115200 run main.py```   
### run -n 
Run the code without waiting for it to finish and print
                   output.  Use this when running code with main loops that
                   never return.

    
If filesystem have main.py its will be run   
```ampy --port /dev/ttyUSB0 --baud 115200 put main.py```   

## netcat 
connect to server  
```nc -u 192.168.1.15 31111```  