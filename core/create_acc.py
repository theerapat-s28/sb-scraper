from core import settings
import os


def create_credential_file():
  '''
  Create file that store username and password for siambit.
  '''
  try:
    username = input('Username: ')
    password = input('Password: ')
    credential_file_path = settings.BASE_DIR/'core/credential.py'
    with open(credential_file_path, 'x') as f:
        f.write(f'USERNAME="{username}"')
        f.write('\n')
        f.write(f'PASSWORD="{password}"')

  except:
      print("Error @ create_credential_file()")


def check_credential():
  '''
  desc: Check if credential file exist and create if does not.
  '''
  credential_file_path = settings.BASE_DIR/'core/credential.py'
  is_file_exist = os.path.exists(credential_file_path)
  
  if not is_file_exist:
    create_credential_file()
  else:
    from core import credential
