/*
 * TODO: errors
 * TODO: player manager
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

class LinkedList<T> with IterableMixin<T> {
    Node<T> beginNode;
    Node<T> endNode;

    LinkedList();

    LinkedList.from(Iterable<T> fromIterable) {
        this.addAll(fromIterable);
    }

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

    void add(T value) {
         this.addToEnd(value);
    }

	void addAll(Iterable items) {
		for (T item in items) {
            this.addToEnd(item);
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
             Node<T> tempNode = this.beginNode;
             for (int index = 0; index < getIndex; index++) {
                 tempNode = tempNode.next;
             }

             return tempNode.value;
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
         int length = 0;
         for (T _ in this) {
             length++;
         }

         return length;
     }

     LinkedList<newT> map<newT>(newT Function(T) mapFunction) {
         LinkedList<newT> mappedLinkedList = LinkedList<newT>();
         for (T item in this) {
             mappedLinkedList.add(mapFunction(item));
         }

         return mappedLinkedList;
     }

     LinkedList<T> where(bool Function(T) condition) {
         LinkedList<T> wheredLinkedList = LinkedList<T>();
         for (T item in this) {
             if (condition(item)) {
                 wheredLinkedList.add(item);
             }
         }

         return wheredLinkedList;
     }

     LinkedList<int> whereIndex(bool Function(T) condition) {
         LinkedList<int> whereIndexdLinkedList = LinkedList<int>();
         int index = 0;
         for (T item in this) {
             if (condition(item)) {
                 whereIndexdLinkedList.add(index);
             }
             index++;
         }

         return whereIndexdLinkedList;
     }

     Iterator<T> get iterator {
         return LinkedListIterator<T>(this.beginNode);
     }

     String toString() {
         String items = this.toList().join(', ');
         return 'LinkedList<${T.toString()}> [${items}]';
     }

	T operator [](int getIndex) {
		return this.get(getIndex);
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
	int baseDataLengthMaxMultiplayerDigits;

    GameClient(Socket client, int id, Map<String, dynamic> Function(String, Map<String, dynamic>) onMessage, {bool outputEnabled=false, int baseDataLength=1024, this.baseDataLengthMaxMultiplayerDigits=3}) {
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

		String dataMultString = dataMult.toString().padLeft(this.baseDataLengthMaxMultiplayerDigits, '0');

		if (dataMultString.length <= this.baseDataLengthMaxMultiplayerDigits) {
			data = '${dataMultString}'+data;

	        this.client.add(utf8.encode(data));
		} else {
			this.output('Message sending failed (Too long message)');
		}
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
        return this.where((Player player) {return player.id == id;})[0];
    }

    Player popById(int id) {
        int removeIndex = this.whereIndex((Player player) {return player.id == id;})[0];

        return this.pop(removeIndex);
    }

    List<Map<String, dynamic>> toMap(int playerId) {
        return this.map((Player player) {return player.toMap(playerId);}).toList();
    }

    LinkedList<Player> getPlaying() {
        return this.where((Player player) {return player.playing;});
    }
}

/* -------------------- Style --------------------
 *
 */

class Style {
	String name;

	Style() {
		this.name = '';
	}

	void update() {
	}

	Map<String, dynamic> getDetailsMap() {
		Map<String, dynamic> details = {
		};

		return details;
	}

	Map<String, dynamic> toMap() {
		Map<String, dynamic> data = {
			'name': this.name,
			'details': this.getDetailsMap(),
		};

		return data;
	}
}

class StyleSnakeDefault extends Style {
	StyleSnakeDefault() {
		this.name = 'default';
	}
}

class StyleSnakeRainbow extends Style {
	int phase;

	StyleSnakeRainbow() {
		this.name = 'rainbow';

		this.phase = 0;
	}

	void update() {
		this.phase += 1;

		if (this.phase >= 7) {
			this.phase = 0;
		}
	}

	Map<String, dynamic> getDetailsMap() {
		Map<String, dynamic> details = {
			'phase': this.phase,
		};

		return details;
	}
}

class StyleBoostFood extends Style {
	StyleBoostFood() {
		this.name = 'food';
	}
}

class StyleBoostLgbt extends Style {
	StyleBoostLgbt() {
		this.name = 'lgbt';
	}
}

class StyleMazeDefault extends Style {
	StyleMazeDefault() {
		this.name = 'default';
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

    Style defaultStyle;
	LinkedList<BoostPostEffect> boostPostEffectsStack;

    Player player;

    Snake(int x, int y, this.player) {
        this.blocks = LinkedList<SnakeBlock>();
        this.blocks.addToBegin(SnakeBlock(x, y, true));
        this.length = 5;

        this.velX = 1;
        this.velY = 0;
        this.velChanged = false;

        this.defaultStyle = StyleSnakeDefault();
		this.boostPostEffectsStack = LinkedList<BoostPostEffect>();
    }

    void update() {
        SnakeBlock pos = this.blocks[0];
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
			Boost boost = this.player.game.blockGetBoost(newX, newY);
			if (boost != null) {
				boost.eat(this);

				if (boost.boostType.boosPostEffectFactory != null) {
					this.boostPostEffectsStack.addToBegin(boost.boostType.boosPostEffectFactory(this));
				}
			}

            pos.isHead = false;
            SnakeBlock newPos = SnakeBlock(newX, newY, true);

            this.blocks.addToBegin(newPos);

            if (this.blocks.getLength() > this.length) {
                this.blocks.popFromEnd();
            }

			LinkedList<BoostPostEffect> newBoostPostEffectsStack = LinkedList<BoostPostEffect>();
			for (BoostPostEffect boostPostEffect in this.boostPostEffectsStack) {
				if (!boostPostEffect.end()) {
					boostPostEffect.update();
					newBoostPostEffectsStack.addToEnd(boostPostEffect);
				}
			}

			this.boostPostEffectsStack = newBoostPostEffectsStack;

			this.getActiveStyle().update();

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

	Style getActiveStyle() {
		Style style = null;

		for (BoostPostEffect boostPostEffect in this.boostPostEffectsStack) {
			if (boostPostEffect.style != null) {
				style = boostPostEffect.style;

				break;
			}
		}

		if (style == null) {
			style = this.defaultStyle;
		}

		return style;
	}

    Map<String, dynamic> toMap() {
        List<Map<String, dynamic>> blocksMap = this.blocks.map<Map<String, dynamic>>((SnakeBlock block) {return block.toMap();}).toList();

        Map<String, dynamic> data = {
            'blocks': blocksMap,
            'style': this.getActiveStyle().toMap(),
        };

        return data;
    }
}

/* -------------------- Boost --------------------
 *
 */

class BoostManager {
	LinkedList<BoostGroup> boostGroups;
	Game game;

	BoostManager(this.boostGroups, this.game) {
	}

	void update() {
		for (BoostGroup boostGroup in this.boostGroups) {
			boostGroup.update();

			BoostType newBoostType = boostGroup.getNewBoost();

			if (newBoostType != null) {
				Tuple2<int, int> pos = this.game.findFreeBlock();
				int x = pos.item1;
				int y = pos.item2;
				Boost newBoost = Boost(x, y, newBoostType);

				boostGroup.addBoost(newBoost);
			}
		}
	}

	List<Map<String, dynamic>> toMap() {
		List<Map<String, dynamic>> boostsMap = this.getBoosts().map((Boost boost) {return boost.toMap();}).toList();

		return boostsMap;
	}

	LinkedList<Boost> getBoosts() {
		LinkedList<Boost> boosts = LinkedList<Boost>();

		for (BoostGroup boostGroup in this.boostGroups) {
			boosts.addAll(boostGroup.boosts);
		}

		return boosts;
	}

	Boost getBoost(int x, int y) {
		Boost boost = this.getBoosts().fold(null, (Boost foundBoost, Boost boost) {
			if (boost.x == x && boost.y == y) {
				return boost;
			} else {
				return foundBoost;
			}
		});

		return boost;
	}
}

class BoostGroup {
	LinkedList<BoostType> boostTypes;
	int spawnChance;
	int spawnMaxChance;
	int maxCount;

	LinkedList<Boost> boosts;

	BoostGroup(this.spawnChance, this.spawnMaxChance, this.maxCount) {
		this.boostTypes = LinkedList<BoostType>();
		this.boosts = LinkedList<Boost>();
	}

	addBoostType(BoostType boostType) {
		this.boostTypes.add(boostType);
	}

	addBoost(Boost boost) {
		this.boosts.add(boost);
	}

	BoostType getNewBoost() {
		bool spawn = false;

		if (this.boosts.getLength() < this.maxCount) {
			int spawnRandom = Random().nextInt(this.spawnMaxChance)+1;

			if (spawnRandom <= this.spawnChance) {
				spawn = true;
			}
		}

		if (spawn) {
			int boostTypeIndex = Random().nextInt(this.boostTypes.length);

			return this.boostTypes[boostTypeIndex];
		} else {
			return null;
		}
	}

	void update() {
		for (Boost boost in this.boosts) {
			boost.update();
		}

		this.boosts = this.boosts.where((Boost boost) {return boost.lifetime > 0;});
	}
}

class BoostType {
	Style Function() styleFactory;
	BoostPostEffect Function(Snake)  boosPostEffectFactory;

	void Function(Snake) onEat;
	int lifetime;
	bool limitedLifetime;

	BoostType(this.styleFactory, this.onEat, this.lifetime, [this.boosPostEffectFactory=null]) {
		this.limitedLifetime = this.lifetime != null;
	}
}

class Boost {
	int x;
	int y;

	BoostType boostType;
	int lifetime;

	Style style;

	Boost(this.x, this.y, this.boostType) {
		if (this.boostType.limitedLifetime) {
			this.lifetime = this.boostType.lifetime;
		} else {
			this.lifetime = 1;
		}

		this.style = this.boostType.styleFactory();
	}

	void update() {
		if (this.boostType.limitedLifetime) {
			this.lifetime--;
		}

		this.style.update();
	}

	void eat(Snake snake) {
		this.boostType.onEat(snake);
		this.lifetime = 0;
	}

	Map<String, dynamic> toMap() {
		Map<String, dynamic> data = {
			'style': this.style.toMap(),
			'x': this.x,
			'y': this.y,
		};

		return data;
	}
}

/* -------------------- BoostPostEffect --------------------
 *
 */

class BoostPostEffect {
	Style style;

	BoostPostEffect(Snake snake) {
	}

	void update() {
		if (this.style != null) {
			this.style.update();
		}
	}

	bool end() {
		return true;
	}
}

class BoostPostEffectLgbt extends BoostPostEffect {
	int lifetime;

	BoostPostEffectLgbt(Snake snake):super(snake) {
		this.style = StyleSnakeRainbow();
		this.lifetime = 15;
	}

	void update() {
		super.update();

		this.lifetime--;
	}

	bool end() {
		return this.lifetime <= 0;
	}
}

/* -------------------- Map+Maze --------------------
 *
 */
class MazeBlock {
    int x;
    int y;

	Style style;

	MazeBlock(this.x, this.y) {
		this.style = StyleMazeDefault();
	}

    Map<String, dynamic> toMap() {
        Map<String, dynamic> data = {
			'style': this.style.toMap(),
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

	BoostManager boostManager;

    Mainloop playersUpdateMainloop;

    Game(this.server, int xSize, int ySize) {
        this.gameMap = GameMap(xSize, ySize);
        this.gameMap.createBorder();

		LinkedList<BoostGroup> boostGroups = LinkedList<BoostGroup>();

		BoostGroup boostGroup1 = BoostGroup(10, 10, 1);
		boostGroup1.addBoostType(BoostType(() {return StyleBoostFood();}, (Snake snake) {snake.length++;}, null));

		BoostGroup boostGroup2 = BoostGroup(100, 100, 1);
		boostGroup2.addBoostType(BoostType(() {return StyleBoostLgbt();}, (Snake snake) {snake.length+=3;}, 50, (Snake snake) {return BoostPostEffectLgbt(snake);}));

		boostGroups.add(boostGroup1);
		boostGroups.add(boostGroup2);

		this.boostManager = BoostManager(boostGroups, this);

        this.players = PlayerList();
        this.nextPlayerId = 0;

        this.playersUpdateMainloop = Mainloop(Duration(milliseconds: 100), this.getUpdateFuncs);
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

	Boost blockGetBoost(int x, int y) {
		return this.boostManager.getBoost(x, y);
	}

    Tuple2<int, int> findFreeBlock() {
        bool found = false;

        int x;
        int y;

        while (!found) {
            x = Random().nextInt(this.gameMap.xSize);
            y = Random().nextInt(this.gameMap.ySize);

            found = (!this.blockIsSnake(x, y)) && (!this.blockIsMaze(x, y) && (this.blockGetBoost(x, y) == null));
        }

        return Tuple2<int, int>(x, y);
    }

	List<void Function()> getUpdateFuncs() {
		List<void Function()> playersUpdateFunc = this.players.getPlaying().map((Player player) {return player.update;}).toList();

		List<void Function()> updateFuncs = List<void Function()>();

		if (playersUpdateFunc.length > 0) {
	        updateFuncs.addAll(playersUpdateFunc);
			updateFuncs.add(this.boostManager.update);
		}

        return updateFuncs;
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

				Map<String, dynamic> responseMessage = {
					'error': {
					},
				};

				if (this.players.getPlaying().getLength() >= 2) {
					Map<String, dynamic> errorMessage = {
						'title': 'GameFull',
					};
					responseMessage['error'] = errorMessage;

					return responseMessage;
				} else {
					player.startPlaying();

	                return responseMessage;
				}
            } else if (title == 'endPlaying') {
                Player player = this.players.getById(playerId);

                player.endPlaying();

                return {};
            } else if (title == 'loop') {
                Map<String, dynamic> responseMessage = {
                    'players': this.players.toMap(playerId),
					'boosts': this.boostManager.toMap(),
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
					'boosts': this.boostManager.toMap(),
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
    //     print(linkedList[0]);
    //     print(linkedList.pop(0));
    // }

    // print(linkedList.toList());

    // print(linkedList.findIndex((Node<int> tempNode) {return tempNode.value%2 == 1;}));
}

Future main() async {
    // test();

    ServerSocket server = await ServerSocket.bind(
        '192.168.1.4',
        4042,
    );

    Game(server, 30, 30);
}
