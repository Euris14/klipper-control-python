from flask import Flask, render_template
from fluidd import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', variable = f'{i}')

if __name__ == "__main__":
    main()
    app.run()
    

