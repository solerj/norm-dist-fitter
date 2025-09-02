import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Title and description
st.title("Normal Distribution Fitter")
st.write("""
Fit a normal distribution to the data below by adjusting the sliders for the Mean and Standard Deviation. Then click on "Check Parameters" to compare your estimates with the actual parameters of the data.
""")

# Function to generate random data
def generate_data():
    random_mean = np.random.uniform(-3, 3)  # Random mean between -3 and 3
    random_std = np.random.uniform(1, 3)  # Random std between 0.5 and 3
    data = np.random.normal(loc=random_mean, scale=random_std, size=1000)
    return data, random_mean, random_std

# Generate initial data
if "data" not in st.session_state:
    st.session_state.data, st.session_state.random_mean, st.session_state.random_std = generate_data()

# Button to regenerate histogram data
if st.button("Regenerate Histogram"):
    st.session_state.data, st.session_state.random_mean, st.session_state.random_std = generate_data()
    #st.experimental_rerun()

# Retrieve the current data and parameters
data = st.session_state.data
random_mean = st.session_state.random_mean
random_std = st.session_state.random_std

# User inputs for mean and variance
mean = st.slider("Mean", -5.0, 5.0, 0.0, step=0.1)
std = st.slider("Standard Deviation", 0.1, 5.0, 1.0, step=0.1)

# Create histogram and normal distribution
x = np.linspace(-10, 10, 1000)
y = (1 / np.sqrt(2 * np.pi * (std**2))) * np.exp(-0.5 * ((x - mean) ** 2 / (std**2)))

fig, ax = plt.subplots()
ax.hist(data, bins=30, density=True, alpha=0.6, color="green", label="Histogram")
ax.plot(x, y, 'r-', lw=2, label="Fitted Normal Distribution")
ax.set_ylim(0, 0.5)
ax.set_xlabel("Value")
ax.set_ylabel("Density")
ax.legend()
ax.set_title("Fitting a Normal Distribution")

# Display the plot in Streamlit
st.pyplot(fig)

random_mean_data = np.mean(data)
random_std_data = np.std(data)

# Button to check parameters
if st.button("Check Parameters"):
    st.write(f"**Inputted Mean:** {mean:.2f}, **Actual Mean:** {random_mean_data:.2f}")
    st.write(f"**Inputted Standard Deviation:** {std:.2f}, **Actual Standard Deviation:** {random_std_data:.2f}")

    error = round(abs(mean-random_mean_data)/random_mean_data*100,1)
    if error<10
        st.write(f"""
        Amazing! You were very close. Your error is just {error:.2f}%. Well done.
        """)
    else
        st.write(f"""
        Ouch! Some thing went wrong. There is a difference of {error:.2f}% between your estimate and the actual mean. Try again.
        """)





