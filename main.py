import logging

from evreka.__init__ import create_app
from evreka.controller import load_devices_from_db

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':
    load_devices_from_db()
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=4444, use_reloader=False)