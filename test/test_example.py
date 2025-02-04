def test_str():
	assert str(1) == "1"
	assert 'Hello' != "World"


class Student:
	def __init__(self, first_name,last_name, phone_number):
		self.first_name = first_name
		self.last_name = last_name
		self.phone_number = phone_number

def test_people():
	p = Student("Ketmon","Teshaboyev","993561212")
	assert p.first_name == "Ketmon"
	assert p.last_name == "Teshaboyev"
	assert p.phone_number == "993561212"
