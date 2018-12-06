from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/res/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = "<html><body>"
            output += """<form method='POST' enctype='multipart/form-data'
            action='/res/new'>
            <h2>What would you like to tell me</h2>
            <input name='message' type='text'>
            <input type='submit' value='submit'></form>
            </body></html>"""
            self.wfile.write(output.encode())
            # print(output)
        # return
        elif self.path.endswith("/edit"):
            resturantIdfromPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(id = resturantIdfromPath).one()
            if myRestaurantQuery != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>"
                output += myRestaurantQuery.name
                output += "</h1>"
                output += """<form method='POST' enctype='multipart/form-data'
                        action='/restaurants/%s/edit'>""" % resturantIdfromPath
                output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
                output += "<input type='submit' value='Rename'>"
                output += "</form>" 
                self.wfile.write(output.encode())
        elif self.path.endswith("/delete"):
            resturantIdfromPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).filter_by(id = resturantIdfromPath).one()
            if myRestaurantQuery != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>Are you sure you want to delete %s ?" %myRestaurantQuery.name
                output += "<form method='POST' enctype='multipart/form-data' action ='/restaurants/%s/delete'>" %resturantIdfromPath
                output += "<input type='submit' value ='Delete' /></form></body></html>"
                self.wfile.write(output.encode())



        elif self.path.endswith("/restaurants"):
            Restaurants = session.query(Restaurant).all()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = "<html></body>"
            output += "<br/> <a href='/res/new'>Add New Restaurant</a></br>"
            for restaurant in Restaurants:
                output += "<h4>" + restaurant.name.encode() + "</h4>"
                output += "<a href='restaurants/%s/edit'>Edit</a>" % restaurant.id 
                output += "<a href='restaurants/%s/delete'>Delete</a>" % restaurant.id
            output += "</body></html>"
            self.wfile.write(output.encode())
            # print(output)

        elif self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = """<html><body>Hello!</body></html>
            <form method='POST' enctype='multipart/form-data'
            action='/hello'>
            <h2>What would you like to tell me</h2>
            <input name='message' type='text'>
            <input type='submit' value='submit'></form>
            </body></html>"""
            self.wfile.write(output.encode())
            print(output)

        elif self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = """<html><body>Hello!</body></html>
            <form method='POST' enctype='multipart/form-data'
            action='/hello'>
            <h2>What would you like to tell me</h2>
            <input name='message' type='text'>
            <input type='submit' value='submit'></form>
            </body></html>"""
            self.wfile.write(output.encode())
            print(output)
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if self.path.endswith('/res/new'):
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            elif self.path.endswith('/delete'):
                resturantIdfromPath = self.path.split("/")[2]
                myRestaurantQuery  = session.query(Restaurant).filter_by(id = resturantIdfromPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            elif self.path.endswith("/edit"):
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    resturantIdfromPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=resturantIdfromPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                    
            elif(self.path.endswith('/hello')
                 or self.path.endswith('/hola')):
                    output = ""
                    output += "<html></body>"
                    output += "<h2> Okay! how about this </h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += """<form method='POST'
                    enctype='multipart/form-data'
                    action='/hello'>
                    <h2>What would you like to tell me</h2>
                    <input name='message' type='text'>
                    <input type='submit' value='submit'></form>
                    </body></html>"""

            self.wfile.write(output.encode())
        except:
            pass    


def main():
    try:
        port = 8088
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
