import xbmc, xbmcgui
import pigpio
import time

class TimerDialogCallback:
	def __init__(self, pi, gpio, timeout, text, callback):
		self.pi = pi
		self.gpio = gpio
		self.timeout = timeout
		self.text = text
		self.callback = callback

		pi.set_mode(self.gpio, pigpio.INPUT)
		pi.set_pull_up_down(self.gpio, pigpio.PUD_UP)

		self.cb = self.pi.callback(self.gpio, pigpio.RISING_EDGE, self._pulse)
	
	def _pulse(self, gpio, level, tick):
		dialog = xbmcgui.DialogProgress()
		dialog.create(self.text)

		secs = 0
		increment = 100 / time_to_wait

		cancelled = False
		while secs <= time_to_wait:

			if (dialog.iscanceled()):
				cancelled = True
				break

			if secs != 0: 
				xbmc.sleep(1000)

			secs_left = time_to_wait - secs
			if secs_left == 0: 
				percent = 100
			else: 
				percent = increment * secs

			remaining_display = ('shutting down in %s seconds') % secs_left
			dialog.update(percent, text, remaining_display)

			secs += 1

		if cancelled == True:     
			self.log_notice('countdown cancelled')
			return False
		else:
			self.log_debug('countdown finished waiting')
			self.callback()

def my_func():
	xbmc.executebuiltin('Shutdown()')

if __name__ == '__main__':
	pi = pigpio.pi()
	timer = TimerDialogCallback(pi, 10, 10, "Shutting Down", my_func)

	while 1:
		time.sleep(1)