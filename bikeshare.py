import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
days = {'1':'sunday',
        '2':'monday',
        '3':'tuesday',
        '4':'wednesday',
        '5':'thursday',
        '6':'friday',
        '7':'saturday',
        'all':'all'}
cities = {'a':'chicago',
          'b':'washington',
          'c':'new york city'}
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

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
    while True:
        try:
            city_selection = input("Would you like to see the data for\n a: Chicago\n b: Washington\n c: New York\n")
            if city_selection.lower() in ['a','b','c']:
                break
        except KeyboardInterrupt as ex:
                print("Invalid selection\n")

    city = cities[city_selection.lower()].lower()

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please choose a month:\n january\n february\n march\n april\n may\n june\n all\n")
            if month.lower() not in months:
                print("Please enter a valid format\n")
            else:
                break
        except KeyboardInterrupt as ex:
            print("Invalid selection\n")

    month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        try:
            day_selection = input("Please choose a day by number (i.e. 1=Sunday)\n")
            if day_selection == 'all':
                break
            if int(day_selection) < 0 or int(day_selection) > 7:
                print("Please enter a valid format\n")
            else:
                break
        except KeyboardInterrupt as ex:
            print("Invalid selection\n")

    day = days[day_selection]

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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    try:
        # display the most common month
        # extract month from the Start Time column to create a month column
        df['month'] = df['Start Time'].dt.month
        # find the most popular month
        popular_month = df['month'].mode()[0]
        print('Most Popular Month:', popular_month)

        # display the most common day of week
        # extract day from the Start Time column to create a day column
        df['day'] = df['Start Time'].dt.day
        # find the most popular day
        popular_day = df['day'].mode()[0]
        print('Most Popular Day:', popular_day)

        # display the most common start hour
        # extract hour from the Start Time column to create an hour column
        df['hour'] = df['Start Time'].dt.hour
        # find the most popular hour
        popular_hour = df['hour'].mode()[0]
        print('Most Popular Start Hour:', popular_hour)
    except ValueError as ex:
        print(ex.args)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    try:
        # display most commonly used start station
        print("The most common start station is", df['Start Station'].value_counts().idxmax(axis = 1, skipna = True))
        # display most commonly used end station
        print("The most common end station is", df['End Station'].value_counts().idxmax(axis = 1, skipna = True))
        # display most frequent combination of start station and end station trip
        print("The most frequent combination of start station and end station trip is", df.groupby(['Start Station', 'End Station']).size().idxmax(axis = 1, skipna = True))
    except ValueError as ex:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        # display total travel time
        print("Total travel time is", sum(df['Trip Duration']))
        # display mean travel time
        print("Mean travel time is", df.loc[:, "Trip Duration"].mean())
    except ValueError as ex:
        print(ex.args)
    except Exception as ex:
        print(ex.args)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts of user types
        print("User Types:\n", df['User Type'].value_counts().to_string())
        # Display counts of gender
        print("Gender count:\n", df['Gender'].value_counts().to_string())
        # Display earliest, most recent, and most common year of birth
        print("Earliest Year of Birth", df['Birth Year'].min())
        print("Most Recent Year of Birth", df['Birth Year'].max())
        print("Most Common Year of Birth", df['Birth Year'].value_counts().idxmax(axis = 1, skipna = True))
    except KeyError as ex:
        print(ex.args)
    except Exception as ex:
        print(ex.args)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(city):
    print("Raw Data is available to view...\n")
    display_raw = input("Do you want to display it? Type yes or no.\n")
    while display_raw == 'yes':
        try:
            for chunk in pd.read_csv(CITY_DATA[city], chunksize = 5):
                print(chunk)
                display_raw = input("Do you want to display it? Type yes or no.\n")
                if display_raw != 'yes':
                    print('Thank you\n')
                    break
                break
        except KeyboardInterrupt:
            print('Goodbye!')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
