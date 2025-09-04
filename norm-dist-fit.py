import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os
from openai import OpenAI

# Title and description
st.title("Can you fit a Normal Distribution?")
st.write("""
         Fit a normal distribution to the data below by adjusting the sliders for the Mean and Standard Deviation.
         This will help you build intuition and confidence around the normal distribution.
         When you are happy with your choice of parameter values, click on "Check Parameters" to compare your estimates with the actual parameters of the data.
         If your estimates are off, don't worry! You will be guided on where you went wrong and you can try again.
         
         To repeat the exercise with new data, simply click on "Regenerate Histogram".
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
    # st.write(f"**Inputted Mean:** {mean:.2f}, **Actual Mean:** {random_mean_data:.2f}")
    # st.write(f"**Inputted Standard Deviation:** {std:.2f}, **Actual Standard Deviation:** {random_std_data:.2f}")

    mean_error = abs(mean-random_mean_data)/abs(random_mean_data)*100
    std_error = abs(std-random_std_data)/abs(random_std_data)*100

    if (mean_error<15 and std_error<15):
        st.write(f"**Inputted Mean:** {mean:.2f}, **Actual Mean:** {random_mean_data:.2f}")
        st.write(f"**Inputted Standard Deviation:** {std:.2f}, **Actual Standard Deviation:** {random_std_data:.2f}")
        st.write(f"""
                 Amazing! Your intuition is spot-on! Well done.
                 You can try the exercise again with new data by clicking on "Regenerate Histogram".
                 """)
    #chatbot support ------------------------------------
    elif (mean_error<15 and std_error>=15):
        SYSTEM_PROMPT = f"""
        You are a helpful assistant that answers questions about statistics and data analysis.
        The exercise for the student is to manually adjust sliders that represent the mean and standard deviation of a normal distribution such that it fits a histogram of data as well as possible.
        The actual mean and standard deviation of the data are {random_mean_data:.2f} and {random_std_data:.2f}, respectively.
        The student was close enough on the mean, but was off by at least +/-0.15 error in the standard deviation.
        So guide them where they went wrong and encourage them to try again by adjusting the sliders and clicking on "Check Parameters" again.
        Explain that their mistake is that the normal distribution is either too narrow or too wide compared to the histogram.
        Do not share the actual mean and standard deviation to the student.
        Be as concise as possible and show digit-by-digit arithmetic.
        """
    elif (mean_error>=15 and std_error<15):
        SYSTEM_PROMPT = f"""
        You are a helpful assistant that answers questions about statistics and data analysis.
        The exercise for the student is to manually adjust sliders that represent the mean and standard deviation of a normal distribution such that it fits a histogram of data as well as possible.
        The actual mean and standard deviation of the data are {random_mean_data:.2f} and {random_std_data:.2f}, respectively.
        The student was close enough on the standard deviation, but was off by at least +/-0.15 error in the mean.
        So guide them where they went wrong and encourage them to try again by adjusting the sliders and clicking on "Check Parameters" again.
        Explain that their mistake is that the normal distribution is shifted too far left or right compared to the histogram.
        Do not share the actual mean and standard deviation to the student.
        Be as concise as possible and show digit-by-digit arithmetic.
        """
    else:
        SYSTEM_PROMPT = f"""
        You are a helpful assistant that answers questions about statistics and data analysis.
        The exercise for the student is to manually adjust sliders that represent the mean and standard deviation of a normal distribution such that it fits a histogram of data as well as possible.
        The actual mean and standard deviation of the data are {random_mean_data:.2f} and {random_std_data:.2f}, respectively.
        The student was off by at least +/-0.15 error, so guide them where they went wrong and encourage them to try again by adjusting the sliders and clicking on "Check Parameters" again.
        Explain that their mistake is that the normal distribution is shifted too far left or right compared to the histogram.
        Explain also that their mistake is that the normal distribution is either too narrow or too wide compared to the histogram.
        Do not share the actual mean and standard deviation to the student.
        Be as concise as possible and show digit-by-digit arithmetic.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("Please set the OPENAI_API_KEY environment variable.")
            st.stop()
        client = OpenAI(api_key=api_key)
        
        r = client.responses.create(
            model="gpt-4o-mini",
            input=[{"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"""The mean and the standard deviation I inputted are {mean:.2f} and {std:.2f}, respectively. Are my estimates correct?"""}],
                    max_output_tokens=500,
                    temperature=0.2
        )
        st.write(r.output_text)