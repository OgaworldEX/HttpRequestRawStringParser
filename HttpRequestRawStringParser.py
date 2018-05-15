class HttpRequestRawStringParser:

    delimiter = '\r\n'
    requestRawString = ''
    requestLine = ''

    def __init__(self, requestRawString,delimiter='\r\n'):
        self.requestRawString = requestRawString
        self.delimiter = delimiter
        self.requestLine = self.getRequestLine()

    def getRequestLine(self):
        index = self.requestRawString.find(self.delimiter)
        self.requestLine = self.requestRawString[0:index]
        return self.requestLine

    def getRequestMethod(self):
        index = self.requestLine.find(' ')
        return self.requestLine[0:index]

    def getRequestPath(self):
        findex = self.requestLine.find(' ')
        bindex = self.requestLine.rfind(' ')
        return self.requestLine[findex + 1:bindex]

    def getRequestHttpVersion(self):
        index = self.requestLine.rfind(' ')
        return self.requestLine[index + 1:len(self.requestLine)]

    def getHeadderArray(self):
        index = self.requestRawString.find(self.delimiter + self.delimiter)
        headders = self.requestRawString[0:index].split(self.delimiter)
        del headders[0]
        return headders

    def getRequestBodyString(self):
        index = self.requestRawString.rfind(self.delimiter + self.delimiter)
        return self.requestRawString[index+2:len(self.requestRawString)]

    def getUrlParamString(self):
        return self.requestLine.split(' ')[1]

    def getUrlParamDic(self):
        requestPath = self.getUrlParamString()
        index = requestPath.rfind('?')
        param = requestPath[index + 1:len(requestPath)]

        ret = {}
        for keyValue in param.split('&'):
            tmp = keyValue.split('=')
            if len(tmp) > 1:
                ret[tmp[0]] = tmp[1]

        return ret

    def getHeadderDic(self):
        headders = self.getHeadderArray()
        ret = {}
        for headder in headders:
            tmp = headder.split(': ')
            if len(tmp) > 1:
                ret[tmp[0]] = tmp[1]

        return ret

    def getCookieDic(self):
        headderDic = self.getHeadderDic()

        for key in headderDic.keys():
            if key.lower() == 'cookie':
                cookiekey = key
                break;

        cookieLine =headderDic[cookiekey]
        cookieArray = cookieLine.split(';')

        ret = {}
        for cookie in cookieArray:
            cookie.strip()
            tmp = cookie.split('=')
            if len(tmp) > 1:
                ret[tmp[0]] = tmp[1]

        return ret

    def getBodyParamDic(self):
        bodyString = self.getRequestBodyString()

        ret = {}
        for keyValue in bodyString.split('&'):
            tmp = keyValue.split('=')
            if len(tmp) > 1:
                ret[tmp[0]] = tmp[1]

        return ret


if __name__ == "__main__":

    testString = """POST /spam/eggs/?key1=value1&key2=value2 HTTP/1.1
Host: 127.0.0.1
User-Agent: Mojilla/5.0 (Winbows NT 1.1; WOW128; rv:45.0) Geko/ FireRaccoon/1.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ja,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1:8000/spam/
Cookie: csrftoken=fjaewiaurfjweal; eggssessionid=78gu8ghrejkhgr843vsihrs
Connection: close
Content-Length: 26

key3=value3&key4=value4"""

    hrsp = HttpRequestRawStringParser(testString ,'\n')
    print('-Result-')
    print('getRequestLine(): ' + hrsp.getRequestLine())
    print('-')
    print('getRequestMethod(): ' + hrsp.getRequestMethod())
    print('getRequestPath(): ' + hrsp.getRequestPath())
    print('getRequestHttpVersion(): ' + hrsp.getRequestHttpVersion())
    print('-')
    print('getUrlParamString(): ' + hrsp.getUrlParamString())
    print('getUrlParamDic(): ' + str(hrsp.getUrlParamDic()))
    print('getHeadderArray(): ' + str(hrsp.getHeadderArray()))
    print('getHeadderDic(): ' + str(hrsp.getHeadderDic()))
    print('hrsp.getCookieDic(): ' + str(hrsp.getCookieDic()))
    print('getRequestBodyString(): ' + hrsp.getRequestBodyString())
    print('getBodyParamDic(): ' + str(hrsp.getBodyParamDic()))
    print('-')
