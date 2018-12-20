import unittest
import json
import users_contact
import random
import string
import requests

class Test_Users_Contact(unittest.TestCase):

    def test_add_contact(self):
        print(">>>>Testing add contact method<<<<<")
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        data = {}
        data['name'] = random_string
        data['contact'] = 12323222
        response = requests.post("http://localhost:8080/contact", json=data)
        print(response.text)
        success_sting = json.dumps({'success': True})
        self.assertEqual(response.text, success_sting)

    def test_get_contact(self):
        print(">>>>Testing get contact method<<<<<<")
        users_exists_string = json.dumps({'success': False, 'message': 'Sorry, the user already exists'}, 200,
                          {'ContentType': 'application/json'})

        successful_user = json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        user_not_found = json.dumps({'Success':False, 'message': 'User not found'}, 200, {'Content-Type':False})

        randomName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

        response = json.loads(users_contact.get_contact("Pranav"))
        self.assertEqual(users_contact.get_contact(randomName), user_not_found)
        self.assertTrue(response)

    def test_update_contact(self):
        print(">>>>>Testing update contact method<<<<<<")
        users_exists_string = json.dumps({'success': False, 'message': 'Sorry, the requested user doesn\'t exists'}, 200,
                          {'ContentType': 'application/json'})
        randomName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        self.assertEqual(users_contact.update_contact(randomName), users_exists_string)
    def test_delete_contact(self):
        user_exits_string = json.dumps({'success': False, 'message': 'Sorry, the requested user doesn\'t exists'}, 200,
                          {'ContentType': 'application/json'})

        randomName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        self.assertEqual(users_contact.delete_contact(randomName), user_exits_string)


if __name__ == '__main__':
    unittest.main()