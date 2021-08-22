import gc
try:
  import usocket as socket
except:
  import socket
led_state = "OFF"
from machine import Pin
import time
import re

led = Pin(2, Pin.OUT)
led.off()

def web_page():
    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .button1 {
            background-color: #000000;
        }
    </style>
</head>

<body>
    <h2>ESP Gate Bluetooth Proximity Server</h2>
    <form action="/action">
        <p>
            <label for="addBT">Add</label>
            <input type="text" id="addBT" name="addBT" maxlength = "16"><br><br>
        </p>
        <p>
            <label for="delBT">Remove</label>
            <input type="text" id="deleteBT" name="delBT" maxlength = "16"><br><br> 
        </p>
        <input type="submit" value="Submit">

    </form>
</body>

</html>"""
    
    return html

def webserverstart():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    return s

def getParam(paramName, s):
    ret = ""
    i = s.find(paramName+"=")
    if i > 0: 
        i = i + len(paramName)+1
        i1 = i
        while i < len(s) and s[i] != "&" and s[i] != " ":
            i = i + 1
        if i > i1: ret = s[i1:i]
    return ret

def webserver(s, onAdd, onDelete):
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        rs = request.decode("utf-8")
        print('GET Rquest Content = %s' % rs)
        rrr = rs.find('/action')
        isAction = rrr == 4
        print("RRR",rrr)
        if isAction: 
            print("found")
            addBT=getParam("addBT",rs).replace("%3A",":")
            delBT=getParam("delBT",rs).replace("%3A",":")
            print("BT",addBT,delBT)
            onAdd(addBT)
            print('LED ON -> GPIO2')
            led_state = "ON"
            led.on()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
