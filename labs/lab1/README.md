Grader Comment:
```
Compile with error messages:

0





FFF
======================================================================
FAIL: testP1 (__main__.TestCases)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "lab1.py", line 133, in testP1
    self.assertEqual(sarah.info(), "Sarah works in the Engineering department")
AssertionError: None != 'Sarah works in the Engineering department'

======================================================================
FAIL: testP2 (__main__.TestCases)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "lab1.py", line 145, in testP2
    self.assertEqual(marketing.name, "Marketing")
AssertionError: None != 'Marketing'

======================================================================
FAIL: testP3 (__main__.TestCases)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "lab1.py", line 156, in testP3
    self.assertEqual(manager_sarah.manager_info(), "Sarah works in the Engineering department with manager id: " + str(9167766))
AssertionError: None != 'Sarah works in the Engineering department with manager id: 9167766'

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=3)
```
Grade:
```
Not Passed
```

# Basic OOP in Python
In this lab, your learn the basics of OOP in python. The conceots learned in this lab are really helpful for your projects
in this class. In this lab, you'll learn how to create classes and how the classes can inherit data from others. 

In this lab unit tests are provided to check that your code performs according to specifications. In order to get a 
passing grade in this lab, your code must pass all the unit tests provided. 

Do not modify the unit tests provided. Modifying or hardcoding unit tests will be penalized with a bad grade in this lab. 

## Note: This is a take home lab. This lab is due on Feb 03 before class. 
