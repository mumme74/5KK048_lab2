# Answers to tasks in lab2 primarily Task j
This is my attempt to resolve the tasks in lab2 (version control)

# This is a heading

## This is a subheading

## List
1. item one
2. item two
3. item three
   - bullet list 1
 
## Datetime module (task j (I))
You can read more about the datetime module for python at python docs.
Python [datetime](https://docs.python.org/3/library/datetime.html)

# Explicit type conversion (task j (II))
The word explict means that something is clearly expressed, as opposed to implicit which is more "read between the lines".
Therefore explicit type conversion means that you clearly express what type you want a variable to be.

example:
```python3
# implict type
three = 3.0 # will implicitly get float type

# explicit type
pi = float("3.14159265") # explicitly stating that pi variable is float type
```

# Task l 
## Describe a datetime module part (I):
I choosed the [timedelta](https://docs.python.org/3/library/datetime.html#timedelta-objects)

The timedelta object is part of datetime module. It is used to represent a time duration, aka difference between to date or datetime instances.

Let say we want the time exacly 3 weeks ago. We could get that date using code below.
```python3
from datetime import datetime, timedelta
weeks = timedelta(weeks=-3) # go back 3 week
date_obj = datetime.now() + weeks # adding negative 21days (-3 weeks)
print(date_obj)

```

## Practical example of explicit type conversion (II)
To do an explicit type conversion you have to do an explict typecast.
example:
```python
s = str(123) # convert to a string
i = int("1") # convert to an integer
f = float("2.71828182846")
```

## Whats the origin of the modules in task g?
- wordrain (external lib, install through anaconda)
- numpy  (external lib, install through pip or anaconda)
- scipy  (external lib, install through pip or anaconda)
- scikit-learn (external lib, install through pip or anaconda)
- gensim (external lib, install through pip or anaconda)
- nltk   (external lib, install through pip or anaconda)
- matplotlib (external lib, install through pip or anaconda)
- python-bidi (external lib, install through pip or anaconda)
- reportlab (external lib, install through pip or anaconda)
- math   (standard/builtin module)
- typing (standard/builtin module)
- os     (standard/builtin module)
- json   (standard/builtin module)
- pickle (standard/builtin module)
- sys    (standard/builtin module)


