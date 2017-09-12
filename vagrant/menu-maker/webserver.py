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
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name + "<br>"
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)


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
