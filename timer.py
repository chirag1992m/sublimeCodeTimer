from datetime import datetime, timedelta
import sublime
from sublime_plugin import ApplicationCommand, TextCommand

class CodeCountdownStartCommand(TextCommand):
	TimeValues = ["10 minutes", "15 minutes", "30 minues", "45 minutes", "1 hour"]
	TimeValuesInSeconds = {
		0: 600,
		1: 900,
		2: 1800,
		3: 2700,
		4: 3600
	}

	def run(self, edit):
		if not hasattr(sublime, 'code_timer_isrunning'):
			sublime.code_timer_isrunning = True
		elif sublime.code_timer_isrunning is True:
			sublime.error_message('Code Timer is already running, stop previous first.')
			return
		else:
			sublime.code_timer_isrunning = True

		if sublime.code_timer_isrunning is True:
			self.view.window().show_quick_panel(CodeCountdownStartCommand.TimeValues,
				CodeCountdownStartCommand.onChoose,
				sublime.MONOSPACE_FONT)

	@staticmethod
	def onChoose(choice):
		if choice == -1:
			sublime.code_timer_isrunning = False
		else:
			CodeCountdownStartCommand.decrementTimer(datetime.now(), timedelta(seconds = CodeCountdownStartCommand.TimeValuesInSeconds[choice]))

	@staticmethod
	def decrementTimer(startTime, countDownTime):
		if sublime.code_timer_isrunning is True:
			timeLeft = (startTime - datetime.now()) + countDownTime
			# sublime.status_message("time: {0}".format(timeLeft.total_seconds()))
			if timeLeft.total_seconds() > 0:
				CodeCountdownStartCommand.printStats(timeLeft)
				sublime.set_timeout(lambda: CodeCountdownStartCommand.decrementTimer(startTime, countDownTime),
					100)
			else:
				sublime.code_timer_isrunning = False
				sublime.message_dialog("Your time is up!")

	@staticmethod
	def printStats(timeElapsed):
		seconds = timeElapsed.seconds
		minutes, seconds = divmod(seconds, 60)
		sublime.status_message("Time Left, {0}:{1}".format(minutes, seconds))

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