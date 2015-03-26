'''
Created on Feb 21, 2014

@author: brunj7
'''

class Digit_prod:
    '''
    Given a number N, find the smallest 3 digits number such that product of its digits is equal to N
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #list storing the 3 digits
        self.digit3 = []
        #list to handle the case the number is divided in 2 digits
        self.digit3_in_2 = []
        self.digit_range = range(2,10)
        self.digit_range2 = range(2,5)
        self.digit_range.sort(reverse =True)
        self.digit_range2.sort(reverse =True)

    def _is_toobig(self):
        if self.numb < 730:
            return True
        else:
            return False
        
    def _is_prime(self, num):
        '''check if number entered is prime'''
        if num > 2:
            #n = num / 2
            for i in range(2, 10):
                if ((float(num) % i) == 0.0):
                    return False
            return True
        else:
            return True
    
    def _divider(self,x):
        while not self._is_prime(x):
            for d in self.digit_range:
                if float(x) % d == 0:
                    x = x/d
                    self.digit3.append(d)
                    break
                        
    def _handle_2digits(self):            
        for d2 in self.digit3:
            if not self._is_prime(d2):
                for n in self.digit_range2:
                    if (d2 % n == 0) and (float(d2)/n > 1):
                        num = d2/n
                        self.digit3_in_2.append(num)
                        self.digit3_in_2.append(n)
                        break
            else:          
                self.digit3_in_2.append(d2)
                
        if len(self.digit3_in_2) == 3:
            self.digit3_in_2.sort()
            print "The 3 digits number for "+str(self.numb)+" is " + ''.join(map(str, self.digit3_in_2))
                
    def compute(self, number):
        self.numb = number
        if self._is_toobig():
            self._divider(number) 
            if len(self.digit3) == 3:
                self.digit3.sort()
                print "The 3 digits number for "+str(number)+" is " + ''.join(map(str, self.digit3))
            elif len(self.digit3) == 2:
                self._handle_2digits()
            else:
                print str(number)+" can not be expressed as a 3 digits product"
        else:
            print str(number)+" is too large (above 729) to be expressed as a 3 digits product"   
        self.__init__()
                
#===========================================================================================================

if __name__=='__main__':       
    p = Digit_prod()
    for n in range(2,500):
        #print n
        p.compute(n)
    
