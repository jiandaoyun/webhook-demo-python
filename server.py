#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import hashlib
import threading
import json
from flask import Flask, request
import pymysql
from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql, 5, host='localhost', user='root', passwd='123456', db='webhook', port=3306, charset='utf8')

app = Flask(__name__)

def handle (payload):
    if payload['op'] == 'data_create':
        return add(payload['data'])
    if payload['op'] == 'data_update':
        return update(payload['data'])
    if payload['op'] == 'data_remove':
        return remove(payload['data'])

def add(data):
    oid = data['_id']
    time = data['_widget_1515649885212']
    types = data['_widget_1516945244833']
    address = data['_widget_1516945244846']
    order_items = data['_widget_1516945244887']
    price = data['_widget_1516945245257']
    conn = pool.connection()
    cursor = conn.cursor()
    sql = 'insert into `order` values ("%s", "%s", "%s", "%s", "%s", "%f")' % \
          (oid, time, types, address, order_items, price)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    cursor.close()
    conn.close()

def update(data):
    oid = data['_id']
    time = data['_widget_1515649885212']
    types = data['_widget_1516945244833']
    address = data['_widget_1516945244846']
    order_items = data['_widget_1516945244887']
    price = data['_widget_1516945245257']
    conn = pool.connection()
    cursor = conn.cursor()
    sql = 'update `order` set time = "%s", types = "%s", address = "%s", orderItems = "%s", price = "%f" where id = "%s"' % \
          (time, types, address, order_items, price, oid)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    cursor.close()
    conn.close()

def remove(data):
    oid = data['_id']
    conn = pool.connection()
    cursor = conn.cursor()
    sql = 'delete from `order` where id = "%s"' % (oid)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    cursor.close()
    conn.close()

def get_signature(nonce, payload, secret, timestamp):
    content = ':'.join([nonce, payload, secret, timestamp]).encode('utf-8')
    m = hashlib.sha1()
    m.update(content)
    return m.hexdigest()

@app.route('/callback', methods=['POST'])
def callback():
    payload = request.data.decode('utf-8')
    nonce = request.args['nonce']
    timestamp = request.args['timestamp']
    if request.headers['x-jdy-signature'] != get_signature(nonce, payload, 'test-secret', timestamp):
        return 'fail', 401
    threading.Thread(target=handle, args=(json.loads(payload), )).start()
    return 'success'

if __name__ == "__main__":
    app.run(port=3100)
