import numpy as np
from numpy import sqrt, log as ln, linspace
from matplotlib import pyplot as plt
from pprint import pprint


def main():
    
    def approx_ln(x,n):
        """
            Approximates `ln(x)` using the algorithm described by B.C. Carlsson.\n

            `x`: The value of which to approximate the natural logarithm. Must be greater than 0.

            `n`: The number of iterations for the computations of the algorithm. A greater `n` results in a more accurate approximation.
        """
        # X must be greater than 0, or else the code should not be run.
        if not x < 0:
            # Initialize a value a_0 and g_0 and initialize an error value.
            a = (1+x)/2
            g = sqrt(x)
            # For every step...
            for i in range(1,n+1):

                # Make a_i+1 equal to (a_i + g_i) / 2 and g_i+1 to be sqrt(a_i+1 * g_i)
                next_a = (a + g)/2
                next_g = sqrt(next_a * g)
                
                # Assign the previously calculated a_i+1/g_i+1 values to be a_i/g_i,
                # so that they will be used in the next iteration.
                a = next_a
                g = next_g

            # Calculate the approximation and return the result and error
            approx = (x-1)/a
            err = abs(approx - ln(x))
            return approx, err

        else:
            # Raise an error if x is not greater than 0.
            raise ValueError("Input must be greater than 0.")
    
    def fast_approx_ln(x,n):
        """
            Approximates `ln(x)` using the accelerated algorithm described by B.C. Carlsson.\n

            `x`: The value of which to approximate the natural logarithm. Must be greater than 0.

            `n`: The number of iterations for the computations of the algorithm. A greater `n` results in a more accurate approximation.
        """
        if not x < 0:
            def a(x,n):
                # Initialize a_0, g_0
                a = (1+x)/2
                g = sqrt(x)

                for i in range(n):
                    # Make a_i+1 equal to (a_i + g_i) / 2 and g_i+1 to be sqrt(a_i+1 * g_i)
                    next_a = (a+g)/2
                    next_g = sqrt(next_a*g)
                    
                    # Assign the previously calculated a_i+1/g_i+1 values to be a_i/g_i,
                    # so that they will be used in the next iteration.
                    a = next_a
                    g = next_g
                
                return a

            # For the fast_approx_ln, it is apparent from the description of the method, that it concerns
            # a recursive methods of approximation. Therefore, a function d() is made, that will calculate
            # the value, by calling itself, with k being a value from 1 to n and i from 0 to n.
            def d(x,k,i):
                # Like the method described, for k = 0, we want to simply return a_i.
                if k == 0:
                    return a(x,i)
                # Else, use the formula as decsribed for the accelerated method.
                else:
                    return (d(x,k-1,i)-(4**(-k))*(d(x,k-1,i-1)))/(1-4**(-k))

            # Calculate the approximation and return the result and error
            approx = (x-1)/d(x,n,n)
            err = abs(ln(x) - approx)
            return approx, err
        
        else:
            # Raise an error if x is not greater than 0.
            raise ValueError("Input must be greater than 0.")
    
    def task_1():
        """
            Approximates `ln(x)` using the algorithm described by B.C. Carlsson. A greater `n` results in a more accurate approximation.
        """
        # User input
        x = int(input("Please specify what x to approximate ln(x) for: "))
        n = int(input("Please specify a value for n (number of steps for approximation): "))
        
        # Run the algorithm & print results
        approx, err = approx_ln(x,n)
        print(f"----------------\nResults\n----------------\nApproximating: ln({x})\nIterations: {n}\nApproximation: {approx}\nError: {err}")
    
    def task_2():
        """
            Plots an approximation of ln(x) using `approx_ln()` against the actual function of ln(x).\n
            A higher `n` results in greater precision.
        """
        # Allow user to specify any values of x and n
        x = int(input("Please specify a range of x for the plot: "))
        n = int(input("Please specify the steps n for the algorithm: "))

        # Make the x axis more detailed by taking 1/10th steps between 0 and x.
        x_axis = linspace(1,x,(x*10))
        # Creating a list of approximation results, with their corresponding error, for every x in the x-axis.
        results = [approx_ln(x,n) for x in x_axis]
        # List of approximations of ln(x) from the previously calculated results.
        y_approx = [r[0] for r in results]
        #  List of ln(x) for every x in the x-axis.
        y_ln = [ln(x) for x in x_axis]

        # Show approx_ln() and ln(x) plotted against the x-axis.
        plt.subplot(1,2,1)
        plt.plot(x_axis, y_approx, label=f"Approx. for ln(x) with n = {n}")
        plt.plot(x_axis, y_ln, label="ln(x)")
        plt.xlabel("x")
        plt.ylabel("ln(x)")
        plt.legend()

        # Create a list of the errors, retrieved from the results list.
        y_err = [r[1] for r in results]

        # Show the error plotted against the x-axis.
        plt.subplot(1,2,2)
        plt.plot(x_axis, y_err, label=f"|approx_ln(x)-ln(x)| with n = {n}")
        plt.xlabel("x")
        plt.ylabel("Error of approximation")
        plt.legend()
        
        plt.show()

    def task_3():
        """
            Plots the error of approx_ln(1.41,n) against a certain integer n.
        """
        # User input & setting x to 1.41.
        n = int(input("Please specify the steps n for the algorithm: "))
        x = 1.41

        # Let the x-axis be the values of n.
        x_axis = linspace(1,n,n)
        # Create a list of y-values for the error of approx_ln() of x = 1.41
        y_err = [approx_ln(x,i)[1] for i in range(1,n+1)]

        # Show the error of approximation for x = 1.41 plotted against n.
        plt.plot(x_axis, y_err, label="Error of approximation of ln(1.41)")
        plt.xlabel("n number of steps in the algorithm")
        plt.legend()
        plt.show()
    
    def task_4():
        """
            Approximates `ln(x)` using the accelerated B.C. Carlsson method. A greater `n` results in a more accurate approximation.
        """
        # User input
        x = int(input("Please specify what x to approximate ln(x) for: "))
        n = int(input("Please specify a value for n (number of steps for approximation): "))
        
        # Run the fast approximation algorithm & print results
        approx, err = fast_approx_ln(x,n)
        print(f"----------------\nResults\n----------------\nApproximating: ln({x})\nIterations: {n}\nApproximation: {approx}\nError: {err}")
    
    def task_5():
        """
           For the n values 2 to 5, and x from 1 to 20, this function plots
           the error of approximation of `fast_approx_ln(x,n)` on a logarithmic scale.
        """
        # Set a linspace from 1 to 20, with 1/10th steps of detail between every integer of x.
        x = linspace(1,21,200)

        # For 2 to 5 iterations (n), plot the error value of fast_approx_ln(x,n).
        # The x axis is what is being approximated. So one will obtain 4 graphs for
        # n in [2,5] for x values of 1 to 20.
        for n in range(2,6):
            plt.plot(x, [fast_approx_ln(x,n)[1] for x in range(200)], label=f"{n} iterations")
        
        # Observing the graph in the task description, it is clearly a logarithmic scale on the y-axis.
        plt.yscale("log")

        # Show legend and assign labels/titles, and show the graph.
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("Error")
        plt.title("Error behavior of accelerated Carlsson method for the natural log")
        plt.show()

    # This part of the code will run any individual task based on user input in the terminal.
    run = True
    print('----------------')
    # As long as the program needs to run, keep the while loop running.
    while run:
        query = input("Select task to run or type stop to quit: ")

        if query == 'stop':
            print("----------------\nQuitting program!\n----------------")
            run = False
        
        # Run one of the 5 tasks based on user input.
        elif query in ['1','2','3','4','5']:
            print(f"----------------\nTask {query} starting\n----------------")
            if query == '1':
                task_1()
            elif query == '2':
                task_2()
            elif query == '3':
                task_3()
            elif query == '4':
                task_4()
            elif query == '5':
                task_5()
            print(f"----------------\nTask {query} finished!\n----------------")
        else:
            print(f"----------------\nInvalid input!\n----------------")

# Run main code
main()