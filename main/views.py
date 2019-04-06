from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from .forms import ImageForm
from .forms import ImageDecForm
from .models import Images
from .models import ImageDecrypt
from PIL import Image

# Create your views here.
def homepage(request):
    return render(request=request,template_name="main/home.html")

def encrypt(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('/doencrypt/')
    form = ImageForm()
    return render(request,'main/encrypt.html',{
        'form': form
    })

def doencrypt(request):
    image = Images.objects.all()
    for data in image:
        message = data.message
        key = data.key
        img_url = data.img.path
        img_name = data.img.name
        image.delete()


    import string
    #create dictionary with english alphabet keys and numerical values
    alphabet = dict(zip(string.ascii_lowercase, range(1, 27)))
    alphabet[" "] = " "
    #input text and key
    text = message
    #convert key to a list
    key = list(key)
    number = 0
    for letter in key:#convert the key list to numbers
        key[number] = alphabet[key[number]]
        number = number + 1
    text = list(text)#convert text to list
    number = 0
    for letter in text:#convert text list to numbers
        text[number] = alphabet[text[number]]
        number = number + 1
    #check if the lenght of the key is as long as the len of the text
    if len(key) < len(text):#if the len of the key is shorter than the len of the text
        number = 0
        keychain = len(key)
        for x in range(len(text)):#repeat key until its as long an the text 'key="py" text="hello" (output will be:"pypy")'
            key.append(key[number])
            number = number + 1
            if number == keychain:
                number = 0
    out = []
    for x in range(len(text)):#decryption process[subtract the key from the text (unless the the key is " " in that case it'll just add a space to the output)]
        if text[x]==" " or text[x]=="." or text[x]==",":
            o=" "
        else:
            o = int(text[x]) + int(key[x])
            if o > 26:
                o = o - 26

        out.append(o)#output

    output = ""
    for x in range(len(out)):#define find key by value
        def getKey(dict, value):
            return [key for key in dict.keys() if (dict[key] == value)]
        output += ''.join(getKey(alphabet, out[x]))#convert encrypted number to letter using the dictionary


    #code for encoding the encrypted text in the image
        
        
    from PIL import Image
    def encode_image(img, msg):
        length = len(msg)

        if img.mode != 'RGB':
            print("image mode needs to be RGB")
            return False

        encoded = img.copy()
        width, height = img.size
        index = 0
        for row in range(height):
            for col in range(width):
                r, g, b = img.getpixel((col, row))

                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    c = msg[index -1]
                    asc = ord(c)
                else:
                    asc = r
                encoded.putpixel((col, row), (asc, g , b))
                index += 1
        return encoded

    original_image_file = img_url

    img = Image.open(original_image_file)

    encoded_image_file = "media/enc_" + img_name
    secret_msg = output
    img_encoded = encode_image(img, secret_msg)

    if img_encoded:
        img_encoded.save(encoded_image_file)
        print("{} saved!".format(encoded_image_file))

    return render(request, 'main/doencrypt.html', {
        'url' : encoded_image_file
    })


def decrypt(request):
    if request.method == 'POST':
        form = ImageDecForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('/dodecrypt/')
    form = ImageDecForm()
    return render(request,'main/decrypt.html',{
        'form': form
    })

def dodecrypt(request):
    image = ImageDecrypt.objects.all()
    for data in image:
        key = data.key
        img_url = data.EncImage.path
        img_name = data.EncImage.name
        image.delete()

    from PIL import Image
    def decode_image(img):

        width, height = img.size
        msg = ""
        index = 0
        for row in range(height):
            for col in range(width):
                try:
                    r, g, b = img.getpixel((col, row))
                except ValueError:

                    r, g, b, a = img.getpixel((col, row))

                if row == 0 and col == 0:
                    length = r
                elif index <= length:
                    msg += chr(r)
                index += 1
        return msg

    encoded_image_file = img_url

    img2 = Image.open(encoded_image_file)
    print(img2, img2.mode)  # test
    hidden_text = decode_image(img2)



    #Decrypt the hidden text to get the original message


    #text = decrypted text

    import string
    #create dictionaries with english alphabet keys and numerical values
    alphabetneg = {'a': -25, 'b': -24, 'c': -23, 'd': -22, 'e': -21, 'f': -20
                , 'g': -19, 'h': -18, 'i': -17, 'j': -16, 'k': -15, 'l': -14
                , 'm': -13, 'n': -12, 'o': -11, 'p': -10, 'q': -9, 'r': -8
                , 's': -7, 't': -6, 'u': -5, 'v': -4, 'w': -3, 'x': -2, 'y': -1
                , 'z': 0, ' ': ' '}

    alphabet = dict(zip(string.ascii_lowercase, range(1, 27)))
    alphabet[" "] = " "
    #input text and key
    text = hidden_text
    #convert key to a list
    key = list(key)
    number = 0
    for letter in key:#convert the key list to numbers
        key[number] = alphabet[key[number]]
        number = number + 1
    text = list(text)#convert text to list
    number = 0
    for letter in text:#convert text list to numbers
        text[number] = alphabet[text[number]]
        number = number + 1
    #check if the lenght of the key is as long as the len of the text
    if len(key) < len(text):#if the len of the key is shorter than the len of the text
        number = 0
        keychain = len(key)
        for x in range(len(text)):#repeat key until its as long an the text 'key="py" text="hello" (output will be:"pypy")'
            key.append(key[number])
            number = number + 1
            if number == keychain:
                number = 0
    out = []
    for x in range(len(text)):#decryption process[subtract the key from the text (unless the the key is " " in that case it'll just add a space to the output)]
        if text[x]==" " or text[x]=="." or text[x]==",":
            o=" "
        else:
            o = int(text[x]) - int(key[x])
            

        out.append(o)#output
    output = ""
    for x in range(len(out)):
        def getKey(dict, value):#define find key by value 
            return [key for key in dict.keys() if (dict[key] == value)]
        if out[x]==" ":# if letter==" " add " "
            output+=" "
        elif int(out[x])<=0 :#if number is negative or zero use negative dictionary
            output += ''.join(getKey(alphabetneg, out[x]))
        else:#if number is positive use positive dictionary
            output += ''.join(getKey(alphabet, out[x]))
    print(output)

    return render(request, 'main/dodecrypt.html', {
        'message' : output, 'url' : img_name
    })
