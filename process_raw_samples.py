import os
os.environ['RIAK_HOST'] = '127.0.0.1'
os.environ['GOOGLE_STORAGE_BUCKET'] = "auguryresearch"
os.environ['GOOGLE_CLOUD_PROJECT'] = "research-150008"
os.environ['ALGO_SERVICE_BUCKET'] = "algo-service-research"

from sample_processing.sample import SampleFormat
from sample_processing.sample_generator import SessionSampleGenerator
from data_manager.context import DataMissionsContext
from data_manager.tasker import Tasker
import datetime
from file_transfer_manager.file_transfer_manager import FileTransferManager
import calendar
import matplotlib.pyplot as plt


# remember 'research-riak' in terminal to open tunnel to riak

session_id = '5c269f9f4d5f1f0001f9efb7'

ctx = DataMissionsContext(calendar.timegm(datetime.datetime.now().timetuple()))
ftm = FileTransferManager(ctx.logger)

output = Tasker("algo.hw_validity.start", ctx, {"session_id": session_id}).process_tasks()
riak_session = output.get('riak_session')
riak_session_local_samples = ftm.download_samples(riak_session)
sample_gen = SessionSampleGenerator(riak_session_local_samples)

for sample in sample_gen.generate(sensor_type='magnetic'):
    sample_fft = sample.get_data(output_format=SampleFormat.POWER_SPECTRUM)
    plt.figure()
    plt.plot(sample_fft['frequencies'], sample_fft['values'])
plt.show()