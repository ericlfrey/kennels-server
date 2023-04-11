import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import (get_all, retrieve, update, delete, create)


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """This function splits the client path string into parts to isolate the requested id"""
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    def get_all_or_single(self, resource, id):
        """Tests whether to get All items, or get Single item"""
        if id is not None:
            response = retrieve(resource, id)
            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = get_all(resource)

        return response

    def do_GET(self):
        """Handles GET requests to the server"""
        response = None
        (resource, id) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server"""

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)

        new_dict = None
        required_attributes_list_mapper = {
            "animals": ["name", "species",
                        "status", "locationId", "customerId"],
            "locations": ["name", "address"],
            "employees": ["name"],
            "customers": ["name"]
        }

        if all(key_item in post_body for key_item in required_attributes_list_mapper[resource]):
            self._set_headers(201)
            new_dict = create(post_body, resource)
        else:
            key_list = ([key_item for key_item in
                        required_attributes_list_mapper[resource]
                        if key_item not in post_body])
            key_string = ', '.join([str(item) for item in key_list])
            self._set_headers(400)
            new_dict = {
                "message": f"{key_string} is required"
            }
        self.wfile.write(json.dumps(new_dict).encode())

    # A method that handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server"""
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        update(id, post_body, resource)
        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handles DELETE requests to server"""
        (resource, id) = self.parse_url(self.path)

        if resource == "customers":
            self._set_headers(405)
            error_message = {
                "message": "Deleting the customers requires contacting the company directly."
            }
            self.wfile.write(json.dumps(error_message).encode())
        else:
            self._set_headers(204)
            delete(resource, id)
            self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
