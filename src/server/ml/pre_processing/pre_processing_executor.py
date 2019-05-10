import thread
import time
from Queue import Queue
from src.server.ml.pre_processing.text_pre_processing_utils import load_pp_html_to_db, clean_pp_html_records, \
	split_or_bypass_pp
from src.server.utils.db.tools import db_utils


class PreProcessingExecutor:

	def __init__(self, consumers_number, batch_size):
		self._queue = Queue()
		self._batch_size = batch_size
		self._consumers_number = consumers_number
		self._producer = None
		self._consumers = None

	def start_produce_and_consume(self):
		self._producer = thread.start_new_thread(self._produce_pp, ("producer",))
		self._consumers = self._init_consumers(self._consumers_number)

	def _produce_pp(self, thread_name):
		counter = 0
		while True:
			counter += 1
			print(thread_name + " started to produce " + str(counter) + " times")
			url_records_ok = load_pp_html_to_db(self._batch_size)
			if url_records_ok is None:
				time.sleep(5)
				continue
			self._queue.put(url_records_ok)

	def _init_consumers(self, consumers_number):
		consumers = []
		for i in range(consumers_number):
			thread.start_new_thread(self._consume_pp, ("consumer_" + str(i+1), ))
		return consumers

	def _consume_pp(self, thread_name):
		counter = 0
		while True:
			print(thread_name + " started to consume " + str(counter) + " times")
			counter += 1
			url_records_ok = self._queue.get(block=True)
			cleaned_pp_records = clean_pp_html_records(url_records_ok)
			split_or_bypass_pp(cleaned_pp_records)


db_utils.exec_command("TRUNCATE privacy_policy, privacy_policy_paragraphs, privacy_policy_paragraphs_prediction")

executor = PreProcessingExecutor(consumers_number=3, batch_size=20)
executor.start_produce_and_consume()
while 1:
	pass

