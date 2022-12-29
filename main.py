from core.create_acc import check_credential
from xidol import xidol

def main():
  #(v) initiate credential file
  check_credential()

  print('''
  Which scraping program to use?
    1 = siambit
    2 = xidol
  ''')
  program = input('Please select: ')

  if program == '1':
    from siambit.siambit import screen_shot_scrapper
    screen_shot_scrapper()
  elif program == '2':
    xidol.main()


if __name__ == "__main__":
	main()