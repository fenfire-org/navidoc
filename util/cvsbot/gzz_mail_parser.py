

class GZZMailParser:
    """Methods for parsing and formatting the (email) message."""
    data = ""
    fileChanges = {}

    class NoCommitterError: pass
    
    def __init__(self, data):
        self.data = data

    def getField(self, field):
        """New method to extract from the message rest of a line that starts
           with field."""
        data = self.data
        field = '\n'+field
        begin = data.find(field)+len(field)
        if begin != -1:
            end = data.find('\n', begin)
            return data[begin:end].lstrip()
 
    def getProject(self):
        """Called by MsgListener.doCommitMessage to find out the scope of
           files."""
        return self.getField('Module name:')
    
    def getCVSROOT(self, string = 'CVSROOT:'):
        data = self.data
        begin = data.rfind(string)
        if begin != -1:
            end = data[begin:].find('\n') + begin
            return data[begin:end].split()[1][9:]

    def getReceivedFrom(self, string = 'Received: from'):
        data = self.data
        begin = data.rfind(string)
        if begin != -1:
            end = data[begin:].find('\n') + begin
            return data[begin:end].split()[2]

    def getAddedFiles(self, string = 'Added files'):
        path = ''
        data = self.data
        addedFiles = []
        begin = data.find(string)
        flag = False
        if begin != -1:
            for l in data[begin:].split('\n'):
                if l == '': break
                if l.find('Removed files') != -1: break # XXX: hmm

                if flag:
                    x = l.split(':')
                    if len(x) == 2:
                        path, file = x[0], x[1]
                    else:
                        file = x[0]
                    for l in file.split():
                        self.fileChanges.setdefault(path.strip(), []).append('+' + l)
                flag = True

    def getModifiedFiles(self, string = 'Modified files'):
        path =''
        data = self.data
        modifiedFiles = []
        begin = data.find(string)
        flag = False
        if begin != -1:
            for l in data[begin:].split('\n'):
                if l == '': break
                if l.find('Added files') != -1: break   # XXX: hmm
                if l.find('Removed files') != -1: break # XXX: hmm
                
                if flag:
                    x = l.split(':')
                    if len(x) == 2:
                        path, file = x[0], x[1]
                    else:
                        file = x[0]
                    for l in file.split():
                        self.fileChanges.setdefault(path.strip(), []).append(l)
                flag = True

    
    def getCommitMessage(self, string = 'Log message'):
        data = self.data
        flag = False
        logMessage = []
        begin = data.find(string)
        if begin == -1: begin = data.find('Log Message') # XXX: hmm
        if begin != -1:
            for l in data[begin:].split('\n'):
                if l == '': break
                if flag:
                    logMessage.append(l.strip())
                flag = True
        return ' '.join(logMessage)

    def getRemovedFiles(self, string = 'Removed files'):
        path = ''
        data = self.data
        flag = False
        removedFiles = []
        begin = data.find(string)
        
        if begin != -1:
            for l in data[begin:].split('\n'):
                if l == '': break
                if l.find('Added files') != -1: break   # XXX: hmm
                if l.find('Modified files') != -1: break # XXX: hmm
                
                if flag:
                    x = l.split(':')
                    if len(x) == 2:
                        path, file = x[0], x[1]
                    else:
                        file = x[0]
                    for l in file.split():
                        self.fileChanges.setdefault(path.strip(), []).append('-' + l)
                flag = True

    def formatMessage(self, by = '', msg = '', project = ''):
        """Returns a formatted string for feeding to
        IRC. Returns <%submitter> "%string" (%files)
        by default."""
        
        MAXLENGTH = 350
        if not by: raise self.NoCommitterError()
        
        d = self.fileChanges    
        files = []
        x = d.keys()
        x.sort()
        
        if '.' in x: 
            files.append(', '.join(d['.']))
            del x[0]
            
        for dire in x:
            files.append('%s: %s' % (dire, ', '.join(d[dire])))

        flag = False
        while len('; '.join(files)) > MAXLENGTH:
            files.pop()
            flag = True
        if flag: files.append('...')
            
        files = '(%s)' % '; '.join(files)
        if files == '()' : files = ''
        
        maxl = MAXLENGTH / 2
        if len(msg) > maxl: msg = msg[:maxl-3] + '...'

        self.fileChanges.clear()
        return '%s: <%s> "%s" %s' % (project, by, msg, files)
