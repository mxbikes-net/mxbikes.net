from app.__init__ import create_app
import os
from flask import Flask, send_from_directory, make_response

app = create_app()

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    with app.app_context():
        from app.models import db
        db.create_all()
    app.run(host='127.0.0.1', port=8001, debug=True, use_reloader=False)
