import json
import hashlib

# (c)
def is_valid_phone_number(number):
    if number is None:
        return False
    number = ''.join(filter(str.isdigit, number))
    return len(number) == 10 and number.startswith(('91', '0')) and 6000000000 <= int(number) <= 9999999999

# Function to calculate age based on birth date
def calculate_age(birth_date):
    if birth_date is None:
        return None
    # Extract year from the birth date string
    birth_year = int(birth_date[:4])
    # Calculate the current year
    current_year = 2023
    # Calculate the age
    age = current_year - birth_year
    return age

file_path = r'D:\PRINCE\Downloads\bajaj_test\qualifier_2\DataEngineeringQ2.json'

# provided json file
with open(file_path) as file:
    data = json.load(file)

# final output container
results = []

# (a)
for entry in data:
    result = {}
    result['appointmentId'] = entry.get('appointmentId')
    result['phoneNumber'] = entry.get('phoneNumber')

    # (a)
    patient_details = entry.get('patientDetails')
    result['firstName'] = patient_details.get('firstName')
    result['lastName'] = patient_details.get('lastName')

    # (a)
    gender = patient_details.get('gender')
    if gender == 'M':
        result['gender'] = 'male'
    elif gender == 'F':
        result['gender'] = 'female'
    else:
        result['gender'] = 'others'

    # (a)
    result['DOB'] = patient_details.get('birthDate')

    # (b)
    result['fullName'] = f"{result['firstName']} {result['lastName']}"

    # (c)
    result['isValidMobile'] = is_valid_phone_number(result['phoneNumber'])

    # (d)
    if result['isValidMobile']:
        phone_number_hash = hashlib.sha256(result['phoneNumber'].encode()).hexdigest()
    else:
        phone_number_hash = None
    result['phoneNumberHash'] = phone_number_hash

    # Calculate age
    result['Age'] = calculate_age(result['DOB'])

    # Extract medicines information
    consultation_data = entry.get('consultationData')
    medicines = consultation_data.get('medicines', [])

    # (a.7)
    result['noOfMedicines'] = len(medicines)

    # (f)
    result['noOfActiveMedicines'] = sum(medicine.get('IsActive', False) for medicine in medicines)
    result['noOfInActiveMedicines'] = sum(not medicine.get('IsActive', False) for medicine in medicines)

    # (f)
    active_medicines = [medicine['medicineName'] for medicine in medicines if medicine.get('IsActive', False)]
    result['medicineNames'] = ', '.join(active_medicines)

    # my final output
    results.append(result)

for result in results:
    print(result)
