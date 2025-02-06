import streamlit as st

def calculate_percentage_earnings(income1, income2):
    total_income = income1 + income2
    percent1 = (income1 / total_income) * 100
    percent2 = (income2 / total_income) * 100
    return percent1, percent2

def calculate_50_50(expenses, income1, income2):
    share = expenses / 2
    percent1 = (share / income1) * 100
    percent2 = (share / income2) * 100
    remaining1 = income1 - share
    remaining2 = income2 - share
    return share, percent1, percent2, remaining1, remaining2

def calculate_complete_share(expenses, income1, income2):
    total_income = income1 + income2
    total_percent = (expenses / total_income) * 100
    expenses1 = (income1*total_percent)
    expenses2 = (income2*total_percent)
    remaining = (total_income - expenses) / 2
    return total_percent, remaining, expenses1, expenses2

def calculate_proportional_expenses(expenses, income1, income2):
    total_income = income1 + income2
    total_percent = (expenses / total_income) * 100
    percent1 = (income1 / total_income) * 100
    percent2 = (income2 / total_income) * 100
    expense1 = (percent1 / 100 * expenses)
    expense2 = (percent2 / 100 * expenses)
    remaining1 = income1 - expense1
    remaining2 = income2 - expense2
    return percent1, percent2, remaining1, remaining2, expense1, expense2

def calculate_split_by_bills(bills, income1, income2):
    total_expenses = sum([bill[1] for bill in bills])
    total_income = income1 + income2
    bill_share1 = sum([bill[1] for bill in bills if bill[2] == 'Person 1'])
    bill_share2 = sum([bill[1] for bill in bills if bill[2] == 'Person 2'])
    total_bills = bill_share1 + bill_share2
    percent1 = (bill_share1 / income1) * 100
    percent2 = (bill_share2 / income2) * 100
    remaining1 = income1 - bill_share1
    remaining2 = income2 - bill_share2
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

# Store the radio button selection and calculations in session_state
if "calculated" not in st.session_state:
    st.session_state.calculated = False  # Track whether calculations were done

# Radio buttons for split options
option = st.radio("How would you like to split your expenses?", 
                  ('50/50 split', 'Complete share', 'Proportional expenses', 'Split by bills'), key="split_option")

# Calculate Button to trigger calculations and store the result
calculate_button = st.button("Calculate")

# Update session state on calculate button click
if calculate_button:
    st.session_state.calculated = True

# Only proceed with calculations if the button is clicked and inputs are valid
if st.session_state.calculated and income1 > 0 and income2 > 0 and expenses > 0:
    percent1, percent2 = calculate_percentage_earnings(income1, income2)
    st.markdown(f"<h3 style='color: #2f4f4f;'>You make {percent1:.2f}% of your household income</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #2f4f4f;'>Your partner makes {percent2:.2f}% of your household income</h3>", unsafe_allow_html=True)

    # Horizontal Radio Buttons using HTML and CSS
    st.markdown("""
        <style>
            .stRadio label {
                display: inline-block;
                margin-right: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    if option == '50/50 split':
        share, percent1, percent2, remaining1, remaining2 = calculate_50_50(expenses, income1, income2)
        st.markdown(f"<h3 style='color: #f5724b;'>Each person pays: ${share:.2f}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Person 1</strong> pays <span style='color: #228b22;'>{percent1:.2f}%</span> of their income, leaving <span style='color: #228b22;'>${remaining1:.2f}</span> after expenses.</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Person 2</strong> pays <span style='color: #228b22;'>{percent2:.2f}%</span> of their income, leaving <span style='color: #228b22;'>${remaining2:.2f}</span> after expenses.</p>", unsafe_allow_html=True)

    elif option == 'Complete share':
        total_percent, remaining = calculate_complete_share(expenses, income1, income2, expense1, expense2)
        st.markdown(f"<h3 style='color: #f5724b;'>Each person pays: {total_percent:.2f}% of their income for all expenses.</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>You will pay <span style='color: #228b22;'>${expense1:.2f}</span> and your partner will pay <span style='color: #228b22;'>${expense2:.2f}</span>.</p>", unsafe_allow_html=True)
        st.markdown(f"<p>You each have <span style='color: #228b22;'>${remaining:.2f}</span> left after expenses.</p>", unsafe_allow_html=True)

    elif option == 'Proportional expenses':
        percent1, percent2, remaining1, remaining2, expense1, expense2 = calculate_proportional_expenses(expenses, income1, income2)
        st.markdown(f"<h3 style='color: #f5724b;'>You pay: {percent1:.2f}% of the expenses, ${expense1:.2f}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #f5724b;'>Your partner pays: {percent2:.2f}% of the expenses, ${expense2:.2f}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Person 1</strong> has <span style='color: #228b22;'>${remaining1:.2f}</span> left after expenses.</p>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Person 2</strong> has <span style='color: #228b22;'>${remaining2:.2f}</span> left after expenses.</p>", unsafe_allow_html=True)

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

        if bills:
            percent1, percent2, remaining1, remaining2, bill_share1, bill_share2 = calculate_split_by_bills(bills, income1, income2)
            st.markdown(f"<p><strong>Person 1</strong> pays <span style='color: #228b22;'>{percent1:.2f}%</span> of their income for bills, leaving <span style='color: #228b22;'>${remaining1:.2f}</span> after bills. They pay a total of <span style='color: #f5724b;'>${bill_share1:.2f}</span>.</p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Person 2</strong> pays <span style='color: #228b22;'>{percent2:.2f}%</span> of their income for bills, leaving <span style='color: #228b22;'>${remaining2:.2f}</span> after bills. They pay a total of <span style='color: #f5724b;'>${bill_share2:.2f}</span>.</p>", unsafe_allow_html=True)
else:
    st.warning("Please fill in all fields and click 'Calculate' to see the results.")


