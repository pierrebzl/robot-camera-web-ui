import logging
import traceback
from time import sleep
from multiprocessing import Process

import RPi.GPIO as GPIO
import time

import sys
from importlib import import_module
GPIO.setmode(GPIO.BCM)
env = sys.argv[1] if len(sys.argv) == 2 else 'default'
config = import_module('conf.%s' % env).config


class Robot:

    def __init__(self, q):

        self.q = q
        self.worker_process = None

        self.log = logging.getLogger('robot_master')
        self.log.setLevel(logging.INFO)

        # These three blocks of code configure the PWM settings for
        # the two DC motors on the RC car. It defines the two GPIO
        # pins used for the input, starts the PWM and sets the
        # motors' speed to 0
        self.pin_propulsion_ppm = config['PIN_PROP_PPM']
        self.pin_propulsion_sens = config['PIN_PROP_SENS']

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_propulsion_ppm, GPIO.OUT)
        GPIO.setup(self.pin_propulsion_sens, GPIO.OUT)

        self.propulsion = GPIO.PWM(22,100) # pin, frequence
        self.propulsion.ChangeDutyCycle(0)

        # Setting the PWM pins to false so the motors will not move
        # until the user presses the first key
        GPIO.output(self.pin_propulsion_ppm, False)
        GPIO.output(self.pin_propulsion_sens, False)

        self.action_resolver = {
            'stop': self.__stop_current_task,
            'forward': self.__send_task_to_worker,
            'backward': self.__send_task_to_worker,
        }

    def run(self):
        while True:
            task = self.q.get(True)
            action_type = task[0]
            self.log.info('Got task of action type %s.' % action_type)
            self.action_resolver[action_type](task)

    def __start_worker(self, task):
        self.log.info('Instanciating worker.')
        w = WorkerProcess(self.propulsion,
                          self.pin_propulsion_ppm,
                          self.pin_propulsion_sens,
                          task)
        w.run()
        self.log.info('Worker process is done.')

    def __stop_current_task(self, task):
        if self.worker_process and self.worker_process.is_alive():
            self.worker_process.terminate()
            self.worker_process = None
            self.propulsion.stop()
            GPIO.output(self.pin_propulsion_ppm, False)

        else:
            self.log.info('Worker process is already stopped. Ignoring task')
            self.propulsion.stop()
            GPIO.output(self.pin_propulsion_ppm, False)
            return False

        return True

    def __send_task_to_worker(self, task):
        if self.worker_process and self.worker_process.is_alive():
            self.log.info(
                'Worker is not done with the current task. Stoppping task.')
            self.worker_process.terminate()
            self.worker_process = None
            sleep(0.5)

        self.worker_process = Process(target=self.__start_worker, args=(task,))
        self.worker_process.start()


class WorkerProcess():

    def __init__(self, propulsion, pin_propulsion_ppm, pin_propulsion_sens, task):
        self.propulsion = propulsion
        self.pin_propulsion_ppm = pin_propulsion_ppm
        self.pin_propulsion_sens = pin_propulsion_sens
        self.task = task
        self.speed = 0

        self.log = logging.getLogger('gpio_master')
        self.log.setLevel(logging.INFO)

        self.action_resolver = {
            'forward': self.__forward,
            'backward': self.__backward,
        }

    def run(self):
        try:
            self.log.info('Worker going to execute task.')
            self.action_resolver[self.task[0]]()
        except Exception as e:
            self.log.error(e)
            trace = traceback.format_exc()
            self.log.error(trace)

    def __forward(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_propulsion_ppm, GPIO.OUT)
        GPIO.setup(self.pin_propulsion_sens, GPIO.OUT)
        GPIO.output(self.pin_propulsion_ppm, True)
        GPIO.output(self.pin_propulsion_sens, False)

    def __backward(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_propulsion_ppm, GPIO.OUT)
        GPIO.setup(self.pin_propulsion_sens, GPIO.OUT)
        GPIO.output(self.pin_propulsion_ppm, True)
        GPIO.output(self.pin_propulsion_sens, True)

        if(self.speed != 0):
            self.ramp_down()

    def ramp_up(self):
        while self.speed <= config['MAX_DC']:
            self.speed = self.speed + 5
            self.propulsion.ChangeDutyCycle(self.speed)

    def ramp_down(self):
        while self.speed >= 0:
            self.speed = self.speed - 5
            self.propulsion.ChangeDutyCycle(self.speed)
