import random
from   membership import User


random.seed()

text = '''\
Hello {name},

Per our previous email, we are automating the way we handle membership renewals.  To facilitate this change, we have set up
an online account for you.

Please sign in to:
  1 - verify your contact info and membership status and
  2 - change your user name
  3 - change your password

https://membership.sjaa.net/login

user name: {login}
password: {password}


Sincerely,
Dave Ittner
SJAA Membership Chair

'''

def signup():
    good = 0
    bad  = 0
    for user in User.objects.filter(pk_gte=1000):
        if signup_user(user):
            good += 1
        else:
            bad  += 1
    print('good / bad  :  {} / {}'.format(good, bad))


subject = 'SJAA Membership Account'
test_modes = []


def signup_user(user):
    # generate username, password
    password = str(random.randint(10000000, 99999999))
    user.set_password(password)
    # generate email
    addr_to = user.email
    subst_dict = {'name' : user.get_full_name(),
                  'username' : user.username,
                  'password' : password}
    body = text.format(**subst_dict)
    try:
        send_gmail('me', addr_to, subject, body, test_modes)
        user.save()
        return True
    except:
        print('
        return False

