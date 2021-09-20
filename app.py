import os, socket
import dropbox

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
  
ip = socket.gethostbyname(socket.gethostname())


# class for dropbox
class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

class MyHandler(FTPHandler):

    def on_connect(self):
        print ("connected")

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        # dropbox informations
        access_token = '8cav-lnOtoIAAAAAAAAAAWQD0QUTmG7Zk1xA0izMY5fpB-uljUUfpk9JmelGX4jj'
        transferData = TransferData(access_token)
        file_from = file
        file_to = '/test/' + file.rsplit("/", 1)[-1]
        transferData.upload_file(file_from, file_to)
        print("the file is received")
    
        os.remove(file)
        pass

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)


def main():

    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', homedir='./files', perm='elradfmwMT')
    authorizer.add_anonymous(homedir='./files')

    handler = MyHandler
    handler.authorizer = authorizer
    server = FTPServer((ip, 2121), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()