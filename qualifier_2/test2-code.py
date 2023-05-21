import json
import hashlib
import pandas as pd
import matplotlib.pyplot as plt

# Function to check if a phone number is valid
def is_valid_phone_number(number):
    if number is None:
        return False
    # Remove any non-digit characters from the number
    number = ''.join(filter(str.isdigit, number))
    # Check if the number is a valid Indian phone number
    if len(number) == 10 and number[0] in ['7', '8', '9']:
        return True
    else:
        return False

file_path = r'D:\PRINCE\Downloads\bajaj_test\qualifier_2\DataEngineeringQ2.json'

# provided json file
with open(file_path) as file:
    data = json.load(file)

# Extract the required columns
columns = ['appointmentId', 'phoneNumber', 'patientDetails.firstName', 'patientDetails.lastName', 'patientDetails.gender', 'patientDetails.birthDate', 'consultationData.medicines']
df = pd.json_normalize(data, sep='_')[columns]

# Create a derived column fullName
df['fullName'] = df['patientDetails.firstName'] + ' ' + df['patientDetails.lastName']

# Add a column isValidMobile of boolean
df['isValidMobile'] = df['phoneNumber'].apply(is_valid_phone_number)

# Add a column phoneNumberHash
df['phoneNumberHash'] = df['phoneNumber'].apply(lambda x: hashlib.md5(x.encode()).hexdigest())

# Rename the birthDate column as DOB
df = df.rename(columns={'patientDetails.birthDate': 'DOB'})

# Calculate the age based on DOB
df['Age'] = pd.to_datetime('today').year - pd.to_datetime(df['DOB']).dt.year

# Count the number of medicines
df['noOfMedicines'] = df['consultationData.medicines'].apply(lambda x: len(x))

# Count the number of active and inactive medicines
df['noOfActiveMedicines'] = df['consultationData.medicines'].apply(lambda x: sum(medicine['IsActive'] for medicine in x))
df['noOfInActiveMedicines'] = df['consultationData.medicines'].apply(lambda x: sum(not medicine['IsActive'] for medicine in x))

# Extract names of active medicines separated by comma
df['MedicineNames'] = df['consultationData.medicines'].apply(lambda x: ', '.join(medicine['medicineName'] for medicine in x if medicine['IsActive']))

# Export the dataframe to a CSV file
df.to_csv('output.csv', sep='~', index=False)

# Create the aggregated data
aggregated_data = {
    'Age': df['Age'].mean(),
    'gender': df['patientDetails.gender'].value_counts().to_dict(),
    'validPhoneNumbers': df['isValidMobile'].sum(),
    'appointments': len(df),
    'medicines': df['noOfMedicines'].sum(),
    'activeMedicines': df['noOfActiveMedicines'].sum()
}

# Export the aggregated data to a JSON file
with open('aggregated_data.json', 'w') as file:
    json.dump(aggregated_data, file)

# Plot a pie chart for number of appointments against gender
gender_counts = df['patientDetails.gender'].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%')
plt.title('Appointments by Gender')
plt.show()
