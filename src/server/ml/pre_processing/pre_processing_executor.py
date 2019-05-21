import threading
import time
from Queue import Queue
from src.server.ml.pre_processing.text_pre_processing_utils import load_pp_html_to_db, clean_pp_html_records, \
    split_or_bypass_pp, load_pp_from_db
from src.server.utils.db.tools import db_utils


class PreProcessingExecutor:

    def __init__(self, consumers_number, batch_size):
        self._queue = Queue()
        self._batch_size = batch_size
        self._consumers_number = consumers_number
        self._should_stop = False
        self._producer = None
        self._consumers = None

    def start_produce_and_consume(self, timeout=0):
        self._producer = threading.Thread(target=self._produce_pp, args=("producer",))
        self._producer.start()
        self._consumers = self._init_consumers(self._consumers_number)
        if timeout == 0:
            while 1:
                pass
        else:
            time.sleep(timeout)
            self.eliminate()

    def eliminate(self):
        self._should_stop = True
        self._producer.join()
        for i in range(len(self._consumers)):
            self._queue.put([])
        for consumer in self._consumers:
            consumer.join()

    def _produce_pp(self, thread_name):
        counter = 0
        while not self._should_stop:
            counter += 1
            url_records = load_pp_from_db(self._batch_size)
            if url_records is None:
                time.sleep(5)
                continue
            print(thread_name + " started to produce " + str(counter ) + " times")
            self._queue.put(url_records)

    def _init_consumers(self, consumers_number):
        consumers = []
        for i in range(consumers_number):
            consumers.append(threading.Thread(target=self._consume_pp, args=("consumer_" + str(i + 1),)))
            consumers[i].start()
        return consumers

    def _consume_pp(self, thread_name):
        counter = 0
        while not self._should_stop:
            print(thread_name + " started to consume " + str(counter + 1) + " times")
            counter += 1
            url_records = self._queue.get(block=True)
            if len(url_records) == 0:
                continue
            url_records_ok = load_pp_html_to_db(url_records)
            cleaned_pp_records = clean_pp_html_records(url_records_ok)
            split_or_bypass_pp(cleaned_pp_records)


# db_utils.exec_command("TRUNCATE privacy_policy, privacy_policy_paragraphs, privacy_policy_paragraphs_prediction")

executor = PreProcessingExecutor(consumers_number=10, batch_size=5)
executor.start_produce_and_consume(timeout=0)

