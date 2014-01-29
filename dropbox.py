# encoding: utf-8

"""
Dropbox からファイルのダウンロード、アップロードを行うスクリプト
"""

__author__  = 'mystblue'
__version__ = '0.1'
__date__    = '2014/01/29'

import urllib, urllib2
import cookielib
import re

import mimetypes
import os.path
import random
import sys

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
urllib2.install_opener(opener)

# ログインしてクッキーを取得
req = urllib2.Request('https://www.dropbox.com/login')
req.add_header("User-agent", 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36')
cookie = urllib2.urlopen(req).read()
#print cookie

pattern = re.compile('input type="hidden" name="t" value="([^"]+)"')
security_key = ''
match = pattern.search(cookie)
if match:
    security_key = match.group(1)
else:
    print "no match"

# クッキーをセットしてリクエスト送信
req = urllib2.Request('https://www.dropbox.com/login')
req.add_header('t', security_key)
#req.add_header('login_email', 'mysterious.blue.star@gmail.com')
#req.add_header('login_password', 'dirdarot')
#req.add_header('lhs_type', 'anywhere')
req.add_header("User-agent", 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36')
param = {'t':security_key, 'login_email':'mysterious.blue.star@gmail.com', 'login_password':'dirdarot'}
params = urllib.urlencode(param)
content = urllib2.urlopen(req, params)

buf = content.read()
print security_key

with open("test.html", "wb") as f:
    f.write(buf)

pattern = re.compile('input type="hidden" name="t" value="([^"]+)"')
security_key = ''
match = pattern.search(buf)
if match:
    security_key = match.group(1)
else:
    print "no match"
print security_key


#req = urllib2.Request('https://www.dropbox.com/home/Public/default.css')
req = urllib2.Request('https://dl-web.dropbox.com/get/Public/default.css?_subject_uid=1203890&w=AAD626rGmjgeUayN0wGRduld-lSKhC7T_7paqG9Tn1rgmQ')
req.add_header("User-agent", 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36')
content = urllib2.urlopen(req)
buf = content.read()












## POST



OS_FILESYSTEM_ENCODING = sys.getfilesystemencoding()

FORMENCODE_HEADERS = {
     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
     "Accept-Language": "ja",
     "Accept-Charset": "utf-8"}

MULTIPART_HEADERS = {
     "Content-Type": 'multipart/form-data; boundary=',
     "Accept-Language": "ja",}


        
def is_multipart(postdata):
    for value in postdata.values():
        if isinstance(value, file):
            return True
    return False

def encode_postdata(postdata):
    getRandomChar = lambda: chr(random.choice(range(97, 123)))
    randomChar = [getRandomChar() for x in xrange(20)]
    boundary = "----------%s" % ("".join(randomChar))
    lines = ["--" + boundary]
    for key, value in postdata.iteritems():
        header = 'Content-Disposition: form-data; name="%s"' % key
        if hasattr(value, "name"):
            name = value.name
            if isinstance(name, str):
                name = name.decode(OS_FILESYSTEM_ENCODING)
            header += '; filename="%s"' % os.path.split(name.encode("utf-8"))[-1]
            lines.append(header)
            mtypes = mimetypes.guess_type(value.name)
            if mtypes:
                contentType = mtypes[0]
                header = "Content-Type: %s" % contentType
                lines.append(header)
            lines.append("Content-Transfer-Encoding: binary")
        else:
            lines.append(header)

        lines.append("")
        if hasattr(value, "read"):
            lines.append(value.read())
        elif isinstance(value, unicode):
            lines.append(value.encode("utf-8"))
        else:
            lines.append(value)
        lines.append("--" + boundary)
    lines[-1] += "--"

    return "\r\n".join(lines), boundary



def open_url(url, postdata=None, headers = None):
    encoded = None
    _headers = None
    if postdata:
        if is_multipart(postdata):
            encoded, boundary = encode_postdata(postdata)
            _headers = MULTIPART_HEADERS.copy()
            _headers["Content-Type"] = _headers["Content-Type"] + boundary
        else:
            encoded = urllib.urlencode(postdata)
            _headers = FORMENCODE_HEADERS

    request = urllib2.Request(url, encoded)
    if _headers:
        for key, value in _headers.iteritems():
            request.add_header(key, value)
    if headers:
        for key, value in headers.iteritems():
            request.add_header(key, value)
    #opener = urllib2.build_opener()
    #response = opener.open(request)
    response = urllib2.urlopen(request)

    return response


url = "https://dl-web.dropbox.com/upload"
postdata = {"role": "personal", 'plain':'yes', 'dest':'/Public', 't':security_key, 'mtime':'0',
            "file": open("api.txt", "r+b")}
resp = open_url(url, postdata)
print resp.read()
