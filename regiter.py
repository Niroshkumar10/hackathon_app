import kivy
import mysql.connector
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image

# Set window size
Window.size = (400, 600)

def create_connection():
    """Create a connection to the MySQL database."""
    return mysql.connector.connect(
        host='DESKTOP-MOAA7P3',  # Your host
        user='root',              # Your MySQL username
        password='12345',         # Your MySQL password
        database='safeapp'        # Your database name
    )

def insert_user(userrid, username, gender, contact, favoritecontact, locationid):
    """Insert user details into the database."""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (userrid, username, gender, contact, favoritecontact, locationid)
                          VALUES (%s, %s, %s, %s, %s, %s)''',
                       (userrid, username, gender, contact, favoritecontact, locationid))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def register_user(username, password):
    """Insert login credentials into the database."""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO logins (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def verify_login(username, password):
    """Verify login credentials."""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM logins WHERE username=%s AND password=%s', (username, password))
        user = cursor.fetchone()
        return user is not None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_car_details():
    """Fetch car details from the database."""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT carid, carownername, carno, carmodel FROM cardetails')
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def send_alert_message(contact):
    """Simulate sending an alert message."""
    print(f"Alert sent to {contact}: You are in a risk place!")

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Image(source='logo.png', size_hint=(1, 0.4)))  # Adjust size as necessary
        layout.add_widget(Label(text='Welcome to Women Travel Safety App', font_size='24sp', color=(1, 0.5, 0, 1), size_hint_y=None, height=40))
        layout.add_widget(Button(text='Register', background_color=(0.2, 0.6, 0.8, 1), size_hint_y=None, height=50, on_press=lambda x: setattr(self.manager, 'current', 'register')))
        layout.add_widget(Button(text='Login', background_color=(0.2, 0.6, 0.8, 1), size_hint_y=None, height=50, on_press=lambda x: setattr(self.manager, 'current', 'login')))
        self.add_widget(layout)

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Register', font_size='24sp', color=(1, 0.5, 0, 1), size_hint_y=None, height=40))
        self.username = TextInput(hint_text='Username', size_hint_y=None, height=40)
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=40)
        
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(Button(text='Register', on_press=self.register, size_hint_y=None, height=50))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home'), size_hint_y=None, height=50))
        
        self.add_widget(layout)

    def register(self, instance):
        username = self.username.text
        password = self.password.text
        
        register_user(username, password)

        # Clear inputs
        self.username.text = ''
        self.password.text = ''

        popup = Popup(title='Success', content=Label(text='User Registered Successfully!'), size_hint=(0.5, 0.5))
        popup.open()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Login', font_size='24sp', color=(1, 0.5, 0, 1), size_hint_y=None, height=40))
        self.username = TextInput(hint_text='Username', size_hint_y=None, height=40)
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=40)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(Button(text='Login', on_press=self.login, size_hint_y=None, height=50))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home'), size_hint_y=None, height=50))
        self.add_widget(layout)

    def login(self, instance):
        username = self.username.text
        password = self.password.text
        
        if verify_login(username, password):
            self.manager.current_user = username  # Store current user
            popup = Popup(title='Success', content=Label(text='Login Successful!'), size_hint=(0.5, 0.5))
            popup.open()
            setattr(self.manager, 'current', 'home_after_login')
        else:
            popup = Popup(title='Error', content=Label(text='Invalid Credentials!'), size_hint=(0.5, 0.5))
            popup.open()

class HomeAfterLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Welcome Back!', font_size='24sp', color=(1, 0.5, 0, 1), size_hint_y=None, height=40))
        layout.add_widget(Button(text='Book Taxi', background_color=(0.2, 0.8, 0.4, 1), size_hint_y=None, height=50, on_press=lambda x: setattr(self.manager, 'current', 'book_taxi')))
        layout.add_widget(Button(text='Send Emergency Alert', background_color=(0.8, 0.2, 0.4, 1), size_hint_y=None, height=50, on_press=self.check_location_and_alert))
        layout.add_widget(Button(text='Notify Trusted Contacts', background_color=(0.8, 0.8, 0.2, 1), size_hint_y=None, height=50, on_press=lambda x: setattr(self.manager, 'current', 'notify_contacts')))
        layout.add_widget(Button(text='Logout', background_color=(0.8, 0.6, 0.2, 1), size_hint_y=None, height=50, on_press=self.logout))
        self.add_widget(layout)

    def check_location_and_alert(self, instance):
        # Simulating location check
        user_location = "Pollachi"  # Assume user is in Pollachi
        if user_location == "Pollachi":
            send_alert_message(self.manager.current_user)  # Send alert message
            popup = Popup(title='Alert', content=Label(text='Alert sent: You are in a risk place!'), size_hint=(0.5, 0.5))
            popup.open()
        else:
            popup = Popup(title='Info', content=Label(text='You are safe.'), size_hint=(0.5, 0.5))
            popup.open()

    def logout(self, instance):
        self.manager.current_user = None  # Clear current user
        setattr(self.manager, 'current', 'home')

class BookTaxiScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Available Cars', font_size='24sp', color=(1, 0.5, 0, 1), size_hint_y=None, height=40))

        # Fetch car details
        self.car_details = fetch_car_details()
        self.dropdown = DropDown()

        for car in self.car_details:
            car_info = f"{car[1]} - {car[2]} ({car[3]})"  # carownername - carno (carmodel)
            btn = Button(text=car_info, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.mainbutton = Button(text='Select a Car', size_hint_y=None, height=40)
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))

        layout.add_widget(self.mainbutton)
        layout.add_widget(Button(text='Book Selected Car', on_press=self.book_car, size_hint_y=None, height=50))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home_after_login'), size_hint_y=None, height=50))
        self.add_widget(layout)

    def book_car(self, instance):
        selected_car = self.mainbutton.text
        if selected_car == 'Select a Car':
            popup = Popup(title='Error', content=Label(text='Please select a car!'), size_hint=(0.5, 0.5))
            popup.open()
        else:
            popup = Popup(title='Success', content=Label(text=f'You booked: {selected_car}'), size_hint=(0.5, 0.5))
            popup.open()

class SendAlertScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Send Emergency Alert', font_size='24sp', color=(1, 0.5, 0, 1), size_hint_y=None, height=40))
        layout.add_widget(Button(text='Send Alert', on_press=self.send_alert, size_hint_y=None, height=50))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home_after_login'), size_hint_y=None, height=50))
        self.add_widget(layout)

    def send_alert(self, instance):
        # Placeholder for alert logic
        popup = Popup(title='Alert', content=Label(text='Emergency Alert Sent!'), size_hint=(0.5, 0.5))
        popup.open()

class NotifyContactsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='Notify Trusted Contacts', font_size='24sp', color=(1, 0.5, 0, 1), size_hint_y=None, height=40))
        layout.add_widget(Button(text='Notify Contacts', on_press=self.notify_contacts, size_hint_y=None, height=50))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home_after_login'), size_hint_y=None, height=50))
        self.add_widget(layout)

    def notify_contacts(self, instance):
        popup = Popup(title='Notification', content=Label(text='Contacts Notified!'), size_hint=(0.5, 0.5))
        popup.open()

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeAfterLoginScreen(name='home_after_login'))
        sm.add_widget(BookTaxiScreen(name='book_taxi'))
        sm.add_widget(SendAlertScreen(name='send_alert'))
        sm.add_widget(NotifyContactsScreen(name='notify_contacts'))
        return sm

if __name__ == '__main__':
    MyApp().run()
