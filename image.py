
from PIL import Image as img
class IMG:
    def __init__(self, img_abspath):
        
        self.img_path = img_abspath
        assert self.img_path is not None        
        self.img = None
        self.img_size = 0
        self.img_type = None
        self.img_mode = None
        
        self.supported = ['TIFF', 'PNG', 'ICO', 'BMP']
        self.analyze_img()

    def analyze_img(self):
        try:
            self.img = img.open(self.img_path)
            self.img_size = self.img.size[0]*self.img.size[1]
            self.img_type = self.img_path.split('.')[-1]
            self.img_mode = ''.join(self.img.getbands())
            print("carrier:", self.img_path, self.img_type, self.img_mode, self.img_size)
    
        except Exception as e:
            raise Exception('error analyzing image: {} - {}'.format(self.img_path, str(e)))
        
    def assign_output_type(self):
        '''
        Determines the correct file format.
        '''
        image_type = self.img_type.lower()
        if image_type in ['jpg', 'jpeg']:
            return 'jpeg'
        elif image_type in ['tif', 'tiff']:
            return 'TIFF'
        elif image_type == 'png':
            return 'png'
        elif image_type == 'bmp':
            return 'bmp'


       
    
        
            
    
