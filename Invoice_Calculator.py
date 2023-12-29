from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window

#Set the app size
Window.size = 300, 600

class StylesLayout(Widget):

    red_color = [1, 0, 0]
    green_color = [0, 1, 0]
    default_color = [0.3, 0.3, 0.3]

    def change_repeat_customer_button_state(self):
            if self.ids.repeat_customer_button.state == "down":
                self.ids.repeat_customer_button.background_color = self.green_color
            else:
                self.ids.repeat_customer_button.background_color = self.default_color

    def change_shipping_button_state(self):
        if self.ids.shipping_button.state == "down":
            self.ids.shipping_button.background_color = self.green_color
        else:
            self.ids.shipping_button.background_color = self.default_color

    def change_parts_button_state(self):
        if self.ids.one_part_button.state == "down":
            self.ids.one_part_button.background_color = self.green_color
            self.ids.two_parts_button.background_color = self.default_color
            self.ids.three_parts_button.background_color = self.default_color
        elif self.ids.two_parts_button.state == "down":
            self.ids.one_part_button.background_color = self.default_color
            self.ids.two_parts_button.background_color = self.green_color
            self.ids.three_parts_button.background_color = self.default_color
        elif self.ids.three_parts_button.state == "down":
            self.ids.one_part_button.background_color = self.default_color
            self.ids.two_parts_button.background_color = self.default_color
            self.ids.three_parts_button.background_color = self.green_color
        else:
            self.ids.one_part_button.background_color = self.default_color
            self.ids.two_parts_button.background_color = self.default_color
            self.ids.three_parts_button.background_color = self.default_color

    def change_worker_button_state(self):
            if self.ids.workers_button.state == "down":
                self.ids.workers_button.background_color = self.green_color
            else:
                self.ids.workers_button.background_color = self.default_color

    def submit(self):
        try:
            main_price = float(self.ids.main_price.text)
        except:
            self.ids.main_price.hint_text = "price field cannot be empty"
            self.ids.submit_button.background_color = self.red_color
        
        sellers_tax = 8.75
        multiplication_index = 8
        
        #labor
        labor_cost = round(main_price/100*40)
        if self.ids.workers_button.state == "down":
            labor_cost = 210
        elif labor_cost < 149:
            labor_cost = 149
        elif labor_cost > 179:
            labor_cost = 179
        labor_discount = labor_cost/10

        #shipping
        if self.ids.shipping_button.state == "down":
            shipping = 20
        else:
            shipping = 0
        
        #main part
        main_part_price = main_price - labor_cost - shipping
        tax_inside_a_price = main_part_price/100*multiplication_index
        total_parts_cost = (main_price - labor_cost - shipping)-tax_inside_a_price
        part_tax = total_parts_cost/100*sellers_tax

        if self.ids.repeat_customer_button.state == "down":
            total_parts_cost += labor_discount
        else:
            labor_discount = 0

        #total price
        total_price = total_parts_cost + part_tax + labor_cost + shipping - labor_discount

        #truncation .0 numbers
        def truncate(float_number):
            multiplier = 100
            return str(int(float_number * multiplier)/multiplier)

        #output
        if self.ids.two_parts_button.state == "down":
            first_part = main_part_price/100*60
            second_part = main_part_price/100*40
            print("first part price: " + truncate(first_part))
            print("second part price: " + truncate(second_part))
        elif self.ids.three_parts_button.state == "down":
            first_part = main_part_price/100*50
            second_part = main_part_price/100*30
            third_part = main_part_price/100*20
            print("first part price: " + truncate(first_part))
            print("second part price: " + truncate(second_part))
            print("third part price: " + truncate(third_part))

        print( "total part cost: " + truncate(total_parts_cost) )
        print( "tax: " + truncate(part_tax) )
        print( "labor: " + str(labor_cost) )
        print("discount: " + str(labor_discount) )
        print("shipping: " + str(shipping))
        print( "total: " + truncate(total_price))

class styles(App):
    def build(self):
        return StylesLayout()

if __name__ == "__main__":
    styles().run()