import bb_bot


def main():
    print('================================================================================')
    print('|             Bautura-Online.ro 1.0.0.0 by Allex Radu [www.ATFR.net]            |')
    print('|   Get the latest version at https://github.com/allexradu/Bautura_Online_Bot   |')
    print('================================================================================')
    print('|     Instructions: Save your Excel Workbook as "a.xls" and place it in         |')
    print('|     the excel folder, make sure the file in not opened.                       |')
    print('================================================================================')
    print('|         WARNING!!! WRITE THIS DOWN! To stop the bot press CTRL + C            |')
    print('================================================================================')

    while True:
        try:
            seconds_delay = float(input('Number of seconds delay from one image to another: ' +
                                        '\n (the slower the computer / connection the higher the number)' +
                                        '\n [Minimum 1 sec recommended] seconds: '))
        except:
            print('Invalid Input!!! Try again!')
        else:
            bb_bot.BBBot(delay = seconds_delay)
            break


if __name__ == '__main__':
    main()
