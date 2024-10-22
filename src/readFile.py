# importing libraries
import numpy as np

def readFile(raw_file_path): 
    # function for loading all events in one file as Event class.
    # returns array of Event classes

    with open(raw_file_path, 'rb') as f:
        hexdata = f.read().hex()    # opening the file as hex code

    SAMPLE_LENGTH_CONST = 434    # constant length of one data sample (in hex letters)

    first_header=-1     # -1 while the index could possibly be on position 0
    checkedByte=0           # the iterated variable in the cycle below
    while first_header==-1:     # = while the first header not found
        if hexdata[checkedByte:checkedByte+4] == 'fff0':     # searching first header in the file
            first_header = checkedByte                      # saving the found position if lucky
        checkedByte += 1       # adding 1 to continue the search for header
    
    # number of events in file, that are not divided
    n_events = int((len(hexdata) - first_header - ((len(hexdata)-first_header)%SAMPLE_LENGTH_CONST)) / SAMPLE_LENGTH_CONST)
    # filling new list with Event classes
    events = []
    for i in range(n_events):
        events.append(Event(hexdata, first_header+SAMPLE_LENGTH_CONST*i))
    
    # final print out
    print(f"File {raw_file_path} read.")

    return events

class Event:
    # class for parsing one event in file

    def __init__(self, data, start_byte):
        """
        Initialization. The hex data (str) and the start byte (int) needed.
        """
        self.position = start_byte      # saving the position to object for better access from outside
        self.parse_from_binary(data)    # calling the parsing function - to be clearer
    
    def parse_from_binary(self, data):

        # check header - 2 bytes
        if data[self.position:self.position+4] != 'fff0':
            print('Error: Can not create event, header not found')      # the position is probably wrong
        
        # detector code
        self.detector = int(data[self.position-2:self.position], 16)    # on byte (=> two letters) before the header

        # header1 - 2 bytes
        self.h1 = int(data[self.position+4:self.position+8], 16)

        # number of samples - 2 bytes
        self.length = int(data[self.position+8:self.position+12], 16)
        
        # now parse data
        self.samples = []   # preparing array
        for i in range(self.length):
            self.samples.append(int(data[4*i + self.position + 12 : 4*i + self.position + 16], 16))     # leaps over 4 letters = 2 bytes
        self.samples = np.array(self.samples)      # for better manipulation

        # times
        self.t1 = int(data[self.position + 4*self.length + 12 : self.position + 4*self.length + 16], 16)    # see the event structure
        self.t2 = int(data[self.position + 4*self.length + 16 : self.position + 4*self.length + 20], 16)    # I wasn't fixing 100 as default samples length
        self.t3 = int(data[self.position + 4*self.length + 20 : self.position + 4*self.length + 24], 16)

        # lost events & checksum
        self.lost_events = int(data[self.position + 4*self.length + 24 : self.position + 4*self.length + 28], 16)
        self.checksum = int(data[self.position + 4*self.length + 28 : self.position + 4*self.length + 32], 16)
        
        # check the next event header (the two bytes before are the detector number)
        if data[self.position + 4*self.length + 34 : self.position + 4*self.length + 38]!='fff0':
            print(f"Warning: the next event not found (instead: {data[self.position + 4*self.length + 34 : self.position + 4*self.length + 38]})")

if __name__ == '__main__':
    # example, not runned if imported (__name__ != '__main__')
    readFile("./Programming/Projects/S3Python/data/data_2024-01-04_11_12_09_658.raw")