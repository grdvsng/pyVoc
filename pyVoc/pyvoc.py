''' Module: pyvoc
    Author: Sergey Trishkin
    Version: 1.0.0.0
    Description: Module for create and read special pyvoc formate.
    Used module: os.
   
    Pyvoc format:    
    |--------------------------------| Hierarchy: 
    |<Zone = "Zone name">            | Foo.pyvoc - every document has any zones, categories, nodes.                             
    |    <Category = "Category name">|  ||               
    |        <KeyI  = Value>         |  \/                
    |        <KeyII = Value>         | Zones - every zone has any Categories.
    |        <... = ...>             |  ||
    |    </Category>                 |  \/
	|<... = ...>                     | Categories - every category has any nodes. 
	|	<... = ...>                  |  ||
	|</Zone>                         |  \/
    |--------------------------------| Nodes - every node has key and value.

    Pyvoc syntax:
    __________________________
    |Operators:              |
    |< - line start;         |
    |> - line close;         | 
    |= - assignment operator.|
    |<\...> - close element* |
    |*for zones & categories.|
    |________________________|
    |Tabulation (use space): |
    |0 - zones;              |
    |4 - categories;         |
    |8 - nodes.              |
    |________________________|
    
    Example:
    <zone = Work>
        <category = Office>
            <John = chef>
            <Bob = colleague>
            <Steve = friend>
        </category>
	</category>
    
    For information:
    I   Pyvoc only use just string or number;
    II  Tabulation unrequired;
    III Only zones and categories start with '=', but node will use only key.
    
'''

class Vocabulary(object):
    ''' Class Vocabulary self object.
    attributes:
            errors    - module special list with errors;
            map       - special diction with pyvoc node;
            file_path - path of pyvoc document;
            name      - name of exemplar;
            zone      - the main node of pyvoc format.
    modules:
            __init__(pyvoc, name) - constructor;
            
            __read()                   - read document;
            __write(self, pyvoc, path) - write self.map on pyvoc format;
                private method used with __read and __write:
                __striper(list);
                __check(self, z, c, k, param, R).

            __errors(key, value) - error catcher;   
            __str__()            - formate pyvoc document in console;
            __call__(zone, category, key) - return method get;
            
            add_zone(zone)               - create new zone;
            add_category(zone, category) - create new category in zone;
            add_key(zone, category, key, val) - create new node in category;      
            add(zone, category, key, value)   - append new zone, category and node;
            create(self, path, name)          - create new pyvoc document;
            delete(zone, category, key)       - delete same element from pyvoc;
            get(zone, category, key) - find some nodes in pyvoc;
            set(zone, category, key, val) - set same node value;
            
    '''
    
    errors = {0: "File not found. Please, try append 'r' before string (r'path').",
              1: "Zone not found, please check value.",
              2: "Category not found, please check value.",
              3: "Key not found, please check value.",
              4: "File not assigned.",
              5: "You must set document, early than append positions.",
              6: "{} with name: '{}', already exists.",
              7: "{} with name: '{}', not exists.",
              8: "Incorrect text. Please, try append 'r' before string (r'path').",
              9: "File is already exists, please, change name."}
    
    map = {}
    
    def __init__(self, pyvoc=None, name='PyVoc'):
        ''' Method __init__ Class Vocabulary.
            Parameters: 
                        pyvoc = document path(required).
                        name = special name for document if need this.
                        
        '''
        self.file_path = abspath(pyvoc)  ## Абсолютный адрес докуммента.
        self.name = name                 ## Имя докуммента.
        self.zone = []                   ## Список содержащий все зоны докуммента.
        
        if pyvoc == None: self.file_path = None                  ## Режим для создания файла.
        elif not exists(self.file_path): self.__errors(0, pyvoc) ## Файл не найден.
        else: self.__read()                                      ## Файл найден.
    
    def __read(self):
        ''' Class Vocabulary method __read.
            read pyvoc document and append nodes in self.map and self.zone. 
            
        '''
        
        # Переменные нужны для обнуления результатов обработки доккументов.
        temp = true_zone = true_category = '' 
        # При обработки доккумента когда начинается регион документа для чтения.
        listen = False                     
        # Открываем файл для обработки.
        file = open(self.file_path)

        z = c = v = None
        for i in file.read():                   
            if i == '<': listen = True          # < - символ начала чтение символов в доккументе.
            if i == '>' or i == '/':            # / or > - символ закрытия региона.
                if temp != '': 
                    temp = temp.split('=')      # Разделяем значение, [0] - ключ/регион, [1] - значение.
                    temp = self.__striper(temp) # Очищаем переменную от "лишних" знаков.
                    
                    # Далее следует обработка полученных значений в соответствии с регионо и последующее распределение.
                    if temp[0] == 'zone':
                        true_zone = temp[1]
                        self.map[true_zone] = {}
                        
                    elif temp[0] == 'category': 
                        true_category = temp[1]
                        self.map[true_zone][true_category]={}
                    
                    else: self.map[true_zone][true_category][temp[0]] = temp[1]
                
                listen = False 
                temp = ''
            
            if listen and i != '<': temp += i # Добавляем допустимый символ из документа. 
        file.close()

    def __striper(self, list):
        ## Замена начальных и конечных пробелов.
        n = 0
        
        for i in list:
            cur = i.rstrip()
            cur = cur.lstrip()
            list[n] = cur
            
            n += 1
        
        return list
    
    def __errors(self, key, value=None):
        ## Метод возвращает ошибки, которые могут возникнуть в процессе выполнения.
        line = '\n{}\n'.format('--'*40)
        val = '{0}\t{1}'.format(line, self.errors[key])
        
        if key == 6 or key == 7: 
            val = self.errors[key].format(value[0], value[1])
            raise ValueError('{1}{0}{1}'.format(val, line))
            
        if value != None: val += "\n\tError in value: '{1}'.{0}".format(line, value)
        else: val += line
        
        raise ValueError('%s' % val)
    
    def __check(self, z, c=None, k=None, param=3, R=True):
        ## Проверят ключевые значения документа, значение param уровень проверки (1-4).
        n = 0
        
        v = [None, z, c, k]
        
        try: 
            temp = self.map[z]; n += 1
            temp = self.map[z][c]; n += 1
            temp = self.map[z][c][k]; n += 1
        except: pass
        
        if param != n:     
            if R: return self.__errors(param, v[n])
            else: return True
        return False
        
    def get(self, zone=None, category=None, key=False):
        ''' Method get Class Vocabulary.
            Parameters: 
                        zone - zone of document (required). 
                        category - category of zone (required).
                        key - key of category nodes (unrequited).
            
            if key == None and not errors: return diction with all keys and values.
            
        '''
        
        ## Проверяем параметры на ошибки.
        if self.file_path == None: return self.__errors(4)
        if category == None or zone == None: return 'You must enter zone and category too search. '  
        
        if key: test = self.__check(zone, category, key, 3) # Прорверка уровня 3.
        else: test = self.__check(zone, category, 2)        # Прорверка уровня 2.
        if test: return test # Если при проверке найдены ошибки.
        
        if key: return self.map[zone][category][key] # Если ключ задан возвразается значение.
        else:
            # Перебераем все ключи категории и возвращаем словарь всех nodes.
            D = {}

            for key in self.map[zone][category].keys(): 
                D[key] = self.map[zone][category][key]
                
            return D
    
    def add_zone(self, zone):
        ''' Method add_zone class Vocabulary
            Parameter: zone - name of new zone.
            
        '''
        
        if self.file_path == None: return self.__errors(5)
        if not self.__check(zone, param=1, R=False): return self.__errors(6, ('Zone', zone))
            
        self.map[zone] = {}
        return self.__write()
        
    def add_category(self, zone, category):
        ''' Method add_category class Vocabulary
            Parameter: zone - name of zone (required).
                       category - name of new category (required). 
            
        '''
        if self.file_path == None: return self.__errors(5)
        if not self.__check(zone, category, param=2, R=False): return self.__errors(6, ('Category', category))
        
        if self.__check(zone, param=2, R=False): self.map[zone][category] = {}
        else: return self.__check(zone, param=2)
        
        return self.__write()
        
    def add_key(self, zone, category, key, value=None):
        ''' Method add_category class Vocabulary
            Parameter: zone - name of zone (required).
                       category - name of category (required).
                       key - name of new key (required).
                       value - value of new key (unrequited).
            
        '''
        
        if self.file_path == None: return self.__errors(5)
        if not self.__check(zone, category, key, R=False): return self.__errors(6, ('Key', key))

        else: self.map[zone][category][key] = value
        
        return self.__write()
    
    def add(self, zone, category, key, value=None):
        ''' Method add class Vocabulary
            Parameter: zone - name of zone (required).
                       category - name of category (required).
                       key - name of new key (required).
                       value - value of new key (unrequited).
            
        '''
        
        ## Метод создает zone, category, key c нуля.
        if self.file_path == None: return self.__errors(5)
        
        self.add_zone(zone)
        self.add_category(zone, category)
        self.add_key(zone, category, key, value)
        
        return self.__write()
    
    def delete(self, zone, category=None, key=None):
        ''' Method delete class Vocabulary
            Parameter: zone - name of zone (required).
                       category - name of category (unrequired).
                       key - name of new key (unrequired).
            
        '''
        
        ## Удаляется последний из заданных параметров.
        if key != None: 
            if not self.__check(zone, param=3, R=False): del self.map[zone][category][key]
            else: return self.__errors(7, ('Key', key))
            
        elif key == None and category != None: 
            if not self.__check(zone, param=2, R=False):del self.map[zone][category]
            else: return self.__errors(7, ('Category', category))
            
        else: 
            if not self.__check(zone, param=1, R=False):del self.map[zone]
            else: return self.__errors(7, ('Zone', zone))
        
        return self.__write()
    
    def create(self, path='New_PyVoc.pyvoc', name='New_PyVoc'):
        ''' Method create class Vocabulary
            Parameter: path - path of new document absolute (unrequired).
                       name - new vocabulary name(unrequired).
            
        '''
        
        if exists(path): return self.__errors(9, path)
        
        try: open(path, 'w')
        except: return self.__errors(8, path)
        
        self.__init__(path, name)
    
    def __write(self, pyvoc=None, path=None):
        if pyvoc == None: pyvoc = self.map
        if path == None and self.file_path == None: path = ".\\"
        if path == None and self.file_path != None: path = self.file_path
        
        file = open(path, 'w') # Открываем файлы для записи.
        
        for key in pyvoc.keys():
            file.write('<zone=%s>' % key)
            for k in pyvoc[key].keys(): 
                file.write('\n\t<category=%s>' % k)   
                for K in pyvoc[key][k].keys():
                    file.write('\n\t\t<{}={}>'.format(K, self.map[key][k][K]))   
                file.write('\n\t</category>')
            file.write('\n</zone>\n')
            
        file.close()
    
    def set(self, zone, category, key, val=None):
        ''' Method set class Vocabulary
            Parameter: zone - name of zone (required).
                       category - name of category (required).
                       key - name of new key (required).
                       value - value of new key (unrequited).
            
        '''
        
        ## Изменения параметров заданных ключем.
        if self.file_path == None: return self.__errors(4)
        
        test = self.__check(zone, category, key, 4) 
        if test: return test
        
        self.map[zone][category][key] = val
        self.__write(path=self.file_path)
        
    def __str__(self):
        if self.file_path == None: return self.__errors(4)
        
        striper = '\n{}'.format('--' * 40) 
        voc = '{}Document name: {} \nos_path: {}'.format(striper, self.name, self.file_path)
        
        for key in self.map.keys():
            voc += '{}\nZone: {}'.format(striper, key)
            for k in self.map[key].keys(): 
                voc += '\n\tCategory: %s' % k
                for K in self.map[key][k].keys():
                    voc += '\n\t\t{} {}'.format(K, self.map[key][k][K])
                    
        voc += striper
        return voc
        
    def __call__(self, zone=None, category=None, key=False):
        return self.get(zone, category, key)


if __name__ ==  "__main__": 
    from os.path import exists, abspath
    
else:
    temp = {'exists(".\none.txt")': ('os.path', 'exists'),
            'abspath(".\.")'  : ('os.path', 'abspath')}
    
    for key in temp.keys():
        try: eval(key);
        except: exec('from {} import {}'.format(temp[key][0], temp[key][1]))