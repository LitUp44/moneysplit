import streamlit as st

def calculate_percentage_earnings(income1, income2)
    total_income = income1 + income2
    percent1 = (income1 / total_income) * 100
    percent2 = (income2 / total_income) * 100
    return percent1, percent2

# Function to calculate 50/50 split
def calculate_50_50(expenses, income1, income2):
    share = expenses / 2
    percent1 = (share / income1) * 100
    percent2 = (share / income2) * 100
    remaining1 = income1 - share
    remaining2 = income2 - share
    return share, percent1, percent2, remaining1, remaining2

# Function to calculate complete share
def calculate_complete_share(expenses, income1, income2):
    total_income = income1 + income2
    total_percent = (expenses / total_income) * 100
    remaining1 = income1 - (expenses / 2)
    remaining2 = income2 - (expenses / 2)
    return total_percent, remaining1, remaining2

# Function to calculate proportional expenses
def calculate_proportional_expenses(expenses, income1, income2):
    total_income = income1 + income2
    percent1 = (income1 / total_income) * 100
    percent2 = (income2 / total_income) * 100
    expense1 = (expenses * percent1) / 100
    expense2 = (expenses * percent2) / 100
    remaining1 = income1 - expense1
    remaining2 = income2 - expense2
    return percent1, percent2, expense1, expense2, remaining1, remaining2

# Function to calculate split by bills
def calculate_split_by_bills(bills, income1, income2):
    total_expenses = sum([bill[1] for bill in bills])
    total_income = income1 + income2
    bill_share1 = sum([bill[1] for bill in bills if bill[2] == 'Person 1'])
    bill_share2 = sum([bill[1] for bill in bills if bill[2] == 'Person 2'])
    
    percent1 = (bill_share1 / total_income) * 100
    percent2 = (bill_share2 / total_income) * 100
    remaining1 = income1 - bill_share1
    remaining2 = income2 - bill_share2
    return percent1, percent2, remaining1, remaining2

# Streamlit interface
st.title('How should you split your finances?')

st.markdown("Use this tool to help you decide how to split your finances with your partner. Enter your details below.")

# Input for incomes and expenses
income1 = st.number_input("Enter your post-tax income", min_value=0.0, value=0.0)
income2 = st.number_input("Enter your partner's post-tax income", min_value=0.0, value=0.0)
expenses = st.number_input("Enter your average monthly expenses", min_value=0.0, value=0.0)

percent1, percent2 = calculate_percentage_earnings(income1, income2)
st.write(f"You make {percent1:.2f}% of your household income")
st.write(f"Your partner makes {percent2:.2f}% of your household income")

# Radio buttons for split options
option = st.radio("How would you like to split your expenses?", 
                  ('50/50 split', 'Complete share', 'Proportional expenses', 'Split by bills'))

if option == '50/50 split':
    share, percent1, percent2, remaining1, remaining2 = calculate_50_50(expenses, income1, income2)
    st.write(f"Each person pays: ${share:.2f}")
    st.write(f"Person 1 pays {percent1:.2f}% of their income, leaving ${remaining1:.2f} after expenses.")
    st.write(f"Person 2 pays {percent2:.2f}% of their income, leaving ${remaining2:.2f} after expenses.")

elif option == 'Complete share':
    total_percent, remaining1, remaining2 = calculate_complete_share(expenses, income1, income2)
    st.write(f"Each person pays {total_percent:.2f}% of their income for all expenses.")
    st.write(f"Person 1 has ${remaining1:.2f} left after expenses.")
    st.write(f"Person 2 has ${remaining2:.2f} left after expenses.")

elif option == 'Proportional expenses':
    percent1, percent2, expense1, expense2, remaining1, remaining2 = calculate_proportional_expenses(expenses, income1, income2)
    st.write(f"Person 1 pays {percent1:.2f}% of their income, which equals ${expense1:.2f}.")
    st.write(f"Person 2 pays {percent2:.2f}% of their income, which equals ${expense2:.2f}.")
    st.write(f"Person 1 has ${remaining1:.2f} left after expenses.")
    st.write(f"Person 2 has ${remaining2:.2f} left after expenses.")

elif option == 'Split by bills':
    # Collect bills input from the user
    st.write("Enter the bills you want to split.")
    bills = []
    num_bills = st.number_input("How many bills do you want to enter?", min_value=1, step=1)

    for i in range(num_bills):
        bill_name = st.text_input(f"Enter bill name {i+1}")
        bill_amount = st.number_input(f"Enter amount for bill {i+1}")
        person = st.selectbox(f"Who pays for bill {i+1}?", ['Person 1', 'Person 2'], key=i)
        bills.append((bill_name, bill_amount, person))

    # Calculate the split by bills
    if bills:
        percent1, percent2, remaining1, remaining2 = calculate_split_by_bills(bills, income1, income2)
        st.write(f"Person 1 pays {percent1:.2f}% of their income for bills, leaving ${remaining1:.2f} after bills.")
        st.write(f"Person 2 pays {percent2:.2f}% of their income for bills, leaving ${remaining2:.2f} after bills.")

