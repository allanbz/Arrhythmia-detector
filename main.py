from sklearn.model_selection import train_test_split
from interval_func import create_intervals
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout

# Patient ID list according to database files
patients_id = ['100', '101', '102', '103', '104', '105', '106', '107', '108', '109',
			   '111', '112', '113', '114', '115', '116', '117', '118', '119', '121',
			   '122', '123', '124', '200', '201', '202', '203', '205', '207', '208',
			   '209', '210', '212', '213', '214', '215', '217', '219', '220', '221',
		       '222', '223', '228', '230', '231', '232', '233', '234']

# Interval period to be considered (in seconds)
period = 5

# Sampling rate according to PhysioNet (in Hz or samples per second)
frequency = 360

# Separate patients into training (75%) and testing group (25%)
training_group_size = int(len(patients_id) * 0.75)
training_ids, testing_ids = train_test_split(patients_id, train_size = training_group_size)

## Create training and testing datasets
training_input_dataset = []
training_output_dataset = []
testing_input_dataset = []
testing_output_dataset = []

# Interval size according to sampling rate
interval_size = period * frequency

# For each patient, takes valid sample intervals
ids = [training_ids, testing_ids]
inputs = [training_input_dataset, testing_input_dataset]
outputs = [training_output_dataset, testing_output_dataset]

for _id, _input, _output in zip(ids, inputs, outputs):
	for patient_id in _id:
		intervals, beat_types = create_intervals(patient_id, interval_size)
		_input.extend(intervals)
		_output.extend(beat_types)

# Converting to NumPy array for use in Keras
training_input_dataset = np.array(training_input_dataset)
training_output_dataset = np.array(training_output_dataset)
testing_input_dataset = np.array(testing_input_dataset)
testing_output_dataset = np.array(testing_output_dataset)

# Expading output for standardization
training_output_dataset = np.expand_dims(training_output_dataset, axis=1)
testing_output_dataset = np.expand_dims(testing_output_dataset, axis=1)

## Structuring Neural Network
# Save input size for structuring purposes
input_size = training_input_dataset.shape[1]
output_size = training_output_dataset.shape[1]

# Declares model
model = Sequential()
model.add(Dense(input_size * 2, input_shape = (input_size, ), activation = 'relu'))
model.add(Dropout(0.2))
model.add(Dense(input_size * 2, activation = 'relu'))
model.add(Dense(output_size, activation = 'sigmoid'))

# Compiles model
model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# Training model
model.fit(training_input_dataset, training_output_dataset, epochs = 1, verbose = 1)

# Evaluating model
score = model.evaluate(testing_input_dataset, testing_output_dataset, verbose = 1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])