# All asset images drawn by myself
bgURL = 'https://64.media.tumblr.com/41b660528784aacedfcb0472ac7091dd/881ddbaec1f23e43-a9/s1280x1920/7ddd9bc1bc4e35674ed06004ff22ad70e3218ee5.png'
playerURL = 'https://64.media.tumblr.com/e42df5e052e4111dec860975689f9f7f/881ddbaec1f23e43-1f/s75x75_c1/a06f400c047f5d7f91488af06fe85eac8edd3e90.png'

r1bg = 'https://64.media.tumblr.com/a28b2ece45642fcbc29b00f2b707ff21/881ddbaec1f23e43-15/s1280x1920/4acaed3ad8fc3c6d75205841809a4638a408e6bd.png' #jake
r2bg = 'https://64.media.tumblr.com/8fbf4a9bfc86b05c38411f156aff65ae/881ddbaec1f23e43-cc/s1280x1920/2a81327750aee48ad405aa67f73dc3037a75bf49.png' #finn
r3bg = 'https://64.media.tumblr.com/bfcdf12d0e92a729696432735bddbbc8/881ddbaec1f23e43-a4/s1280x1920/2db542740759716fecb25c6e195de6479606a5b7.png' #pb
r4bg = 'https://64.media.tumblr.com/48de68b599f2e7cc7d7d71a0b923ea00/881ddbaec1f23e43-c3/s1280x1920/ea3707db377643199a2f5642ad6b6fd3cc5fdd58.png' #marceline

roomBg = [r1bg, r2bg, r3bg, r4bg]
# list of all items in the room
r1=[
    {
        "name": "bacon",
        "interaction": "password",
        "status": False,
        "require": None,
        "timed": True,
        "position": (609, 279),
        "img": 'https://64.media.tumblr.com/12f386b282120db014c9f44102d0e068/881ddbaec1f23e43-07/s100x200/80f41c6a0b591510b771aef260e0ec95d64ed922.png'
    },
    {
        "name": "flour",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (480, 74),
        "img": 'https://64.media.tumblr.com/d35e463cfa40b24038c97ee8d960a4fc/881ddbaec1f23e43-ab/s100x200/9fb80a976fc492e9b187a73fb7d89877e772d712.png'
    },
    {
        "name": "eggs",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (594, 24),
        "img": 'https://64.media.tumblr.com/68ae859e8a903c6ba638254985824cf1/881ddbaec1f23e43-65/s100x200/7500fd948e9a0808108f6ea603834c70f10f03ee.png'
    },
    {
        "name": "G, Em, C, D7",
        "interaction": "see",
        "status": False,
        "require": None,
        "timed": False,
        "position": (238, 279),
        "img": ""
    },
    {
        "name": "pan",
        "interaction": "combine",
        "status": False,
        "require": ["flour", "eggs"],
        "timed": False,
        "position": (243, 179),
        "img": "https://64.media.tumblr.com/bda21dfc5bc796b68f22092c6b31ee2a/881ddbaec1f23e43-e4/s100x200/c93f4f2987525c7992a417869554500bff6502b8.png"
    }
]
r2 =[
    {
        "name": "cake mix",
        "interaction": "password",
        "status": False,
        "require": None,
        "timed": False,
        "position": (147, 343),
        "img": "https://64.media.tumblr.com/5c4defe505c902b687ef618cb18412ef/881ddbaec1f23e43-e4/s100x200/cdbc732bf24193cb01a984d5263a1e3282e0f7e6.png"
    },
    {
        "name": "chocolate frosting",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (640, 250),
        "img": "https://64.media.tumblr.com/03339c547cc45926319df1b5cc949ee4/881ddbaec1f23e43-81/s100x200/c2d0941a1237c502c2db57c7cb65cb87ecc80716.png"
    },
    {
        "name": "vanilla frosting",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (506, 355),
        "img": "https://64.media.tumblr.com/88d40c15063ee920058b96860d41fb6d/881ddbaec1f23e43-4c/s100x200/a77fa657910d2c3fffc0a8eb2f5ae2038247398c.png"
    }
]
r3 =[
    {
        "name": "cow",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (74, 350),
        "img": "https://64.media.tumblr.com/9385abf9b6545d1d5a8bc3dcfd8cfd0e/881ddbaec1f23e43-cc/s100x200/97789aee7f5327a86d2ee7b32cbd21ed34c9b922.png"
    },
    {
        "name": "lettuce",
        "interaction": "password",
        "status": False,
        "require": None,
        "timed": True,
        "position": (750, 305),
        "img": "https://64.media.tumblr.com/71ee7de9f845ef76da055dcc0d4fd980/881ddbaec1f23e43-e5/s100x200/7e25c330dfa41d6d541d3f65f8ea0706d33e6a39.png"
    },
    {
        "name": "jellyfish",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (710, 50),
        "img": "https://64.media.tumblr.com/0dda130eef4b82bcf8afe40a006d3961/881ddbaec1f23e43-c6/s100x200/d06f1d2d70f5994a227b17d7f8e962d86ecf97ba.png"
    },
    {
        "name": "red balloon",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (504, 266),
        "img": "https://64.media.tumblr.com/787c2824b2bfab04567df0e8b31cbf05/881ddbaec1f23e43-93/s100x200/411248d54fdeb83355f583f73e6c0269c086bdd5.png"
    },
    {
        "name": "mixer",
        "interaction": "combine",
        "status": False,
        "require": ["jellyfish", "red balloon"],
        "timed": False,
        "position": (417, 155),
        "img": "https://64.media.tumblr.com/eb7cf5a89133e84b6819a152480a2177/881ddbaec1f23e43-c3/s100x200/638fcd6c8dbf214771af19b28152f737f8154022.png"
    },
    {
        "name": "bread",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (715, 161),
        "img": "https://64.media.tumblr.com/c77fa40916cf8c6a4a52e483052e4266/881ddbaec1f23e43-ef/s100x200/0f6679cbcebaed0ab6accff9edecb8a9d28f46eb.png"
    }
]
r4 =[
    {
        "name": "apple",
        "interaction": "password",
        "status": False,
        "require": None,
        "timed": True,
        "position": (525, 215),
        "img": "https://64.media.tumblr.com/6496ace4d8f821b855aac8efb77e44b3/881ddbaec1f23e43-d3/s100x200/b803464dba839aa03f4e34c70d5e9ceb19cc2fe2.png"
    },
    {
        "name": "marker",
        "interaction": "remove",
        "status": False,
        "require": None,
        "timed": True,
        "position": (54, 300),
        "img": "https://64.media.tumblr.com/5e2fe6bebf1febe92dc26f5ae8b24b7a/881ddbaec1f23e43-d9/s100x200/c2d8f4179b0503871527086b07787907b85d757f.png"
    },
    {
        "name": "book",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (297, 227),
        "img": "https://64.media.tumblr.com/83f09c47021404550681d193d0da2556/881ddbaec1f23e43-ec/s100x200/c5688bbb6fc927f055e75313b52f5bc450bf98c9.png"
    },
    {
        "name": "lamp",
        "interaction": "remove",
        "status": False,
        "require": None,
        "timed": False,
        "position": (642, 327),
        "img": "https://64.media.tumblr.com/edd42bbdc88cd70c36e2139c90b1c4e8/881ddbaec1f23e43-21/s100x200/f2b8f8bc3a122405a1423ade252e4bbb1990c51b.png"
    },
    {
        "name": "frame",
        "interaction": "add",
        "status": False,
        "require": None,
        "timed": False,
        "position": (378, 339),
        "img": "https://64.media.tumblr.com/e4e5ed6e3f8ab44665708e9f2da0d723/881ddbaec1f23e43-ee/s100x200/3cd2b959f5d8de90aa277291f1c64dcdfebbb58f.png"
    }
]

r1AllItems = {"bacon", "flour", "eggs"}
r2AllItems = {"cake", "chocolate frosting", "vanilla frosting"}
r3AllItems = {"cheese", "lettuce", "jellyfish", "red balloon", "bread"}
r4AllItems = {"apple", "marker", "book", "frame"}

roomAllItems = [r1AllItems, r2AllItems, r3AllItems, r4AllItems]
roomProperties = [r1, r2, r3, r4]   
roomNames = ["JAKE'S BACON PANCAKE", "FINN'S FINN CAKE", "PRINCESS BUBBLEGUM'S PERFECT SANDWICH", "MARCELINE'S RED THINGS"] 
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