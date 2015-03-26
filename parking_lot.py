'''
Created on March 14, 2014

Design a parking lot system where you need to provide a token with the parking space number on it to each new entry for the space closest to the entrance. 
When someone leave you need update this space as empty. 
What data structures will you use to perform the closest empty space tracking, plus finding what all space a occupied at a give time.

@author: JBrun
'''


import random
from collections import Counter

#Possible parking state
free_spot = 'free'
taken_lot = 'occupied'

class Parking:
    '''This class simulate a parking lot where cars come in and out'''
    
    def __init__(self,size=10):
        '''initialize an empty parking'''
        self.parking_size = size
        self.parking_storage = {}
        token_list = range (1,size+1)
        #init parking
        for t in token_list:
            self.parking_storage[t] = free_spot

    def status_check(self):
        '''Check status of the parking'''
        c = Counter(self.parking_storage.values())
        print "There are " + str(int(c.get(free_spot) or 0)) + " parking spaces available"
        print
        print self.parking_storage
    
    def insert_car(self, nb_car_in):
        '''Insert car in the parking'''
        c = Counter(self.parking_storage.values())
        empty_spot = int(c.get(free_spot) or 0)
        if nb_car_in > empty_spot:
            delta = nb_car_in - empty_spot
            print "only "+str(empty_spot)+ " parking spaces are available. "+ str(delta) + " cars can not enter"
            nb_car_in = empty_spot            
        for t,o in self.parking_storage.iteritems():
            if o == 'free':
                self.parking_storage[t] = taken_lot
                nb_car_in = nb_car_in -1
            if nb_car_in < 1:
                break
    
    def remove_car(self, nb_car_out):
        '''Remove car from the parking'''
        c = Counter(self.parking_storage.values())
        occupied_spot = int(c.get(taken_lot) or 0)
        if nb_car_out > occupied_spot:
            #delta = nb_car_out-self.occupied_spot
            print "only "+ str(occupied_spot) + " cars are in the parking. They all be removed"
            nb_car_out = occupied_spot
            
        tkl = random.sample(range(1,self.parking_size+1), self.parking_size)
        for tk in tkl:
            if self.parking_storage[tk] == taken_lot:
                self.parking_storage[tk] = free_spot
                nb_car_out = nb_car_out -1
            if nb_car_out < 1:
                break
