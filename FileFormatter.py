#! /usr/bin/python3
# -*- coding:utf-8 -*-
# apt-get install p7zip-full
from msilib.schema import CheckBox
import threading
from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivymd.uix.picker import MDDatePicker
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from functools import partial
from kivymd.uix.tooltip import MDTooltip
from plyer import filechooser
import pyperclip
import subprocess
import os
import math
import logzero
import shutil
import platform

logger = logzero.logger
MAX_SPLIT_SIZE = 2000

z_install = r"C:\Program Files\7-Zip\7z.exe"
z_win = r"7zwin/7za.exe"
z_mac = r"7zmac/7zz"
cwd = os.getcwd()
if platform.system() == "Windows":
    if os.path.exists(z_install):
        z_path = z_install
    else:
        z_path = os.path.join(cwd, z_win)
elif platform.system() == "Mac":
    z_path = os.path.join(cwd, z_mac)

KV = """
#:import rgba kivy.utils.rgba
<TooltipCheckbox@CheckBox+MDTooltip>
<TooltipMDLabel@MDLabel+MDTooltip>
<LogLabel@RelativeLayout>:
    # using a boxlayout here allows us to have better control of the text
    # position
    text: ''
    index: None
    Label:
        y: 0
        x: 5
        size_hint: None, None
        size: self.texture_size
        padding: dp(5), dp(5)
        color: rgba("#3f3e36")
        text: root.text
        canvas.before:
            Color:
                rgba: rgba("#dbeeff")
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: dp(5), dp(5)

<Properties@GridLayout>:
    cols: 2
    spacing: dp(2)
    row_force_default: True
    row_default_height: 30
    MDLabel:
        size_hint_x: None
        width: 125
        text: 'Type:'
    GridLayout:
        cols: 7
        MDLabel:
            text: 'Monthly'
            halign: "right"
            size_hint: 0.55, 1
        CheckBox:
            group: "type_selector"
            active: True
            size_hint: 0.2, 1
            on_active: app.checkbox_click(self, self.active, "Monthly")
        MDLabel:
            text: 'Kickstarter'
            halign: "right"
            size_hint: 0.75, 1
        CheckBox:
            group: "type_selector"
            size_hint: 0.2, 1
            on_active: app.checkbox_click(self, self.active, "Kickstarter")
        MDLabel:
            text: 'Trove'
            halign: "right"
            size_hint: 0.5, 1
        CheckBox:
            group: "type_selector"
            size_hint: 0.2, 1
            on_active: app.checkbox_click(self, self.active, "Trove")
        MDLabel:
            text: ''
            size_hint: 2, 1
    MDLabel:
        size_hint_x: None
        width: 125
        text: 'Creator:'
    BoxLayout:
        orientation: 'horizontal'
        MDLabel:
            text: ''
            size_hint_x: None
            width: 25
        TextInput:
            id: creator_entry
            font_size: 16
            multiline: False
            write_tab: False
            hint_text: 'E.G. Lord of the Print'
    MDLabel:
        size_hint_x: None
        width: 125
        text: 'Date:'
        opacity: 1 if app.type_entry == "Monthly" else 0
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(2)
        opacity: 1 if app.type_entry == "Monthly" else 0
        MDLabel:
            text: ''
            size_hint_x: None
            width: 25
        MDLabel:
            id: date_string
            text: app.date_string
            pos_hint: {'center_x': .95, 'center_y': .4}
        MDRaisedButton:
            text: "Open Date Picker"
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release: app.show_date_picker()
    MDLabel:
        size_hint_x: None
        width: 125
        text: 'Description:'
    BoxLayout:
        orientation: 'horizontal'
        MDLabel:
            text: ''
            size_hint_x: None
            width: 25
        TextInput:
            id: description_entry
            font_size: 16
            multiline: False
            write_tab: False
            hint_text: 'optional' if app.type_entry == "Monthly" else 'E.G. wing bits'
    TooltipMDLabel:
        size_hint_x: None
        width: 125
        text: 'Repack Zip:'
        tooltip_text: 'Extract files then rezip in 2GB parts'
    BoxLayout:
        id: zipbox
        TooltipCheckbox:
            id: rezip
            active: True
            size_hint: 0.1, 1
            tooltip_text: 'Extract files then rezip in 2GB parts'
        TooltipMDLabel:
            text: 'Delete Old Zip:'
            size_hint: 0.49, 1
            halign: "right"
            tooltip_text: 'If enabled original zip will be deleted, otherwise it will be renamed to *-old'
        TooltipCheckbox:
            id: delete_after
            active: True
            size_hint: 0.4, 1
            tooltip_text: 'If enabled original zip will be deleted, otherwise it will be renamed to *-old'
    TooltipMDLabel:
        text: 'Compression:'
        tooltip_text: 'How much 7zip will attempt to compress the files. low is faster, high makes a smaller zip'
        width: 125
        size_hint_x: None
    GridLayout:
        cols: 7
        TooltipMDLabel:
            text: 'Low'
            halign: "right"
            size_hint: 0.35, 1
            tooltip_text: 'How much 7zip will attempt to compress the files. low is faster, high makes a smaller zip'
        CheckBox:
            group: "zip_selector"
            on_active: app.zip_checkbox_click(self, self.active, "-mx=1")
            size_hint: 0.2, 1
        TooltipMDLabel:
            text: 'Medium'
            halign: "right"
            size_hint: 0.8, 1
            tooltip_text: 'How much 7zip will attempt to compress the files. low is faster, high makes a smaller zip'
        CheckBox:
            group: "zip_selector"
            on_active: app.zip_checkbox_click(self, self.active, "-mx=5")
            size_hint: 0.2, 1
        TooltipMDLabel:
            text: 'High'
            halign: "right"
            size_hint: 0.6, 1
            tooltip_text: 'How much 7zip will attempt to compress the files. low is faster, high makes a smaller zip'
        CheckBox:
            group: "zip_selector"
            active: True
            on_active: app.zip_checkbox_click(self, self.active, "-mx=9")
            size_hint: 0.2, 1
        MDLabel:
            text: ''
            size_hint: 2, 1
    MDLabel:
        size_hint_x: None
        width: 125
        text: 'Telegram Tags:'
        opacity: 0 if not app.telegram_tags else 1
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(2)
        opacity: 0 if not app.telegram_tags else 1
        MDLabel:
            text: ''
            size_hint_x: None
            width: 25
        MDLabel:
            text: app.telegram_tags
            pos_hint: {'center_x': .95, 'center_y': .4}
        MDRaisedButton:
            text: "Copy"
            pos_hint: {'center_x': .5, 'center_y': .5}
            on_release:
                app.copy_click()
    MDRaisedButton:
        text: 'Browse'
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_load()
    MDLabel:
        text: ""
    

GridLayout:
    cols: 1
    spacing: dp(2)
    Properties:
        id: properties
    Label:
        opacity: 1 if not app.data else 0
        size_hint_y: None
        text: 'Drag & Drop files here'    
    FixedRecycleView:
        size_hint: 1,2
        id: rv
        data: app.data
        viewclass: 'LogLabel'
        RecycleBoxLayout:
            id: box
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            default_size: 0, 48
            default_size_hint: 1, None
            spacing: dp(1)
    AnchorLayout:
        size_hint: 1, .15
        MDRaisedButton:
            text: 'convert'
            on_press: app.convert()
            size_hint: 0.5, 1


<PopupBox>:
    pop_up_text: _pop_up_text
    size_hint: .5, .5
    auto_dismiss: False
    title: 'Status'   

    BoxLayout:
        orientation: "vertical"
        Label:
            id: _pop_up_text
            text: ''
"""


def file_extract_7z(file_path, extract_path):
    cmd_7z = [z_path, "x", "-o{}".format(extract_path), file_path]
    proc = subprocess.Popen(cmd_7z, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    logger.info("7z output | {}".format(out.decode("utf-8")))
    if b"Everything is Ok" not in out:
        logger.error("7z output | {}".format(out.decode("utf-8")))
        logger.error("7z error | {}".format(err.decode("utf-8")))


def file_split_7z(folder_path, compression_level, split_size=MAX_SPLIT_SIZE):
    file_path_7z_list = []
    # if origin file is 7z file rename it
    origin_file_path = ""
    if os.path.splitext(folder_path)[1] == ".7z":
        origin_file_path = folder_path
        folder_path = os.path.splitext(origin_file_path)[0] + ".7zo"
        os.rename(origin_file_path, folder_path)
    # do 7z compress
    pathsize = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            pathsize += os.path.getsize(fp)
    fz = pathsize / 1024 / 1024
    pa = math.ceil(fz / split_size)
    archive_head = folder_path + ".7z"
    for i in range(pa):
        check_file_name = "{}.{:03d}".format(archive_head, i + 1)
        if os.path.isfile(check_file_name):
            logger.debug("remove exists file | {}".format(check_file_name))
            os.remove(check_file_name)
    cmd_7z = [z_path, "a", "-v{}m".format(split_size), "-y", "-m0=lzma", "{}".format(compression_level), "-mfb=64", "-md=32m", "-ms=on",
              archive_head, folder_path]
    proc = subprocess.Popen(cmd_7z, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    logger.debug("7z output | {}".format(out.decode("utf-8")))
    if b"Everything is Ok" not in out:
        logger.error("7z output | {}".format(out.decode("utf-8")))
        logger.error("7z error | {}".format(err.decode("utf-8")))
        return file_path_7z_list

    for i in range(pa):
        check_file_name = "{}.{:03d}".format(archive_head, i + 1)
        if os.path.isfile(check_file_name):
            file_path_7z_list.append(check_file_name)
    # if origin file is 7z file rename it back
    if len(file_path_7z_list) == 1:
        os.rename(file_path_7z_list[0], archive_head)
    return file_path_7z_list


def do_file_split(file_path, split_size=MAX_SPLIT_SIZE):
    """caculate split size
       example max split size is 1495 file size is 1500
       than the split part num should be int(1500 / 1495 + 0.5) = 2
       so the split size should be 1000 + 1000 but not 1495 + 505
       with the file size increase the upload risk would be increase too
    """
    file_size = os.path.getsize(file_path) / 2 ** 20
    split_part = math.ceil(file_size / split_size)
    new_split_size = math.ceil(file_size / split_part)
    logger.debug("file size | {} | split num | {} | split size | {}".format(file_size, split_part, new_split_size))
    file_path_7z_list = file_split_7z(file_path, split_size=new_split_size)
    return file_path_7z_list


class FixedRecycleView(RecycleView):
    pass


class PopupBox(Popup):
    pop_up_text = ObjectProperty()

    def update_pop_up_text(self, p_message):
        self.pop_up_text.text = p_message
        
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Application(MDApp):
    data = ListProperty()
    date_entry = ObjectProperty()
    date_string = ObjectProperty()
    type_entry = ObjectProperty()
    telegram_tags = ObjectProperty()
    loadfile = ObjectProperty(None)
    zip_level = ObjectProperty()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Window.bind(on_drop_file=self._on_file_drop)
        self.date_entry = datetime.now()
        self.date_string = self.date_entry.strftime("%Y.%m")
        self.type_entry = "Monthly"
        self.telegram_tags = ""
        self.zip_level = "-mx=9"
        return Builder.load_string(KV)

    def _on_file_drop(self, window, file_path, var2, var3):
        self.data.append({
            'index': len(self.data),
            'text': file_path.decode('UTF-8')
        })
        return

    def show_load(self):
        files = filechooser.open_file(title="Choose files..", multiple=True,
                             filters=[("All Files", "*.*")])
        for path in files:
            self.data.append({
                'index': len(self.data),
                'text': path
        })

    def zip(self, file):
        filename = os.path.basename(file)
        filename_no_ext = os.path.splitext(filename)[0]
        filename_ext = os.path.splitext(filename)[1]
        extract_path = os.path.dirname(file)
        extract_path = os.path.join(extract_path, filename_no_ext)
        if self.root.ids.properties.ids.rezip.active:
            try:
                self.pop_up.update_pop_up_text('extracting archive...')
                if os.path.exists(extract_path):
                    shutil.rmtree(extract_path)
                file_extract_7z(file, extract_path)
                logger.info("archive extracted")
            except Exception as e:
                logger.error("exception while extracting archive: {}".format(e))
                return
            try:
                #rename or delete the original file to avoid name conflict
                if self.root.ids.properties.ids.delete_after.active:
                    os.remove(file)
                else:
                    os.rename(file,extract_path+"-old"+filename_ext)
                self.pop_up.update_pop_up_text('recompressing archive...')
                file_split_7z(extract_path, self.zip_level)
                logger.info("archive created")
            except Exception as e:
                logger.error("exception while recompressing archive: {}".format(e))
                return
            # os.remove(extract_path)
            logger.info("cleaning up temp files: {}".format(extract_path))
            shutil.rmtree(extract_path)
            # os.remove(file_backup)

    def process(self):
        self.format_files()
        self.data.clear()
        logger.info("data cleared")
        self.pop_up.dismiss()
        logger.info("popup closed")

    def convert(self):
        description = self.root.ids.properties.ids.description_entry.text
        creator = self.root.ids.properties.ids.creator_entry.text
        if (self.type_entry == "Monthly" or self.type_entry == "Kickstarter") and not creator:
            return
        if self.type_entry == "Trove" and (not creator or not description):
            return
        self.show_popup()
        thread = threading.Thread(target=self.process)
        thread.start()

    def show_popup(self):
        self.pop_up = PopupBox()
        self.pop_up.open()
        logger.info("popup open")

    def format_files(self):
        image_index = 0
        image_count = 0
        zip_index = 0
        zip_count = 0

        # just a check if we have multiple zips/images so we don't add descriptions for no reason
        for x in self.data:
            file = (x.get('text'))
            extension = os.path.splitext(file)[1]
            if extension.lower() == ".png" or extension.lower() == ".jpg":
                image_count += 1
            if ".zip" == extension.lower() or ".rar" == extension.lower() or ".7z" == extension.lower():
                zip_count += 1
        for x in self.data:
            file = (x.get('text'))
            parent_dir = os.path.dirname(file)
            extension = os.path.splitext(file)[1]
            description = self.root.ids.properties.ids.description_entry.text
            creator = self.root.ids.properties.ids.creator_entry.text

            if (extension.lower() == ".png" or extension.lower() == ".jpg") and image_count > 1:
                description += str(image_index)
                image_index += 1
            if (".zip" == extension.lower() or ".rar" == extension.lower() or ".7z" == extension.lower()) and zip_count > 1:
                description += str(zip_index)
                zip_index += 1
            if self.type_entry == "Monthly":
                if description:
                    filename = "{}-{}-{}-{}".format(self.type_entry, creator, self.date_entry.strftime("%Y.%m"),
                                                    description)
                else:
                    filename = "{}-{}-{}".format(self.type_entry, creator, self.date_entry.strftime("%Y.%m"))
                tags = "#{} #{} #{}".format(self.type_entry, self.date_entry.strftime("%Y%b"), creator.replace(" ", ""))
                Clock.schedule_once(partial(self.set_telegram_tag_property, tags))
            else:
                if description:
                    filename = "{}-{}-{}".format(self.type_entry, creator, description)
                else:
                    filename = "{}-{}".format(self.type_entry, creator)
                tags = "#{} #{}".format(self.type_entry, creator.replace(" ", ""))
                Clock.schedule_once(partial(self.set_telegram_tag_property, tags))
            final_path = os.path.join(parent_dir, filename + extension)
            try:
                logger.debug("renaming: {}\nto: {}".format(file, final_path))
                os.rename(file, final_path)
                if ".zip" == extension.lower() or ".rar" == extension.lower() or ".7z" == extension.lower():
                    self.zip(final_path)
            except Exception as e:
                logger.error("exception renaming file: {}".format(e))

    def date_picker_on_save(self, instance, value, date_range):
        self.date_entry = value
        self.date_string = value.strftime("%Y.%m")

    def date_picker_on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.date_picker_on_save, on_cancel=self.date_picker_on_cancel)
        date_dialog.open()

    def checkbox_click(self, instance, value, type):
        if value:
            self.type_entry = type

    def zip_checkbox_click(self, instance, value, level):
        if value:
            self.zip_level = level

    # this may only be called from the main kivy thread
    def set_telegram_tag_property(self, value, *largs):
        self.telegram_tags = value

    def copy_click(self):
        pyperclip.copy(self.telegram_tags)

Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Application().run()
