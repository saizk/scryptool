from . import write_meta as meta
import csv
import json
import os


def outputExt(objType, fType):
    if objType == "str":
        objType = "username"
    outExt = f"/{objType}s.{fType}"

    return outExt


def addExt(base, objType, fType):
    if len(base.split('.')) == 1:
        createDirIfMissing(base)
        base += outputExt(objType, fType)

    return base


def Text(entry, f):
    print(entry.replace('\n', ' '), file=open(f, "a", encoding="utf-8"))


def Type(config):
    if config.User_full:
        _type = "user"
    elif config.Followers or config.Following:
        _type = "username"
    else:
        _type = "tweet"

    return _type


def struct(obj, custom, _type):
    if custom:
        fieldnames = custom
        row = {}
        for f in fieldnames:
            row[f] = meta.Data(obj, _type)[f]
    else:
        fieldnames = meta.Fieldnames(_type)
        row = meta.Data(obj, _type)

    return fieldnames, row


def createDirIfMissing(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def Csv(obj, config):
    _obj_type = obj.__class__.__name__
    if _obj_type == "str":
        _obj_type = "username"
    fieldnames, row = struct(obj, config.Custom[_obj_type], _obj_type)

    if config.Lang is not None and row.get('language') != config.Lang:
        return

    if not config.SaveMeta:
        fieldnames = ('created_at', 'tweet', 'username', 'hashtags', 'cashtags',
                      'retweets_count', 'likes_count', 'replies_count')
        row = dict((k, row[k]) for k in fieldnames if k in row)

    dialect = 'excel-tab' if 'Tabs' in config.__dict__ else 'excel'

    # global_csv(config, fieldnames, dialect, row, write_header)
    slow_csv(config, fieldnames, dialect, row)


global_csv_file = None

def global_csv(config, fieldnames, dialect, row):
    global global_csv_file
    if global_csv_file is None:
    # if not os.path.exists(config.Output):
        global_csv_file = open(config.Output, "a", newline='', encoding="utf-8")
        writer = csv.DictWriter(global_csv_file, fieldnames=fieldnames, dialect=dialect)
        writer.writeheader()

    csv_file = global_csv_file
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, dialect=dialect)
    writer.writerow(row)


def slow_csv(config, fieldnames, dialect, row):
    write_header = False
    if not os.path.exists(config.Output):
        write_header = True

    with open(config.Output, "a", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, dialect=dialect)
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def Json(obj, config):
    _obj_type = obj.__class__.__name__
    if _obj_type == "str":
        _obj_type = "username"
    null, data = struct(obj, config.Custom[_obj_type], _obj_type)

    base = addExt(config.Output, _obj_type, "json")

    with open(base, "a", newline='', encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False)
        json_file.write("\n")
