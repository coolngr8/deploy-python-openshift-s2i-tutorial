# -*- coding: UTF-8 -*-

from flask import Flask, request  # From module flask import class Flask
app = Flask(__name__)    # Construct an instance of Flask class for our webapp

def get_something_from_database_():
    import psycopg2
    
    connection_ = psycopg2.connect(host="172.30.184.140", port=5432, user="postgres", password="postgres")
    cursor_ = connection_.cursor()
    
    cursor_.execute("SELECT * FROM AHMEDABAD")
    return cursor_.fetchall()

@app.route('/', methods=['POST'])   # URL '/' to be handled by main() route handler
def main():
    """Say hello"""
    #return 'Hello, world!'
    try:
        return {
            "num-num": int(request.form['num'])*2,
            "db-response": get_something_from_database_()
        }
    except Exception as e_:
        return {
            "num-num": int(request.form['num'])*2,
            "db-response": str(e_)
        }

if __name__ == '__main__':  # Script executed directly?
    print("Hello, World. Uses S2I to build the application.")
    app.run(host="0.0.0.0", port=8080, debug=True,use_reloader=True)  # Launch built-in web server and run this Flask webapp
