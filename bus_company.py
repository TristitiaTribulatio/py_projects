import json
import re
import itertools

db, type_error, quantity_error = input(), dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0, stop_type=0, a_time=0), 0
bus_id, sp_stops, wrong_time, wrong_stop_type = {}, {'start': list(), 'transfer': set(), 'finish': list(), 'buses': {}}, {}, list()
json_db = json.loads(db)


def main():
    # check_types()
    # check_syntax()
    # bus_line_info()
    # special_stops()
    # unlost_in_time()
    # on_demand()


def check_types():
    global type_error, json_db

    for i in range(len(json_db)):
        if not isinstance((json_db[i])['bus_id'], int) or bool((json_db[i])['bus_id']) is False:
            type_error['bus_id'] += 1
        if not isinstance((json_db[i])['stop_id'], int) or bool((json_db[i])['stop_id']) is False:
            type_error['stop_id'] += 1
        if not isinstance((json_db[i])['stop_name'], str) or bool((json_db[i])['stop_name']) is False:
            type_error['stop_name'] += 1
        if not isinstance((json_db[i])['next_stop'], int) or (bool((json_db[i])['next_stop']) is False and (json_db[i])['next_stop'] != 0):
            type_error['next_stop'] += 1
        if (json_db[i])['stop_type'] not in ["S", "O", "F", ""] and not isinstance((json_db[i])['stop_type'], str) or len(str((json_db[i])['stop_type'])) not in [0, 1]:
            type_error['stop_type'] += 1
        if not isinstance((json_db[i])['a_time'], str) or bool((json_db[i])['a_time']) is False:
            type_error['a_time'] += 1

    output_errors('type')


def output_errors(condition):
    global quantity_error, type_error

    for er in type_error:
        quantity_error += type_error[er]

    print("Type and required field validation: {0} errors".format(quantity_error))
    if condition == 'type':
        for er in type_error:
            print("{0}: {1}".format(er, type_error[er]))
    elif condition == 'syntax':
        print("{0}: {1}".format('stop_name', type_error['stop_name']))
        print("{0}: {1}".format('stop_type', type_error['stop_type']))
        print("{0}: {1}".format('a_time', type_error['a_time']))


def check_syntax():
    global type_error, json_db

    for i in range(len(json_db)):
        if re.match(r"[A-Z][a-zA-Z\s]{1,}\s(Road|Avenue|Boulevard|Street)\Z", (json_db[i])['stop_name']) is None:
            type_error['stop_name'] += 1
        if re.match(r"(S|O|F|" ")\Z", (json_db[i])['stop_type']) is None:
            type_error['stop_type'] += 1
        if re.match(r"[0-2][0-9]:[0-5][0-9]\Z", (json_db[i])['a_time']) is None:
            type_error['a_time'] += 1

    output_errors('syntax')


def bus_line_info():
    global bus_id

    for i in range(len(json_db)):
        if bus_id.get((json_db[i])['bus_id']) is None:
            bus_id[(json_db[i])['bus_id']] = 1
        else:
            bus_id[(json_db[i])['bus_id']] += 1

    output_lines()


def output_lines():
    global bus_id

    print("Line names and number of stops:")
    for i in bus_id:
        print("bus_id: {0}, stops: {1}".format(i, bus_id[i]))


def special_stops():
    global json_db, sp_stops

    for i in range(len(json_db)):
        if (json_db[i])['stop_type'] in ["S", "F"]:
            if (sp_stops['buses']).get((json_db[i])['bus_id']) is None:
                (sp_stops['buses'])[(json_db[i])['bus_id']] = 1
            else:
                (sp_stops['buses'])[(json_db[i])['bus_id']] += 1

    for i in sp_stops['buses']:
        if (sp_stops['buses']).get(i) != 2:
            print("There is no start or end stop for the line: {0}".format(i))
            return True

    list_stops = [(json_db[j])['stop_name'] for j in range(len(json_db))]
    tmp_iter = itertools.combinations(list_stops, 2)

    for i in range(len(json_db)):
        if (json_db[i])['stop_type'] == "F" and (json_db[i])['stop_name'] not in sp_stops['finish']:
            sp_stops['finish'].append((json_db[i])['stop_name'])
        if (json_db[i])['stop_type'] == "S" and (json_db[i])['stop_name'] not in sp_stops['start']:
            sp_stops['start'].append((json_db[i])['stop_name'])
        for x, y in tmp_iter:
            if x == y:
                sp_stops['transfer'].add(x)

    print("Start stops: {0} {1}".format(len(sp_stops['start']), sorted(sp_stops['start'])))
    print("Transfer stops: {0} {1}".format(len(sp_stops['transfer']), sorted(sp_stops['transfer'])))
    print("Finish stops: {0} {1}".format(len(sp_stops['finish']), sorted(sp_stops['finish'])))


def unlost_in_time():
    global json_db, wrong_time

    a_time, current_bus, check = "00:00", (json_db[0])['bus_id'], 1

    for i in range(len(json_db)):
        if (json_db[i])['bus_id'] != current_bus:
            current_bus, a_time, check = (json_db[i])['bus_id'], "00:00", 1
        if (json_db[i])['a_time'] <= a_time and check:
            wrong_time[(json_db[i])['bus_id']] = (json_db[i])['stop_name']
            check = 0
        a_time = (json_db[i])['a_time']

    if wrong_time == {}:
        print("Arrival time test:\n OK")
    else:
        print("Arrival time test:")
        for i in wrong_time:
            print("bus_id line {0}: wrong time on station {1}".format(i, wrong_time[i]))


def on_demand():
    global json_db, sp_stops, wrong_stop_type

    for i in range(len(json_db)):
        if (json_db[i])['stop_type'] == "O":
            if (json_db[i])['stop_name'] in sp_stops['transfer']:
                wrong_stop_type.append((json_db[i])['stop_name'])
                continue
            elif (json_db[i])['stop_name'] in sp_stops['start']:
                wrong_stop_type.append((json_db[i])['stop_name'])
                continue
            elif (json_db[i])['stop_name'] in sp_stops['finish']:
                wrong_stop_type.append((json_db[i])['stop_name'])
                continue

    if wrong_stop_type == []:
        print("On demand stops test:\nOK")
    else:
        wrong_stop_type.sort()
        print("On demand stops test:\nWrong stop type: {0}".format(wrong_stop_type))


main()
