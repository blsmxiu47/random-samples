# import altair as alt
# import numpy as np
# import pandas as pd
from scipy.stats import norm
import streamlit as st


def main():
    st.subheader("Distribution")
    distribution = st.selectbox("Select distribution", ("Gaussian", "Beta"))

    sample_size = st.slider("Select sample size", 1, 1000) # can also be an enter-a-number srt of deal

    if distribution == "Gaussian":
        st.subheader("Parameters")
        mu = st.slider("\u03BC (Mean)", -100, 100)
        sigma_squared = st.slider("\u03C3\u00B2 (Variance)", 0.01, 100.0)
        # params = (mu, sigma_squared)
        
        rvs = norm.rvs(loc=mu, scale=sigma_squared, size=sample_size)
        # x = np.linspace(norm.ppf(0.01), norm.ppf(0.99), 100)

    elif distribution == "Beta":
        params = (alpha, beta)

st.title("Random Samples")
"1. Pick a distribution"
"2. Select parameters and sample size"
"3. Run simulation"
main()
