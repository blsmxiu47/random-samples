import altair as alt
import numpy as np
import pandas as pd
from scipy.stats import norm, beta, expon
import streamlit as st


def generate_altair_pdf(df):
    """Builds and returns an pdf (probability density function) Altair line chart from a Pandas DataFrame
     containing some array x and the array of values corresponding to the value of a given pdf, f(x), at each x"""
    pdf_line = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x='x',
            y='f(x)'
        )
    )

    nearest = alt.selection(
        type='single', 
        nearest=True, 
        on='mouseover', 
        fields=['x'], 
        empty='none'
    )

    selectors = (
        alt.Chart(df)
        .mark_point()
        .encode(
            x='x:Q',
            opacity=alt.value(0),
        )
        .add_selection(nearest)
    )

    points = (
        pdf_line
        .mark_point()
        .encode(
            opacity=(
                alt.condition(
                    nearest, 
                    alt.value(1), 
                    alt.value(0)
                )
            )
        )
    )

    text = (
        pdf_line
        .mark_text(
            align='left', 
            dx=5, 
            dy=-5, 
            color='white'
        )
        .encode(
            text=(
                alt.condition(
                    nearest, 
                    'f(x):Q', 
                    alt.value(' ')
                )
            )
        )
    )

    rules = (
        alt.Chart(df)
        .mark_rule(color='gray')
        .encode(x='x:Q',)
        .transform_filter(nearest)
    )

    pdf_chart = alt.layer(
        pdf_line, 
        selectors, 
        points, 
        rules, 
        text
    )

    return pdf_chart


def generate_altair_sample_hist(sample):
    """Builds and returns and Altair histogram chart from a Pandas DataFrame"""
    base = alt.Chart(sample)

    max_bins = st.slider('Max histogram bins', 5, 40, 40)

    sample_hist = (
        base
        .mark_bar()
        .encode(
            x=alt.X(
                'vals:Q', 
                bin={"maxbins": max_bins}
            ),
            y='count()'
        )
        .properties(
            title=f'Random Sample (n = {len(sample)})'
        )
    )

    sample_hist = (
        sample_hist
        .configure_title(
            fontSize=20,
            font='Courier New'
        )
    )

    return sample_hist


def main():
    # Distribution Selection
    st.sidebar.subheader("Distribution")
    distribution = st.sidebar.selectbox(
        label='Select distribution', 
        options=('Gaussian', 'Beta', 'Exponential')
    )

    # Sample Size Selection
    sample_size = st.sidebar.slider(
        label='Select sample size', 
        min_value=1, 
        max_value=10000, 
        value=1000
    ) # can also be an enter-a-number srt of deal
 
    st.sidebar.subheader('Parameters')
    if distribution == "Gaussian":
        # Gaussian parameters
        input_type = st.sidebar.radio(
            'Input Type',
            ('Sliders', 'Enter Values')
        )
        if input_type == 'Sliders':
            mu = st.sidebar.slider(
                label='\u03BC (Mean)', 
                min_value=-10.0, 
                max_value=10.0, 
                value=0.0
            )
            sigma_squared = st.sidebar.slider(
                label='\u03C3\u00B2 (Variance)', 
                min_value=0.01, 
                max_value=10.0, 
                value=1.0
            )
        elif input_type == 'Enter Values':
            mu = st.sidebar.number_input(
                label='\u03BC (Mean)', 
                value=0.0, 
                step=1.0
            )
            sigma_squared = st.sidebar.number_input(
                label='\u03C3\u00B2 (Variance)', 
                min_value=0.01, 
                value=1.0, 
                step=0.1
            )

        # Gaussian PDF
        x = np.linspace(
            norm.ppf(0.001, mu, sigma_squared), 
            norm.ppf(0.999, mu, sigma_squared),
            1000
        )
        df = pd.DataFrame({
            'x': x, 
            'f(x)': norm.pdf(x, mu, sigma_squared)
        })
        # Gaussian PDF line chart
        norm_pdf_chart = generate_altair_pdf(df)
        # Display in app
        st.latex('PDF\\ of\\ \mathcal{N}'+f'({np.round(mu, 2)}, {np.round(sigma_squared, 2)})')
        st.altair_chart(
            norm_pdf_chart, 
            use_container_width=True
        )
        
        # Random sample
        sample = pd.DataFrame(
            norm.rvs(loc=mu, scale=sigma_squared, size=sample_size), 
            columns=['vals']
        )
        # Sample histogram
        sample_hist = generate_altair_sample_hist(sample)
        # Display in app
        st.altair_chart(
            sample_hist, 
            use_container_width=True
        )

    elif distribution == "Beta":
        # Beta parameters
        input_type = st.sidebar.radio(
            'Input Type',
            ('Sliders', 'Enter Values')
        )
        if input_type == 'Sliders':
            a = st.sidebar.slider(
                label='\u03B1', 
                min_value=0.01, 
                max_value=10.0, 
                value=2.0
            )
            b = st.sidebar.slider(
                label='\u03B2', 
                min_value=0.01, 
                max_value=10.0, 
                value=5.0
            )
        elif input_type == 'Enter Values':
            a = st.sidebar.number_input(
                label='\u03B1', 
                min_value=0.01, 
                value=2.0,
                step=0.1
            )
            b = st.sidebar.number_input(
                label='\u03B2', 
                min_value=0.01, 
                value=5.0,
                step=0.1
            )

        # Beta PDF
        x = np.linspace(
            beta.ppf(0.001, a, b), 
            beta.ppf(0.999, a, b), 
            1000
        )

        # Log option
        logpdf = st.sidebar.checkbox(
            label='logpdf (useful for small values of \u03B1, \u03B2)'
        )
        
        if logpdf:
            fx = beta.logpdf(x, a, b)
        else:
            fx = beta.pdf(x, a, b)
            
        df = pd.DataFrame({
                'x': x, 
                'f(x)': fx
        })
        
        # Beta PDF line chart
        beta_pdf_chart = generate_altair_pdf(df)
        # Display in app
        st.latex('PDF\\ of\\ \mathcal{Beta}'+f'({np.round(a, 2)}, {np.round(b, 2)})')
        st.altair_chart(
            beta_pdf_chart, 
            use_container_width=True
        )

        # Random sample
        sample = pd.DataFrame(
            beta.rvs(a, b, size=sample_size), 
            columns=['vals']
        )
        # Sample histogram
        sample_hist = generate_altair_sample_hist(sample)
        # Display in app
        st.altair_chart(
            sample_hist, 
            use_container_width=True
        )

    elif distribution == "Exponential":
        # Exponential parameters
        input_type = st.sidebar.radio(
            'Input Type',
            ('Sliders', 'Enter Values')
        )
        if input_type == 'Sliders':
            l = st.sidebar.slider(
                label='\u03BB', 
                min_value=0.01, 
                max_value=10.0, 
                value=1.0
            )
        elif input_type == 'Enter Values':
            l = st.sidebar.number_input(
                label='\u03BB', 
                min_value=0.01, 
                value=1.0,
                step=0.1
            )


        # Exponential PDF
        x = np.linspace(
            expon.ppf(0.001, scale=1/l), 
            expon.ppf(0.999, scale=1/l), 
            1000
        )
        df = pd.DataFrame({
            'x': x, 
            'f(x)': expon.pdf(x, scale=1/l)
        })
        # Exponential PDF line chart
        expon_pdf_chart = generate_altair_pdf(df)
        # Display in app
        st.latex('PDF\\ of\\ Exp'+f'({np.round(l, 2)})')
        st.altair_chart(
            expon_pdf_chart, 
            use_container_width=True
        )

        # Random sample
        sample = pd.DataFrame(
            expon.rvs(scale=1/l, size=sample_size), 
            columns=['vals']
        )
        # Sample histogram
        sample_hist = generate_altair_sample_hist(sample)
        # Display in app
        st.altair_chart(
            sample_hist, 
            use_container_width=True
        )


st.sidebar.title('Random Samples')
st.sidebar.write('1. Pick a distribution')
st.sidebar.write('2. Select sample size and parameters')
main()
