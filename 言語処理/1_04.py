s='Hi He Lied Because Boron Could Not Oxidize Fluorine.New Nations Might Also sign Peace Security Clause. Arthur King Can.'
s=s.replace(",","").replace(".","").split()

def function(num,word):
        if num in [1,5,6,7,8,9,15,16,19]:
            return(word[0],num)
        else:
             return(word[:2],num)

ans=[function(num,word) for num,word in enumerate(s,1)]

print(dict(ans))
