'''This is original root founding program which implements Bisection method, and this program can work
properly from the tests.'''
from numpy import array
def bisect(target, f, start=None, bounds=None, tols=[0.001,0.010], maxtier=1000):
# first check whether supplied bounds
    # no bounds
    if bounds is None:
        x=100.0; a=start-x; b=start+x
        n = 1; c=[]
        while n <= maxtier:
            # find stopping step
            c.append((a+b)*0.5) # create a list for x values
            if abs(b - a) <= tols[0] or abs(f(c[n-1]) - target) <= tols[1]:
                return array(c),n  # Find root
            if f(c[n-1]) < target:
                a = c[n-1]
            if f(c[n-1]) > target:
                b = c[n-1]
            n +=1
        # after all iterations, still no solution
        try:
            raise
        except:
            print("There is no solution after all iteration")

    # When bounds aren't none
    # check the whether these bounds contain a solution
    if min(bounds[0], bounds[1],key=f)<= target <= max(bounds[0], bounds[1],key=f):
        a = bounds[0]; b = bounds[1]; n=1; c=[]
        # first iteration in start point
        if start is None:  # if don't input start point
            c.append((a + b) * 0.5)
        else:  # if input feasible start point
            c.append(start)
        if abs(b - a) <= tols[0] or abs(f(c[n-1]) - target) <= tols[1]:
            return array(c),n # Find root
        if f(c[n-1]) < target:
            a = c[n-1]
        if f(c[n-1]) > target:
            b = c[n-1]
        # start from second iteration
        n = 2
        while n <= maxtier:
            # find stopping step
            c.append((a + b) * 0.5)
            if abs(b - a) <= tols[0] or abs(f(c[n-1]) - target) <= tols[1]:
                return array(c),n # Find root
            if f(c[n-1]) < target:
                a = c[n-1]
            if f(c[n-1]) > target:
                b = c[n-1]
            n += 1
        try:
            raise
        except:
            print("There is no solution after all iteration")

    # no solution in the domain
    else:
        print('There is no solution in the domain, please input feasible bounds')

'Test bisect method only in this file'
if __name__ =='__main__':
    f = lambda x: x ** 3.0 + 2.0 * x ** 2.0 - 5.0
    # 1. can find a solution
    root1 = bisect(0., f, None, [-5.0, 5.0], [0.001, 0.01], 1000)
    print("MyRoot1 is:", root1)
    # 2. bounds are not feasible
    root2 = bisect(0., f, None, [1.0, 5.0], [0.001, 0.01], 1000)
    print("MyRoot2 is:", root2)
    # 3. solution is beyond maxiter
    root3 = bisect(0., f, None, [-100.0, 100.0], [0.001, 0.01], 2)
    print("MyRoot3 is:", root3)

    f4 =lambda x: x**3
    root4 = bisect(8.0,f4,None, [-10.0, 10.0], [0.001, 0.01], 1000)
    print("MyRoot4 is:", root4)
