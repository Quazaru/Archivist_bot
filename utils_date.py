import datetime
class DateHelper:
    userTimeStr_template = "{hrs}:{mins}:{secs} {dd}\\{mm}\\{yy}"
    datetimeTimeStr_template = "%H:%M:%S %d\\%m\\%Y"
    def _parseTimeStr(timeStr) -> datetime:
        convertedTime = datetime.datetime.strptime(timeStr, DateHelper.datetimeTimeStr_template)
        return convertedTime
    

    def getTimestamp() -> float:
        return datetime.datetime.now().timestamp()
    def getStr(timestamp=None) -> str:
        if timestamp:
            currentTime = datetime.datetime.fromtimestamp(timestamp).strftime(DateHelper.datetimeTimeStr_template)
        else:
            currentTime = datetime.datetime.now().strftime(DateHelper.datetimeTimeStr_template)
        return currentTime
    
    def compare(toCompareTimeStr, withCompareTimeStr):
        """
        args:
        two string in format "{hrs}:{mins}:{secs} {dd}/{mm}/{yy}"
        - toCompareTimeStr - time that is being compared 
        - withCompareTimeStr - time to compare with
        _____________
        return:
        - (int):  1 if toCompareTimeStr > withCompareTimeStr
        - (int):  0 if toCompareTimeStr == withCompareTimeStr
        - (int): -1 if toCompareTimeStr < withCompareTimeStr
        """
        isEqual = DateHelper._parseTimeStr(toCompareTimeStr) == DateHelper._parseTimeStr(withCompareTimeStr)
        compareResult = DateHelper._parseTimeStr(toCompareTimeStr) > DateHelper._parseTimeStr(withCompareTimeStr)
        if isEqual: return 0
        if compareResult: return 1
        return -1

