# -*- coding: UTF-8 -*-

class Database:
    
    def __init__(self):
        import psycopg2
        
        # Navigate to pod and find the internal IP for Postgres service
        #self.connection_ = psycopg2.connect(host="", port=5432, user="postgres", password="postgres")
        
        # For local testing (before deploying the service), use command oc port-forward <pod-name> 12345:5432
        #self.connection_ = psycopg2.connect(host="127.0.0.1", port=12345, user="postgres", password="postgres")
        
        self.cursor_ = self.connection_.cursor()
        
    def insert_(self, stream_id_, seq_id_, image_base64_str_):
        SQL_ = """INSERT INTO AHMEDABAD(STREAM_ID, SEQ_ID, IMAGE_BASE64_STR, PROGRESS_FLAG) 
                    VALUES(%s, %s, %s, %s) RETURNING SEQ_ID;"""
        
        self.cursor_.execute(SQL_, (stream_id_, seq_id_, image_base64_str_, 0))
        self.connection_.commit()
        return
        
    def select_(self):
        self.cursor_.execute("SELECT STREAM_ID, SEQ_ID, PROGRESS_FLAG FROM AHMEDABAD")
        return self.cursor_.fetchall()

from flask import Flask, request  # From module flask import class Flask
app = Flask(__name__)    # Construct an instance of Flask class for our webapp

@app.route('/view', methods=['GET'])   # URL '/' to be handled by main() route handler
def view():
    try:
        database_ = Database()
        return {
            "db-response": {
                "data": database_.select_(),
                "error": False
            }
        }
    except Exception as e_:
        return {
            "db-response": {
                "error": True,
                "data": str(e_)
            }
        }

@app.route('/', methods=['POST'])   # URL '/' to be handled by main() route handler
def main():
    try:
        database_ = Database()
        database_.insert_(
            int(request.form['stream_id']), int(request.form['seq_id']), 
            request.form['image_base64_str'])
        return {
            "db-response": {
                "error": False,
                "comments": []
            }
        }
    except Exception as e_:
        return {
            "db-response": {
                "error": True,
                "comments": [str(e_)]
            }
        }

if __name__ == '__main__':  # Script executed directly?
    print("Hello, World. Uses S2I to build the application.")
    app.run(host="0.0.0.0", port=8080, debug=True,use_reloader=True)  # Launch built-in web server and run this Flask webapp
