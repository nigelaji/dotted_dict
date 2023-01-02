# dotted_dict
Convert keys like jsonpath to traditional keys

example 1

```python
uncompress({"a.b.c": 1, "a.b.d": 2, "a.e": 3, "f": 4})
```
convert to ==> 
```python
{
    "a": {
        "b": {
            "c": 1,
            "d": 2
        },
        "e": 3
    },
    "f": 4
}
```
------------------------------------------
example 2

```python

uncompress({"a[0][1].b[1][1].c": 1})
```
convert to ==>
```Python
{
    'a': [
        [
            None,
            {
                'b': [
                    [None, None],
                    [None, {'c': 1}]
                ]
            }
        ],
        [None, None]
    ]
}
```
