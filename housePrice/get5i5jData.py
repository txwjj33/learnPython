# _*_ coding: UTF-8 _*_
import urllib
import urllib2
import cookielib

# userAgent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
filename = "cookie.txt"
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

def login(username, password):
    data = {
        "username": username,
        "password": password,
        "aim": "pc",
        "service": "https://tj.5i5j.com/reglogin/index?preUrl=https%3A%2F%2Ftj.5i5j.com%2Fzufang%2F",
        # "status": 1
    }
    postdata = urllib.urlencode(data)
    loginURL = "https://passport.5i5j.com/passport/sigin?city=tj"
    result = opener.open(loginURL, postdata)
    # cookie.save(ignore_discard = True, ignore_expires = True)

login("18301268696", "txwjj123456")

focusURL = "https://tj.5i5j.com/user/myfocus/2/"
result1 = opener.open(focusURL)
print(result1.read())
