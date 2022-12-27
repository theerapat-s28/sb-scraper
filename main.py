from core.create_acc import check_credential


def main():
  #(v) initiate credential
  check_credential()

  from siambit.siambit import screen_shot_scrapper
  screen_shot_scrapper()


if __name__ == "__main__":
	main()