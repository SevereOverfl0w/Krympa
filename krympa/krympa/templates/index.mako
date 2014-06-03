<!DOCTYPE html>
<html>
<head>
    <title>${project}</title>
</head>
<body>
    <header id="header">
        <h1 id="title">${project} URL Shortener</h1>
        <img src="${request.static_url('krympa:static/logo.png')}" />
    </header>
    <section id="shortener">
        <form action="${request.route_url('api')}" method="POST" id="shortenForm">
            <label id="urlLabel" for="url">URL</label>
            <input type="text" name="url" id="urlInput" />
            <button type="submit" id="shortenBtn">Submit</button>
        </form>
    </section>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="${request.static_url('krympa:static/app.js')}"></script>
</body>
</html>
