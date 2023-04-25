# -*- coding: utf-8 -*-


#Pile
def creerPile():
    L=[]
    return L

def estPileVide(L):
    if len(L)==0:
        return True
    else:
        return False
    
def empiler(element,L):
    L.append(element)
    return L

def depiler(L):
    if L==[]:
        return (False,'Erreur')
    else:
        return L.pop(),L
    
def affiche(L):
    chaine = f"{L[0]}"
    for element in L[1:]:
        chaine += f" -> {element}"
    return chaine


def regarde(pile):
    sommet=depiler(pile)[0]
    pile=empiler(sommet, pile)
    return sommet

#######################################################################
operator=["+","-","*","/","%","//","**"]
operatorprio=[["+","-"],["*","/","%","//"],["**"]]
def compareValue(operator1:str,operator2:str)->str:
    """

    Parameters
    ----------
    operator1 : str
    operator2 : str

    Returns
    -------
    str
        Retourne l'operateur le plus prioritaire entre le 1er et le 2ème sachant que les parenthèses sont les plus prioritaires
    int   
        la 'valeur' de cet opérateur (plus il est important plus cette valeur est grande)
    """
    val1=0
    val2=0
    for i in range(len(operatorprio)):
        if operator1 in operatorprio[i]:
            val1=i
        if operator2 in operatorprio[i]:
            val2=i
        if operator1=="(":
            val1=4
        if operator2=="(":
            val2=4
    if val1<val2:return operator2,val2
    if val2<val1:return operator1,val1
    if val2==val1:return 'equal',val1
#Test
print('=================TEST DE LA FONCTION "compareValue"========================')
print("On compare * et une parenthèse fermée")
print(f"La fonction renvoie : {compareValue('*',')')}\n")
print("On compare ** et //")
print(f"La fonction renvoie : {compareValue('**','//')} \n")
print("On compare + et -")
print(f"La fonction renvoie : {compareValue('+','-')}\n")
#Complexité
print("La complexitée de compareValue.py dépend d'une liste avec longueur fixe donc : O(1)")
print('================================================================================ \n \n')


def tokens_to_postfix(Lt:list)->(bool,list):
    """

    Parameters 
    ----------
    Lt : list
        Tokens a étudier.

    Returns
    -------
    bool
        Retourne True si l'expression ne contient pas d'erreur et inversement.
    List
        Retourne la liste de l'expression écrite en notation post-fixée.

    """    
    L_postfix=[]
    pile_op=creerPile()
    indice=0
    for elem in Lt:
        indice+=1
        if type(elem)==float or type(elem)==int: # Si on détécte un nombre on l'ajoute à la liste
            L_postfix.append(elem)
        if type(elem)==str:
            if elem in operator:
                if not estPileVide(pile_op): # si la pile n'est pas vide on compare les opérateurs entre eux pour voir les priorités
                    sommetPile=depiler(pile_op)[0]
                    value,m=compareValue(elem,sommetPile) #on évite de trop surcharger en complexitée
                    
                    # on a eu probleme sur le calcul 9//5**3-4 et ça nous ne rendait la bonne réponse. Pour le regler on rajoute cette partie :
                    if m==2 and value==sommetPile: #si on obtient l'opérateur ** nous avons un problème que l'on doit regler
                        L_postfix.append(sommetPile) #On ajoute l'operateur à la liste
                        if not estPileVide(pile_op): # la pile doit etre non vide
                            sommetPile=depiler(pile_op)[0] #on dépile pour étudier l'opérateur précédent
                            while compareValue(elem,sommetPile)==(sommetPile,2): #tant que notre élément est plus fort que les opérateurs précédents on continue
                                if not estPileVide(pile_op): # si la pile est non vide et que l'opérateur précédent est encore inferieur à l'elem 
                                    L_postfix.append(sommetPile) #on ajoute l'opérateur précedent à l'expression et on l'enlève de la pile
                                    sommetPile=depiler(pile_op)[0]
                                else:
                                    L_postfix.append(sommetPile) # sinon on ajoute l'opérateur et on arrête le while
                                    break
                            value=compareValue(elem,sommetPile)[0]
                            if value==sommetPile or value=='equal': # on revérifie le sommet de la pile est encore prioritaire 
                                if sommetPile !="(": #Si ce n'est pas une parenthèse on le retire de la pile
                                    L_postfix.append(sommetPile)
                                else: #si on voit une parenthèse on la laisse dans la pile
                                    empiler(sommetPile,pile_op)
                            else:
                                pile_op=empiler(sommetPile,pile_op)
                    
                    elif value==sommetPile or value=='equal': 
                        if sommetPile !="(": #Si ce n'est pas une parenthèse on le retire de la pile
                            L_postfix.append(sommetPile)
                        else: #si on voit une parenthèse on la laisse dans la pile
                            empiler(sommetPile,pile_op)
                    else:
                        empiler(sommetPile,pile_op)
                empiler(elem,pile_op)
                
            if elem =="(":
                empiler(elem,pile_op)
            if elem ==")": # si on détécte une parenthèse fermante on dépile jusqu'a ce que l'on trouve une parenthèse ouvrante
                if estPileVide(pile_op):return (False,'Erreur')# Si la liste est vide de base on retourne une erreur
                while regarde(pile_op)!="(":
                    depile=depiler(pile_op)[0]
                    if depile!="(":
                        L_postfix.append(depile)
                    if estPileVide(pile_op):return (False,'Erreur') # si on a vidé la pile sans trouver de parenthèses ouvrantes on retourne une erreur
                depiler(pile_op)#on enlève la parenthèse ouvrante
    while not estPileVide(pile_op): #ensuite on vide la pile 
        depile=depiler(pile_op)[0]
        if depile=="(": return (False,'Erreur',indice)
        else:L_postfix.append(depile)
    return (True,L_postfix)

#Test
print('=================TEST DE LA FONCTION "tokens_to_postifx"========================')
print("Tokens : ['(','(',2,'*','(',6,'+',-2,')','-','(',11,'+',1,')',')','-',3,')']")
print(f"La fonction renvoie : {tokens_to_postfix(['(','(',2,'*','(',6,'+',-2,')','-','(',11,'+',1,')',')','-',3,')'])}\n")
print("Tokens : ['-',2,'+',2]")
print(f"La fonction renvoie : {tokens_to_postfix(['-',2,'+',2])} \n")
print("Tokens : [9, 8, 2, '**', '**', 7, '-']")
print(f"La fonction renvoie : {tokens_to_postfix([9, 8, 2, '**', '**', 7, '-'])}\n")
print("Tokens : [9, 7, '-',')']")
print(f"La fonction renvoie : {tokens_to_postfix([9, 7, '-',')'])}\n")
#Complexité
print('La complexitée de tokens_to_postfix.py est quadratique : O(len(Lt)²)')
print('================================================================================ \n \n')




#########################################################################################
def compute_postfix(liste_jetons:list)->(bool,float):
    """

    Parameters
    ----------
    liste_jetons : list
        liste de "jetons" représentant une expression en notation post-fixée

    Returns
    -------
    bool
        Retourne True si le calcul est possible et inversement sinon.
    str/int/float
        la valeur numérique de cette expression si le calcul est possible (float ou int en depend du résultat) ou 'Erreur' si le calcul est impossible

    """ 
    
    Pile=creerPile()
    for jeton in liste_jetons:
        if type(jeton)!=str: 
            empiler(jeton,Pile) #si le jeton est un chiffre, on l'empile dans la pile
        else:
            y=depiler(Pile)[0]
            x=depiler(Pile)[0] #si le jeton est un opérateur, on dépile deux fois la pile 
            if type(x)!=type(y):
                return (False,'Erreur') 
            else:        
                if jeton=="+":
                    empiler(x+y,Pile)
                if jeton=="-":
                    empiler(x-y,Pile)
                if jeton=="*":
                    empiler(x*y,Pile)
                if jeton=="/":
                    empiler(x/y,Pile)
                if jeton=="%":
                    empiler(x%y,Pile)
                if jeton=="//":
                    empiler(x//y,Pile)
                if jeton=="**":
                    empiler(x**y,Pile)
    if len(Pile)!=1:
        return (False,'Erreur')
    else:
        return (True,Pile[0])
    
#Test
print('=================TEST DE LA FONCTION "compute_postfix"==========================')
L=[2,6,-2,'+','*',11,1,'+','-',3,'-']    
print(f"Expression Postfixée : {L}")
print(f"La fonction renvoie : {compute_postfix(L)} \n")

L=[7.0, 8.0, '*', 4.0, '//', 6.0, '+']    
print(f"Expression Postfixée : {L}")
print(f"La fonction renvoie : {compute_postfix(L)}\n")

L=['a', 8.0, '**', 4.0, '+', 2.0, '+']    
print(f"Expression Postfixée : {L}")
print(f"La fonction renvoie : {compute_postfix(L)}\n")
#Complexité
print('La complexitée de compute_postfix.py est linéaire : O(len(liste_jetons))')

print('================================================================================\n \n')



def str_to_tokens (expression:str)->(bool,list):
    """
    verifie si l'expfression proposée est valide  la transforme en tokens'

    Parameters
    ----------
    expression : chaine de caractères représentant une expression à calculer.

    Returns 
    -------
    tuple (bool, str) si erreur : 
                    -Opérateurs interdits (Ex : --, */)
                    -Caractères non reconnus (Ex : a*7)
                    -Mauvaises utilisation des décimaux (Ex : 4.6.5)
                    -Commencer avec un opérateur (Ex : *7-6)
    tuple (bool, list) si l'expression est valide'

    """
    chiffres=['0','1','2','3','4','5','6','7','8','9',"."]
    operateurs=["+","-","*","/","**","%","//"]
    parentheses=["(",")"]
    
    
    
    for i in range (len(expression)):# vérifie que tous les caractères utilisés sont bien définis
        if expression[i]==" ": 
            1==1
        elif expression[i]not in chiffres and expression[i] not in operateurs and expression[i]not in parentheses :
            return (False, 'Erreur',i)
    tokens=[]
    virgule=False
    k=-1
    
    #On verifie que le premier élément autre qu'une parenthèse ne soit PAS un opérateur
    Valide=False #On part du principe que l'expression est fausse
    for i in range(0,len(expression)):
        if Valide==False and expression[i] in chiffres: #Si on trouve un operateur avant le premier chiffre, il y a une erreur
            Valide=True
        if Valide==False and expression[i] in [operateurs[0]]+operateurs[2:]:
            return (False,'Erreur',i)
    
    for i in range(len(expression)):
        if expression[i]==" ":
            1==1       
        if expression[i]=="-"and expression[i-1]=="(":#prend en charge les nombre négatifs
            tokens.append(expression[i])
            k=i+1 #on pose un indice pour éviter de repasser sur ce qu'on va étudier dans le while
            while expression[k]!=")":
                tokens[-1]+=expression[k]
                k+=1
            tokens[-1]=float(tokens[-1])
        
        if (expression[i] in parentheses and k<i) or (expression[i] in  operateurs and k<i): #Si on étudie pas quelque chose de deja étudié on continue
            if len(expression)>i: #on évite les erreurs de out of range
                if expression[i] in  operateurs and expression[i+1] in  operateurs:# si jamais on a deux opérateurs d'affilés
                    if expression[i]==expression[i+1] and (not expression[i]=='*' and not expression[i]=='/'):#s'ils sont égaux et qu'ils sont différents de // ou **
                        return(False,'Erreur',i)
                    elif expression[i]==expression[i+1] and (expression[i]=='*' or  expression[i]=='/'): #Sinon si ils font partie des opérateurs légaux ** ou //
                        if len(expression)>i+1:
                            if expression[i]==expression[i+2]:#On evite les erreurs s'il y en a 3 d'affilés
                                return(False,'Erreur',i)
                            else: 
                                k=i+1 #on saute 2 éléments ca on rajoute **
                                tokens.append(expression[i]+expression[i+1])
                    else:
                        return(False,'Erreur',i)
                elif expression[i]=="(" :
                    if not expression[i+1]=="-":
                        tokens.append(expression[i])
                else:
                    tokens.append(expression[i])                    
            else:
                tokens.append(expression[i])
                
        if expression[i] in chiffres and k<=i: # on reprend au bon indice sans réétudier les nombres deja analysés par le while
            if virgule:#prend en charge les nombres décimaux
                if expression[i]==".":
                    return (False,'Erreur',i)
                if i<len(expression)-1:
                    if expression[i+1] not in chiffres:
                        virgule=False
                        tokens[-1]+=expression[i]
                    else: 
                        tokens[-1]+=expression[i]
                else: 
                    tokens[-1]+=expression[i]
            elif not virgule:
                if expression[i]==".":
                    virgule=True
                    if tokens==[]: # si on a une expression qui commence par ., on l'ajoute dans la liste tokken
                        tokens.append(expression[i])
                    else:
                        tokens[-1]+=expression[i]
                elif i>0 and expression[i-1] in chiffres:
                    tokens[-1]+=expression[i]
                else :
                    tokens.append(expression[i]) 
    for k in range (len(tokens)): #Transformer les chiffres de str en tokens
        if tokens[k] not in operateurs and  tokens[k] not in parentheses:
            tokens[k]=float(tokens[k])
        else :
            1==1
    return(True,tokens)         
 
#Test
print('=================TEST DE LA FONCTION "str_to_tokens"============================')
L="3*7//8-4" 
print(f"Expression : {L}")
print(f"La fonction renvoie : {str_to_tokens(L)} \n")

L="(4.9--9)"
print(f"Expression : {L}")
print(f"La fonction renvoie : {str_to_tokens(L)}\n")

L="((4.5+5)**8)-((-9)-6))"
print(f"Expression : {L}")
print(f"La fonction renvoie : {str_to_tokens(L)}\n")

L="(4.5.8-9*7)"
print(f"Expression : {L}")
print(f"La fonction renvoie : {str_to_tokens(L)}\n")

L="(*7+4)"
print(f"Expression : {L}")
print(f"La fonction renvoie : {str_to_tokens(L)}\n")

L="(a*8)"
print(f"Expression : {L}")
print(f"La fonction renvoie : {str_to_tokens(L)}\n")
#Complexité
print('La complexitée de str_to_tokens.py est quadratique : O(len(expression)²)')

print('================================================================================\n')

                    

    


def affichage()->None:
    """
        
    Affiche un terminal qui fonctionne comme une calculette. Tapez "exit" pour quitter le programme.
    
    Returns
    -------
    None.

    """
    print("==================================================== \nCalculette Prépa INP (taper exit pour quitter) \n====================================================")
    expression=input(">>> ")
    while expression != "exit":
        #on verifie d'où viens le problème
        token=str_to_tokens(expression) #complexité de O(n^2)
        postfix=tokens_to_postfix(token[1])#complexité de O(n^2)
        indicerreur1=-1
        indicerreur2=-1
        if len(token)==3:
            indicerreur1=token[2]
        elif len(postfix)==3:
            indicerreur2=postfix[2]
        valeur=compute_postfix(postfix[1])[1] #complexité de O(n)
        if valeur=='Erreur':
            if indicerreur1!=-1 and indicerreur2!=-1: #si jamais il y a plusieurs erreur
                ie=min(indicerreur1,indicerreur2)
            if indicerreur1==-1: #si jamais il y a plusieurs erreur
                ie=indicerreur2
            if indicerreur2==-1: #si jamais il y a plusieurs erreur
                ie=indicerreur1
            print(f'Erreur : {expression}')
            print((ie+9)*" "+"^") #on rajoute 8 caractère vide pour dépasser 'Erreur : '
            print((ie+9)*" "+"|")
        else:
            print("Expression postfixe :")
            carac=str(postfix[0])
            for element in postfix[1:]:
                carac+=", "+str(element)
            print(carac)
            print(f'Résultat: {valeur}')
        expression=input(">>> ")
    return None
    
print('=================TEST DE LA FONCTION "affichage"================================')
#Complexité
print('La complexitée de str_to_tokens.py est quadratique : O(len(expression)²)')

print('================================================================================')
