import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str()
    while (city != 'chicago') and (city != 'new york city') and (city != 'washington'):
        city = input('\nWhich city\'s data would you like to analyze? Please enter Chicago, New York City, or Washington.\n')
        city = city.lower()

    # get user input for month (all, january, february, ... , june)
    month = str()
    filter_month = input('\nWould you like to filter by month? (y or n)\n')
    filter_month = filter_month.lower()
    while (filter_month != 'y') and (filter_month != 'n'):
        filter_month = input('Response not valid. Filter by month? Please enter y or n.\n')
        filter_month = filter_month.lower()
    if filter_month == 'y':
    	while month not in months:
            month = input('Please select a month from January to June:\n')
            month = month.lower()
    else:
    	month = 'all'


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = str()
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    filter_day = input('\nWould you like to filter by day? (y or n)\n')
    filter_day = filter_day.lower()
    while (filter_day != 'y') and (filter_day != 'n'):
        filter_day = input('Response not valid. Filter by day? Please enter y or n.\n')
        filter_day = filter_day.lower()
    if filter_day == 'y':
    	while day not in days:
    		day = input('Please select a day of the week:\n')
    		day = day.lower()
    else:
    	day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('\nMost Common Month:', months[popular_month - 1].title())

    # display the most common day of week
    popular_day = df['Day of Week'].mode()[0]
    print('\nMost Common Day of Week:', popular_day)

    # display the most common start hour - extract hour from the Start Time column to create an hour column
    df['Hour'] = df['Start Time'].dt.hour
    # find the most common hour (from 0 to 23)
    popular_hour = df['Hour'].mode()[0]
    print('\nMost Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost Commonly Used Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost Commonly Used End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Station Combo'] = df['Start Station'] + ' to ' + df['End Station']
    station_combination = df['Station Combo'].mode()[0]
    print('\nMost Frequent Combination of Start and End Station:', station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal Travel Time: {} seconds'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean Travel Time: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender where available
    try:
        user_gender = df['Gender'].value_counts()
        print('\nBreakdown by Gender:')
        print(user_gender)
    except:
    	print('\nNo Gender Data Available')

    # Display earliest, most recent, and most common year of birth where available
    try:
        birth_years = df['Birth Year']
        print('\nEarliest Birth Year:', birth_years.min())
        print('\nMost Recent Birth Year:', birth_years.max())
        print('\nMost Common Birth Year:', birth_years.mode()[0])
    except:
    	print('\nNo Birth Year Data Available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Generator function used to iterate through raw data at user's discretion.
        def data_range(x):
            i = 0
            while i < x:
                yield i
                i += 1

        # Gives user the option to see raw data.
        display_data = input('\nWould you like to display individual trip data? (y or n)\n')
        while display_data == 'y':
            for x in data_range(df.ndim):
            	print()
            	print(df.iloc[x])
            	display_data = input('\nDisplay more data? (y or n)\n')

        # Gives user the option to start over and analyze the data using new filter options.
        restart = input('\nWould you like to restart? (y or n)\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()