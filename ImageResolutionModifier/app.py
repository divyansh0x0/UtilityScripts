import io
import math
import os
import time

import pygame
from pygame import display, event, image, transform, draw

from components.button import Button
from components.slider import Slider
from components.toast import Toast


# Validate img path and file type
def is_valid_img_path(im_path):
    return os.path.exists(im_path) and os.path.isfile(im_path) and os.path.splitext(im_path)[1].lower() in [".png",
                                                                                                            ".jpeg",
                                                                                                            ".jpg",
                                                                                                            ".webp"]


# Format byte size to human-readable format
def format_byte_count(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


# Main application class
class ImageQualityModifier:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = display.set_mode((640, 480), flags=pygame.RESIZABLE)
        try:
            pygame.display.set_caption("Image Quality Modifier", "Image Quality Modifier")
        except Exception as e:
            print(e)

        self.__all_text_color = (255, 255, 255)
        self.__bg_color = (22, 22, 22)

        self.is_dragging_on_slider = True
        self.was_save_btn_pressed = False

        self.img_quality = 0
        self.predicted_img_size = None
        self.imgRenderPos = (100, 100)
        self.img_render_size = (0, 0)
        self.img_original_res = (0, 0)
        self.new_img_res = (0, 0)
        self.img_extension = None
        self.img_path = None
        self.modified_img_path = None

        self.information_text_box_size = 0
        self.font = pygame.font.SysFont(None, 30)
        self.pad = 20
        self.img_information = {"Original Image Resolution": "", "New Image Resolution": "", "Save path": "",
                                "Size": ""}

        self.drag_delta = (0, 0)
        self.zoom = 1.0
        self.MIN_ZOOM = 0.3
        self.MAX_ZOOM = 5.0

        self.is_dragging = False

        # maintain a copy of original image in memory to allow fast resizing
        self.original_img_surface = None
        # this image surface is constantly modified
        self.active_img_surface = None
        save_btn_pos = self.screen.get_width() - 100 - self.pad, self.screen.get_height() - 40 - self.pad
        self.save_btn = Button((75, 104, 250), (88, 116, 252), (0, 0, 0), self.font, "Save",
                               (100, 40), save_btn_pos)
        self.toast = Toast("Drag an img here", self.font, 3, (255, 255, 255), (0, 0, 0))
        self.resolution_slider = Slider((100, 100, 100), (190, 190, 190), (0, 0, 0), self.font, 1, 100, 100,"Quality:100%")

        # show "Drag an image here" message on app launch
        self.toast.show()

    def update(self):
        pad = self.pad

        # slider
        mouse_pos = pygame.mouse.get_pos()
        screen_size = self.screen.get_size()
        slider_size = (screen_size[0] - self.save_btn.size[0] - pad * 2, self.resolution_slider.size[1])
        slider_y_pos = min(screen_size[1] - slider_size[1] - 10, screen_size[1] - slider_size[1])
        slider_x_pos = (screen_size[0] - slider_size[0]) / 2 - self.save_btn.size[0] / 2

        self.resolution_slider.setPos(slider_x_pos, slider_y_pos)
        self.resolution_slider.setSize(slider_size[0], slider_size[1])

        # update save button position
        self.save_btn.setPos(self.resolution_slider.pos[0] + self.resolution_slider.size[0] + 10,
                             self.resolution_slider.pos[1])

        if self.resolution_slider.containsPoint(mouse_pos[0], mouse_pos[1]) or self.is_dragging_on_slider:
            # initialVal = None
            if pygame.mouse.get_pressed()[0]:
                # self.resolution_slider.value
                # add dragging functionality
                ratio = (mouse_pos[0] - self.resolution_slider.pos[0]) / self.resolution_slider.size[0]
                self.resolution_slider.setValueRatio(ratio)
                self.is_dragging_on_slider = True
            else:
                if self.is_dragging_on_slider and self.active_img_surface is not None:
                    ratio = self.resolution_slider.value / self.resolution_slider.max_val
                    print(ratio)
                    self.new_img_res = (
                        int(self.img_original_res[0] * ratio), int(self.img_original_res[1] * ratio))

                    # self.reloadImage(self.imgPath)
                    self.active_img_surface = transform.scale(self.original_img_surface, self.new_img_res)
                    bytes_arr = io.BytesIO()
                    image.save(self.active_img_surface, bytes_arr, self.img_extension)
                    self.img_information["Size"] = (format_byte_count(len(bytes_arr.getvalue())))

                    self.active_img_surface = transform.scale(self.active_img_surface, self.img_render_size)

                    self.resolution_slider.setText("Quality : " + str(self.resolution_slider.value) + "%")
                    print(self.img_original_res, "->", self.new_img_res)
                    self.img_information["New Image Resolution"] = str(self.new_img_res[0]) + "x" + str(
                        self.new_img_res[1])
                self.is_dragging_on_slider = False

        # recalculate image size and position
        if self.active_img_surface is not None:

            aspect_ratio = self.img_original_res[0] / self.img_original_res[1]

            new_width = min(self.screen.get_width() - pad, int((self.screen.get_height() - self.information_text_box_size - self.resolution_slider.size[1] - 2 * pad) * aspect_ratio)) * 0.9
            new_height = min(self.screen.get_height() - self.information_text_box_size - self.resolution_slider.size[1] - 2 * pad, int((self.screen.get_width() - pad) / aspect_ratio)) * 0.9
            self.img_render_size = (abs(round(new_width * self.zoom)), abs(round(new_height * self.zoom)))

            x = self.drag_delta[0] + (self.screen.get_width() - self.img_render_size[0]) / 2
            y = self.drag_delta[1] + self.information_text_box_size / 2 + (
                    self.screen.get_height() - self.img_render_size[1]) / 2 - pad
            self.imgRenderPos = (x, y)

        if self.is_dragging:
            delta = pygame.mouse.get_rel()
            self.drag_delta = (self.drag_delta[0] + delta[0], self.drag_delta[1] + delta[1])
        else:
            self.drag_delta = (0, 0)

    def save_img(self):
        try:
            if self.original_img_surface is not None and self.modified_img_path is not None:
                print("Saving img to", self.modified_img_path)
                pygame.image.save(transform.scale(self.original_img_surface, self.new_img_res), self.modified_img_path,
                                  self.img_extension)
                self.toast.show("Image saved")
        except Exception as e:
            self.toast.show("Error occured:" + str(e))

    def render(self):
        self.screen.fill(self.__bg_color)

        border_width = 10
        if self.active_img_surface is not None:
            if (self.img_render_size[0] != self.active_img_surface.get_width()
                    or self.img_render_size[1] != self.active_img_surface.get_height()):
                print("Rendering surface in", self.img_render_size)
                self.active_img_surface = transform.scale(self.original_img_surface, self.img_render_size)
                self.img_render_size = (self.active_img_surface.get_width(), self.active_img_surface.get_height())
                self.active_img_surface = transform.scale(self.original_img_surface, self.new_img_res)
                self.active_img_surface = transform.scale(self.active_img_surface, self.img_render_size)

            draw.rect(self.screen, (0, 0, 0), rect=(
                self.imgRenderPos[0] - border_width, self.imgRenderPos[1] - border_width,
                self.img_render_size[0] + 2 * border_width, self.img_render_size[1] + 2 * border_width),
                      border_radius=10)
            self.screen.blit(self.active_img_surface, self.imgRenderPos)
        self.resolution_slider.setText("Quality: " + str(self.resolution_slider.value) + "%")
        self.resolution_slider.draw(self.screen)
        self.save_btn.draw(self.screen)
        self.toast.draw(self.screen)
        self.draw_text()

    # used for loading img for first time
    def load_img(self, path):
        try:
            if is_valid_img_path(path):
                self.img_path = path
                # make
                self.modified_img_path = os.path.join(os.path.dirname(self.img_path),
                                                      'modified_' + os.path.basename(self.img_path))

                self.img_extension = os.path.splitext(self.modified_img_path)[1].lower()
                self.active_img_surface = pygame.image.load(self.img_path)

                self.original_img_surface = pygame.image.load(self.img_path)

                self.img_original_res = (self.active_img_surface.get_width(), self.active_img_surface.get_height())
                self.img_render_size = self.img_original_res
                self.new_img_res = (self.active_img_surface.get_width(), self.active_img_surface.get_height())

                self.resolution_slider.setValue(self.resolution_slider.max_val)
                self.img_information["Save path"] = self.modified_img_path
                self.img_information["Original Image Resolution"] = f"{self.img_original_res[0]}x{self.img_original_res[1]}"
                self.img_information["New Image Resolution"] = f"{self.new_img_res[0]}x{self.new_img_res[1]}"
                # reads all bytes in image into a byte array and the uses its length to get size of image
                bytes_arr = io.BytesIO()
                pygame.image.save(self.original_img_surface, bytes_arr, self.img_extension)
                self.img_information["Size"] = (format_byte_count(len(bytes_arr.getvalue())))

                print(f"Loaded {self.img_path} {self.modified_img_path}")
            else:
                self.toast.show(f"Invalid img: {os.path.basename(path)}")
        except Exception as e:
            self.toast.show("Error occurred:" + e.args[0])

    # used for reloading the img: occurs when its resolution has been modified
    def reload_img(self, path):
        if is_valid_img_path(path):
            self.img_path = path
            # adds modified_ as suffix for the name the img will be saved as
            self.modified_img_path = os.path.join(os.path.dirname(self.img_path),  'modified_' + os.path.basename(self.img_path))
            self.active_img_surface = pygame.image.load(self.img_path)

            print("Reloaded ", self.img_path, self.modified_img_path)
        else:
            self.toast.show("Image was not found " + str(path))

    def draw_text(self):
        y = 10
        render_area = (self.screen.get_width() - self.pad * 2, self.screen.get_height())
        for key, value in self.img_information.items():
            text = str(key) + " : " + str(value)
            if self.font.size(text)[0] > render_area[0]:
                while self.font.size(text + "...")[0] > render_area[0]:
                    text = text[:-1]
                text += "..."
            self.screen.blit(self.font.render(text, True, self.__all_text_color), (self.pad, y))
            y += self.font.get_height()
        self.information_text_box_size = y

    def handle_event(self, event_data):
        if event_data.type == pygame.DROPFILE:
            self.load_img(event_data.dict["file"])
        # checks if save button was pressed
        elif event_data.type == pygame.MOUSEBUTTONDOWN:
            if event_data.dict["button"] == 1:
                pos = event_data.dict["pos"]
                if self.save_btn.containsPoint(pos[0], pos[1]):
                    self.was_save_btn_pressed = True
            elif event_data.dict["button"] == 3:
                pygame.mouse.get_rel()
                self.is_dragging = True

        # Checks if save button was released
        elif event_data.type == pygame.MOUSEBUTTONUP:
            pos = event_data.dict["pos"]
            if self.was_save_btn_pressed and self.save_btn.containsPoint(pos[0], pos[1]):
                self.save_img()
                self.was_save_btn_pressed = False

            self.is_dragging = False

        elif event_data.type == pygame.MOUSEWHEEL:
            delta = event_data.dict["precise_y"]
            self.zoom += 0.5 * delta
            if self.zoom < self.MIN_ZOOM:
                self.zoom = self.MIN_ZOOM
            if self.zoom > self.MAX_ZOOM:
                self.zoom = self.MAX_ZOOM
            print(self.zoom)

    def loop(self):
        max_fps = 60
        min_frame_time = 1e9 / max_fps

        t1 = time.time_ns()
        stop = False

        # FPS = 60
        # time_accumulated = 0
        while not stop:
            for e in event.get():
                if e.type == pygame.QUIT:
                    stop = True
                else:
                    self.handle_event(e)
            t2 = time.time_ns()
            dt = t2 - t1
            if dt < min_frame_time:
                continue
            self.update()
            self.render()
            display.update()
            t1 = t2


if __name__ == "__main__":
    try:

        print(
            "----------------------------Running ImageQualityModifier--------------------------------")
        ImageQualityModifier().loop()

    except Exception as e:
        print("Error occurred: " + str(e))
