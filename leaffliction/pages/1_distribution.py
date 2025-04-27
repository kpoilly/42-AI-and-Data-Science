from distribution import distribution, plot_distribution
import streamlit as st
import os
st.set_page_config(page_title="Distribution", page_icon="📊")

st.markdown("# Distribution")
st.sidebar.header("Distribution")
st.write(
    """This Page is used to visualize the distribution of the data."""
)


def view():
    path = st.text_input(
        "Enter the path to the data directory",
        value="data/",
        key="data_path",
    )
    if not os.path.exists(path) or not os.path.isdir(path):
        st.error("Please enter a valid directory path.")
        return

    def display_plot():
        dist_map = distribution(path)
        st.success("Plot generated!")
        st.write("### Distribution of Images by directory")
        plot_distribution(
            dist_map,
            displayfunc=st.pyplot,
        )

    if st.button("Show Distribution"):
        with st.spinner("Generating distribution plot..."):
            try:
                display_plot()
            except Exception as e:
                st.error(f"Error generating plot: {e}")
                return


view()
