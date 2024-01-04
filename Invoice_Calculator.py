from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

#Set the app size
Window.size = 300, 600

class InputWindow(Screen):
    red_color = [.7, 0, 0, 1]
    green_color = [0, .7, 0, 1]
    default_color = [0.1, 0.12, 0.22, 1]
    gray_color = [.5, .5, .5, 1]
    check_symbol = u"\u2713"
    cross_symbol = "X"

    def change_parts_button_state(self):
        if self.ids.one_part_button.state == "down":
            self.ids.one_part_button.back_color = self.green_color
            self.ids.two_parts_button.back_color = self.default_color
            self.ids.three_parts_button.back_color = self.default_color
        elif self.ids.two_parts_button.state == "down":
            self.ids.one_part_button.back_color = self.default_color
            self.ids.two_parts_button.back_color = self.green_color
            self.ids.three_parts_button.back_color = self.default_color
        elif self.ids.three_parts_button.state == "down":
            self.ids.one_part_button.back_color = self.default_color
            self.ids.two_parts_button.back_color = self.default_color
            self.ids.three_parts_button.back_color = self.green_color
        else:
            self.ids.one_part_button.back_color = self.default_color
            self.ids.two_parts_button.back_color = self.default_color
            self.ids.three_parts_button.back_color = self.default_color

    def change_repeat_customer_button_state(self):
            if self.ids.repeat_customer_button.state == "down":
                self.ids.repeat_customer_button.back_color = self.green_color
                self.manager.get_screen("output").ids.discount_label.color = self.green_color
                self.ids.repeat_customer_button.text = self.check_symbol
            else:
                self.ids.repeat_customer_button.back_color = self.default_color
                self.manager.get_screen("output").ids.discount_label.color = self.gray_color
                self.ids.repeat_customer_button.text = self.cross_symbol

    def change_shipping_button_state(self):
        if self.ids.shipping_button.state == "down":
            self.manager.get_screen("output").ids.shipping_label.color = self.green_color
            self.ids.shipping_button.back_color = self.green_color
            self.ids.shipping_button.text = self.check_symbol
        else:
            self.manager.get_screen("output").ids.shipping_label.color = self.gray_color
            self.ids.shipping_button.back_color = self.default_color
            self.ids.shipping_button.text = self.cross_symbol

    def change_worker_button_state(self):
            if self.ids.workers_button.state == "down":
                self.ids.workers_button.back_color = self.green_color
                self.ids.workers_button.text = self.check_symbol
                self.manager.get_screen("output").ids.labor_label.color = self.green_color

            else:
                self.ids.workers_button.back_color = self.default_color
                self.ids.workers_button.text = self.cross_symbol
                self.manager.get_screen("output").ids.labor_label.color = [1, 1, 1, 1]

    #logic
    def submit(self):
        try:
            #constants
            sellers_tax = 8.75
            multiplication_index = 8
            self.ids.submit_button.back_color = self.green_color
            self.ids.main_price.hint_text = "Enter the price:"
            
            #main price input
            main_price = float(self.ids.main_price.text)

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

            #truncation all numbers with .0
            def truncate(float_number):
                multiplier = 100
                return str(int(float_number * multiplier)/multiplier)

            #more than one part
            if self.ids.one_part_button.state == "down":
                self.manager.get_screen("output").ids.first_part_label.size_hint = 0, 0
                self.manager.get_screen("output").ids.second_part_label.size_hint = 0, 0
                self.manager.get_screen("output").ids.third_part_label.size_hint = 0, 0
                self.manager.get_screen("output").ids.parts_grid.size_hint = 0, 0
                self.manager.get_screen("output").ids.first_part_label.text = ""
                self.manager.get_screen("output").ids.second_part_label.text = ""
                self.manager.get_screen("output").ids.third_part_label.text = ""
            elif self.ids.two_parts_button.state == "down":
                first_part = float(total_parts_cost/100*60)
                second_part = float(total_parts_cost/100*40)
                third_part = 0
                self.manager.get_screen("output").ids.parts_grid.size_hint = 1, 1
                self.manager.get_screen("output").ids.first_part_label.size_hint = 1, .1
                self.manager.get_screen("output").ids.second_part_label.size_hint = 1, .1
                self.manager.get_screen("output").ids.third_part_label.size_hint = 0, 0

                self.manager.get_screen("output").ids.first_part_label.text =(
                    "First part cost: " + f"{truncate(first_part)}"
                )
                self.manager.get_screen("output").ids.second_part_label.text =(
                    "Second part cost: " + f"{truncate(second_part)}"
                )
                self.manager.get_screen("output").ids.third_part_label.text = ""
            elif self.ids.three_parts_button.state == "down":
                first_part = float(total_parts_cost/100*50)
                second_part = float(total_parts_cost/100*30)
                third_part = float(total_parts_cost/100*20)
                self.manager.get_screen("output").ids.parts_grid.size_hint = 1, 1
                self.manager.get_screen("output").ids.first_part_label.size_hint = 1, .1
                self.manager.get_screen("output").ids.second_part_label.size_hint = 1, .1
                self.manager.get_screen("output").ids.third_part_label.size_hint = 1, .1

                self.manager.get_screen("output").ids.first_part_label.text =(
                    "First part costs: " + f"{truncate(first_part)}"
                )
                self.manager.get_screen("output").ids.second_part_label.text =(
                    "Second part costs: " + f"{truncate(second_part)}"
                )
                self.manager.get_screen("output").ids.third_part_label.text =(
                    "Third part costs: " + f"{truncate(third_part)}"
                )
            else:
                self.manager.get_screen("output").ids.first_part_label.size_hint = 0, 0
                self.manager.get_screen("output").ids.second_part_label.size_hint = 0, 0
                self.manager.get_screen("output").ids.third_part_label.size_hint = 0, 0
                self.manager.get_screen("output").ids.parts_grid.size_hint = 0, 0
                self.manager.get_screen("output").ids.first_part_label.text = ""
                self.manager.get_screen("output").ids.second_part_label.text = ""
                self.manager.get_screen("output").ids.third_part_label.text = ""
            
            #output   
            self.manager.get_screen('output').ids.total_parts_cost_label.text = (
                "Total parts cost: " + f"{truncate(total_parts_cost)}"
            )
            self.manager.get_screen('output').ids.tax_label.text = "Tax: " + f"{truncate(part_tax)}"
            self.manager.get_screen('output').ids.labor_label.text = "Labor: " + f"{str(labor_cost)}"
            self.manager.get_screen('output').ids.discount_label.text = "Discount: " + f"{str(labor_discount)}"
            self.manager.get_screen('output').ids.shipping_label.text = "Shipping: " + f"{str(shipping)}"
            self.manager.get_screen('output').ids.total_label.text = "Total: " + f"{truncate(total_price)}"
        except:
            self.ids.main_price.hint_text = "!!!PRICE FIELD IS EMPTY!!!"
            self.ids.submit_button.back_color = self.red_color

class OutputWindow(Screen):
    pass
class WindowManager(ScreenManager):
    pass

#Designate .kv design file
class InvoiceCalculator(App):
    def build(self):
        return Builder.load_file('layout.kv')

if __name__ == "__main__":
    InvoiceCalculator().run()