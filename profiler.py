from werkzeug.middleware.profiler import ProfilerMiddleware
from tweetsourcing import create_app

app = create_app()
app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[15])
app.run(debug=True)