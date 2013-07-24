
class Time(object):
    
    mMinutes = 0
    mSeconds = 0
    mMilliseconds = 0
    
    def __init__(self, timestring):
        self.mMinutes, self.mSeconds, self.mMilliseconds = timestring.split(":")
        
    """
    Return true if othertime is better(lower) than self
    """
    def compareTimes(self, othertime):
        mtime1 = int(int(self.minutes) * 60000 + int(self.seconds) * 1000 + float(self.milliseconds))
        mtime2 = int(int(othertime.minutes) * 60000 + int(othertime.seconds) * 1000 + float(othertime.milliseconds))
        
        if mtime2 == 0: return False
        return True if mtime2 <= mtime1 else False
        
    def toString(self):
        return "%s:%s:%s" % (self.minutes, self.seconds, self.milliseconds)
    
    def __minutes(self):
        return self.mMinutes
    
    def __seconds(self):
        return self.mSeconds
    
    def __milliseconds(self):
        return self.mMilliseconds
    
    minutes = property(__minutes, None)
    seconds = property(__seconds, None)
    milliseconds = property(__milliseconds, None)
    