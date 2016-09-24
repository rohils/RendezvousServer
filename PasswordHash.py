from passlib.hash import md5_crypt

class PasswordHash(object):
    def __init__(self, hash_):
        self.hash = str(hash_)

    def __eq__(self, candidate):
        if type(candidate) == str:
            return md5_crypt.verify(candidate, self.hash)
        return False

    def __repr__(self):
        return '<{}>'.format(type(self).__name__)

    @classmethod
    def new(cls, pwd):
        return cls(md5_crypt.encrypt(pwd))
