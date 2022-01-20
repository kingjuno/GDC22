from http.server import HTTPServer, SimpleHTTPRequestHandler

from solve_me import TasksCommand

class MyServer(SimpleHTTPRequestHandler):

    # ------------------------- vars -------------------------
    css = """
    <style>
    body {
        font-family: sans-serif;
        font-size: 1.2em;
    }
    button {
        font-size: 1.2em;
        font-weight: bold;
        padding: 0.5em;
        border: 1px solid #ccc;
        border-radius: 0.5em;
        background-color: #eee;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    form {
        margin:10% auto 0 auto;
        padding:30px;
        width:400px;
        height:auto;
        overflow:hidden;
        background:white;
        border-radius:10px;
    }
    form input {
        float:left;
        clear:both;
    }

    form input {
        margin:15px 0;
        padding:15px 10px;
        width:100%;
        outline:none;
        border:1px solid #bbb;
        border-radius:20px;
        display:inline-block;
        -webkit-box-sizing:border-box;
        -moz-box-sizing:border-box;
                box-sizing:border-box;
        -webkit-transition:0.2s ease all;
        -moz-transition:0.2s ease all;
            -ms-transition:0.2s ease all;
            -o-transition:0.2s ease all;
                transition:0.2s ease all;
    }

    form input[type=text]:focus,
    form input[type="password"]:focus {
        border-color:cornflowerblue;
    }

    input[type=submit] {
        padding:15px 50px;
        width:auto;
        background:#1abc9c;
        border:none;
        color:white;
        cursor:pointer;
        display:inline-block;
        position: relative;
        left: 50%;
        transform: translate(-50%, -50%);
        clear:right;
        -webkit-transition:0.2s ease all;
        -moz-transition:0.2s ease all;
            -ms-transition:0.2s ease all;
            -o-transition:0.2s ease all;
                transition:0.2s ease all;
    }

    input[type=submit]:hover {
        opacity:0.8;
    }

    input[type="submit"]:active {
        opacity:0.4;
    }

    </style>
    """

    # ------------------------- method ------------------------------
    def render_pending_tasks(self):
        command = "ls"
        arguments = None
        content = TasksCommand().run(command, arguments).replace("\n", "<br>")
        content = self.css + content + """<br>
            <button onclick='window.location.href = \"http://127.0.0.1:8000/\"'>
            Back
            </button>
        """ 
        return bytes(content, "utf-8")

    def render_completed_tasks(self):
        command = "report"
        arguments = None
        content = TasksCommand().run(command, arguments).replace("\n", "<br>")
        content = "Completed :"+content.split("Completed :")[1]
        content = self.css + content + """<br>
            <button onclick='window.location.href = \"http://127.0.0.1:8000/\"'>
            Back
            </button>
        """ 
        return bytes(content, "utf-8")

    # ------------------------------------------------------------------
    
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path == '/':
            self.wfile.write(bytes(self.css+"""
                    <html>
                    <body>
                        <form method='POST' action='/' autocomplete="off">
                            <input type='text' placeholder = ">" name='command'>
                            <input type='submit' value='Submit'>
                        </form>
                    </body>
                    </html>""", "utf-8"
                )
            )
        elif self.path == '/tasks':
            self.wfile.write(self.render_pending_tasks())
        elif self.path == '/completed':
            self.wfile.write(self.render_completed_tasks())
        else:
            self.wfile.write(bytes(self.css+"404", "utf-8"))

    def do_POST(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        cli_args = body.decode("utf-8").split("=")[1].split("+")

        command = None
        arguments = None
        if len(cli_args) == 0:
            raise Exception("Arguments not supplied")
        elif len(cli_args) == 1:
            command = cli_args[0]
        if len(cli_args) > 1:
            command = cli_args[0]
            arguments = cli_args[1:]
        
        content = TasksCommand().run(command, arguments).replace("\n", "<br>")
        content = content + """<br>
            <button onclick='window.location.href = \"http://127.0.0.1:8000/\"'>
            Back
            </button>
        """
        self.wfile.write(bytes(content, "utf-8"))
        

address = ('127.0.0.1', 8000)
server = HTTPServer(address, MyServer)
server.serve_forever()
