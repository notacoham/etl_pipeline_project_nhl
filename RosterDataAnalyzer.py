import requests 
import pandas as pd
import matplotlib.pyplot as plt

class RosterDataAnalyzer:
    def __init__(self, team_abbreviation, season='20242025'):
        self.team_abbreviation = team_abbreviation
        self.season = season
        self.base_url = f'https://api-web.nhle.com/v1/roster/{team_abbreviation}/{season}'
        self.roster_data = None

    def get_roster_data(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()

            self.roster_data = response.json()
            return self.roster_data
        except requests.RequestException as e:
            print(f'Error fetching roster data: {e}')
            return None
        
    def create_player_dataframe(self):
        if not self.roster_data:
            self.get_roster_data()

        if not self.roster_data:
            print("Error, no roster data detected.")
            return None
        
        players = (
            self.roster_data.get('forwards', []) + 
            self.roster_data.get('defensemen', []) + 
            self.roster_data.get('goalies', [])
        )

        return(pd.DataFrame(players))

    def get_roster_count(self):
        if not self.roster_data:
            self.get_roster_data()

        if not self.roster_data:
            print('Error, no roster data detected')
            return None
        
        return (
            len(self.roster_data.get('forwards', [])) + 
            len(self.roster_data.get('defensemen', [])) + 
            len(self.roster_data.get('goalies', [])) 
        )
    
    def plot_player_stats(self, stat_column='heightInCentimeters'):
        """
        Create a visualization of player statistics.
        
        :param stat_column: Column to visualize (default: 'height')
        """
        df = self.create_player_dataframe()
        
        if df is None:
            print("Cannot create plot without player data")
            return
        
        plt.figure(figsize=(10, 6))
        df[stat_column].hist()
        plt.title(f'Distribution of Player {stat_column.capitalize()}')
        plt.xlabel(stat_column.capitalize())
        plt.ylabel('Number of Players')
        plt.show()
        
    def load_data_to_csv(self):
        df = self.create_player_dataframe()
        
        if df is None:
            print("Cannot create file without player data")
            return
        
        df.to_csv(f'roster_data_{self.season}', index=False)

    def read_csv_data(self):
        read_df = pd.read_csv(f'roster_data_{self.season}')
        return read_df


# Create instance of RosterDataAnalyzer
team_roster = RosterDataAnalyzer('uta', '20242025')

# Instantiate the player dataframe
player_dataframe = team_roster.create_player_dataframe()

# Run player count function
player_count = team_roster.get_roster_count()
print(player_count)

# plot the player stats
stats = team_roster.plot_player_stats()

# load to new csv file
load = team_roster.load_data_to_csv()

# read csv file
read = team_roster.read_csv_data()
print(read)