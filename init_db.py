import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO products (name, description, image, price) VALUES (?, ?, ?, ?)",
            ('SAMSUNG Galaxy S23 5G (Lavender, 256 GB)  (8 GB RAM)', 'Give yourself a smartphone that recognises your emotions and responds appropriately. The Samsung Galaxy S23 5G\'s enhanced AI and Nightography feature produces low-light photos and videos that are vivid and colourful from dusk to dawn and back again. The Snapdragon processor in this phone also offers quick video streaming and gaming. Additionally, adaptive 120 Hz makes scrolling fluid, and Eye Comfort Shield guards against eye fatigue even while looking in low light.', 'S23', 79999)
            )

cur.execute("INSERT INTO products (name, description, image, price) VALUES (?, ?, ?, ?)",
            ('Google Pixel 7a (Sea, 128 GB)  (8 GB RAM)', 'Experience the simplicity and seamless transitions with the Google Pixel 7a, which is loaded with a variety of incredible features. The Tensor G2 processor, designed by Google, boosts the Pixel 7a\'s speed, effectiveness, and security. It\'s the same chip that\'s in Pixel 7 and Pixel 7 Pro. Furthermore, With a dual rear camera system and Google Tensor G2\'s advanced image processing, Pixel 7a lets you create perfect photos every time. It\'s easy to take amazing pictures in low light, or fix your blurry photos and remove distractions with a few taps in Google Photos. Moreover, the Pixel 7a camera includes Super Res Zoom, so that you can get up close without an extra telephoto lens.', 'pixel', 35999)
            )

cur.execute("INSERT INTO products (name, description, image, price) VALUES (?, ?, ?, ?)",
            ('OnePlus 11 5G (Eternal Green, 256 GB)  (16 GB RAM)',
             'The OnePlus 11 5G flagship combines power with effortless elegance. Driven by the most extreme hardware in OnePlus history, dial every possibility up to 11. The OnePlus 11 5G is the Shape of Power.', 'oneplus11', 61999)
            )

cur.execute("INSERT INTO products (name, description, image, price) VALUES (?, ?, ?, ?)",
            ('MOTOROLA Razr (Black, 128 GB)  (6 GB RAM)', 'The Motorola Razr is here to redefine your smartphone experience with its sleek and stylish foldable display. Featuring the zero-gap hinge design, you can flip open this phone to view your favourite visuals on the main 15.75 cm (6.2) 21:9 CinemaVision display. That\’s not all, this smartphone features different camera modes and AI-based features to help you click stunning images that everyone will be in awe of.', 'razr', 149999)
            )

cur.execute("INSERT INTO products (name, description, image, price) VALUES (?, ?, ?, ?)", ('APPLE iPhone 15 Plus (Black, 128 GB)', 'Experience the iPhone 15 Plus – your dynamic companion. Dynamic Island ensures you stay connected, bubbling up alerts seamlessly while you\'re busy. Its durable design features infused glass and aerospace-grade aluminum, making it dependable and resistant to water and dust. Capture life with precision using the 48 MP Main Camera, perfect for any shot. Powered by the A16 Bionic Processor, it excels in computational photography and more, all while conserving battery life. Plus, it\'s USB-C compatible, simplifying your charging needs. Elevate your tech game with the iPhone 15 Plus – innovation at your fingertips. Goodbye cable clutter, hello convenience.', 'iphone', 89900))

connection.commit()
connection.close()
