import streamlit as st
import math
import datetime
import pandas as pd


def calculate_value_factor(maxvalue, bv, bid):
  """Calculates the value factor based on the given parameters.

  Args:
    maxvalue: The maximum value for the artwork.
    bv: The base value of the artwork.
    bid: The bid for the artwork.

  Returns:
    The calculated value factor.
  """

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
  """Calculates the artwork value based on the given parameters.

  Args:
    base_value: The base value of the artwork.
    dgr: The base daily growth rate.
    maxvalue: The maximum value used for determining the value factor.
    bid: The bid price for the artwork.
    year: The year.
    month: The month.
    day: The day.

  Returns:
    The calculated value of the artwork.
  """
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

st.title("7APs Value Calculator")

currency_options = ("NGN", "USD")
selected_currency = st.selectbox("Currency", currency_options)
currency_symbol = "$" if selected_currency == "USD" else "#"
if not selected_currency:
  st.warning("Please select your preferred currency")

base_value_placeholder = f"Enter Base Value ({currency_symbol})"if selected_currency else"Select your currency"
maxvalue_placeholder = f"Enter Maximum Value ({currency_symbol})"if selected_currency else"Select your currency"
bid_placeholder = f"Enter Bid Price ({currency_symbol})"if selected_currency else"Select your currency"
base_value = st.number_input(base_value_placeholder, min_value=1, format="%d", disabled=not selected_currency)
maxvalue = st.number_input(maxvalue_placeholder, min_value=1, format="%d", disabled=not selected_currency)
bid = st.number_input(bid_placeholder, min_value=1, format="%d", disabled=not selected_currency) 

year_input = st.number_input("Year", min_value=2024, format="%d")
month_input = st.number_input("Month of the year", min_value=1, max_value=12, format="%d")
day_input = st.number_input("Day of the month", min_value=1, max_value=31, format="%d")

if st.button("Calculate Value"):
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

if st.button("Next 20 Days"):
  errors = validate_input(base_value, maxvalue, bid, year_input, month_input, day_input)
  if errors:
    for error in errors:
      st.error(error)
  else:
    start_date = datetime.date(year_input, month_input, day_input)
    next_20_days_data = next_20_days_value(base_value, maxvalue, bid, start_date, currency_symbol)
    st.subheader("Next 20 Days Value")
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

if st.button("Next 10 Years"):
  errors = validate_input(base_value, maxvalue, bid, year_input, month_input, day_input)
  if errors:
    for error in errors:
      st.error(error)
  else:
    start_year = year_input
    next_10_years_data, errors = next_10_years_value(base_value, maxvalue, bid, start_year, currency_symbol)
    st.subheader("Next 10 Years Value")
    if errors:
      for error in errors:
        st.error(error)
    else:
      st.table(pd.DataFrame(next_10_years_data, columns=["Date", "Value"]))