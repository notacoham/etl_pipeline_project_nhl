import requests
import pandas as pd
import matplotlib.pyplot as plt

class StandingAnalyzer:
    def __init__(self, date='2024-12-07'):
        self.date = date
        self.base_url = f'https://api-web.nhle.com/v1/standings/{date}'
        self.standing_data = None

    def get_standing_data(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()

            self.standing_data = response.json()
            return self.standing_data
        except requests.RequestException as e:
            print(f'Error fetching standing data: {e}')
            return None
        
    def create_standings_dataframe(self):
        if not self.standing_data:
            self.get_standing_data()
        
        if not self.standing_data:
            print('Error, cannot plot without standing data.')
            return None
        
        teams = (
            self.standing_data.get('standings', [])
        )

        return pd.DataFrame(teams)
    
    def plot_standings_data(self, scatter_x_axis='goalFor', scatter_y_axis='points'):
        if not self.standing_data:
            self.get_standing_data()

        if not self.standing_data:
            print('Error, no roster data detected')
            return None
        
        df = self.create_standings_dataframe()

        if df is None:
            print('Error, cannot plot without data')
            return None
                
        plt.scatter(df[scatter_x_axis], df[scatter_y_axis])
        plt.title(f'Scatter Plot Distribution of {scatter_x_axis} by {scatter_y_axis}')
        plt.xlabel(f'{scatter_x_axis}')
        plt.ylabel(f'{scatter_y_axis}')
        plt.show()

    def display_standings(self):
        if not self.standing_data:
            self.get_standing_data()

        if not self.standing_data:
            print('Error, no roster data detected')
            return None
        
        df = self.create_standings_dataframe()
        
        if df is None:
            print('Error, cannot plot without data')
            return None
                
        return df['placeName']
        
        

# Create instance of the Standing analyzer
analyzer = StandingAnalyzer()

# Instantiate the dataframe
dataframe = analyzer.create_standings_dataframe()

# Display Standings in the terminal
current_standings = analyzer.display_standings()
print(current_standings)

# Plot data using matplotlib
standing_plot = analyzer.plot_standings_data()