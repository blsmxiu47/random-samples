import altair as alt
import numpy as np
import pandas as pd
from scipy.stats import norm, beta
import streamlit as st


def main():
    st.sidebar.subheader("Distribution")
    distribution = st.sidebar.selectbox("Select distribution", ("Gaussian", "Beta"))

    sample_size = st.sidebar.slider("Select sample size", 1, 1000, 100) # can also be an enter-a-number srt of deal

    st.sidebar.subheader("Parameters")
    if distribution == "Gaussian":
        mu = st.sidebar.slider("\u03BC (Mean)", -10, 10, 0)
        sigma_squared = st.sidebar.slider("\u03C3\u00B2 (Variance)", 0.01, 10.0, 1.0)

        # Base
        x = np.linspace(norm.ppf(0.0001, mu, sigma_squared), norm.ppf(0.9999, mu, sigma_squared), 100)
        df = pd.DataFrame({'x': x, 'f(x)': norm.pdf(x, mu, sigma_squared)})

        # Normal pdf line chart
        norm_pdf_line = alt.Chart(df).mark_line().encode(
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
        points = norm_pdf_line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )
        text = norm_pdf_line.mark_text(align='left', dx=5, dy=-5, color='white').encode(
            text=alt.condition(nearest, 'f(x):Q', alt.value(' '))
        )
        rules = alt.Chart(df).mark_rule(color='gray').encode(
            x='x:Q',
        ).transform_filter(
            nearest
        )
        norm_pdf_chart = alt.layer(
            norm_pdf_line, selectors, points, rules, text
        )
        st.latex("PDF\\ of\\ \mathcal{N}"+f"({mu}, {sigma_squared})")
        st.altair_chart(norm_pdf_chart, use_container_width=True)
        
        # Histogram of random sample
        sample = pd.DataFrame(norm.rvs(loc=mu, scale=sigma_squared, size=sample_size), columns=['vals'])
        base = alt.Chart(sample)

        max_bins = st.slider("Max histogram bins", 5, 40, 20)
        sample_hist = base.mark_bar().encode(
            x=alt.X('vals:Q', bin={"maxbins": max_bins}),
            y='count()'
        ).properties(
            title=f'Random Sample (n = {sample_size})'
        )
        sample_hist = sample_hist.configure_title(
            fontSize=20,
            font='Courier New'
        )
        st.altair_chart(sample_hist, use_container_width=True)

        # combined = alt.layer(norm_pdf_chart, sample_hist)
        # st.altair_chart(combined, use_container_width=True)

    elif distribution == "Beta":
        a = st.slider("\u03B1", 0.01, 10.00)
        b = st.slider("\u03B2", 0.01, 10.00)

        # Base
        x = np.linspace(beta.ppf(0.0001, a, b), beta.ppf(0.9999, a, b), 100)
        df = pd.DataFrame({'x': x, 'f(x)': beta.pdf(x, a, b)})

        # Normal pdf line chart
        beta_pdf_line = alt.Chart(df).mark_line().encode(
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
        points = beta_pdf_line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )
        text = beta_pdf_line.mark_text(align='left', dx=5, dy=-5, color='white').encode(
            text=alt.condition(nearest, 'f(x):Q', alt.value(' '))
        )
        rules = alt.Chart(df).mark_rule(color='gray').encode(
            x='x:Q',
        ).transform_filter(
            nearest
        )
        beta_pdf_chart = alt.layer(
            beta_pdf_line, selectors, points, rules, text
        )
        st.latex("PDF\\ of\\ \mathcal{Beta}"+f"({a}, {b})")
        st.altair_chart(beta_pdf_chart, use_container_width=True)


st.sidebar.title("Random Samples")
st.sidebar.write("1. Pick a distribution")
st.sidebar.write("2. Select sample size and parameters")
main()
