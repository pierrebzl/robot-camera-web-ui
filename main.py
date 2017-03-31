#!/usr/bin/env python3
from multiprocessing import Process, Queue
from importlib import import_module
from robot import Robot
import sys
import server
import os, re

def start_flask_app(app):
    app.run(debug=True, threaded=True, port=8080, host='0.0.0.0')


def start_robot_master(q):
    robot = Robot(q)
    robot.run()

if __name__ == '__main__':
    env = sys.argv[1] if len(sys.argv) == 2 else 'default'
    config = import_module('conf.%s' % env).config

    os.system("rm -f static/*.jpg")

    q = Queue()
    flask_app = server.setup(q)

    p_flask = Process(target=start_flask_app, args=(flask_app,))
    p_flask.start()

    p_robot = Process(target=start_robot_master, args=(q,))
    p_robot.start()
    p_robot.join()
