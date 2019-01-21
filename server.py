#  coding: utf-8 
import socketserver
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        method = self.data.decode().split()[0]
        # method not allowed
        if method != 'GET':
            self.request.sendall(bytearray(response_405, 'utf-8'))
            return
        path = self.data.decode().split()[1]
        # determin the file type
        if 'css' in path:
            Format = 'css'
        else:
            Format = 'html'
        try:
            # this handles if the requested file exists
            if '.' in path:
                # request for specific file
                path = 'www' + path
                #safety check
                paths = path.split('/')
                safe = 0
                for i in paths:
                    if i == '..':
                        safe -= 1
                    else:
                        safe += 1
                if safe < 1:
                    raise ValueError('Not Safe!')
                response = open(path, 'rb')
            elif path[-1] == '/':
                # request for the index file under that folder
                path = 'www' + path + 'index.html'
                response = open(path, 'rb')            
            else:
                # redirect
                path = path + '/'
                try:
                    # check if redirected link exits in server directory
                    f = open('www'+path+'index.html')
                    f.close()
                    self.request.sendall(bytearray(moved_away_response.format(PATH=path), 'utf-8'))
                    return  
                except:
                    # redirected link does not exit
                    path = 'not found'
                    raise ValueError('Not Found')
        except:
            # requested fiel does not exist
            print('404')
            path = 'www/404.html'
            response = open(path, 'rb')
            self.request.sendall(bytearray(response_404.format(FORMAT='html'), 'utf-8'))
            self.request.sendfile(response)
            response.close()
            return
            
        self.request.sendall(bytearray(ok_response.format(FORMAT=Format), 'utf-8'))
        self.request.sendfile(response)
        response.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    moved_away_response = """HTTP/1.1 301 Permanently moved to {PATH}
Location: {PATH}
    
"""
    response_405 = """HTTP/1.1 405 Method Not Allowed
Server: Yi's server

"""
    
    response_404 = """HTTP/1.1 404 Not Found
Server: Yi's server
Content-Type: text/{FORMAT}

"""
    ok_response = """HTTP/1.1 200 OK
Server: Yi's server
Content-Type: text/{FORMAT}

"""

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
