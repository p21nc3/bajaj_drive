import json
import matplotlib.pyplot as plt

file_path = r'D:\PRINCE\Downloads\bajaj_test\qualifier_2\DataEngineeringQ2.json'

with open(file_path) as file:
    data = json.load(file)
    
results = []

for entry in data:
    result = {}
    result['appointmentId'] = entry.get('appointmentId')
    result['phoneNumber'] = entry.get('phoneNumber')
    
    patient_details = entry.get('patientDetails')
    if patient_details:
        result['firstName'] = patient_details.get('firstName')
        result['lastName'] = patient_details.get('lastName')
        
        gender = patient_details.get('gender')
        if gender:
            result['gender'] = gender
        else:
            result['gender'] = 'Others'
            
        result['DOB'] = patient_details.get('birthDate')
        
    consultation_data = entry.get('consultationData')
    if consultation_data:
        result['medicines'] = consultation_data.get('medicines')
    
    results.append(result)

# Task 1: Aggregating the data
aggregated_data = {
    'Age': len(results),
    'gender': {
        'male': sum(1 for res in results if res.get('gender') == 'male'),
        'female': sum(1 for res in results if res.get('gender') == 'female'),
        'Others': sum(1 for res in results if res.get('gender') == 'Others')
    },
    'validPhoneNumbers': sum(1 for res in results if res.get('phoneNumber')),
    'appointments': len(results),
    'medicines': sum(len(res.get('medicines', [])) for res in results),
    'activeMedicines': sum(1 for res in results for medicine in res.get('medicines', []) if medicine.get('IsActive'))
}

# Task 2: Plotting a pie chart
gender_counts = [aggregated_data['gender']['male'], aggregated_data['gender']['female'], aggregated_data['gender']['Others']]
labels = ['Male', 'Female', 'Others']
plt.pie(gender_counts, labels=labels, autopct='%1.1f%%')
plt.title('Appointments by Gender')
plt.show()

# Exporting the aggregated data in JSON format
with open('aggregated_data.json', 'w') as outfile:
    json.dump(aggregated_data, outfile)
