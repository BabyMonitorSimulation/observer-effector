from project import app


if __name__ == "__main__":
    port = 5001
    print(f'Run Observer port:{port} \n')
    app.run(port=port ,debug=True)
