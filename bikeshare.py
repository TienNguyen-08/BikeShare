import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york.csv',
    'washington': 'washington.csv'
}

# Helper function to get a valid user input from a list of options
def get_user_choice(prompt, options):
    choice = None
    while choice not in options:
        choice = input(prompt).lower()
        if choice not in options:
            print(f"Invalid input. Please enter one of the following: {', '.join(options)}")
    return choice

def get_filters():
    print("Hello! Let's explore some US bikeshare data!")

    city = get_user_choice(
        "\nPlease choose the city you want to filter data [chicago, new york, washington]: ",
        ['chicago', 'new york', 'washington']
    )

    month = get_user_choice(
        "Please choose a month you want to filter (all, january, february, ... , june): ",
        ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    )

    day = get_user_choice(
        "Please choose a day you want to filter (all, monday, tuesday, ... sunday): ",
        ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    )

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def display_rows(df):
    """Displays the first 5 rows of the dataframe and asks if the user wants to see more."""
    start_loc = 0
    while True:
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5

        more_rows = input("\nDo you want to see the next 5 rows of the data? Enter yes or no: ").lower()
        if more_rows != 'yes':
            break

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('Most common Month'.ljust(30, '.'), common_month)

    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week'.ljust(30, '.'), common_day)

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common Start Hour'.ljust(30, '.'), common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most commonly used Start station '.ljust(30, '.'), df['Start Station'].mode()[0])
    print('Most commonly used End station '.ljust(30, '.'), df['End Station'].mode()[0])

    df['route'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most frequent route '.ljust(30, '.'), df['route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = np.sum(df['Trip Duration'])
    mean_travel_time = np.mean(df['Trip Duration'])
    most_travel_time = np.argmax(np.bincount(df['Trip Duration'].astype(int)))

    print('Total Travel Time '.ljust(30, '.'), total_travel_time)
    print('Avg Travel Time '.ljust(30, '.'), mean_travel_time)
    print('Most Travel Time '.ljust(30, '.'), most_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 70)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print(' User type stats '.center(60, '-'))
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print(' Gender '.center(60, '-'))
        df.fillna({'Gender': 'Not specified'}, inplace=True)
        print(df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        print(' Age '.center(60, '-'))
        print('Earliest Birth Year '.ljust(40, '.'), int(df['Birth Year'].min()))
        print('Most recent Birth Year '.ljust(40, '.'), int(df['Birth Year'].max()))
        print('Most common Birth Year '.ljust(40, '.'), int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 50)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_data = input("\nDo you want to check the first 5 rows of the dataset related to the chosen city? Enter yes or no: ").lower()
        if show_data == 'yes':
            display_rows(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
