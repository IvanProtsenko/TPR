# -*- coding: utf-8 -*-
from prettytable import PrettyTable

import csv


def importData():
    output = []
    with open("input_data.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            output.append(row)
    return output


def printTable(data):
    output = []
    header = list(data[0])
    table = PrettyTable(header)
    for i in range(1, len(data)):
        for j in range(len(header)):
            output.append(data[i][j])
    while output:
        table.add_row(output[:len(header)])
        output = output[len(header):]
    print(table)


def makeParett(data):
    output = [data[0]]
    for i in range(1, len(data)):
        for j in range(i+1, len(data)):
            result = []
            for k in range(2, len(data[0])):
                if data[0][k][-2] == '+':
                    param1 = data[i][k]
                    param2 = data[j][k]
                else:
                    param1 = -data[i][k]
                    param2 = -data[j][k]
                if param1 > param2:
                    result.append(i)
                elif param1 < param2:
                    result.append(j)
                else:
                    result.append('-')
            if i in result and j not in result:
                output.append(data[i])
            elif i not in result and j in result:
                output.append(data[j])
    return output


def firstSort(data):
    sorting = []
    working = data[:]
    output = [working[0]]
    with open("first_params.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            sorting.append(row)
    sorting = sorting[0]
    for i in range(1, len(working)):
        comp_res = []
        for j in range(len(sorting)):
            if sorting[j] == '-':
                comp_res.append('+')
                continue
            if working[0][j+2][-2] == '+' and working[i][j+2] >= sorting[j]:
                comp_res.append('+')
                continue
            if working[0][j+2][-2] == '-' and working[i][j+2] <= sorting[j]:
                comp_res.append('+')
                continue
            comp_res.append('-')
            break
        if '-' not in comp_res:
            output.append(working[i])
    return output


def secondSort(data):
    sorting = []
    working = data[:]
    output = [working[0]]
    with open("second_params.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            sorting.append(row)
    sorting = sorting[0]
    opt_index = 0
    for i in range(1, len(working)):
        result = []
        for j in range(len(sorting)):
            if sorting[j] == 'max':
                result.append('max')
                opt_index = j
                continue
            if '+' == working[0][j + 2][-2] and working[i][j + 2] >= sorting[j]:
                result.append('+')
                continue
            if working[0][j + 2][-2] == '-' and working[i][j + 2] <= sorting[j]:
                result.append('+')
                continue
            result.append('-')
            break
        if '-' not in result:
            output.append(working[i])
    print("\nСужение по субоптимизации (предварительная таблица):")
    printTable(output)
    max_index = 0
    max_value = -1
    for i in range(1, len(output)):
        if output[i][opt_index] > max_value:
            max_val = output[i][opt_index]
            max_index = i
    output_data = [working[0], output[max_index]]
    return output_data


def thirdSort(data):
    sorting = []
    working = data[:]
    output = []
    with open("third_params.csv") as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            for i in range(len(row)):
                row[i] = int(row[i])
            sorting.append(row)
    sorting = sorting[0]
    for i in range(len(working)):
        output.append([working[i][0], working[i][1]])
    for i in range(len(output)):
        for j in range(len(sorting)):
            output[i].append(working[i][sorting[j]+1])
    for i in range(2, len(working)+2):
        if len(output) == 1:
            break
        max_indexes = []
        all_indexes = []
        for j in range(1, len(output)):
            all_indexes.append(output[j][i])
        for j in range(1, len(output)):
            if output[j][i] == max(all_indexes):
                max_indexes.append(j)
        temp = output[:]
        output = [temp[0]]
        for j in range(1, len(temp)):
            if j in max_indexes:
                output.append(temp[j])
    return output


def allOutput():
    data = importData()
    print("Полная таблица вариантов:")
    printTable(data)
    parett_data = makeParett(data)
    print("\nПарето-оптимальная таблица вариантов:")
    printTable(parett_data)
    first_sorted = firstSort(parett_data)
    print("\nСужение по указанию верхних/нижних границ критериев:")
    printTable(first_sorted)
    second_sorted = secondSort(parett_data)
    print("\nСужение по субоптимизации:")
    printTable(second_sorted)
    third_sorted = thirdSort(parett_data)
    print("\nСужение по лексикографии:")
    printTable(third_sorted)


allOutput()
