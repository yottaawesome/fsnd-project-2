from app.web_app import app

if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1', port = 5000)
