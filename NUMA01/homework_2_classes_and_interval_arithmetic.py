import inspect, numpy as np
from matplotlib import pyplot as plt

# Task 6
def inf_check(interval):
    for value in vars(interval).values(): # Check all the attributes of the interval object.
        if value == float('inf'):
            return True # If a value is equal to infinity, the check returns True.
        else:
            pass
    return False # If no infinity is found, the check fails and returns False.

# Task 1 - Construct the class
class Interval:
    
    def __init__(self,left,right=None): # 1: left & right value for object
        
        if right == None: # Right value defaults to None, if it's the case..
            right = left # Then only left value was entered. Make right = left, degenerative interval

        try:
            check = lambda x: float(x) if not (type(x) == int) else x
            left = check(left)
            right = check(right)
        except: # If float is not possible, and the type is not int, then it's not a real number.
            raise ValueError("The values for either the left or right endpoints was not a real number.")
        
        self.left = left # Assign input to the corresponding attributes of the object instance.
        self.right = right # Assign input to the corresponding attributes of the object instance.

    # Task 2 - Provide methods for the 4 basic arithmetic operations
    """
        For these methods, I used variable 'b' to signify the second object/integer
        in the arithmetic operations (a+b),(a-b),(a*b),(a/b).
    """
    def __add__(self, b):
        # Task 8 - Adjust the code to allow operations with real numbers
        if not inspect.isclass(b) and type(b) in (float,int): # If b is not a class and it's a real number,
            b = Interval(b,b) # Create a degenerative interval for b.

        res = Interval((self.left+b.left),(self.right+b.right)) # [a,b]+[c,d] = [a+c,b+d]
        
        if not inf_check(res): 
            return res # If the infinity check fails, return the result.
        else:
            raise ValueError("Either end of the interval is infinity.") # Otherwise raise error.

    def __sub__(self, b):
        if not inspect.isclass(b) and type(b) in (float,int):
            b = Interval(b,b)
        
        res = Interval((self.left-b.right),(self.right-b.left)) # [a,b]-[c,d] = [a-d,b-c]
        
        if not inf_check(res):
            return res
        else:
            raise ValueError("Either end of the interval is infinity.")

    def __mul__(self, b):
        if not inspect.isclass(b) and type(b) in (float,int):
            b = Interval(b,b)

        # Creating a list of a*c, a*d, b*c, b*d & finding the minimum and maximum
        # [a,b]*[c,d] = [min(ac,ad,bc,bd),max(ac,ad,bc,bd)]
        ls = [self.left*b.left, self.left*b.right, self.right*b.left, self.right*b.right]
        res = Interval(min(ls), max(ls))
        
        if not inf_check(res):
            return res
        else:
            raise ValueError("Either end of the interval is infinity.")

    def __truediv__(self, b):
        if not inspect.isclass(b) and type(b) in (float,int):
            b = Interval(b,b)

        if not b.left == 0 and not b.right == 0: # TASK 6 Division by zero check.
            # Creating a list of a/c, a/d, b/c, b/d & finding the minimum and maximum
            # [a,b]/[c,d] = [min(a/c,a/d,b/c,b/d),max(a/c,a/d,b/c,b/d)]   
            results = [self.left/b.left, self.left/b.right, self.right/b.left, self.right/b.right]
            res = Interval(min(results), max(results))
            
            if not inf_check(res):
                return res
            else:
                raise ValueError("Either end of the interval is infinity.")
        else:
            raise ValueError("A division by zero occured.") # If any division by 0, raise error.
    
    # Task 8 - Adjust the code to allow operations with real numbers
    """
        To allow operations where the real number percedes the Interval object,
        I chose to add the 'reverse' arithmetic methods to the class. Now, if
        one types '1 + Interval(a,b)', the code will not throw an error.
        Rather, it will 'flip' the Interval object and the number, then treating the
        Interval object as 'self' and the number as 'b'.
    """
    def __radd__(self, b):
        if not inspect.isclass(b) and type(b) in (float,int):
            b = Interval(b,b)

        res = Interval((self.left+b.left),(self.right+b.right)) # The order for addition does not matter.
        
        if not inf_check(res):
            return res
        else:
            raise ValueError("Either end of the interval is infinity.")

    def __rsub__(self, b):
        if not inspect.isclass(b) and type(b) in (float,int):
            b = Interval(b,b)
        
        # IMPORTANT: for the reverse sub, we must flip the self left/right and the b left/right,
        # Since in subtraction the order of numbers matters.
        res = Interval((b.left-self.right),(b.right-self.left))
        
        if not inf_check(res):
            return res
        else:
            raise ValueError("Either end of the interval is infinity.")

    def __rmul__(self, b):
        if not inspect.isclass(b) and type(b) in (float,int):
            b = Interval(b,b)

        ls = [self.left*b.left, self.left*b.right, self.right*b.left, self.right*b.right]
        res = Interval(min(ls), max(ls))
        
        if not inf_check(res):
            return res
        else:
            raise ValueError("Either end of the interval is infinity.")
    
    # Task 9 - Implement the power function
    def __pow__(self, b):

        if type(b) in (float,int): # Check whether b is a real number.

            res = Interval(self.left**b,self.right**b)
            
            if not inf_check(res):
                return res
            else:
                raise ValueError("Either end of the interval is infinity.")
        else:
            raise ValueError("The power was not a real number.") # If not b in R, raise error.
    
    # Task 3 - Provide a print method so that the code prints [a,b]
    """
       A __repr__ method will work perfectly fine here. I created a string representation
       Of a list of the attributes of the Interval object to achieve this.
    """
    def __repr__(self):
        return str(list(vars(self).values()))

    # Task 5 - Create a __contains__ method to check if a number is in an interval.
    """
        This is fairly trivial. A simple inequality works here. If the number is larger
        than the left interval but smaller than the right, it is contained in the interval.
        It will return True if the inequality holds, else it returns False.
    """
    def __contains__(self,num):
        if self.left <= num <= self.right:
            return True
        else:
            return False

def task_3(): # Task 3 testing. (Also 1 and 2)
    print(Interval(1,3))

def task_4(): # Task 4 testing.
    int_1 = Interval(1,4)
    int_2 = Interval(-2,-1)
    print(f"Intervals: a:{int_1}, b:{int_2}")
    print(f"(a+b): {int_1+int_2}")
    print(f"(a-b): {int_1-int_2}")
    print(f"(a*b): {int_1*int_2}")
    print(f"(a/b): {int_1/int_2}")

def task_5(): # Task 5 testing.
    int_1 = Interval(1,4)
    int_2 = Interval(-2,-1)
    print(f"2 is part of {int_1}: {2 in int_1}")
    print(f"7 is part of {int_1}: {7 in int_1}")
    print(f"-1.01 is part of {int_2}: {-1.01 in int_2}")
    print(f"0 is part of {int_2}: {0 in int_2}")

def task_6(): # Task 6 testing.
    int_1 = Interval(1,0)
    int_2 = Interval(1e500,4)
    
    try:
        print(int_1+int_2)
    except ValueError as err:
        print("ValueError: "+str(err))
    
    try:
        print(int_2/int_1)
    except ValueError as err:
        print("ValueError: "+str(err))

def task_7(): # Task 7 testing.
    print(Interval(1))

def task_8(): # Task 8 testing.
    print(Interval(2,3)+1)
    print(1+Interval(2,3))
    print(1.0+Interval(2,3))
    print(Interval(2,3)+1.0)
    print(1-Interval(2,3))
    print(Interval(2,3)-1)
    print(1.0-Interval(2,3))
    print(Interval(2,3)-1.0)
    print(Interval(2,3)*1)
    print(1*Interval(2,3))
    print(1.0*Interval(2,3))
    print(Interval(2,3)*1.0)

def task_9(): # Task 9 testing.
    x = Interval(-2,2) 
    print(x**2,x**3)

def task_10(): # Task 10 testing.
    # Creating a list of 1000 intervals (a,a+0.5) for a in [0,1]
    ints_x = [Interval(a,a+0.5) for a in np.linspace(0,1,1000)]
    # Creating a list of p(I)=3I^3-2I^2-5I-1 for the list of intervals.
    ints_y = [((3*(a**3))-(2*(a**2))-(5*a)-1) for a in ints_x]

    # Plotting lower & upper y bounds (y_l and y_u) against only the lower bound of
    # the x-values (i.e. the left end of the interval.)
    plt.plot([a.left for a in ints_x], [a.left for a in ints_y])
    plt.plot([a.left for a in ints_x], [a.right for a in ints_y])

    # Labels & show graph.
    plt.title("p(I)=3I^3-2I^2-5I-1, I = Interval(x,x+0.5)")
    plt.xlabel("x")
    plt.ylabel("p(I)")
    plt.show()

# Some code to be able to select any task to run.
def main():

    run = True
    while run:
        txt = input('----------\nSelect a task to run: ')
        print("----------")
        if txt == 'stb':
            run = False
        else:
            if int(txt) in range(3,11):
                exec(f"task_{txt}()")
            else:
                print("Invalid task.")

main()