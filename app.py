import streamlit as st
from datetime import datetime
import time
fourWeekIncome = st.number_input ("28 day pay rate")
lastStatementDayOfMonth = st.date_input ('Day of month of Statement Start').day
daysSinceLastStatement = datetime.now().day - lastStatementDayOfMonth
moneySpentSoFar = st.number_input("How much money have you spent so far")
dailyPay = fourWeekIncome/28
hourlyPay = fourWeekIncome/28/24
minutePay = fourWeekIncome/28/24/60
secondIncome = fourWeekIncome/28/24/60/60
millisecondIncome = secondIncome/1000
howMuchSaved = daysSinceLastStatement*dailyPay-moneySpentSoFar
placeholder = st.empty()
for i in range(200000):
    now = datetime.now()
    millisecondsSinceMidnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0) ).total_seconds()*1000
    lastVal = howMuchSaved
    howMuchSaved = daysSinceLastStatement*dailyPay-moneySpentSoFar + millisecondsSinceMidnight*millisecondIncome 
    with placeholder.container() :
        st.metric("How much you've saved", round (howMuchSaved,4))
        time.sleep(.05)