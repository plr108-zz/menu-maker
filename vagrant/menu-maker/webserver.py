from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                output = "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' "
                output += "action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' "
                output += "placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                restaurants = session.query(Restaurant).all()
                output = "<a href='/restaurants/new'> "
                output += "Make a New Restaurant Here</a><br><br>"
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name + "<br>"
                    output += "<a href='#'>Edit</a><br>"
                    output += "<a href='#'>Delete</a><br><br><br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader("content-type"))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get("newRestaurantName")
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Location", "/restaurants")
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(("", port), webserverHandler)
        message = "Web server running...\nOpen localhost:%s" % port
        message += "/restaurants in your browser"
        print message
        server.serve_forever()
    except KeyboardInterrupt:
        print "\nStopping web server..."
        server.socket.close()


if __name__ == "__main__":
    main()
