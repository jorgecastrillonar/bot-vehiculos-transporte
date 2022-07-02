############################################333
from random import random, randrange
##############################################################################
"""
Metodo que genera un emoji aleatorio en formato unicode que represente un exito.
return string arrayEmojisExito
"""
def emojis_exito():
    #\U0001F603 #\U0001F604 #\U0001F973 #\U0001F44D #\U0001F638
    arrayEmojisExito = [{'id':1, 'emojiUC':'\U0001F603'},
                        {'id':2, 'emojiUC':'\U0001F604'},
                        {'id':3, 'emojiUC':'\U0001F973'},
                        {'id':4, 'emojiUC':'\U0001F44D'},
                        {'id':5, 'emojiUC':'\U0001F638'}]
    randomDigit = randrange(1,len(arrayEmojisExito))
    return arrayEmojisExito[randomDigit]['emojiUC']
##############################################################################
"""
Metodo que genera un emoji aleatorio en formato unicode que represente un fallo.
return string arrayEmojisFallo
"""
def emojis_fallo():
    #\U0001F603 #\U0001F604 #\U0001F973 #\U0001F44D #\U0001F638
    arrayEmojisFallo = [{'id':1, 'emojiUC':'\U0001F603'},
                        {'id':2, 'emojiUC':'\U0001F604'},
                        {'id':3, 'emojiUC':'\U0001F973'},
                        {'id':4, 'emojiUC':'\U0001F44D'},
                        {'id':5, 'emojiUC':'\U0001F638'}]
    randomDigit = randrange(1,len(arrayEmojisFallo))
    return arrayEmojisFallo[randomDigit]['emojiUC']
##############################################################################
"""
Metodo que genera un emoji aleatorio en formato unicode que represente una pregunta.
return string arrayEmojisPregunta
"""
def emojis_pregunta():
    #\U0001F603 #\U0001F604 #\U0001F973 #\U0001F44D #\U0001F638
    arrayEmojisPregunta = [{'id':1, 'emojiUC':'\U0001F603'},
                        {'id':2, 'emojiUC':'\U0001F604'},
                        {'id':3, 'emojiUC':'\U0001F973'},
                        {'id':4, 'emojiUC':'\U0001F44D'},
                        {'id':5, 'emojiUC':'\U0001F638'}]
    randomDigit = randrange(1,len(arrayEmojisPregunta))
    return arrayEmojisPregunta[randomDigit]['emojiUC']
##############################################################################
"""
Metodo que genera un emoji aleatorio en formato unicode que represente una excepcion.
return string arrayEmojisExepcion
"""
def emojis_excepcion():
    #\U0001F603 #\U0001F604 #\U0001F973 #\U0001F44D #\U0001F638
    arrayEmojisExepcion = [{'id':1, 'emojiUC':'\U0001F603'},
                        {'id':2, 'emojiUC':'\U0001F604'},
                        {'id':3, 'emojiUC':'\U0001F973'},
                        {'id':4, 'emojiUC':'\U0001F44D'},
                        {'id':5, 'emojiUC':'\U0001F638'}]
    randomDigit = randrange(1,len(arrayEmojisExepcion))
    return arrayEmojisExepcion[randomDigit]['emojiUC']