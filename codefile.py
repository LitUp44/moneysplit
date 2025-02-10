import streamlit as st
import pandas as pd

# Custom CSS for table styling
st.markdown("""
    <style>
        /* Style for alternating rows - 'You' and 'Your Partner' */
        .streamlit-table tbody tr:nth-child(odd) {
            background-color: #f5724b; /* Orange for "You" row */
            color: #ffeae6; /* Text color for the "You" row */
        }
        .streamlit-table tbody tr:nth-child(even) {
            background-color: #8f4e52; /* Brown for "Your Partner" row */
            color: #ffeae6; /* Text color for the "Your Partner" row */
        }
        
        /* Keep header row background color white */
        .streamlit-table th {
            background-color: white;
            color: black;
        }
        
        /* Style for table columns */
        .streamlit-table td, .streamlit-table th {
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# Function definitions (calculate_percentage_earnings, calculate_50_50, etc.) here...
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
    percent1 = (expenses / income1) * 100 if income1 > 0 else 0
    percent2 = (expenses / income2) * 100 if income2 > 0 else 0
    total_percent = (expenses / total_income) * 100 if total_income > 0 else 0
    paid1 = (expenses*percent1/100) if income1 > 0 else 0
    paid2 = (expenses*percent2/100) if income2 > 0 else 0
    remaining = (total_income - expenses) / 2 if total_income > 0 else 0
    return total_percent, remaining, percent1, percent2, paid1, paid2

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
income1 = st.number_input("Enter your monthly post-tax income", min_value=0.0, value=0.0)
income2 = st.number_input("Enter your partner's monthly post-tax income", min_value=0.0, value=0.0)
expenses = st.number_input("Enter your joint average monthly expenses", min_value=0.0, value=0.0)

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
                  ('50/50 split', 'Complete share', 'Proportional expenses', 'Split by bills'), key="split_option",  horizontal=True)

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
        <p>This is usually the first place that people start because before you’ve talked about it, it feels like the easiest thing to each pay for yourself. Usually, this means you would put the same amount of money in a <strong>joint chequing account</strong> and use that for <strong>bills</strong>, <strong>date nights</strong>, and <strong>vacations</strong>.</p>

        <p>It’s rare as you progress in a relationship that this is the right way forwards. It absolutely can be – if you both make enough money to afford the life you want and you don’t mind saving at different rates for the future. But this is rare, especially as <strong>life circumstances</strong> change. (Ie. one person taking more time off to be with children, or taking a step back in their career.)</p>
    """, unsafe_allow_html=True)
    st.image("5050 split.png", width=700)  # Adjust image path as needed

elif option == 'Complete share':
    st.markdown("""
        <h3 style='color: #f5724b;'>Explanation:</h3>
        <p>With the complete share option, the idea is to fully combine your income in a joint account which you then use to pay for your <strong>joint expenses</strong>. After these have all been paid and money has been saved & invested, you would then transfer out exactly the same amount of money to your individual accounts to have for personal or ‘fun’ money.</p>

        <p>This is your <strong>no guilt, no stress, you</strong> money. This is generally for couples that are married or have decided this is their life partner because the partner who earns more needs to be comfortable that they will be dividing the excess that they make.</p>

        <p>One way to think of it – if you chose to do life with this person, wouldn’t you want them to have the same opportunities as you?</p>
    """, unsafe_allow_html=True)
    st.image("Complete share.png", width=700)  # Adjust image path as needed

elif option == 'Proportional expenses':
    st.markdown("""
        <h3 style='color: #f5724b;'>Explanation:</h3>
        <p>This means that you contribute to your life – <strong>expenses</strong>, <strong>bills</strong>, even <strong>children</strong> – according to the amount you make but you also only get that same percentage of ‘<strong>fun</strong>’ money.</p>

        <p>So let’s say your partner earns $4,000 and you make $8,000 a month. After paying for all of your <strong>bills</strong>, <strong>savings</strong>, <strong>investments</strong>, etc., you have $1,000 / month to split for fun money. You would get $666 and they would get $337. This can make sense if you’re proud of your individual achievements and want your spending power to reflect that.</p>

        <p>One caution is that this can lead to resentment over time. Having unequal access to money in the long run can be tricky for a relationship.</p>
    """, unsafe_allow_html=True)
    st.image("Proportional expenses.png", width=700)  # Adjust image path as needed

elif option == 'Split by bills':
    st.markdown("""
        <h3 style='color: #f5724b;'>Explanation:</h3>
        <p>This is an interesting one that a lot of people fall into. They’ll start divvying up payments – one person pays for the <strong>utilities</strong> and <strong>car payments</strong>, the other the <strong>mortgage</strong> and the <strong>groceries</strong>. This can work if both people are happy with the arrangement and feel that the split is roughly appropriate according to their incomes or beliefs.</p>

        <p>The challenge is that both <strong>expenses</strong> and <strong>incomes</strong> change on a very consistent basis. This means that you can quickly end up with a situation that looks very different than the one you started with. It’s a lot of effort to be constantly renegotiating how you should be splitting everything up.</p>
    """, unsafe_allow_html=True)
    st.image("Split by bills.png", width=700)  # Adjust image path as needed

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

    # Apply the custom CSS class to the table
    st.markdown(df.to_html(classes='streamlit-table', index=True, header=True, escape=False), unsafe_allow_html=True)

    # Define expenses_data before using it, based on the selected option
    if option == '50/50 split':
        share, percent1, percent2, remaining1, remaining2 = calculate_50_50(expenses, income1, income2)
        expenses_data = {
            'Amount paid of joint expenses': [f"${share:.2f}", f"${share:.2f}"],
            'Percentage of income going to expenses': [f"{percent1:.2f}%", f"{percent2:.2f}%"]
        }
    
    elif option == 'Complete share':
        total_percent, remaining, percent1, percent2, paid1, paid2 = calculate_complete_share(expenses, income1, income2)
        expenses_data = {
            'Amount paid of joint expenses': [f"${paid1:.2f}", f"${paid2:.2f}"],
            'Percentage of income going to expenses': [f"{percent1:.2f}%", f"{percent2:.2f}%"]
        }
    
    elif option == 'Proportional expenses':
        percent1, percent2, remaining1, remaining2, expense1, expense2 = calculate_proportional_expenses(expenses, income1, income2)
        expenses_data = {
            'Amount paid of joint expenses': [f"${expense1:.2f}", f"${expense2:.2f}"],
            'Percentage of income going to expenses': [f"{percent1:.2f}%", f"{percent2:.2f}%"]
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
                'Amount paid of joint expenses': [f"${bill_share1:.2f}", f"${bill_share2:.2f}"],
                'Percentage of income going to expenses': [f"{percent1:.2f}%", f"{percent2:.2f}%"]
            }

    # Display the Expenses table with rows as You and Your Partner
    st.markdown("### Expenses")
    df_expenses = pd.DataFrame(expenses_data, index=['You', 'Your partner'])
    st.markdown(df_expenses.to_html(classes='streamlit-table', index=True, header=True, escape=False), unsafe_allow_html=True)

    # Personal Money Table (Third table under expenses)
    st.markdown("### Personal money left over")
    if option == '50/50 split':
        personal_money_data = {
            'Personal money left over': [f"${remaining1:.2f}", f"${remaining2:.2f}"]
        }
    
    elif option == 'Complete share':
        personal_money_data = {
            'Personal money left over': [f"${remaining:.2f}", f"${remaining:.2f}"]
        }
    
    elif option == 'Proportional expenses':
        personal_money_data = {
            'Personal money left over': [f"${remaining1:.2f}", f"${remaining2:.2f}"]
        }
    
    elif option == 'Split by bills':
        personal_money_data = {
            'Personal money left over': [f"${remaining1:.2f}", f"${remaining2:.2f}"]
        }

    # Display the Personal Money table with rows as You and Your Partner
    df_personal_money = pd.DataFrame(personal_money_data, index=['You', 'Your Partner'])
    st.markdown(df_personal_money.to_html(classes='streamlit-table', index=True, header=True, escape=False), unsafe_allow_html=True)

else:
    st.warning("Please fill in all fields and click 'Calculate' to see the results.")











