class Time(object):
    
    mMinutes = 0
    mSeconds = 0
    mMilliseconds = 0
    
    def __init__(self, timestring):
        self.mMinutes, self.mSeconds, self.mMilliseconds = timestring.split(":")
        
    """
    Return true if this is better(lower) than other
    """
    def isFaster(self, othertime):
        this = int(int(self.minutes) * 60000 + int(self.seconds) * 1000 + float(self.milliseconds))
        other= int(int(othertime.minutes) * 60000 + int(othertime.seconds) * 1000 + float(othertime.milliseconds))
        
        if this == 0: return False
        if other == 0: return True
        return True if this <= other else False
        
    def toString(self):
        return "%s:%s:%s" % (self.minutes, self.seconds, self.milliseconds)
    
    def __minutes(self):
        return self.mMinutes
    
    def __seconds(self):
        return self.mSeconds
    
    def __milliseconds(self):
        return self.mMilliseconds
    
    @staticmethod
    def convertToTimeFormat(floattime):     
        m, s = divmod(floattime, 60)
        s, mi = str(s).split(".")
        
        m = str(int(m))
        if len(str(m)) == 1: m = "0" + m
        if len(s) == 1: s = "0" + s
        if len(mi) > 2: mi = mi[:2]
        if len(mi) == 1: mi = mi + "0"
        return Time("%s:%s:%s" % (m, s, mi))
    
    @staticmethod
    def convertToTimeString(floattime):
        m, s = divmod(floattime, 60)
        s, mi = str(s).split(".")
        
        m = str(int(m))
        if len(str(m)) == 1: m = "0" + m
        if len(s) == 1: s = "0" + s
        if len(mi) > 2: mi = mi[:2]
        if len(mi) == 1: mi = mi + "0"
        
        return "%s:%s.%s" % (m, s, mi)
    
    minutes = property(__minutes, None)
    seconds = property(__seconds, None)
    milliseconds = property(__milliseconds, None)
    