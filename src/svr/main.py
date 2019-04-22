from app import main_app

if __name__ == '__main__':
    main_app.debug = True
    main_app.run(host = '127.0.0.1', port = 5000)
