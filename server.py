# import json
# from http.server import BaseHTTPRequestHandler, HTTPServer
# from views import (
#     get_all_animals,
#     get_single_animal,
#     create_animal,
#     delete_animal,
#     update_animal,
#     get_all_locations,
#     get_single_location,
#     create_location,
#     delete_location,
#     update_location,
#     get_all_employees,
#     get_single_employee,
#     create_employee,
#     delete_employee,
#     update_employee,
#     get_all_customers,
#     get_single_customer,
#     create_customer,
#     # delete_customer,
#     update_customer
# )

# method_mapper = {
#     "animals": {
#         "all": get_all_animals,
#         "single": get_single_animal
#     },
#     "locations": {
#         "all": get_all_locations,
#         "single": get_single_location
#     },
#     "employees": {
#         "all": get_all_employees,
#         "single": get_single_employee
#     },
#     "customers": {
#         "all": get_all_customers,
#         "single": get_single_customer
#     }
# }


# class HandleRequests(BaseHTTPRequestHandler):
#     """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
#     """

#     def parse_url(self, path):
#         """This function splits the client path string into parts to isolate the requested id"""
#         path_params = path.split("/")
#         resource = path_params[1]
#         id = None

#         try:
#             # Convert the string "1" to the integer 1
#             # This is the new parseInt()
#             id = int(path_params[2])
#         except IndexError:
#             pass  # No route parameter exists: /animals
#         except ValueError:
#             pass  # Request had trailing slash: /animals/

#         return (resource, id)  # This is a tuple

#     def get_all_or_single(self, resource, id):
#         """Reusable Function"""
#         if id is not None:
#             response = method_mapper[resource]["single"](id)

#             if response is not None:
#                 self._set_headers(200)
#             else:
#                 self._set_headers(404)
#                 response = ''
#         else:
#             self._set_headers(200)
#             response = method_mapper[resource]["all"]()

#         return response

#     # Here's a class function

#     # Here's a method on the class that overrides the parent's method.
#     # It handles any GET request.
#     def do_GET(self):
#         """Handles GET requests to the server"""
#         response = None
#         (resource, id) = self.parse_url(self.path)
#         response = self.get_all_or_single(resource, id)
#         self.wfile.write(json.dumps(response).encode())

#     # Here's a method on the class that overrides the parent's method.
#     # It handles any POST request.
#     def do_POST(self):
#         """Handles POST requests to the server"""

#         # Set response code to 'Created'
#         # self._set_headers(201)
#         content_len = int(self.headers.get('content-length', 0))
#         post_body = self.rfile.read(content_len)

#         # Convert JSON string to a Python dictionary
#         post_body = json.loads(post_body)

#         # Parse the URL
#         (resource, id) = self.parse_url(self.path)

#         # Initialize new object - dictionary?
#         new_animal = None
#         new_location = None
#         new_employee = None
#         new_customer = None

#         # Add a new animal to the list. Don't worry about
#         # the orange squiggle, you'll define the create_animal
#         # function next.
#         if resource == "animals":
#             animals_list = ["name", "species",
#                             "status", "locationId", "customerId"]
#             if all(animals_list_item in post_body for animals_list_item in animals_list):
#                 self._set_headers(201)
#                 new_animal = create_animal(post_body)
#             else:
#                 self._set_headers(400)
#                 new_animal = {
#                     "message": f"{'name is required' if 'name' not in post_body else ''}{'species is required' if 'species' not in post_body else ''}{'status is required' if 'status' not in post_body else ''} {'locationId is required' if 'locationId' not in post_body else ''}{'customerId is required' if 'customerId' not in post_body else ''}"
#                 }
#             self.wfile.write(json.dumps(new_animal).encode())

#         if resource == "locations":
#             locations_list = ["name", "address"]
#             if all(locations_list_item in post_body for locations_list_item in locations_list):
#                 self._set_headers(201)
#                 new_location = create_location(post_body)
#             else:
#                 self._set_headers(400)
#                 new_location = {
#                     "message": f"{'name is required' if 'name' not in post_body else ''}{'address is required' if 'address' not in post_body else ''}"
#                 }
#             self.wfile.write(json.dumps(new_location).encode())

#         if resource == "employees":
#             if "name" in post_body:
#                 self._set_headers(201)
#                 new_employee = create_employee(post_body)
#             else:
#                 self._set_headers(400)
#                 new_employee = {
#                     "message": f"{'name is required' if 'name' not in post_body else ''}"
#                 }
#             self.wfile.write(json.dumps(new_employee).encode())

#         if resource == "customers":
#             if "name" in post_body:
#                 self._set_headers(201)
#                 new_customer = create_customer(post_body)
#             else:
#                 self._set_headers(400)
#                 new_customer = {
#                     "message": f"{'name is required' if 'name' not in post_body else ''}"
#                 }
#             self.wfile.write(json.dumps(new_customer).encode())

#     # A method that handles any PUT request.

#     def do_PUT(self):
#         """Handles PUT requests to the server"""
#         self._set_headers(204)
#         content_len = int(self.headers.get('content-length', 0))
#         post_body = self.rfile.read(content_len)
#         post_body = json.loads(post_body)

#         # Parse the URL
#         (resource, id) = self.parse_url(self.path)

#         # Update a single animal in the list
#         if resource == "animals":
#             update_animal(id, post_body)
#         if resource == "locations":
#             update_location(id, post_body)
#         if resource == "employees":
#             update_employee(id, post_body)
#         if resource == "customers":
#             update_customer(id, post_body)

#         # Encode the animal and send in response
#         self.wfile.write("".encode())

#     def do_DELETE(self):
#         """Handles DELETE requests to server"""

#         # Parse the URL
#         (resource, id) = self.parse_url(self.path)

#         # Delete a single animal from the list
#         if resource == "animals":
#             self._set_headers(204)
#             delete_animal(id)
#             self.wfile.write("".encode())
#         elif resource == "locations":
#             self._set_headers(204)
#             delete_location(id)
#             self.wfile.write("".encode())
#         elif resource == "employees":
#             self._set_headers(204)
#             delete_employee(id)
#             self.wfile.write("".encode())
#         # Encode the new animal and send in a response

#         if resource == "customers":
#             self._set_headers(405)
#             error_message = {
#                 "message": "Deleting the customers requires contacting the company directly."
#             }
#             self.wfile.write(json.dumps(error_message).encode())

#     def _set_headers(self, status):
#         # Notice this Docstring also includes information about the arguments passed to the function
#         """Sets the status code, Content-Type and Access-Control-Allow-Origin
#         headers on the response

#         Args:
#             status (number): the status code to return to the front end
#         """
#         self.send_response(status)
#         self.send_header('Content-type', 'application/json')
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.end_headers()

#     # Another method! This supports requests with the OPTIONS verb.
#     def do_OPTIONS(self):
#         """Sets the options headers
#         """
#         self.send_response(200)
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Access-Control-Allow-Methods',
#                          'GET, POST, PUT, DELETE')
#         self.send_header('Access-Control-Allow-Headers',
#                          'X-Requested-With, Content-Type, Accept')
#         self.end_headers()


# # This function is not inside the class. It is the starting
# # point of this application.
# def main():
#     """Starts the server on port 8088 using the HandleRequests class
#     """
#     host = ''
#     port = 8088
#     HTTPServer((host, port), HandleRequests).serve_forever()


# if __name__ == "__main__":
#     main()
