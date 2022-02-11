import hashlib

hash_password = '21232f297a57a5a743894a0e4a801fc3'


def is_admin(password):
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    if md5_hash.hexdigest() == hash_password:
        return True
