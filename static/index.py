from string import Template
INDEX_TEMPLATE = Template("""<!DOCTYPE html>
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

    <h1>Output</h1>
    <div id="output"></div>
</body>
</html> """)