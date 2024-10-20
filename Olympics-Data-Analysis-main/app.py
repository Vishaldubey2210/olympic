import streamlit as st
import pandas as pd
import  preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df , df_region)

st.sidebar.title("Olympic Analysis")
st.sidebar.image('https://images.unsplash.com/photo-1722969561537-4ed6b3b98b50?q=80&w=1467&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')

user_menu =  st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Contrywise Analysis','Athlete Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df) # this will give all the years and the countries avaliable
    selected_year = st.sidebar.selectbox("Select Year" , years)
    selected_country = st.sidebar.selectbox("Select Country" , country)
    medal_tally = helper.fetch_medal_tally(df , selected_year , selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)  # Use st.columns instead of st.beta_columns
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)  # Use st.columns instead of st.beta_columns
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    
    nations_over_time = helper.nations_over_time(df)
    years = nations_over_time['Year']
    counts = nations_over_time['count']
    plt.figure(figsize=(10, 6))
    plt.plot(years, counts, marker='', linestyle='-', color='b')
    plt.title('Year vs Countries Count', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('No of Countries', fontsize=12)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.title("Participating Nations over the YEAR")
    st.pyplot(plt)
    
    
    
    events_over_time = helper.events_over_time(df)
    years = events_over_time['Year']
    events = events_over_time['count']
    plt.figure(figsize=(10, 6))
    plt.plot(years, counts, marker='', linestyle='-', color='b')
    plt.title('Year vs Events over time', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('No of Events', fontsize=12)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.title("Events Occuring over the YEAR")
    st.pyplot(plt)
    
    
       
    athletes_over_time = helper.atheletes_over_time(df)
    years = events_over_time['Year']
    athletes = events_over_time['count']
    plt.figure(figsize=(10, 6))
    plt.plot(years, athletes, marker='', linestyle='-', color='b')
    plt.title('Year vs Atheletes over time', fontsize=14)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('No of Atheletes', fontsize=12)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.title("Atheletes Participating over the YEAR")
    st.pyplot(plt)
    
    x_pivot_table = helper.sports_events(df)
    import seaborn as sns
    plt.figure(figsize=(30,30))
    sns.heatmap(x_pivot_table,annot=True)
    st.title("Events Occured in Each Sports over time")
    # Display the heatmap in Streamlit
    st.pyplot(plt)
    
    st.title("Most Successful Atheletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall') # the purpose of 'Overall' here is likely to represent an option where no specific sport is selected, allowing the user to view results across all sports.
    
    selected_sport = st.selectbox('Select a sport' , sport_list)
    x = helper.most_successful(df , selected_sport)
    st.table(x)

if user_menu == 'Contrywise Analysis':
    # Allowing the user to select the country
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country_list = st.selectbox("Select a country" , country_list)
    country_df = helper.year_wise_medal_tally(df , selected_country_list)
    years = country_df['Year']
    medals = country_df['Medal']
    plt.plot(years, medals, marker='', linestyle='-', color='r')
    st.title(selected_country_list + " Medals Over the Years")
    st.pyplot(plt)
    
    
    country_list_sport = df['region'].dropna().unique().tolist()
    country_list_sport.sort()
    selected_country_list_sport = st.selectbox("Select a country" , country_list_sport , key="country_select_unique")
    sport_medal_df_map = helper.country_sports_map(df , selected_country_list_sport)
    plt.figure(figsize=(20,20)) 
    sns.heatmap(sport_medal_df_map,annot=True)
    st.title(selected_country_list_sport + " Sports & Medals Over the Years")
    st.pyplot(plt)
    
    
    
    country_list_sport = df['region'].dropna().unique().tolist()
    country_list_sport.sort()
    selected_country_list_famous = st.selectbox("Select a country" , country_list_sport , key="country_select_famous")
    st.title(selected_country_list_famous + " Most Successful Atheletes")
    temp_df = helper.most_successful_athelete_country(df , selected_country_list_famous)
    st.table(temp_df)


if user_menu == 'Athlete Analysis':
    # Use Streamlit to set the title
    st.header("Age Distribution by Medal Type of Athletes")
    
    # Drop duplicates and NaN values
    new_df_athe = df.drop_duplicates(subset=['Name','region'])
    x1 = new_df_athe['Age'].dropna()
    x2 = new_df_athe[new_df_athe['Medal'] == 'Gold']['Age'].dropna()
    x3 = new_df_athe[new_df_athe['Medal'] == 'Silver']['Age'].dropna()
    x4 = new_df_athe[new_df_athe['Medal'] == 'Bronze']['Age'].dropna()

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create KDE plots
    sns.kdeplot(x1, label='All Athletes', fill=True, ax=ax)
    sns.kdeplot(x2, label='Gold Medalists', fill=True, ax=ax)
    sns.kdeplot(x3, label='Silver Medalists', fill=True, ax=ax)
    sns.kdeplot(x4, label='Bronze Medalists', fill=True, ax=ax)

    # Add labels
    ax.set_xlabel('Age')
    ax.set_ylabel('Density')

    # Add a legend
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)


    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    x = []
    name = []
    for sport in famous_sports:
        temp_df =  new_df_athe[new_df_athe['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)  
    import matplotlib.pyplot as plt
    # Create a figure and axis for the plots
    fig, ax = plt.subplots(figsize=(20, 20))

    # Plot KDE for each sport
    for ages, sport in zip(x, name):
        sns.kdeplot(ages, label=sport, ax=ax)

    # Add labels and title
    ax.set_xlabel('Age')
    ax.set_ylabel('Density')
    ax.set_title('Distribution of Ages for Gold Medalists by Sport')

    # Add a legend to differentiate sports
    ax.legend(title='Sport')

    # Adjust layout to avoid overlap
    plt.tight_layout()
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    # Show the plot in Streamlit
    st.pyplot(fig)
    
    
    st.title("Distribution of Weight with Sport")
    # Filter the DataFrame for 'Athletics'
    sport_list = st.selectbox("Select a country" ,famous_sports)
    temp_athe = new_df_athe[new_df_athe['Sport'] == sport_list]
    
    # Create a scatter plot
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x=temp_athe['Height'], y=temp_athe['Weight'],
                    hue=temp_athe['Medal'], style=temp_athe['Sex'],
                    palette='viridis', markers={'M': 'o', 'F': 'X'},
                    ax=ax)

    # Add labels and title
    ax.set_xlabel('Height')
    ax.set_ylabel('Weight')
    ax.set_title('Height vs Weight of Athletes in Athletics by Medal and Sex')

    # Add a legend to differentiate medal types and sexes
    ax.legend(title='Medal / Sex')

    # Show the plot in Streamlit
    st.pyplot(fig)


    # Assuming helper.menvswomen(df) returns the required dataframe
    st.title("Men vs Women participation over the Years")

    new_df_athe_camp = helper.menvswomen(df)

    # Men data
    men = new_df_athe_camp[new_df_athe_camp['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    men = men.rename(columns={'Name': 'Count'})

    # Women data
    women = new_df_athe_camp[new_df_athe_camp['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    women = women.rename(columns={'Name': 'Count'})

    # Create a figure
    fig, ax = plt.subplots()

    # Plotting men and women participation
    ax.plot(men['Year'], men['Count'], marker='', linestyle='-', color='b', label='Men')
    ax.plot(women['Year'], women['Count'], marker='', linestyle='-', color='r', label='Women')

    # Adding labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Count of Athletes')
    ax.set_title('Men vs Women Athletes Over the Years')

    # Display the legend
    ax.legend()

    # Show the plot in Streamlit
    st.pyplot(fig)
