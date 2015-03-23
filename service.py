import xbmc, xbmcgui
import pigpio
import time
from os import system

class TimerDialogCallback:
	def __init__(self, pi, gpio, timeout, text, callback):
		self.pi = pi
		self.gpio = gpio
		self.timeout = timeout
		self.text = text
		self.callback = callback
		self._last_tick = 0

		pi.set_mode(self.gpio, pigpio.INPUT)
		pi.set_pull_up_down(self.gpio, pigpio.PUD_UP)

		self.cb = self.pi.callback(self.gpio, pigpio.FALLING_EDGE, self._pulse)
	
	def _pulse(self, gpio, level, tick):
		if tick - self._last_tick < 100000:
			return
		self._last_tick = tick;
		dialog = xbmcgui.DialogProgress()
		dialog.create(self.text)

		secs = 0
		increment = 100 / self.timeout

		cancelled = False
		while secs <= self.timeout:

			if (dialog.iscanceled()):
				cancelled = True
				break

			if secs != 0: 
				xbmc.sleep(1000)

			secs_left = self.timeout - secs
			if secs_left == 0: 
				percent = 100
			else: 
				percent = increment * secs

			remaining_display = ('shutting down in %s seconds') % secs_left
			dialog.update(percent, self.text, remaining_display)

			secs += 1

		remaining_display = 'shutting down'
		dialog.update(percent, self.text, remaining_display)
		if cancelled == False:
			self.callback()

def my_func():
	#xbmc.executebuiltin('Shutdown()')
	system('sudo shutdown -h now');

if __name__ == '__main__':
	while system('pidof pigpiod') != 0:
		time.sleep(1)
	time.sleep(1) # wait for pigpio to get a socket-connection...
	pi = pigpio.pi()
	timer = TimerDialogCallback(pi, 10, 10, "Shutting Down", my_func)

	while 1:
		time.sleep(1)
