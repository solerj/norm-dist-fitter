import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Title and description
st.title("Normal Distribution Fitter")
st.write("""
Use the sliders to adjust the Mean and Standard Deviation to fit a normal distribution to the histogram of randomly generated data.
""")

# Generate data
np.random.seed(42)  # Set seed for reproducibility
random_mean = np.random.uniform(-3, 3)  # Random mean between -1 and 1
random_std = np.random.uniform(0.5, 3)  # Random std between 0.5 and 3
data = np.random.normal(loc=random_mean, scale=random_std, size=1000)

# User inputs for mean and variance
mean = st.slider("Mean", -5.0, 5.0, 0.0, step=0.1)
std = st.slider("Standard Deviation", 0.1, 5.0, 1.0, step=0.1)

# Create histogram and normal distribution
x = np.linspace(-10, 10, 1000)
y = (1 / np.sqrt(2 * np.pi * (std**2))) * np.exp(-0.5 * ((x - mean) ** 2 / (std**2)))

fig, ax = plt.subplots()
ax.hist(data, bins=30, density=True, alpha=0.6, color="green", label="Data Histogram")
ax.plot(x, y, 'r-', lw=2, label="Fitted Normal Distribution")
ax.set_ylim(0, 0.5)
ax.set_xlabel("Value")
ax.set_ylabel("Density")
ax.legend()
ax.set_title("Fitting a Normal Distribution")

# Display the plot in Streamlit
st.pyplot(fig)

# Button to check parameters
if st.button("Check Parameters"):
    st.write(f"**Inputted Mean:** {mean:.2f}, **Actual Mean:** {random_mean:.2f}")
    st.write(f"**Inputted Variance:** {std**2:.2f}, **Actual Variance:** {random_std**2:.2f}")
