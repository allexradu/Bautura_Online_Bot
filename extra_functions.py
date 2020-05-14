category_url = ''
sub_category_url = ''
narrow_list_html = ''
last_page = 0


def main_category_css_path(index):
    return 'ul#nav>li:nth-of-type({main_category_index})>a'.format(main_category_index = index)


def sub_category_xpath(index):
    return '//*[@id="narrow-by-list"]/dd[1]/ol/li[{index}]/a'.format(index = index)


def product_xpath(index):
    return '/html/body/main/div/div/div/div[2]/div[6]/ul/li[{index}]/div/div/div[1]/p/a'.format(index = index)


def extract_attributes_from_html(string, key):
    if string.find(key) != -1:
        start_label_string = string.find(key)
        start_concentration_string = string.find('<td class="data">', start_label_string) + 17
        end_concentration_string = string.find('</td>', start_label_string)
        return string[start_concentration_string:end_concentration_string]
    else:
        return 'n/a'


def value_key(cell_letter, cell_number):
    return '{cell_letter}{cell_number}'.format(cell_letter = cell_letter,
                                               cell_number = cell_number)
