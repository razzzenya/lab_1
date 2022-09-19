from calendar import month
from nturl2path import url2pathname
import os
from bs4 import BeautifulSoup
import requests
import csv

def MaxYearChecker(url): #функция проверки последнего года доступного на сайте
    flag=0
    year_counter=2008
    
    while (flag==0): # цикл пробегает по всем возможным годам путём замены ссылки . В случае не существующей страницы цикл while останавливается
        html_text = requests.get(url, headers={'User-Agent':'agent'}).text 
        data = BeautifulSoup(html_text, 'lxml')
        if data.find('span', class_='grey error-span'): # проверка существования элемента на странице , который отвечает за ошибку 404
            flag = 1
            year_counter -= 1
        else:
            year_counter += 1
            url = url.replace(str(year_counter - 1),str(year_counter)) #замена года в url с предыдущего на текущий

    return year_counter

def MaxMonthChecker(url):  #функция проверки последнего месяца доступного на сайте
    flag=0
    month_counter = 1
    while (flag==0): # цикл пробегает по всем возможным месяцам путём замены ссылки . В случае не существующей страницы смотреть стр.34
        html_text = requests.get(url, headers={'User-Agent':'agent'}).text
        data = BeautifulSoup(html_text, 'lxml')
        if data.find('span', class_='grey error-span'): # проверка существования элемента на странице , который отвечает за ошибку 404
            flag = 1
            month_counter -= 1
        else:
            month_counter += 1
            url = url[0:39]+ '/' + str(month_counter) + '/'  #с месяцами функция .replace делает неправильную замену , поэтому перезаписываю старую ссылку в переменную и меняю в ней послдение цифры
    
    return month_counter

def UrlMonthChange (url, months, flag):
    if flag == 1: # случай когда месяц является 12 , то есть - последним. Необходим переход на след. год , поэтому меняю значение 'months' на 1
        url = url[0:39] + '/1/' # здесь заменяется 12-ый месяц в ссылке на 1-ый
    elif flag == 2:
        url = url[0:39] + '/' + str(months) + '/' 
    return url

def UrlYearChange (url, years):
    url = url.replace(str(years-1),str(years)) # так как изначальная ссылка имеет 2008 год , а не 2007 , замена не произойдёт и первая итерация цикла 'for' будет корректной
    return url

def DataToList (output, elements):
    x = [0,1,2,5,6,7,10]
    for i in x:
        output.append(elements[i].text)
    return output

url = 'https://www.gismeteo.ru/diary/4618/2008/1/' # изначальная ссылка , самым ранним годом имеющим данные является 2008
year_counter = 2008
current_year = MaxYearChecker(url) #заранее узнаём максимальный год доступный на сайте , для 1-го цикла for

for years in range(year_counter, current_year + 1):  
    url = UrlYearChange(url, years)
    max_month = 12
    if (years == current_year):
        max_month = MaxMonthChecker(url)

    for months in range(1, max_month + 1): 
        flag_month = 0
        if (months == max_month):
            url = UrlMonthChange(url, months, 2) 
            flag_month = 1
        elif (months < max_month):
            url = UrlMonthChange(url, months, 2)


        html_text = requests.get(url, headers={'User-Agent':'Ivan'}).text
        soup = BeautifulSoup(html_text, 'lxml')
        lines = soup.find_all('tr', align = 'center')

        for i in range (len(lines)):
            elements = lines[i].find_all('td')
            output=[]
            output = DataToList(output , elements)#список для вывода
            with open('example.csv','a',encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow((output[0],output[1],output[2],output[3],output[4],output[5],output[6]))
        if flag_month == 1:
           url = UrlMonthChange(url, months, 1)