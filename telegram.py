#from collections import UserDict
class Diskinfo():
    def __init__(self, space='', freespace='', volumn=''):
        self._space=space[0:5]
        self._freespace=freespace[0:5]
        self._volumn=volumn[0:10]
    @staticmethod
    def get_length():
        return 21
    def encoding(self, name):
        return "%1s%-5s%-5s%-10s" % (name, self._space, self._freespace, self._volumn) if len(self._space.strip()) > 0 else ""
    def encoding_all(self, name):
        return "%1s%-5s%-5s%-10s" % (name, self._space, self._freespace, self._volumn)
    @staticmethod
    def decoding(disk_info):
        result = Diskinfo()
        result._space=disk_info[1:6]
        result._freespace=disk_info[6:11]
        result._volumn=disk_info[11:21]
        return result

class Telegram(dict):
    def __init__(self, hostname='', cpu_usage=''):
        self._hostname=hostname
        self._cpu_usage=cpu_usage
        self._version='INFO0001'
        for i in range(65,91):
            self[chr(i)] = Diskinfo()
    def get_version(self):
        return self._version
    def set_hostname(self, hostname):
        self._hostname = hostname[0:10]
    def set_cpu_usage(self, cpu_usage):
        self._cpu_usage = cpu_usage[0:2]
    def encoding_disk(self, all_disk = False):
        ret=str(len(self)).rjust(2,'0')
        for name, info in self.items():
            ret += (info.encoding_all(name) if all_disk else info.encoding(name))
        return ret
    def encoding(self, all_disk=False):
        return "%-10s%4s%2s" % (self._hostname, self.get_version(), self._cpu_usage) + self.encoding_disk(all_disk)
    @staticmethod
    def decoding(telegram):
        result = Telegram()
        result.set_hostname(telegram[0:10])
        result._version=telegram[10:18]
        result.set_cpu_usage(telegram[18:20])
        num = telegram[20:22]
        offset = 22
        while offset < len(telegram):
            result[telegram[offset]]=Diskinfo.decoding(telegram[offset:])
            offset += Diskinfo.get_length()

        return result

#a = Telegram()
#a.set_hostname("Host")
#a.set_cpu_usage('66')
#a['C'] = Diskinfo('123', '10', 'JUAN')
#a['D'] = Diskinfo('12345', '10123', 'JUANBBBB')
#print(a.encoding())
#encoded = a.encoding()
#b = Telegram.decoding(encoded)
#print(b.encoding(all_disk=True))

    
