from instabot import Bot


import os 
import glob
usernames = { 
    "semrakazimli": "amelliparol",
    "kataloqlar": "emelliparol"
}

for username, password in usernames.items() :
    try:
        bot = Bot()

        try:
            cookie_del = glob.glob("config/*cookie.json")
            os.remove(cookie_del[0])
        except:
            pass 

        bot.login(username=username, password=password)

        bot.upload_photo("kataloqlar-20231129-0001.webp",caption="DaliDaliDali Saiba ")
    except:
        pass
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