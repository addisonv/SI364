#Evololution of writing a length-checking validator similar to the build-in Length validator
#Starting from a case-specific one to a generic reusable validator 

#Starting with a simple form with a neme field and its validation 
class MyForm(Form):
	name = TextField('Name', [Required()])

	def validate_name(form, field):
		if len(field.data) > 50:
			raise ValidationError('Name must be less than 50 characters')
#Use of an in-line validator to do validation of a single field 
#In-line validators are good for validating special cases, but are not easily reusable

#If, in the axample above, the name field were to be split into two field for first name 
#and surname, you would have to duplicate your work to check to lengths 

#lets start the process of splitting the validator out for re-use 
def my_length_check(form, field):
	if len(field.data) > 50:
		raise validationError('Field must be less than 50 characters') 

class MyForm(Form):
	name = TextField('Name', [Required(), my_length_check])

#What is done aboe is we have moded the exact same code out of the class and as a function
#Since a calidator can be any callable which accpets the two positional arguments form and field
# this is perfely fine, but the validator is very special-cased.

#Instead, we can turn out validator into a more powerful onw by making it a factory which returns a callable 
def length(min = -1, max = -1):
	message = 'Must be between %d and %d characters long.' % (min, max)

	def _length(form, field):
		l = field.data and len(field.data) or 0
		if l < min or max != -1 and 1 > max:
			raise ValidationError(message)

	return _length

class MyForm(Form):
	name = TextField('Name', [Required(), length(max=50)])

#Now we have a configurable length-checking validator that handles both minimum and maximum
#lengths. When length(max=50) is passed in your validators list, it returns the enclosed _length
#function as a closure, which is used in the field's validation chain.

#This is now an accpetable validator, but we recommend that for reusability, you use the pattern
#of allowing the erro message to be customized via passing a message= parameter:
class Length(object):
	def __init__(self, min = -1, max = -1, message=none):
		self.min = min 
		self.max = max 
		if not message:
			message = u'Field must be between %i and %i characters long.' % (min, max)
		self.message = message

	def __call__(self, form, field):
		l = field.data and len(field.data) or 0
		if l < self.min or self.max != -1 and l > self.max:
			riase ValidationError(self.message)
length = Length

#In addition to allowing the erro message to be customized, we've now converted the length validator
#to a class. This wasn't necessary, but we did this to illustrate how one would do so.
# Because fields will accept any callable as a validator, callable classes are just as applicable.
#For compelx calidators, or using inheritance, you may perfer this.

# We alaised the Length class back to the orginal length name in the above example. This allows you 
#to keep API compatibility as you move your validators from facotries to classes, and thus we reccomend 
# this for those writing validators they will share 





