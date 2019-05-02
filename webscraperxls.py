from bs4 import BeautifulSoup
import urllib.request
import xlwt



def get_name(body):
    return body.find('span', {'class':'jcn'}).a.string

def get_phone(body):
    number = ''
    try :
        content = body.find('p', {'class':'contact-info'}).span.a.b.findChildren('span')
        for item in content[-10:]:
            if item['class'][1].split('-')[1] == 'yz':
                number += '1'
            if item['class'][1].split('-')[1] == 'wx':
                number += '2'
            if item['class'][1].split('-')[1] == 'vu':
                number += '3'
            if item['class'][1].split('-')[1] == 'ts':
                number += '4'
            if item['class'][1].split('-')[1] == 'rq':
                number += '5'
            if item['class'][1].split('-')[1] == 'po':
                number += '6'
            if item['class'][1].split('-')[1] == 'nm':
                number += '7'
            if item['class'][1].split('-')[1] == 'lk':
                number += '8'
            if item['class'][1].split('-')[1] == 'ji':
                number += '9'
            if item['class'][1].split('-')[1] == 'acb':
                number += '0'
        return number
    except:
        try:#if Landline Number specified
            content = body.find('p', {'class':'contact-info'}).span.a.findChildren('span')
            for item in content[-8:]:
                if item['class'][1].split('-')[1] == 'yz':
                    number += '1'
                if item['class'][1].split('-')[1] == 'wx':
                    number += '2'
                if item['class'][1].split('-')[1] == 'vu':
                    number += '3'
                if item['class'][1].split('-')[1] == 'ts':
                    number += '4'
                if item['class'][1].split('-')[1] == 'rq':
                    number += '5'
                if item['class'][1].split('-')[1] == 'po':
                    number += '6'
                if item['class'][1].split('-')[1] == 'nm':
                    number += '7'
                if item['class'][1].split('-')[1] == 'lk':
                    number += '8'
                if item['class'][1].split('-')[1] == 'ji':
                    number += '9'
                if item['class'][1].split('-')[1] == 'acb':
                    number += '0'
            return number
        except:#if no number specified
            return number

def get_rating(body):
    rating = 0.0
    text = body.find('span', {'class':'star_m'})
    if text is not None:
        for item in text:
            rating += float(item['class'][0][1:])/10
    return rating

def get_rating_count(body):
    text = body.find('span', {'class':'rt_count'}).string
    # Get only digits
    rating_count =''.join(i for i in text if i.isdigit())
    return rating_count

def get_address(body):
    return body.find('span', {'class':'mrehover'}).text.strip()

def get_categ(body):
    li_categ = []
    categ = body.findChildren('a',{'class':'lng_commn'})
    for cat in categ:
        li_categ.append(cat.string.strip())
    return li_categ

page_number = 1
service_count = 1

book=xlwt.Workbook()
sheet1=book.add_sheet('GymData')
index=['Name','Number','Address','Rating','No. of Reviewers','Category']
style=xlwt.XFStyle()
font=xlwt.Font()
font.name='Times New Roman'
font.bold=True
style.font=font
for n in range(0,len(index)):
    sheet1.write(0,n,index[n].upper(),style)#Write Header Row.
row = 1


while True:
    # Check if reached end of result
    if page_number > 50:
        break
    url="https://www.justdial.com/Mumbai/Gyms/nct-11575244/page-%s" % (page_number)
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    page = urllib.request.urlopen( req )
    soup = BeautifulSoup(page.read(), "html.parser")
    services = soup.find_all('li', {'class': 'cntanr'})
    # Iterate through the 10 results in the page
    for service_html in services:
        name = get_name(service_html)
        phone = get_phone(service_html)
        rating = get_rating(service_html)
        count = get_rating_count(service_html)
        address = get_address(service_html)
        category = get_categ(service_html)
        if name != None:
            sheet1.write(row, 0, name)
        if phone != None:
            sheet1.write(row, 1, phone)
        if address != None:
            sheet1.write(row, 2, address)
        if rating != None:
            sheet1.write(row, 3, rating)
        if count != None:
            sheet1.write(row, 4, count)
        if category != None:
            sheet1.write(row, 5, category)
        row += 1
        service_count += 1
    page_number += 1
book.save('Gym.xls')

