from pathlib import Path
import fitz

import os
import shutil

import time

from pymupdf import FileDataError


def clear_dir(folder : Path):
    

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))






def pdf_cropping_top(input_file_path, output_directory : str, crop_box = fitz.Rect(110, 30, 560, 340), rotation : int = -90):
    try:
        with fitz.open(input_file_path) as doc:
            
            
            for page in doc:
                

                
                
                page.set_cropbox(crop_box)
                page.set_rotation(page.rotation + rotation)

            output_path = str(output_directory) + "\\" + input_file_path.split('\\')[-1]
            doc.save(output_path)
    except FileDataError:
        pass


def pdf_cropping_bottom(input_file_path, output_directory : str, crop_box = fitz.Rect(15, 25, 330, 480), rotation : int = 90):
    with fitz.open(input_file_path) as doc:
        
        
        for page in doc:
            
            
            page.set_rotation(0)
            page.set_cropbox(crop_box)

        output_path = str(output_directory) + "\\" + input_file_path.split('\\')[-1]
        doc.save(output_path)

    
    
        

    
def check_existence_directory():
    if not os.path.exists(Path("pdf_input_qr_bottom")):
        os.makedirs(Path("pdf_input_qr_bottom"))

    if not os.path.exists(Path("pdf_input_qr_top")):
        os.makedirs(Path("pdf_input_qr_top"))


    if not os.path.exists(Path("pdf_output")):
        os.makedirs(Path("pdf_output"))
    

def main():

    check_existence_directory()


    start_time = time.time()

    quantityFile = 0
    
    output_dir = Path("pdf_output")
    
    
    dir1 = Path("pdf_input_qr_top")

    

    for filename in os.listdir(dir1):
        file_path = os.path.join(dir1, filename)

        try:
            pdf_cropping_top(file_path, output_dir)

        except FileDataError:
            pass


        else:

            quantityFile += 1

    
    dir2 = Path("pdf_input_qr_bottom")

    

    for filename in os.listdir(dir2):
        file_path = os.path.join(dir2, filename)

        try:
            pdf_cropping_bottom(file_path, output_dir)

        except FileDataError:
            pass

        else:

            quantityFile += 1


    

    clear_dir(dir1)
    clear_dir(dir2)

    print(f"Обрезано {quantityFile} файлов")
    print(f"Время выполнения {time.time() - start_time} секунд")
        





if __name__ == "__main__":
    main()
