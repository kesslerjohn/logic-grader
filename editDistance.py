import re
import os

'''
Developing a program for grading LFR homework. These will be able to parse input strings
and determine their minimum edit distance from the intended answer, plus identify specific 
divergences from the intended answer and grade accordingly. 
This is a dumb grader which just checks for string equvalence. As a stretch goal: integrate with Haskell 
and evaluate whether the given answer is logically equivalent to the intended answer. 
TODO: Establish grading criteria. Can be based on:
    - Minimum edit distance
    - Whether all atomic statements are present (number of distict variables)
    - Logical equivalence to correct answer 
'''

edit = []
ins = 0
dlt = 0
rpl = 0
responses = []
answers = ["(D->(L&-C)", "(-(W&S)->P)", "(W->(G&--H))", "(-M -> -L)"]

'''REGEXES'''

connective = '[^\w()]{1,2}[^\w-]?' #Matches one non-anum/non-paren character, optionally one more, 
                                   #and optionally a third that is not '-'
                                   #Will return one logical connective if the string contains one.
                                   #Not working perfectly yet.
nnd = '&'
orr = 'v'
bcn = '<->'
cnd = '->' #Doesn't quite work. I want it to match only '->'. Can be solved dumbly by checking for this after '<->'. 
ntt = '-' #Also not perfect: will pull the - from a conditional. Currently patching this, too, with ordered checking. 
connectives = ['&', 'v', bcn, cnd, ntt, '(', ')'] 
replacements = ['&', 'v', '3', ';', '-', '', '']

def Simplify(s):
    s = s.replace(" ", "")
    for i in range(len(connectives)):
        s = s.replace(connectives[i], replacements[i])
    #variables = list(set([p for p in s]))
    return s

def getVars(s):
    s = s.replace(" ", "")
    for c in connectives:
        s = s.replace(c, "")
    variables = list(set([p for p in s]))
    return variables

'''
The function below gives the edit distance between two strings, for use comparing given answers to the 
correct ones. 
In its parameters, s1 is the student's answer, and s2 is the correct answer. 
At each decision point, this should check which connectives are at index i of the given string (if any)
and if they are incorrect, then deduct a certain number of points. 
Actually, I will do string processing ahead of time and replace each connective with a dedicated character.
Then I can just check each index. 
TODO: (DONE) strip whitespace from given string before comparing. 
TODO: sort vars before comparing. By combining this with edit distance, I can determine if the student
switched the order of connectives in a conditional. 
NOTE: This will combine well with Haskell integration, since this might catch out biconditionals, but
they will be found logically equivalent. 
'''

def EditDistance(s1, s2):
    s1 = s1.replace(" ", "") #strip whitespace before comparing. 
    edit = [[0 for num in range(len(s2)+1)] for num in range(len(s1)+1)]
    for j in range(0, len(s2)+1):
        edit[0][j] = j
    for i in range(1, len(s1)+1):
        edit[i][0] = i
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            ins = (edit[i][j-1] + 1)
            dlt = (edit[i-1][j] + 1)
            if s1[i-1] == s2[j-1]:
                rpl = (edit[i-1][j-1])
            else:
                rpl = (edit[i-1][j-1] + 1)
            edit[i][j] = min(ins, dlt, rpl)
    return (edit[-1][-1])

def main():
    print("Please paste the absolute directory path here: \n")
    directory = input()
    os.chdir(directory)
    score = 100
    with open(directory+'/answers.rtf', 'r') as ans:
        print("Answers found: ")
        for line in ans:
            if (re.search('\#.*\$', line)):
                answer = re.search('\#.*\$', line).group(0).replace("#", "").replace("$", "")
                print(answer)
                responses.append(answer)
    for i in range(len(answers)):
        if responses[i].replace(" ", "") == "":
            print("Empty response, -4 points\nExpected: {}\n".format(answers[i]))
            score -= 4
        else:
            print("Actual: {}\nExpected: {}\n".format(responses[i], answers[i]))
            score -= EditDistance(responses[i], answers[i])
    print("Your final score is {}%".format(score))


'''TEST'''

given = "(P <-> -Q)"
correct = "(P & -Q)"
long = "(B -> (B & -C)"

if __name__ == "__main__":
    main()


#print(EditDistance("(P -> Q)", "(P->(Q&R))"))
#print("The value of __name__ is: ", repr(__name__))