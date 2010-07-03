import math

def schaffer_f6(a, b):
   t1 = math.sin(math.sqrt(a*a + b*b))
   t2 = 1 + 0.001*(a*a + b*b)
   score = 0.5 + (t1*t1 - 0.5)/(t2*t2)
   return score
