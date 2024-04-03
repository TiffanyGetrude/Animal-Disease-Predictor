import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import pickle

# Read Data
data = pd.read_csv(r'Animal_Disease_dataset.csv')

# Split x and y values
x = data.drop(['Dangerous','Disease'], axis=1)
y = data['Disease']

# Split x, y into train test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)

# Applying All columns Onehotencoder
onehot = OneHotEncoder()
onehot.fit(x[['AnimalName','symptoms1','symptoms2','symptoms3','symptoms4','symptoms5']])

# Make column transformer
a = make_column_transformer((OneHotEncoder(categories=onehot.categories_, handle_unknown='ignore'), ['AnimalName','symptoms1','symptoms2','symptoms3','symptoms4','symptoms5']), remainder='passthrough')

# Model Creation
model = RandomForestClassifier()

# Pipe Using
pipe = make_pipeline(a, model)

# Fit the pipeline
pipe.fit(x_train, y_train)

# Check Accuracy
test_accuracy = pipe.score(x_test, y_test)
train_accuracy = pipe.score(x_train, y_train)
print("Test Accuracy:", test_accuracy)
print("Train Accuracy:", train_accuracy)

# Save the model
pickle.dump(pipe, open('Random1.pkl', 'wb'))

# Example prediction
example_data = pd.DataFrame([['Snake','Fever','Difficulty breathing','Poor Appetite','Eye and Skin change','Unable to exercise']], columns=['AnimalName','symptoms1','symptoms2','symptoms3','symptoms4','symptoms5'])
prediction = pipe.predict(example_data)
print("Example Prediction:", prediction)
