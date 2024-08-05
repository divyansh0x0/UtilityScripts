
import time, os, base64, io
ICON = "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"

def isValidImagePath(imPath):
    return os.path.exists(imPath) and os.path.isfile(imPath) and os.path.splitext(imPath)[1].lower() in [".png",".jpeg",".jpg",".webp"]
class Toast:
    def __init__(self,msg,font,duration_secs,text_color=(255,255,255),bg_color=(0,0,0)) -> None:
        self.msg = msg
        self.font :pygame.font.Font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.duration_secs = duration_secs
        self.isShowing = False
    def show(self,msg=None):
        if msg != None:
            self.setMessage(msg)
        self.time_displayed_at_ns = time.time_ns()
        self.isShowing = True
    def hide(self):
        self.isShowing= False
    def setMessage(self,msg):
        self.msg = msg
    def draw(self,surface):
        if self.isShowing:
            if (time.time_ns() - self.time_displayed_at_ns) * 1e-9 >= self.duration_secs :
                self.hide()
        if self.isShowing:
            txtSize= self.font.size(self.msg)
            pad = 10
            draw.rect(surface,self.bg_color,rect=(surface.get_width()/2 - txtSize[0]/2 - pad, surface.get_height()/2 - pad - txtSize[1]/2,txtSize[0] + pad *2 ,txtSize[1] + pad*2),border_radius=10)
            surface.blit(self.font.render(self.msg, True, self. text_color, self.bg_color),(surface.get_width()/2 - txtSize[0]/2, surface.get_height()/2 - txtSize[1]/2))        
class Button:
    def __init__(self,bg,hover_color,text_color,font,text,size=(200,40), pos=(0,0)) -> None:
        self.bg_color = bg
        self.hover_color = hover_color
        self.text_color = text_color
        self.font:pygame.font.Font = font
        self.text = text
        self.size = size
        self.pos = pos
    def setPos(self,x:int,y:int):
        self.pos = (x,y)
    def draw(self,surface):
        mouse_pos = pygame.mouse.get_pos()
        bg_color = self.hover_color if self.containsPoint(mouse_pos[0],mouse_pos[1]) else self.bg_color
        draw.rect(surface,bg_color,rect=(self.pos[0],self.pos[1],self.size[0],self.size[1]),border_radius=10)
        txtSize= self.font.size(self.text)
        surface.blit(self.font.render(self.text, True, self.text_color),(self.pos[0] + self.size[0]/2 - txtSize[0]/2, self.pos[1] + self.size[1]/2 - txtSize[1]/2))
    def setText(self,text):
        self.text = text
    def containsPoint(self,x,y):   
        return (self.pos[0] <= x <= self.pos[0]+self.size[0] and self.pos[1] <= y <= self.pos[1]+self.size[1])
class Slider:
    def __init__(self,bg,slider_color,text_color,font,min_val,max_val,value=0,text="",size=(200,40), pos=(0,0)) -> None:
        self.slider_color = slider_color
        self.bg_color = bg
        self.text_color = text_color
        self.font:pygame.font.Font = font
        self.size = size
        self.pos = pos
        self.value = value
        self.text = text
        
        self.setMinMaxValues(min_val,max_val)
    def setMinMaxValues(self,min_val,max_val):
        if max_val<min_val:
            raise ValueError("max_val cannot be less than min_val")
        if max_val < 0 or min_val < 0:
            raise ValueError("max_val and min_val cannot be less than 0")
        self.min_val = min_val
        self.max_val = max_val
        self.value_range =(self.max_val +self.min_val)
        
    def setSize(self,width,height):
        self.size = (width,height)
    def setPos(self,x:int,y:int):
        self.pos = (x,y)
    def setText(self,text):
        self.text = text
        
    def draw(self,surface):

        
        ratio = (self.value - self.min_val)/(self.max_val - self.min_val)

        draw.rect(surface,self.bg_color,rect=(self.pos[0],self.pos[1],self.size[0],self.size[1]),border_radius=10)
        draw.rect(surface,self.slider_color,rect=(self.pos[0],self.pos[1],ratio*self.size[0],self.size[1]),border_radius=10)
        txtSize= self.font.size(self.text)
        
        surface.blit(self.font.render(self.text, True, self.text_color),(self.pos[0] + self.size[0]/2 - txtSize[0]/2, self.pos[1] + self.size[1]/2 - txtSize[1]/2))

    def setValue(self,value):
        self.value = self.max_val if value > self.max_val else self.min_val if value < self.min_val else value
        self.value = round(self.value,2)
        # print(self.value)
    def containsPoint(self,x,y):
        return (self.pos[0] <= x <= self.pos[0]+self.size[0] and self.pos[1] <= y <= self.pos[1]+self.size[1])
    def setValueRatio(self,ratio):
        if ratio > 1:
           ratio = 1
        if ratio < 0:
           ratio = 0
        self.setValue(self.min_val + self.value_range * ratio)
class ImageQualityModifier:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = display.set_mode((640, 480),flags=pygame.RESIZABLE)
        try:
            pygame.display.set_caption("Image Quality Modifier","Image Quality Modifier")
            pygame.display.set_icon(image.load(io.BytesIO(base64.b64decode(ICON))))
        except Exception as e:
            print(e)
        self.imagePath = None
        self.predictedImageSize = None
        self.imageQuality = 0
        self.modifiedImagePath = None
        self.imgSurface : surface.Surface  = None
        self.pilImg = None
        self.font = pygame.font.SysFont(None,30)
        self.textColor = (255,255,255)
        self.bgColor = (22,22,22)
        self.resolution_slider = Slider((100,100,100),(190,190,190),(0,0,0),self.font,1,100,100,"Quality:100%")
        self.isDraggingOnSlider= True
        self.imageRenderPos = (100,100)
        self.imageRenderSize = (100,100)
        self.imageOriginalResolution = (0,0)
        self.newImageResolution = (0,0)
        self.text_box_height = 0
        self.pad = 20
        self.dataValueDic = {"Original Image Resolution":self.imageOriginalResolution, "New Image Resolution":self.imageRenderSize, "Save path:":self.modifiedImagePath}
        self.originalImageSurface = None
        self.saveButton = Button((75, 104, 250),(88, 116, 252),(0,0,0),self.font,"Save",size=(100,40),pos=(self.screen.get_width() - 100 - self.pad, self.screen.get_height() - 40 - self.pad))
        self.toast = Toast("Drag an image here",self.font, 3, (255,255,255), (0,0,0))
        self.wasSaveButtonPressed = False
        self.delta = (0,0)

        self.zoom = 1.0        
        self.MIN_ZOOM = 0.3
        self.MAX_ZOOM = 5.0

        self.dragStarted = False
        self.toast.show()

    def update(self):
        pad = self.pad


        #slider
        mouse_pos = pygame.mouse.get_pos()
        screen_size = self.screen.get_size()
        slider_size = (screen_size[0] - self.saveButton.size[0] - pad*2,self.resolution_slider.size[1])
        slider_y_pos = min(screen_size[1]-slider_size[1] - 10,screen_size[1]-slider_size[1])
        slider_x_pos = (screen_size[0]-slider_size[0])/2  - self.saveButton.size[0]/2 

        self.resolution_slider.setPos(slider_x_pos, slider_y_pos)
        self.resolution_slider.setSize(slider_size[0],slider_size[1])

        #save button
        self.saveButton.setPos(self.resolution_slider.pos[0] + self.resolution_slider.size[0] + 10, self.resolution_slider.pos[1])        
        
        if self.resolution_slider.containsPoint(mouse_pos[0],mouse_pos[1]) or self.isDraggingOnSlider:
            if pygame.mouse.get_pressed()[0]:
            #add dragging functionality
                initialVal = self.resolution_slider.value
                ratio =(mouse_pos[0]-self.resolution_slider.pos[0])/self.resolution_slider.size[0]
                self.resolution_slider.setValueRatio(ratio)
                self.isDraggingOnSlider = True
                
                if self.resolution_slider.value != initialVal and self.imgSurface != None:
                    ratio = self.resolution_slider.value/self.resolution_slider.value_range
                    self.newImageResolution = (int(self.imageOriginalResolution[0]*ratio),int(self.imageOriginalResolution[1]*ratio))
                    
                    self.reloadImage(self.imagePath)
                    self.imgSurface = transform.scale(self.imgSurface,self.newImageResolution)
                    self.imgSurface = transform.scale(self.imgSurface,self.imageRenderSize)
                    
                    
                    self.resolution_slider.setText("Quality : " + str(self.resolution_slider.value) + "%")
                    print(self.imageOriginalResolution, "->",self.newImageResolution)
                    self.dataValueDic["New Image Resolution"] = str(self.newImageResolution[0]) + "x" + str(self.newImageResolution[1])       
                
            else:
                self.isDraggingOnSlider = False
        #image
        if self.imgSurface != None:
            aspect_ratio = self.imageOriginalResolution[0] / self.imageOriginalResolution[1]
            new_width = min(self.screen.get_width() - pad, int((self.screen.get_height() - self.text_box_height - self.resolution_slider.size[1] -2* pad) * aspect_ratio)) *0.9 
            new_height = min(self.screen.get_height() - self.text_box_height - self.resolution_slider.size[1] - 2* pad, int((self.screen.get_width() - pad)/ aspect_ratio)) *0.9
            self.imageRenderSize = (abs(round(new_width * self.zoom )) , abs(round(new_height * self.zoom)) )
            x = self.delta[0] + (self.screen.get_width()- self.imageRenderSize[0] )/2
            y = self.delta[1] + self.text_box_height/2 + (self.screen.get_height() - self.imageRenderSize[1] )/2 - pad
            self.imageRenderPos = (x,y)
            
        if self.dragStarted:
            delta =  pygame.mouse.get_rel()
            self.delta = (self.delta[0] + delta[0],self.delta[1] + delta[1])
            print(self.delta)
        else:
            self.delta = (0,0)
    def saveImage(self):
        if self.originalImageSurface != None and self.modifiedImagePath != None:
            print("Saving image to", self.modifiedImagePath)
            image.save(transform.scale(self.originalImageSurface,self.newImageResolution),self.modifiedImagePath)
            self.toast.show("Image saved")
    def render(self):
        self.screen.fill(self.bgColor)
        
        borderWidth = 10
        if self.imgSurface != None:
            if self.imageRenderSize[0] != self.imgSurface.get_width() or self.imageRenderSize[1] != self.imgSurface.get_height():
                self.reloadImage(self.imagePath)
                print("Rendering surface in", self.imageRenderSize)
                self.imgSurface = transform.scale(self.imgSurface,self.imageRenderSize)
                self.imageRenderSize = (self.imgSurface.get_width(),self.imgSurface.get_height())
                self.imgSurface = transform.scale(self.imgSurface,self.newImageResolution)
                self.imgSurface = transform.scale(self.imgSurface,self.imageRenderSize)
                
            draw.rect(self.screen,(0,0,0),rect=(self.imageRenderPos[0]-borderWidth,self.imageRenderPos[1]-borderWidth,self.imageRenderSize[0]+2*borderWidth,self.imageRenderSize[1]+2*borderWidth),border_radius=10)
            self.screen.blit(self.imgSurface,self.imageRenderPos)
        self.resolution_slider.setText("Quality: " + str(self.resolution_slider.value) + "%")
        self.resolution_slider.draw(self.screen)
        self.saveButton.draw(self.screen)
        self.toast.draw(self.screen)
        self.drawText()
    def loadImage(self,path):
        try:
            if isValidImagePath(path):
                self.imagePath = path                
                self.modifiedImagePath = os.path.join(os.path.dirname(self.imagePath), 'modified_' + os.path.basename(self.imagePath))
                self.imgSurface=  image.load(self.imagePath)
                self.originalImageSurface = image.load(self.imagePath)
                self.imageOriginalResolution = (self.imgSurface.get_width(),self.imgSurface.get_height())
                self.newImageResolution = (self.imgSurface.get_width(),self.imgSurface.get_height())
                self.resolution_slider.setValue(self.resolution_slider.max_val)
                self.imageRenderSize = self.imageOriginalResolution
                self.dataValueDic["Save path:"] = self.modifiedImagePath
                self.dataValueDic["Original Image Resolution"] = str(self.imageOriginalResolution[0]) + "x" + str(self.imageOriginalResolution[1])
                self.dataValueDic["New Image Resolution"] = str(self.newImageResolution[0]) + "x" + str(self.newImageResolution[1])       
            
                print("Loaded",self.imagePath,self.modifiedImagePath)
                self.reloadImage(path)
            else:
                self.toast.show("Invalid image: " + os.path.basename(path))
        except Exception as e:
            self.toast.show("Error occurred:" + e.args[0])
    def reloadImage(self,path):
        if isValidImagePath(path):
            self.imagePath = path                
            self.modifiedImagePath = os.path.join(os.path.dirname(self.imagePath), 'modified_' + os.path.basename(self.imagePath))
            self.imgSurface=  image.load(self.imagePath)
            
            print("Reloaded ",self.imagePath,self.modifiedImagePath)
    def drawText(self):
        y  = 10
        render_area = (self.screen.get_width() - self.pad*2, self.screen.get_height())
        for key,value in self.dataValueDic.items():
            text = str(key) + " : " + str(value)
            if self.font.size(text)[0] > render_area[0]:
                while self.font.size(text + "...")[0] > render_area[0]:
                    text = text[:-1]
                text += "..."
            self.screen.blit(self.font.render(text, True, self.textColor),(self.pad, y))
            y += self.font.get_height()
        self.text_box_height = y

    def handleEvent(self,e):
        if e.type == pygame.DROPFILE:
            self.loadImage(e.dict["file"])
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.dict["button"] == 1:
                pos = e.dict["pos"]
                if self.saveButton.containsPoint(pos[0],pos[1]):
                    self.wasSaveButtonPressed = True
            elif e.dict["button"] == 3:
                pygame.mouse.get_rel()
                self.dragStarted = True
        elif e.type == pygame.MOUSEBUTTONUP:
            pos = e.dict["pos"]
            if self.wasSaveButtonPressed and self.saveButton.containsPoint(pos[0],pos[1]):
                    self.saveImage()
                    self.wasSaveButtonPressed = False
                
            self.dragStarted = False
            
        elif e.type == pygame.MOUSEWHEEL:
            delta = e.dict["precise_y"]
            self.zoom += 0.5 * delta
            if(self.zoom < self.MIN_ZOOM):
                self.zoom =self.MIN_ZOOM
            if(self.zoom > self.MAX_ZOOM):
                self.zoom = self.MAX_ZOOM
            print(self.zoom)

    def loop(self):
        MAX_FPS = 60
        MIN_FRAME_TIME = 1e9 / MAX_FPS

        t1 = time.time_ns()
        stop = False
      
        # FPS = 60
        # time_accumulated = 0     
        while not stop:
            for e in event.get():
                if e.type == pygame.QUIT:
                    stop = True
                else:
                    self.handleEvent(e)
            t2 = time.time_ns()
            dt = t2-t1
            if dt < MIN_FRAME_TIME:
                continue
            self.update()
            self.render()
            display.update()
            t1 = t2
            # FPS +=1
            # time_accumulated += dt
            # if time_accumulated >= 1e9:
            #     # print("FPS",FPS)
            #     FPS = 0
            #     time_accumulated = 0

if __name__ == "__main__":
    try:
        import pygame
        from pygame import display, event, image, transform, surface,draw
        print("---------------------------------------------Running ImageQualityModifier-------------------------------------------------------")
        ImageQualityModifier().loop()
        
    except Exception as e:
        print("Required module (pygame 2.6.0) was not found! Consider running the following command: pip install pygame==2.6.0")
    