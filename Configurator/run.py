from project import app


if __name__ == "__main__":
    port = 5003
    print(f'Running Configurator (Middleware) port:{port} \n')
    app.run(port=port, debug=True)
