from pdf2image import convert_from_path

def pdf2image():

    path = 'C:\\Users\\NovaPM\\Desktop\\denemedosyası\\'

    images = convert_from_path('C:\\Users\\NovaPM\\Desktop\\barkodlu_kitapcik\\test_b_kit.PDF', dpi=300, output_folder=path, fmt='JPEG', output_file="sayfa")  #pdf to jpg
    print(images)

