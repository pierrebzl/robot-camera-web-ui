#!/usr/bin/env python3
from multiprocessing import Process, Queue

import server


def start_flask_app(app):
    app.run(debug=True, threaded=True, port=8080, host='0.0.0.0')


if __name__ == '__main__':

    q = Queue()
    flask_app = server.setup(q)

    p_flask = Process(target=start_flask_app, args=(flask_app,))
    p_flask.start()

    #print('Starting GPIO master')
    #p_gpio = Process(target=start_gpio_master, args=(q,))
    #p_gpio.start()
    #p_gpio.join()