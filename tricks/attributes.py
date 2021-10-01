func = lambda t: 3 + t

# https://www.oreilly.com/library/view/learning-python/9781783551712/ch04s08.html

special_attributes = [
"__doc__", "__name__", "__qualname__", "__module__",
"__defaults__", "__code__", "__globals__", "__dict__",
"__closure__", "__annotations__", "__kwdefaults__",
]

# for attribute in special_attributes:
#     print(attribute, '->', getattr(func, attribute))

# https://stackoverflow.com/questions/582056/getting-list-of-parameter-names-inside-python-function

print(func.__code__.co_argcount)
print(func.__code__.co_varnames)
print(func.__defaults__)

# https://stackoverflow.com/questions/36517173/how-to-store-a-javascript-function-in-json

# This seems promising
# https://stackoverflow.com/questions/51634917/how-to-instantiate-a-function-from-string-in-python-3-x
exec("func=lambda t: t+3", globals())