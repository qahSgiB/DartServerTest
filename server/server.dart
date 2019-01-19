/*
 * TODO: errors
 *
 */

import 'dart:io';
import 'dart:async';
import 'dart:convert';
import 'dart:math';

import 'package:tuple/tuple.dart';



typedef onMessageType = Map<Object, Object> Function(String, Map<Object, Object>);



class Node<T> {
    T value;
    Node next;
    Node previous;

    Node(T value) {
        this.value = value;
    }
}

class Proceeder<nodeType, funcReturnType> {
    nodeType beginNode;

    Proceeder(this.beginNode);

    funcReturnType proceed(funcReturnType Function(nodeType, funcReturnType) func, nodeType Function(nodeType) getNext, funcReturnType startResult) {
        nodeType temp = this.beginNode;
        funcReturnType result = startResult;

        while (temp != null) {
            result = func(temp, result);

            temp = getNext(temp);
        }

        return result;
    }
}

class LinkedList<T> {
    Node<T> beginNode;
    Node<T> endNode;

    LinkedList() {

    }

    void add(T value) {
        if (this.beginNode == null) {
            this.beginNode = Node<T>(value);
            this.endNode = this.beginNode;
        } else {
            this.endNode.next = Node<T>(value);
            this.endNode.next.previous = this.endNode;
            this.endNode = this.endNode.next;
        }
    }

    void addToBegin(T value) {
        if (this.beginNode == null) {
            this.beginNode = Node<T>(value);
            this.endNode = this.beginNode;
        } else {
            this.beginNode.previous = Node<T>(value);
            this.beginNode.previous.next = this.beginNode;
            this.beginNode = this.beginNode.previous;
        }
    }

    T get(int getIndex) {
        if (getIndex > this.getLength()-1 || getIndex < 0) {
            return null;
        } else {
            Tuple2<T, int> Function(Node<T>, Tuple2<T, int>) nodeFunc = (Node<T> node, Tuple2<T, int> info) {
                int index = info.item2;
                T result = info.item1;

                if (index == getIndex) {
                    return Tuple2<T, int>(node.value, index+1);
                } else {
                    return Tuple2<T, int>(result, index+1);
                }
            };
            Node<T> Function(Node<T>) nodeGetNext = (Node<T> node) {
                return node.next;
            };

            Proceeder<Node<T>, Tuple2<T, int>> proceeder = Proceeder<Node<T>, Tuple2<T, int>>(this.beginNode);
            Tuple2<T, int> getValue = proceeder.proceed(nodeFunc, nodeGetNext, Tuple2<T, int>(null, 0));

            return getValue.item1;
        }
    }

    T pop(int index) {
        if (index < 0 || index > this.getLength()-1) {
            return null;
        } else if (this.getLength() == 1) {
            Node<T> beginNodeH = this.beginNode;
            this.beginNode = null;
            this.endNode = null;

            return beginNodeH.value;
        } else if (index == 0) {
            Node<T> beginNodeH = this.beginNode;
            this.beginNode = this.beginNode.next;
            this.beginNode.previous = null;

            return beginNodeH.value;
        } else if (index == this.getLength()-1) {
            Node<T> endNodeH = this.endNode;
            this.endNode = this.endNode.previous;
            this.endNode.next = null;

            return endNodeH.value;
        } else {
            Node<T> temp = this.beginNode;

            for (int i=0; i<index; i++) {
                temp = temp.next;
            }

            temp.previous.next = temp.next;
            temp.next.previous = temp.previous;

            return temp.value;
        }
    }

    int getLength() {
        int Function(Node<T>, int) nodeFunc = (Node<T> node, int tempLength) {
            return tempLength+1;
        };
        Node<T> Function(Node<T>) nodeGetNext = (Node<T> node) {
            return node.next;
        };

        Proceeder<Node<T>, int> proceeder = Proceeder(this.beginNode);
        int length = proceeder.proceed(nodeFunc, nodeGetNext, 0);

        return length;
    }

    List<T> toList() {
        List<T> Function(Node<T>, List<T>) nodeFunc = (Node<T> node, List<T> tempList) {
            tempList.add(node.value);
            return tempList;
        };
        Node<T> Function(Node<T>) nodeGetNext = (Node<T> node) {
            return node.next;
        };

        Proceeder<Node<T>, List<T>> proceeder = Proceeder(this.beginNode);
        List<T> list = proceeder.proceed(nodeFunc, nodeGetNext, List<T>()).toList();

        return list;
    }

    List<T> find(bool Function(Node<T>) condition) {
        LinkedList<T> Function(Node<T>, LinkedList<T>) nodeFunc = (Node<T> node, LinkedList<T> tempList) {
            if (condition(node)) {
                tempList.add(node.value);
            }
            return tempList;
        };
        Node<T> Function(Node<T>) nodeGetNext = (Node<T> node) {
            return node.next;
        };

        Proceeder<Node<T>, LinkedList<T>> proceeder = Proceeder(this.beginNode);
        List<T> list = proceeder.proceed(nodeFunc, nodeGetNext, LinkedList<T>()).toList();

        return list;
    }

    List<int> findIndex(bool Function(Node<T>) condition) {
        Tuple2<LinkedList<int>, int> Function(Node<T>, Tuple2<LinkedList<int>, int>) nodeFunc = (Node<T> node, Tuple2<LinkedList<int>, int> temp) {
            int index = temp.item2;
            LinkedList<int> tempList = temp.item1;

            if (condition(node)) {
                tempList.add(index);
            }
            return Tuple2<LinkedList<int>, int>(tempList, index+1);
        };
        Node<T> Function(Node<T>) nodeGetNext = (Node<T> node) {
            return node.next;
        };

        Proceeder<Node<T>, Tuple2<LinkedList<int>, int>> proceeder = Proceeder<Node<T>, Tuple2<LinkedList<int>, int>>(this.beginNode);
        List<int> list = proceeder.proceed(nodeFunc, nodeGetNext, Tuple2<LinkedList<int>, int>(LinkedList<int>(), 0)).item1.toList();

        return list;
    }
}

class SocketStreamableItem {
    int id;

    SocketStreamableItem(this.id);

    Map<Object, Object> toMap() {
        return {};
    }
}

class SocketStreamableItemsList {
    LinkedList<SocketStreamableItem> list;

    SocketStreamableItemsList() {
        list = LinkedList<SocketStreamableItem>();
    }

    List<int> getIndex(int id) {
        return this.list.findIndex((Node<SocketStreamableItem> item) {return item.value.id == id;});
    }

    void remove(int id) {
        List<int> indexes = this.getIndex(id);

        for (int index in indexes) {
            this.list.pop(index);
        }
    }

    SocketStreamableItem get(int id) {
        int index = this.getIndex(id)[0];

        return this.list.get(index);
    }

    void add(SocketStreamableItem socketStreamableItem) {
        this.list.add(socketStreamableItem);
    }

    List<Map<Object, Object>> toList() {
        List<Map<Object, Object>> Function(Node<SocketStreamableItem>, List<Map<Object, Object>>) nodeFunc = (Node<SocketStreamableItem> node, List<Map<Object, Object>> tempList) {
            tempList.add(node.value.toMap());
            return tempList;
        };
        Node<SocketStreamableItem> Function(Node<SocketStreamableItem>) nodeGetNext = (Node<SocketStreamableItem> node) {
            return node.next;
        };

        Proceeder<Node<SocketStreamableItem>, List<Map<Object, Object>>> proceeder = Proceeder(this.list.beginNode);
        List<Map<Object, Object>> list = proceeder.proceed(nodeFunc, nodeGetNext, List<Map<Object, Object>>());

        return list;
    }
}

class Player extends SocketStreamableItem {
    int x;
    int y;

    Player(this.x, this.y, int id):super(id);

    Map<Object, Object> toMap() {
        Map<Object, Object> data = {
            'id': this.id,
            'x': this.x,
            'y': this.y,
        };

        return data;
    }
}

class GameClient {
    Socket client;
    String address;
    int port;
    int id;
    bool outputEnabled;
    onMessageType onMessage;

    GameClient(Socket client, int id, onMessageType onMessage, {bool outputEnabled=false}) {
        this.client = client;
        this.address = this.client.remoteAddress.address;
        this.port = this.client.remotePort;
        this.id = id;

        this.outputEnabled = outputEnabled;

        this.onMessage = onMessage;

        this.client.listen(this.listen);

        this.output('Connection from ${this.address}:${this.port}');
    }

    void output(String text) {
        if (this.outputEnabled) {
            print('(${this.address}:${this.port} ${this.id}) ${text}');
        }
    }

    void listen(List<int> data) {
        Map<Object, Object> message = json.decode(String.fromCharCodes(data).trim());

        String title = message['title'];

        if (title == 'beginCommunication') {
            this.begin(message['data']);
        } else if (title == 'endCommunication') {
            this.end(message['data']);
        } else if (this.onMessage != null) {
            this.sendData(this.onMessage(title, message['data']));
        }
    }

    void sendData(Map<Object, Object> message) {
        String data = json.encode(message);

        this.client.write(data);
    }

    void begin(Map<Object, Object> message) {
        this.output('Begin | id:${this.id}');

        Map<Object, Object> responseMessage = {
            'id': this.id,
        };

        this.sendData(responseMessage);
    }

    void end(Map<Object, Object> message) {
        this.output('End');

        Map<Object, Object> responseMessage = {
        };

        this.sendData(responseMessage);

        this.client.close();
    }
}

class Game {
    ServerSocket server;
    SocketStreamableItemsList players;
    int nextPlayerId;
    int width;
    int height;

    Game(this.server, this.width, this.height) {
        this.players = SocketStreamableItemsList();
        this.nextPlayerId = 0;

        this.server.listen(this.newClient);
    }

    void newClient(Socket client) {
        int playerId = this.nextPlayerId;

        Map<Object, Object> gameClientOnMessage(String title, Map<Object, Object> message) {
            if (title == 'addPlayer') {
                Player player = Player(Random().nextInt(this.width), Random().nextInt(this.height), playerId);
                this.players.add(player);

                Map<Object, Object> responseMessage = {
                    'player': player.toMap()
                };

                return responseMessage;
            } else if (title == 'loop') {
                Map<Object, Object> responseMessage = {
                    'players': this.players.toList(),
                };

                return responseMessage;
            } else if (title == 'initInfo') {
                Map<Object, Object> responseMessage = {
                    'width': this.width,
                    'height': this.height,
                };

                return responseMessage;
            } else if (title == 'changeXY') {
                int x = message['x'];
                int y = message['y'];

                Player player = this.players.get(playerId);

                player.x = x;
                player.y = y;

                Map<Object, Object> responseMessage = {
                };

                return responseMessage;
            } else if (title == 'end') {
                this.players.remove(playerId);

                Map<Object, Object> responseMessage = {
                };

                return responseMessage;
            } else {
                return {};
            }
        }

        GameClient(client, playerId, gameClientOnMessage, outputEnabled: true);

        this.nextPlayerId++;
    }
}



void test() {
    LinkedList<int> linkedList = LinkedList<int>();

    // print(linkedList.toList());

    linkedList.add(1);
    linkedList.add(2);
    linkedList.add(3);
    linkedList.add(5);

    // print(linkedList.pop(3));
    // print(linkedList.pop(0));
    // print(linkedList.pop(0));
    // print(linkedList.pop(0));
    // print(linkedList.pop(0));
    // print(linkedList.endNode == linkedList.beginNode);

    // print(linkedList.getLength());

    // while (linkedList.getLength() > 0) {
    //     print(linkedList.get(0));
    //     print(linkedList.pop(0));
    // }

    // print(linkedList.toList());

    // print(linkedList.findIndex((Node<int> tempNode) {return tempNode.value%2 == 1;}));
}

Future main() async {
    // test();

    ServerSocket server = await ServerSocket.bind(
        '192.168.1.4',
        4040,
    );

    Game(server, 500, 500);

    // int nextId = 0;
    //
    // server.listen((Socket client) {
    //     GameClient(client, nextId, outputEnabled: true);
    //     nextId++;
    // });
}
