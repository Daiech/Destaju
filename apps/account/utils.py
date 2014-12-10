def getNextName(value):
    """
    the entry value is already exists.
    then, search a new value.
    """
    num = value.split("_")[-1]
    # print "value", value
    # print "Num:", num
    if (num != value) and num.isdigit():
        num = int(num) + 1
        # print "num + 1", num
        value = "_".join(value.split("_")[:-1]) + "_" + str(num)
        # print "VALUE True", value
    else:
        value = value + "_1"
        # print "VALUE false", value
    return value


def validateUniqueField(model, field_name, value):
    try:
        # print field_name
        # print value
        model.objects.get(**{field_name: value})
    except model.DoesNotExist:
        print "No exists, se devuelve tal cual"
        return value
    while True:
        value = getNextName(value)
        # print "siguiente:", value
        try:
            model.objects.get(**{field_name: value})
        except model.DoesNotExist:
            print "no exists, se devuelve"
            return value
            break
