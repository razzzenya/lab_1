from bs4 import BeautifulSoup
import requests
import csv


def max_year_checker(url):
    flag = 0
    year_counter = 2008

    while (flag == 0):
        html_text = requests.get(url, headers={'User-Agent': 'agent'}).text
        data = BeautifulSoup(html_text, 'lxml')
        if data.find('span', class_='grey error-span'):
            flag = 1
            year_counter -= 1
        else:
            year_counter += 1
            url = url.replace(str(year_counter - 1), str(year_counter))

    return year_counter


def max_month_checker(url):
    flag = 0
    month_counter = 1

    while (flag == 0):
        html_text = requests.get(url, headers={'User-Agent': 'agent'}).text
        data = BeautifulSoup(html_text, 'lxml')
        if data.find('span', class_='grey error-span'):
            flag = 1
            month_counter -= 1
        else:
            month_counter += 1
            url = url[0:39] + '/' + str(month_counter) + '/'

    return month_counter


def url_month_change(url, months, flag):
    if flag == 1:
        url = url[0:39] + '/1/'
    elif flag == 2:
        url = url[0:39] + '/' + str(months) + '/'
    return url


def url_year_change(url, years):
    url = url.replace(str(years-1), str(years))
    return url


def data_to_list(output, elements):
    x = [0, 1, 2, 5, 6, 7, 10]
    for i in x:
        output.append(elements[i].text)
    return output


def days_redact(output):
    if (int(output[0]) < 10):
        return ('0' + output[0])

    else:
        return (output[0])


def months_redact(month):
    if (month < 10):
        return ('0' + str(month))

    else:
        return (str(month))


url = 'https://www.gismeteo.ru/diary/4618/2008/1/'
year_counter = 2008
current_year = max_year_checker(url)

for years in range(year_counter, current_year + 1):
    url = url_year_change(url, years)
    max_month = 12
    if (years == current_year):
        max_month = max_month_checker(url)

    for months in range(1, max_month + 1):
        is_month_last = False
        if (months == max_month):
            url = url_month_change(url, months, 2)
            is_month_last = True
        elif (months < max_month):
            url = url_month_change(url, months, 2)

        html_text = requests.get(url, headers={'User-Agent': 'Ivan'}).text
        soup = BeautifulSoup(html_text, 'lxml')
        lines = soup.find_all('tr', align='center')

        for i in range(len(lines)):
            elements = lines[i].find_all('td')
            output = []
            output = data_to_list(output, elements)
            with open('result.csv', 'a', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, lineterminator='\n')
                writer.writerow((str(years) + '-' + months_redact(months) + '-' + days_redact(
                    output), output[1], output[2], output[3], output[4], output[5], output[6]))
        if is_month_last == True:
            url = url_month_change(url, months, 1)
