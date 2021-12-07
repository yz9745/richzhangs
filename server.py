from waitress import serve
from richzhangs import app

serve(app.server, host='localhost', port=3000)
