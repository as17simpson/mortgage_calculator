import streamlit as st
import pandas as pd
import plotly.express as px


with st.form("Calculator"):
    amount_borrowed = st.number_input("How much did you borrow?", min_value=0, step=1)
    interest_rate = st.number_input("What is your interest rate (%)?", min_value=0.00, max_value=100.0, step=0.01)
    term = st.number_input("What is your mortgage term?", min_value=0, step=1)
    years_passed = st.number_input("How many years have passed?", min_value=0, step=1)

    submitted = st.form_submit_button("calculate")


interest_rate = interest_rate/100

def equity(amount_borrowed, interest_rate, term, years_passed):
    return  amount_borrowed - (amount_borrowed*(((1+ interest_rate/12)**(term*12)) - ((1+interest_rate/12)**(years_passed*12)))/ ((1+interest_rate/12)**(term*12) -1))

def mortgage_repayments(amount_borrowed, interest_rate, term):
    return amount_borrowed*(interest_rate/12)*((1+interest_rate/12)**(term*12))/((1+interest_rate/12)**(term*12) - 1)

if submitted:
    if years_passed == 0:
        st.warning("Please enter a non zero value for B")
    else:
        equity_in_house = equity(amount_borrowed, interest_rate, term, years_passed)
        #equity_in_house = amount_borrowed - (amount_borrowed*(((1+ interest_rate/12)**(term*12)) - ((1+interest_rate/12)**(years_passed*12)))/ ((1+interest_rate/12)**(term*12) -1))
        st.write(f"Your equitey in the house after {years_passed} years is: £{round(equity_in_house)}")
        equity_range = []
        for year in range(term+1):
            equity_range.append(equity(amount_borrowed, interest_rate, term, year))
        
        df = pd.DataFrame([equity_range], columns = list(range(term + 1)))
        st.dataframe(df.style.format("£{:,.0f}"))
        print(equity_range)

        df2 = pd.DataFrame({"Year": list(range(term+1)), "Equity": equity_range})
        st.write(f"Your monthly mortgage repayments are: £{round(mortgage_repayments(amount_borrowed, interest_rate, term))}")

        fig = px.line(df2, x="Year", y="Equity", title = "Equity in house")
        fig.update_traces(mode="lines+markers")
        st.plotly_chart(fig, use_container_width=True)


# $B4 - ($B4*(((1+$A4/12)^($H4*12))-((1+$A4/12)^(I$3*12)))/((1+$A4/12)^($H4*12)-1))
# B4 = Amount borrowed, A4 = interest rate, H4 = Term, I3 = years passed

# $B4*(($A4/12)*(1+$A4/12)^(C$3*12))/((1+$A4/12)^(C$3*12)-1)
# C3 = term, 

