from flask import Flask, request
app=Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ahoj')
def ahoj():
    # Získání vstupu z query parametru "jmeno"
    jmeno = request.args.get('jmeno', 'Neznámý')
    return f'Ahoj, {jmeno}!'


if __name__=='__main__':
    app.run(debug=True)
