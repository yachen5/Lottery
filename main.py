# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import streamlit as st
import random
import time
# from icecream import ic

def start_here():
    st.header("Lottery Testing Version 1.1")
    df = pd.read_csv("data/names.csv")

    alist = list(df.Name.unique())
    alist.append("")
    list_len = len(alist)
    blist = alist.copy()
    col1, col3, col2 = st.columns((1,1,2))
    col1.markdown("### Your Name:")
    a_name = col1.selectbox("Select your name:", alist, list_len-1)

    angel_row = df[df['Name']==a_name]
    try:
        angel = angel_row.iloc[0, 0]
    except IndexError:
        angel = ""
    col2.markdown("### The system is going to pick a person from this list: ")


    if len(angel)>0:
        if angel == "Justin":
            st.markdown(f"## What are you thinking? You are Yangchi's angel this year!")
        else:
            a_family = angel_row.iloc[0, 1]
            df_s = df.copy()
            df_s = df_s[~(df_s['Family'] == a_family)]
            candidates = list(df_s['Name'].unique())
            candidates.remove("Yangchi")
            for a_name in candidates:
                col2.markdown(f"- {a_name}")

            rd = st.button("Go!")
            cont = st.empty()
            if rd:
                for i in range(50):
                    random_index = random.randint(0, len(candidates) - 1)
                    selected = candidates[random_index]
                    cont.markdown(f"{selected}")
                    time.sleep(0.1)
                st.markdown(f"## {angel} is {selected}'s angel this year!")
                st.balloons()

    # print(df)
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_here()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
