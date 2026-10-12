**APRIORI ALGORITHM NOTES**



A => antecedent

B => consequent



When A is present, B is also likely to be present.

At the minimum, it is one directional, A -> B. CAN be bidirectional

in specific cases, A <-> B (If A is present, B is also likely to be

present, and vice versa).





**CONCEPTS IN THE APRIORI ALGORITHM:**



* Support (A -> B)	= **Count (A U B) / Total Transactions**

&#x09;		= Percentage (%) of occurences of an itemset(IS)





* Frequent Item Set	= Given IS ⊆ Items, IS is frequent

&#x09;		  if Support **(IS) >= MinSupport**, where

&#x09;		  MinSupport is a given.



* ItemSet Formation	= **IS = A U B**



* Confidence (A -> B)	= **Support(A U B) / Support(A)**

&#x09;		= Percentage of transactions where that contains

&#x09;		  antecedent (A) that also contain the consequent

&#x09;		  (B).

&#x09;		= How often B occurs, IF A occurs.





For following concepts, here are the definitions of these terms:

&#x09;\~ ***Actual Support*** -> *Support(A U B)*, the support of A and B together

&#x09;*\~ **Expected Support*** -> *Support(A) \* Support(B)*, the support of A

&#x09;		      and B occuring together from an independent

&#x09;		      perspective.





* Lift (A -> B) 	= Longform: **Support(A U B) / Support(A) \* Support(B)**

&#x09;		= Shortcut: **Confidence(A -> B) / Support(B)**

&#x09;		= Asks: How ***many times*** more or less often do A and B occur

&#x09;			together than we would expect if they were independent?

&#x09;		= Let l be Lift:

&#x09;			• l > 1 == Positive Association

&#x09;			• l = 1 == No Association

&#x09;			• l < 1 == Negative Association

&#x09;		= Results in a Ratio



* Leverage (A -> B) 	= **Support (A U B) - Support(A) \* Support(B)**

&#x09;		= Asks: How ***much*** more or less often do A and B occur

&#x09;		  together than we would expect if they were independent?

&#x09;		= Let L be Leverage:

&#x09;			• L > 0 == Positive Association

&#x09;			• L = 0 == No Association

&#x09;			• L < 0 == Negative Association

&#x09;		= Results in a Difference





**GENERAL GUIDELINES IN MAKING GOOD ASSOCIATION RULES**



1. There should be no ∅ antecedents or consequents
2. Consequents should only be ItemSets (IS) with a size of 1.





