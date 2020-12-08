# list of all items in the room
r1=[
    {
        "name": "bacon",
        "interaction": "password",
        "status": False,
        "require": None,
        "timed": True
    },
    {
        "name": "flour",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "raw eggs",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "G",
        "interaction": "see",
        "status": False,
        "require": None,
        "timed": True
    },
    {
        "name": "Em",
        "interaction": "see",
        "status": False,
        "require": None,
        "timed": True
    },
    {
        "name": "C",
        "interaction": "see",
        "status": False,
        "require": None,
        "timed": True
    },
    {
        "name": "D7",
        "interaction": "see",
        "status": False,
        "require": None,
        "timed": True
    },
    {
        "name": "pan",
        "interaction": "combine",
        "status": False,
        "require": ["flour", "raw eggs"],
        "timed": False
    }
]
r2 =[
    {
        "name": "cake mix",
        "interaction": "password",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "chocolate frosting",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "vanilla frosting",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "shelve",
        "interaction": "remove",
        "status": False,
        "require": None,
        "timed": False
    }
]
r3 =[
    {
        "name": "cow",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "centrifuge",
        "interaction": "combine",
        "status": False,
        "require": ["cow"],
        "timed": False
    },
    {
        "name": "lettuce",
        "interaction": "game",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "jellyfish",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "red balloon",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "mixer",
        "interaction": "combine",
        "status": False,
        "require": ["jellyfish", "red balloon"],
        "timed": False
    },
    {
        "name": "bread",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    }
]
r4 =[
    {
        "name": "apple",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "marker",
        "interaction": "password",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "book",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "bed",
        "interaction": "remove",
        "status": False,
        "require": None,
        "timed": False
    },
    {
        "name": "bass",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False
    }
]

r1AllItems = {"bacon", "pancakes", "eggs"}
r2AllItems = {"cake", "chocolate frosting", "vanilla frosting"}
r3AllItems = {"cheese", "lettuce", "tomato", "bread"}
r4AllItems = {"apple", "marker", "book", "bass"}

roomAllItems = [r1AllItems, r2AllItems, r3AllItems, r4AllItems]
roomProperties = [r1, r2, r3, r4]   
roomNames = ["JAKE", "FINN", "PRINCESS BUBBLEGUM", "MARCELINE"] 
roomColors = ["#a14b00", "#00a6ff", "#ffb04f", "#696d70"]

riddles =[
            {
                "Q": "What vegetable is the most fun to be around and the one that everybody wants to hang out with?",
                "A": "fungi"
            },
            {
                "Q": "What is the wealthiest nut?",
                "A": "cashew"
            },
            {
                "Q": "What did the doctor prescribe to the sick lemon?",
                "A": "lemonade"
            },
            {
                "Q": "What fruit never ever wants to be alone?",
                "A": "pear"
            },
            {
                "Q": "What food loves to yell and shout?",
                "A": "ice cream"
            },
            {
                "Q": "What kind of room can you eat?",
                "A": "mushroom"
            }
        ]

r1Question = "Sing the bacon pancake song! (connect with ',')"
r1Answer = "G,Em,C,D7"

riddleAddItem = ["bacon", "cake", "", "marker"]