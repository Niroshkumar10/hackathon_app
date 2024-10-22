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

# Set window size
Window.size = (400, 600)

def create_connection():
    """Create a connection to the MySQL database."""
    return mysql.connector.connect(
        host='DESKTOP-MOAA7P3',   # Your host
        user='root',               # Your MySQL username
        password='12345',          # Your MySQL password
        database='safeapp'         # Your database name
    )

def insert_user(userrid, username, gender, contact, favoritecontact, locationid):
    """Insert user details into the database."""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (userrid, username, gender, contact, favoritecontact, locationid)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (userrid, username, gender, contact, favoritecontact, locationid))
        conn.commit()
        print("User details inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Welcome to Women Travel Safety App', font_size='24sp', color=(1, 0.5, 0, 1)))
        layout.add_widget(Button(text='Login', background_color=(0.2, 0.6, 0.8, 1), on_press=lambda x: setattr(self.manager, 'current', 'login')))
        layout.add_widget(Button(text='Book Taxi', background_color=(0.2, 0.8, 0.4, 1), on_press=lambda x: setattr(self.manager, 'current', 'book_taxi')))
        layout.add_widget(Button(text='Send Emergency Alert', background_color=(0.8, 0.2, 0.4, 1), on_press=lambda x: setattr(self.manager, 'current', 'send_alert')))
        layout.add_widget(Button(text='Notify Trusted Contacts', background_color=(0.8, 0.8, 0.2, 1), on_press=lambda x: setattr(self.manager, 'current', 'notify_contacts')))
        layout.add_widget(Button(text='Add User', background_color=(0.8, 0.6, 0.2, 1), on_press=lambda x: setattr(self.manager, 'current', 'add_user')))
        self.add_widget(layout)

class AddUserScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.userrid = TextInput(hint_text='User ID', size_hint_y=None, height=40)
        self.username = TextInput(hint_text='Username', size_hint_y=None, height=40)
        self.gender = TextInput(hint_text='Gender (Male/Female/Other)', size_hint_y=None, height=40)
        self.contact = TextInput(hint_text='Contact', size_hint_y=None, height=40)
        self.favoritecontact = TextInput(hint_text='Favorite Contact', size_hint_y=None, height=40)
        self.locationid = TextInput(hint_text='Location ID', size_hint_y=None, height=40)
        
        layout.add_widget(self.userrid)
        layout.add_widget(self.username)
        layout.add_widget(self.gender)
        layout.add_widget(self.contact)
        layout.add_widget(self.favoritecontact)
        layout.add_widget(self.locationid)
        
        layout.add_widget(Button(text='Add User', on_press=self.add_user))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home')))
        
        self.add_widget(layout)

    def add_user(self, instance):
        userrid = self.userrid.text
        username = self.username.text
        gender = self.gender.text
        contact = self.contact.text
        favoritecontact = self.favoritecontact.text
        locationid = self.locationid.text
        
        insert_user(userrid, username, gender, contact, favoritecontact, locationid)

        # Clear inputs
        self.userrid.text = ''
        self.username.text = ''
        self.gender.text = ''
        self.contact.text = ''
        self.favoritecontact.text = ''
        self.locationid.text = ''

        popup = Popup(title='Success', content=Label(text='User Added Successfully!'), size_hint=(0.5, 0.5))
        popup.open()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.username = TextInput(hint_text='Username', size_hint_y=None, height=40)
        self.password = TextInput(hint_text='Password', password=True, size_hint_y=None, height=40)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(Button(text='Login', on_press=self.login))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home')))
        self.add_widget(layout)

    def login(self, instance):
        username = self.username.text
        password = self.password.text
        
        # Connect to the MySQL database
        conn = create_connection()
        cursor = conn.cursor()

        # Check for the user (replace with your own table logic)
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            popup = Popup(title='Success', content=Label(text='Login Successful!'), size_hint=(0.5, 0.5))
            popup.open()
        else:
            popup = Popup(title='Error', content=Label(text='Invalid Credentials!'), size_hint=(0.5, 0.5))
            popup.open()

class BookTaxiScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Book a Taxi', font_size='24sp', color=(1, 0.5, 0, 1)))
        layout.add_widget(Label(text='This feature is under construction.'))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home')))
        self.add_widget(layout)

class SendAlertScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Send Emergency Alert', font_size='24sp', color=(1, 0.5, 0, 1)))
        layout.add_widget(Button(text='Send Alert', on_press=self.send_alert))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home')))
        self.add_widget(layout)

    def send_alert(self, instance):
        popup = Popup(title='Alert', content=Label(text='Emergency Alert Sent!'), size_hint=(0.5, 0.5))
        popup.open()

class NotifyContactsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Notify Trusted Contacts', font_size='24sp', color=(1, 0.5, 0, 1)))
        layout.add_widget(Button(text='Notify Contacts', on_press=self.notify_contacts))
        layout.add_widget(Button(text='Back to Home', on_press=lambda x: setattr(self.manager, 'current', 'home')))
        self.add_widget(layout)

    def notify_contacts(self, instance):
        popup = Popup(title='Notification', content=Label(text='Contacts Notified!'), size_hint=(0.5, 0.5))
        popup.open()

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AddUserScreen(name='add_user'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(BookTaxiScreen(name='book_taxi'))
        sm.add_widget(SendAlertScreen(name='send_alert'))
        sm.add_widget(NotifyContactsScreen(name='notify_contacts'))
        return sm

if __name__ == '__main__':
    MyApp().run()
