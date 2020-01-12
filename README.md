# [loadbalancer.py](https://github.com/vishnuvardhan-kumar/loadbalancer.py/blob/master/loadbalancer.py)

## Explanation

Due to popular request on LinkedIn, I'm writing this line by line explanation of how the 7-line code snippet works. 

Read on, and please contact me on [LinkedIn](https://www.linkedin.com/in/vishnuvardhan-kumar/)/[Github](https://github.com/vishnuvardhan-kumar) if you have any other questions.


## The Code

```
import flask, requests, itertools
app, self_host, self_port, nodes = flask.Flask(__name__), "0.0.0.0", 5000, itertools.cycle(['Put your urls here'])
@app.errorhandler(404)
def route_page(err):
    curr_node = next(nodes)
    return getattr(requests, flask.request.method.lower())(f"{curr_node}{flask.request.path}").text
if __name__ == "__main__": app.run(host=self_host, port=self_port)
```

Let's go over this line-by-line.


## Line 1

```
import flask, requests, itertools
```

- `flask` is a lightweight web framework for Python, perfect for our purposes.

- `requests` is a wrapper around urllib3 and provides high-level methods.
- `itertools` is a library module, with some interesting iterator functions.

## Line 2

```
app, self_host, self_port, nodes = flask.Flask(__name__), "0.0.0.0", 5000, itertools.cycle(['Put your urls here'])
```

So this is me taking advantage of Python's tuple unpacking variable assignments, which boils down to this:
```
# This line is equivalent to

app = flask.Flask(__name__)
self_host = "0.0.0.0"
self_port = 5000
nodes = itertools.cycle(['Put your urls here'])
```

- `flask.Flask()` is the WSGI application constructor, which instantiates the app.
- `self_host` and `self_port` are self-explanatory, the hostname and port to bind the app to.

- `itertools.cycle(['Put your urls here'])` is a utility function in `itertools` that will endlessly loop over an iterable, so as to mimic `round-robin` load-balancing.
```
x = itertools.cycle([1,2,3]) 
# x -> 1, 2, 3, 1, 2, 3, 1, 2, 3, 1.....

# Pick hosts to send requests in cyclic order
nodes = itertools.cycle(['host1:port1', 'host2:port2']) 
```

## Line 3 & 4

```
@app.errorhandler(404)
def route_page(err):
```

These lines start the definition of the function `route_page(err)` , with `app.errorhandler(404)` as the [decorator](https://realpython.com/primer-on-python-decorators/).

The idea is that whenever the client requests a page that is not available, a `404 NOT FOUND` is raised, and this function is called by `Flask` to handle the error/display a custom `404.html` page.

Since we do NOT have any routes configured, `Every request is a 404`, and `route_page()` can send the request to one of the nodes.

## Line 5

```
curr_node = next(nodes)
```

Again, pretty straight-forward, this assigns the `next()` value of the iterator to curr_node (where the request is going to be forwarded).

## Line 6

```
return getattr(requests, flask.request.method.lower())(f"{curr_node}{flask.request.path}").text
```

This is the core of the request-forwarding logic right here. Let's break down what is happening here:

`getattr(requests, flask.request.method.lower)`

The HTTP methods in the `requests` library are named as follows:

- `requests.get` : HTTP GET
- `requests.post` : HTTP POST
- `requests.put` : HTTP PUT
- `requests.delete` : HTTP DELETE (...and so on)

And `flask.request.method` is one of `GET, POST, PUT, DELETE` depending on which kind of request the client sends, the Python builtin function `lower()` converts it to lowercase. `getattr()` fetches the correct member attribute from the module for us.

So as a whole, this idiom represents the correct function object from `requests` to be used with our args.

`f"{curr_node}{flask.request.path}"`

This is a Python [f-string](https://realpython.com/python-f-strings/) that formats the complete url for the request.

For example if curr_node is `http://host1:port1` and the client requests `/index.html`, the value of the f-string becomes 

`http://host1:port1/index.html`

The `.text` at the end is to get the body of the response object.


## Line 7

```
if __name__ == "__main__": app.run(host=self_host, port=self_port)
```

This is a common Python pattern, this conditional is executed only when the script is run directly and not when imported into another module.

`app.run(host=self_host, port=self_port)`

This starts the Flask event loop and binds the app to the given host/port.


## Conclusion

This snippet is more of a proof of concept that this can be done in these few lines, rather than how it should be done. It was actually conceived when a friend claimed that this couldn't be done in fewer than 200 lines.

Thanks for reading till the end, if you liked it, star and follow for more stuff like this.