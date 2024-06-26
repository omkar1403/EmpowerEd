import random
import pandas as pd
from datetime import datetime
import indian_names

# Function to generate realistic UCID numbers
def generate_ucid_number():
    ucid = '2' + ''.join(random.choices('0123456789', k=9))
    return f"{ucid}"


# Function to generate random date between April 2017 and April 2024
def generate_random_date():
    start_date = datetime(2017, 4, 1)
    end_date = datetime(2024, 4, 30)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%Y-%m-%d")

# Function to generate random remarks
def generate_remarks():
    remarks_list = [
        "Excellent performance in last semester.",
        "Active participant in extracurricular activities.",
        "Top scorer in the recent quiz competition.",
        "Consistent attendance throughout the academic year.",
        "Received special recognition for outstanding project work.",
        "Demonstrated strong leadership skills in group projects.",
        "Well-prepared and actively engaged during class discussions.",
        "Received positive feedback from mentors and instructors.",
        "Strong potential for future academic and professional success.",
        "Demonstrated dedication and commitment to academic excellence."
    ]
    return random.choice(remarks_list)

# Dummy data generation function
def generate_dummy_data(num_records):
    data = []
    for i in range(1, num_records+1):
        record_no = i
        date = generate_random_date()  # Random date between April 2017 and April 2024
        name = indian_names.get_full_name()
        ucid_number = generate_ucid_number()
        class_ = random.choice(["EXTC", "CSE-DS", "CSE-AIML", "COMPS"])  
        mobile_number = f"98765{random.randint(10000, 99999)}"
        sanctioned_amount = random.randint(100, 2000)  # Sanctioned amount between 100 and 2000
        description_of_scheme = random.choice([
            "External Technical Training Programs",
            "Conference - Seminar - Workshops - Exhibition - Technical Festival",
            "Membership - IET, IEEE, CSI, ASM"
        ])
        remark = generate_remarks()  # Generate random remark
        
        data.append([record_no, date, name, ucid_number, class_, mobile_number, 
                     sanctioned_amount, description_of_scheme, remark])
    
    return data

# Generate dummy data for 1000 records

n=2000
dummy_data = generate_dummy_data(2000)

# Convert to DataFrame
df = pd.DataFrame(dummy_data, columns=[ "Record No.", "Date", "Name of the student", 
                                       "UCID Number", "Class", "Mobile Number", 
                                       "Sanctioned Amount", "Description of Scheme", "Remark"])

# Save DataFrame to Excel

df.to_csv("dummy_data.csv", index=False)

print("Data saved to 'dummy_data.xlsx'.")
