<!DOCTYPE html>
<html>
<head>
    <title>${project}</title>
    <link href="${request.static_url('krympa:static/styles/main.css')}" rel="stylesheet" type="text/css">
</head>
<body>
    <main class="main">
        <header id="header">
            <h1 id="title">${project} URL Shortener</h1>
        </header>
        <section id="shortener">
            <form action="${request.route_url('api')}" method="POST" id="shortenForm">
                <input type="text" name="url" id="urlInput" placeholder="Enter link to shorten it." />
                <button type="submit" id="shortenBtn">Shorten</button>
            </form>
        </section>
    </main>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="${request.static_url('krympa:static/js/app.js')}"></script>
</body>
</html>
