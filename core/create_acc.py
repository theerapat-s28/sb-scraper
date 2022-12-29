from core import settings
import os


def create_credential_file():
  '''
  Create file that store username and password for siambit.
  '''
  try:
    siambit_username = input('Siambit Username: ')
    siambit_password = input('Siambit Password: ')
    rapidgator_username = input('Rapidgator Username: ')
    rapidgator_password = input('Rapidgator Password: ')
    credential_file_path = settings.BASE_DIR/'core/credential.py'
    with open(credential_file_path, 'x') as f:
        f.write(f'SIAMBIT_USERNAME="{siambit_username}"')
        f.write('\n')
        f.write(f'SIAMBIT_PASSWORD="{siambit_password}"')
        f.write('\n')
        f.write(f'RAPIDGATOR_USERNAME="{rapidgator_username}"')
        f.write('\n')
        f.write(f'RAPIDGATOR_PASSWORD="{rapidgator_password}"')

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
