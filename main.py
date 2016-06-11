import flask
from shelljob import proc
from static.index import INDEX_TEMPLATE

import eventlet
eventlet.monkey_patch()

app = flask.Flask(__name__)

@app.route( '/stream/<cmd>' )
def stream(cmd):

    g = proc.Group()
    #p = g.run( [ "bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done" ] )
    p = g.run( [ "zsh", "-c", "{args}".format(args=cmd)])

    def read_process():
        while g.is_pending():   
            lines = g.readlines()
            for proc, line in lines:
                yield "data:" + line + "\n\n"

    return flask.Response( read_process(), mimetype= 'text/event-stream' )

@app.route('/page')
def get_page():
    return """ <!DOCTYPE html>
<html>
<head>
    <script>
    var source = new EventSource("/stream");
    source.onmessage = function(event) {
        document.getElementById("output").innerHTML += event.data + "<br/>"
    }
    </script>
</head>
<body>
    <h1> Input </h1>
    <div id="input"></div>

    <h1>Output</h1>
    <div id="output"></div>
</body>
</html> """

    #return flask.send_file('page.html')
    #html = INDEX_TEMPLATE.substitute()
    #return html

@app.route('/')
def root():
    return """ <center><h1> FlaskLiveTerminal </h1></center>
     """

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1337)