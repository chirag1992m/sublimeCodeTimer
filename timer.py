from datetime import datetime, timedelta
import sublime
from sublime_plugin import ApplicationCommand

class CodeTimerStartCommand(ApplicationCommand):
	def run(self):
		if not hasattr(sublime, 'code_timer_isrunning'):
			sublime.code_timer_isrunning = True
		elif sublime.code_timer_isrunning is True:
			sublime.error_message('Code Timer is already running, stop previous first.')
			return
		else:
			sublime.code_timer_isrunning = True

		if sublime.code_timer_isrunning is True:
			currentTime = datetime.now()
			CodeTimerStartCommand.incrementTimer(currentTime)

	@staticmethod
	def incrementTimer(startTime):
		if sublime.code_timer_isrunning is True:
			timeElapsed = datetime.now() - startTime
			CodeTimerStartCommand.printStats(timeElapsed)
			sublime.set_timeout(lambda: CodeTimerStartCommand.incrementTimer(startTime),
				100)

	@staticmethod
	def printStats(timeElapsed):
		seconds = timeElapsed.seconds
		hours, seconds = divmod(seconds, 3600)
		minutes, seconds = divmod(seconds, 60)
		sublime.status_message("Time elapsed, {0}:{1}:{2}".format(hours, minutes, seconds))


class CodeTimerStopCommand(ApplicationCommand):
	def run(self):
		if (not hasattr(sublime, 'code_timer_isrunning')) or (sublime.code_timer_isrunning is False):
			sublime.error_message('Code Timer is not running.')
		else:
			sublime.code_timer_isrunning = False
			sublime.status_message("Timer stopped")