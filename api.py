# response = requests.get(f"http://ergast.com/api/f1/{selected_season}/5/drivers/{selected_pairing[0]}/laps/1")
# if response.status_code == 200:
#     try:
#         # Convert XML response to dictionary
#         data_dict = xmltodict.parse(response.content)
#
#         # Convert dictionary to JSON
#         json_data = json.dumps(data_dict, indent=4)
#         st.json(json_data)  # Display JSON data
#     except Exception as e:
#         st.error(f"Failed to convert XML to JSON: {e}")
# else:
#     st.error(f"Error: {response.status_code}")
#     data = response.json()  # Parse JSON response
#     st.write(data)  # Display the data