import json
from lib2to3.pgen2 import driver

from time import sleep

from random import randint

from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait


# ======================================================================================================================
# class login
class Loginpage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://www.instagram.com/accounts/login/')

    def Readuserpassword(self, Filename):
        fp = open(Filename, 'r')
        lines = fp.readlines()

        username = lines[0].replace('\n', '')

        password = lines[1].replace('\n', '')

        return username, password

    def login(self, Username, Password):
        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        username_input.send_keys(Username)
        password_input = self.browser.find_element_by_css_selector("input[name='password']")
        password_input.send_keys(Password)

        login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()
        sleep(3)

        notnow = self.browser.find_element_by_css_selector(
            '#react-root > section > main > div > div > div > div > button')
        notnow.click()
        sleep(randint(1, 6))
        notNotifications = self.browser.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
        notNotifications.click()


# ==================================================================================================

# Main
browser = webdriver.Firefox()
browser.implicitly_wait(3)
filename = 'C:/Users/MYava/Desktop/instagram.txt'
AutoLogin = Loginpage(browser)
Username, Password = AutoLogin.Readuserpassword(filename)
AutoLogin.login(Username, Password)
sleep(5)
# =================================================================================================

# find post  public page

page_id = ['ketabbaztv']
output_page = 'C:/Users/MYava/Desktop/link_post_page.txt'
with open(output_page, 'w') as page:
    tag = -1
    for post in page_id:
        tag += 1
        browser.get('https://www.instagram.com/' + page_id[tag] + '/')
        sleep(7)
        for i in range(1, 4):
            try:
                for j in range(1, 4):
                    # آدرس پست ها رو داخل یک فایل ذخیره میکنه
                    elementpath = '#react-root > section > main > div > div._2z6nI > article > div:nth-child(1) > div > div:nth-child(' + str(
                        i) + ') > div:nth-child(' + str(j) + ') > a'
                    thumbnail = browser.find_element_by_css_selector(elementpath)
                    posturl = thumbnail.get_attribute("href")
                    print('posturl: ', posturl)
                    sleep(randint(1, 12))
                    page.write('{}\n'.format(posturl))

                browser.execute_script("window.scrollBy(0,3000000)")
                sleep(randint(1, 8))
                browser.execute_script("arguments[0].scrollIntoView();", elementpath)
            except:
                continue

page.close()
print('آدرس پست های پیدا شده ذخیره شد.')
print("============================================================================================")
# =================================================================================================
# open post and get comments
dic_post_Comments = {}
list_comments_info = []
f1 = 1

like_post = " "
view_post = " "

reply_comment = " "

outputfile_path = 'C:/Users/MYava/Desktop/link_post_page.txt'
with open(outputfile_path, 'r') as posts_URL:
    for address in posts_URL.readlines():
        # فایل آدرس های ذخیره شده رو باز میکنه
        list_comments_info = []
        like_post = " "
        view_post = " "
        reply_comment = " "
        print('f1 = ', f1)
        f1 = f1 + 1
        print('address=', address)
        browser.get(address)
        # کپشن پست رو میگیره
        caption = browser.find_element_by_class_name("MOdxS ").find_element_by_tag_name("span").text
        print('caption: ', caption)
        # تاریخ انتشار پست رو میگیره
        time_post = browser.find_element_by_css_selector("._1o9PC").text
        try:
            # اگر پست ویدئو باشه تعداد بازدید ویدئو رو میگیره
            view_post = browser.find_element_by_css_selector(".vcOH2 > div:nth-child(1) > span:nth-child(1)").text
        except:
            # اگر پست فقط عکس باشه تعداد لایک پست رو میگیره
            print("post is image")
            like_post = browser.find_element_by_css_selector(
                ".gL6fO > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > span:nth-child(1)").text

        print("view post:", view_post)
        print("like post: ", like_post)

        # برای اینکه تعداد بیشتری کامنت قابل مشاهده باشه روی گزینه more comment کلیلک میکنه
        for i in range(1, 6):
            WebDriverWait(driver, 20)
            sleep(randint(1, 3))
            more_comment_button = browser.find_element_by_css_selector(".NUiEW > button:nth-child(1)")
            more_comment_button.click()
            sleep(randint(1, 10))
        #تمام کامنتها رو میگیره
        comments = browser.find_element_by_class_name("XQXOT").find_elements_by_class_name("Mr508")
        l = 1
        for comment in comments:
            # برای کامنت آیدی فرد و متن کامنت رو میگیره
            l = l + 1
            d = comment.find_element_by_class_name("ZyFrc").find_element_by_tag_name("li").find_element_by_class_name(
                "P9YgZ").find_element_by_tag_name("div")
            d = d.find_element_by_class_name("C4VMK")
            user = d.find_element_by_tag_name("h3").text
            comm_text = d.find_element_by_class_name("_7UhW9").text
            # تعداد لایکی که کامنت خورده
            like_comment = browser.find_element_by_css_selector("ul.Mr508:nth-child(" + str(
                l) + ") > div:nth-child(1) > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > div:nth-child(1)")
            num_like_comment = like_comment.text
            # print("num like comment: ", num_like_comment)
            if num_like_comment == "Reply":
                num_like_comment = "0 like"
            # اگر کامنت reply خورده تعداد reply رو میگیره
            try:
                reply_comment = browser.find_element_by_css_selector("ul.Mr508:nth-child(" + str(
                    l) + ") > li:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > div:nth-child(1) > button:nth-child(1) > span:nth-child(2)").text
                print("reply comment: ", reply_comment)
            except:
                print("comment not reply so reply = 0")
                reply_comment = "0"


            if like_post != " ":
                list_comments_info.append(
                    {"username": user, "comment": comm_text, "like comment": num_like_comment,
                     "reply comment": reply_comment, "address": address,
                     "caption": caption, "like_post": like_post, "time_post": time_post})
            elif view_post != " ":
                list_comments_info.append(
                    {"username": user, "comment": comm_text, "like comment": num_like_comment,
                     "reply comment": reply_comment, "address": address,
                     "caption": caption, "view_post": view_post, "time_post": time_post})

            # ذخیره اطلاعاتی که گرفته شده داخل دیکشنری
            dic_post_Comments[address.replace('.', '^')] = list_comments_info
            print("----------------------------------------------------------")


        print("============================================================================================")

    # save to json file
    json_output = {}
    json_output['post_Comments'] = dic_post_Comments
    # dic_post_Comments = {}
    y = json.dumps(json_output, ensure_ascii=False).encode('utf-8')
    final_output_path = 'C:/Users/MYava/Desktop/output_post_page.json'
    fp = open(final_output_path, 'w', encoding='utf8')
    fp.write(str(y.decode('utf-8')))
    fp.close()

# =======================================================================================================================

browser.close()
