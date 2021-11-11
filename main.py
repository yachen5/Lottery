import pandas as pd
import streamlit as st
import random
import time
# import config as cf
import airtable.airtable as at
import datetime as datetime
import plotly_express as px

base_id = st.secrets['base_id']
table_name = st.secrets['table_name']
api_key = st.secrest['api_key']

# a_table = at.Airtable(cf.base_id, cf.table_name, cf.api_key)
a_table = at.Airtable(base_id, table_name, api_key)


def show_stats(df):
    df_time = df.copy()

    st.markdown("- Percentage of people who have planed")
    df = df.groupby(['status'], as_index=False).agg({'name':'count'})
    fig = px.pie(df, names='status', values='name')
    st.plotly_chart(fig)

    st.markdown("- Timeline")
    df_time = df_time.dropna(subset=['enter_date'])
    fig2 = px.bar(df_time, x='enter_date', y='status', color='name')
    st.plotly_chart(fig2)



def get_table():
    # Downloads all your records into a dataframe.
    records = a_table.get_all()
    df = pd.DataFrame.from_records((r['fields'] for r in records))

    return df

def write_picked(a_name, a_pick):
    t_day = datetime.date.today()
    a_table.update_by_field('name', a_name, {'picked': a_pick, 'status':1, 'enter_date':t_day.isoformat()})

# print(df)
# airtable.insert({'Name': 'Brian'})
#
# r = airtable.search('Name', 'Jamie')
# print(r)

#
# airtable.delete_by_field('Name', 'Tom')

def check_last_name(a_dict, a_last_name):
    if a_dict['last_name'] == a_last_name:
        r = True
    else:
        r = False
    return r

def start_here():
    st.title("2021 Year End - Kenting Trip")
    st.header("Lottery Version 1.0")
    # show_stats()
    # df = pd.read_csv("data/names.csv")
    df = get_table()
    show_stats(df)

    alist = list(df.name.unique())
    l_list = list(df.last_name.unique())
    l_list.sort()
    l_list.append("")
    alist.append("")
    list_len = len(alist)
    blist = alist.copy()
    col1, col3, col2 = st.columns((1,1,2))
    col1.markdown("### Your Name:")
    a_name = col1.selectbox("Select your name:", alist, list_len-1)

    picked_names = list(df.picked.unique())

    angel_row = df[df['name']==a_name].squeeze().to_dict()
    try:
        angel = angel_row['name']
    except KeyError:
        angel = ""
    col2.markdown("### The system is going to pick a person from this list: ")


    if len(angel)>0:
        if angel == "Justin":
            st.markdown(f"## What are you thinking? You are Yangchi's angel this year!")
        else:
            l_name = col1.selectbox("Please select your last name",l_list, index=len(l_list)-1)
            if (check_last_name(angel_row, l_name)):
                if angel_row['status'] ==0:
                    a_family = angel_row['family']
                    df_s = df.copy()
                    df_s = df_s[~(df_s['family'] == a_family)]
                    df_s = df_s[~(df_s['name'].isin(picked_names))]
                    candidates = list(df_s['name'].unique())
                    try:
                        candidates.remove("Yangchi")
                    except ValueError:
                        pass
                    for a_name in candidates:
                        col2.markdown(f"- {a_name}")
                    st.markdown("### You only have one chance to play. Are you Ready?")
                    rd = st.button("Go!")
                    cont = st.empty()
                    if rd:
                        for i in range(30):
                            random_index = random.randint(0, len(candidates) - 1)
                            selected = candidates[random_index]
                            cont.markdown(f"{selected}")
                            time.sleep(0.1)
                        st.markdown(f"## {angel} is {selected}'s angel this year!")
                        write_picked(angel, selected)
                        st.balloons()
                else:
                    st.markdown("## You have played the lottery!")
                    # st.write(angel_row['picked'])
                    pass
            elif len(l_name)>0:
                st.error("Wrong Last Name")
            else:
                pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_here()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
