import io
import streamlit as st
from research import search_web, get_clean_text, agentic_research
import os

os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"

def dounload_results(text):
    return text


st.set_page_config(page_title="Research Assistant Ai Agent", layout="wide")

st.title("Agentic Research Ai")

query = st.text_input("Enter your research topic")

if st.button("Start Researching") and query:
    with st.spinner("Agent is Researching... please wait"):
        urls = search_web(query)
        if urls:
            try:
                final_summary, source_summaries = agentic_research(query, urls)
                st.session_state.summary_text = final_summary
                st.session_state.source_data = source_summaries

                st.subheader("Final Research Summary")
                st.write(final_summary)

                st.subheader("Source Highlights")
                for i, source in enumerate(source_summaries):
                    with st.expander(f"Source {i+1}"):
                        st.write(source)

            except Exception as e:
                st.eror(f"Error running agentic Research: {e}")
        
        else:
            st.warning("No search results found")

if st.button("Dounload Summary")and "summary_text" in st.session_state:
    text_data = st.session_state.summary_text
    st.download_button(
        "Download Summary as .txt",
        data=text_data,  # just pass the string directly
        file_name=f"{query}_summary.txt",
        mime="text/plain"
    )