import numpy as np
import streamlit as st
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# Global variables to store user inputs
selected_season = None
selected_pairing = None
ok_button_clicked = False

# Function to get F1 seasons
def get_f1_seasons():
    return list(range(2000, 2024))


# Function to get driver pairings for a specific season
def get_driver_pairings(season):
    driver_pairings = {
        2019: {
            "Alfa Romeo": [("Alfa Romeo", "Giovinazzi", "Raikkonen")],
            "Ferrari": [("Ferrari", "Leclerc", "Vettel")],
            "Haas": [("Haas", "Grosjean", "Magnussen")],
            "McLaren": [("McLaren", "Norris", "Sainz")],
            "Mercedes": [("Mercedes", "Bottas", "Hamilton")],
            "Racing Point": [("Racing Point", "Pérez", "Stroll")],
            "Red Bull": [("Red Bull", "Gasly", "Verstappen"), ("Red Bull", "Albon", "Verstappen")],
            "Renault": [("Renault", "Ocon", "Ricciardo")],
            "Toro Rosso": [("Toro Rosso", "Albon", "Kvyat"), ("Toro Rosso", "Gasly", "Kvyat")],
            "Williams": [("Williams", "Kubica", "Russell")]
        },
        2020: {
            "Alfa Romeo": [("Alfa Romeo", "Giovinazzi", "Raikkonen")],
            "AlphaTauri": [("AlphaTauri", "Gasly", "Kvyat")],
            "Ferrari": [("Ferrari", "Leclerc", "Vettel")],
            "Haas": [("Haas", "Grosjean", "Magnussen")],
            "McLaren": [("McLaren", "Norris", "Sainz")],
            "Mercedes": [("Mercedes", "Bottas", "Hamilton")],
            "Racing Point": [("Racing Point", "Pérez", "Stroll")],
            "Red Bull": [("Red Bull", "Albon", "Verstappen")],
            "Renault": [("Renault", "Ocon", "Ricciardo")],
            "Williams": [("Williams", "Latifi", "Russell")]
        },
        2021: {
            "Alfa Romeo": [("Alfa Romeo", "Giovinazzi", "Raikkonen")],
            "AlphaTauri": [("AlphaTauri", "Gasly", "Tsunoda")],
            "Alpine": [("Alpine", "Alonso", "Ocon")],
            "Aston Martin": [("Aston Martin", "Stroll", "Vettel")],
            "Ferrari": [("Ferrari", "Leclerc", "Sainz")],
            "Haas": [("Haas", "Mazepin", "Schumacher")],
            "McLaren": [("McLaren", "Norris", "Ricciardo")],
            "Mercedes": [("Mercedes", "Bottas", "Hamilton")],
            "Red Bull": [("Red Bull", "Verstappen", "Pérez")],
            "Williams": [("Williams", "Latifi", "Russell")]
        },
        2022: {
            "Alfa Romeo": [("Alfa Romeo", "Bottas", "Zhou")],
            "AlphaTauri": [("AlphaTauri", "Gasly", "Tsunoda")],
            "Alpine": [("Alpine", "Alonso", "Ocon")],
            "Aston Martin": [("Aston Martin", "Stroll", "Vettel")],
            "Ferrari": [("Ferrari", "Leclerc", "Sainz")],
            "Haas": [("Haas", "Magnussen", "Schumacher")],
            "McLaren": [("McLaren", "Norris", "Ricciardo")],
            "Mercedes": [("Mercedes", "Hamilton", "Russell")],
            "Red Bull": [("Red Bull", "Verstappen", "Pérez")],
            "Williams": [("Williams", "Albon", "Latifi")]
        },
        2023: {
            "Alfa Romeo": [("Alfa Romeo", "Bottas", "Zhou")],
            "AlphaTauri": [("AlphaTauri", "de Vries", "Ricciardo"), ("AlphaTauri", "Lawson", "Tsunoda")],
            "Alpine": [("Alpine", "Gasly", "Ocon")],
            "Aston Martin": [("Aston Martin", "Alonso", "Stroll")],
            "Ferrari": [("Ferrari", "Leclerc", "Sainz")],
            "Haas": [("Haas", "Magnussen", "Hülkenberg")],
            "McLaren": [("McLaren", "Norris", "Piastri")],
            "Mercedes": [("Mercedes", "Hamilton", "Russell")],
            "Red Bull": [("Red Bull", "Verstappen", "Pérez")],
            "Williams": [("Williams", "Albon", "Latifi")]
        }
    }

    return driver_pairings.get(season, [])


# Main function to build the UI
def main():
    st.set_page_config(layout="wide")
    global selected_season, selected_pairing, ok_button_clicked
    st.title("F1 Teammate Analysis")

    # Dropdown to select F1 season
    selected_season = st.selectbox("Select F1 Season", options=get_f1_seasons(), index=len(get_f1_seasons()) - 1)

    # Get driver pairings for selected season
    driver_pairings = get_driver_pairings(selected_season)

    if not driver_pairings:
        st.warning("No data available for the selected season.")
    else:
        # Dropdown to select driver pairing
        selected_pairing = st.selectbox("Select Driver Pairing", options=[f"{pair[0]}: {pair[1]} vs {pair[2]}" for team_pairings in driver_pairings.values() for pair in team_pairings])

        # OK button
        if st.button("OK"):
            display_results()


# Function to display results page
def display_results():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("Results")
        season_pairings = get_driver_pairings(selected_season)
        team = selected_pairing.split(':')[0].strip()
        driver1_surname = selected_pairing.split("vs")[0].split(":")[1].strip()
        driver2_surname = selected_pairing.split("vs")[1].strip()
        st.markdown(f"##### Season: {selected_season}")
        st.write(f"##### Team: {team}")
        st.write(f"##### Drivers: {driver1_surname} vs {driver2_surname}")
        st.title("Race")
    with col2:
        # Add space below the table
        st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.title("Qualifying")
    with col3:
        st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
        st.title("Fastest laps")

    # Extract surnames from tuples
    driver1_surname = selected_pairing.split("vs")[0].split(":")[1].strip()
    driver2_surname = selected_pairing.split("vs")[1].strip()

    races_and_results_df = pd.read_csv("C:/Users/danie/PycharmProjects/formula-one-teammate-analysis/races_results_drivers.csv")
    qualifying_drivers_races_df = pd.read_csv("C:/Users/danie/PycharmProjects/formula-one-teammate-analysis/qualifying_drivers_races.csv")

    # Filter DataFrames based on selected F1 season
    df_season_races_and_results = races_and_results_df[races_and_results_df['year'] == selected_season]
    df_season_qualifying = qualifying_drivers_races_df[qualifying_drivers_races_df['year'] == selected_season]

    # Accessing corresponding round and position for the driver's surname
    driver_1_info = df_season_races_and_results[df_season_races_and_results['surname'] == driver1_surname]
    if driver_1_info.empty:
        st.write(f"Driver {driver1_surname} not found in the DataFrame.")

    driver_2_info = df_season_races_and_results[df_season_races_and_results['surname'] == driver2_surname]
    if driver_2_info.empty:
        st.write(f"Driver {driver2_surname} not found in the DataFrame.")

    #---------------------------------------------------------------------------------------------------------------------

    # Create dictionaries to store the data for each driver
    driver1_data = {'round': [], 'name': [], 'position': []}
    driver2_data = {'round': [], 'name': [], 'position': []}

    # Iterate over the DataFrame to extract the required information
    for index, row in df_season_races_and_results.iterrows():
        driver_surname = row['surname']
        round_number = row['round']
        name = row['name']
        position = row['position']

        # Check if the row corresponds to driver1 or driver2
        if driver_surname == driver1_surname:
            driver1_data['round'].append(round_number)
            driver1_data['name'].append(name)
            driver1_data['position'].append(position)
        elif driver_surname == driver2_surname:
            driver2_data['round'].append(round_number)
            driver2_data['name'].append(name)
            driver2_data['position'].append(position)

    # Create DataFrames for each driver
    driver1_df = pd.DataFrame(driver1_data)
    driver2_df = pd.DataFrame(driver2_data)

    # Merge the DataFrames on the round and name columns
    merged_df = pd.merge(driver1_df, driver2_df, on=['round', 'name'], suffixes=(driver1_surname, driver2_surname))

    # Rename the driver's columns
    merged_df = merged_df.rename(
        columns={f'position{driver1_surname}': driver1_surname, f'position{driver2_surname}': driver2_surname})

    # Function to highlight cells based on condition
    def highlight_cell_lower(row):
        """Highlight cells based on position comparison."""
        styles = ['background-color: green' if row[driver1_surname] < row[driver2_surname] else '',
                  'background-color: green' if row[driver2_surname] < row[driver1_surname] else '']
        return styles

    # Apply conditional formatting
    formatted_df = merged_df.style.apply(highlight_cell_lower, axis=1,
                                         subset=pd.IndexSlice[:, [driver1_surname, driver2_surname]])

    # Display formatted DataFrame in Streamlit
    with col1:
        st.markdown("## Race finishing positions")
        st.dataframe(formatted_df, hide_index=True)

    #--------------------------------------------------------------------------------------

    # Calculate head-to-head scores
    driver1_lower_count = (merged_df[driver1_surname] < merged_df[driver2_surname]).sum()
    driver2_lower_count = (merged_df[driver2_surname] < merged_df[driver1_surname]).sum()

    # Create a DataFrame to display the counts
    count_df = pd.DataFrame({
        driver1_surname: [driver1_lower_count],
        driver2_surname: [driver2_lower_count]
    })

    # Function to highlight cells based on condition

    def highlight_cell_higher(row):
        """Highlight cells based on position comparison."""
        styles = ['background-color: green' if row[driver1_surname] > row[driver2_surname] else '',
                  'background-color: green' if row[driver2_surname] > row[driver1_surname] else '']
        return styles

    # Apply conditional formatting to the count DataFrame
    formatted_count_df = count_df.style.apply(lambda row: highlight_cell_higher(row), axis=1)
    # with col1:
    #     # Display the count DataFrame in Streamlit
    #     st.markdown("#### Head to head wins")
    #     st.dataframe(formatted_count_df, hide_index=True)

    #-------------------------------------------------------------------------------------------
    # Calculate head-to-head %

    total_wins = driver1_lower_count + driver2_lower_count
    driver1_win_percentage = int((driver1_lower_count / total_wins * 100))
    driver2_win_percentage = int((driver2_lower_count / total_wins * 100))

    # Create a DataFrame to display the counts
    count_df = pd.DataFrame({
        driver1_surname: [driver1_win_percentage],
        driver2_surname: [driver2_win_percentage]
    })

    # Apply conditional formatting to the count DataFrame
    formatted_win_percentage_df = count_df.style.apply(highlight_cell_higher, axis=1)

    # with col1:
    #     # Display the percentages DataFrame in Streamlit
    #     st.markdown("#### Head to head win %")
    #     st.dataframe(formatted_win_percentage_df, hide_index=True)

    # -----------------------------------------------------------------------------------------------------
    # Calculate win counts for each driver
    driver1_wins = merged_df[merged_df[driver1_surname] < merged_df[driver2_surname]].shape[0]
    driver2_wins = merged_df[merged_df[driver2_surname] < merged_df[driver1_surname]].shape[0]

    # Calculate win percentages
    total_wins = driver1_wins + driver2_wins
    driver1_win_percentage = (driver1_wins / total_wins) * 100
    driver2_win_percentage = (driver2_wins / total_wins) * 100

    # Create DataFrame for wins vs. teammate
    win_data = {
        'Driver': ['Wins vs teammate', 'Win % vs teammate'],
        driver1_surname: [int(driver1_wins), int(driver1_win_percentage)],
        driver2_surname: [int(driver2_wins), int(driver2_win_percentage)]
    }
    win_df = pd.DataFrame(win_data)

    def highlight_cell_percentage(row):
        """Highlight cells based on position comparison."""
        styles = ['background-color: green' if row[driver1_surname] == row[driver2_surname] else '',
                  'background-color: green' if row[driver2_surname] < row[driver1_surname] else '',
                  'background-color: green' if row[driver1_surname] < row[driver2_surname] else ''
                  ]
        return styles

    # Apply conditional formatting to the count DataFrame
    formatted_win_df = win_df.style.apply(lambda row: highlight_cell_percentage(row), axis=1)

    with col1:
        # Display the DataFrame below the table
        st.markdown("## Race win statistics")
        st.dataframe(formatted_win_df, hide_index=True)
    #--------------------------------------------------------------------------------------------------------

    ## Qualifying
    # Create dictionaries to store the data for each driver
    driver1_qualifying_data = {'round': [], 'name': [], 'position': [], 'q1': [], 'q2': [], 'q3': []}
    driver2_qualifying_data = {'round': [], 'name': [], 'position': [], 'q1': [], 'q2': [], 'q3': []}

    # Iterate over the DataFrame to extract the required information
    for index, row in df_season_qualifying.iterrows():
        driver_surname = row['surname']
        round_number = row['round']
        name = row['name']
        position = row['position']
        q1 = row['q1']
        q2 = row['q2']
        q3 = row['q3']

        # Check if the row corresponds to driver1 or driver2
        if driver_surname == driver1_surname:
            driver1_qualifying_data['round'].append(round_number)
            driver1_qualifying_data['name'].append(name)
            driver1_qualifying_data['position'].append(position)
            driver1_qualifying_data['q1'].append(q1)
            driver1_qualifying_data['q2'].append(q2)
            driver1_qualifying_data['q3'].append(q3)
        elif driver_surname == driver2_surname:
            driver2_qualifying_data['round'].append(round_number)
            driver2_qualifying_data['name'].append(name)
            driver2_qualifying_data['position'].append(position)
            driver2_qualifying_data['q1'].append(q1)
            driver2_qualifying_data['q2'].append(q2)
            driver2_qualifying_data['q3'].append(q3)

    # Create DataFrames for each driver
    driver1_qualifying_df = pd.DataFrame(driver1_qualifying_data)
    driver2_qualifying_df = pd.DataFrame(driver2_qualifying_data)

    # Merge the DataFrames on the round and name columns
    merged_qualifying_df = pd.merge(driver1_qualifying_df, driver2_qualifying_df, on=['round', 'name'], suffixes=(driver1_surname, driver2_surname))

    # Rename the driver's columns
    merged_qualifying_df = merged_qualifying_df.rename(
        columns={f'position{driver1_surname}': driver1_surname, f'position{driver2_surname}': driver2_surname})

    # Remove the index from the DataFrame
    merged_qualifying_df = merged_qualifying_df.reset_index(drop=True)

    # Function to highlight cells based on condition

    # Apply conditional formatting
    formatted_qualifying_df = merged_qualifying_df.style.apply(highlight_cell_lower, axis=1,
                                         subset=pd.IndexSlice[:, [driver1_surname, driver2_surname]])

    with col2:

        # Display formatted DataFrame in Streamlit
        st.markdown("## Qualifying finishing positions")
        st.dataframe(formatted_qualifying_df, hide_index=True)

    #---------------------------------------------------------------------------------------------------------

    # Calculate win counts for each driver
    driver1_q_wins = merged_qualifying_df[merged_qualifying_df[driver1_surname] < merged_qualifying_df[driver2_surname]].shape[0]
    driver2_q_wins = merged_qualifying_df[merged_qualifying_df[driver2_surname] < merged_qualifying_df[driver1_surname]].shape[0]

    # Calculate win percentages
    total_q_wins = driver1_q_wins + driver2_q_wins
    driver1_q_win_percentage = (driver1_q_wins / total_q_wins) * 100
    driver2_q_win_percentage = (driver2_q_wins / total_q_wins) * 100

    # Calculate average qualifying gap to teammate

    # Create DataFrame for wins vs. teammate
    q_win_data = {
        'Driver': ['Qualifying wins vs teammate', 'Qualifying win % vs teammate'],
        driver1_surname: [int(driver1_q_wins), int(driver1_q_win_percentage)],
        driver2_surname: [int(driver2_q_wins), int(driver2_q_win_percentage)]
    }
    q_win_df = pd.DataFrame(q_win_data)

    # Apply conditional formatting to the count DataFrame
    formatted_q_win_df = q_win_df.style.apply(lambda row: highlight_cell_percentage(row), axis=1)

    with col2:
        # Display the DataFrame below the table
        st.markdown("## Qualifying win statistics")
        st.dataframe(formatted_q_win_df, hide_index=True)

    #-------------------------------------------------------------------------------------

    # Qualifying summary bar chart seaborn
    if team == "Ferrari" or team == "Alfa Romeo":
        team_color = [(255, 0 , 0)]
    else:
        team_color = "blue"

    with col2:
        # Add titles and labels
        st.markdown("## Qualifying wins")
        # Create the bar chart
        st.bar_chart(q_win_df.iloc[0, 1:], use_container_width=True, color=team_color)

    race_wins_df = merged_df.copy()

    with col1:
        # Add titles and labels
        st.markdown("## Race wins")
        # Create the bar chart
        st.bar_chart(win_df.iloc[0, 1:], use_container_width=True, color=team_color)

    #------------------------------------------------------------------------------------------------------------------------

    # Create dictionaries to store the data for each driver
    driver1_fastest_lap_data = {'round': [], 'name': [], 'fastest_lap_time': []}
    driver2_fastest_lap_data = {'round': [], 'name': [], 'fastest_lap_time': []}

    # Iterate over the DataFrame to extract the required information
    for index, row in df_season_races_and_results.iterrows():
        driver_surname = row['surname']
        round_number = row['round']
        name = row['name']
        fastest_lap_time = row['fastestLapTime']

        # Check if the row corresponds to driver1 or driver2
        if driver_surname == driver1_surname:
            driver1_fastest_lap_data['round'].append(round_number)
            driver1_fastest_lap_data['name'].append(name)
            driver1_fastest_lap_data['fastest_lap_time'].append(fastest_lap_time)
        elif driver_surname == driver2_surname:
            driver2_fastest_lap_data['round'].append(round_number)
            driver2_fastest_lap_data['name'].append(name)
            driver2_fastest_lap_data['fastest_lap_time'].append(fastest_lap_time)

    # Create DataFrames for each driver
    driver1_fastest_lap_df = pd.DataFrame(driver1_fastest_lap_data)
    driver2_fastest_lap_df = pd.DataFrame(driver2_fastest_lap_data)

    # Merge the DataFrames on the round and name columns
    fastest_lap_df = pd.merge(driver1_fastest_lap_df, driver2_fastest_lap_df, on=['round', 'name'], suffixes=(driver1_surname, driver2_surname))

    # Rename the driver's columns
    fastest_lap_df = fastest_lap_df.rename(
        columns={f'fastest_lap_time{driver1_surname}': driver1_surname, f'fastest_lap_time{driver2_surname}': driver2_surname})

    # Remove the index from the DataFrame
    fastest_lap_df = fastest_lap_df.reset_index(drop=True)
    formatted_fastest_lap_df = fastest_lap_df.style.apply(highlight_cell_lower, axis=1,
                                                          subset=pd.IndexSlice[:, [driver1_surname, driver2_surname]])

    with col3:
        st.markdown("## Race fastest laps")
        st.dataframe(formatted_fastest_lap_df, hide_index=True)

    #-------------------------------------------------------------------------------------------------------------------

    # Calculate fastest lap counts for each driver
    driver1_fastest_laps = fastest_lap_df[fastest_lap_df[driver1_surname] < fastest_lap_df[driver2_surname]].shape[0]
    driver2_fastest_laps = fastest_lap_df[fastest_lap_df[driver2_surname] < fastest_lap_df[driver1_surname]].shape[0]

    # Calculate win percentages
    total_fastest_laps = driver1_fastest_laps + driver2_fastest_laps
    driver1_fastest_lap_percentage = (driver1_fastest_laps / total_fastest_laps) * 100
    driver2_fastest_lap_percentage = (driver2_fastest_laps / total_fastest_laps) * 100

    # Create DataFrame for wins vs. teammate
    fastest_lap_data = {
        'Driver': ['Fastest laps vs teammate', 'Fastest lap % vs teammate'],
        driver1_surname: [int(driver1_fastest_laps), int(driver1_fastest_lap_percentage)],
        driver2_surname: [int(driver2_fastest_laps), int(driver2_fastest_lap_percentage)]
    }
    fastest_lap_count_df = pd.DataFrame(fastest_lap_data)

    def highlight_cell_percentage(row):
        """Highlight cells based on position comparison."""
        styles = ['background-color: green' if row[driver1_surname] == row[driver2_surname] else '',
                  'background-color: green' if row[driver2_surname] < row[driver1_surname] else '',
                  'background-color: green' if row[driver1_surname] < row[driver2_surname] else ''
                  ]
        return styles

    # Apply conditional formatting to the count DataFrame
    formatted_fastest_lap_count_df = fastest_lap_count_df.style.apply(lambda row: highlight_cell_percentage(row), axis=1)

    with col3:
        # Display the DataFrame below the table
        st.markdown("## Fastest lap statistics")
        st.dataframe(formatted_fastest_lap_count_df, hide_index=True)
    #-------------------------------------------------------------------------------------------------------------------------------------

    with col3:
        st.markdown("## Fastest laps")
        # Create the bar chart
        st.bar_chart(fastest_lap_count_df.iloc[0, 1:], use_container_width=True, color=team_color)
    #------------------------------------------------------------------------------------------------

    # Set the index of the DataFrame to 'round' column
    fastest_lap_df.set_index('round', inplace=True)

    # Replace "\N" with NaN
    fastest_lap_df.replace("\\N", np.nan, inplace=True)

    # Remove all rows containing null values
    fastest_lap_df.dropna(inplace=True)

    with col3:
        st.markdown("## Fastest lap pace")
        # Plot the line chart
        st.bar_chart(fastest_lap_df[[driver1_surname, driver2_surname]])
    #----------------------------------------------------------------------------------------------------------------
    # Create dictionaries to store the data for each driver
    driver1_race_pace_data = {'round': [], 'time': []}
    driver2_race_pace_data = {'round': [], 'time': []}

    # Iterate over the DataFrame to extract the required information
    for index, row in df_season_races_and_results.iterrows():
        driver_surname = row['surname']
        round_number = row['round']
        time = row['milliseconds']

        # Check if the row corresponds to driver1 or driver2
        if driver_surname == driver1_surname:
            driver1_race_pace_data['round'].append(round_number)
            driver1_race_pace_data['time'].append(time)
        elif driver_surname == driver2_surname:
            driver2_race_pace_data['round'].append(round_number)
            driver2_race_pace_data['time'].append(time)

    # Create DataFrames for each driver
    driver1_race_pace_df = pd.DataFrame(driver1_race_pace_data)
    driver2_race_pace_df = pd.DataFrame(driver2_race_pace_data)

    # Merge the DataFrames on the round and name columns
    race_pace_df = pd.merge(driver1_race_pace_df, driver2_race_pace_df, on=['round'], suffixes=(driver1_surname, driver2_surname))

    # Rename the driver's columns
    race_pace_df = race_pace_df.rename(
        columns={f'time{driver1_surname}': driver1_surname, f'time{driver2_surname}': driver2_surname})

    # Set the index of the DataFrame to 'round' column
    race_pace_df.set_index('round', inplace=True)

    # Replace "\N" with NaN
    race_pace_df.replace("\\N", np.nan, inplace=True)

    # Remove all rows containing null values
    race_pace_df.dropna(inplace=True)

    # with col1:
    #     st.markdown("## Race pace")
    #     # Plot the line chart
    #     st.bar_chart(race_pace_df[[driver1_surname, driver2_surname]])
    #------------------------------------------------------------------------------------------------------------------

    # Qualifying pace bar chart
    qualifying_pace_df = merged_qualifying_df.copy()

    columns_wanted = ["round", driver1_surname, driver2_surname]

    qualifying_pace_df = qualifying_pace_df.loc[:, columns_wanted]

    # # Drop unnecessary columns
    # columns_to_drop = ["name", f'q1{driver1_surname}', f'q2{driver1_surname}', f'q3{driver1_surname}',
    #                    f'q1{driver2_surname}', f'q2{driver2_surname}', f'q3{driver2_surname}']
    # qualifying_pace_df = qualifying_pace_df.drop(columns=columns_to_drop, inplace=True)


    # Replace "\N" with NaN
    qualifying_pace_df.replace("\\N", np.nan, inplace=True)

    # Remove all rows containing null values
    qualifying_pace_df.dropna(inplace=True)

    # Reset index
    qualifying_pace_df.reset_index(inplace=True)

    # Set the index of the DataFrame to 'round' column
    qualifying_pace_df.set_index('round', inplace=True)

    # # Convert q1, q2, and q3 columns to datetime
    # qualifying_pace_df[f'q1{driver1_surname}'] = pd.to_datetime(qualifying_pace_df[f'q1{driver1_surname}'],
    #                                                             format='%M:%S.%f')
    # qualifying_pace_df[f'q2{driver1_surname}'] = pd.to_datetime(qualifying_pace_df[f'q2{driver1_surname}'],
    #                                                             format='%M:%S.%f')
    # qualifying_pace_df[f'q3{driver1_surname}'] = pd.to_datetime(qualifying_pace_df[f'q3{driver1_surname}'],
    #                                                             format='%M:%S.%f')
    # qualifying_pace_df[f'q1{driver2_surname}'] = pd.to_datetime(qualifying_pace_df[f'q1{driver2_surname}'],
    #                                                             format='%M:%S.%f')
    # qualifying_pace_df[f'q2{driver2_surname}'] = pd.to_datetime(qualifying_pace_df[f'q2{driver2_surname}'],
    #                                                             format='%M:%S.%f')
    # qualifying_pace_df[f'q3{driver2_surname}'] = pd.to_datetime(qualifying_pace_df[f'q3{driver2_surname}'],
    #                                                             format='%M:%S.%f')
    #
    # # Find the fastest time for each driver for each round
    # qualifying_pace_df[f"time{driver1_surname}"] = qualifying_pace_df[[f'q1{driver1_surname}', f'q2{driver1_surname}', f'q3{driver1_surname}']].min(axis=1)
    # qualifying_pace_df[f"time{driver2_surname}"] = qualifying_pace_df[[f'q1{driver2_surname}', f'q2{driver2_surname}', f'q3{driver2_surname}']].min(axis=1)



    # qualifying_pace_df = qualifying_pace_df.rename(
    #     columns={driver1_surname: f'position{driver1_surname}', driver2_surname: f'position{driver2_surname}'})

    # f'time{driver1_surname}', f'time{driver2_surname}'



    # # Rename the driver's columns
    # qualifying_pace_pace_df = qualifying_pace_df.rename(
    #     columns={f'time{driver1_surname}': driver1_surname, f'time{driver2_surname}': driver2_surname})

    with col2:
        st.markdown("## Qualifying positions")
        # Plot the line chart
        st.line_chart(qualifying_pace_df[[driver1_surname, driver2_surname]])
    #------------------------------------------------------------------------------------------------------------------------------
    # Replace "\N" with NaN
    race_positions_df = merged_df.copy()
    race_positions_df.replace("\\N", np.nan, inplace=True)

    # Remove all rows containing null values
    race_positions_df.dropna(inplace=True)

    # Reset index
    race_positions_df.reset_index(inplace=True)

    # Set the index of the DataFrame to 'round' column
    race_positions_df.set_index('round', inplace=True)
    with col1:
        st.markdown("## Race positions")
        # Plot the line chart
        st.bar_chart(race_positions_df[[driver1_surname, driver2_surname]])


if __name__ == "__main__":
    main()
