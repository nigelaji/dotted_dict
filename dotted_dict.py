class List(list):
    def __mul__(self, value: int):
        lis = []
        for i in range(value):
            lis.extend(deepcopy(self))
        return lis


def init_multidimensional_list(depth: int, dimension: int, init_value=None):
    """ initialize a multidimensional list
    :param depth:
    :param dimension:
    :param init_value:
    :return:
    """
    init_v = str(init_value)
    _ds = f"List([{init_v}]) * depth"
    for _ in range(dimension - 1):
        _ds = "List([" + _ds + "]) * depth"
    return eval(_ds, None, {"depth": depth + 1, "List": List})


def multidimensional_list_assignment(mdl, dimension, *subscripts, values: list = None):
    """Assignment to multidimensional list
    :param mdl:
    :param dimension:
    :param subscripts:
    :param values:
    :return:
    """
    for sub_s, v in zip(subscripts, values or []):
        count = len(sub_s)
        if count != dimension:
            raise ValueError('The number of subscripts does not match the dimension')
        _ = "mdl"
        for idx in sub_s:
            _ += "[" + str(idx) + "]"
        _ += f"={v}"
        exec(_, None, {"mdl": mdl})
    return mdl


def multi_dimensional(depth: int, dimension: int, *subscripts, sub_values: list = None, init_value=None):
    """ 生成一个多维列表，指定一些位置的值
    :param depth:
    :param dimension:
    :param subscripts:
    :param sub_values:
    :param init_value:
    :return:
    """
    if depth < 1 or dimension < 1:
        return []
    return multidimensional_list_assignment(
        init_multidimensional_list(
            depth, dimension, init_value=init_value
        ),
        dimension, *subscripts, values=sub_values
    )


def uncompress(dotted_map: dict):
    """ lue lue lue
    :param dotted_map:
    :return:
    """

    def analysis_key(key):
        fs = []
        locs = key.split('.')
        for loc in locs:
            f = []
            var_name = loc.split('[')[0]
            if loc[-1] == ']':
                idxes = [int(i[:-1]) for i in loc.split('[') if ']' in i]
                dimension = len(idxes)
                depth = max(idxes)
                f.extend([var_name, idxes, dimension, depth])
            else:
                f.extend([var_name, None, 0, 0])
            fs.append(f)
        return fs[::-1]

    def assign(f, v):
        var_name, idxes, dim, dep = f
        if idxes is None:
            return {
                var_name: v
            }
        return {
            var_name: multi_dimensional(dep, dim, *(idxes,), sub_values=[v])
        }

    uncompress_map = {}
    for squeeze_key, value in dotted_map.items():
        features = analysis_key(squeeze_key)
        for feature in features:
            value = assign(feature, value)
        uncompress_map.update(value)
    return uncompress_map


def compress(nested, lost=None):
    warnings.warn("This method has bugs and cannot be used yet. i'm stupid, unresolved. The above method may also "
                  "have a bug")
    lost = lost or []

    def deconstruct_dict(nest, ks=None, in_list=False):
        ks = ks or []
        if isinstance(nest, dict):
            for _k, _v in nest.items():
                ks.append(_k)
                yield from deconstruct_dict(_v, ks, in_list)
            print('dict', ks)
        elif isinstance(nest, list):
            length = len(nest)
            for i, item in enumerate(nest):
                ks.append(i)
                yield from deconstruct_dict(item, ks, in_list)
                if ks:
                    ks.pop()
            print('list', ks)
            ks.clear()
        else:
            yield ks, nest
            print(ks, nest)
            ks.pop()

    def locs_join(locs, value):
        if value in lost:
            return {}
        key = ""
        for loc in locs:
            if isinstance(loc, int):
                loc = f"[{loc}]"
                key = key[:-1]
            key += loc + "."
        key = key[:-1]
        return {key: value}

    compress_map = {}
    for _locs, v in deconstruct_dict(nested):
        compress_map.update(locs_join(_locs, v))
    return compress_map
