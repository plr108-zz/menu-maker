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
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    output = "<html><body><h1>%s" % myRestaurantQuery.name
                    output += "</h1><form method='POST' "
                    output += "enctype='multipart/form-data' action = "
                    output += "'/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name='newRestaurantName' type='text' "
                    output += "placeholder='%s'>" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
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
                    edit_path = '/restaurants/%s/edit' % restaurant.id
                    output += restaurant.name + "<br>"
                    output += "<a href='%s'>" % edit_path
                    output += "Edit</a><br><a href='#'>Delete</a>"
                    output += "<br><br><br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, "File Not Found: %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader("content-type"))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get("newRestaurantName")
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header("Content-type", "text/html")
                        self.send_header("Location", "/restaurants")
                        self.end_headers()
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
