# (c): Matti J. Katila

import sys, string, os

def printUsage():
    print  """
This is a small application for adding cvs ignores.

Usage (for example):

    foo% cvs up -dP | python ../navidoc/util/cvsignores.py
    """

class CVSIgnores:
    def __init__(self, firstLine):
        lines = sys.stdin.readlines()
        lines.append(firstLine)

        self.removeDirty(lines)
        list = self.separateFileAndPath(lines)
        for l in lines: print l

        self.addIgnoreFiles(list)


    def removeDirty(self, list):
        i = 0
        while i<len(list):
            if list[i][0] != '?':
                list.pop(i)
            else:
                list[i] = list[i][2:-1]
                i += 1

    def separateFileAndPath(self, list):
        for i in range(len(list)):
            l = list[i]
            ind = string.rfind(l, '/')
            if ind == -1:
                list[i] = [ '', l ]
            else:
                ind += 1
                list[i] = [ l[0:ind], l[ind:] ]
        return list

    def addIgnoreFiles(self, list):
        print os.getcwd()
        for l in list:
            f = open(l[0]+'.cvsignore', 'a+')
            f.readlines()
            f.write(l[1] + '\n')
            f.close()

        for l in list:
            f = open(l[0]+'.cvsignore')
            print f.readlines()


if __name__ == '__main__':
    first = sys.stdin.readline() 
    if len(first) < 2:
        printUsage()
    else:
        CVSIgnores(first)

    
