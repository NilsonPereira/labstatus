from tango.server import Device, attribute, command
import threading
import time
import tango

class nmdev(Device):
    title = attribute(dtype=str, access=tango.READ_WRITE)
    var01 = attribute(dtype='float', access=tango.READ_WRITE)
    var01_label = attribute(dtype=str, access=tango.READ_WRITE)
    var02 = attribute(dtype='float', access=tango.READ_WRITE)
    var02_label = attribute(dtype=str, access=tango.READ_WRITE)
    progress = attribute(dtype='float', access=tango.READ_WRITE)
    varstatus = attribute(dtype=str, access=tango.READ_WRITE)

    attribute_list = ['title', 'var01', 'var01_label', 'var02', 'var02_label', 'progress', 'varstatus', 'State', 'Status']

    ## tango attribute read functions
    def read_title(self): return self._title
    def read_var01(self): return self._var01
    def read_var01_label(self): return self._var01_label
    def read_var02(self): return self._var02
    def read_var02_label(self): return self._var02_label
    def read_progress(self): return self._progress
    def read_varstatus(self): return self._varstatus
    
    ## tango attribute write functions
    def write_title(self, value): 
        self._title = str(value)
        self.push_change_event('title', self._title)
    def write_var01(self, value): 
        self._var01 = float(value)
        self.push_change_event('var01', self._var01)
    def write_var01_label(self, value): 
        self._var01_label = str(value)
        self.push_change_event('var01_label', self._var01_label)
    def write_var02(self, value): 
        self._var02 = float(value)
        self.push_change_event('var02', self._var02)
    def write_var02_label(self, value):
        self._var02_label = str(value)
        self.push_change_event('var02_label', self._var02_label)
    def write_progress(self, value):
        self._progress = float(value)
        self.push_change_event('progress', self._progress)
    def write_varstatus(self, value):
        self._varstatus = str(value)
        self.push_change_event('varstatus', self._varstatus)

    @command()
    def reset_all(self):
        self.write_title(" ")
        self.write_var01(0.0)
        self.write_var01_label(" ")
        self.write_var02(0.0)
        self.write_var02_label(" ")
        self.write_progress(0.0)
        self.write_varstatus(" ")

    ## init variables
    _title = " "
    _var01 = 0.0
    _var01_label = " "
    _var02 = 0.0
    _var02_label = " "
    _progress = 0.0
    _varstatus = " "

    def init_device(self):
        super().init_device()
        for attr in self.attribute_list:
            self.set_change_event(attr,True,False)
        #self.set_change_event('var01',True,False)         
        self.set_state(tango.DevState.ON)
        #self.t = threading.Thread(target=self.update_loop)
        #self.t.start()

if __name__ == "__main__":
    nmdev.run_server()
    print("ok")
