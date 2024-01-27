from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

from data import books, movies
import cgi
from helpers.getBookHandler import get_book
from helpers.fileMetadata import file_metadata
from helpers.updateListWithNewItem import update_list
from helpers.info import endpoints_info

class SimpleHandler(SimpleHTTPRequestHandler):
    def _send_response(self, message, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, 'utf8'))


    def do_GET(self):
        print(self.path)

        if self.path == '/':
            self._send_response(json.dumps(endpoints_info, sort_keys=True, indent=4))

        if self.path == '/text':
            self._send_response('Simple text')

        elif self.path == '/books':
            self._send_response(json.dumps(books.older_books + books.modern_books))

        elif self.path == '/movies':
            self._send_response(json.dumps(movies))


        elif self.path == '/html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('assets/random_html1.html', 'rb') as file:
                html_content = file.read()
            self.wfile.write(html_content)


        elif self.path.startswith('/image/'):
            image_file = self.path[7:]
            file_path = 'assets/images/' + image_file

            try:
                with open(file_path, 'rb') as file:
                    image_content = file.read()

                self.send_response(200)
                self.send_header('Content-type','image/jpeg')
                self.end_headers()
                self.wfile.write(image_content)

            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Image not found')

            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Internal Server Error')

        elif self.path.startswith('/checkurl'):
            # http://localhost:8001/checkurl?url=https://teaching.kse.org.ua/mod/assign/view.php?id=37061
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            url_to_check = query_params.get('url', [None])[0]

            if url_to_check is None:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('URL parameter is missing'.encode('utf-8'))
                return
            try:
                parsed_url = urlparse(url_to_check)
                response = {
                    'scheme': parsed_url.scheme,
                    'domain': parsed_url.netloc,
                    'path': parsed_url.path,
                    'query': parsed_url.query
                }
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

        elif self.path.startswith('/books?'):
            book = get_book(self.path)
            self._send_response(json.dumps(book))

        else:
            self._send_response('not found', status=404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)

        if self.path == '/':
            try:
                data = json.loads(post_data.decode('utf-8'))
                self._send_response(
                    json.dumps({'req': 'This is a POST request with path ' + self.path, 'data_received': data}))
            except json.JSONDecodeError:
                self._send_response('Error: Invalid JSON data received in the POST request.', status=400)

        if self.path == '/add':
            try:
                added_json = json.loads(post_data.decode('utf-8'))
                updated_list = update_list(added_json)
                self._send_response(
                    json.dumps({'updated list': updated_list}))
            except json.JSONDecodeError:
                self._send_response('Error: Invalid JSON data received in the POST request.', status=400)

        if self.path == '/upload':
            try:
                added_json = json.loads(post_data.decode('utf-8'))
                filename = added_json.get('filename')
                search_string = added_json.get('string')

                # {"filename":"/Users/bunjee/Documents/WebDevepment/python-setup/data/12.txt","string":"vareniki"}

                metadata = file_metadata(filename, search_string)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(metadata).encode('utf-8'))
            except json.JSONDecodeError:
                self._send_response('Error: Invalid JSON data received in the POST request.', status=400)



def run_server(port=8001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

