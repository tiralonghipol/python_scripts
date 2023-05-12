# import sympy 
from sympy import * 
  
x, y = symbols('x y')
expr = x**2 + 2 * y + y**3
print("Expression : {} ".format(expr))
   
# Use sympy.Derivative() method 
expr_diff = Derivative(expr, x)  
      
print("Derivative of expression with respect to x : {}".format(expr_diff))  
print("Value of the derivative : {} ".format(expr_diff.doit()))