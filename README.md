
# **Spotify Recently Played Tracks Tracker**

**Description:**
This project is a simple tool to track and store information about the tracks a Spotify user has recently played. It utilizes the Spotify Web API to retrieve the user's recently played tracks and stores them in a SQLite database. The tool is written in Python and utilizes libraries such as Pandas, Requests, and SQLAlchemy.

**How it Works:**
1. **Data Retrieval:** The script sends a request to the Spotify API to fetch the user's recently played tracks.
2. **Data Processing:** It extracts relevant information such as song name, artist name, played timestamp, and date from the API response.
3. **Data Validation:** The script checks if the retrieved data is valid, ensuring there are no empty datasets, duplicate timestamps, or null values.
4. **Database Setup:** It creates a SQLite database if it doesn't exist already and defines a table schema to store the track information.
5. **Data Storage:** The script saves the track data into the SQLite database.
6. **Error Handling:** It handles exceptions such as existing data in the database.
7. **Logging:** The script prints messages indicating the status of each stage of execution.

**Project Structure:**
- `spotify_recently_played.py`: Main script file containing the code.
- `my_played_tracks.sqlite`: SQLite database file to store the track information.

**Setup:**
1. Install the required Python libraries: `pandas`, `requests`, `sqlalchemy`.
2. Obtain a Spotify API token and replace the `TOKEN` variable with your token.
3. Run the script to start tracking your recently played tracks.

**Usage:**
- Execute the script to fetch and store your recently played tracks.
- Check the database to view the stored track information.

**Future Enhancements:**
- Add functionality to visualize track listening trends over time.
- Implement user authentication for secure access to the stored data.
- Extend support for multiple users or playlists.

**Note:**
- Ensure your Spotify account is active and connected to the Spotify Web API.
- Regularly update the Spotify API token to maintain access to the service.
