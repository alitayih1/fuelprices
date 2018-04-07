#we have fuel prices in chile (dummy prices) as json file 
#so we need to insert this file into database and i chose Sqlite3 database 
#note : the content of json file included at the end of this script as comment   
#as will as table script that you need to create on database

import json
import sqlite3
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'

conn = sqlite3.connect(r'GasPrices.db');



class GasPrices():
    def __init__(self, json_dict, type_of_gas, normal = True):
        self.normal_higher = "normal" if normal else "higher"
        self.type_of_gas = type_of_gas
        self.tax_co2 = json_dict[type_of_gas][self.normal_higher]["tax_co2"]
        self.tax = json_dict[type_of_gas][self.normal_higher]["tax"]
        self.charge = json_dict[type_of_gas][self.normal_higher]["charge"]
        self.updated = json_dict[type_of_gas][self.normal_higher]["updated"]
        self.excise_duty = json_dict[type_of_gas][self.normal_higher]["excise_duty"]
        self.price = json_dict[type_of_gas][self.normal_higher]["price"]
        self.price_neto = json_dict[type_of_gas][self.normal_higher]["price_neto"]
        

class Country():
    def __init__(self, country, json_dict):
        self.jsonDict = json_dict[country]
        self.country = country
        self.currency = self.jsonDict["currency"]
        self.gas_100 = GasPrices(self.jsonDict, "100")
        self.gas_95 = GasPrices(self.jsonDict, "95")
        self.diesel = GasPrices(self.jsonDict, "diesel")
        self.fl = GasPrices(self.jsonDict, "fl")
        
        

    def __repr__(self):
        print("price of Diesel: ", self.diesel.price)
        print("price for 100: ", self.gas_100.price)
        print("price for 95: ", self.gas_95.price)
        print("price for fl: ", self.fl.price)
        return(self.country)
        
    def create_table():

        
     conn.execute('''CREATE TABLE `GasPrice` (
 	`_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
 	`country`	TEXT NOT NULL,
 	`currency`	TEXT NOT NULL,
 	`gas_type`	TEXT NOT NULL,
 	`normal`	INTEGER NOT NULL DEFAULT 1,
 	`price`	REAL,
 	`price_neto`	REAL,
 	`charge`	REAL,
 	`excise_duty`	REAL,
 	`tax`	REAL,
 	`tax_co2`	INTEGER,
 	`updated`	TEXT
 );''')
     




    def save_to_database(self):
        
     con = sqlite3.connect(r"GasPrices.db") 
     
     with con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row


            # check if entry is updated!
            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?", (self.country, self.diesel.type_of_gas))
            should_update_diesel = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_diesel = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_diesel = True
                i += 1

            # diesel
            if (should_update_diesel):
                cur.execute("INSERT INTO GasPrice"
                        "("
                        "country,"
                        "currency,"
                        "gas_type,"
                        "normal,"
                        "price,"
                        "price_neto,"
                        "charge,"
                        "excise_duty,"
                        "tax,"
                        "tax_co2,"
                        "updated"
                        ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    self.country,
                    self.currency,
                    self.diesel.type_of_gas,
                    1,
                    self.diesel.price,
                    self.diesel.price_neto,
                    self.diesel.charge,
                    self.diesel.excise_duty,
                    self.diesel.tax,
                    self.diesel.tax_co2,
                    self.diesel.updated
                )
            )

            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?", (self.country, self.gas_100.type_of_gas))
            should_update_gas_100 = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_gas_100 = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_gas_100 = True
                i += 1
            if (should_update_gas_100):
                # 100
                cur.execute("INSERT INTO GasPrice"
                            "("
                            "country,"
                            "currency,"
                            "gas_type,"
                            "normal,"
                            "price,"
                            "price_neto,"
                            "charge,"
                            "excise_duty,"
                            "tax,"
                            "tax_co2,"
                            "updated"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        self.country,
                        self.currency,
                        self.gas_100.type_of_gas,
                        1,
                        self.gas_100.price,
                        self.gas_100.price_neto,
                        self.gas_100.charge,
                        self.gas_100.excise_duty,
                        self.gas_100.tax,
                        self.gas_100.tax_co2,
                        self.gas_100.updated
                    )
                )


            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?", (self.country, self.gas_95.type_of_gas))
            should_update_gas_95 = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_gas_95 = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_gas_95 = True
                i += 1
            # 95

            if (should_update_gas_95):
                cur.execute("INSERT INTO GasPrice"
                        "("
                        "country,"
                        "currency,"
                        "gas_type,"
                        "normal,"
                        "price,"
                        "price_neto,"
                        "charge,"
                        "excise_duty,"
                        "tax,"
                        "tax_co2,"
                        "updated"
                        ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (
                    self.country,
                    self.currency,
                    self.gas_95.type_of_gas,
                    1,
                    self.gas_95.price,
                    self.gas_95.price_neto,
                    self.gas_95.charge,
                    self.gas_95.excise_duty,
                    self.gas_95.tax,
                    self.gas_95.tax_co2,
                    self.gas_95.updated
                )
            )


            cur.execute("SELECT updated FROM GasPrice WHERE country=? AND gas_type=?", (self.country, self.fl.type_of_gas))
            should_update_fl = False
            i = 0
            while True:
                row = cur.fetchone()
                if (row == None):
                    if (i == 0):
                        should_update_fl = True
                    break
                if (datetime.strptime(row[0], DATE_FORMAT) < datetime.strptime(self.diesel.updated, DATE_FORMAT)):
                    should_update_fl = True
                i += 1
            if (should_update_fl):
                # fuel oil fl
                cur.execute("INSERT INTO GasPrice"
                            "("
                            "country,"
                            "currency,"
                            "gas_type,"
                            "normal,"
                            "price,"
                            "price_neto,"
                            "charge,"
                            "excise_duty,"
                            "tax,"
                            "tax_co2,"
                            "updated"
                            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        self.country,
                        self.currency,
                        self.fl.type_of_gas,
                        1,
                        self.fl.price,
                        self.fl.price_neto,
                        self.fl.charge,
                        self.fl.excise_duty,
                        self.fl.tax,
                        self.fl.tax_co2,
                        self.fl.updated
                    )
                )
                    


    conn.commit()
    conn.close()



    def open_connection(self):
        return sqlite3.connect("GasPrices.db")


response = open(r'C:\Users\Usuario\.spyder-py3\fuel_prices.json')
a = str(response.read())
#a = a[2:len(a)-1]
# print(a)
b = json.loads(a) # decode JSON format

#save it into database
prices_in_slo = Country("Chile", b)
prices_in_slo.save_to_database()

#{
#    "Chile": {
#        "95": {
#            "normal": {
#                "price": "793.2",
#                "price_neto": "500.1",
#                "charge": "100.2",
#                "excise_duty": "40.99",
#                "tax": "116.000",
#                "tax_co2": "60.9",
#                "updated": "2018-04-02"
#            }
#        },
#        "100": {
#            "normal": {
#                "price": "905",
#                "price_neto": "600.1",
#                "charge": "200.2",
#                "excise_duty": "60.99",
#                "tax": "120.000",
#                "tax_co2": "70.9",
#                "updated": "2018-04-02"
#            }
#        },
#        "currency": "Chilean Peso",
#        "diesel": {
#            "normal": {
#                "price": "534.60",
#                "price_neto": "400.1",
#                "charge": "100.2",
#                "excise_duty": "30.99",
#                "tax": "110.000",
#                "tax_co2": "50.9",
#                "updated": "2018-04-02"
#            }
#        },
#        "lpg": {
#            "normal": {
#                "price": "450.4",
#                "price_neto": "200.1",
#                "charge": "50.2",
#                "excise_duty": "10.99",
#                "tax": "100.000",
#                "tax_co2": "50.9",
#                "updated": "2018-04-02"
#            }
#        },
#        "fl": {
#            "normal": {
#                "price": "50.1",
#                "price_neto": "30.1",
#                "charge": "10.2",
#                "excise_duty": "5.99",
#                "tax": "9.000",
#                "tax_co2": "1.9",
#                "updated": "2018-04-02"
#            }
#        }
#    }
#}

#########################################################################

#CREATE TABLE GasPrice (
#    _id         INTEGER NOT NULL
#                        PRIMARY KEY AUTOINCREMENT
#                        UNIQUE,
#    country     TEXT    NOT NULL,
#    currency    TEXT    NOT NULL,
#    gas_type    TEXT    NOT NULL,
#    normal      INTEGER NOT NULL
#                        DEFAULT 1,
#    price       REAL,
#    price_neto  REAL,
#    charge      REAL,
#    excise_duty REAL,
#    tax         REAL,
#    tax_co2     INTEGER,
#    updated     TEXT
#);