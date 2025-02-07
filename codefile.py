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
    expense1 = (income1*total_percent/100)
    expense2 = (income2*total_percent/100)
    remaining = (total_income - expenses) / 2
    return total_percent, remaining, expense1, expense2

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
st.markdown("""
    ## Let's help you answer the question: How to *fairly* split money in your partnership

    There are many options for what can feel ‘fair’ for you! We’ll help you outline the options and think about what’s right for you. 

    1. **50/50 split**: this is usually the first place that people start because before you’ve talked about it, it feels like the easiest thing to each pay for yourself. Usually this means you would put the same amount of money in a joint chequing account and use that for bills, date nights and vacations. 

    It’s rare as you progress in a relationship that this is the right way forwards. It absolutely can be - if you both make enough money to afford the life you want and you don’t mind saving at different rates for the future. But this is rare, especially as life curcumstances change. (Ie. one person taking more time off to be with children, or taking a step back in their career.)

    So what are my other options? 

    2. **Combine finances equally**  
    This is my preferred method because it’s truly equal. The recommendation here is that you fully record / aggregate each person’s income - you use your shared money to pay for your joint expenses, and then you transfer out exactly the same amount of money to your individual accounts to have for personal or ‘fun’ expenses. This is your no guilt, no stress, ‘you’ money. 

    This is generally for partners that are married or have decided this is their ‘life partner’ because the partner who earns more needs to be comfortable that they will be dividing the excess they make with their partner. 

    The way I like to think of it - if you chose to do life with this person, wouldn’t you want them to have the same opportunities as you?

    3. **Split expenses and fun money proportionally**  
    This means that you contribute to your life; expenses, bills, even children according to the amount you make but you also only get that same percentage of ‘fun’ money. 

    So let’s say your partner earns $4,000 and you make $8,000 a month. After paying for all of your bills, savings, investments etc you have $1,000 / month to split for fun money, you would get $333 and they would get $667. 

    This can make sense if you’re proud of your individual achievements and want your spending power to reflect that. One caution is that this can lead to resentment over time. Having unequal access to money in the long run can be tricky for a relationship. 

    4. **Split bills & individual items**  
    This is an interesting one that a lot of people fall into. They’ll start divvying up payments - "you pay for the utilities and car payments, I’ll pay for the mortgage and the groceries". 

    This can work if both people are happy with the arrangement and feel that the split is roughly appropriate according to their incomes or beliefs. The challenge is that both expenses and incomes change on a very consistent basis. This means that you can quickly end up with a situation that looks very different than the one you started with. It’s a lot of effort to be constantly renegotiating how you should be splitting everything up. 

    There are of course varieties to each of these methods! You might do 50/50 generally but one partner pays more for rent, for example. OR you combine expenses fully but you contribute to investment / pension accounts at different rates. Whatever works for you - the important part is DECIDING together and not falling into a trap of just doing whatever is easiest at the time.
""")

st.markdown("Enter your details below.")

# Input for incomes and expenses
income1 = st.number_input("Enter your monthly post-tax income", min_value=0.0, value=0.0)
income2 = st.number_input("Enter your partner's monthly post-tax income", min_value=0.0, value=0.0)
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
        total_percent, remaining, expense1, expense2 = calculate_complete_share(expenses, income1, income2)
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


