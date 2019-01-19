import json



class JSONEncoding():
    def decode(messageEncoded):
        message = json.loads(messageEncoded)

        return message

    def encode(message):
        messageEncoded = json.dumps(message)

        return messageEncoded

    def decodeDecorator(func):
        def newFunc(*args, **params):
            message = JSONEncoding.decode(func(*args, **params))
            return message

        return newFunc

    def encodeDecoratorX(classMethod=False):
        if classMethod:
            def encodeDecorator(func):
                def newFunc(self, message, *args, **params):
                    encodedMessage = JSONEncoding.encode(message)
                    return func(self, encodedMessage, *args, **params)

                return newFunc
            return encodeDecorator
        else:
            def encodeDecorator(func):
                def newFunc(message, *args, **params):
                    encodedMessage = JSONEncoding.encode(message)
                    return func(encodedMessage, *args, **params)

                return newFunc
            return encodeDecorator
