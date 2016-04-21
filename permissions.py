import bcrypt

from eve import Eve
from eve.auth import BasicAuth
from werkzeug.security import check_password_hash


class RolesAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        if resource == 'accounts':
            return username == 'superuser' and password == 'password'
        accounts = app.data.driver.db['accounts']
        lookup = {'username': username}
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        print lookup
        account = accounts.find_one(lookup)
        print account, account['password'], password
        return account and account['password'] in password
        #return account and bcrypt.hashpw(password, account['password']) == account['password']


if __name__ == '__main__':
    app = Eve(auth=RolesAuth)
    app.run()
