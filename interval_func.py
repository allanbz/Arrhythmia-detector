from file_func import read_file

# Normal (N) and abnormal (rest) beat symbols according to PhysioBank Annotations
# Annotations available at: https://archive.physionet.org/physiobank/annotations.shtml
beat_annotations = ['N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r',
					'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?']

def create_intervals(patient_id, interval_size):
	# Read patient file
	ecg_signal, ecg_symbol, ecg_index = read_file(patient_id)

	# Get all valid intervals and the respective beat type from patient ECG signal
	# Valid interval: 5 seconds of sample, starting with a beat
	# Beat type: 0 - normal / 1 - abnormal
	intervals = []
	beat_types = []

	# For each beat, check if it generates a valid interval and if beat type is normal
	for symbol, index in zip(ecg_symbol, ecg_index):
		if symbol in beat_annotations:
			interval_end = index + interval_size
			if interval_end < len(ecg_signal):
				interval = ecg_signal[index:interval_end]
				intervals.append(interval)
				beat_type = 0 if symbol == 'N' else 1
				beat_types.append(beat_type)

	return intervals, beat_types