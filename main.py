import streamlit as st
import pandas as pd

# Global variables to store user inputs
selected_season = None
selected_pairing = None
ok_button_clicked = False

# Function to get F1 seasons
def get_f1_seasons():
    return list(range(2003, 2024))


# Function to get driver pairings for a specific season
def get_driver_pairings(season):
    # Dummy data, you would replace this with actual API calls
    driver_pairings = {
        2003: [("Driver A", "Driver B"), ("Driver C", "Driver D")],
        2004: [("Driver E", "Driver F"), ("Driver G", "Driver H")],
        # Add data for other seasons
        # ...
        2023: {
            "Alfa Romeo": [("Alfa Romeo", "Bottas", "Zhou")],
            "Alpine": [("Alpine", "Gasly", "Ocon")],
            "Aston Martin": [("Aston Martin", "Alonso", "Stroll")],
            "AlphaTauri": [("AlphaTauri", "de Vries", "Ricciardo"), ("AlphaTauri", "Lawson", "Tsunoda")],
            "Ferrari": [("Ferrari", "Leclerc", "Sainz")],
            "Haas": [("Haas", "Magnussen", "Hülkenberg")],
            "McLaren": [("McLaren", "Norris", "Piastri")],
            "Mercedes": [("Mercedes", "Hamilton", "Russell")],
            "Red Bull": [("Red Bull", "Verstappen", "Pérez")],
            "Williams": [("Williams", "Sargeant", "Albon")]
        }
    }

    return driver_pairings.get(season, [])


# Main function to build the UI
def main():
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
    st.title("Results")
    st.write("Selected F1 Season:", selected_season)
    st.write("Selected Driver Pairing:", selected_pairing)
    season_pairings = get_driver_pairings(selected_season)

    # Extract surnames from tuples
    driver1_surname = selected_pairing.split("vs")[0].split(":")[1].strip()
    driver2_surname = selected_pairing.split("vs")[1].strip()
   
    st.write(driver1_surname)
    st.write(driver2_surname)
    races_and_results_df = pd.read_csv(r"C:/Users/danie/PycharmProjects/formula-one-teammate-analysis/races_results_drivers.csv")

    # Filter DataFrame based on selected F1 season
    df_season = races_and_results_df[races_and_results_df['year'] == selected_season]

    # Accessing corresponding round and position for the driver's surname
    driver_1_info = df_season[df_season['surname'] == driver1_surname]
    if not driver_1_info.empty:
        driver_1_round = driver_1_info['round'].values[0]
        driver_1_position = driver_1_info['position'].values[0]
        st.write(f"For {driver1_surname}: Round {driver_1_round}, Position {driver_1_position}")
    else:
        st.write(f"Driver {driver1_surname} not found in the DataFrame.")

    driver_2_info = df_season[df_season['surname'] == driver2_surname]
    if not driver_2_info.empty:
        driver_2_round = driver_2_info['round'].values[0]
        driver_2_position = driver_2_info['position'].values[0]
        st.write(f"For {driver2_surname}: Round {driver_2_round}, Position {driver_2_position}")
    else:
        st.write(f"Driver {driver2_surname} not found in the DataFrame.")

    # Create dictionaries to store the data for each driver
    driver1_data = {'round': [], 'name': [], 'position': []}
    driver2_data = {'round': [], 'name': [], 'position': []}

    # Iterate over the DataFrame to extract the required information
    for index, row in df_season.iterrows():
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

    # Remove the index from the DataFrame
    merged_df = merged_df.reset_index(drop=True)
    st.dataframe(merged_df, hide_index=True)

    # Function to highlight cells based on condition
    def highlight_cell(row):
        """Highlight cells based on position comparison."""
        styles = ['background-color: lightgreen' if row[driver1_surname] < row[driver2_surname] else '',
                  'background-color: lightgreen' if row[driver2_surname] < row[driver1_surname] else '']
        return styles

    # Apply conditional formatting
    formatted_df = merged_df.style.apply(highlight_cell, axis=1,
                                         subset=pd.IndexSlice[:, [driver1_surname, driver2_surname]])

    # Display formatted DataFrame in Streamlit
    st.dataframe(formatted_df, hide_index=True)

    # # Group by round and name (Grand Prix)
    # grouped = df_season.groupby(['round', 'name'])
    #
    # st.write(grouped)

    # # Create a DataFrame to hold race positions
    # race_positions = pd.DataFrame(index=grouped.groups.keys())
    #
    # # Get unique driver surnames
    # drivers = races_and_results_df['surname'].unique()
    #
    # # Create columns for each driver
    # for driver in drivers:
    #     race_positions[driver] = None
    #
    # # Fill the DataFrame with race positions for each driver
    # for (round, grand_prix), group in grouped:
    #     for driver, position in group[['surname', 'position']].values:
    #         race_positions.loc[(round, grand_prix), driver] = position
    #
    # # Color the cells based on race positions
    # def color_negative_green(val):
    #     color = 'green' if val == min(group['position']) else 'white'
    #     return f'background-color: {color}'
    #
    # # Apply cell coloring
    # race_positions_styled = race_positions.style.applymap(color_negative_green)
    #
    # # Display the table
    # st.write(race_positions_styled)


if __name__ == "__main__":
    main()
