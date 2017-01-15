#!/usr/bin/env python2.7
import os, sys, argparse as ap, operator

p = ap.ArgumentParser(description=('Read [file].  Return all unique occurrences in [PRIMARY], where [INDEX] is the most recent occurrence for [PRIMARY].'))
p.add_argument("-f", "--file", help="The csv file for input", type=str)
p.add_argument("-p", "--primary", help=("Primary \"key\" column, by field number, in which to base output. Ex: Clients"), type=int)
p.add_argument("-s", "--secondary", help=("Secondary \"key\" column (optional), by field number, in which to base output. Ex: Notified (T/c versus noto"), type=int, default=-1)
p.add_argument("-i", "--index", help=("Sequence index column, by field number. Ex: Timestamps or ticket numbers"), type=int)
p.add_argument("-I", "--ignore", help="Ignore first line (column headers)", action="store_true")
p.add_argument("-o", "--output", help="Output results to file. Will be output with '-output' added to basename of file.", action="store_true")
a = p.parse_args()

class shuffle():
    def __init__(self):
        ### Most important interface from outside would be self.post, which is the final product.  Might want to send that object to printer.
        self.file=a.file
        self.primary=a.primary-1
        self.secondary=a.secondary-1 if not a.secondary == -1 else -1
        self.index=a.index-1
        self.pre=[]
        self.unique_keys=[]
        self.unique_secondaries=[]
        self.unique_indexes=[]
        self.post=[]
        self.skip=[]
        self.ignore=1 if a.ignore == True else 0
        self.output=1 if a.output == True else 0
        self.col_headers=[]
        self.newfilename=self.file.rstrip(".csv") + "-output.csv"
        with open(self.file) as f:
            self.pre = f.readlines()
            f.close()
            if self.ignore == 1:
                self.col_headers=self.pre.pop(0)
            self.pre = sorted(self.pre, key=operator.itemgetter(self.index), reverse=True)
        for item in self.pre:
            if item.split(',')[self.primary].replace(' ', '') not in self.unique_keys:
                self.unique_keys.append( item.split(',')[self.primary].replace(' ', ''))
        if self.secondary != -1:
            for item in self.pre:
                if item.split(',')[self.index].replace(' ', '') not in self.unique_indexes:
                    self.unique_indexes.append(item.split(',')[self.index].replace(' ', ''))
        for item in self.pre:
            if item.split(',')[self.secondary].replace(' ', '') not in self.unique_secondaries:
                self.unique_secondaries.append(item.split(',')[self.secondary].replace(' ', ''))
        self.unique_keys.sort()
        if self.secondary == -1:
            for item in self.unique_keys:
                for meti in self.pre:
                    if item in meti.split(',')[self.primary].replace(' ', '') and item not in self.skip:
                        self.skip.append(item)
                        self.post.append(meti)
        else:
            for item in self.unique_keys:
                for timmeh in self.unique_secondaries:
                    for meti in self.pre:
                        temp=str(meti).split(",")
                        if item in temp[self.primary].replace(' ', '') and timmeh in temp[self.secondary].replace(' ', '') and item+timmeh not in self.skip:
                            self.skip.append(item+timmeh)
                            self.post.append(meti)


    def headercount(self):
        count = 1
        this = self.col_headers.split(',')
        that = ""
        for item in this:
            that = that + ", (" + str(count) + ")" + item
            count += 1
        that = that.lstrip(', ')
        print ("Col Headers:\n\t" + that)

    def debug(self, obj):
        if self.secondary == -1:
            print("Samples:\n\tPrimary:\t(" + str(self.primary +1) + ")" + str(obj[len(obj) - 1].split(",")[self.primary].strip('"').strip("'"))
                  + "\n\tIndex:\t\t(" + str(self.index +1) + ")" + str(obj[len(obj) - 1].split(",")[self.index]).strip('"').strip("'"))
        else:
            print("Samples:\n\tPrimary:\t(" + str(self.primary +1) + ")" + str(obj[len(obj) - 1].split(",")[self.primary].strip('"').strip("'"))
                  + "\n\tSecondary:\t(" + str(self.secondary +1) + ")" + str(obj[len(obj) - 1].split(",")[self.secondary].strip('"').strip("'"))
                  + "\n\tIndex:\t\t(" + str(self.index +1) + ")" + str(obj[len(obj) - 1].split(",")[self.index]).strip('"').strip("'"))

    def printer(self, obj):
        for item in obj:
            print(item)

    def printer2(self, obj, strng):
        print(str(strng+":").ljust(24) + str(len(obj)).ljust(20))

    def writer(self, obj):
        userin="0"
        while userin != "1" and userin != "2":
            userin=raw_input("[?] Write post-op output to file?\n\t[1] Yes\n\t[2] No\n[!]: ")
        if userin == "1":
            obj.insert(0, self.col_headers)
            with open(self.newfilename, "w") as nfn:
                for item in obj:
                    nfn.write(item)
            nfn.close()
            print("[!] Output written to " + self.newfilename + "\n")


if __name__=="__main__":
    this=shuffle()
    this.printer(this.post)
    this.printer2(this.pre, "Pre-op")
    this.printer2(this.unique_keys, "Uniuqe primaries")
    this.printer2(this.unique_secondaries, "Unique secondaries")
    this.printer2(this.unique_indexes, "Unique indexes")
    this.printer2(this.post, "Post-op")
    this.debug(this.post)
    if this.ignore == 1:
        this.headercount()
    if this.output == 1:
        this.writer(this.post)


