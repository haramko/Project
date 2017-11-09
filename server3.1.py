import psycopg2
import urllib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import json
import datetime
import re

class LocalData(object):
        records= {}
class MyHandler(BaseHTTPRequestHandler):

    myID = 10
    device_id = 0

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

            #params = urllib.urlencode({'temperature':10})
            #self.wfile.write(params)
            if None != re.search('/device_id/', self.path):
                #self.deviceID = self.path.split('/')[-1]
                #if LocalData.records.has_key(deviceID):
                #print "Check:" + self.deviceID
                #self.wfile.write(LocalData.records[deviceID])
                #self.read_db(self.deviceID)

                try:
                    conn = psycopg2.connect("host='192.168.100.181' port='5432' dbname='sensor' user=postgres password='psql123'")
                    #conn.autocommit = True
                except psycopg2.DatabaseError as error:
                    print error
                    #print "cannot SQL Execute"
                    #print "not connect"
                cur=conn.cursor()
                try:
                    params = []
                    i=0
                    #print "deviceID IS " + self.deviceID
                    #cur.execute("SELECT * FROM Devices WHERE id=%s",(self.deviceID,))
                    #cur.execute("SELECT * FROM Devices WHERE DATE_FORMAT(date, '%Y-%m-%d') = ( SELECT DATE_FORMAT(MAX(date), '%Y-%m-%d') FROM Devices)
                    cur.execute("SELECT * FROM Devices WHERE id = (select MAX(id) from devices)")
                    rows = cur.fetchall()
                    print "rows:" + str(rows)
                    for row in rows:
                    #print data
                    params = json.dumps(data)
                    self.wfile.write(params)
                    #print params
                except psycopg2.DatabaseError as error:
                    print error
                    #print "cannot SQL Execute"

                conn.commit()
                cur.close()
                conn.close()


        except IOError:
            self.send_error(404, 'File Not Found')
        print "get end"

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        print "post start "
        self._set_headers()
        self.myID = self.myID + 1
        print "myID is"+ str(self.myID)
        if None != re.search('/session_number/*', self.path):
                self.device_id= self.path.split('/')[-1]
                #print self.device_id
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        print "in post action: " + data_string
        self.insert_db(data_string)


    def insert_db(self, data_x):
        try:

            conn = psycopg2.connect("host='192.168.100.181' port='5432' dbname='sensor' user=postgres password='psql123'")
            #conn.autocommit = True
            print 1
        except psycopg2.DatabaseError as error:
            print error

        now = datetime.datetime.now()
        temp_D = str(now.date())
        t = now.time()
        tt = str(t)
        temp_T = tt[0:8]
        cur=conn.cursor()
        print "data_x is" + data_x
        data_x = str(data_x)
        data_x1 = re.sub('[^0-9]','',data_x)
        print "data_x1 is" + data_x1
        #print self.myID
        #print type(self.myID)
        #print type(self.device_id)

        try:
            #sqlString = "INSERT INTO  Sessions (id,MeasurementTime,Nsamples, Data, device_id) VALUES (21,'03:04:52', 4,%s, 21);"
            #myID = 10
            cur.execute("INSERT INTO  sensorData(id, NSamples, Data, device_id, date, time) VALUES (%s, 4,%s, %s, %s, %s);", (self.myID, data_x1, self.device_id,temp_D,temp_T))
            #cur.execute("INSERT INTO  sensorData(id,measurementtime,nsamples,Data, device_id) VALUES (10,'03:03:03',4,'123424141', 1);")
            print 2

        except psycopg2.DatabaseError as error:
            print "inserDA : cannot SQL Execute"
            print error

        conn.commit()
        cur.close()
        conn.close()

    def read_db(self, device_id):
        try:
            conn = psycopg2.connect("host='192.168.100.181' port='5432' dbname='sensor' user=postgres password='psql123'")
        except psycopg2.DatabaseError as error:
            print error

        cur=conn.cursor()
        try:
            #print device_id
            # sqlString = "SELECT Device_Name FROM Devices WHERE id=%s"
            #sqlString = "SELECT Device_Name FROM Devices"
            cur.execute("SELECT Device_Name FROM Device_Profile WHERE device_id=%s",(device_id,))
            #rows1 = cur.fetchall()
            #for row1 in rows1:
            #x = row1[0]

            x = cur.fetchone()[0]
            #print x, type(x), repr(x)
            #print x
        except psycopg2.DatabaseError as error:
            #print "cannot SQL Execute"
            print error

        conn.commit()
        cur.close()
        conn.close()


def main():
        try:
                server = HTTPServer(("",30008), MyHandler)
                print 'Welcome to the machine'
                server.serve_forever()
        except KeyboardInterrupt:
                server.socket.close()

if __name__== '__main__':
        main()
