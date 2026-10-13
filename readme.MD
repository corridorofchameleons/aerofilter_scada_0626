# Запуск

```
pip install -r requirements.txt
python3 main.py # на виндовс заменить на python
```

# API
Серверная часть приложения имеет 8 (восемь) топиков:

- prism/telemetry
- prism/ack
- prism/set
- prism/setlist
- sql/write
- sql/read
- sql/data
- sql/get

### prism/telemetry
**B->F**<br/>
Задача: отправлять данные без обратной связи с короткой периодичностью (используется только для передачи данных типа float).<br/>

*Формат*:
```json
{
  "timestamp": 12345678,
  "data": [
    {
      "ns_name": "rewrite_in_rust",
      "name": "oil_pressure_before",
      "value": 17.3      
    },
    {
      "ns_name": "rewrite_in_rust",
      "name": "oil_pressure_after",
      "value": 17.2      
    }
  ]
}
```

### prism/ack
**B->F**<br/>
Задача: отправлять данные разово, как правило в ответ на команды (используется для управления состоянием кнопок и виджетов).<br/>

*Формат*:
```json
{
  "timestamp": 12345678,
  "data": [
    {
      "ns_name": "rewrite_in_rust",
      "name": "valve_foo",
      "value": true      
    },
    {
      "ns_name": "rewrite_in_rust",
      "name": "valve_bar",
      "value": false,
      "disabled": true
    }
  ]
}
```
Опциональное поле disabled ставит соответствующий флаг на виджет, блокируя интерфейс.<br/>
**ВАЖНО:** если в этот топик не отправить данные, ui не обновится. Некоторые виджеты останутся скрыты. Другими словами, ui обновляется ТОЛЬКО по сообщениям этого топика.

### prism/set
**F->B**<br/>
Задача: получать одиночные команды от скады.<br/>

*Формат*:
```json
{
  "timestamp": 12345678,
  "data": {
      "ns_name": "rewrite_in_rust",
      "name": "button",
      "value": true      
    }
}
```

### prism/setlist
**F->B**<br/>
Задача: получать список команд от скады.<br/>

*Формат*:
```json
{
  "timestamp": 12345678,
  "data": [
    {
      "ns_name": "rewrite_in_rust",
      "name": "oil_test_num",
      "value": 11      
    },
    {
      "ns_name": "rewrite_in_rust",
      "name": "oil_test_before_2um_1",
      "value": null      
    }
  ]
}
```

### sql/write
**B->DB**<br/>
Задача: записывать значения в базу данных.<br/>

*Формат*:
```json
{
  "timestamp": 12345678,
  "data": [
    {
      "ns_name": "rewrite_in_rust",
      "name": "valve_foo",
      "value": true      
    },
    {
      "ns_name": "rewrite_in_rust",
      "name": "valve_bar",
      "value": false,
      "disabled": true
    }
  ]
}
```

### sql/read
**B->DB**<br/>
Задача: запрашивать данные из БД.<br/>

*Формат (для выбора всех строк)*:
```json
{
  "timestamp": 12345678,
  "data": null
}
```

*Формат (с фильтрацией по имени тэга)*:
```json
{
  "timestamp": 12345678,
  "data": ["oil_test_before_2um_1", "oil_test_before_3um_1"]
}
```

### sql/data
**DB->B**<br/>
Задача: получать данные из базы данных.<br/>

*Формат*:
```json
{
  "timestamp": 12345678,
  "data": [
    {
      "ns_name": "rewrite_in_rust",
      "name": "valve_foo",
      "value": true,
      "disabled": null
    },
    {
      "ns_name": "rewrite_in_rust",
      "name": "valve_bar",
      "value": false,
      "disabled": true
    }
  ]
}
```

### sql/get
**F->B**<br/>
Задача: получать запрос на данные из БД от скады.<br/>

*Формат*:
```json
{
  "timestamp": 12345678,
  "data": ["oil_test_before_2um_1", "oil_test_before_3um_1"]
}
```

# ОПИСАНИЕ

## 1. Запуск

Скада при запуске отправляет запрос в ***sql/get*** с payload: null для получения сохраненного состояния. <br/>
- запрос пересылается в ***sql/read***
- читается в ***sql/data*** 
- отправляется в ***prism/ack***

В случае, если скада уже открыта, при запуске сервера неоходимо последние 3 действия сделать принудительно.

## 2. Обработка нажатий кнопок мнемосхемы

Все кнопки и виджеты на мнемосхеме, кроме некоторых, о которых ниже, имеют тип данных **bool** и два состояния:
**true** (active) и **false** (inactive). При нажатии на кнопку приходит новый желаемый статус (опраделяется на скаде).
Например, кнопка включает свет. После включения света необходимо для обновления интерфейса вернуть в ***prism/ack*** данные в формате, 
соответствующем топику, в любом количестве, если необходимо при включении света, например, выключать насос или блокировать 
помпу.

Поля ввода значения работают аналогичным образом, но имеют тип **float**.<br/>
Кнопка выбора стенда имеет тип **int**: 0 - стенд не выбран (значение по умолчанию), 1 - выбран масляный стенд, 2 - топливный.

## 3. Табличная часть

Шапка таблицы имеет 3 **int** состояния на каждую ячейку:
0 - измерение не проведено (серая)
1 - измерение проведено (синяя)
2 - измерение отменено (зеленая)

### Количество измерений.<br/>
Работает аналогично полям ввода, но имеет тип **int** с диапазоном значений от 1 до 11. 
### Измерение ДО/ПОСЛЕ. 
При активации и деактивации кнопки в ***prism/set*** улетает значение с текущим индексом измерения:
```json
{
  "timestamp": 12345678,
  "data": [
    {
      "ns_name": "rewrite_in_rust",
      "name": "oil_select_before",
      "value": true
    },
    {
      "ns_name": "rewrite_in_rust",
      "name": "oil_before_index",
      "value": 5
    }
]}
```
1. Когда измерение проведено, и в скаду в заданный столбец пришли значения, индекс пересчитывается и на сервер **prism/set** 
отправляется значение:
```json
{
  "timestamp": 12345678,
  "data": {
      "name": "oil_before_index",
      "value": 3
    }
}
```
На сервере хранить это значение не обязательно, но **ОБЯЗАТЕЛЬНО** записать в базу данных!!!
Этот тэг КРАЙНЕ НУЖЕН для сохранения состояния.
2. После получения измерения в столбец, верхняя ячейка превращается в кнопку "отменить". При нажатии на нее в ***prism/set***
уходят данные:
```json
{
  "timestamp": 12345678,
  "data": {
      "name": "oil_before_index_1",
      "value": 2
    }
}
```
С этим не надо делать ничего, кроме записи в БД и возврата в исходном виде.
Далее индекс пересчитывается и повторяется п.3.
3. После нажатия "отменить" кнопка превращается в кнопку "вернуть". При нажатии в ***prism/set*** уходят данные:
```json
{
  "timestamp": 12345678,
  "data": {
      "name": "oil_before_index_1",
      "value": 1
    }
}
```
Поступать надо аналогично п.4. Это только для сохранения состояния.

Параллельно с этим запросом также происходит запрос на ***sql/get***, с запросом на список имен, которые нужно получить 
из БД, чтобы заполнить очищенные ячейки. С запросом не нужно ничего делать - просто выполнить такую же последовательность,
как при запуске:
- запрос пересылается в ***sql/read***
- читается в ***sql/data*** 
- отправляется в ***prism/ack***

Далее индекс пересчитывается и повторяется п.3.

### Новое измерение
При нажании на кнопку в ***prism/setlist*** уходит список тэгов, которым нужно задать initial значения.

### *Все запросы на сервер должны прислать ответ в prism/ack*

# ТЭГИ И ТИПЫ ДАННЫХ

### delta_as200
    oil_probe_after_6ka3: bool
    oil_probe_before_6ka4: bool
    oil_mixer_input_valve: bool
    oil_mixer_output_valve: bool
    oil_pressure_before: float
    oil_pressure_after: float
    oil_temperature_before: float
    oil_temperature_after: float
    oil_moisture_before: float
    oil_moisture_after: float
    oil_tank_temperature: float
    oil_flow_meter: float
    oil_main_pump_start: bool
    oil_mixing_pump_start: bool
    oil_tank_heater: bool
    oil_light: bool
    oil_set_tank_temperature: float
    oil_set_flow: float
    fuel_probe_after_6ka3: bool
    fuel_probe_before_6ka4: bool
    fuel_mixer_input_valve: bool
    fuel_mixer_output_valve: bool
    fuel_pressure_before: float
    fuel_pressure_after: float
    fuel_temperature_before: float
    fuel_temperature_after: float
    fuel_moisture_before: float
    fuel_moisture_after: float
    fuel_tank_temperature: float
    fuel_flow_meter: float
    fuel_main_pump_start: bool
    fuel_mixing_pump_start: bool
    fuel_tank_heater: bool
    fuel_light: bool
    fuel_set_tank_temperature: float
    fuel_set_flow: float
### pump_values
    oil_pump_frequency_setpoint: float
    fuel_pump_frequency_setpoint: float
### value_table
    oil_before_2um_1: int
    ...
    fuel_before_2um_1: int
    ...
    oil_effectiveness_2: float
    ...
    fuel_effectiveness_2: float
    ...
### particle_select
    stand_select: int
    oil_test_num: int
    oil_effectiveness: float
    oil_before_index: int
    oil_after_index: int
    oil_select_before: bool
    oil_select_after: bool
    fuel_test_num: int, initial=TEST_NUM
    fuel_effectiveness: float
    fuel_before_index: int
    fuel_after_index: int
    fuel_select_before: bool
    fuel_select_after: bool