import streamlit as st
import math
import datetime
import pandas as pd
import time



st.logo(
    "images/base_image.png",
    link="https://www.zapwithus.com",
    icon_image="images/base_image.png",
)







def runeffect():
    with st.spinner('Setting things up... '):
      for i in range(5):
        st.empty()
        time.sleep(0.5)



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
  if not selected_currency in {"USD", "NGN"}:
    errors.append("You haven't selected any currency.  \nChoose one above and try again.")
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
  "1: Polar" : "Polar",
  "2: Something" : "Something",
  "3: Gear" : "Gear",
  "4: Script" : "Script",
  "5: Wheel" : "Wheel",
  "6: Nothing" : "Nothing",
  "7: Binary" : "Binary"
}
artworkprices = {
  "Polar": {"base": 400000, "max": 1500000},
  "Something": {"base": 1000000, "max": 5000000},
  "Gear": {"base": 400000, "max": 1500000},
  "Script": {"base": 100000, "max": 800000},
  "Wheel": {"base": 400000, "max": 1500000},
  "Nothing": {"base": 1000000, "max": 5000000},
  "Binary": {"base": 400000, "max": 1500000},
}



st.title("Welcome to this other side.")
st.write("This external page was created for you to be able to check the funky arithmetics out. ")
st.title("Brief:")
st.write("7AP stands for Seven Artworks Project. This is intended to be pronunced as 'Zap' after some great works that are underway.  \nMuch has been discussed about this elsewhere which I guess you know about already but if you don't, start checking them out from here: https://www.zapwithus.com/7ap")

st.markdown("---")
st.title("7APs Value Projector")
st.write("For all of the artworks on sale, you can now have a go at what's possible under different scenarios.")
st.write("Start by having their respective base and maximum values set below then add and vary your inputs as much as you'd like.")




col1, col2 = st.columns(2)

with col1:
  choice_options = (
                   "1: Polar",
                   "2: Something",
                   "3: Gear",
                   "4: Script",
                   "5: Wheel",
                   "6: Nothing",
                   "7: Binary",
                   "Enter manually"
                  )
  def update_input_labels():
        runeffect()
        runlabels()


  calc_mode = st.selectbox("Make your choice", choice_options, on_change=update_input_labels, key="calc_value_selection_key")


with col2:
  currency_options = ("...", "USD", "NGN")
  selected_currency = st.selectbox("Select your currency", currency_options, on_change=runeffect, key="currency_selection_key" )
  if selected_currency == "...":
    st.error("⚠️  \n Please select your preferred currency above.")
    currency_symbol = "[You have not made a choice of what currency to use]"
  else:
    currency_symbol = "$" if selected_currency == "USD" else "#"

def quickcheck():
  artwork = check_artworks(st.session_state.calc_value_selection_key)
  if artwork:
          data = artworkprices[artwork]
          if selected_currency == "NGN":
            factor = 1500
            st.session_state.base_key = data["base"]*factor
            st.session_state.max_key = data["max"]*factor
          else:
            st.session_state.base_key = data["base"]
            st.session_state.max_key = data["max"]

def runlabels(modinput = 0):
      if not modinput:
        quickcheck()
      else:
        if calc_mode != "Enter manually":
          st.session_state.calc_value_selection_key = "Enter manually"



#Show description
xx = check_artworks(st.session_state.calc_value_selection_key)
if xx:
  if xx == "Polar":
    position = "1st"
    aboutmessage = "Polar is the first piece of this puzzle.  \n It is an 'empty' card if not for one stroke of 'something.'  \n It is meant to symbolize simplicity, focus and the undying virtue of taking 'calculated chances.'  \n Alternative names explored for this include Alif [the first letter of the Arabic alphabet,] One [the first number for single entities] and Path."
  elif xx == "Something":
    position = "2nd"
    aboutmessage = "Life is a game of cards, we play the ones we are dealt.  \n Though we can't see what other players are holding, we know they will surely add strength to our hands.  \n Being the second 'part' of this puzzle, this piece is centered on the notion that 'something' that's empty is 'nothing' but 'nothing' is 'something' that's empty too.  \n Because everything whole around us are made up of parts, Something is anything and everything and this piece symbolizes potentials.  \n For the very reason that something that's empty is nothing, this piece and the second to the last are valued equal starting out. Alternative names explored for this includes; Eva [meaning life,] Canvas and Chaos."
  elif xx == "Gear":
    position = "3rd"
    aboutmessage = "Gear is the agent of turning point in this grand narrative.  \n As the third piece in this puzzle, it represents the dynamic shift from potential to action.  \n It is the cog that drives the machinery of creation; switching it constantly helps transforms the effect of actions into results.  \n Like a key unlocking new possibilities, Gear is essential to the evolution of the collection. It is the embodiment of progress, the momentum that propels narratives forward.  \n Alternative names explored for this includes; Motion, Struggle and Catalyst."
  elif xx == "Script":
    position = "4th"
    aboutmessage = "Script is the blueprint of the collection, the underlying code that gives form to the abstract.  \n As the fourth and central piece, it represents the mechanics of creation, the framework upon which the other pieces took their form.  \n It is the invisible hand that shapes the visible world.  \n Alternative names explored for this includes; DNA, Program and Skin."
  elif xx == "Wheel":
    position = "5th"
    aboutmessage = "Wheel is the architect of connectivity between systems.  \n As the fifth piece, it represents the intricate web of relationships between everything at play in the making and delivery of the collection.  \n It is the collection's nervous system and can not be collected till the others are all taken.  \n Alternative names explored for this includes; Zed [after the last English alphabet,] Wake [trails of moving things] and Processor [like CPU.]"
  elif xx == "Nothing":
    position = "6th"
    aboutmessage = "Nothing is the void, the antithesis of Something.  \n It is the absence that precedes creation, the emptiness that holds the potential for all existence.  \n As the sixth and second to the last piece in this collection, it represents the cyclical nature of being, a return to the primordial state. Yet, it is not a barren wasteland but a cosmic womb, nurturing the seeds of new beginnings.  \n Nothing is both the end and the start, the alpha and the omega, a paradox of infinite possibility.  \n Alternative names explored for this includes; Phoenix, Ashes and Retrograde."
  elif xx == "Binary":
    position = "7th"
    aboutmessage = "Binary is the culmination of the collection, representing the digital age and the convergence of art and technology.  \n As the seventh and final piece, it symbolizes the complexity arising from simplicity, the infinite possibilities encoded within binary systems.  \n It is a testament to human innovation and our ability to create new realities.  \n Alternative names explored for this includes; Genesis, Perspective and Mirrors."
  else:
    position = "Huh huh..."
    aboutmessage = "You shouldn't be seeing this, something went wrong."
  text = f"<span style='text-decoration: underline;'>{xx}'s Description:</span>"
  st.markdown(text, unsafe_allow_html=True)
  st.write(f"Position in collection: {position}")
  st.success(aboutmessage)








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
  if selected_currency == "NGN":
    st.write("(Converted at NGN1500 for every USD)")
  st.warning("ℹ️  \nThese valuations were independently arrived at by me as a highly discounted sum of the value of resources I had to put forth in bringing this to you. Now it's your turn to value the cost of that which can not be priced; time.  \n You can help by valuing the precious time you've just spent on this too, collecting one of these gems or better yet, joining the ongoing crowdfunding campaign we are running by doing your part on https://www.zapwithus.com")

else:
  st.error("ℹ️  \nYou are now in manual mode. All basic principles still apply.  \n If you've got any concern or inquiry, do leave a note at outreach@zapwithus.com")


bid = st.number_input(bid_placeholder, min_value=1, format="%d", disabled=not selected_currency) 


if check_artworks(st.session_state.calc_value_selection_key):
  st.warning("ℹ️  \nAmounts beyond base and max-values are allowed in bids and the extent to which you extend your 'generousity' to these valuables has been programmed to have massive impact on their projected worth over time.")

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
      if today.day == day_input and today.month == month_input and today.year == year_input:
        sameday = 1
        suffix = "today"
      else:
        sameday = 0
        suffix = f"on {day_input}-{month_input}-{year_input}"
      focusedart = check_artworks(st.session_state.calc_value_selection_key)
      if focusedart:
        prefix = focusedart
      else:
        prefix = "the artwork"
      prefix = f"{prefix}'s worth is projected to be"
      phrase = f"{prefix} approximately {currency_symbol}{value:.2f} {suffix} over about {vf:.2f}% annual growth factor."
      st.success(f"⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇  \n Under the conditions supplied above and 'the correct result of the script' ran, {phrase}")


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

st.markdown("---")

st.write("Got no clue about what any of these means? You can brush up by reading my medium piece: https://medium.com/@teetaofeeq/zapwithuss-7aps-inception-and-beyond-1121eba65345")
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
st.write("Should you choose to collect these works of art, you should understand that neither myself, nor any organization I'm [or would be] affiliated with or anybody for that matter is under any obligation of 'buying back,' fulfilling, enforcing [or anything of these sorts] the presumed or generated values. I know you know this already of course.")
st.write("Collectors can choose to do whatever they like at any point in time with the 'parts' they hold but the 'fair value' of these artworks would always be based on the output of whatever 'the script' yields at any point in time when 'used correctly.'")
st.write("Every details concerning the formula is opensourced and it has purposely been worked into one of the artworks against 'oblivion.'")
st.write("To make and keep this 'sane,' it wouldn't be advisable for anyone at any point in time to part away with any of these works at prices lesser than the greater of thier base values or how much they were last collected for.")
st.write("Should it be [or not be: in all situations] that someone got one for an amount below the base value, the greater of most recent highest purchase amount or base value shall be the 'inherrent' bid price to be used with the script in generating actual values and projections.")
st.write("Yes, we're good now.")
st.write("⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇⬇")
st.write("Visit https://www.zapwithus.com/7ap to learn more.")

st.markdown("---")
st.write("Eagles fly alone till they find like minds. I've already met a handful; some already masters at their arts, others on the path of becoming. I look forward to meeting you too.")
st.markdown("---")
st.write("Always doing my part, I don't know if you will get some of these works now or not but I understand that having planted the right seeds, this will grow. I expect that growth to happen fast but of course, that is not in my control but I'm going to sell out and sell more. Art is life.  \n All proceeds from this are going into Zapwithus and other humanitarian causes. Thanks.")

st.markdown("---")
st.warning("Access the sourcecodes through here: https://github.com/bayor11/7arts-zapwithus")
text = f"<div style='display: flex; justify-content: center;'>©{today.year} Zapwithus  \nAll rights reserved.</div>"
st.markdown(text, unsafe_allow_html=True)