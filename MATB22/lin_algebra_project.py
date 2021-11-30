import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import scipy.optimize

# Task 1 - Find the vector x in R^3 that minimizes ||Ax-b||
def task_1():
    A = np.array([[1, 1, 2],
                [1, 2, 1],
                [2, 1, 1],
                [2, 2, 1]])

    b = np.array([1, -1, 1, -1]) # Numpy interprets this as a column matrix.
    
    def min_x(A, b):
        '''
        (1.1) Solves normal equation A_t . A . x = A_t . b for x by:
            * Taking transpose of matrix A.
            * Taking the dot products A_t . A and A_t . b, and assign them new names B and C.
            * Returning linalg.solve(B,C) to find the solution for Bx = C.
        '''
        A_t = np.transpose(A)
        B = np.dot(A_t, A)
        C = np.dot(A_t, b)
        return np.linalg.solve(B, C)

    def min_x_norm(A, b, x_guess = [0, 0, 0]):
        '''
        (1.2) Finds the solution for ||Ax-b|| by:
            * Creating a lambda function f, which represents ||Ax-b|| in a programatical way.
            * Finding a suitable 'guess' for the algorithm, which is based on the result of min_x().
            * Use scipy.optimize.fmin() with the guess for x to solve for x
        '''

        f = lambda x: np.linalg.norm((np.dot(A, x) - b))
        return scipy.optimize.fmin(f, x_guess,disp=False)
    
    min_x_normal = min_x(A, b)
    min_x_scipy = min_x_norm(A, b)

    print(f"Task 1.1 - Using the normal equation A_t . A . x = A_t . b and solving for x, we obtain:\n{min_x_normal}\n")
    print(f"Task 1.2 - With scipy.optimize.fmin(), the x for which ||Ax-b|| is minimized is:\n{min_x_scipy}\n")
    print(f"Task 1.2 - The difference between the two is:\n{min_x_normal - min_x_scipy}\n")

    def r(a):
        '''
        (1.3) Creates a function representing the residual ||Ax(a) - b(a)|| by:
            * Using min_x() from 1.1 to minimize the new solution x dependent on input a.
            * Returning ||Ax(a)-b(a)||.
        '''
        b = [1, a, 1, a] # Numpy interprets this as a column matrix.
        x = min_x(A, b)
        return np.linalg.norm(np.dot(A, x) - b)

    x_axis = np.linspace(0,100,1000)
    y_axis = [r(a) for a in x_axis] # For every value a, take ||Ax(a)-b(a)|| using the r(a) fn.

    # Show the result of task 1.3.
    plt.plot(x_axis, y_axis)
    plt.xlabel("a")
    plt.ylabel("r(a)")
    plt.grid(color='black', linestyle='-', alpha=0.2)
    plt.title("Residual r(a) = ||Ax(a)-b(a)||")
    plt.show()

def task_2():
    A = np.array([[ 1,3,2],
                [-3,4,3],
                [ 2,3,1]])

    z_0 = np.array([8,3,12])

    def z_closed(n):
        '''
        (2.1) Returns z_n based on derived closed form (to be shown in presentation).
        '''
        e_1 = np.array([1,12,-19])
        e_2 = np.array([1,0,1])
        e_3 = np.array([3,1,3])
        return (-1)**(n+1) * 1/5 * e_1 - 3**n * 8 * e_2 + 4**n * 27/5 * e_3

    def v_n(n):
        '''
        (2.2) Function representation of v_n := z_n / ||z_n||
        '''
        z_n = z_closed(n)
        return z_n/np.linalg.norm(z_n)

    def q_n(n):
        '''
        (2.4) Returns q_n for every normalized iterate of v_n by:
            * Computing v_n for nth iterate.
            * Returning q_n where q_n = v_n^T A v_n
        '''
        v = v_n(n)
        return np.transpose(v).dot(A.dot(v))

    def iterates(a_n,a,epsilon):
        '''
        (2.6) Determines iterates necessary to satisfy an epsilon difference by:
            * Taking the norm ||v_n - v||.
            * Returning amount of iterates when the norm is less than epsilon.
        '''
        n = 0
        while True:
            if np.linalg.norm(a_n(n)-a) < epsilon:
                return n
            n += 1

    # (2.1) Check if z_n converges as n -> 'infinity' and print last result.
    z_vals = [ z_closed(n) for n in range(0, 200) ]
    print(f"Task 2.1 - As n → ∞, we have after 200 iterations that:\nz_n = {z_vals[-1]}")
    
    plt.plot(np.array(range(0,200)), [ np.linalg.norm(z) for z in z_vals ])
    plt.title("Graph of Z_n as n → ∞")
    plt.show()
   
    # (2.2) Determining numerically the value that v_n converges to.
    v_vals = [ v_n(n) for n in range(0,200) ]
    v = v_vals[-1]
    print(f"Task 2.2 - As n → ∞, v_n converges to {v}")
    
    # (2.2) Plot iterates of v_n
    X = [ v[0] for v in v_vals ]
    Y = [ v[1] for v in v_vals ]
    Z = [ v[2] for v in v_vals ]
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(X,Y,Z)
    ax.plot(X,Y,Z)
    plt.title(f"Iteration of v_n := z_n / ||z_n|| for n from 0 to {len(v_vals)}")
    plt.show()
    fig.clf() # clear figure

    # (2.4) Check limit of q_n as n -> 'infinity', and print last result.
    q_vals = [ q_n(n) for n in range(0,200) ]
    q = q_vals[-1]
    print(f"Task 2.4 - the limit of q as n -> inf is approximately {round(q,2)}.")

    # (2.6) Define epsilon from task and print result
    epsilon = 10**-8
    print(f"Task 2.6 - {iterates(v_n,v,epsilon)} iterations needed for ||v_n - v|| < ε")

    # (2.7) Set a range of epsilons between 10^-1 and 10^-14, and compute number of
    # iterates required for the result to be less than some epsilon in the range.
    epsilon_vals = 10**((-1)*np.linspace(1,14,1000))
    v_iterates = [ iterates(v_n,v,eps) for eps in epsilon_vals ]
    q_iterates = [ iterates(q_n,q,eps) for eps in epsilon_vals ]

    # (2.7) Plot the number of iterates of ||v_n-v|| and ||q_n-n|| against epsilon.
    plt.gca().invert_xaxis()
    plt.semilogx(epsilon_vals,v_iterates,label="||v_n - v|| < ε")
    plt.semilogx(epsilon_vals,q_iterates,label="||q_n - q|| < ε")
    plt.legend()
    plt.show()

def task_3():
    def f(x_1,x_2):
        '''
        (3b) Determines solution of x_3 for a given x_1 and x_2 by:
            * Defining g as the given function, but making RHS equal to 0 (for fsolve()).
            * Defining two reasonable initial values for the fsolve().
            * Return the result.
        '''
        g = lambda x_3 : 2*x_1**2 - x_2**2 + 2*x_3**2 - 10*x_1*x_2 - 4*x_1*x_3 + 10*x_2*x_3 - 1
        result_1 = scipy.optimize.fsolve(g,-10)
        result_2 = scipy.optimize.fsolve(g,10)
        return [result_1[0],result_2[0]]

    # (3.1) Setting some parameters for the 3D plot of the function.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.linspace(-1,1,20)
    y = np.linspace(-1,1,20)
    X,Y = np.meshgrid(x,y)

    Z_1 = []
    Z_2 = []

    # Below, we calculate z for all x-y combinations by looping over every y_coord
    # and then generating a list of z values for every x_coord in x.
    # This covers all possible x-y combinations of the plot.
    # zip(*z_coord_list) separates the two different z values of each coordinate into their own lists.
    
    z_coord_list = []
    for y_coord in y:
       z = [f(x_coord, y_coord) for x_coord in x]
       z_coord_list.append(zip(*z))
    Z_1, Z_2 = zip(*z_coord_list)
    
    # (3.1) Plot the surfaces
    Z_1 = np.array(Z_1)
    Z_2 = np.array(Z_2)

    ax.plot_surface(X,Y,Z_1)
    ax.plot_surface(X,Y,Z_2)

    plt.show()
    fig.clf()

# Main function to run all the tasks.
def main():
    task_list = [task_1, task_2, task_3]
    while True:
        try:
            i = int(input("Select the task to run! (0 to quit): "))
            # If task nr is valid, execute it and finish by clearing matplotlib figure.
            if i in range(1,4):
                task_list[i-1]()
            elif i == 0:
                break # Exits while loop & closes program.
            else:
                raise ValueError
        except:
            print("Invalid input!")

if __name__ == "__main__":
    main()
