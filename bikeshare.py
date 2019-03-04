import pandas as pd
import time
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """

    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ['chicago', 'washington', 'new york city']
    mth = ['january', 'february','march', 'april', 'may', 'june']
    avail_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    responses =['month', 'day','both', 'none']
    city = input("What city do you want to analyze, chicago,new york city, washington?").lower()
    while city not in cities:
       city = input("city not available, enter a valid city").lower()
    response = input("do you want to filter by month, day or both? type 'none' for no time filters").lower()
    while response not in responses:
        response = input("Enter a valid response please. Do you want to filter by month, day or both? type 'none' for no time filter").lower()
    if response == "month":
        month = input("Enter the month you want to filter with e.g january, february e.t.c").lower()
        day = 'all'
        while month not in mth:
           month = input("month not available,The month you entered must not exceed 'june'.Pls enter a valid month").lower()

    elif response == "day":
        day = input("Enter the day you want to filter with e.g. sunday, friday e.t.c").lower()
        month ='all'
        while day not in avail_day:
           day = input("Day not available. Enter a valid day e.g, sunday, monday etc ").lower()

    elif response =="both":
        month = input("which month? e.g january, february e.t.c").lower()
        while month not in mth:
           month = input("month not available,The month you entered must not exceed 'june'.Pls enter a valid month").lower()
        day = input("which day? Please enter the day e.g. sunday, friday e.t.c").lower()
        while day not in avail_day:
           day = input("Day not available. Enter a valid day e.g. sunday, monday, friday").lower()

    else:
        day ='all'
        month = 'all'
        print("Your data will display without a filter")
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
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
        print('-'*40)
    return df

def time_stats(df):
    """
    This function computes the time statistics as requested by the users
    Args: Dataframe received from the load_data function
    """
    start_time = time.time()
    print("Computing the most frequent times of travel.")
    # find the most popular hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    count = df['hour'].value_counts().head(1)
    print('count:{}'.format(count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    # find the most popular day
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular day_of_week:', popular_day)
    count = df['day_of_week'].value_counts().head(1)
    print('count:{}'.format(count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    # find the most popular month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Popular month:', popular_month)
    count = df['month'].value_counts().head(1)
    print('count:{}'.format(count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    start_time = time.time()
    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('\nThe Most Popular Start Stations is...\n')
    # find the most popular start station
    popular_start_station = df['Start Station'].mode()[0]
    print('popular start station:', popular_start_station)
    count = df['Start Station'].value_counts().head(1)
    print('count:{}'.format(count))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('\nThe Most Popular End Stations is...\n')

    popular_end_station = df['End Station'].mode()[0]
    print('popular end station:', popular_end_station)
    count = df['End Station'].value_counts().head(1)
    print('count:{}'.format(count))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\nThe Most Popular End and Star Stations are...\n')
    df['start_and_end_station'] = df['Start Station'] + df['End Station']
    popular_start_end_station = df['start_and_end_station'].mode()[0]
    print('popular end and start station:', popular_start_end_station)
    count = df['start_and_end_station'].value_counts().head(1)
    print('count:{}'.format(count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print(df.describe())
    df.loc['sum'] = df['Trip Duration'].sum()
    df.loc['mean'] = df['Trip Duration'].mean()
    Total_travel_time =  df.loc['sum']['Trip Duration']
    mean_travel_time = df.loc['mean']['Trip Duration']
    print("Total travel time is:{}".format(Total_travel_time))
    print("Mean travel time is:{}".format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def user_stats(df):
    try:
        """Displays statistics on bikeshare users."""
        print('\nCalculating User Stats...\n')
        start_time = time.time()
        user_types = df['User Type'].value_counts().head(1)
        print(user_types)
        gender = df['Gender'].value_counts().head(1)
        print(gender)
        df.sort_values(by=['Birth Year'])
        print('earliest birth year:.....')
        print(df['Birth Year'].head(1))
        popular_birth_year = df['Birth Year'].mode()[0]
        print('Most Popular year:', popular_birth_year)
        count = df['Birth Year'].value_counts().head(1)
        print('count:{}'.format(count))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print(" An error occured. Possibly a missing raw data to compute your request")

def display_data(city):
    """Displays raw data on bikeshare users."""
    df = pd.read_csv(CITY_DATA[city])
    response = input('Do you want to see the raw data?yes or no?')
    count = 5
    while response == 'yes':
        print(df.iloc[1 : (count + 1 )])
        count += 5
        response = input('Do you want to see more raw data? yes or no?')
    return

def main():
    """ This is the main function"""
    while True:

        city, month, day = get_filters()
        display_data(city)

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
