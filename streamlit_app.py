import streamlit as st
import pandas as pd

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv("FinalPrototypeErgebnis_ohneArtikel.csv", parse_dates=["Date"])
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# Title
st.title("📊 News Impact Viewer")
st.markdown("See how recent news affects companies based on articles and sentiment analysis.")

# Company selector
companies = ["Apple","BMW","Palantir","Samsung Electronics","Huawei","Google","Siemens AG","Volkswagen AG","Gazprom","Uniper SE","Meta","Axel Springer SE","Lockheed Martin","GoldmanSachs","Exxon Mobil"]
selected_company = st.selectbox("Choose a company:", companies)

# Filter for selected company and ignore articles with "Not Affected" impact
filtered_df = df[
    (df["Company"].str.lower() == selected_company.lower()) &
    (df["Impact"].str.strip().str.lower() != "not affected")
]

# Show results
if filtered_df.empty:
    st.info("✅ We don't see anything you have to worry about.")
else:
    st.subheader(f"📰 Articles about {selected_company}")
    
    # Optional: Sort by date descending
    filtered_df = filtered_df.sort_values(by="Date", ascending=False)
    
    # Show impact summary if multiple types
    if filtered_df["Impact"].nunique() <= 5:
        sentiment_counts = filtered_df["Impact"].value_counts()
        st.markdown("**Impact summary:**")
        st.write(sentiment_counts.to_frame(name="Count"))
    
    # Display filtered results
    st.markdown("### 🧾 Detailed View")
    for _, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"**🗓️ Date:** {row['Date']}  ")
            st.markdown(f"**💥 Impact:** {row['Impact']}  ")
            st.markdown(f"**🧠 Reasoning:** {row['Reasoning']}  ")
            st.markdown(f"[🔗 Read full article]({row['Link']})")
            st.markdown("---")


    # Expand full article content
    #with st.expander("🗞️ Full Articles"):
    #    for idx, row in filtered_df.iterrows():
    #        st.markdown(f"**{row['Date']} - Impact: {row['Impact']}**")
    #        st.markdown(f"*Reasoning:* {row['Reasoning']}")
    #        st.markdown(f"*Article:* {row['Article']}")
    #        st.markdown("---")
