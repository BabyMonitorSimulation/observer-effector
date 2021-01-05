from project import app


if __name__ == "__main__":
    port = 5002
    print(f'Running Decider port:{port} \n')
    app.run(port=port, debug=True)
