import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
cities = {'a':'chicago','b':'washington', 'c':'new york city'}
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
            city_selection = input("Would you like to see the data for a: Chicago, b: Washington or c: New York?\n")
            if city_selection in ['a','b','c']:
                break
        except KeyboardInterrupt as e:
                print("Invalid selection")

    city = cities[city_selection].lower()

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please choose a month: January, February, March, April, May, June\n")
        if month not in months:
            print("Please enter a valid format\n")
        else:
            break

    month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("Please choose a day by number(i.e. 1=Sunday)\n")
        if int(day) < 0 or int(day) > 7:
            print("Please enter a valid format\n")
        else:
            break

    day = days[int(day) - 1]

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
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
    try:
        # display the most common month
        print("The most common month is ", df['month'].value_counts().idxmax())
        # display the most common day of week
        print("The most common day of the week is ", df['day_of_week'].value_counts().idxmax())
        # display the most common start hour
        print("The most common start hour is ", df['Start time'].value_counts().idxmax())
    except ValueError as e:
        print(e.args)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    try:
        # display most commonly used start station
        print("The most common start station is ", df['Start Station'].value_counts().idxmax())
        # display most commonly used end station
        print("The most common end station is ", df['End Station'].value_counts().idxmax())
        # display most frequent combination of start station and end station trip
        print("The most frequent combination of start station and end station trip is ", df.groupby(['Start Station', 'End Station'].size().idxmax()))
    except ValueError as e:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        # display total travel time
        print("Total travel time is ", sum(df['Trip Duration']))
        # display mean travel time
        print("Mean travel time is ", df.loc[:, "Trip Duration"].mean())
    except ValueError as e:
        print(e.args)
    except Exception as e:
        print(e.args)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts of user types
        print("User Types: ", df['User Type'].value_counts())
        # Display counts of gender
        print("Gender count: ", df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print("Earliest Year of Birth ", df['Birth Year'].min())
        print("Most Recent Year of Birth ", df['Birth Year'].max())
        print("Most Common Year of Birth ", df['Birth Year'].value_counts().idxmax())
    except KeyError as e:
        print(e.args)
    except Exception as e:
        print(e.args)

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
