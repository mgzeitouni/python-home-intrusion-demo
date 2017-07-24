import requests
import json
from urllib2 import urlopen
import time
import calendar
import base64

base_url = "https://api.netatmo.com"
current_token = "581a043f29977eb6608b4745|c697018549d7b8843b1330f5c4d50372"
client_id = "581a17bf29977ec4218b4b8f"
client_secret = "ptCT8AQc7WEBWPL22F0gBtR7ZYhI8LGoV0"
grant_type = "password"
username = "mgzeitou@us.ibm.com"
password = "Watsoniot1@"
scope = "read_camera"
refresh_token1 = "581a043f29977eb6608b4745|523d6c34db86ce2ee6e5ae1f172e4191"
cloudant_url = "https://9a894360-dc51-4785-a399-b2a8719c20bb-bluemix:e180413ec8c4116acc4c682a0583ef7c8ef935b3ccd62801b4f2777e2734192e@9a894360-dc51-4785-a399-b2a8719c20bb-bluemix.cloudant.com"


def get_save_face(image_id, key):

    image_url = "%s/api/getcamerapicture?image_id=%s&key=%s" % (base_url, image_id, key)
    image_name = "%s.jpg" %calendar.timegm(time.gmtime())
    unix_time = calendar.timegm(time.gmtime())
    f = open('images/%s'%image_name,'wb')

    f.write(urlopen(image_url).read())
    f.close()

    with open('images/%s'%image_name, "rb") as binary_file:
    # Read the whole file at once
        jpeg_data = base64.b64encode(binary_file.read())


    headers = {"Content-Type": "application/json"}

    # Create document
    payload = {"_id":str(unix_time), "netatmo_image_id":image_id, "netatmo_face_key":key}
    rev = requests.post("%s/face_images" %(cloudant_url),  data=json.dumps(payload), headers=headers).json()["rev"]

    # Create attachment
    payload = {"_id":str(unix_time),
               "_rev":rev,
               "netatmo_image_id":image_id,
               "netatmo_face_key":key,
            "_attachments":
              {
    str(unix_time):
    {
      "content_type":"image/jpeg",
      "data": "%s" %str(jpeg_data)
    }
    }
              }

    url = "%s/face_images/%s" %(cloudant_url,str(unix_time) )
    print url
    print requests.put(url, data=json.dumps(payload), headers=headers).text
    return image_name, jpeg_data
