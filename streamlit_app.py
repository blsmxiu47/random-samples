import altair as alt
import numpy as np
import pandas as pd
from scipy.stats import norm, beta
import streamlit as st


def generate_altair_pdf(df):
    pdf_line = alt.Chart(df).mark_line().encode(
        x='x',
        y='f(x)'
    )
    nearest = alt.selection(
        type='single', nearest=True, on='mouseover', 
        fields=['x'], empty='none'
    )
    selectors = alt.Chart(df).mark_point().encode(
        x='x:Q',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )
    points = pdf_line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    text = pdf_line.mark_text(align='left', dx=5, dy=-5, color='white').encode(
        text=alt.condition(nearest, 'f(x):Q', alt.value(' '))
    )
    rules = alt.Chart(df).mark_rule(color='gray').encode(
        x='x:Q',
    ).transform_filter(
        nearest
    )
    pdf_chart = alt.layer(
        pdf_line, selectors, points, rules, text
    )

    return pdf_chart


def generate_altair_sample_hist(sample):
    base = alt.Chart(sample)
    max_bins = st.slider("Max histogram bins", 5, 40, 40)
    sample_hist = base.mark_bar().encode(
        x=alt.X('vals:Q', bin={"maxbins": max_bins}),
        y='count()'
    ).properties(
        title=f'Random Sample (n = {len(sample)})'
    )
    sample_hist = sample_hist.configure_title(
        fontSize=20,
        font='Courier New'
    )

    return sample_hist


def main():
    st.sidebar.subheader("Distribution")
    distribution = st.sidebar.selectbox("Select distribution", ("Gaussian", "Beta"))

    sample_size = st.sidebar.slider("Select sample size", 1, 10000, 1000) # can also be an enter-a-number srt of deal

    st.sidebar.subheader("Parameters")
    if distribution == "Gaussian":
        # Gaussian parameters
        mu = st.sidebar.slider("\u03BC (Mean)", -10, 10, 0)
        sigma_squared = st.sidebar.slider("\u03C3\u00B2 (Variance)", 0.01, 10.0, 1.0)

        # PDF
        x = np.linspace(norm.ppf(0.0001, mu, sigma_squared), norm.ppf(0.9999, mu, sigma_squared), 100)
        df = pd.DataFrame({'x': x, 'f(x)': norm.pdf(x, mu, sigma_squared)})
        # Normal pdf line chart
        norm_pdf_chart = generate_altair_pdf(df)
        # Display in app
        st.latex("PDF\\ of\\ \mathcal{N}"+f"({mu}, {sigma_squared})")
        st.altair_chart(norm_pdf_chart, use_container_width=True)
        
        # Random sample
        sample = pd.DataFrame(norm.rvs(loc=mu, scale=sigma_squared, size=sample_size), columns=['vals'])
        # Sample histogram
        sample_hist = generate_altair_sample_hist(sample)
        # Display in app
        st.altair_chart(sample_hist, use_container_width=True)

    elif distribution == "Beta":
        # Beta parameters
        a = st.sidebar.slider("\u03B1", 0.01, 10.0, 2.0)
        b = st.sidebar.slider("\u03B2", 0.01, 10.0, 5.0)

        # PDF
        x = np.linspace(beta.ppf(0.0001, a, b), beta.ppf(0.9999, a, b), 100)
        df = pd.DataFrame({'x': x, 'f(x)': beta.pdf(x, a, b)})
        # Beta pdf line chart
        beta_pdf_chart = generate_altair_pdf(df)
        # Display in app
        st.latex("PDF\\ of\\ \mathcal{Beta}"+f"({a}, {b})")
        st.altair_chart(beta_pdf_chart, use_container_width=True)

        # Random sample
        sample = pd.DataFrame(beta.rvs(a, b, size=sample_size), columns=['vals'])
        # Sample histogram
        sample_hist = generate_altair_sample_hist(sample)
        # Display in app
        st.altair_chart(sample_hist, use_container_width=True)


st.sidebar.title("Random Samples")
st.sidebar.write("1. Pick a distribution")
st.sidebar.write("2. Select sample size and parameters")
main()
