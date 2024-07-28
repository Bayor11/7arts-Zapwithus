
Source codes for Seven Artworks Project (7AP) Value Projector hosted on Streamlit.  

This was quickly strungged up to run on Streamlit for you to be able to see the calculations in perspective.
You can look it up by visiting 👇 👇 👇 
https://sevenartworks.streamlit.app/


Here's the central script the entire app is based on:


## Recap of the Model

### Formula for Artwork Value

```
Value = BaseValue * (1 + (DGR * ValueFactor))^((Year - 2024) * 365 + DayOfYear)
```

### Value Factor Calculation

```
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

  # Linear increase within the maxvalue range
  if bid <= maxvalue:
    value_factor = 1 + (bid - bv) / (maxvalue - bv) * 5
    return max(value_factor, 1)

  # Quadratic increase beyond the maxvalue range
  else:
    excess = bid - maxvalue
    quadratic_factor = 6 + (excess / midvalue) ** 2
    return quadratic_factor
```

### Summary of Terms

* **Value:** The calculated value of the artwork.
* **BaseValue (BV):** The initial purchase price of the artwork.
* **DGR:** The base daily growth rate (e.g., 0.0012 for approximately 50% annual growth).
* **ValueFactor:** A multiplier for the base daily growth rate, determined by the `calculate_value_factor` function.
* **Year:** The current year (e.g., 2024).
* **DayOfYear:** The day of the year (1-366).
* **maxvalue:** The maximum value used for determining the value factor.
* **bv:** The base value of the artwork (same as BaseValue).
* **bid:** The bid price for the artwork.
* **midvalue:** The average of maxvalue and base value.

### How it Works
* The `calculate_value_factor` function determines a multiplier based on the bid price relative to the base value and maximum value.
* The `valueFactor` is applied to the base daily growth rate to adjust the overall growth rate.
* The adjusted growth rate is compounded over time using the number of days since the start of 2024.
* The final value is calculated by multiplying the base value by the compounded growth factor.

This model provides a flexible framework for valuing artwork based on various parameters and incorporates a dynamic growth rate mechanism.
 
*********************

Brush up on what's going on by visiting:
https://www.zapwithus.com/7AP

🔥 🔥 🔥 