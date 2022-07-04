from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from sys import argv

from bar_chart import gen_bar_chart
from heap_map import gen_heap_map
from line_chart import gen_line_chart


class VliangServer(BaseHTTPRequestHandler):

    # def do_GET(self):
    #     self.send_response(200)
    #     self.send_header('Content-type', 'text/html;charset=UTF-8')
    #     self.end_headers()
    #     f = open('../html/index.html', 'r')
    #     output = f.read()
    #     print(output)
    #     output = bytes(output, 'UTF-8')
    #     self.wfile.write(output)

    def do_POST(self):
        # get the size of data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(post_data)
        json_dict = json.loads(post_data)

        province = json_dict["province"]
        city = json_dict["city"]
        county = json_dict["county"]
        graph_type = json_dict["graph_type"]
        city_or_con = json_dict["city_or_con"]

        if json_dict["month"] == "":
            month = 1
        else:
            month = json_dict["month"]
            print(month)

        if graph_type == '0':
            gen_heap_map(month)
        elif graph_type == '1':
            if city_or_con == '市':
                gen_line_chart(_city=city, _flag=city_or_con)
            else:
                try:
                    gen_line_chart(_city=city + county, _flag=city_or_con)
                except Exception as e:
                    gen_line_chart(_city=county, _flag=city_or_con)
        elif graph_type == '2':
            if city_or_con == '市':
                gen_bar_chart(_city=city, _flag=city_or_con)
            else:
                gen_bar_chart(_city=city + county, _flag=city_or_con)

        # self.send_response(200)
        # self.send_header('Content-type', 'text/html;charset=UTF-8')
        # self.send_header("Access-Control-Allow-Origin", "*")
        # self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, PUT")
        # self.send_header("Access-Control-Max-Age", "3600")
        # self.send_header("Access-Control-Allow-Headers", "Content-Type, Access-Token, Authorization, ybg")
        # self.end_headers()
        # self.wfile.write("".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=VliangServer, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('server starts.\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("httpd.server_close()")
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    run(port=8080)
