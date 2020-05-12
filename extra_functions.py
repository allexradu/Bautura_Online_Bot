category_url = ''
sub_category_url = ''
narrow_list_html = ''
last_page = 0


def sub_category_xpath(index):
    return '//*[@id="narrow-by-list"]/dd[1]/ol/li[{index}]/a'.format(index = index)


def product_xpath(index):
    return '/html/body/main/div/div/div/div[2]/div[6]/ul/li[{index}]/div/div/div[1]/p/a'.format(index = index)
