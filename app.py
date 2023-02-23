import streamlit as st
from datetime import datetime
import time
import json
import asyncio

session_now = datetime.now()
if 'session_now' not in st.session_state:
    st.session_state.session_now = session_now
placeholder3 = st.empty()
with open('streaming_costs.json') as file:
    streamingCosts = json.load(file)


def mill_rate(dollar_amount, frequency_days):
    return dollar_amount/frequency_days/24/60/60*1000
 
def mill_volume(now, period):
    if period == 'Minute':
        return (now - now.replace(second=0, microsecond=0)).total_seconds()
    if period == 'Hour':
        return (now - now.replace(minute = 0, second=0, microsecond=0)).total_seconds()
    if period == 'Day':
        return (now - now.replace(hour = 0, minute = 0 , second=0, microsecond=0)).total_seconds()
    if period == 'Month':
        return (now - now.replace(day = 1, hour = 0, minute = 0,second=0, microsecond=0)).total_seconds()
    if period == 'Year':
        return (now - now.replace(month = 1, day = 1, hour = 0, minute = 0, second=0, microsecond=0)).total_seconds()

async def live_mill_rate_accumulation(mill_rates, containers):
    while True:
        now = datetime.now()
        for i in range(len(containers)):
            container = containers[i]
            mill_rate = mill_rates[i]
            with container.container():
                if i == 2:
                    col1,col2 = st.columns(2)
                    col1.metric(":green[Gross Money earned in Mills since opening this webpage]", ((now-st.session_state.session_now).total_seconds()*mill_rates[0]).__round__(5))
                    col2.metric(":green[Adjusted Money earned in Mills since opening this webpage]", ((now-st.session_state.session_now).total_seconds()*mill_rates[1]).__round__(5))
                    col1.metric(":green[Gross Money earned in Dollars since opening this webpage]", ((now-st.session_state.session_now).total_seconds()*mill_rates[0]/1000).__round__(5))
                    col2.metric(":green[Adjusted Money earned in Dollars since opening this webpage]", ((now-st.session_state.session_now).total_seconds()*mill_rates[1]/1000).__round__(5))
                else:
                    col1,col2,col3,col4,col5,col6 = st.columns(6)
                    cols = [col1,col2,col3,col4,col5,col6]
                    headers = ['Unit', 'Minute', 'Hour', 'Day', 'Month', 'Year']
                    for i in range(len(cols)):
                        cols[i].subheader(headers[i])
                    minuteVolume = mill_volume(now, 'Minute')*mill_rate
                    hourVolume = mill_volume(now, 'Hour')*mill_rate
                    dayVolume = mill_volume(now, 'Day')*mill_rate
                    monthVolume = mill_volume(now, 'Month')*mill_rate
                    yearVolume = mill_volume(now, 'Year')*mill_rate
                    
                    col1.write('Mills')
                    col2.write(round(minuteVolume,5))
                    col3.write(round(hourVolume,5))
                    col4.write(round(dayVolume,5))
                    col5.write(round(monthVolume,5))
                    col6.write(round(yearVolume,5))
                    
                    col1.write('Dollars')
                    col2.write(round(minuteVolume/1000,5))
                    col3.write(round(hourVolume/1000,5))
                    col4.write(round(dayVolume/1000,5))
                    col5.write(round(monthVolume/1000,5))
                    col6.write(round(yearVolume/1000,5))
        r = await asyncio.sleep(.01)



st.title("Volumetric Money Flow")
st.header('Introduction to flow')
st.markdown('The flow of water can is a great analog for the flow of money.  Money flows in and out of our lives constantly')
st.markdown("How do we measure flow?")
st.markdown("$Q=V/t$ is the equation for Volume flow rate.  Here $Q$ is equal to the flow rate. $V$ is the volume of water moving and $t$ is the time it takes that volume of water to move")
st.markdown("For money we can define a similar equation.  $M = I/t$ where $M$ is our money flow rate.  $I$ is your income and t is the time it takes you to earn that money.")
st.markdown("We commonly refer to how much we make an hour or our income earned per year.  But, what is your income per second? This is called your **Mill Rate** and it is measured in how many thousandths of a dollar you make a second.  Let's calculate your **Mill Rate**.")


st.header('What is your Mill Rate?')
fourWeekIncome = st.number_input("On average how much do you make in 28 days")
millRateIncome = mill_rate(fourWeekIncome,28)
st.metric(":blue[This is your Mill Rate :droplet:]", millRateIncome.__round__(5))
st.caption("This is how much you have earned in the last minute, hour, day, month, and year")
placeholder = st.empty()
st.caption('Confused why the hour is lower?  This is your rate every hour of the day even when you are sleeping.')


st.subheader('Enter your recurring charges')
st.caption('All of these costs decrease your Mill Rate.  Some by a little, some by a lot.')






rent = st.number_input('How much is your rent')
millRateRent = mill_rate(rent,30)
debt = st.number_input('How much do you pay a month in debt')
millRateDebt = mill_rate(debt, 30)
subcriptions = st.multiselect('Any streaming subcriptions? Select all', streamingCosts.keys())
subcriptionCost = sum([streamingCosts[subcription] for subcription in subcriptions])
millRateSubcriptions = mill_rate(subcriptionCost, 30)
other = st.number_input('Enter any other recurring payments')
millRateOther = mill_rate(other, 30)
millRateRecurring = sum([millRateRent,millRateDebt,millRateSubcriptions, millRateOther])
millRateAdjusted = millRateIncome - millRateRecurring
st.metric(":red[This is how much your Mill Rate is being reduced by from recurring payments. 🩸]", millRateRecurring.__round__(5))
st.metric(":blue[This is your Adjusted Mill Rate :droplet:]", millRateAdjusted.__round__(5), delta = (-1)*millRateRecurring.__round__(5))
placeholder2 = st.empty()


st.header('The Credit Card Problem')
st.markdown("Credit cards affect your flow in an interesting way.  To understand this let's work with a real life example. Suppose your credit card statment begins on January 1st")
st.markdown("And let's say on the 1st you make a $30 dollar purhcase")
st.markdown("And let's say your statments ends 30 days later and for simplicity you decide to pay off your debt exactly 30 days later")
st.markdown("$StatmentStart = 1/1/2023$")
st.markdown('$DateOfPayment = 1/31/2023$')
st.markdown("So the time it took you to pay a $30 transaction was 30 days.  Or in other words, you have 30 days to earn 30 dollars to pay off your credit card bill.  We now have an amount of money and period of time, so we can calculate a Mill Rate")
st.markdown('$C = P/t_{\Delta}$*')
st.markdown('Here $C$ is the flow rate for a credit card transaction. Or how much your flow is decreased. $P$ is the price of your purchase and $t_{\Delta}$ is the amount of time it will take you to pay off this transaction.  In our example we made the purchase on the 1st and paid for it on the 31st so our $t_{\Delta} = 30$')
st.markdown("So now we see the date of our purchase and the start and closing date of our statement effects our money flow rate.  It is more difficult to pay off purchases made at the end of a statement than at the beginning of our statement because you have less time to earn the money you need to pay off the purhcase. There's something your credit card company didn't tell you.")
st.markdown("It makes you wonder... What's the point of having statements at all?  What if instead of paying off an item over 30 days, you paid it off over 30 seconds, or an hour, or 5 days, or 600 days.  And each transactions payoff period was independent of one anothers.")


# st.header('How do credit card payments affect your Mill Rate?')
# st.markdown("Let's look at how a $30 purchase every day on a credit card affects your Mill Rate")
# # st.metric('$30 spent every day')
# lastStatementDayOfMonth = st.date_input('Day of month of Statement Start')
# credit = st.number_input("What is your credit card bill as of right now?")


# placeholder = st.empty()
# for i in range(200000):
#     now = datetime.now()
#     millisecondsSinceMidnight = (
#         now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()*1000
#     lastVal = howMuchSaved
#     howMuchSaved = daysSinceLastStatement*dailyPay - \
#         moneySpentSoFar + millisecondsSinceMidnight*millisecondIncome
#     millisecondsSinceStatement = 1000*60*60 * \
#         24*(now.day-1)+millisecondsSinceMidnight
#     secondsSinceStatement = millisecondsSinceStatement/1000
#     with placeholder.container():
#         a = st.metric(":green[Real time money earnings]",
#                       round(howMuchSaved, 5))
#         b = st.metric(
#             ':green[Second income in Mills(Thousandth of a dollar)]', secondIncome*1000)
#         total_subs = 0
#         for subscription in streaming_costs:
#             c = st.metric(':red[Cost of {} plan per second in Mills(Thousands of a dollar)]'.format(
#                 subscription), streaming_costs[subscription]/30/24/60/60*1000)
#             total_subs += streaming_costs[subscription]
#         d = st.metric(
#             ':red[Cost of all plans per second in Mills(Thousands of a dollar)]', total_subs/30/24/60/60*1000)
#         e = st.metric(
#             ':red[This is how much you pay in rent per second(Thousands of a dollar)]', how_much_rent*1000)
#         # st.metric('Buying power reduction', )
#         h = st.metric(':red[This is your credit spending per second(Thousandth of a dollar)]',
#                       moneySpentSoFar/secondsSinceStatement*1000)
#         adjusted_buying_power = secondIncome*1000 - \
#             (total_subs/30/24/60/60*1000)-how_much_rent * \
#             1000 - moneySpentSoFar/secondsSinceStatement*1000
#         f = st.metric(
#             ':green[Adjusted Second income in Mills(Thousandth of a dollar)]', adjusted_buying_power)
#         g = st.metric(":green[Adjusted Real time money earnings]", round(
#             adjusted_buying_power/1000*secondsSinceStatement, 5))
#         time.sleep(.05)
# st.text('Test if we ever get here')

asyncio.run(live_mill_rate_accumulation([millRateIncome,millRateAdjusted, millRateIncome], [placeholder,placeholder2, placeholder3]))
