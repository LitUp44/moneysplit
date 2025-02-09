import streamlit as st
import pandas as pd

def calculate_percentage_earnings(income1, income2):
    total_income = income1 + income2
    percent1 = (income1 / total_income) * 100 if total_income > 0 else 0
    percent2 = (income2 / total_income) * 100 if total_income > 0 else 0
    return percent1, percent2

def calculate_50_50(expenses, income1, income2):
    share = expenses / 2
    percent1 = (share / income1) * 100 if income1 > 0 else 0
    percent2 = (share / income2) * 100 if income2 > 0 else 0
    remaining1 = income1 - share if income1 > 0 else 0
    remaining2 = income2 - share if income2 > 0 else 0
    return share, percent1, percent2, remaining1, remaining2

def calculate_complete_share(expenses, income1, income2):
    total_income = income1 + income2
    total_percent = (expenses / total_income) * 100 if total_income > 0 else 0
    remaining = (total_income - expenses) / 2 if total_income > 0 else 0
    return total_percent, remaining

def calculate_proportional_expenses(expenses, income1, income2):
    total_income = income1 + income2
    total_percent = (expenses / total_income) * 100 if total_income > 0 else 0
    percent1 = (income1 / total_income) * 100 if total_income > 0 else 0
    percent2 = (income2 / total_income) * 100 if total_income > 0 else 0
    expense1 = (percent1 / 100 * expenses) if total_income > 0 else 0
    expense2 = (percent2 / 100 * expenses) if total_income > 0 else 0
    remaining1 = income1 - expense1 if income1 > 0 else 0
    remaining2 = income2 - expense2 if income2 > 0 else 0
    return percent1, percent2, remaining1, remaining2, expense1, expense2

def calculate_split_by_bills(bills, income1, income2):
    total_expenses = sum([bill[1] for bill in bills])
    total_income = income1 + income2
    bill_share1 = sum([bill[1] for bill in bills if bill[2] == 'Person 1'])
    bill_share2 = sum([bill[1] for bill in bills if bill[2] == 'Person 2'])
    total_bills = bill_share1 + bill_share2
    percent1 = (bill_share1 / income1) * 100 if income1 > 0 else 0
    percent2 = (bill_share2 / income2) * 100 if income2 > 0 else 0
    remaining1 = income1 - bill_share1 if income1 > 0 else 0
    remaining2 = income2 - bill_share2 if income2 > 0 else 0
    return percent1, percent2, remaining1, remaining2, bill_share1, bill_share2

def app_header():
    st.image("Aligned White.png", width=200)  # Adjust image path as needed
    st.markdown("""
        <div style="background-color: #f5724b; padding: 10px; text-align: center; border-radius: 8px;">
            <h1 style="color: #ffeae6; margin: 0;">How should you split your finances?</h1>
        </div>
    """, unsafe_allow_html=True)

# Streamlit interface
app_header()

st.markdown("Use this tool to help you decide how to split your finances with your partner. Enter your details below.")

# Input for incomes and expenses
income1 = st.number_input("Enter your post-tax income", min_value=0.0, value=0.0)
income2 = st.number_input("Enter your partner's post-tax income", min_value=0.0, value=0.0)
expenses = st.number_input("Enter your average monthly expenses", min_value=0.0, value=0.0)

# Calculate Button to trigger calculations and store the result
calculate_button = st.button("Calculate")

# Store the radio button selection and calculations in session_state
if "calculated" not in st.session_state:
    st.session_state.calculated = False  # Track whether calculations were done

# Radio buttons for split options (Horizontal Layout)
st.markdown("""
    <style>
        .stRadio label {
            display: inline-block;
            margin-right: 15px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

option = st.radio("How would you like to split your expenses?", 
                  ('50/50 split', 'Complete share', 'Proportional expenses', 'Split by bills'), key="split_option")

# Update session state on calculate button click
if calculate_button:
    st.session_state.calculated = True

# Display explanatory text below the radio button selection
explanatory_text = {
    '50/50 split': "In this option, both of you will pay half of the total expenses.",
    'Complete share': "In this option, both of you will contribute equally as a percentage of your income.",
    'Proportional expenses': "Here, each person pays an amount proportional to their income.",
    'Split by bills': "In this option, you enter your bills and assign them to either person."
}

# Explanatory text with images and paragraphs
if option == '50/50 split':
    st.markdown("""
        <h3 style='color: #f5724b;'>Explanation:</h3>
        <p>This option means that both individuals will equally split the total expenses. This method is simple and works best when both individuals have similar incomes.</p>
    """, unsafe_allow_html=True)

elif option == 'Complete share':
    st.markdown("""
        <h3 style='color: #f5724b;'>Explanation:</h3>
        <p>This option means that both individuals will contribute an equal percentage of their income to cover the total expenses. It helps in situations where both individuals are making a similar income.</p>
    """, unsafe_allow_html=True)

elif option == 'Proportional expenses':
    st.markdown("""
        <h3 style='color: #f5724b;'>Explanation:</h3>
        <p>In this option, each individual will contribute a percentage of their income based on their respective income. This ensures that both individuals contribute fairly according to their financial capacity.</p>
    """, unsafe_allow_html=True)

elif option == 'Split by bills':
    st.markdown("""
        <h3 style='color: #f5724b;'>Explanation:</h3>
        <p>This option allows individuals to input their individual bills and assign them to either person. It allows for more granular control over who is paying for what, especially in cases where expenses are split differently.</p>
    """, unsafe_allow_html=True)

# Always display the Income Table above the Expenses Table
if st.session_state.calculated and income1 > 0 and income2 > 0 and expenses > 0:
    percent1, percent2 = calculate_percentage_earnings(income1, income2)
    
    # Income Table
    st.markdown("### Income")
    data = {
        'Income': [f"${income1:.2f}", f"${income2:.2f}"],
        '% of Total Income': [f"{percent1:.2f}%", f"{percent2:.2f}%"]
    }
    df = pd.DataFrame(data, index=['You', 'Your Partner'])
    st.table(df)

    # Expenses Table
    st.markdown("### Expenses")
    
    # Define the columns for the Expenses table
    if option == '50/50 split':
        share, percent1, percent2, remaining1, remaining2 = calculate_50_50(expenses, income1, income2)
        expenses_data = {
            'Amount Paid of Joint Expenses': [f"${share:.2f}", f"${share:.2f}"],
            'Percentage of Income Going to Expenses': [f"{percent1:.2f}%", f"{percent2:.2f}%"],
            'Personal Money': [f"${remaining1:.2f}", f"${remaining2:.2f}"]
        }
    
    elif option == 'Complete share':
        total_percent, remaining = calculate_complete_share(expenses, income1, income2)
        expenses_data = {
            'Amount Paid of Joint Expenses': [f"${remaining:.2f}", f"${remaining:.2f}"],
            'Percentage of Income Going to Expenses': [f"{total_percent:.2f}%", f"{total_percent:.2f}%"],
            'Personal Money': [f"${remaining:.2f}", f"${remaining:.2f}"]
        }
    
    elif option == 'Proportional expenses':
        percent1, percent2, remaining1, remaining2, expense1, expense2 = calculate_proportional_expenses(expenses, income1, income2)
        expenses_data = {
            'Amount Paid of Joint Expenses': [f"${expense1:.2f}", f"${expense2:.2f}"],
            'Percentage of Income Going to Expenses': [f"{percent1:.2f}%", f"{percent2:.2f}%"],
            'Personal Money': [f"${remaining1:.2f}", f"${remaining2:.2f}"]
        }
    
    elif option == 'Split by bills':
        st.write("Please fill in the bills to calculate the expenses table.")
        bills = []
        num_bills = st.number_input("How many bills do you want to enter?", min_value=1, step=1)

        for i in range(num_bills):
            bill_name = st.text_input(f"Enter bill name {i+1}")
            bill_amount = st.number_input(f"Enter amount for bill {i+1}")
            person = st.selectbox(f"Who pays for bill {i+1}?", ['Person 1', 'Person 2'], key=i)
            bills.append((bill_name, bill_amount, person))

        if bills:
            percent1, percent2, remaining1, remaining2, bill_share1, bill_share2 = calculate_split_by_bills(bills, income1, income2)
            expenses_data = {
                'Amount Paid of Joint Expenses': [f"${bill_share1:.2f}", f"${bill_share2:.2f}"],
                'Percentage of Income Going to Expenses': [f"{percent1:.2f}%", f"{percent2:.2f}%"],
                'Personal Money': [f"${remaining1:.2f}", f"${remaining2:.2f}"]
            }

    # Display the Expenses table with rows as You and Your Partner
    df_expenses = pd.DataFrame(expenses_data, index=['You', 'Your Partner'])
    st.table(df_expenses)
else:
    st.warning("Please fill in all fields and click 'Calculate' to see the results.")










