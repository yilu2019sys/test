from datetime import datetime


def age_of_tree(ab_dates):
    year = datetime.now()
    year = year.year

    date = ab_dates  # date
    date = datetime.strptime(date, '%Y%m%d').year

    age = year-date
    return age


if __name__ == "__main__":
    age = age_of_tree('20170101')
    print('age', age)
    
    print('fin')
