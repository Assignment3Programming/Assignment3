from datetime import date

import json

# GLOBAL VARIABLES
with open('items.json', 'r') as f:
    items = json.load(f)
with open('customers.json', 'r') as f:
    customers = json.load(f)

current_customer_id = str(len(customers))
customers[current_customer_id] = {
    'name': '',
    'address': '',
    'email': '',
    'phone': '',
    'purchased': {}
}
shopping_cart = {}
price = [0]


# 6 MAIN FEATURES
def list_item(temp):
    """
    To show list of available items in the store
    :param temp
    :return: nothing
    """
    for id in items:
        print(id, ':', items[id]['name'])
    print('')
    if temp == 1:
        return
    main('else ')


def list_info_product(temp):
    """
    To show a product's information based on the input ID or name of product
    :param temp
    :return: nothing
    """
    # dict to call function
    acceptable = {
        'n': search_by_name,
        'N': search_by_name,
        'i': search_by_id,
        'I': search_by_id
    }

    while True:
        search_type = input(
            'Would you like to view the product information by ID or name ? (I/N)\n')
        if search_type in acceptable:
            check, type_of_search, result = acceptable[search_type](1)
            if check:
                if type_of_search == 'name':
                    for id in items:
                        if items[id]['name'] == result and items[id]['quantity'] > 0:
                            print('name :', items[id]['name'])
                            print('id :', id)
                            print('author :', items[id]['author'])
                            print('quantity :', items[id]['quantity'])
                            print('price :', items[id]['price'])
                else:
                    print('name :', items[result]['name'])
                    print('id :', result)
                    print('author :', items[result]['author'])
                    print('quantity :', items[result]['quantity'])
                    print('price :', items[result]['price'])
            break
    main('else ')


def search_by_name(temp):
    """
    To show a product's information based on the input name of product
    :param temp:
    :return: nothing
    """
    book_name = input('What is the name of the book ?\n')
    check = False
    for id in items:
        if items[id]['name'] == book_name and items[id]['quantity'] > 0:
            check = True
            print('The book you are looking for is available')
            if (temp != 1):
                print('id :', id)
                print('author :', items[id]['author'])
                print('quantity :', items[id]['quantity'])
                print('price :', items[id]['price'])

    if not check:
        print('The book you are looking for is currently unavailable')
    if temp == 1:
        return check, 'name', book_name
    else:
        main('else ')


def search_by_id(temp):
    """
    To show a product's information based on the input ID of product
    :param temp:
    :return: nothing
    """
    result = 0
    check = False
    try:
        id = input('What is the ID of the book ? \n')
        if id in items:
            check = True
            print('The book you are looking for is available')
            if (temp != 1):
                print('id :', id)
                print('author :', items[id]['author'])
                print('quantity :', items[id]['quantity'])
                print('price :', items[id]['price'])
        else:
            check = False
            print('The book you are looking for is currently unavailable')
        if temp == 1:
            return check, 'id', id
        main('else ')
    except ValueError:
        check = False
        print('You have typed incorrectly or the id does not exist')
        if temp == 1:
            return check, 'id', result
        main('else ')


def list_info_customer(temp):
    """
    To show the customer information based on input customer ID
    :param temp:
    :return:
    """
    while True:
        customer_id = input("Please type customer ID:\n")
        if customer_id == 'end':
            end(temp)
            return
        if customer_id in customers:
            print('id :', customer_id)
            print('customer name :', customers[customer_id]['name'])
            print('customer address :', customers[customer_id]['address'])
            print('customer email address :', customers[customer_id]['email'])
            print('customer phone number :', customers[customer_id]['phone'])
            print('customer purchased :')
            for item_id in customers[customer_id]['purchased']:
                print('id:', item_id, ' name :', items[item_id]['name'],
                      ' quantities :', customers[customer_id]['purchased'][item_id])
        else:
            print('You have typed incorrectly or the ID does not exist')
        break

    main('else ')


def placing_order(temp):
    """
    To check out with all items currently in shopping cart, calculate total prices taking into account the shipment method and promotion. At the same time, store user's information in local database and update the remaining quantity of products
    :param temp
    :return: nothing
    """

    # check whether the cart is empty
    if len(shopping_cart) != 0:

        # print out shopping cart
        show_current_shopping_cart(1)

        # confirm customer information
        print('Please let us take some information')
        name = input('What is your name? ')
        address = input('What is your address? ')
        email_address = input('What is your email address? ')
        phone_number = input('What is your phone number? ')
        customers[current_customer_id]['name'] = name
        customers[current_customer_id]['address'] = address
        customers[current_customer_id]['email'] = email_address
        customers[current_customer_id]['phone'] = phone_number
        customers[current_customer_id]['purchased'] = shopping_cart

        # PROMOTIONS
        promo_check = False
        if price[0] >= 1000000:
            price[0] = round(price[0] * 4 / 5)
            print('the Third promotion has been applied to your order')
            promo_check = True
        elif price[0] >= 500000:
            price[0] = round(price[0] * 9 / 10)
            print('the Second promotion has been applied to your order')
            promo_check = True
        else:
            # check whether this is the first time customer
            first_time = True
            for id in customers:
                if id == current_customer_id:
                    continue
                if customers[id]['phone'] == phone_number:
                    first_time = False
                    break
            if first_time:
                price[0] = round(price[0] * 9 / 10)
                print('the First promotion has been applied to your order')
                promo_check = True
        if promo_check:
            print('Total price after promotion:', price[0])

        # SHIPPING METHODS
        while True:
            shipping_method = {
                "1": 30000,
                "2": 50000,
                "3": 100000,
            }
            # call function
            show_shipping_methods(1)
            shipping_choice = input(
                'What shipping method would you like to use? (1,2,3) ')
            if shipping_choice not in shipping_method:
                continue
            price[0] += shipping_method[shipping_choice]
            customers[current_customer_id]['paid'] = price[0]
            break

        # final announcement
        print('Total price with shipping cost included is: ', price[0])
        print('Your order has been queued!\nWe will try our best to contact you as soon as possible!')

        # update resources after complete the order
        with open('items.json', 'w') as f:
            json.dump(items, f)
        with open('customers.json', 'w') as f:
            json.dump(customers, f)

        # back to the main function
        main('else ')

    else:
        print('Your current shopping cart is empty')
        answer = input('Would you like to add something to your cart? (Y/N)\n')
        if answer.lower() == 'y':
            buy_request(1)
        else:
            main('else ')


# other feature

def buy_request(temp):
    """
    To add chosen items in the shopping cart
    :param temp
    :return: nothing
    """
    list_item(1)
    print('Above are the currently available products in our store')
    while True:
        id = input(
            'Please select Id of the product that you want to purchase: \n')
        if id in items:
            try:
                quantity = int(
                    input('How many of this product do you want ? \n'))
                if quantity <= 0:
                    print('Invalid value')
                    continue
                while quantity > items[id]['quantity']:
                    print('We only have', items[id]['quantity'],
                          'of this product left, please select the quantity again')
                    quantity = int(
                        input('How many of this product do you want ? \n'))

                # update current item quantity
                items[id]['quantity'] -= quantity

                # update current cart price
                price[0] += items[id]['price'] * quantity
                shopping_cart[id] = quantity
                print("Your order has been added to cart!")
                choice = input('Do you want anything else? (Y/N)\n')
                if choice.lower() == 'y':
                    continue
                if temp != 1:
                    print('To complete the order, please go to placing order section.')
                    print('*Please note that the order will not be executed if you do not place it in the placing order section !')
                    break
                placing_order(temp)
            except ValueError:
                print('Sorry we do not understand your order!')
                break

        else:
            print('The Id of the product that you are looking for does not exist')
            if temp != 1:
                main('else ')
    if (temp != 1):
        main('else ')


def show_current_shopping_cart(temp):
    """
    To show all items currently in the shopping cart
    :param temp
    :return: nothing
    """
    if (len(shopping_cart) != 0):
        print('Here is your current shopping cart')
        index = 1
        for item_id in shopping_cart:
            print(index, ') ', 'name:', items[item_id]['name'],
                  'id:', item_id, 'quantity:', shopping_cart[item_id])
            index += 1
        print('Total price: ', price[0], 'VND')
    else:
        print('Your cart is empty!')
    if temp != 1:
        main('else ')


def show_shipping_methods(temp):
    """
    To show all available shipping method and their costs
    :param temp
    :return: nothing
    """
    print(
        'Our store offers 3 available shipping options \n1. Normal: 30000 (1-2 weeks)\n2.Fast:50000 (3-5 days)\n3.Rocket: 100000 (Same day delivery, Only accept if you are in Ha Noi)\n')
    if temp != 1:
        main('else ')


def voucher_promotion(temp):
    """
    To show information about all available promotions
    :param temp
    :return: nothing
    """
    promotions = {
        "1": '-10% Vouchers are applied to first time customers to our store (We base on clients phone number in our database))',
        "2": '-10% Off for customer with bills over 500.000 VND',
        "3": '-20% Off for customer with bills over 1.000.000 VND'
    }
    print(promotions['1'])
    print(promotions['2'])
    print(promotions['3'])
    print('These promotions do not applied together at once')
    if temp == 0:
        main('else ')


def reports_section(temp):
    """
    To receive reports from customers or to show their report history
    :param temp:
    :return: nothing
    """
    with open('reports.json', 'r') as f:
        reports = json.load(f)
    choice = input(
        'Would you like to report issue or access report history (Type 1 or 2)\n')
    if choice == '1':
        issues = input('Please tell us about your problem :')
        print('Please give us some information to answer your request')
        name = input('What is your name ? ')
        phone = input('What is your phone number ? ')
        reports[len(reports)] = {
            'issues': issues,
            'name': name,
            'phone': phone
        }

        # update reports file
        with open('reports.json', 'w') as f:
            json.dump(reports, f)
        print('Thanks for your report!')

    else:
        for report_id in reports:
            print('report id: ', report_id)
            print('problem:', reports[report_id]['issues'])
            print('customer name: ', reports[report_id]['name'])
            print('phone number: ', reports[report_id]['phone'], '\n')
    main('else ')


def end(temp):
    """
    To quit the purchasing session
    :param temp
    :return: nothing
    """
    print("Thank you for shopping with us!")


print('Welcome to our book store!\n')

def welcome():
    """
    To start a purchasing session, give instructions to customers
    :return: nothing
    """
    print('Here are our instructions:')
    print("""1: list item
2: list product information
3: search by name
4: search by id
5: list customer information
6: placing order
7: buy item
8: current shopping cart
9: shipping methods
10: voucher promotion
11: reports section
12: end\n""")


def understand_order(order):
    """
    To determine which action to make according to customers' request
    :param order: a number that implies a request
    :return: call the respective function to execute a request
    """
    # dict to call function
    order_list = {
        1: list_item,
        2: list_info_product,
        3: search_by_name,
        4: search_by_id,
        5: list_info_customer,
        6: placing_order,
        7: buy_request,
        8: show_current_shopping_cart,
        9: show_shipping_methods,
        10: voucher_promotion,
        11: reports_section,
        12: end
    }
    return order_list.get(order)


def main(s):
    """
    To prompt request from customers, pass it to understand_order function
    :param s: a string to complete the message to customers after each request being fulfilled
    :return: nothing
    """
    welcome()
    while True:
        try:
            order = int(
                input('What ' + s + 'can we help ? (Choose a number in our instructions)\n'))
            if order <= 12 and order >= 1:
                break
            else:
                print('Sorry we do not understand your order')
        except ValueError:
            print('Sorry we do not understand your order')
            pass
    understand_order(order)(0)

main('')
