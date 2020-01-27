import wfdb

# Path to database files
# Database available at: https://physionet.org/content/mitdb/1.0.0/
database_path = 'mit-bih-arrhythmia-database-1.0.0/'

def read_file(patient_id):
	# Define file path and read patient info
	file_path = database_path + patient_id

	record = wfdb.rdrecord(file_path)
	annotations = wfdb.rdann(file_path, 'atr')

	# Get ECG signal from patient record
	ecg_signal = record.p_signal[:, 0]

	# Get annotation symbols and indexes related to the ECG signal
	ecg_symbol = annotations.symbol
	ecg_index = annotations.sample

	return ecg_signal, ecg_symbol, ecg_index