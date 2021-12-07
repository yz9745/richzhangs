from waitress import serve
import app

serve(app.server, host='localhost', port=3000)
