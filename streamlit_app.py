import streamlit as st
import math
import datetime
import pandas as pd
import time




def show_loading_message():
  with st.spinner('Calculating'):
    for i in range(5):
      st.empty()
      time.sleep(0.5)

def calculate_value_factor(maxvalue, bv, bid):
  if bid < bv:
    raise ValueError("Bid cannot be less than base value")

  midvalue = (maxvalue + bv) / 2

  if bid <= maxvalue:
    value_factor = 1 + (bid - bv) / (maxvalue - bv) * 5
    return max(value_factor, 1)
  else:
    excess = bid - maxvalue
    quadratic_factor = 6 + (excess / midvalue) ** 2
    return quadratic_factor

def calculate_value(base_value, maxvalue, bid, year, month, day):
  dgr = 0.0012 #approximation of 50percent spread over a period of 1 year as base value 
  try:
    date_obj = datetime.date(year, month, day)
    day_of_year = int(date_obj.strftime('%j'))
  except ValueError as e:
    raise ValueError(f"Invalid date: {e}")

  value_factor = calculate_value_factor(maxvalue, base_value, bid)
  value = base_value * (1 + (dgr * value_factor)) ** ((year - 2024) * 365 + day_of_year)
  return value

def validate_input(base_value, maxvalue, bid, year, month, day):
  errors = []
  if not isinstance(base_value, int):
    errors.append("Base Value must be an integer.")
  if not isinstance(maxvalue, int):
    errors.append("Maximum Value must be an integer.")
  if not isinstance(bid, int):
    errors.append("Bid Price must be an integer.")
  if not isinstance(year, int):
    errors.append("Year must be an integer.")
  if not isinstance(month, int):
    errors.append("Month must be an integer.")
  if not isinstance(day, int):
    errors.append("Day must be an integer.")

  if base_value <= 0:
    errors.append("Base Value must be greater than 0.")
  if maxvalue <= base_value:
    errors.append("Maximum Value must be greater than Base Value.")
  if bid < base_value:
    errors.append("Bid Price cannot be less than Base Value.")
  if year < 2024:
    errors.append("Year must be greater than or equal to 2024.")
  if month < 1 or month > 12:
    errors.append("Month must be between 1 and 12.")
  if day < 1 or day > 31:
    errors.append("Day must be between 1 and 31.")

  try:
    datetime.date(year, month, day)
  except ValueError as e:
    errors.append(f"Invalid date: {e}")
  return errors




def check_artworks(selected):
  if selected in artworks: 
    return artworks[selected]
  else:
    return 0
artworks = {
  "1: Alif" : "Alif",
  "2: Buy One" : "Buy One",
  "3: No Change" : "No Change",
  "4: Ejo" : "Ejo",
  "5: five" : "five",
  "6: six" : "six",
  "7: Seven" : "Seven"
}
artworkprices = {
  "Alif": {"base": 111, "max": 122},
  "Buy One": {"base": 211, "max": 222},
  "No Change": {"base": 311, "max": 322},
  "Ejo": {"base": 411, "max": 422},
  "five": {"base": 511, "max": 522},
  "six": {"base": 611, "max": 622},
  "Seven": {"base": 711, "max": 722},
}



st.title("Welcome to this other side.")
st.write("This external page was created for you to be able to check the funky arithmetics out. ")
st.title("Brief:")
st.write("7AP stands for Seven Artworks Project. This is intended to be pronunced as 'Zap' after some great works that are underway.  Much has been discussed about this elsewhere which I guess you know about already but if you don't, do check it out here: https://www.zapwithus.com/7ap")

st.markdown("---")
st.title("7APs Value Projector")
st.write("For all of the artworks on sale, you can now have a go at what's possible under different scenarios.")
st.write("Start by having their respective base and maximum values set below then add and vary your inputs as much as you'd like.")

col1, col2 = st.columns(2)
with col1:
  currency_options = ("NGN", "USD")
  selected_currency = st.selectbox("Select your currency", currency_options)
  currency_symbol = "$" if selected_currency == "USD" else "#"
if not selected_currency:
  st.warning("Please select your preferred currency")



def quickcheck():
  artwork = check_artworks(st.session_state.calc_value_selection_key)
  if artwork:
          data = artworkprices[artwork]
          st.session_state.base_key = data["base"]
          st.session_state.max_key = data["max"]

def runlabels(modinput = 0):
      artwork = check_artworks(st.session_state.calc_value_selection_key)
      if not modinput:
        quickcheck()
      else:
        if calc_mode != "Enter manually":
          st.session_state.calc_value_selection_key = "Enter manually"


with col2:
  choice_options = ("Enter manually",
                  "1: Alif",
                   "2: Buy One",
                   "3: No Change",
                   "4: Ejo",
                   "5: five",
                   "6: six",
                   "7: Seven")
  def update_input_labels():
        show_loading_message()
        runlabels()


  calc_mode = st.selectbox("Make a choice", choice_options, on_change=update_input_labels, key="calc_value_selection_key")








#Show description
xx = check_artworks(st.session_state.calc_value_selection_key)
if xx:
  aboutmessage = ""
  if xx == "Alif":
    aboutmessage += "1"
  
  st.success(f"{xx}'s Description:\? {aboutmessage}")








defaultbasetext = f"Enter base value of artwork ({currency_symbol})"if selected_currency else"Select your currency"
defaultmaxtext = f"Enter max-value of artwork ({currency_symbol})"if selected_currency else"Select your currency"
nameofpiece = check_artworks(st.session_state.calc_value_selection_key)
if calc_mode != "Enter manually" and nameofpiece:
  quickcheck()
  basetext = f"{nameofpiece}'s base value ({currency_symbol})"if selected_currency else"Select your currency"
  maxtext = f"{nameofpiece}'s max-value ({currency_symbol})"if selected_currency else"Select your currency"
else:  
  basetext = defaultbasetext
  maxtext = defaultmaxtext


def maxcallback():
  currentvalue = st.session_state.max_key
  runlabels(currentvalue) 
      
def basecallback():
  currentvalue = st.session_state.base_key
  runlabels(currentvalue) 

col3,  col4 = st.columns(2)
bid_placeholder = f"Enter your bid price ({currency_symbol})"if selected_currency else"Select your currency"
with col3:
  base_value = st.number_input(basetext, min_value=1, format="%d", on_change=basecallback, key="base_key", disabled=not selected_currency)

col3, col4 = st.columns(2)
with col4:
  maxvalue = st.number_input(maxtext, min_value=1, format="%d", on_change=maxcallback, key="max_key", disabled=not selected_currency)

#show or hide comment
if check_artworks(st.session_state.calc_value_selection_key):
  st.success("These valuations were independently arrived at by me as a highly discounted sum of the value of resources I had to put forth in bringing this to you. Now it's your turn to value the cost of that which can not be priced; time.\n Perhaps you can help us out by valuing the priceless time you've spent on this too or better yet, collecting one of these gems.")
else:
  st.error("You are in manual mode. Are you testing this? If anything funky comes up you can reach out to us and leave a note when you visit https://www.zapwithus.com")


bid = st.number_input(bid_placeholder, min_value=1, format="%d", disabled=not selected_currency) 

st.write("(Amounts beyond base and max-values are allowed in bids and the extent to which you extend 'your generousity' to these valuables has been programmed to have massive impact on their individual worth over time.)")
today = datetime.date.today()

st.markdown("---")
st.write("Modify or leave this part on today's date.")
col5, col6, col7 = st.columns(3)
with col5:  
  year_input = st.number_input("Year", value=today.year, min_value=2024, format="%d")
with col6:
  month_input = st.number_input("Month of the year", value=today.month, min_value=1, max_value=12, format="%d")
with col7:  
  day_input = st.number_input("Day of the month", value=today.day, min_value=1, max_value=31, format="%d")

st.markdown("---")
st.write("Brace up...")
col8, col9, col10 = st.columns(3)
with col8:
  if st.button("Calculate Value"):
    show_loading_message()
    errors = validate_input(base_value, maxvalue, bid, year_input, month_input, day_input)
    if errors:
      for error in errors:
        st.error(error)
    else:
      value = calculate_value(base_value, maxvalue, bid, year_input, month_input, day_input)
      vf = calculate_value_factor(maxvalue, base_value, bid)
      vf = vf*0.0012*365*100
      st.success(f"Artwork Value: {currency_symbol}{value:.2f} under about {vf:.2f}% annual growth factor.")


def next_20_days_value(base_value, maxvalue, bid, start_date, currency_symbol):
  values = []
  for i in range(21):
    next_day = start_date + datetime.timedelta(days=i)
    year, month, day = next_day.year, next_day.month, next_day.day
    value = calculate_value(base_value, maxvalue, bid, year, month, day)
    values.append((next_day.strftime('%Y-%m-%d'), f"{currency_symbol}{value:.2f}"))
  return values

with col9:
  if st.button("Next 20 Days"):
    show_loading_message()
    errors = validate_input(base_value, maxvalue, bid, year_input, month_input, day_input)
    if errors:
      for error in errors:
        st.error(error)
    else:
      start_date = datetime.date(year_input, month_input, day_input)
      next_20_days_data = next_20_days_value(base_value, maxvalue, bid, start_date, currency_symbol)
      st.subheader("⬇⬇⬇⬇⬇⬇⬇⬇")
      st.table(pd.DataFrame(next_20_days_data, columns=["Date", "Value"]))

def next_10_years_value(base_value, maxvalue, bid, start_year, currency_symbol):
  errors = []  # Define errors here
  values = []
  for year in range(start_year, start_year + 11):
    last_day_of_year = datetime.date(year, 12, 31)
    try:
      value = calculate_value(base_value, maxvalue, bid, year, 12, 31)
      values.append((last_day_of_year.strftime('%Y-%m-%d'), f"{currency_symbol}{value:.2f}"))
    except Exception as e:
      errors.append(f"Error calculating value for {last_day_of_year}: {e}")
  return values, errors

with col10:
   if st.button("Next 10 Years"):
    show_loading_message()
    errors = validate_input(base_value, maxvalue, bid, year_input, month_input, day_input)
    if errors:
      for error in errors:
        st.error(error)
    else:
      start_year = year_input
      next_10_years_data, errors = next_10_years_value(base_value, maxvalue, bid, start_year, currency_symbol)
      st.subheader("⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇")
      if errors:
        for error in errors:
          st.error(error)
      else:
        st.table(pd.DataFrame(next_10_years_data, columns=["Date", "Value"]))
st.write("Got no clue about what any of these means? You can brush up by going through my chat with Gemini to get a hang of it here: https://g.co/gemini/share/9280b3feda5e")
st.write("Don't know the current base and max values for any of the artworks? Find them here for the time being: https://www.zapwithus.com/7ap")


st. markdown("---")

st.title("Looking to get one?")
st.write("This way please: https://www.zapwithus.com/7ap/get-one ")

st.markdown("---")
st.markdown("---")


st.title("Disclaimer⚠️")
st.write("Or, should I say terms?")
st.write("The thing about rules is that there are no rules except those we set for ourselves or choose to follow. I'm not going to drool here at all.")
st.write("Beauty is in the eye of the beholder and only those who understand would appreciate this for what it is and nothing more.")
st.write("Should you choose to collect these works of art, you should understand that neither myself, nor any organization I'm (or would be) affiliated with or anybody for that matter is under any obligation of 'buying back,' fulfilling, enforcing (or anything of these sorts) the presumed or generated values. I know you know this already of course.")
st.write("Collectors can choose to do whatever they like at any point in time with the 'parts' they hold but the 'fair value' of these artworks would always be based on the output of whatever this formular/program yields at any point in time.")
st.write("Every details concerning the formula is opensourced and it has purposely been worked into one of the artworks against 'oblivion.'")
st.write("To make and keep this 'sane,' it wouldn't be advisable for anyone at any point in time to part away with any of these works at prices lesser than the base value that was set for them starting out.")
st.write("Should it be (or not be: in all situations) that someone got it for an amount below the base value, the greater of most recent highest purchase amount or base value shall be the 'inherrent' bid price to be used with the code in generating actual values and projections.")
st.write("Yes, we're good now.")
st.write("⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇")
st.write("Visit https://www.zapwithus.com/7ap to learn more")

st.markdown("---")
st.write("Eagles fly alone till they find like minds. I've already met a handful; some already masters at their arts, others on the path of becoming. I look forward to meeting you.")
st.write("At present time, this was created by me, myself and I. Bayo.")