from instabot import Bot
bot = Bot()

import os 
import glob

try:
    cookie_del = glob.glob("config/*cookie.json")
    os.remove(cookie_del[0])
except:
    pass 

bot.login(username="semrakazimli", password="amelliparol")

bot.upload_photo("kataloqlar-20231129-0001.webp",caption="DaliDaliDali Saiba ")
#my_followers = bot.followers

# with open("result.html","w") as write:
#     write.write(str(my_followers))



# # Make a list of users
# urer_ids = ["46646131624", "45392973279"]
 
# # Message
# text = "hi)"
 
# # Sending messages
# bot.send_messages(text, urer_ids)



# print(my_followers)