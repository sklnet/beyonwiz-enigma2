from Components.Console import Console
from config import config
from enigma import eTimer

# _session = None
#
def AutoNTPSync(session=None, **kwargs):
	global ntpsyncpoller
	ntpsyncpoller = NTPSyncPoller()
	ntpsyncpoller.start()

class NTPSyncPoller:
	"""Automatically Poll NTP"""
	def __init__(self):
		# Init Timer
		self.timer = eTimer()
		self.Console = Console()

	def start(self):
		if self.ntp_sync not in self.timer.callback:
			self.timer.callback.append(self.ntp_sync)
		self.timer.startLongTimer(0)

	def stop(self):
		if self.version_check in self.timer.callback:
			self.timer.callback.remove(self.ntp_sync)
		self.timer.stop()

	def ntp_sync(self):
		if config.misc.SyncTimeUsing.value == "1":
			self.Console.ePopen('/usr/bin/ntpdate -s -u pool.ntp.org', self.update_schedule)

	def update_schedule(self, result = None, retval = None, extra_args = None):
		print '[Time By]: Update NTP'
		self.timer.startLongTimer(int(config.misc.useNTPminutes.value) * 60)