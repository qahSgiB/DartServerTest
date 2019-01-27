/*
 * TODO: errors
 * TODO: boosts
 *
 */

import 'dart:io';
import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'dart:collection';

import 'package:tuple/tuple.dart';



/* -------------------- lib: DataStructures/LinkedList --------------------
 *
 */
 class LinkedListIterator<T> implements Iterator<T> {
     Node<T> node;

     LinkedListIterator(Node<T> beginNode) {
         this.node = Node<T>(null);
         this.node.next = beginNode;
     }

     bool moveNext() {
         this.node = this.node.next;

         return this.node != null;
     }

     T get current {
         return this.node.value;
     }
 }

 class Node<T> {
     T value;
     Node<T> next;
     Node<T> previous;

     Node(T value) {
         this.value = value;
     }

     Node<T> getNext() {
         return this.next;
     }

     Node<T> getPrevious() {
         return this.previous;
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

 class LinkedList<T> with IterableMixin<T> {
     Node<T> beginNode;
     Node<T> endNode;

     LinkedList();

     void addToEnd(T value) {
         if (this.beginNode == null) {
             this.beginNode = Node<T>(value);
             this.endNode = this.beginNode;
         } else {
             this.endNode.next = Node<T>(value);
             this.endNode.next.previous = this.endNode;
             this.endNode = this.endNode.next;
         }
     }

     void add(T value) {
         this.addToEnd(value);
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

     T popFromBegin() {
         return this.pop(0);
     }

     T popFromEnd() {
         return this.pop(this.getLength()-1);
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

     List<T> toList({bool growable: true}) {
         List<T> Function(Node<T>, List<T>) nodeFunc = (Node<T> node, List<T> tempList) {
             tempList.add(node.value);
             return tempList;
         };
         Node<T> Function(Node<T>) nodeGetNext = (Node<T> node) {
             return node.next;
         };

         Proceeder<Node<T>, List<T>> proceeder = Proceeder(this.beginNode);
         List<T> list = proceeder.proceed(nodeFunc, nodeGetNext, List<T>());

         return list;
     }

     LinkedList<newT> map<newT>(newT Function(T) mapFunction) {
         LinkedList<newT> Function(Node<T>, LinkedList<newT>) nodeFunc = (Node<T> node, LinkedList<newT> tempList) {
             tempList.add(mapFunction(node.value));
             return tempList;
         };
         Node<T> Function(Node<T>) nodeGetNext = (Node<T> node) {
             return node.next;
         };

         Proceeder<Node<T>, LinkedList<newT>> proceeder = Proceeder(this.beginNode);
         LinkedList<newT> mappedList = proceeder.proceed(nodeFunc, nodeGetNext, LinkedList<newT>());

         return mappedList;
     }

     LinkedList<T> filter(bool Function(Node<T>) condition) {
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
         LinkedList<T> list = proceeder.proceed(nodeFunc, nodeGetNext, LinkedList<T>());

         return list;
     }

     List<int> filterIndex(bool Function(Node<T>) condition) {
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

     Iterator<T> get iterator {
         return LinkedListIterator<T>(this.beginNode);
     }
 }

/* -------------------- lib: Game/GameClient --------------------
 *
 */
class GameClient {
    Socket client;
    String address;
    int port;
    int id;
    bool outputEnabled;
    Map<String, dynamic> Function(String, Map<String, dynamic>) onMessage;
    int baseDataLength;

    GameClient(Socket client, int id, Map<String, dynamic> Function(String, Map<String, dynamic>) onMessage, {bool outputEnabled=false, int baseDataLength=1024}) {
        this.client = client;
        this.address = this.client.remoteAddress.address;
        this.port = this.client.remotePort;
        this.id = id;

        this.outputEnabled = outputEnabled;

        this.baseDataLength = baseDataLength;
        this.onMessage = onMessage;

        this.client.listen(this.listen);

        this.output('Connection from ${this.address}:${this.port}');
    }

    void output(String text) {
        if (this.outputEnabled) {
            print('(${this.address}:${this.port} ${this.id}) ${text}');
        }
    }

    void listen(List<int> dataX) {
        String datasUnsplitted = String.fromCharCodes(dataX).trim();
        List<String> datas = datasUnsplitted.split('_');

        for (String data in datas) {
            if (data.length > 0) {
                this.onData(data);
            }
        }
    }

    void onData(String data) {
        Map<String, dynamic> message = json.decode(data);

        String title = message['title'];

        if (title == 'beginCommunication') {
            this.begin(message['data']);
        } else if (title == 'endCommunication') {
            this.end(message['data']);
        } else if (this.onMessage != null) {
            this.sendData(this.onMessage(title, message['data']));
        }
    }

    void sendData(Map<String, dynamic> message) {
        String data = json.encode(message);

        int totalDataLength = data.length+1;
        int dataMult = totalDataLength~/this.baseDataLength;

        if (dataMult != totalDataLength/this.baseDataLength) {
            dataMult += 1;
        }

        data = '${dataMult}'+data;

        this.client.write(data);
    }

    void begin(Map<String, dynamic> message) {
        this.output('Begin');

        Map<String, dynamic> responseMessage = {
            'id': this.id,
        };

        this.sendData(responseMessage);
    }

    void end(Map<String, dynamic> message) {
        this.output('End');

        Map<String, dynamic> responseMessage = {
        };

        this.sendData(responseMessage);

        this.client.close();
    }
}

/* -------------------- lib: Game/Mainloop --------------------
 *
 */
class Mainloop {
    Duration delay;
    List<void Function()> Function() getUpdateFuncs;

    Mainloop(this.delay, this.getUpdateFuncs);

    void start() {
        Timer.periodic(this.delay, this.loop);
    }

    void loop(Timer timer) {
        for (void Function() updateFunc in this.getUpdateFuncs()) {
            updateFunc();
        }
    }
}

/* -------------------- Player --------------------
 *
 */
class Player {
    int id;
    String name;

    Snake snake;
    bool playing;
    Map<String, dynamic> sendInfo;
    Game game;

    Player(this.id, this.name, this.game) {
        this.playing = false;
        this.resetSendInfo();
    }

    void startPlaying() {
        Tuple2<int, int> pos = game.findFreeBlock();
        int x = pos.item1;
        int y = pos.item2;

        this.snake = Snake(x, y, this);

        this.playing = true;
    }

    void endPlaying() {
        this.playing = false;
        this.snake = null;
    }

    Map<String, dynamic> toMap(int playerId) {
        Map<String, dynamic> data = {
            'id': this.id,
            'name': this.name,
            'playing': this.playing,
            'isPlayer': (playerId == this.id),
        };
        if (this.playing) {
            data['snake'] = this.snake.toMap();
        }

        return data;
    }

    void update() {
        this.snake.update();
    }

    void eliminate(Player player) {
        this.sendInfo['elimination'] = true;

        Map<String, dynamic> eliminationMap = {
            'playerName': player.name,
        };

        this.sendInfo['eliminationInfo'] = eliminationMap;
    }

    void dead(SnakeEliminator eliminator) {
        this.sendInfo['dead'] = true;

        Map<String, dynamic> deadMap = eliminator.toMap();
        this.sendInfo['deadInfo'] = deadMap;

        this.endPlaying();
    }

    void resetSendInfo() {
        this.sendInfo = {
            'dead': false,
            'elimination': false,
        };
    }

    Map<String, dynamic> sendInfoMap() {
        return Map.from(this.sendInfo);
    }
}

class PlayerList extends LinkedList<Player> {
    PlayerList() {
    }

    Player getById(int id) {
        return this.filter((Node<Player> node) {return node.value.id == id;}).get(0);
    }

    Player popById(int id) {
        int removeIndex = this.filterIndex((Node<Player> node) {return node.value.id == id;})[0];

        return this.pop(removeIndex);
    }

    List<Map<String, dynamic>> toMap(int playerId) {
        return this.map((Player player) {return player.toMap(playerId);}).toList();
    }

    LinkedList<Player> getPlaying() {
        return this.filter((Node<Player> node) {return node.value.playing;});
    }
}

/* -------------------- Snake --------------------
 *
 */
class SnakeBlock {
    int x;
    int y;
    bool isHead;

    SnakeBlock(this.x, this.y, this.isHead);

    Map<String, dynamic> toMap() {
        Map<String, dynamic> data = {
            'x': this.x,
            'y': this.y,
            'isHead': this.isHead,
        };

        return data;
    }
}

enum SnakeStyle {
    style1,
}

class SnakeEliminator {
    String type;
    Player player;

    SnakeEliminator(this.type, {this.player: null});

    Map<String, dynamic> toMap() {
        Map<String, dynamic> data = {
            'type': this.type,
        };
        if (this.player != null) {
            data['playerName'] = this.player.name;
        }

        return data;
    }
}

class Snake {
    LinkedList<SnakeBlock> blocks;
    int length;
    int velX;
    int velY;
    bool velChanged;

    SnakeStyle style;

    Player player;

    Snake(int x, int y, this.player) {
        this.blocks = LinkedList<SnakeBlock>();
        this.blocks.addToBegin(SnakeBlock(x, y, true));
        this.length = 5;
        this.velX = 1;
        this.velY = 0;
        this.velChanged = false;

        this.style = SnakeStyle.style1;
    }

    void update() {
        SnakeBlock pos = this.blocks.get(0);
        int newX = pos.x+this.velX;
        int newY = pos.y+this.velY;

        if (this.player.game.blockIsSnake(newX, newY)) {
            Player eliminator;
            for (Player player in  this.player.game.players.getPlaying()) {
                if (player.snake.isBlock(newX, newY)) {
                    eliminator = player;
                }
            }

            eliminator.eliminate(this.player);
            this.player.dead(SnakeEliminator('snake', player: eliminator));
        } else if (this.player.game.blockIsMaze(newX, newY)) {
            this.player.dead(SnakeEliminator('maze'));
        } else {
            pos.isHead = false;
            SnakeBlock newPos = SnakeBlock(newX, newY, true);

            this.blocks.addToBegin(newPos);

            if (this.blocks.getLength() > this.length) {
                this.blocks.popFromEnd();
            }

            this.velChanged = false;
        }
    }

    void changeVel(int newVelX, int newVelY) {
        if (!this.velChanged) {
            if (((newVelX+newVelY).abs() == 1) && !(newVelX == -this.velX && newVelY == -this.velY)) {
                this.velX = newVelX;
                this.velY = newVelY;
                this.velChanged = true;
            }
        }
    }

    bool isBlock(int x, int y) {
        bool isBlock = false;
        for (SnakeBlock block in this.blocks) {
            if (block.x == x && block.y == y) {
                isBlock = true;
            }
        }

        return isBlock;
    }

    Map<String, dynamic> toMap() {
        List<Map<String, dynamic>> blocksMap = this.blocks.map<Map<String, dynamic>>((SnakeBlock block) {return block.toMap();}).toList();

        Map<String, dynamic> data = {
            'blocks': blocksMap,
            'style': this.style.toString().split('.').last,
        };

        return data;
    }
}

/* -------------------- Map+Maze --------------------
 *
 */
class MazeBlock {
    int x;
    int y;

    MazeBlock(this.x, this.y);

    Map<String, dynamic> toMap() {
        Map<String, dynamic> data = {
            'x': x,
            'y': y,
        };

        return data;
    }
}

class Maze {
    List<MazeBlock> blocks;

    Maze() {
        this.blocks = List<MazeBlock>();
    }

    void addBlock(int x, int y) {
        this.blocks.add(MazeBlock(x, y));
    }

    bool isBlock(int x, int y) {
        bool isBlock = false;
        for (MazeBlock block in this.blocks) {
            if (block.x == x && block.y == y) {
                isBlock = true;
            }
        }

        return isBlock;
    }

    Map<String, dynamic> toMap() {
        List<Map<String, dynamic>> blocksMap = [];

        for (MazeBlock block in this.blocks) {
            blocksMap.add(block.toMap());
        }

        Map<String, dynamic> data = {
            'blocks': blocksMap,
        };

        return data;
    }
}

class GameMap {
    int xSize;
    int ySize;

    Maze maze;

    GameMap(this.xSize, this.ySize) {
        this.maze = Maze();
    }

    void addBlock(int x, int y) {
        this.maze.addBlock(x, y);
    }

    void createBorder() {
        for (int x=0; x<this.xSize; x++) {
            this.maze.addBlock(x, 0);
        }
        for (int x=0; x<this.xSize; x++) {
            this.maze.addBlock(x, this.ySize-1);
        }
        for (int y=0; y<this.ySize; y++) {
            this.maze.addBlock(0, y);
        }
        for (int y=0; y<this.ySize; y++) {
            this.maze.addBlock(this.xSize-1, y);
        }
    }

    Map<String, dynamic> toMap() {
        Map<String, dynamic> data = {
            'xSize': this.xSize,
            'ySize': this.ySize,
            'maze': this.maze.toMap(),
        };

        return data;
    }
}

/* -------------------- Game --------------------
 *
 */
class Game {
    ServerSocket server;
    PlayerList players;
    int nextPlayerId;
    GameMap gameMap;
    Mainloop playersUpdateMainloop;

    Game(this.server, int xSize, int ySize) {
        this.gameMap = GameMap(xSize, ySize);
        this.gameMap.createBorder();

        this.players = PlayerList();
        this.nextPlayerId = 0;

        this.playersUpdateMainloop = Mainloop(Duration(milliseconds: 200), this.getPlayersUpdateFunc);
        this.playersUpdateMainloop.start();

        this.server.listen(this.newClient);
    }

    bool blockIsSnake(int x, int y) {
        bool isSnakeBlock = false;
        for (Player player in this.players.getPlaying()) {
            if (player.snake.isBlock(x, y)) {
                isSnakeBlock = true;
            }
        }

        return isSnakeBlock;
    }

    bool blockIsMaze(int x, int y) {
        return this.gameMap.maze.isBlock(x, y);
    }

    Tuple2<int, int> findFreeBlock() {
        bool found = false;

        int x;
        int y;

        while (!found) {
            x = Random().nextInt(this.gameMap.xSize);
            y = Random().nextInt(this.gameMap.ySize);

            found = (!this.blockIsSnake(x, y)) && (!this.blockIsMaze(x, y));
        }

        return Tuple2<int, int>(x, y);
    }

    List<void Function()> getPlayersUpdateFunc() {
        List<void Function()> playersUpadateFuncs = this.players.getPlaying().map((Player player) {return player.update;}).toList();

        return playersUpadateFuncs;
    }

    void newClient(Socket client) {
        int playerId = this.nextPlayerId;

        Map<String, dynamic> gameClientOnMessage(String title, Map<String, dynamic> message) {
            if (title == 'initInfo') {
                Map<String, dynamic> responseMessage = {
                    'error': {},
                    'gameMap': this.gameMap.toMap(),
                };

                return responseMessage;
            } else if (title == 'addPlayer') {
                Player player = Player(playerId, message['name'], this);
                this.players.add(player);

                Map<String, dynamic> responseMessage = {
                    'player': player.toMap(playerId)
                };

                return responseMessage;
            } else if (title == 'startPlaying') {
                Player player = this.players.getById(playerId);

                player.startPlaying();

                return {};
            } else if (title == 'endPlaying') {
                Player player = this.players.getById(playerId);

                player.endPlaying();

                return {};
            } else if (title == 'loop') {
                Map<String, dynamic> responseMessage = {
                    'players': this.players.toMap(playerId),
                };

                return responseMessage;
            } else if (title == 'loopInfo') {
                Player player = this.players.getById(playerId);

                Map<String, dynamic> responseMessage = player.sendInfoMap();
                player.resetSendInfo();

                return responseMessage;
            } else if (title == 'spectate') {
                Map<String, dynamic> responseMessage = {
                    'players': this.players.toMap(null),
                };

                return responseMessage;
            } else if (title == 'changeVel') {
                int newVelX = message['vel']['x'];
                int newVelY = message['vel']['y'];

                Player player = this.players.getById(playerId);

                if (player.playing) {
                    player.snake.changeVel(newVelX, newVelY);
                }

                Map<String, dynamic> responseMessage = {
                };

                return responseMessage;
            } else if (title == 'end') {
                this.players.popById(playerId);

                Map<String, dynamic> responseMessage = {
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

/* -------------------- main -------------------- */
void test() {
    LinkedList<int> linkedList = LinkedList<int>();

    // print(linkedList.toList());

    linkedList.add(1);
    linkedList.add(2);
    linkedList.add(3);
    linkedList.add(5);

    // print(linkedList.pop(0));
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
        '192.168.1.6',
        4042,
    );

    Game(server, 25, 25);
}
