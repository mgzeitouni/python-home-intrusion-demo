import requests
import json

import time
import calendar



base_url = "https://api.netatmo.com"
current_token = "581a043f29977eb6608b4745|c697018549d7b8843b1330f5c4d50372"
client_id = "581a17bf29977ec4218b4b8f"
client_secret = "ptCT8AQc7WEBWPL22F0gBtR7ZYhI8LGoV0"
grant_type = "password"
username = "mgzeitou@us.ibm.com"
password = "Watsoniot1@"
scope = "read_camera"
refresh_token1 = "581a043f29977eb6608b4745|523d6c34db86ce2ee6e5ae1f172e4191"

def get_save_face(image_id, key):
    
    image_url = "%s/api/getcamerapicture?image_id=%s&key=%s" % (base_url, image_id, key)
    image_name = "%s.jpg" %calendar.timegm(time.gmtime())
    
    f = open('images/%s'%image_name,'wb')
    
    f.write(urlopen(image_url).read())
    f.close()
    
    return image_name